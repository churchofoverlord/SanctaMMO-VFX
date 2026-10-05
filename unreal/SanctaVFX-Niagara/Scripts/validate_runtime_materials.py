"""Validate saved definitions independently of generation, with bounded cleanup."""
import unreal as u,json,pathlib,os
root=pathlib.Path(u.Paths.project_dir())
definitions=json.loads((root/'Evidence/gameplay-runtime-definitions.json').read_text(encoding='utf-8'))['definitions']
selection=os.environ.get('SANCTA_BINDINGS_REVALIDATE')=='1'
if selection:
    names=json.loads((root/'Saved/runtime-bindings-revalidation-plan.json').read_text(encoding='utf-8'))['revalidate']
    definitions=[definition for definition in definitions if definition['presentation_id'] in names]
limit=int(os.environ.get('SANCTA_BINDINGS_LIMIT','0'))
offset=int(os.environ.get('SANCTA_BINDINGS_OFFSET','0'))
definitions=definitions[offset:]
if limit:definitions=definitions[:limit]
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
results={}
for index,item in enumerate(definitions):
    definition=u.load_asset(item['asset']);phase=definition.get_editor_property('phases')[0]
    if phase.get_editor_property('gate') in [u.SanctaVFXGate.NATURAL_END,u.SanctaVFXGate.CLEANSE]:continue
    results[item['presentation_id']]=json.loads(u.SanctaVFXLabLibrary.validate_runtime_bindings(definition,world))
    if not results[item['presentation_id']]['passed']:raise RuntimeError('Bindings failed: '+item['presentation_id'])
    if index%16==15:u.SystemLibrary.collect_garbage()
report={'passed':all(result['passed'] for result in results.values()),'definitions_tested':len(results),'results':results,'scope':'First non-terminal phase of each saved definition; native all-phase rendering is checked separately.'}
report['offset']=offset
report['limit']=limit
output='Saved/runtime-material-subset.json' if limit or offset else 'Evidence/gameplay-runtime-material-validation.json'
if selection:output='Saved/runtime-material-revalidation.json'
(root/output).write_text(json.dumps(report,indent=2),encoding='utf-8')
u.log('SanctaRuntime material definitions passed '+str(len(results)))
