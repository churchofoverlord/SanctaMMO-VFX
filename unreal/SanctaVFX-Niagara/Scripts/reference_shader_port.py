"""Experimental source-specific GLSL to material HLSL port.

Each port retains the reference's geometry, uniforms and recorded spawn attributes.
It is a staging method, not an approved performance standard.
"""
import re, json, math, hashlib, base64, pathlib, struct, zlib

def number(value):
    if not math.isfinite(float(value)): raise ValueError('Non-finite source value')
    result=format(float(value),'.9g')
    return result if '.' in result or 'e' in result else result+'.0'

def literal(values):
    if len(values)==1: return number(values[0])
    return 'v%d(%s)'%(len(values),','.join(number(x) for x in values))

def strip_comments(code):
    return re.sub(r'/\*.*?\*/|//[^\n]*','',code,flags=re.S)

def declarations(code):
    found={}
    for qualifier,kind,names in re.findall(r'\b(uniform|varying|attribute)\s+(\w+)\s+([^;]+);',strip_comments(code)):
        for name in names.split(','): found[name.strip()]=(qualifier,kind)
    return found

def end_paren(code,start):
    depth=0
    for i in range(start,len(code)):
        if code[i]=='(': depth+=1
        elif code[i]==')':
            depth-=1
            if not depth:return i+1
    raise ValueError('Unbalanced shader parentheses')

def matrix_products(code):
    matrices=set(re.findall(r'\b(?:mat[234]|float[234]x[234])\s+(\w+)\b',code))
    matrices.update(['projectionMatrix','viewMatrix','modelViewMatrix','modelMatrix','normalMatrix'])
    matrix_functions=set(re.findall(r'\b(?:mat[234]|float[234]x[234])\s+(\w+)\s*\(',code))|{'mat2','mat3','mat4','m2','m3','m4'}
    tokens=matrices|matrix_functions
    pattern=re.compile(r'\b('+'|'.join(sorted(map(re.escape,tokens),key=len,reverse=True))+r')\b')
    for _ in range(256):
        changed=False
        for match in reversed(list(pattern.finditer(code))):
            start=match.start(); stop=match.end()
            if match[1] in matrix_functions:
                tail=re.match(r'\s*\(',code[stop:])
                if not tail:continue
                stop=end_paren(code,stop+tail.end()-1)
            star=re.match(r'\s*\*\s*',code[stop:])
            if not star:continue
            rhs_start=stop+star.end()
            if code[rhs_start:rhs_start+1]=='(':
                rhs_stop=end_paren(code,rhs_start)
            else:
                rhs=re.match(r'(\w+(?:\.[xyzwrgba]+)?)',code[rhs_start:])
                if not rhs:continue
                rhs_stop=rhs_start+rhs.end()
                call=re.match(r'\s*\(',code[rhs_stop:])
                if call:rhs_stop=end_paren(code,rhs_stop+call.end()-1)
            code=code[:start]+'mul('+code[start:stop]+','+code[rhs_start:rhs_stop]+')'+code[rhs_stop:]
            changed=True;break
        if not changed:break
    return code

def translate(code,prefix):
    code=strip_comments(code)
    # GLSL identifiers that are reserved HLSL geometry-shader/interpolation tokens.
    for name in ('line','point','triangle','centroid','sample','linear'):
        code=re.sub(r'\b'+name+r'\b','reference_'+name,code)
    code=re.sub(r'\b(?:uniform|varying|attribute)\s+\w+\s+[^;]+;','',code)
    functions=set(re.findall(r'\b(?:void|float|bool|vec[234]|mat[234])\s+(\w+)\s*\(',code))-{'main'}
    for name in sorted(functions,key=len,reverse=True):code=re.sub(r'\b'+re.escape(name)+r'\b',prefix+name,code)
    code=matrix_products(code)
    for old,new in [('mix','lerp'),('fract','frac'),('mod','gmod'),('texture2D','sampleReference'),('dFdx','ddx'),('dFdy','ddy')]:
        code=re.sub(r'\b'+old+r'\s*\(',new+'(',code)
    # GLSL atan(y,x) is atan2(y,x); atan(x) remains atan(x).
    matches=list(re.finditer(r'\batan\s*\(',code))
    for match in reversed(matches):
        end=end_paren(code,match.end()-1)
        inner=code[match.end():end-1];level=0;comma=False
        for char in inner:
            if char=='(':level+=1
            if char==')':level-=1
            if char==',' and level==0:comma=True
        if comma:code=code[:match.start()]+'atan2('+code[match.end():]
    for size in (2,3,4):
        code=re.sub(r'\bvec'+str(size)+r'\s*\(',f'v{size}(',code)
        code=re.sub(r'\bvec'+str(size)+r'\b',f'float{size}',code)
        code=re.sub(r'\bmat'+str(size)+r'\s*\(',f'm{size}(',code)
        code=re.sub(r'\bmat'+str(size)+r'\b',f'float{size}x{size}',code)
    if prefix=='V_':
        code=re.sub(r'gl_Position\s*=\s*v4\(2\.,2\.,2\.,1\.\);\s*return;', 'Valid=0;return;',code)
        code=re.sub(r'void\s+main\s*\(\s*\)', 'void Vertex()',code)
    else:
        code=re.sub(r'void\s+main\s*\(\s*\)', 'float4 Fragment()',code)
        code=re.sub(r'\bdiscard\s*;', 'return v4(0);',code)
        code=re.sub(r'\bgl_FragColor\s*=', 'return ',code)
        # GLSL commonly has `gl_FragColor=...; return;` in early branches.
        code=re.sub(r'\breturn\s*;', 'return v4(0);',code)
    return code

