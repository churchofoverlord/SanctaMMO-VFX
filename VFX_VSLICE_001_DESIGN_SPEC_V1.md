# VFX_VSLICE_001 — Isolated design and prototype specification

Status: DESIGN COMPLETE; PROTOTYPE READY. Design only: no Niagara assets, Unreal project, code, gameplay data, or main-project files were created or changed.

- Design revision: `VFX_DESIGN_VSLICE_001_V1`
- Source-binding base: `c2aa26acb62ff0c6a5ed379f30a69fc15be26d0d`
- Foundation base: `15ff5728d203e3dd2c8df6d086bdd60fb472a716`

## Scope and authority

This specification advances only VFX-COMBAT-001, VFX-SKILL-001, VFX-CHARACTER-001, and VFX-INTERACT-001. Their exact source bindings and event boundaries remain in the individual briefs. VFX-SKILL-002 remains `SOURCE_DEFERRED`; its ground-area evidence is resolution-only and does not authorize a warning, warning timing, or warning footprint.

The names, modules, materials, and parameter schemas below are proposed design, not assets or runtime contracts. Future effects consume source events and transforms. Preview-only spatial or visual controls must be labeled `LOOKDEV_ONLY — NOT GAMEPLAY AUTHORITY`. They may not supply gameplay dimensions, speed, impact severity, state, or result.

Palette, faction/relationship treatment, regional material language, and final emissive use remain `OPEN` for WorldArt/gameplay authority. They do not block non-color silhouette and motion lookdev. No permanent visual language is declared approved.

## UE sandbox

`UE_VFX_SANDBOX = OPEN`

Inspection of `C:\Dev\SanctaMMO-VFX` found no `.uproject`, `.uplugin`, or VFX sandbox directory. The main-game engine association remains unmapped in the existing baseline. No sandbox was created: there is no project/engine association here that is clearly separate from the Unreal main project. This is a prototype-ready specification, not a technical prototype. A later bounded task may select or establish an unambiguously separate local sandbox.

## Family grammar

Keep one primary cue per effect. Use silhouette, position, motion, and value contrast before decorative particles; colour is optional and currently open. Each family has a different primary shape so related signals remain separable at density:

| VFX_ID | Primary silhouette | Motion | Core meaning and non-meaning |
|---|---|---|---|
| VFX-COMBAT-001 | Compact, near-symmetrical impact stamp with a crisp incomplete rim | Brief radial opening and settle at the supplied event location | Confirms a hit event and location; does not express damage magnitude, surface normal, or facing. |
| VFX-SKILL-001 | Existing projectile body plus one narrow tapered trail | Trail samples the projectile's actual replicated transform; it never extrapolates or steers | Shows current travel path and termination; it does not set speed, target, collision, or impact. |
| VFX-CHARACTER-001 | Actor-space paired drag marks or a broken lower-body band, not a ground footprint | Sparse tethered drift while the source state is active | Associates Slow with an affected actor; visual cadence does not measure Slow strength or duration. |
| VFX-INTERACT-001 | Station-attached open bracket for pending, with distinct closed/admission and broken/rejection result shapes | One compact transition on the real owner result | Communicates request admission/result; accepted means queued, not processing progress or completion. |

All pulse rates, fade envelopes, ribbon widths, and local-preview dimensions are composition controls only: `LOOKDEV_ONLY — NOT GAMEPLAY AUTHORITY`. They do not create a cast window or alter a source lifecycle. Use no fast flicker as the sole state marker.

### Edge, value, direction, and hierarchy

- Keep the primary silhouette's outer edge crisp enough to survive a light or dark background; use a restrained interior value break instead of broad bloom or stacked translucency.
- Hit uses a compact radial stamp with an interrupted edge and stays non-directional. Projectile direction comes only from actor transforms. Slow uses actor-space marks, not a ground boundary. Interaction uses bracket gaps to distinguish request states around the station.
- The primary event/state/station cue outranks every secondary mote or surface accent. Secondary detail may be removed completely at REDUCED and MASS_COMBAT.
- Do not assign hue or faction meaning in this revision. Use placement, silhouette, motion, and value separation for the prototype grammar.

