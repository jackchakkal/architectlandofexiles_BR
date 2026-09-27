#!/usr/bin/env python3
"""Compare old/new English source tables with a PT-BR snapshot after a game update."""
from __future__ import annotations
import argparse, csv, json, pathlib, re

KEY_FIELDS = ('Id', 'Key', 'LocaleKey', 'Type')

def table(path: pathlib.Path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = reader.fieldnames or []
    key = next((x for x in KEY_FIELDS if x in fields), fields[0] if fields else None)
    return fields, key, {r.get(key, ''): r for r in rows if r.get(key, '')}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--old-source',required=True,type=pathlib.Path,help='Extracted CSV/L10N/en directory from the previous game version')
    ap.add_argument('--new-source',required=True,type=pathlib.Path,help='Extracted CSV/L10N/en directory from the updated game version')
    ap.add_argument('--translation',required=True,type=pathlib.Path,help='Snapshot root, e.g. translations/v11-quality/ProjectTT/Content/TT/Data/CSV/L10N/en')
    ap.add_argument('--out',required=True,type=pathlib.Path,help='Local JSON review report; do not commit extracted source strings')
    args=ap.parse_args()
    report={'old_source':str(args.old_source),'new_source':str(args.new_source),'translation':str(args.translation),'tables':{},'summary':{'new_tables':0,'removed_tables':0,'new_rows':0,'removed_rows':0,'changed_source_cells':0,'missing_translation_rows':0,'untranslated_cells':0}}
    names=sorted(set(p.name for p in args.old_source.glob('*.csv'))|set(p.name for p in args.new_source.glob('*.csv')))
    for name in names:
        oldp,newp,tp=args.old_source/name,args.new_source/name,args.translation/name
        if not oldp.exists() or not newp.exists():
            state='new_table' if newp.exists() else 'removed_table'; report['tables'][name]={'state':state}
            report['summary']['new_tables' if newp.exists() else 'removed_tables']+=1; continue
        old_fields,old_key,old=table(oldp); fields,key,new=table(newp)
        trans=table(tp)[2] if tp.exists() else {}
        added=sorted(set(new)-set(old)); removed=sorted(set(old)-set(new)); changed=[]; missing=[]; untranslated=[]
        for ident,row in new.items():
            if ident not in trans: missing.append(ident)
            for col,value in row.items():
                previous=old.get(ident,{}).get(col)
                if ident in old and previous!=value:
                    changed.append({'id':ident,'column':col,'old_source':previous,'new_source':value,'translation':trans.get(ident,{}).get(col)})
                translated=trans.get(ident,{}).get(col)
                if value and col in fields and (translated is None or not translated.strip() or translated==value):
                    untranslated.append({'id':ident,'column':col})
        entry={'row_key':key,'new_ids':added,'removed_ids':removed,'changed_source_cells':changed,'missing_translation_ids':missing,'untranslated_cells':untranslated}
        if added or removed or changed or missing or untranslated: report['tables'][name]=entry
        report['summary']['new_rows']+=len(added); report['summary']['removed_rows']+=len(removed)
        report['summary']['changed_source_cells']+=len(changed); report['summary']['missing_translation_rows']+=len(missing)
        report['summary']['untranslated_cells']+=len(untranslated)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report['summary'],ensure_ascii=False,indent=2))
    print(f'Review report written to {args.out}')

if __name__=='__main__': main()
