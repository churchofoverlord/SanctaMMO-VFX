# Niagara asset and preview map loadability — UE 5.8.2

Status: `TECHNICALLY_PROVEN` for project opening, Niagara system asset loadability, preview map loadability, and actor-to-asset references only.

- Project: `UEVFXSandbox/SanctaMMO_VFXSandbox.uproject`
- Engine build: `5.8.2-0+UE5` from `C:\UE582`
- Observed: 2026-09-23, using the isolated Unreal Editor command-line Python runtime.
- Validation script: `UEVFXSandbox/Scripts/validate_prototype_assets.py`
- Raw local log: `UEVFXSandbox/Saved/Logs/VFX_Prototype_Validation.txt` (generated, ignored by Git).
- Preview map: `/Game/VFX/L_VFX_PrototypePreview` (`UEVFXSandbox/Content/VFX/L_VFX_PrototypePreview.umap`).

| Asset path | Loaded class | Source template |
|---|---|---|
| `/Game/VFX/Combat/NS_VFX_COMBAT_001_BasicHit` | `NiagaraSystem` | `/Niagara/DefaultAssets/Templates/Systems/RadialBurst` |
| `/Game/VFX/Skills/NS_VFX_SKILL_001_ProjectileTrail` | `NiagaraSystem` | `/Niagara/DefaultAssets/Templates/Systems/AttributeReaderTrails` |
| `/Game/VFX/Character/NS_VFX_CHARACTER_001_Slow` | `NiagaraSystem` | `/Niagara/DefaultAssets/Templates/Systems/MinimalLightweight` |
| `/Game/VFX/Interaction/NS_VFX_INTERACT_001_Result` | `NiagaraSystem` | `/Niagara/DefaultAssets/Templates/Systems/DirectionalBurstLightweight` |

The preview map reopens and contains four Niagara actors, each assigned the matching system and labelled `LOOKDEV_ONLY__<VFX_ID>`. The editor script loaded each object, confirmed its class, and checked the level actor labels and asset references. It did not author/compile a custom Niagara graph, render or visually inspect the effect, bind gameplay events/state, profile cost, or verify multiplayer behavior. The systems remain stock-template derivatives and have not passed visual, technical, performance, or formal acceptance review.
