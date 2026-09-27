#!/usr/bin/env python3
"""Lista nomes próprios (fontes do overrides.json: Skills, itens, masmorras, lugares, facções, vendedores...) que foram traduzidos
(célula inteira) ou que sumiram de frases traduzidas.
  python tools/scan_name_mentions.py --source <raiz extraída em inglês> --translation <snapshot> --overrides changes/<x>/overrides.json --out <json>
"""
import csv,os,re,collections,json,argparse
a=argparse.ArgumentParser(); a.add_argument('--source',required=True); a.add_argument('--translation',required=True); a.add_argument('--overrides',required=True); a.add_argument('--out',default='name-mentions.json'); a.add_argument('--min-len',type=int,default=8); A=a.parse_args()
L='/ProjectTT/Content/TT/Data/CSV/L10N/en'; O=A.source+L; T=A.translation+L
CJK=re.compile(r'[぀-ヿ㐀-鿿가-힯]')
DESCRIPTIVE=re.compile(r'^(Increase|Increases|Reduce|Reduces|Decrease|Decreases|Restore|Restores|Grant|Grants|Gain|Gains|Ignore|Ignores|Remove|Removes|Recover|Recovers|Boost|Boosts|Enhance|Enhances|Improve|Improves|Apply|Applies|Deal|Deals|Convert|Converts|Additional|Extra|Max|Maximum|Min|Minimum|Basic|Normal|Bonus|Chance|Damage|Attack|Defense|Skill|Critical|Movement|Cooldown|Heal|Heals|Healing|HP|MP|Level|Test)\b',re.I)
def load(p):
    with open(p,encoding='utf-8-sig',newline='') as f: r=csv.reader(f); h=next(r); return h,{x[0]:x for x in r if x}
ov=json.load(open(A.overrides,encoding='utf-8')); sources=ov.get('__restore_exact_names__',{}).get('sources',[])
names=collections.defaultdict(set)
for fn,col in sources:
    h,d=load(f'{O}/{fn}'); i=h.index(col)
    for r in d.values():
        v=r[i].strip() if i<len(r) else ''
        if len(v)>=A.min_len and ' ' in v and not re.search(r'[{}\[\]<>%]',v) and not CJK.search(v) and not DESCRIPTIVE.match(v): names[fn.replace('_Name.csv','')].add(v)
rx={c:re.compile(r'(?<![A-Za-z])(?:'+'|'.join(re.escape(n) for n in sorted(ns,key=len,reverse=True))+r')(?![A-Za-z])') for c,ns in names.items() if ns}
allnames=set().union(*names.values())
exact=collections.Counter(); sent={}
for fn in sorted(os.listdir(T)):
    ho,eo=load(f'{O}/{fn}'); ht,et=load(f'{T}/{fn}')
    for k,row in eo.items():
        tr=et.get(k)
        if not tr: continue
        for i in range(1,min(len(row),len(tr))):
            e,p=row[i],tr[i]
            if e==p or not e.strip(): continue
            if e.strip() in allnames: exact[(fn,ho[i])]+=1; continue
            for cat,r in rx.items():
                hit=[m for m in r.findall(e) if m not in p]
                if hit: sent.setdefault((cat,fn,ho[i],e),(k,p,sorted(set(hit)))); break
out={'exact':{f'{fn}.{col}':n for (fn,col),n in exact.items()},'sentences':[dict(cat=c,table=fn,column=col,id=k,en=e,pt=p,names=h) for (c,fn,col,e),(k,p,h) in sent.items()]}
json.dump(out,open(A.out,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('células-nome ainda traduzidas:',sum(exact.values()),'| frases únicas com nome perdido:',len(sent))
print(collections.Counter(s['cat'] for s in out['sentences']).most_common())
for key,n in sorted(exact.items(),key=lambda x:-x[1])[:10]: print(' exato',n,key)