### Actor relationship and importance

- VFX-COMBAT-001: the inspected binding is an NPC receiver path. Self/ally/enemy classification is `OPEN`; do not tint or rank by faction. The primary role is event confirmation.
- VFX-SKILL-001: the selected fixture targets a hostile receiver, but observing-client skill and receiver identity are absent. Do not generalize faction treatment. The primary role is travel-path readability.
- VFX-CHARACTER-001: the state belongs to the affected actor. Its client-visible active state is missing. Relation treatment is `OPEN`; do not render a persistent loop until an authoritative state feed exists.
- VFX-INTERACT-001: request/result is owner-only and attached to the selected station. Ally/enemy is not applicable. Keep textual explanation in UI; world VFX is supplementary.

## Niagara and asset architecture

These are effect-specific systems. Do not add a master system, generic state machine, shared gameplay enum, or shared material framework for this four-effect slice.

| VFX_ID | Proposed system and emitters | Runtime-facing user parameters | Simulation, renderer, and cleanup |
|---|---|---|---|
| VFX-COMBAT-001 | `NS_VFX_COMBAT_001_BasicHit`; one `E_BasicHit` short-burst emitter | `User.EventLocation`, `User.EventKind`; `User.EventRotation` only if the real cue supplies it | CPU prototype baseline; one sprite/mesh silhouette. Start only on a successful authoritative hit event. Event lifetime is presentation-only; auto-clean after its visual envelope. |
| VFX-SKILL-001 | `NS_VFX_SKILL_001_Projectile`; `E_ProjectileTrail` ribbon emitter; body remains the source actor's visible mesh unless inspection in the eventual sandbox shows otherwise | `User.ProjectileTransform`, `User.SourceActive`; direction may be derived from successive transforms for presentation | CPU prototype baseline sampling the actor transform. Ribbon is the only planned continuous renderer. Stop and clear on source termination; no extrapolated trajectory. Impact is a separate event, never inferred from trail fade. |
| VFX-CHARACTER-001 | `NS_VFX_CHARACTER_001_Slow`; one actor-associated loop emitter | `User.ActorTransform`, `User.StateActive`; `User.StateId` only if the integration hook provides it | CPU prototype baseline, low-profile sprites. Start/stop only from an authoritative active-state feed. That feed is currently missing, so only a clearly labeled local composition preview can exercise the shape. |
| VFX-INTERACT-001 | `NS_VFX_INTERACT_001_ProcessingFeedback`; one static `E_RequestPending` bracket while the actual request is pending, then one `E_AdmissionResult` one-shot | `User.StationTransform`, `User.FeedbackSequence`, `User.FeedbackState` | CPU prototype baseline. Pending has no periodic spawn/progress motion; result selects accepted/rejected/unknown shape. Clear the pending bracket on the owner result; do not keep any effect for a Queued order. No progress parameter exists. |

The module names are conceptual UE Niagara equivalents, not a promise about an unmapped target engine version. A future sandbox should validate the actual spawn, initialize, particle update, renderer, and cleanup modules before asset creation.

### Proposed module order per emitter

Use the smallest module chain and validate its actual class names in the isolated engine before building assets:

