import unreal
from pathlib import Path

level_path = "/Game/VFX/L_VFX_PrototypePreview"
items = [
    ("/Game/VFX/Combat/NS_VFX_COMBAT_001_BasicHit", "LOOKDEV_ONLY__VFX-COMBAT-001", (-600, 0, 100)),
    ("/Game/VFX/Skills/NS_VFX_SKILL_001_ProjectileTrail", "LOOKDEV_ONLY__VFX-SKILL-001", (-200, 0, 100)),
    ("/Game/VFX/Character/NS_VFX_CHARACTER_001_Slow", "LOOKDEV_ONLY__VFX-CHARACTER-001", (200, 0, 100)),
    ("/Game/VFX/Interaction/NS_VFX_INTERACT_001_Result", "LOOKDEV_ONLY__VFX-INTERACT-001", (600, 0, 100)),
]
if unreal.EditorAssetLibrary.does_asset_exist(level_path):
    raise RuntimeError(f"Refusing to overwrite preview level: {level_path}")
if not unreal.EditorLevelLibrary.new_level(level_path):
    raise RuntimeError(f"Could not create preview level: {level_path}")
results = []
for system_path, label, position in items:
    system = unreal.EditorAssetLibrary.load_asset(system_path)
    if not system:
        raise RuntimeError(f"Niagara system missing: {system_path}")
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.NiagaraActor,
        unreal.Vector(*position),
        unreal.Rotator(0.0, 0.0, 0.0),
    )
    if not actor:
        raise RuntimeError(f"Could not spawn local preview actor: {label}")
    actor.set_actor_label(label)
    component = actor.get_component_by_class(unreal.NiagaraComponent)
    if not component:
        raise RuntimeError(f"NiagaraActor has no NiagaraComponent: {label}")
    component.set_asset(system)
    component.activate(True)
    results.append(f"{label} -> {system_path}")
if not unreal.EditorLevelLibrary.save_current_level():
    raise RuntimeError(f"Could not save preview level: {level_path}")
out = Path(unreal.Paths.project_saved_dir()) / "Logs" / "VFX_Preview_Stage.txt"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join([f"LEVEL {level_path}"] + results), encoding="utf-8")
unreal.log(f"Saved isolated VFX preview stage {level_path} with {len(results)} tagged Niagara actors")
