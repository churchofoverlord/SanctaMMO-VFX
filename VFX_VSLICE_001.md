# VFX_VSLICE_001 — Source binding and production briefs

Status: ISOLATED UE SANDBOX CREATED; FOUR NIAGARA TEMPLATE SEEDS SAVED AND RELOADABLE; VISUAL/GRAPH REVIEW OPEN. No gameplay bindings or Unreal main-project integration have occurred.

## Purpose

Validate a small cross-section of the proposed VFX patterns: event confirmation, motion, spatial warning, persistent state, and interaction feedback. Each item remains presentation work and does not redefine a skill, status, gathering rule, or gameplay contract.

Local previews may use explicit preview-only controls for composition. Preview values are not gameplay defaults.

## Current items

| VFX_ID | Pattern | Source status | Current conclusion | Dependencies |
|---|---|---|---|---|
| VFX-COMBAT-001 | Direct/melee impact | SOURCE_BOUND | Basic Attack hit path is bound; current client cue is location-only and the inspected NPC path is narrower than a universal hit event. | No damage-magnitude intensity; contact point/normal are not supplied. |
| VFX-SKILL-001 | Projectile/travel | SOURCE_BOUND | Server-owned projectile actor and replicated transform provide a path-following source. | Runtime behavior at the pinned current source SHA still needs exact-SHA validation; skill and receiver identity are server-side. |
| VFX-SKILL-002 | Area warning/telegraph | SOURCE_DEFERRED | Ground-area execution provides an impact footprint, not a pre-impact warning lifecycle. | DEFERRED_GAMEPLAY_INPUT; do not invent a warning window or duplicate dimensions. |
| VFX-CHARACTER-001 | Persistent state | SOURCE_BOUND | A real Slow status has server-side identity and lifecycle, but its active state is not replicated for a persistent client visual. | Bounded status presentation hook; CF-VFX-0002. |
| VFX-INTERACT-001 | Interaction feedback | SOURCE_BOUND | Manual processing request and owner result are real; the production order remains Queued and has no progress/completion lifecycle in this source. | Retain request target locally to attach the owner result to its station. |

## Source provenance

The source repository identity is SanctaMMO-Foundation-5.8. Its local read-only checkout was C:\Dev\SanctaMMO-SKILL-001, clean at inspection, with HEAD b5cf12a64ffd971b195c0d6406d6ed1c93326916. The checkout branch was 70 commits ahead of its configured upstream. Every binding below pins an exact commit; this note does not claim that the local branch is shared, formally accepted, or canonical.

For this gate, SOURCE_STABLE means the referenced exact commit exists in a clean local source checkout. TECHNICALLY_PROVEN is claimed only for behavior with runtime evidence at the separately listed evidence SHA. FORMALLY_ACCEPTED and CANONICAL are separate statuses; none of these VFX bindings is either.

The VFX workspace was clean and synchronized to Foundation baseline 15ff5728d203e3dd2c8df6d086bdd60fb472a716 before work. The source-binding commit SHA is reported in the delivery record rather than self-referenced here.

## Source binding results

| VFX_ID | Semantic source | Source revision | Status | Brief |
|---|---|---|---|---|
| VFX-COMBAT-001 | Phase2.BasicAttack.IFV / CombatPlay.BasicAttack.IFV | b5cf12a64ffd971b195c0d6406d6ed1c93326916 | SOURCE_BOUND; Phase 2F attack path was runtime-proven at 61a02eada2632fce7a03f512fb9004ac91b5d9d6; current cue path is code-observed only. | [VFX-COMBAT-001](briefs/VFX-COMBAT-001.md) |
| VFX-SKILL-001 | scout.torpor / ASanctaGameplayProjectile | b5cf12a64ffd971b195c0d6406d6ed1c93326916 | SOURCE_BOUND; replicated movement is code-observed at the pinned SHA; no exact-SHA runtime evidence was found. | [VFX-SKILL-001](briefs/VFX-SKILL-001.md) |
| VFX-SKILL-002 | Candidate only: Phase2.GroundArea.IFV and fighter.crushing_1 | b5cf12a64ffd971b195c0d6406d6ed1c93326916 | SOURCE_DEFERRED; area execution is distinct from telegraphing. | [VFX-SKILL-002](briefs/VFX-SKILL-002.md) |
| VFX-CHARACTER-001 | scout.torpor / ESanctaCoreEffectType::Slow | b5cf12a64ffd971b195c0d6406d6ed1c93326916 | SOURCE_BOUND; live server lifecycle is code-observed at the pinned SHA; the deterministic model contract was proven at bb3f39b3e2cf043cf695a73b342a0834519db86d. | [VFX-CHARACTER-001](briefs/VFX-CHARACTER-001.md) |
| VFX-INTERACT-001 | Phase3P manual processing / Station.Tailoring.HideProcessing | 2cd9457349379106516b9785f0a19230a85c6342 | SOURCE_BOUND; owning-client request/result was runtime-proven at this exact SHA. | [VFX-INTERACT-001](briefs/VFX-INTERACT-001.md) |