| Emitter | Conceptual module sequence |
|---|---|
| `E_BasicHit` | Emitter State (non-looping) → Spawn Burst Instantaneous on the hit event → Initialize Particle from `User.EventLocation` → Particle State / visual size-and-fade over normalized visual age → Sprite or Mesh Renderer → auto cleanup. No force, collision, or damage-driven module. |
| `E_ProjectileTrail` | Emitter State gated by `User.SourceActive` → sample/spawn from `User.ProjectileTransform` → Initialize Particle → Particle State / taper over visual age → Ribbon Renderer → stop spawning and clear on actor termination. Sampling density is a lookdev control only. |
| Slow loop emitter | Emitter State gated only by authoritative `User.StateActive` → initialize around `User.ActorTransform` → Particle State / low-motion offset → Sprite Renderer → stop and clear on inactive. No force/time-scale module. |
| `E_RequestPending`, `E_AdmissionResult` | Pending: actual request/Pending state gates one static station bracket with no repeating Spawn Rate or age-driven timeout. Result: one Spawn Burst Instantaneous from the owner result → Initialize from `User.StationTransform` and the selected result shape → Particle State / visual fade → Sprite Renderer → cleanup. Remove the pending bracket on the real result. No progress emitter. |

Use simple authored shape inputs (sprite geometry or a validated ribbon) rather than forces, collisions, or Niagara-side gameplay logic. Runtime result/state selects a bounded effect-specific path; it does not change game behavior.

### Common implementation choices

- **Dynamic parameters:** none initially. Pass event/state values through a small user-parameter contract. Add a dynamic material parameter only if a tested material requires it.
- **Materials:** one local prototype material per effect at first. Prefer crisp masked/simple unlit shapes; reserve additive treatment for a small core. Avoid broad translucent fills. Final blend mode and material language remain `OPEN` to WorldArt review.
- **Material instances:** none required for the first blockout. Use an instance only when a real visual parameter must vary without duplicating a material.
- **Textures / meshes:** no new texture or mesh is required by the current designs. Use simple sprites, analytic shapes, or a short ribbon. Do not create production geometry from a placeholder.
- **Ribbon:** only VFX-SKILL-001. Keep it narrow and tied to sampled actor transforms; remove secondary strands at lower tiers.
- **Decals, lights, distortion, volumetrics:** none in the initial prototype. Reconsider only if readability evidence shows a specific need and profiling supports the cost.
- **Collision:** none in Niagara. Gameplay collision and hit detection remain exclusively in the source runtime.
- **Pooling/reuse:** use normal source/component cleanup first. No custom pool or shared emitter library until repeated use and measured spawn/cleanup cost justify it.
- **CPU/GPU:** CPU is the simple prototype starting point for sparse event/actor-following systems, not a final performance decision. GPU conversion is deferred to comparative profiling; no budgets are set here.

## Runtime binding contract

| VFX_ID | Required source binding | Available from current source | Missing or `OPEN` |
|---|---|---|---|
| VFX-COMBAT-001 | Successful hit result and supplied event location | Server-side result and an observed replicated cue location on the inspected NPC path | Exact-SHA runtime validation of the cue; player-target/general identity payload; contact point and normal. Directional streaks are excluded until supplied. |
| VFX-SKILL-001 | Current projectile transform and actor termination | Replicated movement is code-observed at pinned SHA | Exact-SHA multiplayer observation; skill/receiver identity for skill-specific treatment. A generic trail needs neither identity. |
| VFX-CHARACTER-001 | Affected actor, status identity, active/inactive transition | Server owns Slow identity/lifecycle | Client-visible `StateActive` hook. Do not simulate state locally or infer it from a one-shot application cue. |
| VFX-INTERACT-001 | Local request, station transform, owner result and correlation sequence | Request/result and replicated station are technically proven at the pinned runtime SHA | Client retains station identity for correlation because the response does not echo it. Progress/completion do not exist in this source. |

`VFX-SKILL-002` has no production binding contract in this spec. Do not add `FootprintShape`, `Radius`, `ActiveDuration`, or warning start/end from preview values. Any shape mock-up must say `LOOKDEV_ONLY — NOT GAMEPLAY AUTHORITY` on the preview control and remain non-semantic.

