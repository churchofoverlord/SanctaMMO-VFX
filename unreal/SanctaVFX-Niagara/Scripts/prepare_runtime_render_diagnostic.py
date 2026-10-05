"""Isolate previously empty captures before accepting another complete batch."""
import pathlib,json,copy
root=pathlib.Path(__file__).resolve().parents[1]
plan=json.loads((root/'Evidence/runtime-review-cases.json').read_text(encoding='utf-8'))
slugs=['CCStunActive','CCRootActive','CCSleepActive','CCFearActive','FireBoltIFlight','FireBoltIIFlight','SeveringCastI','SeveringMark1','VolleyIBleedFlight','VolleyIIBleedAim','ChainsILatchedLink','BasicWandPhysicalRelease','FootContactStone','DodgeAvoided']
cases=[]
for slug in slugs:
    originals=[case for case in plan if case['name'].startswith('All_'+slug+'_')]
    for case in originals:cases.append({**case,'name':case['name'].replace('All_','Diagnostic_',1)})
    if slug in ['CCStunActive','CCRootActive','FireBoltIIFlight','ChainsILatchedLink']:
        case=copy.deepcopy(next(case for case in originals if case['name'].endswith('_0')))
        cases.append({**case,'name':'Diagnostic_'+slug+'_age05','age':.5})
(root/'Evidence/runtime-render-diagnostic-cases.json').write_text(json.dumps(cases,indent=2),encoding='utf-8')
print(json.dumps({'cases':len(cases),'slugs':slugs}))
