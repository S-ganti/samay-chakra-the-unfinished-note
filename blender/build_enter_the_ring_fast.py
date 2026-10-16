"""Build an original editable 2.5D Enter the Ring art/level study.
Run: blender --background --factory-startup --python build_enter_the_ring.py
"""
import bpy, math, random, json
from mathutils import Vector
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
random.seed(8401)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for col in list(bpy.data.collections):
    if col.name != 'Collection': bpy.data.collections.remove(col)
base = bpy.data.collections.get('Collection')
if base: bpy.data.collections.remove(base)
scene = bpy.context.scene
COLS = {}
for name in ['00 sky', '10 distant terrain', '20 ring monument', '30 foliage', '40 gameplay path', '50 foreground', '60 atmosphere', '70 lights']:
    c = bpy.data.collections.new(name); scene.collection.children.link(c); COLS[name] = c

def move(obj, col):
    for c in list(obj.users_collection): c.objects.unlink(obj)
    COLS[col].objects.link(obj)
    return obj

def mat(name, color, rough=.7, metallic=0, emission=0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Roughness'].default_value=rough
    bs.inputs['Metallic'].default_value=metallic
    if emission:
        bs.inputs['Emission Color'].default_value=(*color,1); bs.inputs['Emission Strength'].default_value=emission
    return m

def emiss(name, color, strength=1):
    m=bpy.data.materials.new(name); m.use_nodes=True
    nt=m.node_tree; nt.nodes.clear(); o=nt.nodes.new('ShaderNodeOutputMaterial'); e=nt.nodes.new('ShaderNodeEmission')
    e.inputs[0].default_value=(*color,1); e.inputs[1].default_value=strength; nt.links.new(e.outputs[0],o.inputs['Surface'])
    return m

def texture_stone(name,tint):
    m=mat(name,tint,.85,.05); n=m.node_tree.nodes; l=m.node_tree.links; bs=n.get('Principled BSDF')
    texcoord=n.new('ShaderNodeTexCoord'); mapping=n.new('ShaderNodeVectorMath'); mapping.operation='SCALE'; mapping.inputs[3].default_value=.48
    l.new(texcoord.outputs['Object'],mapping.inputs[0])
    diff=n.new('ShaderNodeTexImage'); diff.image=bpy.data.images.load(str(ASSETS/'rabdentse_ruins_wall_diff_1k.jpg'),check_existing=True); diff.projection='BOX'; diff.projection_blend=.2
    l.new(mapping.outputs[0],diff.inputs['Vector'])
    mix=n.new('ShaderNodeMixRGB'); mix.blend_type='MULTIPLY'; mix.inputs[0].default_value=.6; mix.inputs[2].default_value=(*tint,1)
    l.new(diff.outputs['Color'],mix.inputs[1]); l.new(mix.outputs[0],bs.inputs['Base Color'])
    rough=n.new('ShaderNodeTexImage'); rough.image=bpy.data.images.load(str(ASSETS/'rabdentse_ruins_wall_rough_1k.jpg'),check_existing=True); rough.image.colorspace_settings.name='Non-Color'; rough.projection='BOX'; rough.projection_blend=.2
    l.new(mapping.outputs[0],rough.inputs['Vector']); l.new(rough.outputs[0],bs.inputs['Roughness'])
    normal=n.new('ShaderNodeTexImage'); normal.image=bpy.data.images.load(str(ASSETS/'rabdentse_ruins_wall_nor_gl_1k.jpg'),check_existing=True); normal.image.colorspace_settings.name='Non-Color'; normal.projection='BOX'; normal.projection_blend=.2
    l.new(mapping.outputs[0],normal.inputs['Vector']); bump=n.new('ShaderNodeBump'); bump.inputs['Strength'].default_value=.3; bump.inputs['Distance'].default_value=.14
    l.new(diff.outputs['Color'],bump.inputs['Height']); l.new(bump.outputs[0],bs.inputs['Normal'])
    # The acquired normal map is retained and packed for UV-refined production assets.
    normal.label='CC0 source normal - available for later UV refinement'
    return m

stone=texture_stone('Rabdentse / warm weathered carved stone',(0.61,.44,.27))
pathmat=texture_stone('Rabdentse / wet path flagstones',(.35,.41,.36))
bronze=mat('Oxidised bronze highlights',(.25,.18,.075),.48,.7)
darkstone=mat('Deep carved recesses',(.065,.084,.075),.9,.02)
moss=mat('Moss on upper surfaces',(.105,.16,.063),.94)
leafmat=mat('Deep foreground fern',(.019,.061,.046),.85)
leaflight=mat('Warm leaf rim',(.095,.16,.075),.9)
bark=mat('Tree bark',(.038,.06,.051),.95)
lampmat=emiss('Butter lamp flame',(1,.31,.07),7)
rimlight=emiss('Time ring / amber inlay',(.96,.35,.07),2.5)
metal=mat('Lamp oil bronze',(.18,.095,.035),.3,.8)

# Geometry helpers.
def mesh(name,verts,faces,material,col):
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    ob=bpy.data.objects.new(name,me); COLS[col].objects.link(ob)
    if material: me.materials.append(material)
    return ob

def cube(name,loc,scale,material,col='20 ring monument',bevel=0):
    vs=[(x*scale[0]/2,y*scale[1]/2,z*scale[2]/2) for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
    ob=mesh(name,vs,[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)],material,col);ob.location=loc
    if bevel:
        mod=ob.modifiers.new('Soft chipped edges','BEVEL');mod.width=bevel;mod.segments=2
    return ob

def ico(name,loc,scale,material,col='50 foreground',sub=1):
    import bmesh
    bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=sub,radius=1)
    me=bpy.data.meshes.new(name);bm.to_mesh(me);bm.free()
    ob=bpy.data.objects.new(name,me);COLS[col].objects.link(ob);ob.location=loc;ob.scale=scale;ob.rotation_euler=(random.random(),random.random(),random.random()*6.28);me.materials.append(material)
    for face in me.polygons:face.use_smooth=True
    return ob

