#!/usr/bin/env python3
"""Verificação de nomes próprios (regra do docs/GLOSSARIO-E-REGRAS.md: todo nome próprio fica em inglês em qualquer menção).

Fontes de nomes = __restore_exact_names__ (sources + names) do overrides.json. Para cada célula de TODAS as tabelas/colunas:
  A) "exact": o inglês original é exatamente um nome (placeholders ignorados) e a célula traduzida difere -> nome traduzido.
  B) "sentences": o inglês original contém um nome (>= 2 palavras, não descritivo) e a tradução não contém o nome literal.
  python tools/scan_name_mentions.py --source <raiz extraída em inglês> --translation <snapshot> --overrides changes/<x>/overrides.json --out <json>
Saída 0 = nada encontrado; 1 = há pendências.
"""
import csv,os,re,collections,json,argparse,sys
a=argparse.ArgumentParser(); a.add_argument('--source',required=True); a.add_argument('--translation',required=True); a.add_argument('--overrides',required=True); a.add_argument('--out',default='name-mentions.json'); a.add_argument('--min-len',type=int,default=8); A=a.parse_args()
L='/ProjectTT/Content/TT/Data/CSV/L10N/en'; O=A.source+L; T=A.translation+L
CJK=re.compile(r'[぀-ヿ㐀-鿿가-힯]'); TOK=re.compile(r'\[[^\]\r\n]+\]|\{[^}\r\n]+\}|</?[A-Za-z][^>]*>|</>')
DESCRIPTIVE=re.compile(r'^(Increase|Increases|Increased|Reduce|Reduces|Reduced|Decrease|Decreases|Restore|Restores|Grant|Grants|Gain|Gains|Ignore|Ignores|Remove|Removes|Recover|Recovers|Boost|Boosts|Enhance|Enhances|Improve|Improves|Apply|Applies|Deal|Deals|Convert|Converts|Additional|Extra|Max|Maximum|Min|Minimum|Basic|Normal|Bonus|Chance|Damage|Attack|Defense|Skill|Critical|Movement|Cooldown|Heal|Heals|Healing|HP|MP|Level|Test)\b',re.I)
DESCRIPTIVE_END=re.compile(r'\b(Increase|Decrease|Reduction|Bonus|Effect|Chance|Rate|Speed|Damage|Resistance|Amount|Recovery|Boost|Up|Down|Disabled|Enabled|Waypoint|Stone|Buff|Debuff|Immunity|Penalty|Reward|Time|Limit)\s*(I{1,3}|IV|V)?$',re.I)
def load(p):
    with open(p,encoding='utf-8-sig',newline='') as f: r=csv.reader(f); h=next(r); return h,{x[0]:x for x in r if x}
def load_rows(p):
    with open(p,encoding='utf-8-sig',newline='') as f: r=csv.reader(f); h=next(r); return h,[x for x in r]
ov=json.load(open(A.overrides,encoding='utf-8')); rex=ov.get('__restore_exact_names__',{})
exact=set(); bycat=collections.defaultdict(set)
for fn,col in rex.get('sources',[]):
    h,d=load(f'{O}/{fn}'); i=h.index(col)
    for r in d.values():
        v=r[i].strip() if i<len(r) else ''
        if v and not CJK.search(v): exact.add(v); bycat[fn.replace('_Name.csv','')].add(v)
for n in rex.get('names',[]): exact.add(n.strip()); bycat['explicit'].add(n.strip())
stripped={TOK.sub('',n).strip(' :-\t'):n for n in exact if ' ' in TOK.sub('',n).strip(' :-\t')}   # formas sem placeholder, só com >= 2 palavras (preenchido após is_proper)
rex_cols=set(rex.get('columns',[]))
ignore=set(ov.get('__scan_ignore__',{}))   # 'Tabela.csv:ID' -> justificativa (falsos positivos revisados)
decided={(fn,col,en) for fn,cols in ov.get('__by_text__',{}).items() for col,m in cols.items() for en in m}   # decisões explícitas (ex.: rótulos de falante em PT) não são pendência
def is_proper(n):
    v=TOK.sub('',n).strip(' :-\t')
    return ' ' in v and len(v)>=A.min_len and not DESCRIPTIVE.match(v) and not DESCRIPTIVE_END.search(v) and not re.match(r'^[\d.,]+ ',v) and not re.search(r'\b(of|the|and|a|an|to|for)$',v,re.I)
generic={n for n in exact if not is_proper(n)}   # nomes genéricos/de 1 palavra só contam como pendência nas colunas de nome (rex_cols)
proper=collections.defaultdict(set)
for cat,ns in bycat.items():
    for n in ns:
        v=TOK.sub('',n).strip(' :-\t')
        if is_proper(n) or cat=='explicit': proper[cat].add(v)
rx={c:re.compile(r'(?<![A-Za-z])(?:'+'|'.join(re.escape(n) for n in sorted(ns,key=len,reverse=True))+r')(?![A-Za-z])') for c,ns in proper.items() if ns}
ex=collections.Counter(); ex_samples=collections.defaultdict(list); sent={}
for fn in sorted(os.listdir(T)):
    ho,eo=load_rows(f'{O}/{fn}'); ht,et=load_rows(f'{T}/{fn}'); ed={r[0]:r for r in eo if r}
    for ri,tr in enumerate(et):
        if not tr: continue
        k=tr[0]; row=eo[ri] if ri<len(eo) and eo[ri] and eo[ri][0]==k else ed.get(k)   # IDs repetidos: mesma posição
        if not row: continue
        for i in range(1,min(len(row),len(tr))):
            e,p=row[i],tr[i]
            if e==p or not e.strip() or CJK.search(e): continue
            es=TOK.sub('',e).strip(' :-\t')
            if (fn,ho[i],e) in decided or f'{fn}:{k}' in ignore: continue
            if (e.strip() in exact and (e.strip() not in generic or ho[i] in rex_cols)) or (es in stripped and is_proper(stripped[es]) and es!=e.strip()):
                ex[(fn,ho[i])]+=1
                if len(ex_samples[(fn,ho[i])])<5: ex_samples[(fn,ho[i])].append((k,e,p))
                continue
            for cat,r in rx.items():
                hit=[m for m in r.findall(e) if m not in p]
                if hit: sent.setdefault((cat,fn,ho[i],e),(k,p,sorted(set(hit)))); break
out={'exact':{f'{fn}.{col}':{'count':n,'samples':ex_samples[(fn,col)]} for (fn,col),n in sorted(ex.items(),key=lambda x:-x[1])},'sentences':[dict(cat=c,table=fn,column=col,id=k,en=e,pt=p,names=h) for (c,fn,col,e),(k,p,h) in sent.items()]}
json.dump(out,open(A.out,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('nomes conhecidos:',len(exact),'| células-nome ainda traduzidas:',sum(ex.values()),'em',len(ex),'colunas | frases únicas com nome perdido:',len(sent))
print(collections.Counter(s['cat'] for s in out['sentences']).most_common())
for key,n in sorted(ex.items(),key=lambda x:-x[1])[:25]: print(' exato',n,key,ex_samples[key][0][1],'->',ex_samples[key][0][2])
sys.exit(1 if (ex or sent) else 0)
