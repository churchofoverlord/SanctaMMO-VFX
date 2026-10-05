import unreal as u,json,pathlib,os
R=pathlib.Path(u.Paths.project_dir());L=u.get_editor_subsystem(u.LevelEditorSubsystem);A=u.get_editor_subsystem(u.EditorActorSubsystem)
exec(compile((R/'Scripts/prepare_review_stage.py').read_text(encoding='utf-8'),'fixtures','exec'))
interactive=os.environ.get('SANCTA_RUNTIME_VIEWER')=='1'
map_path='/Game/Sancta/VFX/Review/L_RuntimeViewer' if interactive else '/Game/Sancta/VFX/Review/L_RuntimeAudit'
map_path=os.environ.get('SANCTA_RUNTIME_REVIEW_MAP',map_path)
if u.EditorAssetLibrary.does_asset_exist(map_path):
 if not L.load_level(map_path):raise RuntimeError('Runtime review map could not load')
 for actor in A.get_all_level_actors():
  if isinstance(actor,(u.SanctaVFXReviewActor,u.StaticMeshActor,u.DirectionalLight)):A.destroy_actor(actor)
elif not L.new_level(map_path):raise RuntimeError('Runtime review map creation failed')
case_file=os.environ.get('SANCTA_RUNTIME_CASE_FILE','Evidence/runtime-viewer-cases.json' if interactive else 'Evidence/runtime-review-cases.json')
cases=json.loads((R/case_file).read_text(encoding='utf-8'))
stage=A.spawn_actor_from_class(u.SanctaVFXRuntimeReview,u.Vector())
stage.set_editor_property('bInteractive',interactive)
stage.set_editor_property('cases_json',json.dumps(cases));stage.set_editor_property('system',u.load_asset(json.loads((R/'Evidence/gameplay-runtime-native-assets.json').read_text(encoding='utf-8'))['assets']['ContactPhysical']['asset']))
stage.set_editor_property('camera_position',u.Vector(230,-480,270));stage.set_editor_property('camera_target',u.Vector(0,0,100))
floor=A.spawn_actor_from_class(u.StaticMeshActor,u.Vector(0,0,-3));floor.static_mesh_component.set_static_mesh(u.load_asset('/Engine/BasicShapes/Plane'));floor.set_actor_scale3d(u.Vector(100,100,1));floor.static_mesh_component.set_material(0,floor_material)
floor.set_editor_property('tags',['RuntimeFloor'])
path='/Game/Sancta/VFX/Review/Common/M_RuntimeFloorBright'
if not u.EditorAssetLibrary.does_asset_exist(path):
 bright=tools.create_asset('M_RuntimeFloorBright','/Game/Sancta/VFX/Review/Common',u.Material,u.MaterialFactoryNew());bright.set_editor_property('shading_model',u.MaterialShadingModel.MSM_UNLIT)
 node=lib.create_material_expression(bright,u.MaterialExpressionConstant3Vector,0,0);node.set_editor_property('constant',u.LinearColor(.62,.66,.71,1));lib.connect_material_property(node,'',u.MaterialProperty.MP_EMISSIVE_COLOR);lib.recompile_material(bright)
 if not u.EditorAssetLibrary.save_loaded_asset(bright):raise RuntimeError('Bright review fixture not saved')
light=A.spawn_actor_from_class(u.DirectionalLight,u.Vector(0,0,500),u.Rotator(-50,-30,0));light.light_component.set_editor_property('intensity',3.)
body=A.spawn_actor_from_class(u.StaticMeshActor,u.Vector());body.static_mesh_component.set_static_mesh(review_body);body.static_mesh_component.set_material(0,body_material)
if not L.save_current_level():raise RuntimeError('Runtime review map save failed')
u.SystemLibrary.quit_editor()