def uvball(name,loc,scale,material,col):
    import bmesh
    bm=bmesh.new();bmesh.ops.create_uvsphere(bm,u_segments=12,v_segments=6,radius=1)
    me=bpy.data.meshes.new(name);bm.to_mesh(me);bm.free()
    ob=bpy.data.objects.new(name,me);COLS[col].objects.link(ob);ob.location=loc;ob.scale=scale;me.materials.append(material)
    for face in me.polygons:face.use_smooth=True
    return ob

def cyl_between(name,a,b,r1,r2,material,col='20 ring monument',verts=12):
    d=Vector(b)-Vector(a);mid=(Vector(a)+Vector(b))/2
    vs=[(r*math.cos(i*2*math.pi/verts),r*math.sin(i*2*math.pi/verts),z) for r,z in [(r1,-d.length/2),(r2,d.length/2)] for i in range(verts)]
    fs=[(i,(i+1)%verts,(i+1)%verts+verts,i+verts) for i in range(verts)]+[tuple(reversed(range(verts))),tuple(range(verts,2*verts))]
    ob=mesh(name,vs,fs,material,col);ob.location=mid;ob.rotation_euler=d.to_track_quat('Z','Y').to_euler();return ob

def torus(name,center,major,minor,material,col='20 ring monument',segments=160):
    vs=[];fs=[]
    for i in range(segments):
        a=i*2*math.pi/segments
        for j in range(10):
            b=j*2*math.pi/10;r=major+minor*math.cos(b);vs.append((r*math.cos(a),minor*math.sin(b),r*math.sin(a)))
    for i in range(segments):
        for j in range(10):fs.append((i*10+j,((i+1)%segments)*10+j,((i+1)%segments)*10+(j+1)%10,i*10+(j+1)%10))
    ob=mesh(name,vs,fs,material,col);ob.location=center
    for face in ob.data.polygons:face.use_smooth=True
    return ob

def line(name,points,material,r=.025,col='20 ring monument'):
    cu=bpy.data.curves.new(name,'CURVE'); cu.dimensions='3D'; cu.bevel_depth=r; cu.bevel_resolution=1
    sp=cu.splines.new('POLY'); sp.points.add(len(points)-1)
    for p,co in zip(sp.points,points): p.co=(*co,1)
    ob=bpy.data.objects.new(name,cu); COLS[col].objects.link(ob); cu.materials.append(material); return ob

