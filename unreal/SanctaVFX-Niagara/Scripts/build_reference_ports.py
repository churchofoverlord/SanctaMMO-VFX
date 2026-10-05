"""Build experimental native Niagara ports from recorded reference authoring data."""
import unreal as u
import pathlib, json, traceback, os, hashlib, datetime

ROOT=pathlib.Path(u.Paths.project_dir())
catalog_path=ROOT/'VFX-catalog.json'
catalog=json.loads(catalog_path.read_text(encoding='utf-8-sig'))
helpers=(ROOT/'Scripts/build_firebolt.py').read_text(encoding='utf-8')
exec(compile(helpers.split('\ntry:\n')[0],'converter_helpers','exec'))
OUTPUT=ROOT/'VFX-native-port-report.json'
evidence=json.loads(OUTPUT.read_text(encoding='utf-8-sig')) if OUTPUT.exists() else {'method':'experimental_reference_shader_port','assets':{},'failed':{}}
tools=u.AssetToolsHelpers.get_asset_tools()
lib=u.MaterialEditingLibrary
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
selected=set(filter(None,os.environ.get('SANCTA_PORT_SLUG','').split(',')))
preview_v2=set(filter(None,os.environ.get('SANCTA_PORT_PREVIEW_V2','').split(',')))

def save(asset):
    if not asset or not u.EditorAssetLibrary.save_loaded_asset(asset):raise RuntimeError('Asset not saved')
    return asset

def import_file(source,directory,name,mesh=False):
    path=directory+'/'+name
    existing=u.load_asset(path)
    if existing:return existing
    task=u.AssetImportTask()
    task.set_editor_property('filename',str(ROOT/source))
    task.set_editor_property('destination_path',directory)
    task.set_editor_property('destination_name',name)
    task.set_editor_property('automated',True)
    task.set_editor_property('save',True)
    if mesh:
        task.set_editor_property('factory',u.FbxFactory())
        options=u.FbxImportUI()
        options.set_editor_property('import_mesh',True)
        options.set_editor_property('import_materials',False)
        options.set_editor_property('import_textures',False)
        options.set_editor_property('import_as_skeletal',False)
        data=options.get_editor_property('static_mesh_import_data')
        data.set_editor_property('convert_scene',False)
        data.set_editor_property('convert_scene_unit',False)
        data.set_editor_property('auto_generate_collision',False)
        data.set_editor_property('normal_import_method',u.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS)
        task.set_editor_property('options',options)
    tools.import_asset_tasks([task])
    asset=u.load_asset(path)
    if not asset:raise RuntimeError('Import failed: '+source)
    if not mesh:
        asset.set_editor_property('srgb',False)
        save(asset)
    return asset

def expression(m,kind,property_values=None):
    node=lib.create_material_expression(m,kind,0,0)
    for key,value in (property_values or {}).items():node.set_editor_property(key,value,notify_mode=u.PropertyAccessChangeNotifyMode.NEVER)
    return node

def custom(m,code,kind,inputs):
    node=expression(m,u.MaterialExpressionCustom,{'code':code,'output_type':kind})
    definitions=[]
    for name in inputs:
        definition=u.CustomInput();definition.set_editor_property('input_name',name);definitions.append(definition)
    node.set_editor_property('inputs',definitions,notify_mode=u.PropertyAccessChangeNotifyMode.NEVER)
    for name,(value,pin) in inputs.items():
        if not lib.connect_material_expressions(value,pin,node,name):raise RuntimeError('Material connection failed: '+name)
    return node

