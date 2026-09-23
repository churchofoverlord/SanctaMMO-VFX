import unreal
from pathlib import Path

# First-pass technical scaffolds copied from Epic's UE 5.8.2 Niagara examples.
# These are intentionally not gameplay-bound or formally accepted.
plans = [
    ("/Niagara/DefaultAssets/Templates/Systems/RadialBurst", "/Game/VFX/Combat/NS_VFX_COMBAT_001_BasicHit"),
    ("/Niagara/DefaultAssets/Templates/Systems/AttributeReaderTrails", "/Game/VFX/Skills/NS_VFX_SKILL_001_ProjectileTrail"),
    ("/Niagara/DefaultAssets/Templates/Systems/MinimalLightweight", "/Game/VFX/Character/NS_VFX_CHARACTER_001_Slow"),
    ("/Niagara/DefaultAssets/Templates/Systems/DirectionalBurstLightweight", "/Game/VFX/Interaction/NS_VFX_INTERACT_001_Result"),
]
log_path = Path(unreal.Paths.project_saved_dir()) / "Logs" / "VFX_System_Prototype_Import.txt"
log_path.parent.mkdir(parents=True, exist_ok=True)
results = []
for source, destination in plans:
    if unreal.EditorAssetLibrary.does_asset_exist(destination):
        raise RuntimeError(f"Refusing to overwrite existing prototype: {destination}")
    directory = destination.rsplit("/", 1)[0]
    if not unreal.EditorAssetLibrary.does_directory_exist(directory):
        unreal.EditorAssetLibrary.make_directory(directory)
    template = unreal.EditorAssetLibrary.load_asset(source)
    if not template:
        raise RuntimeError(f"Epic Niagara source template not found: {source}")
    created = unreal.EditorAssetLibrary.duplicate_asset(source, destination)
    if not created:
        raise RuntimeError(f"Could not duplicate source template {source} to {destination}")
    if not unreal.EditorAssetLibrary.save_loaded_asset(created, False):
        raise RuntimeError(f"Could not save prototype asset: {destination}")
    results.append(f"{destination} | class={created.get_class().get_name()} | source={source}")
log_path.write_text("\n".join(results), encoding="utf-8")
unreal.log(f"Created {len(results)} isolated Niagara template prototypes; see {log_path}")
