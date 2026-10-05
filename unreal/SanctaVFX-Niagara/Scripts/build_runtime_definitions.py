"""Create typed native definitions from validated systems. No demonstration systems in composition."""
import unreal as u,json,pathlib,hashlib,re,os
R=pathlib.Path(u.Paths.project_dir());tools=u.AssetToolsHelpers.get_asset_tools()
native=json.loads((R/'Evidence/gameplay-runtime-native-assets.json').read_text(encoding='utf-8'))
jobs=json.loads((R/'Evidence/gameplay-runtime-build-jobs.json').read_text(encoding='utf-8'))['jobs']
defs={};assets=[];pending=[]
current={}
def phase(job,entry):
    p=u.SanctaVFXPhase();p.set_editor_property('phase',job['phase']);p.set_editor_property('component_key',job['slug'])
    p.set_editor_property('system',u.load_asset(entry['asset']))
    for prop,typ,val in [('anchor',u.SanctaVFXAnchor,job['anchor']),('gate',u.SanctaVFXGate,job['gate']),('importance',u.SanctaVFXImportance,job['importance'])]:p.set_editor_property(prop,getattr(typ,re.sub(r'(?<!^)(?=[A-Z])','_',val).upper()))
    for prop,key,default in [('bPersistent','persistent',False),('bStateOwned','state_owned',job['phase'] not in ['Flight','Hold','Movement','Trail','Telegraph']),('bBindTargetLife','target_life',False),('bUseEndpoint','use_endpoint',False),('bUseRadius','use_radius',False),('bUseRange','use_range',False),('bUseConeAngle','use_cone_angle',False),('bContact','contact',False)]:p.set_editor_property(prop,job.get(key,default))
    p.set_editor_property('duration',float(job['duration']));p.set_editor_property('reference_radius',float(job.get('reference_radius',100)))
    p.set_editor_property('reference_range',float(job.get('reference_range',100)));p.set_editor_property('reference_cone_angle',float(job.get('reference_cone_angle',90)))
    return p
for j in jobs:
    n=native['assets'].get(j['slug'])
    data=json.loads((R/j['source']).with_suffix('.port.json').read_text(encoding='utf-8'));data['runtime_emitter_revision']='identity_orientation_persistent_v2'
    for l in data['layers']:l['native_shared_root']='/Game/Sancta/VFX/Common'
    digest=hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
    if not n or n['port_sha256']!=digest or n['source_sha256']!=hashlib.sha256((R/j['source']).read_bytes()).hexdigest():pending.append(j['slug']);continue
    current[j['slug']]=n
    defs.setdefault(j['form'],[]).append(phase(j,n))
    if j.get('parent_skill') and j['parent_skill']!=j['form']:
        # The alias keeps the original phase's lifecycle even when its display
        # name becomes the component key. Travel/preparation cannot own a status.
        alias={**j,'phase':j['slug'],'state_owned':j.get('state_owned',j['phase'] not in ['Flight','Hold','Movement','Trail','Telegraph'])}
        defs.setdefault(j['parent_skill'],[]).append(phase(alias,n))
# A confirmed sequence index selects the same mark regardless of skill rank.
for rank in ['severing-strike','severing-strike-ii','severing-strike-iii']:
    if rank not in defs:continue
    for mark in ['SeveringMark1','SeveringMark2','SeveringMark3']:
        job=next(j for j in jobs if j['slug']==mark)
        if mark in current:defs[rank].append(phase({**job,'phase':mark},current[mark]))
for family in json.loads((R/'Evidence/gameplay-vfx-assessment-20261004.json').read_text(encoding='utf-8'))['weapon_presentations']:
    name=''.join(x.title() for x in re.split(r'[- /]+',family['family']))
    for channel in ['Physical','Magical']:
        contact=current.get('Contact'+channel);form='Combat.Basic.'+name+'.'+channel
        if contact and form in defs:defs[form].append(phase({'slug':'Contact'+channel,'phase':'Impact','gate':'ConfirmedHit','anchor':'World','duration':.3,'importance':'Gameplay','contact':True,'target_life':True},contact))
for action in ['Sprint','Dodge']:
    for surface in ['Stone','Snow','Mud','Water']:
        n=current.get('FootContact'+surface)
        if n:
            p=phase({'slug':'FootContact'+surface,'phase':'FootContact','gate':'Admission','anchor':'World','duration':.5,'importance':'Decorative'},n)
            p.set_editor_property('required_surface',surface);defs.setdefault('Combat.'+action,[]).append(p)
