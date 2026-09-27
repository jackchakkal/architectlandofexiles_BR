#!/usr/bin/env python3
"""Gera um snapshot novo a partir de um snapshot base + overrides.json.

Formato do overrides.json:
  {"Tabela.csv": {"ID": "novo valor", "ID2": {"Coluna": "novo valor"}},   # por ID: valor simples = 2ª coluna; dict = colunas específicas
   "__by_text__": {"Tabela.csv": {"Coluna": {"texto em inglês": "texto PT-BR"}}},  # por texto exato, em qualquer coluna
   "__literal_brackets__": ["<Faction>[Hunter]</>"],   # textos em que [..] é literal (confirmado por outra cultura), não placeholder
   "__restore_exact_names__": {"sources": [["Skill_Name.csv","Name"]], "columns": ["Name","Title"]},
       # toda célula (nas colunas listadas, em qualquer tabela) cujo ORIGINAL em inglês é exatamente um dos nomes das fontes volta ao inglês
   "__replace_translated_names__": {"sources": [["Skill_Name.csv","Name"]]}}
       # em qualquer célula, ocorrências da tradução (base) de um nome-fonte são trocadas pelo nome em inglês (mapa PT->EN vem do snapshot base)
A substituição por texto se aplica a toda célula cujo inglês original é exatamente o texto-chave (traduzida ou não).

Uso:
  python tools/apply_overrides.py --base translations/v12-corrections --overrides changes/v12-to-v13/overrides.json \
      --source ../work/download-pak0-original --out translations/v13

Regras: só a coluna de valor (segunda coluna) é alterada; IDs, cabeçalhos, ordem, BOM e CRLF são preservados.
A validação compara placeholders ([X], {X}) e tags (<X>, </>) do novo valor com o texto-fonte em inglês e falha se divergirem.
"""
import argparse, csv, io, json, os, re, shutil, sys
L10N='ProjectTT/Content/TT/Data/CSV/L10N/en'
TOK=re.compile(r'\[[^\]\r\n]+\]|\{[^}\r\n]+\}|</?[A-Za-z][^>]*>|</>')
TOK_NOBRACKET=re.compile(r'\{[^}\r\n]+\}|</?[A-Za-z][^>]*>|</>')  # para textos em __literal_brackets__ (colchetes são texto, não placeholder)
def read(p):
    with open(p,'rb') as f: raw=f.read()
    assert raw.startswith(b'\xef\xbb\xbf'), f'{p}: sem BOM'
    text=raw[3:].decode('utf-8')
    return list(csv.reader(io.StringIO(text,newline='')))
def write(p,rows):
    buf=io.StringIO(newline='')
    csv.writer(buf,lineterminator='\r\n').writerows(rows)
    with open(p,'wb') as f: f.write(b'\xef\xbb\xbf'+buf.getvalue().encode('utf-8'))
