"""Run with Run-LabScript.ps1 commandlet; manual editor-world simulation is unsuitable here.

Build only ignored local rig variants; never update the general runtime index.
"""
import hashlib, json, pathlib, traceback, unreal as u

R = pathlib.Path(u.Paths.project_dir())
exec(compile((R/'Scripts/build_reference_ports.py').read_text(encoding='utf-8').split('\ntry:\n for item')[0], 'manny_material_helpers', 'exec'))
read = lambda p: json.loads((R/p).read_text(encoding='utf-8-sig'))
rows = read('Evidence/gameplay-manny-binding-sources.json')['rows']
output = {'assets': {}, 'failed': {}, 'production_approved': False, 'scope': 'Local Manny rig variants only.'}
prior_path = R/'Evidence/gameplay-manny-binding-assets.json'
prior = read(prior_path.relative_to(R)) if prior_path.exists() else {'assets': {}}
for row in rows:
    key = row['component']; job = row['job']
    try:
        path = (R/row['source']).with_suffix('.port.json')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        data = json.loads(path.read_text(encoding='utf-8-sig'))
        directory = '/Game/Sancta/VFX/MannyLab/'+key
        name = key+'_'+digest[:8]
        asset = directory+'/NS_'+name
        system = u.load_asset(asset)
        if system:
            old = prior['assets'].get(key, {})
            if old.get('port_sha256') != digest:
                raise RuntimeError('Unverified local rig variant preserved: '+asset)
            output['assets'][key] = old
            continue
        meshes = []; checks = []
        for index, layer in enumerate(data['layers']):
            mesh = import_file(layer['mesh_source'], '/Game/Sancta/VFX/MannyLab/Common/Meshes', layer['mesh_name'], True)
            material, check = native_material(layer, directory, 'MI_'+name+'_Layer'+str(index), job['duration'])
            meshes.append((layer, mesh, material)); checks.append(check)
        system = tools.create_asset('NS_'+name, directory, u.NiagaraSystem, u.NiagaraSystemFactoryNew())
        system.set_editor_property('effect_type', u.load_asset('/Game/Sancta/VFX/Common/Scalability/NET_'+job['importance']))
        box = u.Box(); box.set_editor_property('min', u.Vector(-600,-600,-300)); box.set_editor_property('max', u.Vector(600,600,900)); box.set_editor_property('is_valid', True)
        system.set_editor_property('bFixedBounds', True); system.set_editor_property('FixedBounds', box)
        for parameter, value in {'User.PlaybackRate': 1., 'User.CueLifetime': job['duration'], **data.get('runtime_parameters', {})}.items():
            if not LAB.set_user_float(system, parameter, float(value)):
                raise RuntimeError('Missing user parameter: '+parameter)
        context = FX.create_system_conversion_context(system)
        try:
            for index, (layer, mesh, material) in enumerate(meshes):
                layer['control_bindings'] = layer.get('control_bindings') or {'Y': 'User.RuntimeAge'}
                emitter_from_layer(context, layer, mesh, material, index, job['duration'])
            context.finalize()
            # Conversion can introduce User variables with zero defaults.
            # Reapply the owner defaults after finalizing the emitter graph.
            for parameter, value in {'User.PlaybackRate': 1., 'User.CueLifetime': job['duration'], 'User.RuntimeAge': 0.}.items():
                if not LAB.set_user_float(system, parameter, float(value)):
                    raise RuntimeError('Default parameter update failed: '+parameter)
            binding_count = LAB.configure_runtime_materials(system)
            if binding_count != len(meshes):
                raise RuntimeError('Incomplete private material bindings')
            inspection = json.loads(LAB.inspect_system(system))
            if not inspection['ready_to_run']:
                raise RuntimeError('Rig Niagara compile failed')
            simulation = json.loads(LAB.simulate_system(system, world, [.05, .2, job['duration']+.35]))
            (R/'Saved'/('Manny-simulation-'+key+'.json')).write_text(json.dumps({'inspection': inspection, 'simulation': simulation}, indent=2), encoding='utf-8')
            if not any(e['alive'] for f in simulation['frames'] for e in f['emitters']):
                raise RuntimeError('No simulated particles: '+json.dumps(simulation))
            assert job['persistent'] or not any(e['alive'] for e in simulation['frames'][-1]['emitters'])
            save(system)
        finally:
            context.cleanup()
        output['assets'][key] = {'asset': asset, 'source': row['source'], 'port_sha256': digest,
            'materials': checks, 'inspection': inspection, 'simulation': simulation, 'binding_count': binding_count,
            'status': 'local_native_compile_and_simulation_passed'}
        u.log('Manny rig variant saved: '+key)
    except Exception:
        output['failed'][key] = traceback.format_exc(); u.log_error(output['failed'][key])
    prior_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')
output['passed'] = len(output['assets']) == len(rows) and not output['failed']
prior_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')
if not output['passed']:
    u.log_error('Local Manny variants incomplete: '+json.dumps(output['failed']))
else:
    u.log('Manny rig variants complete: '+str(len(output['assets'])))
u.SystemLibrary.quit_editor()
