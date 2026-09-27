#!/usr/bin/env python3
"""Usa outra cultura do jogo (padrão zh-CN) como referência de completude da tradução PT-BR.

  python tools/check_completeness.py --game-l10n <pasta .../CSV/L10N> --translation translations/v13 [--ref zh-CN] [--en-dir <en original>] [--out relatorio.json]
Atenção: --game-l10n/en precisa ser o inglês ORIGINAL; se a árvore extraída já contém a tradução, passe --en-dir.

Para cada célula (tabela, ID, coluna) classifica:
  missing_in_en   : vazia em en e em PT-BR, mas preenchida na referência -> o inglês não tem esse texto; só dá para traduzir a partir da referência.
  same_as_en      : PT-BR idêntica ao inglês enquanto a referência difere do inglês -> possivelmente não traduzida (exclui nomes mantidos de propósito).
  empty_pt        : vazia em PT-BR com en preenchido (a auditoria oficial já cobre; aqui por completude).
  ref_missing_id  : ID existe em en/PT-BR mas não na referência (informativo).
"""
import argparse, csv, json, os, collections
KEEP={('Item_Name.csv','Name'),('Npc_Name.csv','Name'),('GuideBoss_Name.csv','Name'),('DungeonGlobalBoss_Name.csv','Name'),('World_Name.csv','Name'),('WorldSpot_Name.csv','Name'),('WorldContinent_Name.csv','Name'),('Skill_Name.csv','Name'),('Costume_Name.csv','Name'),('ShopItem_Name.csv','Name')}
def load(p):
    if not os.path.exists(p): return None,{}
    with open(p,encoding='utf-8-sig',newline='') as f:
        r=csv.reader(f); h=next(r); return h,{row[0]:row for row in r if row}
def main():
    a=argparse.ArgumentParser(); a.add_argument('--game-l10n',required=True); a.add_argument('--translation',required=True); a.add_argument('--ref',default='zh-CN'); a.add_argument('--en-dir',help='pasta en ORIGINAL em inglês (padrão: <game-l10n>/en)'); a.add_argument('--out')
    o=a.parse_args()
    en_dir=o.en_dir or os.path.join(o.game_l10n,'en'); ref_dir=os.path.join(o.game_l10n,o.ref); pt_dir=os.path.join(o.translation,'ProjectTT/Content/TT/Data/CSV/L10N/en')
    rep=collections.defaultdict(list); counts=collections.Counter()
    for fn in sorted(f for f in os.listdir(pt_dir) if f.endswith('.csv')):
        h,pt=load(os.path.join(pt_dir,fn)); _,en=load(os.path.join(en_dir,fn)); _,rf=load(os.path.join(ref_dir,fn))
        if not rf: counts['tables_without_ref']+=1; continue
        for id_,row in pt.items():
            e=en.get(id_); r=rf.get(id_)
            if r is None: counts['ref_missing_id']+=1; continue
            for i in range(1,len(h)):
                col=h[i]; p=row[i] if i<len(row) else ''; ev=e[i] if e and i<len(e) else ''; rv=r[i] if i<len(r) else ''
                if not rv.strip(): continue
                if not ev.strip() and not p.strip():
                    counts['missing_in_en']+=1; rep['missing_in_en'].append(dict(table=fn,id=id_,column=col,ref=rv))
                elif ev.strip() and not p.strip():
                    counts['empty_pt']+=1; rep['empty_pt'].append(dict(table=fn,id=id_,column=col,en=ev))
                elif p==ev and rv!=ev and (fn,col) not in KEEP and any(c.isalpha() for c in ev):
                    counts['same_as_en']+=1; rep['same_as_en'].append(dict(table=fn,id=id_,column=col,en=ev,ref=rv))
    print(json.dumps(counts,indent=1))
    per=collections.Counter((x['table']) for x in rep['same_as_en']); print('same_as_en por tabela (top 15):'); [print(f'  {t}: {n}') for t,n in per.most_common(15)]
    per=collections.Counter((x['table']) for x in rep['missing_in_en']); print('missing_in_en por tabela (top 15):'); [print(f'  {t}: {n}') for t,n in per.most_common(15)]
    if o.out: json.dump(rep,open(o.out,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
if __name__=='__main__': main()