# Backdrop gradient: the final art is purposefully atmospheric rather than a flat HDR panorama.
sky=bpy.data.materials.new('Painted dusk sky gradient'); sky.use_nodes=True
n=sky.node_tree.nodes; l=sky.node_tree.links; n.clear(); out=n.new('ShaderNodeOutputMaterial'); e=n.new('ShaderNodeEmission'); e.inputs[1].default_value=.55
coord=n.new('ShaderNodeTexCoord'); sep=n.new('ShaderNodeSeparateXYZ'); ramp=n.new('ShaderNodeValToRGB')
l.new(coord.outputs['Generated'],sep.inputs[0]); l.new(sep.outputs['Z'],ramp.inputs[0]); l.new(ramp.outputs[0],e.inputs[0]); l.new(e.outputs[0],out.inputs[0])
cr=ramp.color_ramp; cr.elements.remove(cr.elements[1]); cr.elements[0].position=0; cr.elements[0].color=(.62,.31,.105,1)
for pos,col in [(0.30,(.58,.33,.17,1)),(.54,(.20,.29,.31,1)),(.77,(.075,.16,.21,1)),(1,(.028,.079,.12,1))]: cr.elements.new(pos).color=col
cube('Cyclorama / horizon to blue hour',(0,-69,20),(150,.1,60),sky,'00 sky')
sunmat=emiss('Sun behind the chakra',(1,.5,.16),1.4)
uvball('Low dusk sun',(-5,-62,7),(3.6,.12,3.6),sunmat,'00 sky')
# Wisps: irregular bands, not repeated flat rectangular clouds.
cloudcols=[emiss('Cloud dusk %d'%i,c,.5) for i,c in enumerate([(.29,.24,.19),(.40,.30,.19),(.16,.23,.25)])]
for k in range(10):
    z=random.uniform(9,22); xc=random.uniform(-40,40); length=random.uniform(6,26)
    verts=[(xc-length,-60,z)];
    for j in range(13): verts.append((xc-length+2*length*j/12,-60,z+random.uniform(.05,.35)+.22*math.sin(j/12*math.pi)))
    for j in reversed(range(13)): verts.append((xc-length+2*length*j/12,-60,z-random.uniform(.05,.18)))
    mesh('Dusk cloud wisp %02d'%k,verts,[tuple(range(len(verts)))],random.choice(cloudcols),'00 sky')

# Layered distant hills and hillsides. Material values fade towards the horizon.
for k,(y,baseh,amp,color) in enumerate([(-53,1.5,6.8,(.25,.30,.28)),(-43,.4,6.2,(.16,.25,.24)),(-31,-1,5.9,(.085,.18,.17)),(-20,-1.6,4.5,(.045,.125,.115))]):
    mm=emiss('Atmospheric ridge %d'%k,color,.65)
    vs=[(-70,y,-15)]
    for i in range(101):
        x=-70+i*1.4; z=baseh+amp*(.34+.25*math.sin(x*.13+k)+.16*math.sin(x*.29-k)+.07*math.sin(x*.76+k))+random.uniform(-.28,.28)
        vs.append((x,y,z))
    vs.append((70,y,-15)); mesh('Distant ridge %02d'%k,vs,[tuple(range(len(vs)))],mm,'10 distant terrain')

# Ring geometry: original segmented Indian-inspired wheel, deliberately no copied game assets.
C=Vector((-3,-3,8.8)); RAD=7.25
# Thick annular masonry with front/back faces.
def ring_band(name,inner,outer,depth,front,material):
    seg=160; vv=[]; ff=[]
    for yy in [front,front-depth]:
        for rr in [inner,outer]:
            for i in range(seg):
                t=2*math.pi*i/seg; vv.append((C.x+rr*math.cos(t),C.y+yy,C.z+rr*math.sin(t)))
    for i in range(seg):
        j=(i+1)%seg
        ff.extend([(i,j,seg+j,seg+i),(2*seg+i,3*seg+i,3*seg+j,2*seg+j),(seg+i,seg+j,3*seg+j,3*seg+i),(i,2*seg+i,2*seg+j,j)])
    ob=mesh(name,vv,ff,material,'20 ring monument'); mod=ob.modifiers.new('Worn edges','BEVEL'); mod.width=.045; mod.segments=2
    ob.modifiers.new('Weighted normals','WEIGHTED_NORMAL'); return ob
