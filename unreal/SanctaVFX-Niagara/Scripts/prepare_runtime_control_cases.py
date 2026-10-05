"""Visual checks of resource occupancy, elemental colors and a held cast."""
import json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
plan=json.loads((root/'Evidence/runtime-capture-plan.json').read_text(encoding='utf-8'))
variants={
 'ArcaneWeavingIResource':[('Empty',{'count':0,'max':2}),('Full',{'count':2,'max':2})],
 'ArcaneWeavingIiResource':[('Empty',{'count':0,'max':10}),('Half',{'count':5,'max':10}),('Full',{'count':10,'max':10})],
 'ElementalWeaverIResource':[('Empty',{'occupied':0}),('OneFire',{'occupied':1,'element_a':0}),('FirePair',{'occupied':3,'element_a':0,'element_b':0}),('IcePair',{'occupied':3,'element_a':1,'element_b':1}),('LightningPair',{'occupied':3,'element_a':2,'element_b':2})],
 'ElementalWeaverIiResource':[('Empty',{'occupied':0}),('OneFire',{'occupied':1,'element_a':0}),('FireIce',{'occupied':3,'element_a':0,'element_b':1}),('IceLightning',{'occupied':3,'element_a':1,'element_b':2}),('LightningFire',{'occupied':3,'element_a':2,'element_b':0})],
 'ManaBarrierIHold':[('Early',{'hold':.1}),('Middle',{'hold':.5}),('Ready',{'hold':1.})],
 'ManaBarrierIiOverchargeHold':[('Early',{'hold':.1}),('Middle',{'hold':.5}),('Ready',{'hold':1.})],
}
cases=[]
for slug,states in variants.items():
    base=next(case for case in plan if case['name']=='All_'+slug+'_0')
    base={**base,'age':8.,'gain_age':-1.,'release':-1.}
    cases.append({**base,'name':'Controls_'+slug+'_baseline','instances':0})
    for label,values in states:cases.append({**base,**values,'name':'Controls_'+slug+'_'+label})
(root/'Evidence/runtime-control-cases.json').write_text(json.dumps(cases,indent=2),encoding='utf-8')
print(json.dumps({'control_cases':len(cases),'scope':'Actual shader snapshots of empty/occupied resources, three elemental colors and cast progress held at eight seconds; transport and real rigs remain separate.'}))
