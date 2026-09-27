#!/usr/bin/env python3
"""Audit translated CSV tables against a separately extracted English source."""
from __future__ import annotations
import argparse,csv,json,pathlib,re

KEY_FIELDS=('Id','Key','LocaleKey','Type')
PLACEHOLDER=re.compile(r'\{[^{}]+\}|\[[A-Za-z0-9_:.-]+\]|<\/?[A-Za-z][A-Za-z0-9_]*(?:=[^>]*)?>|</>')
BAD_TOWER=re.compile(r"Torre do Gigante|Torre do gigante|Torre\s*</>\s*do\s+gigante|Giant[’']s Torre|Giant Torre|Torre do Giant|Torre 3F do Giant",re.I)
SENTINEL=re.compile(r'QZXKEEP\d{5}XZQ')

def load(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        rd=csv.DictReader(f); rows=list(rd); headers=rd.fieldnames or []
    key=next((h for h in KEY_FIELDS if h in headers),headers[0] if headers else None)
    return headers,{r.get(key,''):r for r in rows if r.get(key,'')},key

def tokens(text):
    found=[]
    for token in PLACEHOLDER.findall(text or ''):
        if token.startswith('[') and token.endswith(']'):
            name=token[1:-1]
            # UI labels such as [Daily] are translatable text. Keep only variable-like
            # square tokens (names, counts, values, time units, and date components).
            if not (name in {'Value','Keyword','Name','Time','Count','CharacterName','DashCount','MaxCount','Grade','Level','Param','ItemName','InvasionName','ClanName','Rank','UserName','AreaName','Player','DungeonName','EventName','PityGrade','TargetName','SkillName','AssetName','QuestName','BossName','CurrentCount','CurrentValue','OriginalCount','OriginalName','ClassRank','ScoreValue','RemainCount','WorldName','Score','RatingValue','TournamentName','HardCount','NpcName','MinValue','MaxValue','MaxValue1','MaxValue2','MinValue1','MinValue2','PercentValue','PurchaseCount','StageNo','EndDate','StartDate','MM','HH','SS','DD','YYYY','TIME','COUNT','TEMP','d','h','m','s','MM:SS','HH:MM:SS'} or re.search(r'(?:Name|Value|Count|Param|Rank|Time|Index|Rate|Chance|Point|Level|No|Date|Percent|Duration|Number|Score|Amount)$',name)):
                continue
        found.append(token)
    return sorted(found)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',required=True,type=pathlib.Path,help='Original English CSV/L10N/en directory')
    ap.add_argument('--translation',required=True,type=pathlib.Path,help='Translated CSV/L10N/en directory')
    ap.add_argument('--out',type=pathlib.Path,help='Write JSON report here; defaults to stdout')
    args=ap.parse_args(); report={'summary':{},'issues':[]}; totals={'missing_tables':0,'missing_ids':0,'new_ids':0,'empty_translations':0,'placeholder_mismatches':0,'item_name_mismatches':0,'bad_tower_mentions':0,'left_as_direction_candidates':0}
    for srcp in sorted(args.source.glob('*.csv')):
        trp=args.translation/srcp.name
        if not trp.exists():
            totals['missing_tables']+=1; report['issues'].append({'kind':'missing_table','table':srcp.name}); continue
        sh,source,sk=load(srcp); th,translated,tk=load(trp)
        for ident in sorted(set(source)-set(translated)):
            totals['missing_ids']+=1; report['issues'].append({'kind':'missing_id','table':srcp.name,'id':ident})
        for ident in sorted(set(translated)-set(source)):
            totals['new_ids']+=1; report['issues'].append({'kind':'translation_id_not_in_source','table':srcp.name,'id':ident})
        for ident,srow in source.items():
            trow=translated.get(ident)
            if not trow: continue
            for col,svalue in srow.items():
                tvalue=trow.get(col)
                if svalue and svalue.strip() and (tvalue is None or not tvalue.strip()):
                    totals['empty_translations']+=1; report['issues'].append({'kind':'empty_translation','table':srcp.name,'id':ident,'column':col})
                elif svalue and tvalue:
                    if SENTINEL.search(tvalue):
                        totals.setdefault('stray_translation_sentinels',0); totals['stray_translation_sentinels']+=1
                        report['issues'].append({'kind':'unrestored_translation_sentinel','table':srcp.name,'id':ident,'column':col})
                    if col in {'GuideParam1','GuideParam2','GuideParam3'} and str(svalue).lstrip().startswith('{'):
                        try:
                            sj=json.loads(svalue); tj=json.loads(tvalue)
                            if isinstance(sj,dict) and isinstance(tj,dict) and set(sj)!=set(tj):
                                totals.setdefault('json_structure_mismatches',0); totals['json_structure_mismatches']+=1
                                report['issues'].append({'kind':'json_structure_mismatch','table':srcp.name,'id':ident,'column':col})
                        except Exception:
                            totals.setdefault('invalid_json_parameters',0); totals['invalid_json_parameters']+=1
                            report['issues'].append({'kind':'invalid_json_parameter','table':srcp.name,'id':ident,'column':col})
                        continue
                    sp=tokens(svalue); tp=tokens(tvalue)
                    # Accessory descriptions intentionally expand the source's {Param} template
                    # into natural Portuguese; these two fields are not runtime variables.
                    if srcp.name=='Item_Name.csv' and col=='Desc' and svalue=='This {Param3} is equipped on {Param2}.':
                        sp=[]; tp=[]
                    sp=[x for x in sp if x!='{jstag:}']; tp=[x for x in tp if x!='{jstag:}']
                    # Name fields are intentionally original; formatting tokens remain part of that name template.
                    if sp!=tp and col not in {'Name','Title','BossName','BossTitle','PlaceName','SpotName'}:
                        totals['placeholder_mismatches']+=1; report['issues'].append({'kind':'placeholder_or_tag_mismatch','table':srcp.name,'id':ident,'column':col,'source_tokens':sp,'translation_tokens':tp})
                    if BAD_TOWER.search(tvalue):
                        totals['bad_tower_mentions']+=1; report['issues'].append({'kind':'translated_or_malformed_giants_tower','table':srcp.name,'id':ident,'column':col,'value':tvalue})
                    directional=re.search(r'\b(?:left hand|left-hand|left side|leftmost|bottom left|top left|turn(?:ing)? left|to the left|on your left|at the left|left of|go left|left arrow|arrow left|left key|is to the left|are to the left|is left|are left|located left)\b',svalue,re.I) or re.search(r'(?:LEFT|ARROW|INPUTKEY)',ident,re.I)
                    remaining_context=re.search(r'\b(?:time|times|attempts?|summons?|remaining|until|points?|entries|tickets?|duration|count|left)\b',ident+' '+svalue,re.I)
                    if 'left' in svalue.lower() and remaining_context and not directional and re.search(r'à esquerda|\besquerda\b',tvalue,re.I):
                        totals['left_as_direction_candidates']+=1; report['issues'].append({'kind':'left_may_mean_remaining','table':srcp.name,'id':ident,'column':col,'value':tvalue})
    item_src=args.source/'Item_Name.csv'; item_tr=args.translation/'Item_Name.csv'
    if item_src.exists() and item_tr.exists():
        _,src,_=load(item_src); _,tr,_=load(item_tr)
        for ident,srow in src.items():
            row=tr.get(ident)
            if not row: continue
            if row.get('Name')!=srow.get('Name'):
                totals['item_name_mismatches']+=1; report['issues'].append({'kind':'item_title_changed','table':'Item_Name.csv','id':ident})
            for n in range(1,10):
                field=f'Param{n}'
                if re.search(r'\{'+field+r'\}',srow.get('Name','')) and row.get(field)!=srow.get(field):
                    totals['item_name_mismatches']+=1; report['issues'].append({'kind':'item_title_parameter_changed','table':'Item_Name.csv','id':ident,'field':field})
    report['summary']=totals
    encoded=json.dumps(report,ensure_ascii=False,indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(encoded,encoding='utf-8'); print(json.dumps(totals,ensure_ascii=False,indent=2)); print(f'Report written to {args.out}')
    else: print(encoded)

if __name__=='__main__': main()
