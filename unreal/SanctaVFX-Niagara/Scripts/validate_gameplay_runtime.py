"""Execute native presentation tests in the independent lab, with a real compiled system."""
import unreal as u, pathlib, json, hashlib
r=pathlib.Path(u.Paths.project_dir())
c=json.loads((r/'VFX-catalog.json').read_text(encoding='utf-8'))
item=next(i for i in c['items'] if i['slug']=='fire-bolt-i')
system=u.load_asset(item['ue_asset'])
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
result=json.loads(u.SanctaVFXLabLibrary.validate_presentation_runtime(system,world))
result['system']=item['ue_asset']
result['module_sha256']=hashlib.sha256((r/'Plugins/SanctaVFXBridge/Binaries/Win64/UnrealEditor-SanctaVFXRuntime.dll').read_bytes()).hexdigest()
(r/'Evidence/gameplay-runtime-native-validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
u.log('SanctaRuntime validation '+str(result.get('passed')))
if not result.get('passed'):raise RuntimeError(json.dumps(result))
u.SystemLibrary.quit_editor()