def main():
    a=argparse.ArgumentParser(); a.add_argument('--base',required=True); a.add_argument('--overrides',required=True)
    a.add_argument('--source',required=True,help='raiz da extração original em inglês'); a.add_argument('--out',required=True)
    a.add_argument('--report'); a.add_argument('--allow-existing',action='store_true')
    o=a.parse_args()
    ov=json.load(open(o.overrides,encoding='utf-8')); ov.pop('_comment',None); bytext=ov.pop('__by_text__',{}); literal=set(ov.pop('__literal_brackets__',[])); rex=ov.pop('__restore_exact_names__',None); rtn=ov.pop('__replace_translated_names__',None)
    def load_col(root,fn,colname):
        rows=read(os.path.join(root,L10N,fn)); ci=rows[0].index(colname); return {r[0]:r[ci] for r in rows[1:] if r and ci<len(r)}
    exact_names=set(); name_map={}
    for fn,colname in (rex or {}).get('sources',[]):
        exact_names|={v.strip() for v in load_col(o.source,fn,colname).values() if v.strip()}
    for fn,colname in (rtn or {}).get('sources',[]):
        en_c=load_col(o.source,fn,colname); pt_c=load_col(o.base,fn,colname)
        for k,ev in en_c.items():
            pv=pt_c.get(k,'')
            if ev.strip() and pv.strip() and pv!=ev and len(pv.strip())>=8 and len(ev.strip())>=8: name_map.setdefault(pv.strip(),ev.strip())
    # ordena por tamanho para trocar nomes longos antes dos curtos
    name_keys=sorted(name_map,key=len,reverse=True)
    name_rx=re.compile(r'(?<![A-Za-zÀ-ÿ])(?:'+'|'.join(re.escape(k) for k in name_keys)+r')(?![A-Za-zÀ-ÿ])') if name_keys else None
    rex_cols=set((rex or {}).get('columns',[]))
    src=os.path.join(o.base,L10N); dst=os.path.join(o.out,L10N); srcen=os.path.join(o.source,L10N)
    if os.path.exists(o.out) and not o.allow_existing: sys.exit(f'{o.out} já existe (use --allow-existing para sobrescrever)')
    os.makedirs(dst,exist_ok=True)
    report={'changed':[],'errors':[]}
    for fn in sorted(os.listdir(src)):
        s=os.path.join(src,fn); d=os.path.join(dst,fn)
        if fn not in ov and fn not in bytext and not exact_names and not name_rx: shutil.copyfile(s,d); continue
        rows=read(s); en={r[0]:r for r in read(os.path.join(srcen,fn))[1:] if r}
        pending=dict(ov.get(fn,{})); bt=bytext.get(fn,{}); header=rows[0]
        if exact_names or name_rx:
            for r in rows[1:]:
                e=en.get(r[0]) if r else None
                if not e: continue
                for ci in range(1,min(len(r),len(e))):
                    ev,pv=e[ci],r[ci]
                    if not ev.strip() or pv==ev: continue
                    if exact_names and header[ci] in rex_cols and ev.strip() in exact_names:
                        r[ci]=ev; report['changed'].append({'table':fn,'id':r[0],'column':header[ci],'en':ev,'old':pv,'new':ev,'rule':'restore_exact_name'}); continue
                    if name_rx:
                        def sub(m):
                            en_name=name_map[m.group(0)]
                            return en_name if en_name in ev else m.group(0)   # só troca se o inglês original contém esse nome
                        nv=name_rx.sub(sub,pv)
                        if nv!=pv: r[ci]=nv; report['changed'].append({'table':fn,'id':r[0],'column':header[ci],'en':ev,'old':pv,'new':nv,'rule':'replace_translated_name'})
        # round-trip check: writer must reproduce the base file byte-for-byte before edits
        buf=io.StringIO(newline=''); csv.writer(buf,lineterminator='\r\n').writerows(rows)
        if buf.getvalue().encode('utf-8')!=open(s,'rb').read()[3:]:
            if list(csv.reader(io.StringIO(buf.getvalue(),newline='')))==rows: report.setdefault('warnings',[]).append(f'{fn}: round-trip difere só em bytes (quebra final/aspas); conteúdo idêntico')
            else: report['errors'].append(f'{fn}: round-trip CSV difere; edite manualmente')
        for r in rows[1:]:
            if not r or r[0] not in pending: continue
            spec=pending.pop(r[0]); e=en.get(r[0])
            cols=spec if isinstance(spec,dict) else {header[1]:spec}   # valor simples = 2ª coluna; dict = {coluna: valor}
            for colname,new in cols.items():
                if colname not in header: report['errors'].append(f'{fn}:{r[0]}: coluna {colname} não existe'); continue
                ci=header.index(colname)
                while len(r)<=ci: r.append('')
                srcval=e[ci] if e and ci<len(e) else ''
                if '\r\n' in srcval and '\r\n' not in new: new=new.replace('\n','\r\n')
                tok=TOK if srcval not in literal else TOK_NOBRACKET
                if sorted(tok.findall(new))!=sorted(tok.findall(srcval)):
                    report['errors'].append(f'{fn}:{r[0]}.{colname}: placeholders/tags divergem do inglês: {tok.findall(srcval)} vs {tok.findall(new)}'); continue
                old=r[ci]
                if new!=old: r[ci]=new; report['changed'].append({'table':fn,'id':r[0],'column':colname,'en':srcval,'old':old,'new':new})
        for k in pending: report['errors'].append(f'{fn}: ID {k} não existe')
        if bt:
            used=set()
            for col,mapping in bt.items():
                if col not in header: report['errors'].append(f'{fn}: coluna {col} não existe'); continue
                ci=header.index(col)
                for r in rows[1:]:
                    if not r or ci>=len(r): continue
                    e=en.get(r[0]); srcval=e[ci] if e and ci<len(e) else None
                    if srcval is None or srcval not in mapping: continue   # aplica sempre que o inglês original bate, esteja a célula traduzida ou não
                    new=mapping[srcval]
                    tok=TOK if srcval not in literal else TOK_NOBRACKET
                    if sorted(tok.findall(new))!=sorted(tok.findall(srcval)):
                        report['errors'].append(f'{fn}:{r[0]}.{col}: placeholders/tags divergem: {tok.findall(srcval)} vs {tok.findall(new)}'); continue
                    if new!=r[ci]: r[ci]=new; used.add((col,srcval)); report['changed'].append({'table':fn,'id':r[0],'column':col,'en':srcval,'old':srcval,'new':new})
            for col,mapping in bt.items():
                for k in mapping:
                    if (col,k) not in used: report.setdefault('unused',[]).append(f'{fn}.{col}: {k}')
        write(d,rows)
    print(f"alterados: {len(report['changed'])}  erros: {len(report['errors'])}")
    for e in report['errors']: print('ERRO',e)
    if o.report: json.dump(report,open(o.report,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    sys.exit(1 if report['errors'] else 0)
if __name__=='__main__': main()