HELPERS='''
float2 v2(float x){return x.xx;} float2 v2(float x,float y){return float2(x,y);}
float2 v2(float2 x){return x;} float2 v2(float3 x){return x.xy;} float2 v2(float4 x){return x.xy;}
float3 v3(float x){return x.xxx;} float3 v3(float x,float y,float z){return float3(x,y,z);}
float3 v3(float3 x){return x;} float3 v3(float4 x){return x.xyz;}
float3 v3(float2 xy,float z){return float3(xy,z);} float3 v3(float x,float2 yz){return float3(x,yz);}
float4 v4(float x){return x.xxxx;} float4 v4(float x,float y,float z,float w){return float4(x,y,z,w);}
float4 v4(float4 x){return x;} float4 v4(float x,float3 yzw){return float4(x,yzw);}
float4 v4(float x,float y,float2 zw){return float4(x,y,zw);}
float4 v4(float3 xyz,float w){return float4(xyz,w);} float4 v4(float2 xy,float2 zw){return float4(xy,zw);}
float4 v4(float2 xy,float z,float w){return float4(xy,z,w);}
float2x2 m2(float a,float b,float c,float d){return float2x2(a,c,b,d);}
float2x2 m2(float x){return float2x2(x,0,0,x);}
float2x2 m2(float2 a,float2 b){return transpose(float2x2(a,b));}
float3x3 m3(float3 a,float3 b,float3 c){return transpose(float3x3(a,b,c));}
float3x3 m3(float x){return float3x3(x,0,0,0,x,0,0,0,x);}
float3x3 m3(float a,float b,float c,float d,float e,float f,float g,float h,float i){return float3x3(a,d,g,b,e,h,c,f,i);}
float3x3 m3(float4x4 x){return (float3x3)x;} float3x3 m3(float3x3 x){return x;}
float4x4 m4(float x){return float4x4(x,0,0,0,0,x,0,0,0,0,x,0,0,0,0,x);}
float gmod(float a,float b){return a-b*floor(a/b);}
float2 gmod(float2 a,float b){return a-b*floor(a/b);}
float2 gmod(float2 a,float2 b){return a-b*floor(a/b);}
float3 gmod(float3 a,float b){return a-b*floor(a/b);}
float3 gmod(float3 a,float3 b){return a-b*floor(a/b);}
'''

