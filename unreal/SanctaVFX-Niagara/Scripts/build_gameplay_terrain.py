import unreal as u,pathlib,json
R=pathlib.Path(u.Paths.project_dir());exec(compile((R/'Scripts/build_reference_ports.py').read_text(encoding='utf-8').split('\ntry:\n for item')[0],'helpers','exec'))
mesh=import_file('Source/GameplayRuntime/IcebergBody.obj','/Game/Sancta/VFX/Terrain/Iceberg','SM_IcebergBody',True)
vertices=[u.Vector(*map(float,line.split()[1:])) for line in (R/'Source/GameplayRuntime/IcebergBody.obj').read_text().splitlines() if line.startswith('v ')]
if not LAB.configure_terrain_mesh(mesh,vertices):raise RuntimeError('Iceberg collision creation failed')
save(mesh)
path='/Game/Sancta/VFX/Terrain/Iceberg/M_IcebergBody';m=u.load_asset(path)
if not m:
 m=tools.create_asset('M_IcebergBody','/Game/Sancta/VFX/Terrain/Iceberg',u.Material,u.MaterialFactoryNew())
 pos=expression(m,u.MaterialExpressionWorldPosition);normal=expression(m,u.MaterialExpressionPixelNormalWS)
 integrity=expression(m,u.MaterialExpressionScalarParameter,{'parameter_name':'TerrainIntegrity','default_value':1.})
 code='float3 p=P*.021;float fissure=pow(saturate(1-abs(sin(p.x+sin(p.z*.6)*.8))*18),3)*pow(saturate(sin(p.y*1.7)),8);float frost=saturate(N.z)*.09;return lerp(float3(.055,.15,.23),float3(.14,.28,.35),frost)+fissure*.024*(2-Integrity);'
 c=custom(m,code,u.CustomMaterialOutputType.CMOT_FLOAT3,{'P':(pos,''),'N':(normal,''),'Integrity':(integrity,'')})
 lib.connect_material_property(c,'',u.MaterialProperty.MP_BASE_COLOR)
 rough=expression(m,u.MaterialExpressionConstant,{'r':.32});lib.connect_material_property(rough,'',u.MaterialProperty.MP_ROUGHNESS)
 lib.recompile_material(m);save(m)
valid=json.loads(LAB.validate_terrain(mesh,m,world))
(R/'Evidence/gameplay-runtime-terrain-validation.json').write_text(json.dumps({'mesh':mesh.get_path_name(),'material':m.get_path_name(),'validation':valid,'visual_review':'pending','foundation_modified':False},indent=2),encoding='utf-8')
if not valid['passed']:raise RuntimeError(str(valid))
u.SystemLibrary.quit_editor()
