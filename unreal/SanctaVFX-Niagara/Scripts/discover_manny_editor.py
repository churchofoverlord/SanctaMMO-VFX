"""Inspect copied assets in the lab, not in the original game's editor."""
import datetime, json, pathlib, unreal as u

R = pathlib.Path(u.Paths.project_dir())
mesh = u.load_asset('/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple')
if not mesh:
    raise RuntimeError('Local Manny did not load')
actors = u.get_editor_subsystem(u.EditorActorSubsystem)
actor = actors.spawn_actor_from_class(u.SkeletalMeshActor, u.Vector(0, 0, 0))
c = actor.skeletal_mesh_component
c.set_skeletal_mesh_asset(mesh)
# Here the mesh itself is the actor root. Put it at feet level; the live fixture
# uses a separate root at +96 and a child mesh at -96, matching the game's code.
c.set_relative_location(u.Vector(0, 0, 0), False, False)
c.set_relative_rotation(u.Rotator(pitch=0, yaw=-90, roll=0), False, False)
bones = [str(c.get_bone_name(i)) for i in range(c.get_num_bones())]
required = ['root', 'pelvis', 'spine_03', 'head', 'hand_l', 'hand_r', 'lowerarm_l', 'lowerarm_r', 'foot_l', 'foot_r']
missing = [name for name in required if not c.does_socket_exist(name)]
positions = {name: {'world': {'x': c.get_socket_location(name).x, 'y': c.get_socket_location(name).y,
                              'z': c.get_socket_location(name).z}} for name in required if name not in missing}
registry = u.AssetRegistryHelpers.get_asset_registry()
options = u.AssetRegistryDependencyOptions(include_soft_package_references=True,
                                           include_hard_package_references=True)
roots = ['/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple',
         '/Game/Characters/Mannequins/Anims/Unarmed/MM_Idle',
         '/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_01',
         '/Game/Characters/Mannequins/Anims/Unarmed/Jog/MF_Unarmed_Jog_Fwd',
         '/Game/Characters/Mannequins/Anims/Unarmed/Jump/MM_Dash']
animations = []
for path in roots[1:]:
    asset = u.load_asset(path)
    if not asset:
        raise RuntimeError('Animation missing: ' + path)
    animations.append({'asset': path, 'class': asset.get_class().get_name(),
                       'seconds': float(asset.get_editor_property('sequence_length'))})
pending = list(roots); dependencies = set()
while pending:
    path = pending.pop()
    if path in dependencies:
        continue
    dependencies.add(path)
    pending.extend(str(p) for p in registry.get_dependencies(path, options)
                   if str(p).startswith('/Game/Characters/Mannequins/'))
external = sorted({str(p) for path in dependencies for p in registry.get_dependencies(path, options)
                   if not str(p).startswith(('/Game/Characters/Mannequins/', '/Script/', '/Engine/'))})
unresolved = [path for path in external if not u.load_asset(path)]
report = {'generated_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'mesh': mesh.get_path_name(), 'skeleton': mesh.get_editor_property('skeleton').get_path_name(),
          'bones': bones, 'socket_or_bone_names': [str(x) for x in c.get_all_socket_names()],
          'required_missing': missing, 'reference_pose_world': positions,
          'animations': animations, 'dependencies': sorted(dependencies), 'external_dependencies': external,
          'actor_origin_cm': [0, 0, 96], 'mesh_relative_cm': [0, 0, -96], 'mesh_yaw_degrees': -90,
          'unresolved_dependencies': unresolved,
          'passed': not missing and not unresolved, 'scope': 'Reference-pose discovery only, not live animation calibration'}
(R / 'Evidence/gameplay-manny-discovery.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
actors.destroy_actor(actor)
if not report['passed']:
    raise RuntimeError(str(report))
u.log('Manny discovery: %d bones; %d dependency packages' % (len(bones), len(dependencies)))
u.SystemLibrary.quit_editor()