ring_band('Main solid annular masonry',6.1,7.4,.85,.4,stone)
ring_band('Outer carved archivolt',7.37,7.62,.72,.57,stone)
ring_band('Inner portal collar',2.55,3.05,.85,.58,stone)
ring_band('Outer structural drum',6.3,7.1,1.2,-.25,darkstone)
for r,small,ma,y in [(7.63,.07,bronze,.66),(7.39,.09,stone,.66),(6.15,.13,bronze,.62),(6.39,.07,rimlight,.67),(7.10,.035,bronze,.7),(2.62,.11,bronze,.67),(2.98,.06,rimlight,.66),(3.15,.07,stone,.35)]: torus('Concentric moulding %.2f'%r,C+Vector((0,y,0)),r,small,ma)
# 64 individually carved stones with staggered gaps and geometric relief.
for i in range(64):
    t=i*math.tau/64
    a=C+Vector((6.18*math.cos(t),.63,6.18*math.sin(t))); b=C+Vector((7.37*math.cos(t),.63,7.37*math.sin(t)))
    cyl_between('Radial archivolt carved seam %02d'%i,a,b,.025,.025,darkstone,verts=6)
    for rr in [6.65,7.22]:
        pos=C+Vector((rr*math.cos(t),.78,rr*math.sin(t)))
        ob=cube('Raised geometric stone tessera',pos,(.16,.12,.27),stone,bevel=.035); ob.rotation_euler[1]=-t+math.pi/2
# 16 substantial stone spokes, fluted edges and neck rings.
for i in range(16):
    t=i*math.tau/16
    radial=Vector((math.cos(t),0,math.sin(t))); tangent=Vector((-math.sin(t),0,math.cos(t)))
    a=C+radial*3.05+Vector((0,.03,0)); b=C+radial*6.12+Vector((0,.03,0))
    cyl_between('Radial stone rib %02d'%i,a,b,.20,.31,stone,verts=8)
    for side in [-1,1]: cyl_between('Fluted bronze rib edge',a+tangent*.16+Vector((0,.25,0)),b+tangent*.23+Vector((0,.25,0)),.025,.04,bronze,verts=6)
    for dist in [3.28,3.63,5.55,5.91]:
        p=C+radial*dist+Vector((0,.05,0)); cyl_between('Rib stone collar',p-radial*.065,p+radial*.065,.30,.30,stone,verts=12)
    mid=C+radial*4.56+Vector((0,.38,0)); uvball('Rib relief jewel',mid,(.18,.085,.18),bronze,'20 ring monument')
# Eight rosette medallions with 10 carved petals and central bosses.
for i in range(8):
    t=i*math.tau/8+math.pi/8; p=C+Vector((6.79*math.cos(t),.85,6.79*math.sin(t)))
    cyl_between('Medallion base %02d'%i,p-Vector((0,.07,0)),p+Vector((0,.07,0)),.43,.43,darkstone,verts=32)
    torus('Rosette raised border',p+Vector((0,.1,0)),.39,.045,bronze,segments=40)
    for j in range(10):
        tt=j*math.tau/10; q=p+Vector((.23*math.cos(tt),.17,.23*math.sin(tt)))
        petal=uvball('Carved lotus petal',q,(.08,.055,.17),stone,'20 ring monument'); petal.rotation_euler[1]=math.pi/2-tt
    uvball('Rosette centre',p+Vector((0,.22,0)),(.12,.07,.12),bronze,'20 ring monument')
# Portal inner scallop and jewel work.
for i in range(48):
    t=i*math.tau/48; p=C+Vector((2.84*math.cos(t),.75,2.84*math.sin(t)))
    uvball('Portal border bead',p,(.06,.05,.06),bronze,'20 ring monument')
