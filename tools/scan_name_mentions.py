#!/usr/bin/env python3
"""Lista nomes de Skills, itens e masmorras que foram traduzidos (célula inteira) ou que sumiram de frases traduzidas.
  python tools/scan_name_mentions.py --source <raiz extraída em inglês> --translation <snapshot> --out <json>
"""
import csv,os,re,collections,json,sys,argparse
a=argparse.ArgumentParser(); a.add_argument('--source',required=True); a.add_argument('--translation',required=True); a.add_argument('--out',default='name-mentions.json'); A=a.parse_args()
O=A.source+'/ProjectTT/Content/TT/Data/CSV/L10N/en'; T=A.translation+'/ProjectTT/Content/TT/Data/CSV/L10N/en'
def load(p):
    with open(p,encoding='utf-8-sig',newline='') as f: r=csv.reader(f); h=next(r); return h,{x[0]:x for x in r if x}
def col(p,c):
    h,d=load(p); i=h.index(c); return {k:v[i] for k,v in d.items() if i<len(v)}
def names(p,c,minlen=6,space=True):
    return set(v.strip() for v in col(p,c).values() if len(v.strip())>=minlen and not re.search(r'[{}\[\]<>]',v) and (' ' in v.strip() or not space))
dung=names(f'{O}/Dungeon_Name.csv','Name')|names(f'{O}/Dungeon_Name.csv','Param')|names(f'{O}/DungeonSection_Name.csv','StringParam')|names(f'{O}/DungeonSection_Name.csv','Name')
skill=names(f'{O}/Skill_Name.csv','Name',4,False)
item=names(f'{O}/Item_Name.csv','Name',6,False)
cats={'masmorra':dung,'skill':skill,'item':item}
rx={c:re.compile(r'(?<![A-Za-z])(?:'+'|'.join(re.escape(n) for n in sorted((x for x in ns if len(x)>=8),key=len,reverse=True))+r')(?![A-Za-z])') for c,ns in cats.items()}
exact=collections.Counter(); sent={}
for fn in sorted(os.listdir(T)):
    ho,eo=load(f'{O}/{fn}'); ht,et=load(f'{T}/{fn}')
    for k,row in eo.items():
        tr=et.get(k)
        if not tr: continue
        for i in range(1,min(len(row),len(tr))):
            e,p=row[i],tr[i]
            if e==p or not e.strip(): continue
            es=e.strip(); done=False
            for cat,ns in cats.items():
                if es in ns: exact[(cat,fn,ho[i])]+=1; done=True; break
            if done: continue
            for cat,r in rx.items():
                hit=[m for m in r.findall(e) if m not in p]
                if hit: sent.setdefault((cat,fn,ho[i],e),(k,p,sorted(set(hit)))); break
out={'exact':{f'{c}|{fn}|{col}':n for (c,fn,col),n in exact.items()},'sentences':[dict(cat=c,table=fn,column=col,id=k,en=e,pt=p,names=h) for (c,fn,col,e),(k,p,h) in sent.items()]}
json.dump(out,open(A.out,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('exato total',sum(exact.values()),'| frases únicas',len(sent), collections.Counter(s['cat'] for s in out['sentences']))
for key,n in sorted(exact.items(),key=lambda x:-x[1])[:20]: print(n,key)
