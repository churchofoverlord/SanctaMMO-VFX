import unreal as u
import json, pathlib, traceback, datetime

ROOT = pathlib.Path(u.Paths.project_dir())
REPORT = ROOT / 'VFX-build-report.json'
report = {'status': 'running', 'assets': [], 'parameter_writes': []}
BASE = '/Game/VFXLab/FireBoltI'
FX = getattr(u, 'FXConverterUtilitiesLibrary', None)
CAT = getattr(u, 'ScriptExecutionCategory', None)
LAB = getattr(u, 'SanctaVFXLabLibrary', None)

def record(asset):
    if not asset:
        raise RuntimeError('Asset creation returned None')
    if not u.EditorAssetLibrary.save_loaded_asset(asset):
        raise RuntimeError('Could not save ' + asset.get_path_name())
    report['assets'].append(asset.get_path_name())
    return asset

def material(name, code):
    existing = u.EditorAssetLibrary.load_asset(BASE + '/MI_' + name[2:])
    if existing:
        report['assets'].append(BASE + '/' + name)
        return record(existing)
    tools = u.AssetToolsHelpers.get_asset_tools()
    m = tools.create_asset(name, BASE, u.Material, u.MaterialFactoryNew())
    m.set_editor_property('blend_mode', u.BlendMode.BLEND_ADDITIVE)
    m.set_editor_property('shading_model', u.MaterialShadingModel.MSM_UNLIT)
    m.set_editor_property('two_sided', True)
    m.set_editor_property('used_with_niagara_sprites', True)
    lib = u.MaterialEditingLibrary
    uv = lib.create_material_expression(m, u.MaterialExpressionTextureCoordinate, -600, 0)
    time = lib.create_material_expression(m, u.MaterialExpressionParticleRelativeTime, -600, 200)
    hot = lib.create_material_expression(m, u.MaterialExpressionVectorParameter, -600, 400)
    hot.set_editor_property('parameter_name', 'HotColor')
    hot.set_editor_property('default_value', u.LinearColor(1, .45, .07, 1))
    red = lib.create_material_expression(m, u.MaterialExpressionVectorParameter, -600, 600)
    red.set_editor_property('parameter_name', 'RedColor')
    red.set_editor_property('default_value', u.LinearColor(1, .042, .006, 1))
    gain = lib.create_material_expression(m, u.MaterialExpressionScalarParameter, -600, 800)
    gain.set_editor_property('parameter_name', 'Intensity')
    gain.set_editor_property('default_value', 1.0)
    custom = lib.create_material_expression(m, u.MaterialExpressionCustom, -150, 0)
    custom.set_editor_property('code', code)
    custom.set_editor_property('output_type', u.CustomMaterialOutputType.CMOT_FLOAT3)
    inputs = []
    for label in ['UV', 'Age', 'Hot', 'Red', 'Gain']:
        inp = u.CustomInput()
        inp.set_editor_property('input_name', label)
        inputs.append(inp)
    custom.set_editor_property('inputs', inputs)
    for exp, label in [(uv, 'UV'), (time, 'Age'), (hot, 'Hot'), (red, 'Red'), (gain, 'Gain')]:
        if not lib.connect_material_expressions(exp, '', custom, label):
            raise RuntimeError('Material connection failed: ' + label)
    lib.connect_material_property(custom, '', u.MaterialProperty.MP_EMISSIVE_COLOR)
    opacity = lib.create_material_expression(m, u.MaterialExpressionConstant, -100, 300)
    opacity.set_editor_property('r', 1.0)
    lib.connect_material_property(opacity, '', u.MaterialProperty.MP_OPACITY)
    lib.recompile_material(m)
    record(m)
    mi = tools.create_asset('MI_' + name[2:], BASE, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
    lib.set_material_instance_parent(mi, m)
    return record(mi)

def module(e, name, path, category):
    if not u.load_asset(path):
        raise RuntimeError('Missing Niagara module asset: ' + path)
    data = FX.create_asset_data(path)
    return e.find_or_add_module_script(name, u.CreateScriptContextArgs(data), category)

def setp(mod, name, value):
    ok = mod.set_parameter(name, value)
    report['parameter_writes'].append({'parameter': name, 'success': bool(ok)})
    if not ok:
        raise RuntimeError('Niagara parameter not found: ' + name)

def fl(value):
    return FX.create_script_input_float(value)

def linked(name):
    return FX.create_script_input_linked_parameter(name, u.NiagaraScriptInputType.FLOAT)

def dynamic(folder, asset, inputs, kind=None):
    path = '/Niagara/DynamicInputs/' + folder + '/' + asset + '.' + asset
    ctx = FX.create_script_context(u.CreateScriptContextArgs(FX.create_asset_data(path)))
    for key, value in inputs.items():
        setp(ctx, key, value)
    return FX.create_script_input_dynamic(ctx, kind or u.NiagaraScriptInputType.FLOAT)

def add(a,b): return dynamic('Add', 'Add_Float', {'A':a,'B':b})
def mul(a,b): return dynamic('Multiply', 'Multiply_Float', {'A':a,'B':b})
def div(a,b): return dynamic('Divide', 'Divide_Float', {'A':a,'B':b})
def sub(a,b): return add(a,mul(b,fl(-1)))
def clamp(a,lo,hi): return dynamic('Clamp', 'ClampFloat', {'Float':a,'Min':lo,'Max':hi})
def v2(x,y): return dynamic('TypeConversions','MakeVector2D',{'X':x,'Y':y},u.NiagaraScriptInputType.VEC2)
def along_x(x): return dynamic('Multiply','Multiply_VectorByFloat',{'Vector':FX.create_script_input_vector(u.Vector(1,0,0)),'Float':x},u.NiagaraScriptInputType.VEC3)
def position(x): return dynamic('Transforms','ConvertVectorToPosition',{'Input Position':along_x(x)},u.NiagaraScriptInputType.POSITION)
def flight(): return div(linked('User.Distance'),linked('User.Speed'))

def enum(path, value):
    return FX.create_script_input_enum(path, value)

def emitter(ctx, name, mat, start, life, size, pos, velocity, aligned=False):
    e = ctx.add_empty_emitter(name)
    e.set_enabled(True)
    e.set_local_space(True)
    state = module(e, 'EmitterState', '/Niagara/Modules/Emitter/EmitterState.EmitterState', CAT.EMITTER_UPDATE)
    setp(state, 'Life Cycle Mode', enum('/Niagara/Enums/ENiagaraEmitterLifeCycleMode.ENiagaraEmitterLifeCycleMode', 'Self'))
    setp(state, 'Loop Behavior', enum('/Niagara/Enums/ENiagara_EmitterStateOptions.ENiagara_EmitterStateOptions', 'Once'))
    duration = add(add(linked('User.CastDelay'),flight()),add(linked('User.ImpactDuration'),fl(.1)))
    setp(state, 'Loop Duration', duration)
    burst = module(e, 'SpawnBurst', '/Niagara/Modules/Emitter/SpawnBurst_Instantaneous.SpawnBurst_Instantaneous', CAT.EMITTER_UPDATE)
    setp(burst, 'Spawn Count', FX.create_script_input_int(1))
    setp(burst, 'Spawn Time', add(linked('User.CastDelay'),flight()) if name == 'Impact' else linked('User.CastDelay'))
    # Converter direct assignments precede module scripts. Initialize Particle would
    # overwrite these values; initialize every attribute used by this system here.
    e.set_parameter_directly('Particles.Alive', FX.create_script_input_bool(True), CAT.PARTICLE_SPAWN)
    e.set_parameter_directly('Particles.Color', FX.create_script_input_linear_color(u.LinearColor(1,1,1,1)), CAT.PARTICLE_SPAWN)
    e.set_parameter_directly('Particles.Mass', fl(1), CAT.PARTICLE_SPAWN)
    e.set_parameter_directly('Particles.SpriteRotation', fl(0), CAT.PARTICLE_SPAWN)
    e.set_parameter_directly('Particles.Age', fl(0), CAT.PARTICLE_SPAWN)
    e.set_parameter_directly('Particles.NormalizedAge', fl(0), CAT.PARTICLE_SPAWN)
    lifetime = linked('User.ImpactDuration') if name == 'Impact' else (add(flight(),linked('User.TailFade')) if name == 'Tail' else flight())
    e.set_parameter_directly('Particles.Lifetime', lifetime, CAT.PARTICLE_SPAWN)
    size_x = linked('User.ImpactSize' if name == 'Impact' else 'User.HeadSize')
    e.set_parameter_directly('Particles.SpriteSize', v2(size_x,size_x), CAT.PARTICLE_SPAWN)
    e.set_parameter_directly('Particles.Position', position(linked('User.Distance') if name=='Impact' else fl(0)), CAT.PARTICLE_SPAWN)
    e.set_parameter_directly('Particles.Velocity', along_x(linked('User.Speed') if name != 'Impact' else fl(0)), CAT.PARTICLE_SPAWN)
    module(e, 'ParticleState', '/Niagara/Modules/Update/Lifetime/ParticleState.ParticleState', CAT.PARTICLE_UPDATE)
    if name == 'Head':
        module(e, 'SolveForces', '/Niagara/Modules/Solvers/SolveForcesAndVelocity.SolveForcesAndVelocity', CAT.PARTICLE_UPDATE)
    if name == 'Tail':
        # Same head/tail progression as the HTML, in cm. It grows from the caster and catches up after impact.
        head = add(clamp(mul(linked('Particles.Age'),linked('User.Speed')),fl(0),linked('User.Distance')),fl(18))
        after_hit = clamp(sub(linked('Particles.Age'),flight()),fl(0),linked('User.TailFade'))
        tail = add(clamp(sub(head,linked('User.TailLength')),fl(0),linked('User.Distance')),mul(div(after_hit,linked('User.TailFade')),linked('User.TailLength')))
        length = clamp(sub(head,tail),fl(0),linked('User.TailLength'))
        e.set_parameter_directly('Particles.SpriteSize',v2(linked('User.TailWidth'),length),CAT.PARTICLE_UPDATE)
        e.set_parameter_directly('Particles.Position',position(mul(add(head,tail),fl(.5))),CAT.PARTICLE_UPDATE)
    r = u.NiagaraSpriteRendererProperties()
    r.set_editor_property('material', mat)
    if aligned:
        r.set_editor_property('alignment', u.NiagaraSpriteAlignment.VELOCITY_ALIGNED)
    e.add_renderer(name + 'Renderer', r)
    return e

try:
    if not FX or not LAB:
        raise RuntimeError('SanctaVFXBridge is unavailable. Compile the bridge before preparing the Niagara system.')
    head = material('M_FireBolt_Head', '''float2 p=UV*2-1;
float r=length(p), a=atan2(p.y,p.x);
float fl=.5+.5*sin(a*7+Age*28)*sin(a*3-Age*16);
float core=exp(-r*r*26), inner=exp(-r*r*9), halo=exp(-r*r*3.2)*(.25+.1*fl);
float edge=1-smoothstep(.8,1,r);
return (Red*halo*.45+Hot*inner*.55+float3(1,.9,.72)*core*.9)*edge*Gain;''')
    tail = material('M_FireBolt_Tail', '''float s=1-UV.y, y=UV.x*2-1, m=s*2.6, t=Age*.666667;
float dens=0;
for(int i=0;i<5;i++){float fi=i, ph=fi*1.7;
float yc=(fi-2)*.42*(1-s)+.16*sin(m*2.6-t*9+ph)*(1-s);
float L=.45+.5*frac(fi*.618+.3), w=.05+.1*s;
dens+=exp(-pow((y-yc)/w,2))*smoothstep(1-L,1-L+.35,s)*(.6+.4*fi/4);}
float n=.5+.25*sin(m*9-t*14+y*3)+.25*sin(m*21-t*22+y*6+3);
dens*=smoothstep(.1,.65,n+.45*s);
dens=min(dens*1.35,1.4)*(1-smoothstep(.6,.95,abs(y)));
float T=saturate(pow(s,1.4)*(.55+.6*exp(-y*y*6))*(.8+.4*n));
float3 col=lerp(Red*.15,Hot,T);
return col*dens*(.35+1.1*T)*smoothstep(0,.06,s)*(1-smoothstep(.9,1,s))*Gain;''')
    hit = material('M_FireBolt_Impact', '''float2 p=(UV*2-1)/(0.4+Age*.6);
float r=length(p);
return (Hot*exp(-r*r*8)+float3(1,.9,.72)*exp(-r*r*30))*(1-smoothstep(.65,1,r))*pow(1-Age,2)*Gain;''')
    tools = u.AssetToolsHelpers.get_asset_tools()
    system_path = BASE + '/NS_FireBoltI'
    # Preserve earlier generated versions before replacing the lab asset.
    if u.EditorAssetLibrary.does_asset_exist(system_path):
        backup_path = BASE + '/Archive/NS_FireBoltI_BeforeFix'
        if not u.EditorAssetLibrary.does_asset_exist(backup_path):
            record(u.EditorAssetLibrary.duplicate_asset(system_path,backup_path))
        archive = BASE+'/Archive/NS_FireBoltI_BeforeBuild_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        if not u.EditorAssetLibrary.rename_asset(system_path,archive):
            raise RuntimeError('Could not preserve previous system before rebuilding')
    system = tools.create_asset('NS_FireBoltI', BASE, u.NiagaraSystem, u.NiagaraSystemFactoryNew())
    if not system:
        raise RuntimeError('Could not create fresh Niagara system')
    if FX and LAB:
        for name,value in {'Speed':1200,'Distance':800,'CastDelay':.1,'HeadSize':57.6,'TailLength':260,'TailWidth':104,'TailFade':.2,'ImpactDuration':.25,'ImpactSize':70}.items():
            if not LAB.set_user_float(system,'User.'+name,value):
                raise RuntimeError('Could not expose '+name)
        ctx = FX.create_system_conversion_context(system)
        emitter(ctx, 'Head', head, .1, 8/12, (57.6,57.6), (0,0,0), (1200,0,0))
        emitter(ctx, 'Tail', tail, .1, 8/12, (100,260), (-130,0,0), (1200,0,0), True)
        emitter(ctx, 'Impact', hit, .1+8/12, .25, (70,70), (800,0,0), (0,0,0))
        report['status'] = 'compiling'
        REPORT.write_text(json.dumps(report,indent=2),encoding='utf-8')
        ctx.finalize()
        report['inspection'] = json.loads(LAB.inspect_system(system))
        if not report['inspection']['ready_to_run'] or report['inspection']['emitter_count'] != 3:
            raise RuntimeError('System did not compile with three emitters')
        record(system)
        report['status'] = 'assets_created'
    else:
        record(system)
        report['status'] = 'materials_and_empty_system_created'
        report['blocker'] = 'Installed CascadeToNiagaraConverter module BuildId does not match the running engine. Disabled in lab; emitters must still be authored.'
    report['limitations'] = ['Standalone preview; not connected to gameplay.', 'Visual match to the HTML still needs comparison.']
except Exception:
    report['status'] = 'failed'
    report['error'] = traceback.format_exc()
    u.log_error(report['error'])
finally:
    if 'ctx' in globals() and ctx:
        ctx.cleanup()
    REPORT.write_text(json.dumps(report, indent=2), encoding='utf-8')
    u.log('VFX_BUILD_REPORT ' + str(REPORT))
    (ROOT/'VFX-status.json').write_text(json.dumps({'status':report['status'], 'bridge_compiled':bool(LAB), 'generated_system_saved':report['status']=='assets_created', 'simulation_verified':False, 'visual_verified':False},indent=2),encoding='utf-8')
    if report['status'] == 'assets_created':
        validation = pathlib.Path(__file__).with_name('validate_firebolt.py')
        exec(compile(validation.read_text(encoding='utf-8'), str(validation), 'exec'), {'__name__':'__main__'})
    else:
        u.SystemLibrary.quit_editor()