def port(layer,vertex_only=False,normal_only=False):
    if '${' in layer['vertex']+layer['fragment']:raise ValueError('Unresolved reference template')
    fields=declarations(layer['vertex']+('' if vertex_only else layer['fragment']))
    primitive={'float':'float','int':'int','bool':'bool','vec2':'float2','vec3':'float3','vec4':'float4','mat2':'float2x2','mat3':'float3x3','mat4':'float4x4','sampler2D':'Texture2D'}
    declarations_code=[]
    for name,(qualifier,kind) in fields.items():
        if name=='uBG' and kind=='sampler2D' and not layer['uniforms'].get(name,{}).get('png'):
            continue
        declarations_code.append(primitive[kind]+' '+name+';')
        if kind=='sampler2D':declarations_code.append('SamplerState '+name+'Sampler;')
    known=set(fields)
    builtins={'position':'float3','normal':'float3','uv':'float2','cameraPosition':'float3','projectionMatrix':'float4x4','viewMatrix':'float4x4','modelViewMatrix':'float4x4','modelMatrix':'float4x4','normalMatrix':'float3x3','gl_Position':'float4','gl_PointCoord':'float2','gl_FragCoord':'float4','gl_FrontFacing':'bool','Valid':'float'}
    declarations_code += [kind+' '+name+';' for name,kind in builtins.items() if name not in known]
    attrs=[];assignment=[];textures=[]
    for name,(qualifier,kind) in fields.items():
        if qualifier=='attribute':
            data=layer['attributes'].get(name)
            if not data:
                if name=='bary' and layer['geometry'].get('vertex_attributes',{}).get('bary') and not layer['geometry'].get('uv'):
                    assignment.append('f.bary=float3(UV.x,UV.y,1-UV.x-UV.y);')
                    continue
                raise ValueError('Missing recorded attribute '+name)
            values=data['values']
            if layer.get('attribute_texture'):
                info=layer['attribute_texture'];base='index*'+str(info['stride'])+'+'+str(info['offsets'][name])
                fetch=[f'ReadAttribute({base}+{i})' for i in range(data['size'])]
                result=fetch[0] if len(fetch)==1 else f'v{len(fetch)}('+','.join(fetch)+')'
                attrs.append(primitive[kind]+' attr_'+name+'(int index){return '+result+';}')
            else:
                attrs.append(primitive[kind]+' attr_'+name+'(int index){\n'+primitive[kind]+' values['+str(len(values))+']={'+','.join(literal(v) for v in values)+'};return values[clamp(index,0,'+str(len(values)-1)+')];}')
            assignment.append('f.'+name+'=f.attr_'+name+'(ReferenceIndex);')
        elif qualifier=='uniform':
            body=re.sub(r'\b(?:uniform|varying|attribute)\s+\w+\s+[^;]+;','',layer['vertex']+layer['fragment'])
            if not re.search(r'\b'+re.escape(name)+r'\b',body):
                if kind!='sampler2D':assignment.append('f.'+name+'=('+primitive[kind]+')0;')
                continue
            if name in layer.get('runtime_uniforms',{}):expression=layer['runtime_uniforms'][name]
            elif name=='uTime':expression='ReferenceTime'
            elif name=='uRes':expression='ViewportSize'
            else:
                data=layer['uniforms'].get(name)
                if not data:raise ValueError('Missing reference uniform '+name)
                if data['type']=='texture':
                    if not data.get('png') and name=='uBG':
                        textures.append(name);continue
                    textures.append(name);assignment += ['f.'+name+'='+name+';','f.'+name+'Sampler='+name+'Sampler;'];continue
                elif data['type'] in ('color','vector'):expression='f.'+literal(data['values']) if len(data['values'])>1 else literal(data['values'])
                elif isinstance(data.get('value'),(int,float)):expression=number(data['value'])
                else:raise ValueError('Unsupported uniform '+name)
            assignment.append('f.'+name+'='+expression+';')
        else:
            assignment.append('f.'+name+'=('+primitive[kind]+')0;')
    sampling='float4 sampleReference(Texture2D SourceTexture,SamplerState sampleState,float2 coord){return SourceTexture.SampleLevel(sampleState,coord,0);}'
    if layer.get('attribute_texture'):
        width=layer['attribute_texture']['width']
        declarations_code.append('Texture2D AttributeData;')
        attrs.insert(0,f'float ReadAttribute(int index){{uint4 b=(uint4)round(AttributeData.Load(int3(index%{width},index/{width},0))*255);return asfloat(b.r|(b.g<<8)|(b.b<<16)|(b.a<<24));}}')
        assignment.insert(0,'f.AttributeData=AttributeData;')
    vertex=translate(layer['vertex'],'V_')
    fragment=translate(layer['fragment'],'F_')
    for name in textures:
        if name=='uBG' and not layer['uniforms'][name].get('png'):
            fragment=re.sub(r'\bsampleReference\(\s*uBG\s*,','sampleBackground(',fragment)
            sampling+='\nfloat4 sampleBackground(float2 coord){return float4(DecodeSceneColorForMaterialNode(float2(coord.x,1-coord.y)),1);}'
            continue
        vertex=re.sub(r'\bsampleReference\(\s*'+re.escape(name)+r'\s*,',f'sampleReference({name},{name}Sampler,',vertex)
        fragment=re.sub(r'\bsampleReference\(\s*'+re.escape(name)+r'\s*,',f'sampleReference({name},{name}Sampler,',fragment)
    pre='''
int ReferenceIndex=(int)round(Index);
float ReferenceTime=Age*Duration+TimeOrigin;
ReferencePort f;
f.Valid=1;
f.uv=UV;
f.position=float3((WorldPosition.y-ParticlePosition.y)/100,(WorldPosition.z-ParticlePosition.z)/100,-(WorldPosition.x-ParticlePosition.x)/100);
f.normal=normalize(float3(Normal.y,Normal.z,-Normal.x));
f.cameraPosition=float3((CameraPosition.y-ParticlePosition.y)/100,(CameraPosition.z-ParticlePosition.z)/100,-(CameraPosition.x-ParticlePosition.x)/100);
float3 back=normalize(f.cameraPosition-float3(0,1,0)), right=normalize(cross(float3(0,1,0),back)), up=cross(back,right);
float3 cam=f.cameraPosition;
f.viewMatrix=float4x4(right.x,right.y,right.z,-dot(right,cam),up.x,up.y,up.z,-dot(up,cam),back.x,back.y,back.z,-dot(back,cam),0,0,0,1);
float A=1.428148/max(ViewportSize.x/ViewportSize.y,.1),B=1.428148,C=-1.002002,D=-.2002002;
f.projectionMatrix=float4x4(A,0,0,0,0,B,0,0,0,0,C,D,0,0,-1,0);
f.modelViewMatrix=f.viewMatrix;f.modelMatrix=f.m4(1);f.normalMatrix=f.m3(1);
f.gl_Position=f.v4(0);f.gl_PointCoord=UV;f.gl_FragCoord=float4(REFERENCE_SCREEN_UV*ViewportSize,0,1);f.gl_FrontFacing=true;
'''
    pre=pre.replace('REFERENCE_SCREEN_UV','UV' if vertex_only else 'float2(ScreenUV.x,1-ScreenUV.y)')
    if layer.get('source_playback_scale'):
        pre=pre.replace('Age*Duration+TimeOrigin','Age*Duration*'+number(layer['source_playback_scale'])+'+TimeOrigin')
    if layer.get('position_from_uv'):
        # A flat source quad's local coordinates must be interpolated from its
        # UVs. Reconstructing them from displaced world position produced triangle
        # seams on imported billboards and waist rings.
        mapping=layer['position_from_uv']
        pre+='\nf.position=f.'+literal(mapping['offset'])+'+f.'+literal(mapping['u'])+'*UV.x+f.'+literal(mapping['v'])+'*UV.y;\n'
    elif layer.get('mesh_import_reflect_x'):
        # UE's OBJ/FBX importer reflects Unreal Y even with scene conversion off.
        # Undo that reflection when recovering original Three mesh coordinates.
        pre+='\nf.position.x=-f.position.x;f.normal.x=-f.normal.x;\n'
    suffix='''f.Vertex();
if(f.Valid<.5)return float3(0,0,0);
float4 p=f.gl_Position;
float4 vp=float4(p.x/A,p.y/B,-p.w,(p.z+C*p.w)/D);
vp.xyz/=max(abs(vp.w),1e-6)*sign(vp.w);
float3 destination=cam+right*vp.x+up*vp.y+back*vp.z;
return ParticlePosition+float3(-destination.z,destination.x,destination.y)*100-WorldPosition;
''' if vertex_only else '''f.Vertex();if(f.Valid<.5)return float4(0,0,0,0);return f.Fragment();'''
    if normal_only:suffix='f.Vertex();return normalize(float3(-f.vPortNormal.z,f.vPortNormal.x,f.vPortNormal.y));'
    if not vertex_only and layer.get('art_gain'):
        suffix=suffix.replace('return f.Fragment();','float4 artColour=f.Fragment();artColour.rgb*='+number(layer['art_gain'])+';return artColour;')
    code='struct ReferencePort {\n'+'\n'.join(declarations_code)+'\n'+HELPERS+'\n'+sampling+'\n'+'\n'.join(attrs)+'\n'+vertex+'\n'+('' if vertex_only else fragment)+'\n};\n'+pre+'\n'+'\n'.join(assignment)+'\n'+suffix
    return code,textures

