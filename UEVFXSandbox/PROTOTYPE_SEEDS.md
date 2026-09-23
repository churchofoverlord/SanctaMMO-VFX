# Initial Niagara prototype seeds

Status: four local `NiagaraSystem` assets and one side-by-side preview map were created in the isolated project on UE 5.8.2. The systems are engine-template derivatives; their Niagara graphs remain stock and have not been adapted to SanctaMMO gameplay events or to the final silhouettes in the visual blockout.

Project: `C:\Dev\SanctaMMO-VFX\UEVFXSandbox\SanctaMMO_VFXSandbox.uproject`
Engine: `C:\UE582` — `5.8.2-0+UE5`
Preview map: `/Game/VFX/L_VFX_PrototypePreview` — four NiagaraActors labelled `LOOKDEV_ONLY__<VFX_ID>`.
Design basis: `VFX_DESIGN_VSLICE_001_V1`

| VFX_ID | Sandbox asset | UE 5.8.2 source template | Prototype limit |
|---|---|---|---|
| VFX-COMBAT-001 | `/Game/VFX/Combat/NS_VFX_COMBAT_001_BasicHit` | `/Niagara/DefaultAssets/Templates/Systems/RadialBurst` | Stock radial burst. No successful-hit event binding; no damage/severity mapping; radial rim silhouette not authored yet. |
| VFX-SKILL-001 | `/Game/VFX/Skills/NS_VFX_SKILL_001_ProjectileTrail` | `/Niagara/DefaultAssets/Templates/Systems/AttributeReaderTrails` | Stock trail example. It is not bound to the Sancta projectile actor or its replicated transforms. |
| VFX-CHARACTER-001 | `/Game/VFX/Character/NS_VFX_CHARACTER_001_Slow` | `/Niagara/DefaultAssets/Templates/Systems/MinimalLightweight` | Stock lightweight example. It has no `StateActive` binding and does not represent Slow lifecycle. |
| VFX-INTERACT-001 | `/Game/VFX/Interaction/NS_VFX_INTERACT_001_Result` | `/Niagara/DefaultAssets/Templates/Systems/DirectionalBurstLightweight` | Stock one-shot result accent. No request correlation, station bracket, Pending/Accepted/Rejected/Unknown selection, progress, or completion. |

The assets were loaded from the engine plugin as `NiagaraSystem` objects, duplicated into `/Game/VFX/...`, and saved. `Scripts/validate_prototype_assets.py` checks each system, opens the preview map, and confirms the expected tagged actors and asset references. The observed output is summarized in [EVIDENCE/ASSET_LOADABILITY_UE582.md](EVIDENCE/ASSET_LOADABILITY_UE582.md). This proves asset/map creation and loadability in the selected engine, not visual fidelity, exact Niagara compilation, performance, runtime binding, multiplayer behavior, acceptance, or integration.

All prototypes remain local visual scaffolds. Values, triggers, transform inputs, and state cues are `LOOKDEV_ONLY — NOT GAMEPLAY AUTHORITY`. `VFX-SKILL-002` remains source-deferred and has no Niagara asset.

## Next bounded work

1. Inspect each template-derived system in the Niagara editor.
2. Replace or adapt stock modules only where the approved VFX brief describes the behavior; add no gameplay simulation or duplicated gameplay constants.
3. Build the event, actor-transform, state, and owner-result preview harnesses from local stand-ins, explicitly labelled `LOOKDEV_ONLY`.
4. Review screenshots and all four scalability tiers before claiming visual readability.
5. Keep Slow's runtime lifecycle, Basic Attack's exact-SHA cue validation, and projectile multiplayer observation open. Do not infer them from local preview.
