#!/usr/bin/env python3
"""Restore QZXKEEP markers accidentally left by batched translation tools."""
from __future__ import annotations
import argparse,csv,json,pathlib,re

KEY_FIELDS=('Id','Key','LocaleKey','Type')
NEWLINE=re.compile(r'\\r\\n|\\n|\\r|\r\n|\n|\r')
TAG=re.compile(r'<[^<>]*>|\{[^{}]*\}|\[[A-Za-z_][A-Za-z0-9_]*\]')
MARKER=re.compile(r'QZXKEEP\d{5}XZQ',re.I)
TERMS=re.compile(r'\bSkills?\b|\bCodex\b',re.I)

def load(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        rd=csv.DictReader(f); rows=list(rd); headers=rd.fieldnames or []
    key=next((x for x in KEY_FIELDS if x in headers),headers[0] if headers else None)
    return headers,rows,{r.get(key,''):r for r in rows if r.get(key,'')},key

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',required=True,type=pathlib.Path,help='Original English CSV/L10N/en directory')
    ap.add_argument('--translation',required=True,type=pathlib.Path,help='Translated CSV/L10N/en directory to repair in place')
    ap.add_argument('--out',required=True,type=pathlib.Path,help='JSON report for manual leftovers')
    args=ap.parse_args()
    entities=set()
    for filename in ('Area_Name.csv','Dungeon_Name.csv','DungeonSection_Name.csv','World_Name.csv','WorldSpot_Name.csv','WorldMapArea_Name.csv','Class_Name.csv','Npc_Name.csv'):
        p=args.source/filename
        if not p.exists(): continue
        with p.open(encoding='utf-8-sig',newline='') as f:
            for row in csv.reader(f):
                for value in row[1:]:
                    if value and len(value)>2 and re.search(r'[A-Z]',value): entities.add(value.strip())
    entities.update({'Skill','Skills','skill','skills','Codex'})
    entity_rx=re.compile(r'(?<![\w])('+ '|'.join(re.escape(x) for x in sorted(entities,key=len,reverse=True))+r')(?![\w])') if entities else None
    report={'restored_markers':0,'unmatched_markers':[]}
    for tp in sorted(args.translation.glob('*.csv')):
        sp=args.source/tp.name
        if not sp.exists(): continue
        th,translated,_,key=load(tp); _,_,source,_=load(sp); changed=False
        for row in translated:
            original_row=source.get(row.get(key,''),{})
            if tp.name=='ClientString_Name.csv' and row.get('Key')=='GUDUA_MAXLEVEL_NOTI':
                row['Value']='Gudua está no nível máximo.'; changed=True; continue
            if tp.name=='ClientString_Name.csv' and row.get('Key')=='SPLASH_GRADE_MESSAGE':
                row['Value']='Este jogo possui classificação etária mínima de <Red>15 anos</>, e menores de 15 anos não podem jogar.'; changed=True; continue
            for col,value in row.items():
                if not value or not MARKER.search(value): continue
                source_value=original_row.get(col,'') or ''; keep=[]
                def protect(pattern,text):
                    def repl(m):
                        token=f'QZXKEEP{len(keep):05d}XZQ'; keep.append((token,m.group(0))); return token
                    return pattern.sub(repl,text)
                protected=protect(NEWLINE,source_value); protected=protect(TAG,protected)
                if entity_rx: protected=protect(entity_rx,protected)
                protected=protect(TERMS,protected)
                repaired=value
                for token,segment in keep:
                    repaired=re.sub(re.escape(token),lambda _,s=segment:s,repaired,flags=re.I)
                leftover=MARKER.findall(repaired)
                if leftover:
                    report['unmatched_markers'].append({'table':tp.name,'id':row.get(key,''),'column':col,'markers':leftover})
                if repaired!=value: row[col]=repaired; report['restored_markers']+=len(MARKER.findall(value))-len(leftover); changed=True
        if changed:
            with tp.open('w',encoding='utf-8-sig',newline='') as f:
                wr=csv.DictWriter(f,fieldnames=th,lineterminator='\r\n',extrasaction='ignore');wr.writeheader();wr.writerows(translated)
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'restored_markers':report['restored_markers'],'unmatched_markers':len(report['unmatched_markers'])},indent=2))
if __name__=='__main__':main()
