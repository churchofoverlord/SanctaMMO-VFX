# Niagara Architecture V1

Status: proposed patterns; validate against the first authorized vertical slice.

## Observed baseline

At SanctaMMO-Repo revision 404f39ad798eb935273ccc95fc1982cf4ad72ae0, a file named Content/LevelPrototyping/Interactable/JumpPad/Assets/NS_JumpPad.uasset was observed, alongside M_SimpleGlow, M_GradientGlow, and MI_GlowNT. Asset metadata and Niagara graphs were not opened. No named production VFX folder or other clear Niagara emitter/system names were found by filename search.

The installed UE 5.8.2 directory contains Niagara's plugin descriptor. The project descriptor uses an unmapped EngineAssociation GUID. Project-level plugin/runtime availability and asset membership are therefore OPEN. Existing names are evidence of presence only, not a naming authority or approved VFX direction.

## Architecture rule

Keep SHARED_PATTERN separate from EFFECT_SPECIFIC implementation. Share stable reusable behavior only after a second real use validates the need. A general-purpose effect framework, large module library, or master system with many unrelated switches is out of scope.

### SHARED_PATTERN candidates

- Spawn and initialize: explicit origin, orientation, and exposed parameters; deterministic defaults for visual-only fields.
- Short burst: bounded one-shot event with cleanup tied to source event completion.
- Trail/ribbon: optional presentation attached to runtime-provided samples or transforms; disable secondary strands first at lower tiers.
- Telegraph: shape and timing are supplied as parameters; visual pattern does not own gameplay radius or duration.
- Persistent state: activation/deactivation follows the authoritative state lifecycle and removes components when the state ends.
- Ambient loop: bounded spawn and lifetime, with approved biome/material inputs before regional use.
- Render/material controls: common parameter names and validated material functions only when multiple effects share the same need.

These are pattern descriptions, not implemented Niagara modules or emitters.

### EFFECT_SPECIFIC implementation

Each authorized effect owns its required event mapping, composition, and small set of parameters. Keep effect-specific modules local until at least two production effects need the same behavior. Do not couple unrelated effects through a master enum.

## Runtime binding and lifecycle

- Prefer runtime-provided position, direction, target, footprint, state, and time values where the event contract supplies them.
- Never create a duplicate gameplay constant because Niagara needs a value.
- Separate presentation interpolation from gameplay movement and collision.
- Start and end systems from explicit source events/state; stop loops, detach components, and release transient resources on termination.
- Do not infer that a replicated event or client presentation is authoritative gameplay.

## Naming

The project snapshot contains one name beginning NS_ and material prefixes M_, MI_, and MF_, but their broader consistency was not established. Proposed system/emitter naming can follow UE-readable type prefixes after asset inspection; it is not a Foundation-wide convention yet. Record the actual class and asset name at the first integration review.

## Minimum material strategy

- Additive: use for small bright sparks or cores; control screen coverage and stacked intensity.
- Translucent: reserve for effects that need soft coverage; avoid broad layered sheets and overdraw.
- Masked cards: use for crisp stylized silhouettes or cutout textures where soft transparency is not needed.
- Emissive: parameterize intensity and keep the environmental language compatible with WorldArt's rare, meaningful emissives.
- Fade/dissolve: use exposed normalized presentation parameters tied to event/state lifetime, not new gameplay duration.
- Depth interaction: use soft depth fades only where intersections visibly harm readability; do not use depth tricks to imply collision.
- Decals: keep few, short-lived, and surface-aware; avoid persistent clutter without approved gameplay meaning.
- Distortion: optional and justified only when it adds readable information; remove it early at REDUCED and MASS_COMBAT.
- Mesh particles: use when silhouette or direction benefits; avoid mesh detail whose cost is not visible at gameplay distance.
- Parameterization: use a small shared set for source color/intensity, scale, age, and runtime-bound event/state data. Palette defaults remain open.
- Material Functions: create a shared function only after repeated usage and a measured maintenance/performance benefit.

No material assets are created by this architecture.
