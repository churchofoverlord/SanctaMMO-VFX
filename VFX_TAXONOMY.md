# VFX Taxonomy

Status: LOCAL FOUNDATION V1.

A VFX_ID identifies a production item inside the VFX Project. It does not replace a gameplay Skill ID, Unreal Asset ID, or decision ID.

## Domains and ID prefixes

| Domain | Prefix | Typical scope |
|---|---|---|
| Combat | COMBAT | Impacts, hit confirmation, combat danger cues |
| Skills | SKILL | Cast, travel, target, and skill-family presentation |
| Character | CHARACTER | Aura and persistent character states |
| World | WORLD | World-object and systemic world feedback |
| Atmosphere | ATMOSPHERE | Non-gameplay-critical ambient motion |
| Weather | WEATHER | Rain, wind, snow, and weather-associated effects |
| Interaction | INTERACT | Interaction feedback and progress |
| Gathering | GATHER | Resource gathering presentation |
| Crafting | CRAFT | Crafting and workstation presentation |
| Processing | PROCESS | Refining and transformation presentation |
| Logistics | LOGISTICS | Movement, storage, and delivery feedback |
| Settlements | SETTLEMENT | Settlement state and service presentation |
| Territory | TERRITORY | Territory and control-state feedback |
| Siege | SIEGE | Siege equipment, damage-state, and objective cues |
| Objectives | OBJECTIVE | Objective-state and completion cues |
| Systemic Feedback | SYSTEMIC | Cross-domain world or system feedback |

Format: VFX-<PREFIX>-<NNN>. Use three-digit, zero-padded numbers per prefix. Allocate an ID only to a real registry entry or a bounded proposed slice item; do not reserve speculative ranges.

## Status vocabulary

Use a short status that says what has actually happened:
- PROPOSED_PATTERN: design-only pattern with no production or semantic claim.
- SOURCE_BOUND: a stable committed source and exact revision are recorded; this does not claim implementation, acceptance, or canonical authority.
- SOURCE_DEFERRED: no usable stable source is bound; preserve the generic pattern and record the missing input.
- BRIEF: bounded intent and source binding exist.
- PROTOTYPE: local technical or visual prototype exists.
- IN_REVIEW: evidence is ready for the named review.
- PRODUCTION: authorized production work is underway.
- INTEGRATED: implementation is in the authorized target at a recorded SHA.
- ACCEPTED: required formal acceptance evidence exists.
- DEFERRED_SOURCE: required stable input is unavailable.
- RETIRED: item is no longer active; retain its ID and reason.

Never infer ACCEPTED from a promising asset, local commit, or technical PASS.