# Buttresses and crumbled plinths, heavily bevelled silhouettes.
for x in [-9.9,3.9]:
    cube('Monument footing',(x,-3,1),(2.2,2.9,2.0),stone,bevel=.13)
    cube('Footing cornice',(x,-3,2.04),(2.5,3.1,.34),stone,bevel=.09)
    cube('Buttress shaft',(x,-3,3.2),(1.1,1.8,2.1),stone,bevel=.1)
    cube('Stepped capital',(x,-3,4.4),(1.5,2,.28),bronze,bevel=.08)
    for zz in [.45,.95,1.5,2.6,3.2,3.8]: cube('Buttress seam',(x,-1.48 if zz<2 else -2.05,zz),(2.0 if zz<2 else .96,.018,.028),darkstone)
# Top centre crown / three low stair-like blocks.
for j in range(3): cube('Crown stepped finial',(C.x,C.y,C.z+7.6+j*.3),(.96-j*.21,.9-j*.1,.34),stone,bevel=.05)
uvball('Crown amber point',(C.x,C.y+.45,C.z+8.51),(.06,.06,.06),rimlight,'20 ring monument')

# Ground, causeway, readable walk route and low landing plinths.
water=mat('Still river / dusk reflections',(.028,.072,.068),.16,.35)
cube('Water plane',(0,-1,-.65),(110,95,.2),water,'10 distant terrain')
# A thick broken bridge in front of the ring, flanked by river.
for side in [-1,1]:
    cube('Causeway support',(-6 if side<0 else 10,2,-.65),(20 if side<0 else 12,5.2,2),darkstone,'40 gameplay path',.16)
for i in range(43):
    x=-20.5+i*.98
    for j in range(3):
        y=.6+j*1.36; z=.08+random.uniform(-.035,.035)
        ob=cube('Walkable flagstone %02d_%d'%(i,j),(x+random.uniform(-.03,.03),y,z),(.96,1.32,.3),pathmat,'40 gameplay path',.045)
        ob['walkable']=True
        if random.random()<.32: ico('Moss in flagstone joint',(x,y+random.uniform(-.6,.6),z+.18),(.3,.08,.022),moss,'40 gameplay path')
# Chipped stone balustrade remnants behind path; keep front silhouette open.
for i,x in enumerate([-16,-13.7,-11.4,-9.1,5.5,8,10.4,12.7,15,17]):
    h=random.uniform(.7,1.3); cube('Causeway parapet remnant',(x,-.7,h/2),(1.4,.7,h),stone,'40 gameplay path',.08)
    cube('Parapet worn cap',(x,-.7,h),(1.5,.85,.15),pathmat,'40 gameplay path',.05)
# Double-jump plinth arrangement, short hops/flight ascent; heights in metres.
for idx,(x,z,w) in enumerate([(8.5,1.25,2.4),(5.0,2.45,2.0),(1.6,3.65,1.8)]):
    cube('Landing %d / collision proxy'%(idx+1),(x,2.2,z-.18),(w,2.0,.38),pathmat,'40 gameplay path',.08)
    cube('Landing %d / carved underlip'%(idx+1),(x,2.2,z-.43),(w-.3,1.6,.22),stone,'40 gameplay path',.07)
    for xx in [x-w/2+.25,x+w/2-.25]:
        uvball('Landing amber marker',(xx,3.24,z+.01),(.045,.035,.045),rimlight,'40 gameplay path')
    scene['landing_%d_height_m'%(idx+1)]=z
# Scattered rubble on margins only.
for i in range(90):
    x=random.uniform(-20,20); y=random.choice([random.uniform(-.9,-.25),random.uniform(4.3,7.4)])
    s=random.uniform(.13,.58); ico('Causeway side rubble',(x,y,-.02),(s,s*.7,s*.55),pathmat,'50 foreground',sub=1)

