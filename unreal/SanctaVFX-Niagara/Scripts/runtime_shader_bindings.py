"""Add opt-in live owner bindings to a derived reference port. Historical ports stay identical."""
import re

INPUTS={'RuntimeEnabled':0.,'RuntimeAge':0.,'RuntimeCount':0.,'RuntimeMax':10.,
 'RuntimeElementA':0.,'RuntimeElementB':1.,'RuntimeOccupied':3.,'RuntimeGainAge':-1.,
 'RuntimePending':0.,'RuntimeCastProgress':0.,'RuntimeReleaseAge':-1.,
 'RuntimeBasisX':[1.,0.,0.,0.],'RuntimeBasisY':[0.,1.,0.,0.],
 'RuntimeBasisZ':[0.,0.,1.,0.],'RuntimeEndpoint':[0.,0.,-6.,0.]}

def bind(layer):
    cfg=layer.get('runtime_binding',{})
    layer['runtime_shader_inputs']={**INPUTS,**cfg.get('defaults',{})}
    for field in ['hlsl','hlsl_vertex','hlsl_normal']:
        if field not in layer:continue
        code=layer[field]
        found=re.search(r'float ReferenceTime=([^;]+);',code)
        if not found:raise ValueError('Unrecognized source clock')
        old=found.group(0)
        clock=cfg.get('clock','RuntimeAge+TimeOrigin')
        code=code.replace(old,'float ReferenceTime=lerp('+found.group(1)+','+clock+',RuntimeEnabled);')
        anchor=cfg.get('anchor','float3(0,0,0)')
        # Compute camera/mesh coordinates in the owner basis. The final vertex
        # displacement uses the same basis, including the exact radius scale.
        point='float3 back=normalize(f.cameraPosition-float3(0,1,0))'
        spatial='''
float3 rx=RuntimeBasisX.xyz,ry=RuntimeBasisY.xyz,rz=RuntimeBasisZ.xyz;
float3 cameraDelta=CameraPosition-ParticlePosition;
float3 localCamera=float3(dot(cameraDelta,rx)/max(dot(rx,rx),1e-6),dot(cameraDelta,ry)/max(dot(ry,ry),1e-6),dot(cameraDelta,rz)/max(dot(rz,rz),1e-6));
f.cameraPosition=lerp(f.cameraPosition,float3(localCamera.y,localCamera.z,-localCamera.x)/100,RuntimeEnabled);
'''
        code=code.replace(point,spatial+'\n'+point)
        # Attribute-dependent anchors must be evaluated after attribute assignment.
        hook='\nfloat3 RuntimeAnchor='+anchor+';\n'
        for name,expr in cfg.get('attributes',{}).items():
            hook+='f.'+name+'=lerp(f.'+name+','+expr+',RuntimeEnabled);\n'
        hook+='RuntimeAnchor='+anchor+';\nf.cameraPosition+=RuntimeAnchor*RuntimeEnabled;\n'
        if not layer.get('position_from_uv'):
            sign=-1 if layer.get('mesh_import_reflect_x') else 1
            hook+='''
float3 wd=WorldPosition-ParticlePosition;
float3 lg=float3(dot(wd,normalize(rx)),dot(wd,normalize(ry)),dot(wd,normalize(rz)));
f.position=lerp(f.position,float3(lg.y*SIGN,lg.z,-lg.x)/100,RuntimeEnabled);
f.normal=lerp(f.normal,normalize(float3(dot(Normal,normalize(ry))*SIGN,dot(Normal,normalize(rz)),-dot(Normal,normalize(rx)))),RuntimeEnabled);
'''.replace('SIGN',str(sign))
        # Reconstruct the view after changing its local camera origin; geometric
        # shaders still see their original coordinates and approved shape.
        hook+='''
cam=f.cameraPosition;
back=normalize(cam-RuntimeAnchor*RuntimeEnabled-float3(0,1,0));right=normalize(cross(float3(0,1,0),back));up=cross(back,right);
f.viewMatrix=float4x4(right.x,right.y,right.z,-dot(right,cam),up.x,up.y,up.z,-dot(up,cam),back.x,back.y,back.z,-dot(back,cam),0,0,0,1);
f.modelViewMatrix=f.viewMatrix;
'''
        if cfg.get('probe_anchor'):
            probe=cfg.get('probe_position',[.000001,.000001,.000001])
            # Evaluate the original vertex at its head centre, then restore all
            # varyings with the real vertex. This preserves each approved mesh
            # and its shader while rebasing its recorded travel to the actual owner.
            hook+='''
if(RuntimeEnabled>.5){
float3 previousAnchor=RuntimeAnchor;
float3 savedPosition=f.position;float2 savedUV=f.uv;
f.position=float3(PROBE);f.uv=float2(.5,.5);f.Vertex();
float4 pp=f.gl_Position;
float4 pv=float4(pp.x/A,pp.y/B,-pp.w,(pp.z+C*pp.w)/D);
pv.xyz/=max(abs(pv.w),1e-6)*sign(pv.w);
RuntimeAnchor=cam+right*pv.x+up*pv.y+back*pv.z;
f.position=savedPosition;f.uv=savedUV;f.Valid=1;
f.cameraPosition+=RuntimeAnchor-previousAnchor;
cam=f.cameraPosition;
back=normalize(cam-RuntimeAnchor-float3(0,1,0));right=normalize(cross(float3(0,1,0),back));up=cross(back,right);
f.viewMatrix=float4x4(right.x,right.y,right.z,-dot(right,cam),up.x,up.y,up.z,-dot(up,cam),back.x,back.y,back.z,-dot(back,cam),0,0,0,1);
f.modelViewMatrix=f.viewMatrix;
}
'''.replace('PROBE',','.join(str(v) for v in probe))
        code=code.replace('f.Vertex();',hook+'\nf.Vertex();')
        if field=='hlsl_vertex':
            if cfg.get('native_contact_billboard_cm'):
                # The contact point is already resolved by the native owner.
                # Preserve the reference UV mask while placing the small quad
                # directly in camera space, without a second authored offset.
                size=float(cfg['native_contact_billboard_cm'])
                code=code.replace('float4 p=f.gl_Position;', '''
if(RuntimeEnabled>.5){
float3 toCamera=normalize(CameraPosition-ParticlePosition);
float3 contactRight=normalize(cross(float3(0,0,1),toCamera));
float3 contactUp=cross(toCamera,contactRight);
float2 contactUV=(UV*2-1)*CONTACT_SIZE;
return ParticlePosition+toCamera*2+contactRight*contactUV.x+contactUp*contactUV.y-WorldPosition;
}
float4 p=f.gl_Position;'''.replace('CONTACT_SIZE',str(size)))
            old_return='return ParticlePosition+float3(-destination.z,destination.x,destination.y)*100-WorldPosition;'
            new_return='''
destination-=RuntimeAnchor*RuntimeEnabled;
float3 referencePosition=float3(-destination.z,destination.x,destination.y)*100;
float3 ownerPosition=rx*referencePosition.x+ry*referencePosition.y+rz*referencePosition.z;
return ParticlePosition+lerp(referencePosition,ownerPosition,RuntimeEnabled)-WorldPosition;
'''
            if old_return not in code:raise ValueError('Unrecognized reference displacement')
            code=code.replace(old_return,new_return)
        elif field=='hlsl_normal':
            code=code.replace('return float3(-f.vPortNormal.z,f.vPortNormal.x,f.vPortNormal.y);',
             'float3 n=float3(-f.vPortNormal.z,f.vPortNormal.x,f.vPortNormal.y); return normalize(lerp(n,rx*n.x+ry*n.y+rz*n.z,RuntimeEnabled));')
        if field=='hlsl' and cfg.get('ground_fade_cm'):
            # Billboard fog crosses the opaque floor. Fade its actual displaced
            # height before that intersection, rather than exposing quad cuts.
            height=float(cfg['ground_fade_cm'])/100
            code=code.replace('return f.Fragment();','''
float4 mistClip=f.gl_Position;
float4 mistView=float4(mistClip.x/A,mistClip.y/B,-mistClip.w,(mistClip.z+C*mistClip.w)/D);
mistView.xyz/=max(abs(mistView.w),1e-6)*sign(mistView.w);
float3 mistLocal=cam+right*mistView.x+up*mistView.y+back*mistView.z-RuntimeAnchor*RuntimeEnabled;
float4 mistColour=f.Fragment();
mistColour*=lerp(1.,smoothstep(0.,FADE_HEIGHT,mistLocal.y),RuntimeEnabled);
return mistColour;'''.replace('FADE_HEIGHT',str(height)))
        if field=='hlsl' and layer.get('runtime_composite_contrast'):
            if 'return f.Fragment();' in code:
                code=code.replace('return f.Fragment();','float4 artColour=f.Fragment();return artColour;')
            if 'return artColour;' not in code:raise ValueError('Unrecognized contrast output')
            code=code.replace('return artColour;','artColour.a=saturate(max(artColour.r,max(artColour.g,artColour.b)));return artColour;')
        layer[field]=code
    return layer
