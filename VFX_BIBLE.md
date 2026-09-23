# SanctaMMO VFX Bible V1

Status: initial VFX principles; not a new global Art Direction approval.

## Visual compatibility

The stable local WorldArt source at revision a6b3be7fe42d5cd6c6820efda5ae3c04d4acff7f describes Grounded Stylized Fantasy with Graphic Readability, medium-detail simplified realism, and the priority gameplay readability → silhouette → shape → value/colour grouping → material → detail. It also calls for naturalistic lighting, controlled fog, readable midtones, and rare meaningful environmental emissives.

VFX uses those rules as constraints on its presentation. This Bible adds no biome palette, faction colour, world silhouette, elemental identity, or new environmental material language. Such specifics are DEFERRED_WORLDART_INPUT or DEFERRED_CANON_INPUT.

Source paths: SanctaMMO-WorldArt/CANON/WORLD_ART_BIBLE.md, CANON/MATERIAL_LANGUAGE.md, and CANON/VISUAL_DETAIL_STANDARD.md at the revision above.

## Readability before spectacle

Every effect starts with the gameplay fact it must communicate: what happened, where, in which direction, to whom, whether it persists, and when it ends. Remove detail that competes with that fact.

Use scale, silhouette, movement, timing, edge treatment, and spatial pattern before decorative particles. Use one clear primary cue and only enough secondary cues to distinguish related events.

## Shape and motion

- Use a compact primary silhouette at normal gameplay distance; reserve fragments and fine motes for secondary detail.
- Directional events use motion aligned with runtime-provided direction or trajectory.
- Repeated related effects share a small number of shape and timing patterns; family identity may vary within those patterns.
- Do not encode class, faction, ally/enemy, element, rarity, or biome identity until the relevant visual/gameplay input is stable and approved.

## Lifecycle grammar

| Phase | Visual purpose | Boundary |
|---|---|---|
| Cast / anticipation | Show commitment or imminent action where runtime exposes it | Do not imply a cast time or interrupt state that gameplay does not expose |
| Release / travel | Show a launched event and its direction | Follow the runtime event and transform; do not define projectile speed or targeting |
| Impact | Mark the event location clearly | Intensity must not claim damage magnitude unless runtime explicitly supplies it |
| Area warning | Show the actual authoritative shape, location, direction, and timing | Consume runtime parameters; no duplicated radius or duration |
| Persistent state | Show that a state is active and which entity it belongs to | Follow replicated state and source lifecycle; do not invent duration or owner |
| Termination | Stop, fade, or dissipate when the source state ends | Avoid stale looping visuals; visual fade cannot extend gameplay duration |

## Self, ally, enemy, danger, and systemic cues

Use separate shape/motion/timing treatment as well as colour when differentiating actor relationships or danger. Keep the permanent colour code OPEN until stable gameplay and visual input exists. A danger cue may use stronger silhouette, edge, timing, or spatial contrast, but must not add an unapproved gameplay warning.

Systemic and objective feedback should be spatially attached to the relevant object/state where possible. Keep completion, failure, and state transition distinguishable without requiring a colour read.

## Accessibility

Critical information must not rely on colour alone. Combine as appropriate:
- shape and silhouette;
- movement and direction;
- spatial pattern and placement;
- timing and pulse/frequency;
- edge treatment and intensity.

Avoid fast flicker as the sole state marker. Friend/enemy and hazard patterns remain OPEN until approved input exists. Preserve a readable form under reduced effects and colour-vision variation.

## MMO density

Judge families both alone and alongside overlapping players, projectiles, telegraphs, persistent states, and ambient effects. Layer priority is gameplay-critical warning/state, actor relation, event confirmation, then decorative secondary motion. Reduce overlap, lifetime, secondary spawns, lights, and distortion before suppressing the primary cue.

## Scalability intent

| Effect class | HERO | NORMAL | REDUCED | MASS_COMBAT | Must remain readable |
|---|---|---|---|---|---|
| Impact | Full authored burst and selected secondary detail | Fewer secondary layers | Compact primary pulse | Suppress ornament and excess fragments | Event occurrence, location, direction when supplied |
| Projectile/travel | Full authored trail | Shorter or thinner trail | Minimal directional trace | Remove ribbon ornament and nonessential particles | Active path or direction and termination |
| Telegraph/area | Full edge and restrained fill motion | Reduce secondary animation | Simplify fill and pulse | Use stable high-contrast boundary and timing cue | Authoritative footprint, location, facing, and active timing |
| Persistent state | Full family treatment | Fewer layers | One compact state cue | Remove ornament; keep compact state marker | Active/inactive state and actor association |
| Interaction | Full progress and completion treatment | Fewer particles | Simplified progress cue | Keep compact progress/result cue | Progress, completion, or failure state |
| Ambient | Full approved ambient detail | Reduce spawn density | Minimal ambient motion | May disappear when noncritical | Any gameplay-critical hazard/state signal |

These tiers are conceptual, not final quality settings or numeric budgets. Ambient detail may disappear only when it carries no gameplay-critical information.
