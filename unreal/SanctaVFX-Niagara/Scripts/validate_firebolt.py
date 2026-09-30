import unreal as u
import json, pathlib, traceback
root = pathlib.Path(u.Paths.project_dir())
report = {'status':'running'}
try:
    system = u.EditorAssetLibrary.load_asset('/Game/VFXLab/FireBoltI/NS_FireBoltI')
    if not system:
        raise RuntimeError('Fire Bolt system is missing')
    lab = u.SanctaVFXLabLibrary
    report['inspection'] = json.loads(lab.inspect_system(system))
    if not report['inspection']['ready_to_run'] or report['inspection']['emitter_count'] != 3:
        raise RuntimeError('Niagara system did not compile with three emitters')
    world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    times=[.05,.15,.3,.65,.8,.95,1.2,1.5]
    report['baseline'] = json.loads(lab.simulate_system(system,world,times))
    if 'error' in report['baseline']:
        raise RuntimeError(report['baseline']['error'])
    def frame_at(run,time):
        return min(run['frames'],key=lambda f:abs(f['time']-time))
    def emitter(frame,name):
        return next((e for e in frame['emitters'] if e['name']==name),{'alive':0})
    for name in ['Head','Tail']:
        if emitter(frame_at(report['baseline'],.3),name)['alive'] != 1:
            raise RuntimeError(name+' did not spawn during flight')
    if emitter(frame_at(report['baseline'],.8),'Impact')['alive'] != 1:
        raise RuntimeError('Impact did not spawn at arrival')
    if any(e['alive'] for e in frame_at(report['baseline'],1.5)['emitters']):
        raise RuntimeError('Particles did not finish')
    if not lab.set_user_float(system,'User.Speed',600):
        raise RuntimeError('Speed parameter could not be edited')
    report['half_speed'] = json.loads(lab.simulate_system(system,world,[.3,.65,.8,1.5,1.8]))
    before=emitter(frame_at(report['baseline'],.3),'Head')
    after=emitter(frame_at(report['half_speed'],.3),'Head')
    if after['alive'] != 1 or not (40 < after.get('first_x',0) < before.get('first_x',0)*.75):
        raise RuntimeError('Changing speed did not change projectile movement')
    report['checks']=['Three enabled emitters compiled','Head and tail spawn during flight','Impact spawns at arrival','All particles expire','User.Speed changes movement and arrival timing']
    if not emitter(frame_at(report['half_speed'],1.5),'Impact')['alive']:
        raise RuntimeError('Slower projectile did not delay the impact')
    report['status']='passed'
except Exception:
    report['status']='failed'
    report['error']=traceback.format_exc()
    u.log_error(report['error'])
finally:
    if 'system' in globals() and system:
        u.SanctaVFXLabLibrary.set_user_float(system,'User.Speed',1200)
        u.EditorAssetLibrary.save_loaded_asset(system)
        if 'world' in globals() and world:
            previews=root/'Previews'
            previews.mkdir(exist_ok=True)
            report['previews']={}
            for time,name in [(.3,'firebolt-flight.png'),(.65,'firebolt-tail.png'),(.8,'firebolt-impact.png')]:
                try:
                    report['previews'][name]=bool(u.SanctaVFXLabLibrary.capture_system(system,world,time,str(previews),name))
                except Exception:
                    report['previews'][name]=False
                    report.setdefault('capture_errors',{})[name]=traceback.format_exc()
    (root/'VFX-validation-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (root/'VFX-status.json').write_text(json.dumps({'status':report['status'], 'bridge_compiled':True, 'generated_system_saved':bool(system) if 'system' in globals() else False, 'simulation_verified':report['status']=='passed', 'visual_verified':False, 'previews_exported':report.get('previews',{})},indent=2),encoding='utf-8')
    u.log('VFX_VALIDATION '+report['status'])
    u.SystemLibrary.quit_editor()
