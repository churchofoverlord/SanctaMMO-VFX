# SanctaMMO VFX isolated sandbox

- Project: `SanctaMMO_VFXSandbox.uproject`
- Engine: Unreal Engine 5.8.2 at `C:\UE582`
- Purpose: local VFX design and Niagara prototyping only.
- Plugins: Niagara, Editor Python, Editor Scripting Utilities.
- No SanctaMMO gameplay module, project plugin, ControlState dependency, main-project content, or runtime gameplay bindings are included.
- The editor startup map is `/Game/VFX/L_VFX_PrototypePreview`; it contains four labelled Niagara actor previews.
- Preview-only values and triggers must be tagged `LOOKDEV_ONLY — NOT GAMEPLAY AUTHORITY`.
- `VFX-SKILL-002` remains deferred; do not create a gameplay warning/telegraph.

Assets authored here are prototype evidence only, not integrated or formally accepted. Keep only project source/config/content/scripts in Git. `Binaries`, `DerivedDataCache`, `Intermediate`, and `Saved` are disposable local outputs.