def geometry_obj(geometry):
    pos=geometry['position'];normal=geometry.get('normal');uv=geometry.get('uv');index=geometry.get('index') or list(range(len(pos)//3))
    lines=['# Sancta editable mesh extracted from the approved reference, cm, Z up']
    for i in range(0,len(pos),3):lines.append('v '+ ' '.join(number(x) for x in (-pos[i+2]*100,pos[i]*100,pos[i+1]*100)))
    bary=geometry.get('vertex_attributes',{}).get('bary')
    for i in range(len(pos)//3):
        # FBX/OBJ import changes V to Unreal's top-left texture convention.
        values=[uv[i*2],1-uv[i*2+1]] if uv else ([bary['values'][i*3],1-bary['values'][i*3+1]] if bary else [0,0])
        lines.append('vt '+' '.join(number(x) for x in values))
        lines.append('vn '+(' '.join(number(x) for x in (-normal[i*3+2],normal[i*3],normal[i*3+1])) if normal else '1 0 0'))
    for i in range(0,len(index),3):
        vertices=[index[i]+1,index[i+2]+1,index[i+1]+1]
        lines.append('f '+' '.join(f'{v}/{v}/{v}' for v in vertices))
    return '\n'.join(lines)+'\n'

def prepare(root,sources=None):
    sources=sources or root/'Source/ReferencePorts'; geometries=root/'Source/ReferenceGeometry';geometries.mkdir(exist_ok=True)
    textures=root/'Source/ReferenceTextures';textures.mkdir(exist_ok=True)
    reports=[]
    for source in sources.glob('*.json'):
        if 'before-timing' in source.name or source.name.endswith('.port.json'):continue
        data=json.loads(source.read_text(encoding='utf-8'))
        for layer in data['layers']:
            if data['slug'] in ('astral-aura-moon','astral-aura-sun'):
                states=layer['attributes'].get('aS',{}).get('values',[])
                started=[v[0] for v in states if v[0]>-1000]
                if started:layer['preview_time_origin']=min(started)
            offsets={};stride=0
            for name,a in layer['attributes'].items():offsets[name]=stride;stride+=a['size']
            values=[v for i in range(layer['count']) for a in layer['attributes'].values() for v in a['values'][i]]
            pixels=b''.join(struct.pack('<f',v) for v in values)
            width=256;height=max(1,math.ceil(len(values)/width));pixels+=bytes(width*height*4-len(pixels))
            def chunk(kind,payload):return struct.pack('>I',len(payload))+kind+payload+struct.pack('>I',zlib.crc32(kind+payload)&0xffffffff)
            rows=b''.join(b'\x00'+pixels[y*width*4:(y+1)*width*4] for y in range(height))
            png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(rows))+chunk(b'IEND',b'')
            texture_hash=hashlib.sha256(png).hexdigest()[:16];attribute_file=textures/('T_Attributes_'+texture_hash+'.png')
            if not attribute_file.exists():attribute_file.write_bytes(png)
            layer['attribute_texture']={'source':str(attribute_file.relative_to(root)).replace('\\','/'),'name':attribute_file.stem,'width':width,'height':height,'stride':stride,'offsets':offsets,'format':'float32 bits packed into linear uncompressed RGBA8; read mip 0'}
            mesh_data=geometry_obj(layer['geometry']);mesh_hash=hashlib.sha256(mesh_data.encode()).hexdigest()[:16]
            mesh=geometries/('SM_Reference_'+mesh_hash+'.obj')
            if not mesh.exists():mesh.write_text(mesh_data,encoding='utf-8')
            layer['mesh_source']=str(mesh.relative_to(root)).replace('\\','/')
            layer['mesh_name']=mesh.stem
            for name,uniform in layer['uniforms'].items():
                if uniform['type']=='texture' and uniform.get('png'):
                    png=base64.b64decode(uniform['png'].split(',')[1]);texture_hash=hashlib.sha256(png).hexdigest()[:16]
                    texture=textures/('T_Reference_'+texture_hash+'.png')
                    if not texture.exists():texture.write_bytes(png)
                    uniform['texture_source']=str(texture.relative_to(root)).replace('\\','/')
                    uniform['texture_name']=texture.stem
            try:
                layer['hlsl'],layer['texture_inputs']=port(layer)
                layer['hlsl_vertex'],_=port(layer,True)
                if layer.get('lighting','').startswith('default_lit'):layer['hlsl_normal'],_=port(layer,True,True)
                layer['port_status']='source_translated'
            except Exception as error:
                layer['port_status']='needs_manual_translation';layer['port_error']=str(error)
        data['port_ready']=all(l['port_status']=='source_translated' for l in data['layers'])
        (sources/(source.stem+'.port.json')).write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
        reports.append({'slug':data['slug'],'ready':data['port_ready'],'errors':[l.get('port_error') for l in data['layers'] if l.get('port_error')]})
    (root/'Saved/Reference-port-report.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
    return reports

if __name__=='__main__':
    root=pathlib.Path(__file__).resolve().parents[1]
    reports=prepare(root)
    print(json.dumps({'ready':sum(r['ready'] for r in reports),'manual':[r for r in reports if not r['ready']]}))
