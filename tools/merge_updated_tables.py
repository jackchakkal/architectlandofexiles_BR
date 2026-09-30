#!/usr/bin/env python3
"""Create a new translation draft from a new game CSV dump, preserving reviewed PT-BR cells."""
from __future__ import annotations
import argparse,csv,json,pathlib,re,shutil

KEY_FIELDS=('Id','Key','LocaleKey','Type')
PROTECTED={
 'Npc_Name.csv':{'Title','Name'},
 'GuideBoss_Name.csv':{'PlaceName','Name'},
 'DungeonGlobalBoss_Name.csv':{'BossTitle','BossName'},
 'Dungeon_Name.csv':{'Name','StringParam'},
 'DungeonSection_Name.csv':{'StringParam'},
 'EliteDungeonSection_Name.csv':{'Name'},
 'Area_Name.csv':{'PlaceName'},
 'World_Name.csv':{'Name','Param'},
 'WorldSpot_Name.csv':{'SpotName'},
 'WorldMapArea_Name.csv':{'PlaceName','PlaceParam'},
}

def load(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        rd=csv.DictReader(f); rows=list(rd); headers=rd.fieldnames or []
    key=next((h for h in KEY_FIELDS if h in headers),headers[0] if headers else None)
    return headers,rows,{r.get(key,''):r for r in rows if r.get(key,'')},key

def occurrence_map(rows,key):
    counts={}; indexed={}
    for row in rows:
        ident=row.get(key,''); counts[ident]=counts.get(ident,0)+1
        indexed[(ident,counts[ident])]=row
    return indexed

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--old-source',required=True,type=pathlib.Path,help='Previous English CSV/L10N/en directory')
    ap.add_argument('--new-source',required=True,type=pathlib.Path,help='New English CSV/L10N/en directory')
    ap.add_argument('--old-translation',required=True,type=pathlib.Path,help='Previous translated CSV/L10N/en directory')
    ap.add_argument('--out',required=True,type=pathlib.Path,help='New draft output directory (must be new/empty)')
    ap.add_argument('--report',required=True,type=pathlib.Path,help='Local JSON review report')
    args=ap.parse_args()
    if args.out.exists() and any(args.out.iterdir()): raise SystemExit(f'Output directory must be empty: {args.out}')
    args.out.mkdir(parents=True,exist_ok=True)
    report={'new_translation_rows':[],'removed_source_rows':[],'changed_source_cells_requiring_review':[],'missing_old_translation_tables':[],'reused_exact_translations':[]}
    for newp in sorted(args.new_source.glob('*.csv')):
        name=newp.name; headers,new_rows,new_map,key=load(newp); oldp=args.old_source/name; trans_p=args.old_translation/name
        old_map=occurrence_map(load(oldp)[1],key) if oldp.exists() else {}
        trans_map=occurrence_map(load(trans_p)[1],key) if trans_p.exists() else {}
        new_index=occurrence_map(new_rows,key)
        memory={}
        for occurrence,old_row in old_map.items():
            translated_row=trans_map.get(occurrence)
            if not translated_row: continue
            for col in headers[1:]:
                english=old_row.get(col,'')
                if english and translated_row.get(col,'') != english:
                    memory.setdefault((col,english),set()).add(translated_row.get(col,''))
        if not trans_p.exists(): report['missing_old_translation_tables'].append(name)
        protected=set(PROTECTED.get(name,()))
        if name=='Item_Name.csv':
            protected.add('Name')
        merged=[]
        counts={}
        for row in new_rows:
            ident=row.get(key,''); counts[ident]=counts.get(ident,0)+1
            occurrence=(ident,counts[ident]); old=old_map.get(occurrence); translated=trans_map.get(occurrence)
            if old is None: report['new_translation_rows'].append({'table':name,'id':ident})
            result=dict(row)
            if old is None:
                for col in headers[1:]:
                    values=memory.get((col,row.get(col,'')),set())
                    if len(values)==1:
                        result[col]=next(iter(values))
                        report['reused_exact_translations'].append({'table':name,'id':ident,'column':col})
            if translated:
                row_protected=set(protected)
                if name=='Item_Name.csv':
                    row_protected.update(f'Param{n}' for n in range(1,10) if '{'+f'Param{n}'+'}' in row.get('Name',''))
                for col in headers:
                    if col in row_protected: continue
                    old_source=old.get(col) if old else None
                    new_source=row.get(col)
                    old_translation=translated.get(col)
                    if old is None: continue
                    if old_source==new_source:
                        result[col]=old_translation
                    elif old_translation==old_source:
                        # The old text had never been translated; take the new source string.
                        result[col]=new_source
                    else:
                        # Keep reviewed PT-BR and explicitly queue it for human review.
                        result[col]=old_translation
                        report['changed_source_cells_requiring_review'].append({'table':name,'id':ident,'column':col,'old_source':old_source,'new_source':new_source,'preserved_translation':old_translation})
            merged.append(result)
        for ident,ordinal in sorted(set(old_map)-set(new_index)):
            report['removed_source_rows'].append({'table':name,'id':ident,'occurrence':ordinal})
        dest=args.out/name
        with dest.open('w',encoding='utf-8-sig',newline='') as f:
            wr=csv.DictWriter(f,fieldnames=headers,lineterminator='\r\n',extrasaction='ignore'); wr.writeheader(); wr.writerows(merged)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:len(v) for k,v in report.items()},ensure_ascii=False,indent=2))
    print('New table cells need human review before building a release.')
if __name__=='__main__': main()
