"""Build runtime assets under stable production folders; hash revisions preserve prior assets."""
import unreal as u,json,pathlib,hashlib,traceback,os,copy
R=pathlib.Path(u.Paths.project_dir())
exec(compile((R/'Scripts/build_reference_ports.py').read_text(encoding='utf-8').split('\ntry:\n for item')[0],'reference_helpers','exec'))
jobs=json.loads((R/'Evidence/gameplay-runtime-build-jobs.json').read_text(encoding='utf-8'))['jobs']
path=R/'Evidence/gameplay-runtime-native-assets.json'
result=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'assets':{},'failed':{},'production_approved':False}
selection=set(filter(None,os.environ.get('SANCTA_RUNTIME_SLUGS','').split(',')))
for job in jobs:
    slug=job['slug']
    if selection and slug not in selection:continue
    if (R/'Saved/Stop-gameplay-build.request').exists():break
    try:
        data=json.loads((R/job['source']).with_suffix('.port.json').read_text(encoding='utf-8'))
        data['runtime_emitter_revision']='identity_orientation_persistent_v2'
        for l in data['layers']:l['native_shared_root']='/Game/Sancta/VFX/Common'
        digest=hashlib.sha256((R/job['source']).read_bytes()).hexdigest()
        code_digest=hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
        prior=result['assets'].get(slug,{})
        if prior.get('port_sha256')==code_digest:
            existing=u.load_asset(prior['asset'])
            if existing:
                effect_type=u.load_asset('/Game/Sancta/VFX/Common/Scalability/NET_'+job['importance'])
                if not effect_type:raise RuntimeError('Scalability Effect Type missing')
                if existing.get_editor_property('effect_type')!=effect_type:
                    existing.set_editor_property('effect_type',effect_type);save(existing)
                prior['job']=job
                prior['source_sha256']=digest
                prior['source']=job['source']
                continue
        name=slug+'_'+code_digest[:8]
        group='Combat' if job['form'].startswith('Combat.') else 'Status' if job['form'].startswith('Status.') or slug.startswith('CC') else 'Skills'
        directory='/Game/Sancta/VFX/'+group+'/'+slug
        asset=directory+'/NS_'+name
        system=u.load_asset(asset) if u.EditorAssetLibrary.does_asset_exist(asset) else None
        if system:raise RuntimeError('Unverified existing asset preserved: '+asset)
        meshes=[];checks=[]
        for n,l in enumerate(data['layers']):
            mesh=import_file(l['mesh_source'],'/Game/Sancta/VFX/Common/Meshes',l['mesh_name'],True)
            material,check=native_material(l,directory,'MI_'+name+'_Layer'+str(n),job['duration'])
            meshes.append((l,mesh,material));checks.append(check)
        system=tools.create_asset('NS_'+name,directory,u.NiagaraSystem,u.NiagaraSystemFactoryNew())
        effect_type=u.load_asset('/Game/Sancta/VFX/Common/Scalability/NET_'+job['importance'])
        if not effect_type:raise RuntimeError('Scalability Effect Type missing')
        system.set_editor_property('effect_type',effect_type)
        # Runtime position comes from the owner. No recorded whole-flight world bounds.
        # Links/areas have explicit larger lab bounds pending target hardware scalability.
        margin=1200 if job.get('use_endpoint') or job['anchor']=='World' else 400
        box=u.Box();box.set_editor_property('min',u.Vector(-margin,-margin,-150));box.set_editor_property('max',u.Vector(margin,margin,700));box.set_editor_property('is_valid',True)
        system.set_editor_property('bFixedBounds',True);system.set_editor_property('FixedBounds',box)
        for key,value in {'User.PlaybackRate':1.,'User.CueLifetime':job['duration'],**data.get('runtime_parameters',{})}.items():
            if not LAB.set_user_float(system,key,float(value)):raise RuntimeError('Parameter creation failed '+key)
        ctx=FX.create_system_conversion_context(system)
        try:
            for n,(l,mesh,material) in enumerate(meshes):
                # CueLifetime controls every runtime particle, including states with no auto-expiry.
                l['control_bindings']=l.get('control_bindings') or {'Y':'User.RuntimeAge'}
                emitter_from_layer(ctx,l,mesh,material,n,job['duration'])
            ctx.finalize()
            bindings=LAB.configure_runtime_materials(system)
            if bindings!=len(meshes):raise RuntimeError('Runtime material bindings incomplete')
            inspection=json.loads(LAB.inspect_system(system))
            if not inspection['ready_to_run']:raise RuntimeError('Niagara compilation failed')
            sim=json.loads(LAB.simulate_system(system,world,[.04,.2,job['duration']+.35]))
            if not any(e['alive'] for f in sim['frames'] for e in f['emitters']) or (job['persistent'] and not all(e['alive'] for e in sim['frames'][-1]['emitters'])) or (not job['persistent'] and any(e['alive'] for e in sim['frames'][-1]['emitters'])):raise RuntimeError('Spawn/expiry failed')
            save(system)
        finally:ctx.cleanup()
        result['assets'][slug]={'asset':asset,'source':job['source'],'source_sha256':digest,'port_sha256':code_digest,
            'materials':checks,'material_bindings':bindings,'inspection':inspection,'simulation':sim,
            'status':'native_compile_and_cpu_simulation_passed','visual_review':'pending','runtime_event_test':'pending',
            'gpu_cost':'not_measured','job':job}
        result['failed'].pop(slug,None)
        u.log('SanctaGameplay SAVED '+slug)
    except Exception:
        result['failed'][slug]=traceback.format_exc();u.log_error('SanctaGameplay FAILED '+slug+' '+result['failed'][slug])
    path.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    u.SystemLibrary.collect_garbage()
current=[]
for job in jobs:
    data=json.loads((R/job['source']).with_suffix('.port.json').read_text(encoding='utf-8'))
    data['runtime_emitter_revision']='identity_orientation_persistent_v2'
    for layer in data['layers']:layer['native_shared_root']='/Game/Sancta/VFX/Common'
    entry=result['assets'].get(job['slug'],{})
    if entry.get('port_sha256')==hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest() and entry.get('source_sha256')==hashlib.sha256((R/job['source']).read_bytes()).hexdigest():current.append(job['slug'])
result['job_count']=len(jobs);result['saved_count']=len(current);result['historical_asset_count']=len(result['assets'])
result['pending']=[j['slug'] for j in jobs if j['slug'] not in current]
result['current_failures']={key:value for key,value in result['failed'].items() if key in result['pending']}
result['status']='native_compile_and_cpu_simulation_passed' if not result['pending'] else 'incomplete'
path.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
u.log('SanctaGameplay complete current='+str(len(current))+'/'+str(len(jobs))+' failed='+str(len(result['current_failures'])))
u.SystemLibrary.quit_editor()
