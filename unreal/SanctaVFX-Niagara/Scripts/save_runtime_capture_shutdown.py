"""Preserve an interrupted capture run separately from final acceptance evidence."""
import datetime, hashlib, json, pathlib, re

root=pathlib.Path(__file__).resolve().parents[1]
log_path=root/'Saved/Runtime-all-verified-render-20261005.log'
log=log_path.read_text(encoding='utf-8-sig',errors='replace')
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
read=lambda path:json.loads((root/path).read_text(encoding='utf-8-sig'))
matches=re.findall(r'capture: (All_\w+)\.png saved=1 particles=(\d+) active=(\d+)',log)
frames=[]
missing=[]
for name,particles,active in matches:
    path=root/'Saved/RuntimeCaptures'/(name+'.png')
    if not path.is_file():
        missing.append(name)
        continue
    frames.append({'name':name,'file':path.relative_to(root).as_posix(),'sha256':sha(path),'bytes':path.stat().st_size,'particles':int(particles),'active':int(active)})
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
report={'schema':'sancta-runtime-interrupted-capture/v1','saved_at_utc':stamp,'status':'paused_by_user','reason':'prepara-te que vou ter de desligar','owned_ue_pid':28588,'owned_ue_stopped':True,'ue_exit_code':-1,'background_running':False,'log':log_path.relative_to(root).as_posix(),'log_sha256':sha(log_path),'completed_frames':len(frames),'planned_cases':len(read('Evidence/runtime-review-cases.json')) if isinstance(read('Evidence/runtime-review-cases.json'),list) else None,'missing_pngs':missing,'last_saved_frame':frames[-1]['name'] if frames else None,'frames':frames,'context_sha256':{path:sha(root/path) for path in ['Evidence/gameplay-runtime-build-jobs.json','Evidence/gameplay-runtime-definitions.json','Evidence/gameplay-runtime-compiled-sources.json','Evidence/runtime-capture-plan.json','Plugins/SanctaVFXBridge/Source/SanctaVFXBridge/Private/SanctaVFXRuntimeReview.cpp']},'accepted_final_qa':False,'full_capture_registry_updated':False,'remaining':'Investigate provisional empty frames before completing full capture and quality/performance plans.','export_requires_refresh':True,'git_commit_push_pending':True}
plan=read('Evidence/runtime-review-cases.json')
if isinstance(plan,dict):
    report['planned_cases']=len(plan.get('cases',[]))
(root/'Evidence/runtime-capture-partial-shutdown-20261005.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
interruptions=read('Evidence/runtime-capture-interruption-20261005.json')
interruptions.setdefault('user_shutdowns',[]).append({key:report[key] for key in ['saved_at_utc','owned_ue_pid','owned_ue_stopped','ue_exit_code','background_running','log','completed_frames','last_saved_frame','accepted_final_qa']})
(root/'Evidence/runtime-capture-interruption-20261005.json').write_text(json.dumps(interruptions,indent=2),encoding='utf-8')
print(json.dumps({'saved':True,'partial_frames':len(frames),'missing':missing,'last_frame':report['last_saved_frame']}))