## Runtime parameter contract

| Parameter | Classification | Evidence and boundary |
|---|---|---|
| BasicAttackId, source/receiver identity, authoritative hit result | AVAILABLE_NOW | Present in the server-side combat request/outcome path. The replicated short-lived cue does not carry the complete identity event. |
| ImpactTransform | AVAILABLE_NOW, bounded | The damage cue replicates a world location for the inspected non-player receiver path. It is an actor-relative cue position, not a measured contact point. |
| SurfaceNormal and contact point | MISSING_PRESENTATION_HOOK | Neither is supplied by the selected Basic Attack result path. |
| ProjectileTransform and active travel | AVAILABLE_NOW | ASanctaGameplayProjectile replicates movement. VFX follows that actor; it does not own trajectory, collision, hit, or speed. |
| Projectile skill identity and receiver identity on observing clients | MISSING_PRESENTATION_HOOK | BoundSkillId and BoundReceiver are server-side fields, not replicated presentation data. A generic trail does not need to invent them. |
| Ground-area center and radius at resolution | AVAILABLE_NOW, bounded | The selected area source passes its runtime center/radius to resolution and its impact cue. This does not supply a pre-impact window. |
| Telegraph start, active deadline, and termination | MISSING_PRESENTATION_HOOK | No selected player ability exposes an authoritative telegraph lifecycle with its footprint. |
| Status identity, affected actor, active lifecycle, expiry | AVAILABLE_NOW on server | The authoritative status set owns these values and removes expired/cleared states. |
| Replicated StateActive for persistent VFX | MISSING_PRESENTATION_HOOK | The status set is not replicated; the short application cue is not a status lifecycle contract. |
| Processing station identity/location and owner request result | AVAILABLE_NOW | Station identity/transform replicate; the requester receives Pending, Accepted, or rejection feedback correlated by a local sequence. |
| Processing progress or completion | Not present in selected source | The accepted order remains Queued. Do not imply production progress or completion. |
| Gameplay-semantic change | REQUIRES_GAMEPLAY_CHANGE: NONE | Findings request only bounded presentation access to existing authoritative state, if needed. They do not request new timing, shape, range, damage, or interaction rules. |

## Niagara architecture validation

At the source-binding gate commit, no Niagara System, material, Unreal Content, C++, or Blueprint had been created or modified. The later isolated prototype phase is recorded below.

| Shared pattern | Classification | Source-based reason |
|---|---|---|
| Spawn and initialize | PROVEN_USEFUL | Impact and area cues use explicit location, orientation, and event parameters. |
| Short burst | PROVEN_USEFUL | Basic hit and area-impact cues are discrete events with cleanup. Their cue lifespan is presentation-only and must not be treated as gameplay duration. |
| Trail/ribbon | LIKELY_USEFUL | A real server-owned projectile exposes a replicated transform stream; no exact-SHA runtime/profile evidence supports a final trail implementation yet. |
| Telegraph | TOO_EARLY_TO_GENERALIZE | The bound area evidence is resolution-only; no selected source supplies the complete warning lifecycle. |
| Persistent state | LIKELY_USEFUL | A real authoritative Slow state exists, while client replication needed to drive it is absent. |
| Ambient loop | NOT_NEEDED | No ambient source is part of this slice. |
| Render/material controls | TOO_EARLY_TO_GENERALIZE | Current placeholder cues do not demonstrate two production uses or measured shared-material benefit. |

No architecture revision is justified by this evidence.

## Cross-project findings

- CF-VFX-0001: VFX-SKILL-002 lacks an authoritative pre-impact warning lifecycle; BLOCKING_IMPLEMENTATION, NON_BLOCKING_LOOKDEV.
- CF-VFX-0002: VFX-CHARACTER-001 lacks client-visible active/inactive status state; BLOCKING_IMPLEMENTATION, NON_BLOCKING_LOOKDEV.

The detailed handoffs are in [CROSS_PROJECT_FINDINGS.md](CROSS_PROJECT_FINDINGS.md). No Owner decision is required for these bounded presentation hooks.