def native_master(layer,directory,name,duration):
    path=directory+'/'+name
    revision=hashlib.sha256((material_signature(layer)+str(duration)).encode()).hexdigest()
    m=u.load_asset(path)
    if m:
        if u.EditorAssetLibrary.get_metadata_tag(m,'SanctaPortRevision')==revision:
            checked=json.loads(LAB.validate_material(m,world))
            if checked['passed']:return m,checked
        # Rebuild an experimental material graph in place after correcting its source.
        lib.delete_all_material_expressions(m)
    else:m=tools.create_asset(name,directory,u.Material,u.MaterialFactoryNew())
    lit=layer.get('lighting','unlit').startswith('default_lit')
    m.set_editor_property('blend_mode',u.BlendMode.BLEND_MASKED if lit else (u.BlendMode.BLEND_ADDITIVE if layer['blending']==2 else (u.BlendMode.BLEND_ALPHA_COMPOSITE if layer['blending']==5 else u.BlendMode.BLEND_TRANSLUCENT)),notify_mode=u.PropertyAccessChangeNotifyMode.NEVER)
    m.set_editor_property('shading_model',u.MaterialShadingModel.MSM_DEFAULT_LIT if lit else u.MaterialShadingModel.MSM_UNLIT,notify_mode=u.PropertyAccessChangeNotifyMode.NEVER)
    m.set_editor_property('two_sided',True,notify_mode=u.PropertyAccessChangeNotifyMode.NEVER)
    m.set_editor_property('used_with_niagara_mesh_particles',True,notify_mode=u.PropertyAccessChangeNotifyMode.NEVER)
    nodes={
      'UV':(expression(m,u.MaterialExpressionTextureCoordinate),''),
      'ScreenUV':(expression(m,u.MaterialExpressionScreenPosition),''),
      'Age':(expression(m,u.MaterialExpressionParticleRelativeTime),''),
      'Duration':(expression(m,u.MaterialExpressionScalarParameter,{'parameter_name':'SourceDuration','default_value':duration}),''),
      'TimeOrigin':(expression(m,u.MaterialExpressionScalarParameter,{'parameter_name':'SourceTimeOrigin','default_value':layer.get('preview_time_origin',layer['cast_time'])}),''),
      'Index':(expression(m,u.MaterialExpressionDynamicParameter,{'param_names':['ReferenceIndex','Unused1','Unused2','Unused3'],'default_value':u.LinearColor(0,0,0,0)}),''),
      'WorldPosition':(expression(m,u.MaterialExpressionWorldPosition,{'world_position_shader_offset':u.WorldPositionIncludedOffsets.WPT_EXCLUDE_ALL_SHADER_OFFSETS}),''),
      'ParticlePosition':(expression(m,u.MaterialExpressionParticlePositionWS),''),
      'CameraPosition':(expression(m,u.MaterialExpressionCameraPositionWS),''),
      'ViewportSize':(expression(m,u.MaterialExpressionViewSize),''),
      'Normal':(expression(m,u.MaterialExpressionPixelNormalWS),'')}
    if layer.get('runtime_uniforms'):
        controls=expression(m,u.MaterialExpressionDynamicParameter,{'param_names':['ReferenceIndex','ControlY','ControlZ','ControlW'],'default_value':u.LinearColor(0,0,1,1)})
        outputs=list(lib.get_material_expression_output_names(controls))
        if len(outputs)<4:raise RuntimeError('Dynamic parameter requires four native scalar outputs: '+str(outputs))
        for index,pin in enumerate(('ControlY','ControlZ','ControlW'),1):nodes[pin]=(controls,outputs[index])
    for key,value in layer.get('runtime_shader_inputs',{}).items():
        if isinstance(value,list):
            nodes[key]=(expression(m,u.MaterialExpressionVectorParameter,{'parameter_name':key,'default_value':u.LinearColor(*value)}),'')
        else:
            nodes[key]=(expression(m,u.MaterialExpressionScalarParameter,{'parameter_name':key,'default_value':value}),'')
    for texture in layer['texture_inputs']:
        source=layer['uniforms'][texture]
        if texture=='uBG' and not source.get('texture_source'):
            nodes[texture]=(expression(m,u.MaterialExpressionSceneColor),'')
            continue
        if not source.get('texture_source'):raise RuntimeError('Scene texture needs native material mapping: '+texture)
        asset=import_file(source['texture_source'],layer.get('native_shared_root','/Game/VFXLab/ReferenceShared')+'/Textures',source['texture_name'])
        nodes[texture]=(expression(m,u.MaterialExpressionTextureObjectParameter,{'parameter_name':texture,'texture':asset}),'')
    if layer.get('attribute_texture'):
        info=layer['attribute_texture'];asset=import_file(info['source'],layer.get('native_shared_root','/Game/VFXLab/ReferenceShared')+'/Textures',info['name'])
        asset.set_editor_property('compression_settings',u.TextureCompressionSettings.TC_VECTOR_DISPLACEMENTMAP)
        asset.set_editor_property('mip_gen_settings',u.TextureMipGenSettings.TMGS_NO_MIPMAPS)
        asset.set_editor_property('never_stream',True)
        save(asset)
        nodes['AttributeData']=(expression(m,u.MaterialExpressionTextureObjectParameter,{'parameter_name':'AttributeData','texture':asset}),'')
    pixel=custom(m,layer['hlsl'],u.CustomMaterialOutputType.CMOT_FLOAT4,nodes)
    rgb=expression(m,u.MaterialExpressionComponentMask,{'r':True,'g':True,'b':True,'a':False})
    alpha=expression(m,u.MaterialExpressionComponentMask,{'r':False,'g':False,'b':False,'a':True})
    if not lib.connect_material_expressions(pixel,'',rgb,''):raise RuntimeError('RGB mask connection failed')
    if not lib.connect_material_expressions(pixel,'',alpha,''):raise RuntimeError('Alpha mask connection failed')
    lib.connect_material_property(rgb,'',u.MaterialProperty.MP_BASE_COLOR if lit else u.MaterialProperty.MP_EMISSIVE_COLOR)
    lib.connect_material_property(alpha,'',u.MaterialProperty.MP_OPACITY_MASK if lit else u.MaterialProperty.MP_OPACITY)
    if lit:
        roughness=expression(m,u.MaterialExpressionConstant,{'r':.9})
        lib.connect_material_property(roughness,'',u.MaterialProperty.MP_ROUGHNESS)
        m.set_editor_property('tangent_space_normal',False,notify_mode=u.PropertyAccessChangeNotifyMode.NEVER)
    vertex_nodes=dict(nodes)
    vertex_nodes.pop('ScreenUV')
    if 'uBG' in vertex_nodes and not layer['uniforms']['uBG'].get('texture_source'):vertex_nodes.pop('uBG')
    vertex_nodes['Normal']=(expression(m,u.MaterialExpressionVertexNormalWS),'')
    vertex=custom(m,layer['hlsl_vertex'],u.CustomMaterialOutputType.CMOT_FLOAT3,vertex_nodes)
    lib.connect_material_property(vertex,'',u.MaterialProperty.MP_WORLD_POSITION_OFFSET)
    if lit and layer.get('hlsl_normal'):
        normal=custom(m,layer['hlsl_normal'],u.CustomMaterialOutputType.CMOT_FLOAT3,vertex_nodes)
        lib.connect_material_property(normal,'',u.MaterialProperty.MP_NORMAL)
    lib.recompile_material(m)
    checked=json.loads(LAB.validate_material(m,world))
    if not checked['passed']:raise RuntimeError(json.dumps(checked,ensure_ascii=False))
    u.EditorAssetLibrary.set_metadata_tag(m,'SanctaPortRevision',revision)
    save(m)
    return m,checked

