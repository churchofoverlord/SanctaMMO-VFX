"""Small editable meshes authored for the October art pass, Three coordinates."""
import math
def plane(width=2,height=2,x_segments=1,y_segments=1):
    p=[];n=[];uv=[];idx=[]
    for j in range(y_segments+1):
        for i in range(x_segments+1):
            u=i/x_segments;v=j/y_segments;p.extend([(u-.5)*width,(v-.5)*height,0]);n.extend([0,0,1]);uv.extend([u,v])
    for j in range(y_segments):
        for i in range(x_segments):
            a=j*(x_segments+1)+i;b=a+1;c=a+x_segments+1;d=c+1;idx.extend([a,b,d,a,d,c])
    return {'position':p,'normal':n,'uv':uv,'index':idx,'vertex_attributes':{}}
def sphere(r=1,segments=32,rings=16):
    p=[];n=[];uv=[];idx=[]
    for j in range(rings+1):
        ph=math.pi*j/rings
        for i in range(segments+1):
            th=2*math.pi*i/segments;x=math.sin(ph)*math.cos(th);y=math.cos(ph);z=math.sin(ph)*math.sin(th)
            p.extend([x*r,y*r,z*r]);n.extend([x,y,z]);uv.extend([i/segments,j/rings])
    for j in range(rings):
        for i in range(segments):
            a=j*(segments+1)+i;b=a+1;c=a+segments+1;d=c+1
            if j:idx.extend([a,c,b])
            if j<rings-1:idx.extend([b,c,d])
    return {'position':p,'normal':n,'uv':uv,'index':idx,'vertex_attributes':{}}
def uv_mapping(geometry):
    # Only use a proven affine UV mapping, never for a folded mesh.
    import numpy as np
    if not geometry.get('uv'):return None
    p=np.array(geometry['position']).reshape(-1,3);uv=np.array(geometry['uv']).reshape(-1,2)
    a=np.column_stack([np.ones(len(uv)),uv]);m=np.linalg.lstsq(a,p,rcond=None)[0]
    if np.max(np.abs(a@m-p))>1e-5:return None
    return {'offset':m[0].tolist(),'u':m[1].tolist(),'v':m[2].tolist()}
def crescent(segments=48,sides=10):
    p=[];n=[];uv=[];idx=[]
    for i in range(segments+1):
        s=i/segments;angle=-2.25+s*4.5;rad=.24;tube=.078*max(math.sin(math.pi*s),0)**.6+.005
        for j in range(sides+1):
            a=j/sides*2*math.pi;nx=math.cos(angle)*math.cos(a);ny=math.sin(angle)*math.cos(a);nz=math.sin(a)
            p.extend([math.cos(angle)*rad+nx*tube-.05,math.sin(angle)*rad+ny*tube,nz*tube]);n.extend([nx,ny,nz]);uv.extend([s,j/sides])
    for i in range(segments):
        for j in range(sides):
            a=i*(sides+1)+j;b=a+1;c=a+sides+1;d=c+1;idx.extend([a,c,b,b,c,d])
    return {'position':p,'normal':n,'uv':uv,'index':idx,'vertex_attributes':{}}

def ice_spire():
    """Long angular spire with planar facets and a single continuously tapered tip."""
    base=[(-.45,0,-.28),(-.12,0,-.42),(.34,0,-.26),(.42,0,.25),(.03,0,.32),(-.38,0,.19)]
    shoulder=[(x*.72,.24,z*.72) for x,_,z in base]
    tip=(.015,1.,-.025)
    p=[];normals=[];uv=[];bary=[]
    def triangle(a,b,c):
        ab=[b[i]-a[i] for i in range(3)];ac=[c[i]-a[i] for i in range(3)]
        n=[ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0]]
        length=math.sqrt(sum(v*v for v in n));n=[v/length for v in n]
        for vertex,weights in zip((a,b,c),((1,0,0),(0,1,0),(0,0,1))):
            p.extend(vertex);normals.extend(n);uv.extend((vertex[0]+.5,vertex[1]));bary.extend(weights)
    for i in range(len(base)):
        j=(i+1)%len(base)
        triangle(base[i],shoulder[i],base[j]);triangle(base[j],shoulder[i],shoulder[j])
        triangle(shoulder[i],tip,shoulder[j])
        triangle((0,0,0),base[i],base[j])
    # The reference port stores per-face barycentrics in imported UV channels.
    return {'position':p,'normal':normals,'uv':None,'index':None,
            'vertex_attributes':{'bary':{'size':3,'values':bary}}}
