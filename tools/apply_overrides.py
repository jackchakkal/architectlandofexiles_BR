#!/usr/bin/env python3
"""Gera um snapshot novo a partir de um snapshot base + overrides.json.

Formato do overrides.json:
  {"Tabela.csv": {"ID": "novo valor"},                       # por ID, só a 2ª coluna
   "__by_text__": {"Tabela.csv": {"Coluna": {"texto em inglês": "texto PT-BR"}}},  # por texto exato, em qualquer coluna
   "__literal_brackets__": ["<Faction>[Hunter]</>"]}   # textos em que [..] é literal (confirmado por outra cultura), não placeholder
A substituição por texto só se aplica onde a célula do snapshot base ainda é IGUAL ao inglês original.

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
    ov=json.load(open(o.overrides,encoding='utf-8')); ov.pop('_comment',None); bytext=ov.pop('__by_text__',{}); literal=set(ov.pop('__literal_brackets__',[]))
    src=os.path.join(o.base,L10N); dst=os.path.join(o.out,L10N); srcen=os.path.join(o.source,L10N)
    if os.path.exists(o.out) and not o.allow_existing: sys.exit(f'{o.out} já existe (use --allow-existing para sobrescrever)')
    os.makedirs(dst,exist_ok=True)
    report={'changed':[],'errors':[]}
    for fn in sorted(os.listdir(src)):
        s=os.path.join(src,fn); d=os.path.join(dst,fn)
        if fn not in ov and fn not in bytext: shutil.copyfile(s,d); continue
        rows=read(s); en={r[0]:r for r in read(os.path.join(srcen,fn))[1:] if r}
        pending=dict(ov.get(fn,{})); bt=bytext.get(fn,{}); header=rows[0]
        # round-trip check: writer must reproduce the base file byte-for-byte before edits
        buf=io.StringIO(newline=''); csv.writer(buf,lineterminator='\r\n').writerows(rows)
        if buf.getvalue().encode('utf-8')!=open(s,'rb').read()[3:]: report['errors'].append(f'{fn}: round-trip CSV difere; edite manualmente')
        for r in rows[1:]:
            if not r or r[0] not in pending: continue
            new=pending.pop(r[0]); old=r[1]
            e=en.get(r[0]); srcval=e[1] if e and len(e)>1 else ''
            if sorted(TOK.findall(new))!=sorted(TOK.findall(srcval)):
                report['errors'].append(f'{fn}:{r[0]}: placeholders/tags divergem do inglês: {TOK.findall(srcval)} vs {TOK.findall(new)}'); continue
            if new!=old: r[1]=new; report['changed'].append({'table':fn,'id':r[0],'en':srcval,'old':old,'new':new})
        for k in pending: report['errors'].append(f'{fn}: ID {k} não existe')
        if bt:
            used=set()
            for col,mapping in bt.items():
                if col not in header: report['errors'].append(f'{fn}: coluna {col} não existe'); continue
                ci=header.index(col)
                for r in rows[1:]:
                    if not r or ci>=len(r): continue
                    e=en.get(r[0]); srcval=e[ci] if e and ci<len(e) else None
                    if srcval is None or r[ci]!=srcval or srcval not in mapping: continue
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
