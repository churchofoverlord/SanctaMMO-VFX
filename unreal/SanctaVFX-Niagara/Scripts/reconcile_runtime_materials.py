"""Revalidate changed first phases; preserve only unchanged, verified binding results."""
import argparse,datetime,json,pathlib
from runtime_capture_signatures import CaptureSignatures
root=pathlib.Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('action',choices=['snapshot','prepare','finish']);args=parser.parse_args()
read=lambda p:json.loads((root/p).read_text(encoding='utf-8-sig'))
write=lambda p,data:(root/p).write_text(json.dumps(data,indent=2),encoding='utf-8')
signatures=CaptureSignatures(root)
definitions=read('Evidence/gameplay-runtime-definitions.json')['definitions']
current={}
for definition in definitions:
    phase=definition['phase_details'][0]
    if any(token in phase['gate'] for token in ['NATURAL_END','CLEANSE']):continue
    current[definition['presentation_id']]=signatures.signature({'definition':definition['asset'],'phase':phase['phase']})
baseline_path='Evidence/runtime-material-bindings-before-phase-repairs.json'
plan_path='Saved/runtime-bindings-revalidation-plan.json'
if args.action=='snapshot':
    report=read('Evidence/gameplay-runtime-material-validation.json')
    if not report['passed'] or set(report['results'])!=set(current):raise RuntimeError('Existing binding report does not cover this snapshot')
    write(baseline_path,{'signatures':current,'render_context':signatures.render_context,'report':report})
    print(json.dumps({'snapshotted':len(current)}))
elif args.action=='prepare':
    baseline=read(baseline_path)
    baselines=[baseline]
    report=read('Evidence/gameplay-runtime-material-validation.json')
    if report.get('passed') and report.get('phase_dependency_signatures'):
        baselines.append({'signatures':report['phase_dependency_signatures'],'render_context':report.get('render_context'),'report':report})
    reused={}
    for previous in baselines:
        if previous['render_context']!=signatures.render_context:continue
        for name,digest in current.items():
            result=previous['report']['results'].get(name)
            if previous['signatures'].get(name)==digest and result and result['passed']:reused[name]=result
    changed=[name for name in current if name not in reused]
    write(plan_path,{'current_signatures':current,'render_context':signatures.render_context,'revalidate':changed,'reused_results':reused})
    print(json.dumps({'reused':len(reused),'revalidate':changed}))
else:
    plan=read(plan_path);tested=read('Saved/runtime-material-revalidation.json')
    if not tested['passed'] or set(tested['results'])!=set(plan['revalidate']):raise RuntimeError('Changed binding validation is incomplete')
    if plan['current_signatures']!=current or plan['render_context']!=signatures.render_context:raise RuntimeError('Sources changed during binding validation')
    results={**plan['reused_results'],**tested['results']}
    report={'passed':all(row['passed'] for row in results.values()),'definitions_tested':len(results),'results':results,'phase_dependency_signatures':current,'render_context':signatures.render_context,'reused_unchanged_definitions':len(plan['reused_results']),'retested_changed_definitions':len(tested['results']),'revalidation_runs':tested.get('runs',[]),'validated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'First non-terminal phase of every current definition. Unchanged results retain exact phase/material/mesh/texture/input fingerprints from 17 successful bounded UE runs; changed phases were retested in bounded successful UE processes. All-phase rendering is audited separately.'}
    write('Evidence/gameplay-runtime-material-validation.json',report)
    print(json.dumps({'passed':report['passed'],'definitions':len(results),'retested':len(tested['results'])}))