def material_signature(layer):
    signature=layer['hlsl']+layer['hlsl_vertex']+str(layer['blending'])+layer.get('lighting','unlit')
    if layer.get('hlsl_normal'):signature+='\n// Source-deformed world normal\n'+layer['hlsl_normal']
    if layer.get('runtime_uniforms'):signature+='\n// Runtime controls graph schema 3: scalar outputs precede RGB/RGBA'
    if layer.get('runtime_shader_inputs'):signature+='\n// Runtime owner schema 1 '+json.dumps(layer['runtime_shader_inputs'],sort_keys=True)
    return signature

def native_material(layer,directory,name,duration):
    # Recorded attributes, atlas textures and timing remain per-effect instance values.
    # Share a shader only when its full generated code and blending/lighting match.
    key=hashlib.sha256(material_signature(layer).encode()).hexdigest()[:24]
    shared=layer.get('native_shared_root','/Game/VFXLab/ReferenceShared')+'/Materials'
    master=u.load_asset(shared+'/M_Reference_'+key)
    if master:
        checked=json.loads(LAB.validate_material(master,world))
        if not checked['passed']:raise RuntimeError(json.dumps(checked))
    else:master,checked=native_master(layer,shared,'M_Reference_'+key,duration)
    instance=u.load_asset(directory+'/'+name)
    if instance and not isinstance(instance,u.MaterialInstanceConstant):
        # Preserve a previous experimental base material; use a distinct instance path.
        name='MI_'+name[2:]
        instance=u.load_asset(directory+'/'+name)
    if not instance:instance=tools.create_asset(name,directory,u.MaterialInstanceConstant,u.MaterialInstanceConstantFactoryNew())
    lib.set_material_instance_parent(instance,master)
    lib.set_material_instance_scalar_parameter_value(instance,'SourceDuration',duration)
    lib.set_material_instance_scalar_parameter_value(instance,'SourceTimeOrigin',layer.get('preview_time_origin',layer['cast_time']))
    for texture in layer['texture_inputs']:
        source=layer['uniforms'][texture]
        if source.get('texture_source'):
            value=import_file(source['texture_source'],layer.get('native_shared_root','/Game/VFXLab/ReferenceShared')+'/Textures',source['texture_name'])
            lib.set_material_instance_texture_parameter_value(instance,texture,value)
    if layer.get('attribute_texture'):
        info=layer['attribute_texture'];value=import_file(info['source'],layer.get('native_shared_root','/Game/VFXLab/ReferenceShared')+'/Textures',info['name'])
        value.set_editor_property('compression_settings',u.TextureCompressionSettings.TC_VECTOR_DISPLACEMENTMAP)
        value.set_editor_property('mip_gen_settings',u.TextureMipGenSettings.TMGS_NO_MIPMAPS)
        value.set_editor_property('never_stream',True)
        save(value)
        lib.set_material_instance_texture_parameter_value(instance,'AttributeData',value)
    save(instance)
    instance_check=json.loads(LAB.validate_material(instance,world))
    if not instance_check['passed']:raise RuntimeError(json.dumps(instance_check))
    return instance,instance_check