# Canonical IDs reference the same verified systems, with admission snapshots.
routing=json.loads((R/'Evidence/gameplay-runtime-form-routes.json').read_text(encoding='utf-8'))
fields=['phase','component_key','system','anchor','gate','importance','bPersistent','bStateOwned','bBindTargetLife','bUseEndpoint','bUseRadius','bUseRange','bUseConeAngle','bContact','contact_priority','required_proc_mask','required_surface','duration','reference_radius','reference_range','reference_cone_angle','scalar_defaults','required_mode_snapshot','required_stance_snapshot','required_relation']
canonical_pending=[]
for route in routing['routes']:
    if any(x['presentation'] not in defs for x in route['sources']):canonical_pending.append(route['form_id']);continue
    composed=[]
    for source in route['sources']:
        for original in defs[source['presentation']]:
            p=u.SanctaVFXPhase()
            for field in fields:p.set_editor_property(field,original.get_editor_property(field))
            if source.get('required_stance_snapshot'):p.set_editor_property('required_stance_snapshot',source['required_stance_snapshot'])
            if route['form_id'].startswith('mage.') and route['form_id'].rsplit('.',1)[-1] in ['manifest','weave'] and route['kind']=='execution':p.set_editor_property('required_mode_snapshot',route['form_id'].rsplit('.',1)[-1].title())
            if route['form_id'].rsplit('.',1)[-1] in ['ally','enemy']:p.set_editor_property('required_relation',route['form_id'].rsplit('.',1)[-1].title())
            composed.append(p)
    defs[route['form_id']]=composed
# Shared status compositions also have one owner and explicit terminal causes.
for status in ['Stun','Root','Silence','Fear','Sleep','Taunt']:
    phases=[]
    for suffix in ['Active','Apply','NaturalEnd','Cleanse']:
        phases+=defs.get('Component.CC'+status+suffix,[])
    if phases:defs['Status.CC.'+status]=phases
if 'arcane-weaving-i' in defs:defs['Status.Resource.ArcaneShards']=defs['arcane-weaving-i']
for form,phases in defs.items():
    directory='/Game/Sancta/VFX/Definitions';name='DA_'+re.sub(r'[^A-Za-z0-9_]','_',form)
    obj=u.load_asset(directory+'/'+name) if u.EditorAssetLibrary.does_asset_exist(directory+'/'+name) else None
    if not obj:
        f=u.DataAssetFactory();f.set_editor_property('data_asset_class',u.SanctaVFXDefinition)
        obj=tools.create_asset(name,directory,u.SanctaVFXDefinition,f)
    obj.set_editor_property('form_id',form);obj.set_editor_property('composition_version',2);obj.set_editor_property('phases',phases)
    composition=[{field:(p.get_editor_property(field).get_path_name() if field=='system' else str(p.get_editor_property(field))) for field in fields} for p in phases]
    obj.set_editor_property('source_hash',hashlib.sha256(json.dumps({'form':form,'phases':composition},sort_keys=True).encode()).hexdigest())
    if not u.EditorAssetLibrary.save_loaded_asset(obj):raise RuntimeError('Definition not saved '+form)
    assets.append({'presentation_id':form,'asset':obj.get_path_name(),'phases':len(phases),'source_hash':obj.get_editor_property('source_hash'),'phase_details':composition})
(R/'Evidence/gameplay-runtime-definitions.json').write_text(json.dumps({'definitions':assets,'pending_components':pending,'canonical_form_routing':'Stable handed-off identities, separate production presentation IDs; current mechanics override old travel/timer metadata.','canonical_routes':len(routing['routes']),'canonical_pending':canonical_pending},indent=2,ensure_ascii=False),encoding='utf-8')
if os.environ.get('SANCTA_SKIP_MATERIAL_VALIDATION')!='1':
    world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();results={}
    for d in assets:
        obj=u.load_asset(d['asset']);p=obj.get_editor_property('phases')[0]
        if p.get_editor_property('gate') in [u.SanctaVFXGate.NATURAL_END,u.SanctaVFXGate.CLEANSE]:continue
        results[d['presentation_id']]=json.loads(u.SanctaVFXLabLibrary.validate_runtime_bindings(obj,world))
        u.log('SanctaRuntimeBindings '+d['presentation_id']+' '+str(results[d['presentation_id']]['passed']))
    (R/'Evidence/gameplay-runtime-material-validation.json').write_text(json.dumps({'passed':all(v['passed'] for v in results.values()),'definitions_tested':len(results),'results':results},indent=2),encoding='utf-8')
# The Python commandlet owns shutdown after this script returns. Do not request
# editor shutdown while package saves/material validations are still unwinding.
