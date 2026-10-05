"""Representative bright/Low, real link endpoints, terrain and whole-viewport cost checks."""
import pathlib,json,copy
root=pathlib.Path(__file__).resolve().parents[1]
plan=json.loads((root/'Evidence/runtime-capture-plan.json').read_text(encoding='utf-8'))
jobs=json.loads((root/'Evidence/gameplay-runtime-build-jobs.json').read_text(encoding='utf-8'))['jobs']
by_slug={job['slug']:job for job in jobs}
selected=['ContactPhysical','ContactMagical','GuardActive','GuardMitigation','DodgeAvoided','CCRootActive','FireBoltIFlight','FireBoltIIFlight','GlacialSpikeIAreaImpact','GlacialSpikeIiAreaImpact','ManaStormActive','AstralVeilActive','FullMoonAreaImpact','SicknessAreaImpact','PoisonSacActive','ArcaneWeavingIResource','ArcaneWeavingIiResource','ElementalWeaverIResource','ElementalWeaverIiResource','ManaBarrierIHold','ConnectionIiAllyActive','ConnectionIiEnemyActive']
cases=[]
for slug in selected:
    base=copy.deepcopy(next(case for case in plan if case['name']=='All_'+slug+'_0'))
    if slug in ['GlacialSpikeIAreaImpact','GlacialSpikeIiAreaImpact']:base['age']=1.1
    for background in ['Dark','Bright']:
        frame={**base,'bright':background=='Bright','name':'Quality_'+slug+'_'+background,'decorative_enabled':False}
        if 'Connection' in slug:frame.update(target_x=1000,target_y=250,target_z=100,camera_x=1100,camera_y=-1600,camera_z=1200,look_x=400)
        cases.append({**frame,'name':frame['name']+'_baseline','instances':0})
        cases.append(frame)
terrain=copy.deepcopy(next(case for case in plan if case['name']=='All_ContactPhysical_0'))
terrain.update(instances=0,camera_x=1300,camera_y=-1600,camera_z=1100,look_z=100)
for background in ['Dark','Bright']:
    cases.append({**terrain,'name':'Quality_Iceberg_'+background+'_baseline','bright':background=='Bright'})
    for integrity in [1,.25]:
        cases.append({**terrain,'name':'Quality_Iceberg_'+background+'_'+str(integrity),'bright':background=='Bright','terrain':True,'integrity':integrity})
(root/'Evidence/runtime-quality-cases.json').write_text(json.dumps(cases,indent=2),encoding='utf-8')
base=copy.deepcopy(next(case for case in plan if case['name']=='All_ArcaneWeavingIiResource_0'))
performance=[{**base,'name':'Perf_Arcane_'+str(count),'instances':count,'perf_frames':120} for count in [0,1,16,48]]
(root/'Evidence/runtime-performance-cases.json').write_text(json.dumps(performance,indent=2),encoding='utf-8')
print(json.dumps({'quality_cases':len(cases),'performance_cases':len(performance),'scope':'Low console profile plus decorative presentation disabled. Snapshot renderer bypasses scalability for stable QA; actual distance/instance culling and target hardware budgets remain separate.'}))
