"""Check saved phase contracts against confirmed-result and owner requirements."""
import json,pathlib,datetime
root=pathlib.Path(__file__).resolve().parents[1]
read=lambda p:json.loads((root/p).read_text(encoding='utf-8-sig'))
jobs=read('Evidence/gameplay-runtime-build-jobs.json')['jobs']
definitions=read('Evidence/gameplay-runtime-definitions.json')['definitions']
by_name={job['slug']:job for job in jobs}
checks=[]
def check(name,passed):checks.append({'requirement':name,'passed':bool(passed)})
def contract(slug,phase,anchor,gate,persistent=False):
    job=by_name.get(slug,{})
    check(slug+' event/owner/gate',all(job.get(k)==v for k,v in {'phase':phase,'anchor':anchor,'gate':gate,'persistent':persistent}.items()))
contract('WarLeapAreaImpact','AreaImpact','World','Applied')
contract('WarLeapTelegraph','Telegraph','World','Admission',True)
contract('WarLeapMovement','Movement','Source','Admission',True)
contract('LongJumpHold','Hold','Link','Admission',True)
contract('LongJumpTelegraph','Telegraph','World','Admission',True)
contract('DefiantPresenceActive','Active','World','Applied',True)
for prefix in ['CrushingBlow','CrushingBlowIi','SmokeBombI','SmokeBombIi','CombustIi']:
    contract(prefix+'AreaImpact','AreaImpact','World','Applied')
for prefix in ['ShoulderRush','ShoulderRushIiTank','ShoulderRushIiWarrior']:
    contract(prefix+'Impact','Impact','Target','ConfirmedHit')
for prefix in ['Cleanse','Cleansemage','Cleansemystic','Cleansescout']:
    contract(prefix+'Apply','Apply','Target','Applied')
contract('EvasionProc','Proc','Source','Applied')
for name in ['PressureProvokeImpact','PressureProvokeTankImpact']:
    contract(name,'Impact','World','ConfirmedHit')
    check(name+' contact position keeps confirmed target life',by_name[name]['contact'] and by_name[name]['target_life'])
contract('SandShotCast','Cast','World','Admission')
contract('SandShotImpact','Impact','World','ConfirmedHit')
check('Sand Shot has one confirmed contact and no timed phantom targets',sum(layer['count'] for layer in read(by_name['SandShotImpact']['source'])['layers'])==1 and len(read(by_name['SandShotCast']['source'])['layers'])==2)
for prefix in ['BleedStance','PoisonStance']:
    contract(prefix+'Active','Active','Link','Applied',True)
for prefix in ['ThunderstrikeI','ThunderstrikeIi']:
    contract(prefix+'Strike','Strike','World','Applied')
contract('VortexDisplacement','Displacement','Target','Applied')
contract('AstralPullLink','Link','Link','Applied')
contract('AstralPullRelocate','Relocate','Target','Applied')
check('Severing has no duplicate hit flashes',not any(name.startswith('SeveringHit') for name in by_name))
for name in ['PiercingStrikeImpact','PiercingStrikeIiTankImpact','PiercingStrikeIiWarriorImpact']:
    source=read(by_name[name]['source'])
    check(name+' is one contact per confirmed target',sum(layer['count'] for layer in source['layers'])==1)
selected=[]
for definition in definitions:
    for phase in definition['phase_details']:
        key=phase['component_key']
        if key not in by_name:continue
        selected.append(key)
        job=by_name[key]
        if job['phase'] in ['Hold','Telegraph','Flight','Movement','Trail']:
            check(definition['presentation_id']+'/'+key+' ends with execution',phase['bStateOwned']=='False')
        if job['anchor']=='Link':check(definition['presentation_id']+'/'+key+' binds endpoint',phase['bUseEndpoint']=='True')
        if job['anchor']=='Target':check(definition['presentation_id']+'/'+key+' binds target life',phase['bBindTargetLife']=='True')
check('Every current component appears in saved definitions',set(selected)==set(by_name))
report={'passed':all(row['passed'] for row in checks),'checks':checks,'current_components':len(jobs),'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Saved definition and source contracts; native execution/lifecycle, actual render and rig placement have separate evidence.'}
(root/'Evidence/gameplay-runtime-phase-contracts.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'passed':report['passed'],'checks':len(checks),'failed':[row['requirement'] for row in checks if not row['passed']]}))
if not report['passed']:raise RuntimeError('Saved phase contract audit failed')
