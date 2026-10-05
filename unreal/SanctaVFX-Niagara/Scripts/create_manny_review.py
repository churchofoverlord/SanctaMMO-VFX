"""Create only the ignored local Manny fixture map. Existing viewer stays intact."""
import json, pathlib, unreal as u

R = pathlib.Path(u.Paths.project_dir())
exec(compile((R / 'Scripts/discover_manny_editor.py').read_text(encoding='utf-8').replace('u.SystemLibrary.quit_editor()', ''), 'discovery', 'exec'))
A = u.get_editor_subsystem(u.EditorActorSubsystem)
path = '/Game/Sancta/VFX/MannyLab/L_MannyReview'
if u.EditorAssetLibrary.does_asset_exist(path):
    world = u.EditorLoadingAndSavingUtils.load_map(path)
    if not world:
        raise RuntimeError('Manny map did not load')
    for actor in A.get_all_level_actors():
        A.destroy_actor(actor)
else:
    world = u.EditorLoadingAndSavingUtils.new_blank_map(False)
    if not world:
        raise RuntimeError('Manny map creation failed')
stage = A.spawn_actor_from_class(u.SanctaVFXMannyReview, u.Vector())
stage.set_editor_property('cases_json', (R / 'Evidence/gameplay-manny-cases.json').read_text(encoding='utf-8'))
native = json.loads((R / 'Evidence/gameplay-runtime-native-assets.json').read_text(encoding='utf-8-sig'))
stage.set_editor_property('system', u.load_asset(native['assets']['ContactPhysical']['asset']))
floor = A.spawn_actor_from_class(u.StaticMeshActor, u.Vector(0, 0, -3))
floor.static_mesh_component.set_static_mesh(u.load_asset('/Engine/BasicShapes/Plane'))
floor.set_actor_scale3d(u.Vector(30, 30, 1))
floor.static_mesh_component.set_material(0, u.load_asset('/Game/VFXLab/Review/Fixtures/M_ReviewFloor'))
light = A.spawn_actor_from_class(u.DirectionalLight, u.Vector(0, 0, 500), u.Rotator(pitch=-45, yaw=-40, roll=0))
light.light_component.set_editor_property('intensity', 4.0)
if not u.EditorLoadingAndSavingUtils.save_map(world, path):
    raise RuntimeError('Manny map save failed')
u.log('Manny calibration map saved')
u.SystemLibrary.quit_editor()
