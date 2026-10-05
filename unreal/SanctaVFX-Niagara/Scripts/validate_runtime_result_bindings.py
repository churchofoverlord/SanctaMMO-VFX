"""Inspect actual live materials of a selected result phase, not only alias phase zero."""
import json,pathlib
import unreal as u
root=pathlib.Path(u.Paths.project_dir())
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
rows={}
for form,phase in [('pressure-provoke','Impact'),('pressure-provoke-tank','Impact')]:
    asset='/Game/Sancta/VFX/Definitions/DA_'+form.replace('-','_')
    original=u.load_asset(asset)
    selected=[p for p in original.get_editor_property('phases') if str(p.get_editor_property('phase'))==phase]
    if len(selected)!=1:raise RuntimeError('Result phase missing: '+form)
    transient=u.SanctaVFXDefinition()
    transient.set_editor_property('form_id',form)
    transient.set_editor_property('phases',selected)
    rows[form+'/'+phase]=json.loads(u.SanctaVFXLabLibrary.validate_runtime_bindings(transient,world))
report={'passed':all(row['passed'] for row in rows.values()),'results':rows,'scope':'Native live material objects/inputs of the isolated Pressure/Provoke result phase; appearance is audited separately.'}
(root/'Evidence/gameplay-runtime-result-binding-diagnostic.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
if not report['passed']:raise RuntimeError('Isolated result bindings failed')
u.log('SanctaRuntime result phase bindings passed')