| Binding value | Classification | Limit |
|---|---|---|
| Basic Attack hit kind/location | AVAILABLE_NOW in code; current cue path is not runtime-proven at its pinned SHA | Use only for local preview until exact-SHA validation; no contact normal or universal receiver event. |
| Projectile transform and actor-active lifecycle | AVAILABLE_NOW in code | Runtime observation at exact SHA remains open; do not extrapolate speed/path. |
| Slow actor and status-active transition on observing clients | MISSING_PRESENTATION_HOOK | The server state exists, but VFX must not synthesize or replicate it. |
| Processing station transform and actual owner result | AVAILABLE_NOW and TECHNICALLY_PROVEN | Correlate locally by request sequence and retained station; no production progress. |
| Preview scale, pulse envelope, ribbon thickness | DERIVABLE_SAFELY for local composition only | Every preview control carries `LOOKDEV_ONLY — NOT GAMEPLAY AUTHORITY`; never serialize as a gameplay default. |
| Surface normal/contact data; self/ally/enemy relation | MISSING_PRESENTATION_HOOK / OPEN | Omit the corresponding directional or relationship treatment until an actual source supplies it. |
| Any new gameplay meaning, timing, dimension, speed, or status simulation | REQUIRES_GAMEPLAY_CHANGE | None required or authorized for these designs; stop only that effect if it becomes necessary. |

## Scalability matrix

No tier has a numeric particle or millisecond budget. Preserve the primary source meaning in every tier.

| VFX_ID | HERO | NORMAL | REDUCED | MASS_COMBAT — preserved information |
|---|---|---|---|---|
| VFX-COMBAT-001 | Primary stamp plus restrained edge detail and optional decorative fragments | Fewer decorative fragments and simpler material | Primary silhouette only; shorten decorative fragment lifetime | Hit location and occurrence. No ribbon, light, decal, distortion, volume, or collision. |
| VFX-SKILL-001 | Source body plus narrow ribbon and optional fine accents | One ribbon with lower visual sampling density and simpler material | Thin, shorter visual history; suppress accents | Current direction/path and source termination. Remove ribbon ornament, excess spawn, and translucent width before the primary trace. |
| VFX-CHARACTER-001 | Actor band plus sparse tethered accents | Band with fewer accent spawns | Stable band only with simple material | Active-state association and affected actor, when actual state is available. Drop free particles and shorten only their decorative lifetime; never time out the state band. |
| VFX-INTERACT-001 | Station bracket plus one small result accent | Bracket and result shape with fewer accents | Simplified bracket/result shape and material | Pending versus accepted/rejected/unknown and target station. Remove secondary particles/lifetime; never merge states or shorten pending before its real result. |

Across all four effects, reduce spawn rate, secondary particles, material complexity, ribbon density/width, and decorative particle lifetime where applicable. Lights, decals, distortion, volumetrics, and Niagara collision are absent from the first prototype; if later justified, remove them at REDUCED and MASS_COMBAT before touching primary information.

If a source state is unavailable, scalability must not keep a stale visual alive. If a reduction removes the primary information, the design fails readability review rather than receiving an invented intensity/budget fix.

## Readability review criteria

Future human review should record `PASS/FAIL/OPEN` against each criterion at the tested implementation SHA. No readability claim is made by this specification alone.

1. **Isolated:** one event/state reads at the normal gameplay camera and remains visually attached to its runtime location/actor/station.
2. **Overlap:** inspect each family beside other players, projectile trails, hit cues, status cues, and repeated interaction requests. The four primary silhouettes remain distinct; ornament does not obscure the actor or station.
3. **Backgrounds:** silhouette and value separation hold against both light and dark backgrounds without prescribing a WorldArt palette.
4. **Direction and impact:** projectile direction follows observed transforms; impact reads location only unless a real direction/normal arrives. Never infer a hit from an actor passing near the trail.
5. **Relationship:** no self/ally/enemy distinction is asserted until a stable relation input exists. Check that neutral shape remains legible without color.
6. **Persistence:** Slow loop exists only while real `StateActive` is true; visual fade cannot outlast termination. Until the hook exists, mark the preview simulated and do not grade lifecycle fidelity.
7. **Interaction:** pending, accepted/queued, rejected, and unknown are distinguishable by shape/motion as well as value; none resembles progress or completion. UI retains text and authoritative explanation.
8. **MASS_COMBAT:** remove secondary detail and overlapping translucent layers; the essential hit, path/termination, active-state association, and station result remain identifiable.
9. **Accessibility:** run a colour-independent read and reduced-colour preview; no primary state depends only on hue or fast flicker.
10. **Fidelity:** compare every onset/termination against the source event or state. Any unsupported phase is `OPEN`, not silently animated.