## Readiness

| VFX_ID | Readiness |
|---|---|
| VFX-COMBAT-001 | LOOKDEV_BLOCKOUT_CREATED; READABILITY_REVIEW_OPEN; runtime cue still requires exact-SHA validation before implementation. |
| VFX-SKILL-001 | LOOKDEV_BLOCKOUT_CREATED; READABILITY_REVIEW_OPEN; exact-SHA multiplayer path observation remains open before implementation. |
| VFX-SKILL-002 | READY_FOR_LOCAL_LOOKDEV; DEFERRED_GAMEPLAY_INPUT. |
| VFX-CHARACTER-001 | LOOKDEV_BLOCKOUT_CREATED; READABILITY_REVIEW_OPEN; persistent client visual remains deferred until an authoritative state hook exists. |
| VFX-INTERACT-001 | LOOKDEV_BLOCKOUT_CREATED; READABILITY_REVIEW_OPEN; future implementation is limited to request/result feedback. |

VFX_VSLICE_001_IMPLEMENTATION_READINESS = PARTIAL

SOURCE_BOUND_COUNT = 4
SOURCE_DEFERRED_COUNT = 1
REQUIRES_GAMEPLAY_CHANGE_COUNT = 0
OTHER_PROJECTS_MODIFIED = NO
UNREAL_MAIN_PROJECT_MODIFIED = NO
GAMEPLAY_SEMANTICS_MODIFIED = NO
CANON_MODIFIED = NO
CONTROLSTATE_REQUIRED_FOR_THIS_GATE = NO
OWNER_DECISION_REQUIRED = NO
NEXT_GATE = VFX_VSLICE_001_TEMPLATE_ADAPTATION_AND_READABILITY
STOP_REASON = Four template-derived systems load in the isolated project; their graphs and visual fidelity have not been adapted or reviewed. Unreal main-project integration remains out of scope.

## Isolated design gate

Four `SOURCE_BOUND` items now have concrete silhouette, motion, runtime-binding, architecture, scalability, and review criteria for local prototyping. VFX-SKILL-002 remains `SOURCE_DEFERRED` and is limited to non-semantic shape exploration.

The shared technical specification is [VFX_VSLICE_001_DESIGN_SPEC_V1.md](VFX_VSLICE_001_DESIGN_SPEC_V1.md). It records proposed effect systems and parameters, all conceptual scalability tiers, future readability/performance evidence, unresolved inputs, and the UE sandbox check. The individual briefs contain the item-specific design intent and source boundaries.

`UE_VFX_SANDBOX = CREATED`: the content-only project [UEVFXSandbox/SanctaMMO_VFXSandbox.uproject](UEVFXSandbox/SanctaMMO_VFXSandbox.uproject) is associated with UE 5.8.2 at `C:\UE582`. It contains four saved stock-template Niagara systems; exact source assets and limitations are listed in [UEVFXSandbox/PROTOTYPE_SEEDS.md](UEVFXSandbox/PROTOTYPE_SEEDS.md). The editor startup map is the preview stage `/Game/VFX/L_VFX_PrototypePreview`, with four `LOOKDEV_ONLY` actors; asset and actor references are recorded in [UEVFXSandbox/EVIDENCE/ASSET_LOADABILITY_UE582.md](UEVFXSandbox/EVIDENCE/ASSET_LOADABILITY_UE582.md). The standalone design preview remains at [lookdev/VFX_VSLICE_001_LOOKDEV_V1.html](lookdev/VFX_VSLICE_001_LOOKDEV_V1.html). No source gameplay project or main Unreal project was opened or modified.

```text
VFX_DESIGN_REVISION = VFX_DESIGN_VSLICE_001_V1
VFX_VSLICE_001_DESIGN_READINESS = PROTOTYPE_READY
VFX_VSLICE_001_TECHNICAL_PROTOTYPE = CREATED; TEMPLATE_DERIVATIVE; VISUAL_AND_GRAPH_REVIEW = OPEN
VFX_VSLICE_001_VECTOR_LOOKDEV = CREATED
UE_VFX_SANDBOX = CREATED; UE_VERSION = 5.8.2; PATH = UEVFXSandbox/SanctaMMO_VFXSandbox.uproject
GAMEPLAY_BINDINGS = NONE; MAIN_PROJECT_INTEGRATION = NO
NEXT_GATE = VFX_VSLICE_001_TEMPLATE_ADAPTATION_AND_READABILITY
STOP_REASON = Four stock-template Niagara systems load in the isolated project; custom visual fidelity and graph/lifecycle review remain open.
```