def emitter_from_layer(ctx,layer,mesh,mat,index,duration):
    e=ctx.add_empty_emitter('ReferenceLayer_'+str(index))
    e.set_enabled(True);e.set_local_space(True)
    state=module(e,'EmitterState','/Niagara/Modules/Emitter/EmitterState.EmitterState',CAT.EMITTER_UPDATE)
    setp(state,'Life Cycle Mode',enum('/Niagara/Enums/ENiagaraEmitterLifeCycleMode.ENiagaraEmitterLifeCycleMode','Self'))
    setp(state,'Loop Behavior',enum('/Niagara/Enums/ENiagara_EmitterStateOptions.ENiagara_EmitterStateOptions','Once'))
    life=div(linked('User.CueLifetime') if layer.get('control_bindings') else fl(duration),linked('User.PlaybackRate'))
    setp(state,'Loop Duration',add(life,fl(.15)))
    burst=module(e,'SpawnBurst','/Niagara/Modules/Emitter/SpawnBurst_Instantaneous.SpawnBurst_Instantaneous',CAT.EMITTER_UPDATE)
    setp(burst,'Spawn Count',FX.create_script_input_int(layer['count']))
    setp(burst,'Spawn Time',fl(0))
    def vec(x,y,z):return FX.create_script_input_vector(u.Vector(x,y,z))
    attrs={'Alive':FX.create_script_input_bool(True),'Color':FX.create_script_input_linear_color(u.LinearColor(1,1,1,1)),'Age':fl(0),'NormalizedAge':fl(0),'Lifetime':life,'Mass':fl(1),'Position':position(fl(0)),'Velocity':vec(0,0,0),'Scale':vec(1,1,1),'MeshOrientation':FX.create_script_input_linked_parameter('Engine.Owner.Rotation',u.NiagaraScriptInputType.QUATERNION)}
    if layer.get('runtime_binding') is not None:
        rotation=u.Quat4f()
        for key,value in [('x',0.),('y',0.),('z',0.),('w',1.)]:rotation.set_editor_property(key,value)
        attrs['MeshOrientation']=FX.create_script_input_quat(rotation)
    reference_index=dynamic('Execution','ReturnExecIndex',{},u.NiagaraScriptInputType.FLOAT)
    attrs['DynamicMaterialParameter']=dynamic('TypeConversions','MakeVector4',{'X':reference_index,'Y':fl(0),'Z':fl(0),'W':fl(0)},u.NiagaraScriptInputType.VEC4)
    if layer.get('control_bindings'):
        attrs['ArtReferenceIndex']=reference_index
        controls={'X':reference_index}
        for key in ('Y','Z','W'):
            binding=layer['control_bindings'].get(key)
            controls[key]=linked(binding) if binding else fl(0)
        attrs['DynamicMaterialParameter']=dynamic('TypeConversions','MakeVector4',controls,u.NiagaraScriptInputType.VEC4)
    for name,value in attrs.items():e.set_parameter_directly('Particles.'+name,value,CAT.PARTICLE_SPAWN)
    particle_state=module(e,'ParticleState','/Niagara/Modules/Update/Lifetime/ParticleState.ParticleState',CAT.PARTICLE_UPDATE)
    if layer.get('runtime_persistent'):
        setp(particle_state,'Kill Particles When Lifetime Has Elapsed',FX.create_script_input_bool(False))
    if layer.get('control_bindings'):
        controls['X']=linked('Particles.ArtReferenceIndex')
        e.set_parameter_directly('Particles.DynamicMaterialParameter',dynamic('TypeConversions','MakeVector4',controls,u.NiagaraScriptInputType.VEC4),CAT.PARTICLE_UPDATE)
    renderer=u.NiagaraMeshRendererProperties()
    entry=u.NiagaraMeshRendererMeshProperties();entry.set_editor_property('mesh',mesh)
    override=u.NiagaraMeshMaterialOverride();override.set_editor_property('explicit_mat',mat)
    renderer.set_editor_property('meshes',[entry])
    renderer.set_editor_property('bOverrideMaterials',True)
    renderer.set_editor_property('OverrideMaterials',[override])
    e.add_renderer('ReferenceMesh_'+str(index),renderer)