# Distant trees, bare branchwork and small broadleaf masses; front tree frames the view.
def tree(name,x,y,z,height,material,foliage=True,col='30 foliage',depth=0):
    pts=[Vector((x,y,z)),Vector((x+random.uniform(-.35,.35),y,z+height*.52)),Vector((x+random.uniform(-.55,.55),y,z+height))]
    cyl_between(name+' trunk',pts[0],pts[1],height*.065,height*.036,material,col)
    cyl_between(name+' upper trunk',pts[1],pts[2],height*.036,.018,material,col)
    for k in range(6):
        frac=.4+k*.085; start=pts[0]+Vector((0,0,height*frac)); side=(-1 if k%2==0 else 1); end=start+Vector((side*height*random.uniform(.22,.42),random.uniform(-.5,.5),height*random.uniform(.18,.32)))
        cyl_between(name+' bough',start,end,height*.022,.009,material,col)
        tip=end+Vector((side*height*.12,0,height*.06)); cyl_between(name+' twig',end,tip,.02,.004,material,col,verts=6)
        if foliage:
            ico(name+' canopy',end,(height*.19,height*.11,height*.13),material,col,sub=2)
            ico(name+' outer leaf crown',tip,(height*.13,height*.1,height*.09),material,col,sub=1)
for layer,y,c in [(0,-27,(.035,.101,.093)),(1,-16,(.025,.08,.065))]:
    tm=emiss('Tree silhouette distance %d'%layer,c,.7)
    for i in range(29):
        x=-35+i*2.5+random.uniform(-.7,.7); tree('Distant forest %d_%02d'%(layer,i),x,y+random.uniform(-1,1),.3,random.uniform(3.1,8),tm,True,'30 foliage')
# Side trunks with carefully limited canopy crossing the top edge.
for x,y,h in [(-19,7,17),(21,4,18),(-23,0,21),(25,-2,20)]: tree('Ancient framing tree',x,y,-.2,h,bark,False,'50 foreground')
# Branch arcs frame upper sides. Leaf mesh cards are real geometry, editable and inexpensive.
leafverts=[]; leaffaces=[]
for side in [-1,1]:
    for k in range(6):
        start=Vector((side*21,6-k*.3,10.5+k*1.1)); end=Vector((side*(12-k*.9),5-k*.2,17+k*.5))
        cyl_between('Framing canopy branch',start,end,.17,.025,bark,'50 foreground')
        for j in range(34):
            q=start.lerp(end,random.random())+Vector((random.uniform(-.9,.9),random.uniform(-.8,.8),random.uniform(-.6,.7)))
            angle=random.uniform(0,math.tau); length=random.uniform(.18,.43); width=length*.42
            d=Vector((math.cos(angle),.2,math.sin(angle)))*length; t=Vector((-math.sin(angle),0,math.cos(angle)))*width
            idx=len(leafverts); leafverts.extend([q-d,q+t,q+d,q-t,q+Vector((0,.03,0))]); leaffaces.extend([(idx,idx+1,idx+4),(idx+1,idx+2,idx+4),(idx+2,idx+3,idx+4),(idx+3,idx,idx+4)])
mesh('Individual canopy leaves',leafverts,leaffaces,leafmat,'50 foreground')

# Ferns with curved stems and paired narrow pinnae, all in original consolidated meshes.
def fern(name,x,y,z,size,material):
    vs=[]; fs=[]
    for fr in range(7):
        ang=fr*math.tau/7+random.uniform(-.12,.12); length=size*random.uniform(.8,1.3)
        direction=Vector((math.cos(ang),math.sin(ang)*.55,0)); root=Vector((x,y,z)); points=[]
        for j in range(10):
            t=j/9; p=root+direction*(length*t)+Vector((0,0,length*(1.25*t-.86*t*t))); points.append(p)
            if j==0: continue
            tangent=Vector((-math.sin(ang),math.cos(ang)*.6,.2))
            leaflen=length*.22*(math.sin(t*math.pi)**.7)
            for side in [-1,1]:
                tip=p+tangent*side*leaflen-direction*length*.08+Vector((0,0,leaflen*.08)); idx=len(vs)
                vs.extend([p-direction*.025*size,tip,p+direction*.025*size]); fs.append((idx,idx+1,idx+2))
        line(name+' curved rachis',points,material,.012*size,'50 foreground')
    return mesh(name+' pinnae',vs,fs,material,'50 foreground')
for i in range(52):
    x=random.uniform(-22,22); y=random.uniform(5.3,9); sz=random.uniform(.45,1.3)
    fern('Foreground fern %02d'%i,x,y,-.2,sz,leafmat if i%3 else leaflight)
