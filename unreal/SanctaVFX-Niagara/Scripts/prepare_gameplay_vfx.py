"""Author isolated runtime sources and new combat presentations; preserve all approved lab sources."""
import json,pathlib,copy,hashlib,math,re
from art_review_geometry import plane,sphere,uv_mapping
from reference_shader_port import prepare
from runtime_shader_bindings import bind
R=pathlib.Path(__file__).resolve().parents[1]
OUT=R/'Source/GameplayRuntime';OUT.mkdir(exist_ok=True)
JOBS=[]

def read(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def scalar(v):return {'type':'number','value':v}
def vector(v):return {'type':'vector','values':v}
def attribute(v):return {'size':len(v[0]),'values':v}
def label(s):return ''.join(p.title() for p in re.split(r'[- /]+',s))
def layer(geometry,vertex,fragment,color=(.6,.2,.05),count=1,attrs=None,blending=2):
    return {'pool_index':0,'geometry':geometry,'vertex':vertex,'fragment':fragment,
      'attributes':attrs or {'aO':attribute([[0,0,0]]),'aT':attribute([[0]])},
      'uniforms':{'uTime':scalar(0),'uColor':vector(list(color))},'count':count,
      'cast_time':0,'end_times':[.7],'blending':blending,'lighting':'unlit',
      'position_from_uv':uv_mapping(geometry),'mesh_import_reflect_x':True}

def add(name,layers,form,phase,gate='Admission',anchor='Source',persistent=False,duration=.7,**extra):
    layers=copy.deepcopy(layers)
    if phase in ['Flight','Telegraph','AreaImpact'] or (anchor=='World' and persistent):extra['importance']='Essential'
    # Runtime budget reductions preserve spatial coverage, rather than clipping
    # the first part of a recorded area. Historical art sources remain untouched.
    cap=40 if name.startswith('GlacialSpike') and phase=='AreaImpact' else 20 if 'Chains' in name else 30 if name.startswith(('Mist','AstralPull')) else None
    if cap and sum(l['count'] for l in layers)>cap:
        total=sum(l['count'] for l in layers);left=cap
        for index,l in enumerate(layers):
            n=l['count'];remaining=sum(q['count']>0 for q in layers[index+1:])
            keep=min(n,max(0,left-remaining),left if index==len(layers)-1 else max(1,round(n*cap/total)));left-=keep
            indices=[min(n-1,round(i*(n-1)/max(1,keep-1))) for i in range(keep)]
            for attr in l['attributes'].values():attr['values']=[attr['values'][i] for i in indices]
            l['count']=keep
    for l in layers:
        l['runtime_persistent']=persistent
        l['runtime_binding']=l.get('runtime_binding',{})
        l['runtime_binding'].setdefault('anchor','float3(0,0,0)')
        l['control_bindings']=l.get('control_bindings',{})
        if name in ['GuardActive','ManaStormActive','FullMoonAreaImpact',
          'ArcaneWeavingIResource','ArcaneWeavingIiResource','ElementalWeaverIResource','ElementalWeaverIiResource',
          'ConnectionIAllyActive','ConnectionIEnemyActive','ConnectionIiAllyActive','ConnectionIiEnemyActive'] and l['blending']==2:
            # Preserve the emitted hue on bright scenery. Alpha follows the
            # existing light mask, so the quad edges stay transparent.
            l['blending']=5
            l['runtime_composite_contrast']=True
    data={'slug':name,'title':name,'class':'runtime','method':'event_driven_presentation',
          'layers':layers,'preview_duration':duration,'runtime_parameters':{'User.CueLifetime':duration}}
    file=OUT/(name+'.json');file.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    JOBS.append({'slug':name,'source':file.relative_to(R).as_posix(),'form':form,'phase':phase,
       'gate':gate,'anchor':anchor,'persistent':persistent,'duration':duration,
       'target_life':anchor=='Target','importance':'Gameplay',**extra})

VERT_BILL='''attribute vec3 aO;attribute float aT;uniform float uTime;varying vec2 vQ;varying float vU;
void main(){vU=uTime-aT;vec4 p=viewMatrix*vec4(aO,1.);p.xy+=position.xy*.24;vQ=position.xy;gl_Position=projectionMatrix*p;}'''
FRAG_CONTACT='''uniform vec3 uColor;varying vec2 vQ;varying float vU;
void main(){float t=clamp(vU/.22,0.,1.),r=length(vQ),w=.015+.055*(1.-t);
float star=exp(-pow(min(abs(vQ.x),abs(vQ.y))/w,2.))*exp(-r*r*6.);
float glow=exp(-r*r*16.);float f=pow(1.-t,1.7)*smoothstep(1.,.72,r);
gl_FragColor=vec4(uColor*(star+.35*glow)*f,1.);}'''

def arrow_mesh():
    # Closed 3D shaft and arrowhead, pointing along the actual projectile forward.
    p=[];n=[];uv=[];idx=[]
    rings=[(.34,.006),(-.14,.006),(-.14,.028),(-.32,0.0001)]
    for row,(z,r) in enumerate(rings):
        for i in range(9):
            a=i/8*math.tau;p.extend([math.cos(a)*r,math.sin(a)*r,z]);n.extend([math.cos(a),math.sin(a),0]);uv.extend([i/8,row/3])
    for j in range(3):
        for i in range(8):
            a=j*9+i;b=a+1;c=a+9;d=c+1;idx.extend([a,c,b,b,c,d])
    idx.extend([0,i+1,i] for i in []) # no cap is visible at this scale
    return {'position':p,'normal':n,'uv':uv,'index':idx,'vertex_attributes':{}}

def combat():
    for channel,color in [('Physical',(.65,.36,.16)),('Magical',(.39,.29,.66))]:
        add('Contact'+channel,[layer(plane(),VERT_BILL,FRAG_CONTACT,color)],'Combat.Contact.'+channel,'Impact','ConfirmedHit','World',duration=.3,contact=True,target_life=True)
    weapons=read('Evidence/gameplay-vfx-assessment-20261004.json')['weapon_presentations']
    # Blade dimensions are cosmetic. Actual base/tip positions come from the weapon socket payload.
    widths={'Sword':.026,'Axe':.055,'Club':.065,'Rapier':.014,'Dual Daggers':.018,
      'DualDaggers':.018,'Fists/Gauntlets':.045,'Great Club':.085,'GreatClub':.085,
      'Greatsword':.045,'Greataxe':.07,'Spear':.02}
    for w in weapons:
      for channel,color in [('Physical',(.65,.36,.16)),('Magical',(.39,.29,.66))]:
        family=label(w['family']);form='Combat.Basic.'+family+'.'+channel
        if w['delivery']=='melee':
            width=widths.get(w['family'],.04)
            v='''attribute vec3 aO,aE;attribute float aT;uniform float uTime;varying vec2 vQ;varying float vU;
void main(){vU=uTime-aT;float s=position.x*.5+.5;vec3 p=mix(aO,aE,s);
vec3 dir=normalize(aE-aO+vec3(.00001)),side=normalize(cross(dir,cameraPosition-p));
p+=side*position.y*WIDTH*pow(max(sin(3.14159*s),0.),.7);vQ=vec2(s,position.y);gl_Position=projectionMatrix*viewMatrix*vec4(p,1.);}'''.replace('WIDTH',str(width))
            f='''uniform vec3 uColor;varying vec2 vQ;varying float vU;
void main(){float edge=pow(max(sin(3.14159*vQ.x),0.),.7)*smoothstep(1.,.55,abs(vQ.y));
float light=exp(-vQ.y*vQ.y*18.)+.13*exp(-vQ.y*vQ.y*3.);
gl_FragColor=vec4(uColor*light*edge,1.);}'''
            l=layer(plane(2,2,16,1),v,f,color,attrs={'aO':attribute([[0,0,0]]),'aE':attribute([[0,0,-1]]),'aT':attribute([[0]])})
            l['runtime_binding']={'attributes':{'aE':'RuntimeEndpoint.xyz'}}
            add('Basic'+family+channel+'Trail',[l],form,'Trail',persistent=True,duration=.5,use_endpoint=True,importance='Decorative')
        else:
            arrow=family in ('Bow','Crossbow')
            g=arrow_mesh() if arrow else sphere(1,16,8)
            v=('''attribute vec3 aO;attribute float aT;uniform float uTime;varying vec2 vQ;varying float vU;
void main(){vU=uTime-aT;vec3 p=position;
vQ=uv*2.-1.;gl_Position=projectionMatrix*viewMatrix*vec4(aO+p,1.);}''' if arrow else
               '''attribute vec3 aO;attribute float aT;uniform float uTime;varying vec2 vQ;varying float vU;
void main(){vU=uTime-aT;vec3 p=aO+position*.065*(1.+.04*sin(uTime*8.+position.y*5.));vQ=uv*2.-1.;gl_Position=projectionMatrix*viewMatrix*vec4(p,1.);}''')
            f='''uniform vec3 uColor;varying vec2 vQ;varying float vU;void main(){float s=smoothstep(1.,.75,abs(vQ.y))*smoothstep(1.,.7,abs(vQ.x));gl_FragColor=vec4(uColor*(.55+.2*sin(vU*3.))*s,1.);}'''
            add('Basic'+family+channel+'Flight',[layer(g,v,f,color)],form,'Flight',anchor='Projectile',persistent=True,duration=3.)
            add('Basic'+family+channel+'Release',[layer(plane(),VERT_BILL,FRAG_CONTACT,color)],form,'Release',duration=.3,importance='Decorative')

def new_skills():
    for name,form,col in [('ExploitI','exploit-weakness-i',(.45,.06,.25)),('ExploitII','exploit-weakness-ii',(.65,.06,.28)),('ExploitIII','exploit-weakness-iii',(.8,.08,.3)),('FullMoon','full-moon',(.46,.22,.8)),('CosmicRayI','cosmic-ray-i',(.42,.19,.75)),('CosmicRayII','cosmic-ray-ii',(.64,.26,.92)),('Sickness','sickness',(.24,.4,.065))]:
        v='''attribute vec3 aO;attribute float aT;uniform float uTime;varying vec2 vQ;varying float vU;
void main(){vU=uTime-aT;vec3 p=aO+position*.16;vQ=uv*2.-1.;gl_Position=projectionMatrix*viewMatrix*vec4(p,1.);}'''
        f='''uniform vec3 uColor;varying vec2 vQ;varying float vU;
void main(){float r=length(vQ),line=exp(-pow((r-.55)/.07,2.)),core=exp(-r*r*9.);
gl_FragColor=vec4(uColor*(line*.3+core)*smoothstep(1.,.7,r),1.);}'''
        add(name+'Delivery',[layer(sphere(1,24,12),v,f,col)],form,'Flight',anchor='Projectile',persistent=True,duration=3.)
    # Disarm communicates disabled weapon use; it never removes equipment or implies Stun.
    v=VERT_BILL.replace('*.24','*.19')
    f='''uniform vec3 uColor;varying vec2 vQ;varying float vU;void main(){vec2 p=vQ;
float blade=exp(-pow((p.x+p.y*.22)/.035,2.))*smoothstep(.72,.52,abs(p.y));
float crossLine=exp(-pow((p.x-p.y)/.06,2.))*smoothstep(.9,.65,length(p));
gl_FragColor=vec4(uColor*(blade*.42+crossLine)*smoothstep(1.,.8,length(p)),1.);}'''
    l=layer(plane(),v,f,(.63,.26,.12));l['attributes']['aO']=attribute([[0,2.05,0]]);l['runtime_binding']={'anchor':'float3(0,0,0)'}
    add('CCDisarmActive',[l],'Status.CC.Disarm','Active','Applied','Target',True,3.4,importance='Essential')
    for phase,gate in [('Apply','Applied'),('NaturalEnd','NaturalEnd'),('Cleanse','Cleanse')]:
        add('CCDisarm'+phase,[layer(plane(),v,FRAG_CONTACT,(.63,.26,.12),attrs={'aO':attribute([[0,2.05,0]]),'aT':attribute([[0]])})], 'Status.CC.Disarm',phase,gate,'Target',duration=.3)

def actions():
    # Guard uses one short shield stroke, not a protective dome or perfect-block flash.
    v='''attribute vec3 aO;attribute float aT;uniform float uTime;varying vec2 vQ;varying float vU;
void main(){vU=uTime-aT;vQ=position.xy;vec3 p=aO+vec3(0.,position.y*.35,position.x*.26);gl_Position=projectionMatrix*viewMatrix*vec4(p,1.);}'''
    f='''uniform vec3 uColor;varying vec2 vQ;varying float vU;void main(){float line=exp(-pow((abs(vQ.x)-.68)/.035,2.))*pow(max(1.-abs(vQ.y),0.),.8);gl_FragColor=vec4(uColor*line*.65,1.);}'''
    add('GuardActive',[layer(plane(),v,f,(.23,.35,.42))],'Combat.Guard','Active','Applied',persistent=True,duration=3.,importance='Essential')
    add('GuardMitigation',[layer(plane(),VERT_BILL,FRAG_CONTACT,(.47,.56,.65))],'Combat.Guard','Mitigation','ConfirmedHit',duration=.3,contact=True)
    add('GuardDepletion',[layer(plane(),VERT_BILL,FRAG_CONTACT,(.19,.23,.28))],'Combat.Guard','Depletion','Applied',duration=.25)
    # Foot contact is a material/surface event; no autonomous repeated footsteps.
    v='''attribute vec3 aO;attribute float aT;uniform float uTime;varying vec2 vQ;varying float vU;
void main(){vU=uTime-aT;float k=clamp(vU/.45,0.,1.);vQ=position.xy;vec3 p=aO+vec3(position.x,0.,-position.y)*mix(.12,.32,k)+vec3(0.,.012,0.);gl_Position=projectionMatrix*viewMatrix*vec4(p,1.);}'''
    for surface,col in [('Stone',(.2,.18,.15)),('Snow',(.55,.62,.67)),('Mud',(.16,.10,.065)),('Water',(.21,.39,.49))]:
        f='''uniform vec3 uColor;varying vec2 vQ;varying float vU;void main(){float r=length(vQ),n=.65+.35*sin(vQ.x*15.+sin(vQ.y*12.)*2.);float a=exp(-r*r*5.)*n*pow(max(1.-vU/.45,0.),1.6)*smoothstep(1.,.75,r);gl_FragColor=vec4(uColor*a,a*.4);}'''
        add('FootContact'+surface,[layer(plane(),v,f,col,blending=5)],'Combat.Surface.'+surface,'FootContact','Cosmetic','World',duration=.5,importance='Decorative')
    add('DodgeStart',[layer(plane(),v,f,(.23,.23,.25),blending=5)],'Combat.Dodge','Start',duration=.5,importance='Decorative')
    add('DodgeAvoided',[layer(plane(),VERT_BILL,FRAG_CONTACT,(.3,.33,.38))],'Combat.Dodge','Avoided','Applied',duration=.22)
    # Sprint deliberately owns no aura: its four surface cues are shared foot contacts.

def holds_links():
    catalog=read('VFX-catalog.json')['items']
    for slug in ['mana-barrier-i','mana-barrier-ii-overcharge']:
        item=next(i for i in catalog if i['slug']==slug);d=read(item['review_source']);layers=copy.deepcopy(d['layers'])
        for l in layers:
            l['runtime_uniforms']={**l.get('runtime_uniforms',{}),'uCastProgress':'RuntimeCastProgress','uReleaseAge':'RuntimeReleaseAge','uAutoPreview':'0.'}
            l['runtime_binding']={'anchor':'float3(0,0,0)'}
        add(label(slug)+'Hold',layers,slug,'Hold',persistent=True,duration=3.,state_owned=False)
        add(label(slug)+'Release',layers,slug,'Release',duration=.8)
    for item in catalog:
        if not item['slug'].startswith('connection-'):continue
        d=read(item.get('review_source',f"Source/ReferencePorts/{item['class']}-{item['slug']}.json"));layers=[]
        for l in d['layers']:
            l=copy.deepcopy(l);a=l['attributes'];ids=[i for i,v in enumerate(a['aK']['values']) if v[0]<2.5]
            for x in a.values():x['values']=[x['values'][i] for i in ids]
            l['count']=len(ids)
            if not ids:continue
            l['runtime_binding']={'anchor':'float3(0,0,0)','attributes':{'aA':'float3(0,0,0)','aB':'RuntimeEndpoint.xyz','aT':'float3(0,1e9,1e9)'}}
            layers.append(l)
        add(label(item['slug'])+'Active',layers,item['slug'],'Active','Applied','Link',True,3.4,use_endpoint=True,target_life=True)
        for l in layers:
            # Dissolution starts with a fully grown link. The recorded cast
            # offset must not consume the terminal phase before it is drawn.
            l['runtime_binding']['clock']='RuntimeAge'
            l['runtime_binding']['attributes']['aT']='float3(-(length(RuntimeEndpoint.xyz)/7.+.05),0,1e9)'
        add(label(item['slug'])+'NaturalEnd',layers,item['slug'],'NaturalEnd','NaturalEnd','Link',duration=1.1 if '-ii-' in item['slug'] else .45,use_endpoint=True,target_life=True)

def components():
    items=read('VFX-separated-components.json')['items']
    fixtures=['LightningMemory','HoldLow','HoldHigh']
    for item in items:
        if any(s in item['slug'] for s in fixtures) or item['slug']=='BackstabIIHitSparks' or item['slug'].startswith('SeveringHit'):continue
        d=read(item['component_source']);layers=copy.deepcopy(d['layers']);role=item.get('component_role','')
        name=item['slug'];anchor={'target':'Target','body':'Target','caster':'Source','projectile':'Projectile','caster_to_target':'Link','world':'World'}.get(item['anchor'],'Source')
        persistent=role in ['active','status_active','latched_link'] or 'Latched' in name or name=='TempestStormArea'
        phase='Active' if persistent else 'Impact' if anchor=='Target' else 'Cast'
        gate='Applied' if persistent else 'ConfirmedHit' if anchor=='Target' else 'Admission'
        if 'NaturalEnd' in name:phase='NaturalEnd';gate='NaturalEnd'
        elif 'Cleanse' in name:phase='Cleanse';gate='Cleanse'
        elif name.endswith('Death'):continue # Death removes the active cue; no generic success burst.
        elif 'Flight' in name:phase='Flight';persistent=True
        elif 'Aim' in name and not name.endswith('End'):phase='Hold';persistent=True
        elif name.endswith('End'):phase='End';gate='Cosmetic'
        elif 'Conditional' in name or 'Apply' in name:phase='Apply';gate='Applied'
        if name in ['FireBoltIISpread','TempestSappedProc'] or name.startswith('Rally') or name.startswith('CCForced') or name.startswith('SeveringMark'):phase='Apply';gate='Applied'
        if name in ['TempestGroundImpact','TempestFrostImpact'] or ('GlacialSpike' in name and 'GroundArea' in name):phase='AreaImpact';gate='Applied'
        if name=='TempestTelegraph':phase='Telegraph';gate='Admission';persistent=True
        if name=='BrightStarHeal':name='BrightStarShieldApply';phase='ShieldApply';gate='Applied'
        # Role is authoritative; an arbitrary asset suffix must not turn a
        # confirmed heal/proc/recast into a cast-admission flash.
        applied_roles={'heal':'Heal','cast_complete':'Complete','caster_proc':'Proc',
          'root_apply':'Apply','conditional_proc':'Proc','confirmed_recast':'Recast',
          'confirmed_interrupt':'Interrupt','ground_area':'AreaImpact'}
        if role in applied_roles:phase=applied_roles[role];gate='Applied'
        if role=='tether_target_state':phase='Active';gate='Applied';persistent=True
        if role=='confirmed_chain':
            phase='Chain';gate='Applied';anchor='Link'
            # One pair per event. Gameplay emits one event for each confirmed
            # edge, with its actual origin and endpoint actors/sockets.
            for l in layers:
                attrs=l['attributes'];end=attrs['aE']['values'][0]
                ids=[i for i,v in enumerate(attrs['aE']['values']) if all(abs(a-b)<.001 for a,b in zip(v,end))]
                for attr in attrs.values():attr['values']=[attr['values'][i] for i in ids]
                l['count']=len(ids)
        if name.startswith('Volley') and phase=='Flight':
            # The authority creates the fan's projectiles. This system follows
            # one projectile; spawning it nine times must not create 81 arrows.
            for l in layers:
                i=l['count']//2
                for attr in l['attributes'].values():attr['values']=[attr['values'][i]]
                l['count']=1
        # A component phase has its own stable event name, not a timer in the full cast.
        if name in ['TempestIce','TempestLightning']:
            # Individual confirmed strikes, not the entire recorded sequence.
            for l in layers:
                t=l['attributes'].get('aT');
                if t:
                    first=min(v[0] for v in t['values']);indices=[i for i,v in enumerate(t['values']) if abs(v[0]-first)<.04]
                    for attr in l['attributes'].values():attr['values']=[attr['values'][i] for i in indices]
                    for value in t['values']:value[0]-=first
                    l['count']=len(indices);l['cast_time']=0;l['preview_time_origin']=0
            gate='Applied';phase='Strike';persistent=False
        for l in layers:
            attrs=l['attributes'];o=attrs.get('aO',attrs.get('aA',{})).get('values',[[0,0,0]])[0]
            o=list(o[:3])
            if anchor in ['Target','Source']:o[1]=0 # preserve authored body height above the actor root
            if name in ['TempestIce','TempestLightning']:
                reference=read(next(i['component_source'] for i in items if i['slug']=='TempestLightning'))
                o=list(reference['layers'][0]['attributes']['aE']['values'][0][:3]);o[1]=0
            base='float3('+','.join(str(v) for v in o)+')'
            cfg={'anchor':base,'attributes':{},'defaults':{}}
            if not persistent and attrs.get('aT',{}).get('size') in [1,2] and role not in ['tether_end','telegraph_end']:
                starts=[v[0] for q in layers for v in q['attributes'].get('aT',{}).get('values',[]) if v[0]>-1000]
                if starts and not math.isclose(min(starts),l.get('preview_time_origin',l.get('cast_time',0)),abs_tol=.0001):cfg['clock']='RuntimeAge+'+str(min(starts))
            if persistent and name.startswith('CC') and 'aT' in attrs:
                cfg['attributes']['aT']='float4(0,1e9,1e9,0)' if attrs['aT']['size']==4 else 'ReferenceTime-.5'
            elif persistent and phase!='Flight' and 'aT' in attrs and attrs['aT']['size']==1:
                cfg['attributes']['aT']='ReferenceTime-.6'
            if anchor=='Link':
                cfg['attributes'].update({key:('float3(0,0,0)' if key in ['aA','aO'] else 'RuntimeEndpoint.xyz') for key in ['aA','aO','aB','aE'] if key in attrs});cfg['anchor']='float3(0,0,0)'
                if 'aT' in attrs and attrs['aT']['size']==3:cfg['attributes']['aT']='float3(0,1e9,1e9)'
            if name.startswith('CCTaunt') and 'aK' in attrs:
                # Taunt's application line and temple-side marker use the real
                # taunter endpoint relative to the target, never the recorded caster.
                cfg['attributes']['aK']='float4(f.aK.x,RuntimeEndpoint.xyz)'
            if name=='ResurrectComplete':
                cfg['clock']='RuntimeAge';cfg['attributes']['aT']='float3(0,0,1)'
            if name=='TempestTelegraph':
                cfg['attributes']['aT']='ReferenceTime-clamp(RuntimeCastProgress,0.,1.)*f.aD.z'
                cfg['attributes']['aD']='float4(f.aD.x,RuntimeElementA > 1.5 ? 1. : 0.,f.aD.z,f.aD.w)'
            if name.startswith('Volley') and role in ['telegraph_active','telegraph_end']:
                cfg['attributes']['aT']='ReferenceTime-RuntimeCastProgress*1.2-max(RuntimeReleaseAge,0.)'
                cfg['attributes']['aR']='RuntimeReleaseAge < 0. ? 1e9 : ReferenceTime-RuntimeReleaseAge'
                l['vertex']=re.sub(r'vP = hold >= 1\.2[^;]+;', 'vP = hold >= 1.2 && uReadyAge >= 0. ? max(0.,1.-uReadyAge/.25) : 0.;',l['vertex'])
                l['vertex']='uniform float uReadyAge;\n'+l['vertex'];l['uniforms']['uReadyAge']=scalar(-1)
                l['runtime_uniforms']={**l.get('runtime_uniforms',{}),'uReadyAge':'RuntimeGainAge'}
                l['fragment']=l['fragment'].replace('A = mix(.44, 0., vH), R = mix(9., 18., vH)', 'A = uAimHalfAngle, R = 18.')
                l['fragment']='uniform float uAimHalfAngle;\n'+l['fragment'];l['uniforms']['uAimHalfAngle']=scalar(.44)
                l['runtime_uniforms']['uAimHalfAngle']='RuntimeAimHalfAngle'
                cfg['defaults']['RuntimeAimHalfAngle']=.44
            if name.startswith('Chains') and anchor=='Link':
                tR='(.1+length(RuntimeEndpoint.xyz)/14.)'
                if attrs.get('aF',{}).get('size')==3:
                    slots=max(v[1] for v in attrs['aF']['values'])+1
                    hit='0.' if phase=='Flight' else '1.'
                    cfg['attributes']['aF']='float3('+hit+',f.aF.y,length(RuntimeEndpoint.xyz)/'+str(slots)+')'
                if 'aT' in attrs and attrs['aT']['size']==1:
                    dissolve_start='.45' if name=='ChainsIEnd' else '1.60'
                    offset=tR if phase=='Flight' else tR+'+.25' if persistent else tR+'+'+dissolve_start+'+RuntimeAge' if role=='tether_end' else tR+'+.25'
                    cfg['attributes']['aT']='ReferenceTime-.26-('+offset+')'
                if role=='confirmed_recast' and 'aP' in attrs:cfg['clock']='RuntimeAge+1';cfg['attributes']['aP']='1.'
                if 'aO' in attrs and 'aE' not in attrs:cfg['attributes']['aO']='RuntimeEndpoint.xyz'
            if name.startswith('FireBolt') and 'Flight' in name:
                cfg['attributes']['aT']='ReferenceTime-.45'
                cfg['anchor']='f.aO+normalize(f.aE-f.aO)*min(4.2,length(f.aE-f.aO))'
            elif phase=='Flight' and anchor!='Link' and 'aO' in attrs:
                t=attrs.get('aT')
                if t:
                    cfg['attributes']['aT']='ReferenceTime-.3' if t['size']==1 else 'float2(ReferenceTime-.3,f.aT.y)' if t['size']==2 else 'float3(ReferenceTime-.3,f.aT.y,f.aT.z)'
                cfg['probe_anchor']=True
                if 'trail' in l['vertex'].lower() or l.get('geometry',{}).get('uv'):
                    if 'vS' in l['vertex']:cfg['probe_position']=[1.,0.,0.]
            l['runtime_binding']=cfg
        form='Component.'+name
        parent=item.get('parent_skill')
        for prefix,skill in [('ChainsII','chains-ii'),('ChainsI','chains'),('VolleyIIBleed','volley-ii-bleed'),('VolleyIIPoison','volley-ii-poison'),('VolleyIBleed','volley-i-bleed'),('VolleyIPoison','volley-i-poison')]:
            if name.startswith(prefix):parent=skill;break
        if name.startswith('SeveringHit'):parent=None # Optional reference, not an automatic rank contact.
        add(name,layers,form,phase,gate,anchor,persistent,item['duration'],
           parent_skill=parent,historical_component=item['slug'],use_endpoint=anchor=='Link' or name.startswith('CCTaunt'),
           target_life=anchor=='Target' or (anchor=='Link' and phase!='Flight'),
           importance='Essential' if name.startswith('CC') else 'Gameplay')

def resources():
    catalog=read('VFX-catalog.json')['items']
    for slug in ['arcane-weaving-i','arcane-weaving-ii','elemental-weaver-i','elemental-weaver-ii']:
        item=next(i for i in catalog if i['slug']==slug);d=read(item['review_source']);layers=[]
        for l in d['layers']:
            if 'aP' not in l['attributes']:continue
            l=copy.deepcopy(l);attrs=l['attributes'];cfg={'anchor':'float3(0,0,0)','attributes':{},'defaults':{'RuntimeCount':3.}}
            if slug.startswith('arcane'):
                for a in attrs.values():a['values']=[copy.deepcopy(a['values'][0]) for i in range(11)]
                attrs['aP']['values']=[[0,-1]]+[[0,i] for i in range(10)];l['count']=11
                l['vertex']=l['vertex'].replace('aP.y*2.0944','aP.y*6.283185/max(uResourceMax,1.)')
                l['vertex']='uniform float uResourceMax;\n'+l['vertex'];l['uniforms']['uResourceMax']=scalar(10)
                l['runtime_uniforms']={'uResourceMax':'RuntimeMax'}
                cfg['attributes']['aV']='f.aP.y < -.5 ? 1. : step(f.aP.y+.5,RuntimeCount)'
            else:
                cfg['attributes']['aV']='f.aP.y < -.5 ? 1. : (f.aP.y < .5 ? fmod(RuntimeOccupied,2.) : floor(RuntimeOccupied/2.))'
                l['runtime_uniforms']={**l.get('runtime_uniforms',{}),'uElementA':'RuntimeElementA','uElementB':'RuntimeElementB'}
                if 'uElementA' not in l['vertex']: # orbital line has no element uniforms
                    l['runtime_uniforms'].pop('uElementA',None);l['runtime_uniforms'].pop('uElementB',None)
            cfg['attributes']['aT']='-1e5'
            if 'aG' in attrs:cfg['attributes']['aG']='RuntimeGainAge < 0 ? -1e5 : ReferenceTime-RuntimeGainAge'
            l['runtime_binding']=cfg;layers.append(l)
        add(label(slug)+'Resource',layers,slug,'Active','Applied',persistent=True,duration=3.2,importance='Essential')
    for item in catalog:
        if not item['slug'].startswith('spirit-of-'):continue
        d=read(item.get('review_source',f"Source/ReferencePorts/{item['class']}-{item['slug']}.json"));layers=[]
        for l in d['layers']:
            if 'aS' not in l['attributes'] and 'aP' not in l['attributes']:continue
            l=copy.deepcopy(l);a=l['attributes'];cfg={'anchor':'float3(0,0,0)','attributes':{'aT':'float2(0,RuntimeGainAge < 0 ? -1e5 : ReferenceTime-RuntimeGainAge)'},'defaults':{}}
            if 'aS' in a:cfg['attributes']['aS']='float2(RuntimeCount,RuntimePending)'
            l['runtime_binding']=cfg;layers.append(l)
        add(label(item['slug'])+'State',layers,item['slug'],'Active','Applied','Target',True,3.4,importance='Essential')

def skill_phases():
    names={x['slug']:{i:l['name'] for i,l in enumerate(x['layers'])} for x in read('VFX-reference-layers.json')}
    catalog=read('VFX-catalog.json')['items']
    # Full demonstrations never become production compositions. These authored
    # event groups expose only a source, delivery, area or confirmed result.
    for item in catalog:
        slug=item['slug']
        if slug in ['control','nameplates'] or slug.startswith(('connection-','spirit-of-','arcane-weaving-','elemental-weaver-','mana-barrier-')):continue
        d=read(item.get('review_source',f"Source/ReferencePorts/{item['class']}-{slug}.json"));groups={}
        for source in d['layers']:
            l=copy.deepcopy(source);pool=l['pool_index'];name=names.get(slug,{}).get(pool,'authored')
            phase='Cast';gate='Admission';anchor='Source';persistent=False
            if name in ['hits','marks','locks','payoffs','procs','stacks','resets','sparkS','rings']:
                phase='Impact' if name in ['hits','marks'] else 'Proc';gate='ConfirmedHit' if name in ['hits','marks','sparks'] else 'Applied';anchor='Target'
            elif name in ['sparks','debris']:
                # Contacts have one dominant form; historical redundant decoration stays in the lab.
                if slug!='hemorrhage':continue
            elif name in ['daggers','bombs']:
                phase='Flight';anchor='Projectile';persistent=True
            elif name=='trails':
                if slug.startswith(('shoulder-rush','quickstep')):phase='Movement';anchor='Source';persistent=True
                elif slug=='war-leap':phase='Movement';anchor='Source';persistent=True
                else:phase='Flight';anchor='Projectile';persistent=True
            elif name in ['grounds','fields','walls','zone','vol','smokes','limits','wall','helix','ribs','bh','veil','dome','gdec','cloud','moonB']:
                phase='Active';gate='Applied';anchor='World';persistent=True
            elif name in ['markers','orbits','hands']:
                if slug in ['manifest','weave','warrior-stance','tank-stance','sun-stance','moon-stance','bleed-stance','poison-stance']:
                    phase='Active';gate='Applied';anchor='Source';persistent=True
                else:continue
            elif name=='aura':phase='Active';gate='Applied';anchor='Source';persistent=True
            elif name=='rez':phase='Hold';anchor='Target';persistent=True
            elif name=='ser':continue # Shared source contains timed heal/sleep: isolated components own results.
            elif name=='beam' or (slug=='laser' and pool==2):phase='Active';gate='Applied';anchor='Link';persistent=True
            # Art pass overrides kept pool IDs: classify their final meaning explicitly.
            if slug=='pressure-provoke':
                phase='Cast' if pool==1 else 'Impact';gate='Admission' if pool==1 else 'ConfirmedHit';anchor='Link' if pool==1 else 'World';persistent=False
            if slug=='sand-shot':
                phase='Impact' if pool==2 else 'Cast';gate='ConfirmedHit' if pool==2 else 'Admission';anchor='World';persistent=False
            if slug.startswith('battlecry-challenge'):
                phase='Cast' if pool!=2 else 'Proc';gate='Admission' if pool!=2 else 'Applied';anchor='Source' if pool!=2 else 'Target';persistent=False
            if slug.startswith('rally-'):
                if pool==1:continue # Isolated affected-target cues already exist.
                phase='Cast';gate='Admission';anchor='Source';persistent=False
            if slug.startswith('shoulder-rush') and pool==1:phase='Impact';gate='ConfirmedHit';anchor='Target';persistent=False
            if slug.startswith('cleanse'):phase='Apply';gate='Applied';anchor='Target';persistent=False
            if slug=='evasion':phase='Proc';gate='Applied';anchor='Source';persistent=False
            if slug.startswith('smoke-bomb') and pool==1:phase='AreaImpact';gate='Applied';anchor='World';persistent=False
            if slug=='combust-ii' and pool==20:phase='AreaImpact';gate='Applied';anchor='World';persistent=False
            if slug=='combust-ii' and pool==5:phase='Proc';gate='Applied';anchor='Target';persistent=False
            if slug.startswith('chains'):continue
            if slug.startswith('severing-strike'):continue # Cast/hit/sequence owned by isolated cues.
            if slug.startswith('fire-bolt'):continue # Preserve the approved isolated fire flight/impact composition.
            if slug=='defiant-presence':phase='Active';gate='Applied';anchor='World';persistent=True
            if slug.startswith('glacial-spike'):
                if pool in [2,3,4]:continue
                phase='AreaImpact';gate='Applied';anchor='World';persistent=False
            if slug.startswith('frost-lance') and pool in [2,3,4]:continue
            if slug=='bright-star':
                if pool not in [2,3,4]:continue
                phase='Cast';gate='Admission';anchor='Source';persistent=False
            if slug=='full-moon' or slug=='eclipse':phase='AreaImpact';gate='Applied';anchor='World';persistent=False
            # Art revisions changed pool meanings: classify the current shader,
            # rather than trusting the historical pool label alone.
            if slug=='vortex' and pool in [0,1,2,3,4]:phase='Flight';gate='Admission';anchor='Projectile';persistent=True
            if slug=='vortex' and pool==7:phase='Displacement';gate='Applied';anchor='Target';persistent=False
            if slug.startswith('crushing-blow') and name in ['grounds','bolts']:phase='AreaImpact';gate='Applied';anchor='World';persistent=False
            if slug=='war-leap' and name=='grounds':
                groups.setdefault(('AreaImpact','Applied','World',False),[]).append(copy.deepcopy(l))
                phase='Telegraph';gate='Admission';anchor='World';persistent=True
            if slug=='war-leap' and name=='bolts':phase='AreaImpact';gate='Applied';anchor='World';persistent=False
            if slug.startswith('thunderstrike') and pool==2:phase='Strike';gate='Applied';anchor='World';persistent=False
            if slug.startswith('astral-aura-'):phase='Active';gate='Applied';anchor='Source';persistent=True
            if slug=='astral-pull':
                phase='Link' if pool in [2,3] else 'AreaImpact' if pool==0 else 'Relocate'
                gate='Applied';anchor='Link' if pool in [2,3] else 'World' if pool==0 else 'Target';persistent=False
            if slug.startswith('cosmic-ray'):
                if pool==2:phase='Resolve';gate='Applied';anchor='Target';persistent=False
                else:phase='Pending';gate='Applied';anchor='Target';persistent=True
            if slug.startswith('exploit-weakness'):phase='Impact' if pool==0 else 'Proc';gate='ConfirmedHit' if pool==0 else 'Applied';anchor='Target';persistent=False
            if slug.startswith('basic-attack-'):
                if pool not in [2]:continue
                phase='Overlay';gate='Applied';anchor='Target';persistent=False
            if slug=='tempest':continue # Isolated storm/telegraph/strike/results own all presentation.
            if slug.startswith('volley-'):continue # Existing separated fan/piercing/hold/hit components.
            if slug=='iceberg' and pool==2:continue # Blocking body belongs to the terrain actor, not a Niagara wall.
            if slug in ['rage','bulwark']:phase='Apply';gate='Applied';anchor='Source';persistent=False
            if slug=='mist':phase='Active';gate='Applied';anchor='World';persistent=True
            if slug=='long-jump' and phase=='Flight':phase='Movement';anchor='Source';persistent=True
            if slug=='long-jump' and pool==0:phase='Hold';anchor='Link';gate='Admission';persistent=True
            if slug=='long-jump' and pool==1:phase='Telegraph';anchor='World';gate='Admission';persistent=True
            if slug in ['bleed-stance','poison-stance']:phase='Active';anchor='Link';gate='Applied';persistent=True
            if slug.startswith('vine-field'):phase='Active';gate='Applied';anchor='World';persistent=True
            if slug=='sickness':
                phase='Consume' if pool==6 else 'AreaImpact' if pool in [5,22] else 'Impact'
                gate='Applied';anchor='World' if phase=='AreaImpact' else 'Target';persistent=False
            if slug=='hemorrhage':phase='Consume' if pool==5 else 'Payoff';gate='Applied';anchor='Target';persistent=False
            if slug=='poison-sac' and pool in [4,22]:phase='Active';gate='Applied';anchor='World';persistent=True
            if slug=='poison-sac' and pool==5:phase='Consume';gate='Applied';anchor='Target';persistent=False
            if slug=='second-wind':phase='Heal';gate='Applied';anchor='Source';persistent=False
            if slug=='momentum-mastery':phase='ResourceGain';gate='Applied';anchor='Source';persistent=False
            key=(phase,gate,anchor,persistent)
            groups.setdefault(key,[]).append(l)
        for (phase,gate,anchor,persistent),layers in groups.items():
            origin=([0,0,0] if slug.startswith('glacial-spike') else [0,0,-6]) if slug.startswith(('glacial-spike','vine-field')) else next((l['attributes']['aO']['values'][0] for l in layers if 'aO' in l['attributes']),[0,0,0])
            if slug.startswith('thunderstrike') and phase=='Strike':
                origin=list(layers[0]['attributes']['aE']['values'][0]);origin[1]=0
            if anchor=='Source':origin[1]=0
            if anchor=='Target':origin=list(origin[:3]);origin[1]=0
            start=min((v[0] for l in layers for v in l['attributes'].get('aT',{}).get('values',[]) if v[0]>-1000),default=0)
            for l in layers:
                a=l['attributes'];cfg={'anchor':'float3('+','.join(str(v) for v in origin[:3])+')','attributes':{}}
                if slug=='mist':
                    # The fragment shader must recover the undeformed quad,
                    # rather than reading interpolated post-WPO coordinates.
                    l['position_from_uv']=uv_mapping(l['geometry'])
                    if l['pool_index']==2:cfg['ground_fade_cm']=60
                if slug=='sand-shot':
                    l['position_from_uv']=uv_mapping(l['geometry'])
                    if l['pool_index']==0:
                        l['fragment']=l['fragment'].replace('pow(d, 1.4)*.9, 0., .5','pow(d, .8)*1.25, 0., .65').replace('uSand*.35','uSand*.55').replace('uGold, .12)*.8','uGold, .12)*1.2')
                    if 'aY' in a:cfg['attributes']['aY']='0'
                    if phase=='Impact':
                        cfg['anchor']='float3(0,0,0)';cfg['attributes']['aO']='float3(0,0,0)'
                        cfg['native_contact_billboard_cm']=38
                        for value in a.values():value['values']=value['values'][:1]
                        for value in a['aO']['values']:value[:]=[0,0,0]
                        l['count']=1
                if 'aT' in a:
                    for v in a['aT']['values']:
                        # Preserve duration and state fields in Y/Z; only timestamps move into phase time.
                        if v[0]>-1000:v[0]-=start
                l['cast_time']=0;l['preview_time_origin']=0
                if anchor=='Link':
                    cfg['anchor']='float3(0,0,0)'
                    for n in ['aO','aA','aE','aB']:
                        if n in a:cfg['attributes'][n]='float3(0,0,0)' if n in ['aO','aA'] else 'RuntimeEndpoint.xyz'
                if phase=='Hold' and slug=='resurrect':
                    cfg['attributes']['aT']='float3(0,1e9,0)'
                if phase in ['Active','Telegraph'] and persistent and 'aT' in a:
                    cfg['attributes']['aT']='ReferenceTime-.6' if a['aT']['size']==1 else 'float2(ReferenceTime-.6,1e9)' if a['aT']['size']==2 else cfg['attributes'].get('aT','f.aT')
                if slug=='poison-sac' and l['pool_index']==22:cfg['attributes']['aT']='ReferenceTime-fmod(RuntimeAge+f.aP.x*2.3,2.4)'
                if slug=='sickness' and phase=='AreaImpact':cfg['clock']='RuntimeAge*5.625+TimeOrigin'
                if slug=='arcane-burst' and 'aS' in a:cfg['attributes']['aS']='.16+.018*sqrt(max(RuntimeCount,0.))'
                if slug=='arcane-burst' and phase=='Flight':
                    # aT becomes a live clock offset; it must no longer seed
                    # a random left/right curve on every presentation tick.
                    l['vertex']=l['vertex'].replace(', aT)',', 0.)')
                if slug.startswith('astral-aura-') and 'aS' in a:
                    cfg['attributes']['aS']='float3(ReferenceTime-.6,1e9,1)'
                if slug=='war-leap' and phase=='AreaImpact':cfg['clock']='RuntimeAge+1.0+TimeOrigin'
                if slug.startswith('crushing-blow') and phase=='AreaImpact':cfg['clock']='RuntimeAge+.22+TimeOrigin'
                if slug=='laser' and anchor=='Link':
                    l['vertex']='uniform vec3 uRuntimeEndpoint;\n'+l['vertex']
                    l['uniforms']['uRuntimeEndpoint']=vector([0,0,-6])
                    l['runtime_uniforms']={**l.get('runtime_uniforms',{}),'uRuntimeEndpoint':'RuntimeEndpoint.xyz'}
                    l['vertex']=re.sub(r'aimDir\(aP.x, aP.y, u\)', 'normalize(uRuntimeEndpoint)',l['vertex'])
                    l['vertex']=l['vertex'].replace('22.*','length(uRuntimeEndpoint)*')
                if slug.startswith('cosmic-ray') and phase=='Resolve':
                    l['runtime_uniforms']={**l.get('runtime_uniforms',{}),'uAlly':'f.aO'}
                if slug=='astral-pull':
                    cfg['attributes']['aT']='0'
                    if anchor=='Link':cfg['clock']='RuntimeAge+.26+TimeOrigin'
                if slug=='long-jump' and phase in ['Hold','Telegraph']:
                    cfg['attributes'].update(aT='ReferenceTime-.3',aR='ReferenceTime+1e9')
                    if phase=='Hold':
                        l['vertex']='uniform vec3 uRuntimeEndpoint;\n'+l['vertex']
                        l['uniforms']['uRuntimeEndpoint']=vector([0,0,-6])
                        l['runtime_uniforms']={**l.get('runtime_uniforms',{}),'uRuntimeEndpoint':'RuntimeEndpoint.xyz'}
                        cfg['attributes']['aY']='atan2(-RuntimeEndpoint.x,-RuntimeEndpoint.z)'
                        l['vertex']=re.sub(r'd = 3\.0 \+ 6\.0\*clamp\(h/1\.0, 0\., 1\.\)', 'd = length(uRuntimeEndpoint.xz)',l['vertex'])
                    else:
                        cfg['anchor']='float3(0,0,0)';cfg['attributes']['aO']='float3(0,0,0)'
                        l['vertex']=re.sub(r'C = aO \+ vec3\(-sin\(aY\), 0\., -cos\(aY\)\)\*d;', 'C = aO;',l['vertex'])
                        l['vertex']=re.sub(r'vF = smoothstep\(0\., \.08, u\)\*\(1\. - smoothstep\(0\., \.12, uTime - aR\)\);', 'vF = 1.;',l['vertex'])
                if (slug=='pressure-provoke' or slug.startswith('piercing-strike')) and phase=='Impact':
                    cfg['anchor']='float3(0,0,0)'
                    cfg['attributes']['aO']='float3(0,f.aO.y,0)'
                    if slug=='pressure-provoke':
                        cfg['attributes']['aO']='float3(0,0,0)'
                        cfg['native_contact_billboard_cm']=34
                        # Reconstruct this billboard's reference coordinates
                        # from UVs in both shader stages, after mesh deformation.
                        l['position_from_uv']=uv_mapping(l['geometry'])
                        # Retarget the stored contact as well as its live path;
                        # this brief .16 s flash must be sampled near its onset.
                        for v in a['aO']['values']:v[0]=v[1]=v[2]=0
                if phase=='Pending' and slug.startswith('cosmic-ray'):
                    cfg['attributes']['aT']='float2(ReferenceTime-1.1,1e9)'
                    l['runtime_uniforms']={**l.get('runtime_uniforms',{}),'uAlly':'f.aO'}
                    if 'aF' in a:cfg['attributes']['aF']='float2(0,0)'
                    # Remaining countdown must come from the owner's progress, never the captured 2 s timer.
                    l['vertex']=re.sub(r'vClock\s*=\s*clamp\([^;]+;', 'vClock = clamp(uResolveProgress,0.,1.);',l['vertex'])
                    l['vertex']='uniform float uResolveProgress;\n'+l['vertex'];l['uniforms']['uResolveProgress']=scalar(0)
                    l['runtime_uniforms']['uResolveProgress']='RuntimeCastProgress'
                if phase in ['Flight','Movement'] and 'aO' in a:
                    t=a.get('aT')
                    flight_age='.7' if slug=='arcane-burst' else '.75' if slug=='war-leap' else '.14' if slug.startswith('quickstep') else '.3'
                    clock='ReferenceTime-'+flight_age
                    if t:cfg['attributes']['aT']=clock if t['size']==1 else 'float2('+clock+',f.aT.y)' if t['size']==2 else 'float3('+clock+',f.aT.y,f.aT.z)'
                    cfg['probe_anchor']=True
                    if 'vS' in l['vertex']:cfg['probe_position']=[1.,0.,0.]
                    if slug=='war-leap':cfg['probe_position']=[2*.3/.55-1,0.,0.]
                    if slug.startswith('quickstep'):cfg['probe_position']=[2*(4*(1-(1-.1/.16)**3))/4.2-1,0.,0.]
                    if slug=='vortex' and l['pool_index']==4:cfg['probe_position']=[-.5,0.,0.]
                if slug.startswith('piercing-strike') and phase=='Impact':
                    # One event = one confirmed contact; recorded demo targets
                    # must not become three hits from a single runtime event.
                    for value in a.values():value['values']=value['values'][:1]
                    l['count']=1
                l['runtime_binding']=cfg
            duration=3.4 if persistent else max(.6,d.get('preview_duration',1.5))
            if slug in ['war-leap','crushing-blow','crushing-blow-ii'] and phase=='AreaImpact':duration=.8
            if slug=='pressure-provoke' and phase=='Impact':duration=.18
            if slug=='sand-shot':duration=.18 if phase=='Impact' else .85
            if slug=='sickness':duration=.25 if phase=='Consume' else .8 if phase=='AreaImpact' else .6
            if slug in ['hemorrhage','poison-sac'] and phase=='Consume':duration=.25
            add(label(slug)+phase,layers,slug,phase,gate,anchor,persistent,duration,
                parent_skill=slug,state_owned=phase not in ['Flight','Movement','Hold','Telegraph'],use_endpoint=anchor=='Link',
                contact=phase=='Impact',target_life=anchor=='Target' or (slug in ['pressure-provoke','sand-shot'] and phase=='Impact'),importance='Essential' if phase=='Active' and anchor=='World' else 'Gameplay',
                composition_review='event groups authored; requires native live capture before promotion')
            if slug=='pressure-provoke':
                twin=copy.deepcopy(layers)
                for l in twin:
                    if 'aK' in l['attributes']:
                        for value in l['attributes']['aK']['values']:value[0]=1
                add('PressureProvokeTank'+phase,twin,'pressure-provoke-tank',phase,gate,anchor,persistent,.18 if phase=='Impact' else .95,use_endpoint=anchor=='Link',contact=phase=='Impact',target_life=phase=='Impact')

if __name__=='__main__':
    combat();new_skills();actions();components();resources();holds_links();skill_phases()
    translated=prepare(R,OUT)
    for job in JOBS:
        if job['slug']=='SandShotCast':job.update(use_range=True,use_cone_angle=True,reference_range=400,reference_cone_angle=math.degrees(1.2),importance='Essential')
        if job['slug'].startswith('GlacialSpike') and job['anchor']=='World':job.update(use_range=True,use_cone_angle=True,reference_range=600,reference_cone_angle=80)
        if job['slug']=='ManaStormActive':job.update(use_radius=True,reference_radius=400)
        if job['slug'].startswith('Volley') and job['phase'] in ['Hold','End']:job.update(use_range=True,reference_range=1800,reference_cone_angle=50)
        # These are authored reference dimensions, never gameplay defaults.
        # Radius/Range/ConeAngle always come from the actual execution/state.
        radii={'CrushingBlowAreaImpact':200,'CrushingBlowIiAreaImpact':200,'WarLeapTelegraph':200,'WarLeapAreaImpact':200,
          'DefiantPresenceActive':600,'RallyITankCast':500,'RallyIWarriorCast':500,'RallyIiTankCast':500,'RallyIiWarriorCast':500,
          'AstralAuraMoonActive':1.15/.192*100,'AstralAuraSunActive':1.15/.192*100,'IcebergProc':255,
          'SmokeBombIAreaImpact':300,'SmokeBombIiAreaImpact':300,
          'CombustIiAreaImpact':84,
          'MistActive':700,'AstralVeilActive':320,'BlackHoleIActive':350,'BlackHoleIiActive':350,
          'EclipseAreaImpact':450,'FullMoonAreaImpact':400,'SmokeBombIActive':300,'SmokeBombIiActive':300,
          'VineFieldIActive':300,'VineFieldIiActive':300,'TempestStormArea':600,'TempestTelegraph':100,
          'TempestGroundImpact':120,'TempestFrostImpact':130,'StaticBoltIGroundArea':250,
          'StaticBoltIiGroundArea':250,'ThunderstrikeIiSplashArea':200,'ThunderstrikeIISplash':200,
          'PoisonSacActive':160,'SicknessAreaImpact':350}
        if job['slug'] in radii:job.update(use_radius=True,reference_radius=radii[job['slug']])
        p=R/job['source'];port=p.with_suffix('.port.json');d=json.loads(port.read_text(encoding='utf-8'))
        if not d['port_ready']:raise RuntimeError(job['slug']+' '+str([l.get('port_error') for l in d['layers']]))
        for l in d['layers']:bind(l)
        port.write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf-8')
        job['source_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
    (R/'Evidence/gameplay-runtime-build-jobs.json').write_text(json.dumps({'schema':'sancta-runtime-jobs/v1','jobs':JOBS,'preserves_historical_assets':True},indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'sources':len(JOBS),'translated':sum(x['ready'] for x in translated),'components':sum(j['form'].startswith('Component.') for j in JOBS),'weapon_profiles':28}))
