import unreal
from pathlib import Path

expected = {
    "LOOKDEV_ONLY__VFX-COMBAT-001": "/Game/VFX/Combat/NS_VFX_COMBAT_001_BasicHit",
    "LOOKDEV_ONLY__VFX-SKILL-001": "/Game/VFX/Skills/NS_VFX_SKILL_001_ProjectileTrail",
    "LOOKDEV_ONLY__VFX-CHARACTER-001": "/Game/VFX/Character/NS_VFX_CHARACTER_001_Slow",
    "LOOKDEV_ONLY__VFX-INTERACT-001": "/Game/VFX/Interaction/NS_VFX_INTERACT_001_Result",
}
lines = [f"Engine: {unreal.SystemLibrary.get_engine_version()}", "Project: SanctaMMO_VFXSandbox"]
for label, asset_path in expected.items():
    asset = unreal.EditorAssetLibrary.load_asset(asset_path)
    if not asset or asset.get_class().get_name() != "NiagaraSystem":
        raise RuntimeError(f"NiagaraSystem did not load: {asset_path}")
    lines.append(f"LOADABLE | NiagaraSystem | {asset_path}")
level_path = "/Game/VFX/L_VFX_PrototypePreview"
if not unreal.EditorAssetLibrary.load_asset(level_path):
    raise RuntimeError(f"Preview map asset did not load: {level_path}")
if not unreal.EditorLevelLibrary.load_level(level_path):
    raise RuntimeError(f"Could not open preview map: {level_path}")
actors = unreal.EditorLevelLibrary.get_all_level_actors()
found = {}
for actor in actors:
    label = actor.get_actor_label()
    if label in expected:
        component = actor.get_component_by_class(unreal.NiagaraComponent)
        if not component:
            raise RuntimeError(f"Preview actor has no NiagaraComponent: {label}")
        system = component.get_asset()
        if not system or system.get_path_name().split(".")[0] != expected[label]:
            raise RuntimeError(f"Wrong Niagara system assigned to {label}")
        found[label] = expected[label]
if set(found) != set(expected):
    raise RuntimeError(f"Preview map actor labels differ: {sorted(found)}")
lines.append(f"MAP_LOADABLE | {level_path} | NiagaraActors={len(found)}")
lines.extend(f"ACTOR | {label} -> {asset_path}" for label, asset_path in found.items())
result = "\n".join(lines)
out = Path(unreal.Paths.project_saved_dir()) / "Logs" / "VFX_Prototype_Validation.txt"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(result, encoding="utf-8")
unreal.log(result.replace("\n", " | "))