for i in range(23):
    x=random.uniform(-21,21); y=random.uniform(-1.3,-.2); fern('Moss garden fern %02d'%i,x,y,.0,random.uniform(.3,.6),leaflight)
# Larger foreground river rocks retain crystalline silhouettes and textured surface detail.
for i in range(40):
    x=random.uniform(-24,24); y=random.uniform(8,14); s=random.uniform(.6,1.8)
    ico('Foreground river boulder %02d'%i,(x,y,-.6),(s,s*.7,s*.65),pathmat,'50 foreground',sub=2)
    if i%2==0: ico('Boulder moss patch',(x+.1,y-.1,-.1),(s*.55,s*.5,s*.18),moss,'50 foreground',sub=1)

# Butter lamps: visible warm wayfinding markers, full little bowls/stems with practical lights.
def light(name,kind,loc,color,power,size=1):
    data=bpy.data.lights.new(name,kind); data.energy=power; data.color=color
    if kind=='AREA': data.shape='DISK'; data.size=size
    if kind=='POINT': data.shadow_soft_size=size
    ob=bpy.data.objects.new(name,data); ob.location=loc; COLS['70 lights'].objects.link(ob); return ob
for i,(x,y) in enumerate([(-16,3.6),(-10,3.8),(-5.5,3.6),(-.4,4.0),(5,4),(11,3.7),(17,3.7),(-7,-.5),(1,-.5)]):
    z=.34
    cyl_between('Butter lamp stem', (x,y,z-.16),(x,y,z+.11),.07,.045,metal,'40 gameplay path')
    uvball('Butter lamp bowl',(x,y,z+.14),(.18,.18,.07),metal,'40 gameplay path')
    uvball('Lamp flame',(x,y,z+.29),(.035,.035,.1),lampmat,'40 gameplay path')
    light('Warm practical %02d'%i,'POINT',(x,y,z+.48),(1,.24,.055),22,.4)
# Drifting fireflies make depth perceptible; sparse rather than particle noise.
for i in range(85):
    x=random.uniform(-18,18); y=random.uniform(-7,8); z=random.uniform(.5,12)
    r=random.uniform(.009,.025); uvball('Drifting ember %02d'%i,(x,y,z),(r,r,r),rimlight,'60 atmosphere')

# Small original traveler silhouette for scale; no borrowed GRIS character design.
trav=mat('Traveler / indigo cloak',(.024,.05,.068),.95)
scarf=mat('Traveler / saffron cloth',(.48,.18,.045),.8)
TX=9.8; TY=2.4
cyl_between('Traveler legs',(TX,TY,.22),(TX,TY,.77),.10,.07,trav,'40 gameplay path',verts=8)
uvball('Traveler head',(TX,TY,1.27),(.115,.10,.145),trav,'40 gameplay path')
vs=[(TX-.10,TY,1.17),(TX+.12,TY,1.17),(TX+.28,TY,.51),(TX-.25,TY,.51),(TX,TY+.17,.73)]
mesh('Traveler tapered cloak',vs,[(0,1,2,3),(0,4,1),(1,4,2),(2,4,3),(3,4,0)],trav,'40 gameplay path')
mesh('Traveler wind scarf',[(TX,TY+.03,1.15),(TX+.65,TY+.03,1.1),(TX+.92,TY+.03,1.23),(TX+.49,TY+.03,1.04)],[(0,1,2,3)],scarf,'40 gameplay path')

# Wispy volume only; dense fog would flatten the photometric material relief.
fog=bpy.data.materials.new('Subtle cool river atmosphere'); fog.use_nodes=True; fog.node_tree.nodes.clear()
o=fog.node_tree.nodes.new('ShaderNodeOutputMaterial'); v=fog.node_tree.nodes.new('ShaderNodeVolumePrincipled'); v.inputs['Color'].default_value=(.49,.68,.71,1); v.inputs['Density'].default_value=.0026; v.inputs['Anisotropy'].default_value=.18; fog.node_tree.links.new(v.outputs['Volume'],o.inputs['Volume'])
cube('Air volume',(0,-13,9),(80,90,30),fog,'60 atmosphere')

