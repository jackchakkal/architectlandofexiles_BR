#!/usr/bin/env python3
"""Lista células de interface cuja tradução ficou muito maior que o inglês (candidatas a estourar a tela).

  python tools/find_overflow_candidates.py --source <raiz extraída em inglês> --translation <snapshot> [--table ClientString_Name.csv]
      [--max-source-len 25] [--min-excess 6] [--out arquivo.json]

Também aponta duplicações ("X X") e traduções com mais de 2x o tamanho da fonte em qualquer tabela.
"""
import argparse, csv, json, os, re
L10N='ProjectTT/Content/TT/Data/CSV/L10N/en'
def load(p):
    with open(p,encoding='utf-8-sig',newline='') as f:
        r=csv.reader(f); h=next(r); return h,[row for row in r if row]
def main():
    a=argparse.ArgumentParser(); a.add_argument('--source',required=True); a.add_argument('--translation',required=True)
    a.add_argument('--table',action='append'); a.add_argument('--max-source-len',type=int,default=25); a.add_argument('--min-excess',type=int,default=6); a.add_argument('--out')
    o=a.parse_args()
    src=os.path.join(o.source,L10N); dst=os.path.join(o.translation,L10N)
    tables=o.table or sorted(f for f in os.listdir(dst) if f.endswith('.csv'))
    out=[]
    for fn in tables:
        h,so=load(os.path.join(src,fn)); _,tr=load(os.path.join(dst,fn)); en={r[0]:r for r in so}
        for r in tr:
            e=en.get(r[0])
            if not e: continue
            for i in range(1,min(len(r),len(e))):
                s,d=e[i],r[i]
                if not s.strip() or s==d or '\n' in s: continue
                excess=len(d)-len(s); dup=bool(re.match(r'^(.{6,}?)\s+\1$',d.strip()))
                if dup or (len(s)<=o.max_source_len and excess>=o.min_excess) or len(d)>2*len(s)+10:
                    out.append(dict(table=fn,id=r[0],column=h[i] if i<len(h) else i,en=s,pt=d,excess=excess,duplicate=dup))
    out.sort(key=lambda x:(not x['duplicate'],-x['excess']))
    print(f'candidatos: {len(out)}')
    for c in out[:40]: print(f"{c['excess']:+3d} {'DUP ' if c['duplicate'] else ''}{c['table']}:{c['id']} | {c['en']} | {c['pt']}")
    if o.out: json.dump(out,open(o.out,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
if __name__=='__main__': main()
