# VFX_VSLICE_001 Proposal

Status: PROPOSED; design-only. Do not implement Niagara production effects under Foundation V1.

## Purpose

Validate a small cross-section of the proposed VFX patterns: event confirmation, motion, spatial warning, persistent state, and interaction feedback. Every item remains a generic prototype pattern, not a skill, status, gathering rule, or gameplay contract.

Local prototype stand-ins may use fixed preview controls for composition only. Those values must be labeled preview-only and must not become gameplay defaults.

## Proposed items

| VFX_ID | Category | Source status | Pattern tested | Readability goal | Expected performance risk | Dependencies / deferred inputs |
|---|---|---|---|---|---|---|
| VFX-COMBAT-001 | Direct/melee impact | No stable semantic source selected; generic pattern only | One-shot impact burst and cleanup | Event location and supplied direction; intensity does not imply damage amount | Low–medium: burst count and translucent layers | Runtime impact event and transforms; DEFERRED_GAMEPLAY_INPUT |
| VFX-SKILL-001 | Projectile/travel | No stable skill selected; generic pattern only | Runtime-following trail/ribbon and termination | Direction and active path remain visible without defining movement speed | Medium: ribbon overdraw and concurrent trails | Stable projectile event/path binding; DEFERRED_GAMEPLAY_INPUT |
| VFX-SKILL-002 | Area warning/telegraph | No stable skill selected; generic pattern only | Parameterized footprint edge, fill, and timing | Actual supplied footprint, location, facing, and active timing stay readable at density | Medium–high: area fill overdraw and overlap | Runtime shape/timing contract and future target build; DEFERRED_GAMEPLAY_INPUT |
| VFX-CHARACTER-001 | Persistent state | No stable status selected; generic pattern only | Loop activation, state association, and cleanup | Active/inactive and actor association remain distinct | Medium: long-lived systems and concurrent characters | Stable status ID, lifecycle, and replication behavior; DEFERRED_GAMEPLAY_INPUT |
| VFX-INTERACT-001 | Interaction feedback | No stable action selected; generic pattern only | Progress, completion, failure, and cleanup | Result states differ by shape, motion, or timing as well as colour | Low–medium: repeated progress events and local density | Stable interaction contract; DEFERRED_GAMEPLAY_INPUT |

## Deferred and excluded

- Environmental/ambient effect: DEFERRED_WORLDART_INPUT for a selected environment, approved regional context, and material/palette compatibility. No ambient identity is invented here.
- Gathering or crafting: may later use the interaction pattern, but no stable source action was selected for this proposal.
- Friend/enemy, faction, element, skill identity, damage magnitude, range, radius, duration, and projectile speed: not assigned by this pattern plan.
- Exact performance budgets: DEFERRED_PROFILING_RESULT.
- Existing NS_JumpPad content: observed at the Unreal snapshot only; not selected as a source or accepted look.

## Acceptance needed for a later slice task

Before production implementation, bind selected patterns to stable gameplay event/semantic sources, record their exact revisions and paths, authorize Unreal write scope, and agree on the relevant visual inputs. Review readability at normal and high density, then profile progressively using VFX_PERFORMANCE.md. This proposal itself is not implementation or formal acceptance.