# Real HDR sky lighting is supplemented with deliberate amber/cool art direction.
world=bpy.data.worlds.new('Belfast dusk / CC0 environment'); world.use_nodes=True; scene.world=world
n=world.node_tree.nodes; l=world.node_tree.links; n.clear(); out=n.new('ShaderNodeOutputWorld'); bg=n.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value=.22
tex=n.new('ShaderNodeTexEnvironment'); tex.image=bpy.data.images.load(str(ASSETS/'belfast_sunset_puresky_1k.hdr'),check_existing=True)
l.new(tex.outputs['Color'],bg.inputs['Color']); l.new(bg.outputs[0],out.inputs[0])
key=light('Amber dusk / raking key','AREA',(-6,8,13),(1,.49,.19),5200,8); key.rotation_euler=(Vector((-3,-3,7))-key.location).to_track_quat('-Z','Y').to_euler()
fill=light('Teal open-sky fill','AREA',(13,7,13),(.32,.62,.73),2600,13); fill.rotation_euler=(Vector((0,-3,6))-fill.location).to_track_quat('-Z','Y').to_euler()
back=light('Portal rear halo','AREA',(-3,-8,9),(1,.30,.07),4200,5); back.rotation_euler=(Vector((-3,1,8))-back.location).to_track_quat('-Z','Y').to_euler()
sun=light('Low warm sunset','SUN',(-10,-20,12),(1,.63,.34),1.2); sun.rotation_euler=(math.radians(78),math.radians(-20),math.radians(-135)); sun.data.angle=math.radians(9)
# Camera exactly side-on: X travel, Z vertical, camera looks in negative Y.
camdata=bpy.data.cameras.new('Side-on orthographic art camera'); cam=bpy.data.objects.new('Side-on orthographic art camera',camdata); COLS['70 lights'].objects.link(cam)
cam.location=(0,48,8.2); target=Vector((0,0,8.2)); cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler(); camdata.type='ORTHO'; camdata.ortho_scale=39; camdata.lens=50; scene.camera=cam
scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=1600; scene.render.resolution_y=900; scene.render.resolution_percentage=100
if hasattr(scene,'eevee'):
    if hasattr(scene.eevee,'taa_render_samples'): scene.eevee.taa_render_samples=128
    if hasattr(scene.eevee,'use_raytracing'): scene.eevee.use_raytracing=True
scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'; scene.render.film_transparent=False
scene.render.filepath=str(ROOT/'Enter_the_Ring_scene_study.png')
scene.view_settings.view_transform='AgX'; scene.view_settings.look='AgX - Medium High Contrast'; scene.view_settings.exposure=.2
scene.render.image_settings.color_depth='8'
# Gentle bloom only on actual emissive sources.
scene['project']='Samay Chakra / eight time-of-day worlds'
scene['realm']='01 Enter the Ring / 18:00-21:00 / Raga Yaman'
scene['scope']='Editable 2.5D art and level study, not a finished game'
scene['coordinates']='Camera views -Y, travel X, up Z; gameplay path is collection 40'
scene['asset_provenance']='Poly Haven CC0: Rabdentse Ruins Wall / Belfast Sunset Pure Sky. See assets/download-manifest.json.'
scene['geometry']='Original procedural geometry, no extracted GRIS assets'
scene['movement_notes']='Landing heights: 1.25m, 2.45m, 3.65m. Tune character double jump and gentle flight in engine; no controller supplied.'
# Set saved workspace opening directly in rendered camera framing.
for area in bpy.context.screen.areas if bpy.context.screen else []:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_perspective='CAMERA'; area.spaces.active.shading.type='MATERIAL'
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Enter_the_Ring_editable_scene_study.blend'))
summary={'version':bpy.app.version_string,'objects':len(bpy.data.objects),'collections':list(COLS),'resolution':[1600,900],'file':str(ROOT/'Enter_the_Ring_editable_scene_study.blend'),'render':scene.render.filepath,'camera':'orthographic, looks -Y','seed':8401}
(ROOT/'scene-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print('SCENE_READY='+json.dumps(summary),flush=True)
bpy.ops.render.render(write_still=True)
print('RENDER_COMPLETE',flush=True)