try:
 for item in catalog['items']:
    if (ROOT/'Saved/Stop-reference-batch.request').exists():break
    if selected and item['slug'] not in selected:continue
    if item['conversion_status']!='pending_native_conversion' and item['slug'] not in preview_v2:continue
    source=ROOT/'Source/ReferencePorts'/(item['class']+'-'+item['slug']+'.port.json')
    if not source.exists():continue
    data=json.loads(source.read_text(encoding='utf-8'))
    if not data['port_ready']:continue
    name=''.join(x.upper() if x in ('i','ii','iii') else x.title() for x in item['slug'].split('-'))
    if item['slug'] in preview_v2:name+='PreviewV2'
    directory='/Game/VFXLab/'+item['class'].title()+'/'+name
    asset_path=directory+'/NS_'+name
    if u.EditorAssetLibrary.does_asset_exist(asset_path):
        if item.get('ue_asset')==asset_path and 'simulation_passed' in item['conversion_status']:continue
        evidence['failed'][item['slug']]={'error':'An existing unverified system was preserved; requires inspection.'};continue
    if item['slug'] in preview_v2 and item['slug'] in evidence['assets']:
        archive=ROOT/'Evidence/ReferencePreviewRevisions';archive.mkdir(exist_ok=True)
        previous=archive/(item['slug']+'-before-v2.json')
        if not previous.exists():previous.write_text(json.dumps(evidence['assets'][item['slug']],indent=2),encoding='utf-8')
    result={'source':item['source'],'sha256':item['sha256'],'method':'experimental_reference_shader_port','materials':[],'asset':asset_path,'visual_review':'not_run','gpu_cost':'not_run','gameplay_integration':'not_run','limitations':['Spawn data represent one demonstration cast; runtime targets and sockets still need bindings.','Reference phases run in material vertex/fragment shaders; all mesh particles are created at cast start.','Playback and bounds require review in the actual game; this method has not been approved for production.']}
    try:
        material_mesh=[]
        durations=[t-l['cast_time'] for l in data['layers'] for t in l['end_times'] if t>l['cast_time']]
        # Keep the demonstration's persistent layer visible beyond its transition burst.
        # Gameplay ownership will replace this finite preview hold during integration.
        if any(not layer['end_times'] for layer in data['layers']):durations.append(3.0)
        duration=max(durations or [3.0])+.1
        result['preview_duration_seconds']=duration
        for n,layer in enumerate(data['layers']):
            mesh=import_file(layer['mesh_source'],'/Game/VFXLab/ReferenceShared/Meshes',layer['mesh_name'],True)
            mat,checked=native_material(layer,directory,'M_'+name+'_Layer'+str(n),duration)
            result['materials'].append(checked)
            material_mesh.append((layer,mesh,mat))
        system=tools.create_asset('NS_'+name,directory,u.NiagaraSystem,u.NiagaraSystemFactoryNew())
        points=[(0,0,0)]
        for layer in data['layers']:
            for key in ('aO','aE','aB'):
                attribute=layer['attributes'].get(key)
                if attribute and attribute['size']==3:
                    points.extend((-v[2]*100,v[0]*100,v[1]*100) for v in attribute['values'])
        lower=[min(v[i] for v in points)-300 for i in range(3)]
        upper=[max(v[i] for v in points)+300 for i in range(3)]
        bounds=u.Box()
        bounds.set_editor_property('min',u.Vector(*lower))
        bounds.set_editor_property('max',u.Vector(*upper))
        bounds.set_editor_property('is_valid',True)
        system.set_editor_property('bFixedBounds',True)
        system.set_editor_property('FixedBounds',bounds)
        result['bounds']={'scope':'Reference demonstration origins/endpoints plus 3 m margin; deformation/culling needs production review.','min_cm':lower,'max_cm':upper}
        if not LAB.set_user_float(system,'User.PlaybackRate',1):raise RuntimeError('PlaybackRate parameter unavailable')
        ctx=FX.create_system_conversion_context(system)
        try:
            for n,(layer,mesh,mat) in enumerate(material_mesh):emitter_from_layer(ctx,layer,mesh,mat,n,duration)
            ctx.finalize()
            result['inspection']=json.loads(LAB.inspect_system(system))
            if not result['inspection']['ready_to_run']:raise RuntimeError('Niagara compile failed')
            simulation=json.loads(LAB.simulate_system(system,world,[.05,duration*.25,duration*.5,duration+.3]))
            result['simulation']=simulation
            frames=simulation.get('frames',[])
            if not frames or not any(e['alive'] for f in frames for e in f['emitters']):raise RuntimeError('No particles in native simulation')
            if any(e['alive'] for e in frames[-1]['emitters']):raise RuntimeError('Native particles did not expire')
            binding_checks=[]
            for frame in frames:
                for emitter in frame['emitters']:
                    if not emitter['alive']:continue
                    if 'reference_index_readable' not in emitter:continue
                    if not emitter['reference_index_readable'] or not emitter.get('reference_indices_match_spawn_order'):
                        raise RuntimeError('REFERENCE_BINDING_ERROR: indices do not match source attribute rows')
                    if not emitter.get('age_readable') or emitter['first_lifetime']<=0 or emitter['first_age']<=0:
                        raise RuntimeError('REFERENCE_BINDING_ERROR: age/lifetime unreadable or invalid')
                    if abs(emitter['first_normalized_age']-emitter['first_age']/emitter['first_lifetime'])>1e-5:
                        raise RuntimeError('REFERENCE_BINDING_ERROR: normalized age does not follow lifetime')
                    binding_checks.append(True)
            result['cpu_reference_bindings']={'status':'passed' if binding_checks else 'not_run_old_bridge','scope':'CPU indices and normalized age; GPU sampling and visual appearance not verified.'}
            save(system)
        finally:ctx.cleanup()
        result['status']='shader_and_simulation_passed_visual_unverified'
        evidence['assets'][item['slug']]=result;evidence['failed'].pop(item['slug'],None)
        item.update(ue_asset=asset_path,conversion_status='native_experimental_simulation_passed_visual_unverified')
        catalog_path.write_text(json.dumps(catalog,indent=2,ensure_ascii=False),encoding='utf-8')
    except Exception:
        result['status']='failed';result['error']=traceback.format_exc()
        evidence['failed'][item['slug']]=result;u.log_error(result['error'])
        if 'REFERENCE_BINDING_ERROR' in result['error']:break
    OUTPUT.write_text(json.dumps(evidence,indent=2,ensure_ascii=False),encoding='utf-8')
finally:
    OUTPUT.write_text(json.dumps(evidence,indent=2,ensure_ascii=False),encoding='utf-8')
    u.SystemLibrary.quit_editor()
