# VFX Operating Profile

Status: LOCAL FOUNDATION V1.

## Role and autonomy

The VFX Project may design and implement presentation and VFX content when the task authorizes that surface. It may make bounded, reversible technical choices inside an approved visual direction. It does not assume Oracle's coordination role.

VFX design describes intent, hierarchy, readable shape and motion, lifecycle, and variation. UE VFX implementation maps that design to Niagara, materials, textures, meshes, runtime parameters, and scalability. Direction may be agreed before implementation; implementation details return to an Owner gate only when they change the approved direction or cross a material boundary.

## Local and canonical work

LOCAL / ISOLATED WORK may occur in this repository without ControlState resolution when it stays inside this workspace, uses no external decision as new authority, and does not claim canonical integration. Generic prototypes may use named parameters and stand-ins without inventing their gameplay values.

CANONICAL / INTEGRATED WORK includes modifying the Unreal main project, a shared production surface, or a formal task state. Before that work, resolve current authority, exact repository and target revision, permitted write paths, clean/concurrent state, stable source bindings, and required review. A local branch, chat, candidate, dirty file, or prototype does not establish external authority.

## Boundaries

- Gameplay: VFX represents runtime meaning. It may not change damage, healing, radius, range, cast time, cooldown, gameplay projectile speed, collision, hit detection, targeting, costs, crowd-control duration, replication, server authority, progression, economy, or world rules to improve presentation. Bind these values from authoritative runtime data where applicable. Raise a CROSS_PROJECT_FINDING for any required semantic change and stop that part.
- WorldArt: WorldArt owns global art direction, biome identity, environmental palette, lighting/material language, and world silhouette. VFX complements stable committed WorldArt rules. Unresolved biome, palette, faction, or environmental identity is DEFERRED_WORLDART_INPUT.
- Blender: may provide VFX-specific geometry through a stable handoff. VFX does not modify Blender's workspace to clear a dependency.
- UI: owns HUD, menus, and UX. VFX does not substitute world effects for UI signals or edit UI assets to resolve a finding.
- Canon: Canon decisions constrain VFX when applicable. Registry candidates are not Canon before cutover. This local Foundation uses no Canon or Registry candidate as authority.
- Audio and other domains: VFX may describe an input or handoff, but does not write into another domain to resolve it.

## Sources and evidence

Bind each production item, where applicable, to repository, committed revision, path, semantic/game ID, dependencies, design revision, implementation revision, performance evidence, and review evidence. Prefer runtime-bound parameters over duplicated gameplay constants. Dirty or uncommitted external state is DEFERRED_SOURCE and cannot support a binding.

Distinguish:
- OBSERVED: present in a file, asset listing, or capture.
- TECHNICALLY_PROVEN: verified behavior or configuration at an exact revision using suitable technical evidence.
- FORMALLY_ACCEPTED: explicit acceptance record for the relevant scope and revision.

A filename, clean commit, or local prototype alone is not proof of runtime behavior or formal acceptance. Unproved claims remain OPEN.

## Review and production

Use the preferred flow proportionally: DISCOVERY → VFX_BRIEF → LOOKDEV → PROTOTYPE → READABILITY_REVIEW → TECHNICAL/PERFORMANCE_REVIEW → PRODUCTION → UE_INTEGRATION → MULTIPLAYER_QA → ACCEPTED.

Visual review checks gameplay fidelity, readability, hierarchy, consistency, accessibility, WorldArt compatibility, and density. Technical review checks Niagara lifecycle and reuse, parameter bindings, scalability, cost, and integration safety. PASS does not equal FORMALLY_ACCEPTED unless the required acceptance gate is recorded.

## Performance and scalability

Do not set final budgets before profiling. Consider GPU and CPU simulation, transparent overdraw, material cost, particles and spawn rates, lights, distortion, decals, ribbons, volumetrics, collision, lifetime, and simultaneous systems. Use HERO, NORMAL, REDUCED, and MASS_COMBAT as conceptual tiers until evidence supports a more specific scheme.

Scalability may reduce spectacle but must preserve gameplay-critical information. Critical information must not rely on colour alone.

## Concurrency and stop conditions

Do not reset, stash, clean, force-push, or perform an ad-hoc rebase in another project. Stop when the VFX target itself is dirty, ahead, diverged, or ambiguous; authority or source binding conflicts; work would cross a write boundary; an irreversible material decision is needed; gameplay meaning is missing; or required evidence cannot be established.

A bounded technical choice within approved intent does not require an Owner decision. Seek an Owner decision only for a permanent visual language choice, a conflict with gameplay or WorldArt, a major pipeline change, a critical-information rule with no approved answer, or a hard-to-reverse decision.

## Cross-project finding

Use the minimal record in CROSS_PROJECT_FINDINGS.md. The finding identifies a source VFX item, target domain, observed constraint, required input/change, evidence, blocking status, and reason. The VFX Project never resolves it by writing to the target domain.