## Performance evidence plan

Use the scenarios and capture discipline in `VFX_PERFORMANCE.md`. At each relevant tier, record exact implementation revision, engine/build association, hardware, resolution, scenario, settings, active-system count, warm-up, capture duration, measured values, and the evidence path. Do not convert placeholder targets into budgets.

| VFX_ID | Measurements to capture when a sandbox exists |
|---|---|
| VFX-COMBAT-001 | CPU/GPU simulation, particles per trigger, spawn rate, screen coverage/overdraw, material cost, transient cleanup, overlapping hit-system count. |
| VFX-SKILL-001 | Ribbon sample/spawn rate, live particle count, ribbon overdraw and material cost, transform-update cost, simultaneous projectiles, cleanup after actor destruction. |
| VFX-CHARACTER-001 | Active loop/system count, CPU/GPU simulation, per-character particles, material cost, overdraw, stale components after authoritative termination, dense actor count. |
| VFX-INTERACT-001 | One-shot CPU/GPU cost, overlapping request/result systems, material cost, screen-space overlap at stations, cleanup after each owner result. |

Record lights, decals, distortion, volumetrics, and Niagara collision as zero-use in the first prototype; if a later design adds any, capture their count and cost explicitly. Measure GPU time, CPU simulation, particle count/lifetime/spawn rate, transparent overdraw, material instructions, ribbon cost, and simultaneous system count before tuning a profile.

## OPEN / DEFERRED register

- `OPEN — UE_VFX_SANDBOX`: no isolated `.uproject` or engine association exists in this VFX workspace. No UE path is selected and no prototype asset exists.
- `OPEN — Basic Attack cue`: exact-SHA runtime validation is required before a future implementation binding; current cue code observation is not runtime proof.
- `OPEN — projectile runtime`: exact-SHA multiplayer observation of the actor path is not present. Keep the design transform-following only.
- `OPEN — Slow state`: client-visible active/inactive state is absent. A local shape preview must not simulate gameplay activation.
- `OPEN — WorldArt finish`: palette, material language, emissive use, and any permanent family colour require stable visual input. Shape/value prototyping may proceed without them.
- `OPEN — relationship grammar`: self/ally/enemy/faction treatment is not supplied by the selected presentation contracts.
- `OPEN — engine module mapping`: project-to-engine association and Niagara module availability are unverified in a separate sandbox.
- `DEFERRED_GAMEPLAY_INPUT — VFX-SKILL-002`: no authoritative pre-impact warning lifecycle/footprint. No gameplay telegraph design or implementation.
- `DEFERRED_PROFILING_RESULT`: all final CPU/GPU, particle, overdraw, materials, ribbons, and concurrency budgets.
- `DEFERRED_FORMAL_ACCEPTANCE`: no VFX design or effect is formally accepted or integrated.

## Gate result

```text
VFX_VSLICE_001_DESIGN_READINESS = PROTOTYPE_READY
VFX_VSLICE_001_TECHNICAL_PROTOTYPE = NOT_CREATED
UE_VFX_SANDBOX = OPEN
VFX-SKILL-002 = SOURCE_DEFERRED
FORMALLY_ACCEPTED = NO
INTEGRATED = NO
NEXT_GATE = VFX_VSLICE_001_LOCAL_LOOKDEV
```
