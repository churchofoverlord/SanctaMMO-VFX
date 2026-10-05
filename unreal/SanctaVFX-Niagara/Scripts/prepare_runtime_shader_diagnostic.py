"""Paired captures of previously empty phases, without modifying source art."""
import copy, json, pathlib
root=pathlib.Path(__file__).resolve().parents[1]
plan=json.loads((root/'Evidence/runtime-review-cases.json').read_text(encoding='utf-8'))
slugs=['BasicSwordMagicalTrail','BasicAxePhysicalTrail','FireBoltIISpread','FrostLanceIImpact','TempestIce','SpiritOfTheStarSunState']
cases=[]
for slug in slugs:
    originals=[case for case in plan if case['name'].startswith('All_'+slug+'_')]
    for case in originals:cases.append({**case,'name':case['name'].replace('All_','ShaderReady_',1)})
    if slug=='TempestIce':
        case=copy.deepcopy(next(case for case in originals if case['name'].endswith('_0')))
        cases.append({**case,'name':'ShaderReady_'+slug+'_age2','age':2.})
(root/'Evidence/runtime-shader-diagnostic-cases.json').write_text(json.dumps(cases,indent=2),encoding='utf-8')
print(json.dumps({'cases':len(cases),'slugs':slugs}))
