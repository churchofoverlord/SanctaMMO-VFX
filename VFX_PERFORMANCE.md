# VFX Performance and Scalability Method

Status: methodology only. Numeric budgets are DEFERRED_PROFILING_RESULT.

## Capture discipline

For every profile, record the exact VFX implementation revision, Unreal version/build, hardware, resolution, scalability settings, map or scenario, capture duration, warmed-up state, and number of active systems. Keep comparison settings constant. Save an evidence reference with the registry item.

Use Unreal's available profiling and Niagara inspection tools at the target build. Separate measured facts from visual estimates. Do not infer a budget from a single effect preview.

## Scenarios

| Scenario | Purpose |
|---|---|
| A. Isolated effect | Establish cost and visual behavior for one system and repeated triggers |
| B. Small encounter | Check local overlap and simultaneous instances |
| C. Party encounter | Check player, enemy, projectile, impact, telegraph, and persistent-state combinations |
| D. Larger combat | Find scaling pressure and competition among critical cues |
| E. Mass-combat / high-density | Verify critical information survives aggressive reduction and many concurrent systems |
| F. Accumulated environmental FX | Check long-lived loops, weather, ambience, and state accumulation |

Progress from the smallest scenario that can answer the question. Repeat only when a change affects the measured claim.

## Measurements

Collect as relevant:
- GPU and CPU cost, including CPU simulation;
- transparent overdraw and material complexity;
- active particle count, spawn rate, lifetime, and simultaneous systems;
- dynamic lights, distortion, decals, ribbons, and volumetrics;
- collision and event/tick work;
- component cleanup and effects that remain after their source state ends;
- readability of the gameplay-critical cue at expected density.

Do not set final per-effect budgets until representative measurements exist for the target hardware and scenarios. Track measured values with their conditions; do not turn an isolated best-case result into a universal cap.

## Conceptual scalability tiers

The effect-class reduction and preservation rules are in VFX_BIBLE.md. Apply them through authored scalability controls where practical:
- HERO: full approved layers and family detail.
- NORMAL: balanced primary cue and limited secondary detail.
- REDUCED: suppress secondary spawns, extended ribbons, extra lights, distortion, and broad translucent coverage first.
- MASS_COMBAT: remove decorative layers and reduce instance cost; preserve authoritative footprint, direction, event/state, and termination cues.

Gameplay-critical information must remain readable at every tier. If reduction removes that information, the effect has failed the scalability review.

## Evidence gates

A profile is TECHNICALLY_PROVEN only at its recorded implementation SHA, target build, hardware/settings, and scenario. Human visual review remains necessary for readability and density. Performance PASS alone is not formal acceptance.
