# VFX-SKILL-001 — Projectile travel

## Purpose

Validate a presentation trail that follows a real server-owned projectile actor. VFX must not create or steer gameplay movement.

## Source Binding

- VFX_ID: VFX-SKILL-001
- Source Repository: SanctaMMO-Foundation-5.8; read-only local checkout C:\Dev\SanctaMMO-SKILL-001
- Source Revision: b5cf12a64ffd971b195c0d6406d6ed1c93326916
- Source Path: Source/SanctaMMO/Private/Skills/SanctaT1SkillDefinitions.cpp; Source/SanctaMMO/Public/Skills/SanctaGameplayProjectile.h; Source/SanctaMMO/Private/Skills/SanctaGameplayProjectile.cpp; Source/SanctaMMO/Private/Combat/SanctaCombatComponent.cpp
- Semantic/Game/System ID: scout.torpor; ASanctaGameplayProjectile
- Source Status: SOURCE_STABLE; source code shows a server-owned projectile and replicated movement at the exact SHA. No exact-SHA runtime evidence was found. FORMALLY_ACCEPTED=NO; CANONICAL=NO.
- Runtime Event / Entry Point: Authoritative skill execution spawns ASanctaGameplayProjectile; Tick advances the actor toward the bound receiver and calls authoritative resolution at arrival.
- Available Runtime Parameters: Spawn transform; replicated projectile transform during travel; server-side skill ID, receiver, and authored speed; wall collision termination; successful arrival and receiver outcome cue.
- Missing Parameters: Skill ID and bound receiver are server-side fields, not replicated presentation fields. A receiver ID is not needed for a generic actor-following trail. No exact-SHA multiplayer observation of the actor path was found.
- Lifecycle: Spawn, authoritative travel, successful arrival/resolution followed by short visual cleanup, or obstruction/lost source/life followed by destruction.
- Replication / Authority Notes: Actor movement replicates. Server alone advances movement, traces collision, and resolves the skill. The visible mesh primitive is presentation-only and collisionless.
- Presentation Hook Candidate: Attach a local VFX component to the replicated projectile actor and follow its transform. Stop when the replicated actor ends. Do not implement a second trajectory.
- Why This Source Was Selected: It provides a reusable path-following primitive across selected projectile skills without binding VFX to a special visual identity.

## Production Brief

- Gameplay Meaning: A projectile is active and travelling along the runtime path.
- Presentation Inputs: Projectile actor transform and termination. Use authored direction/path; do not set speed, target, collision, or hit.
- Viewer Priority: Active path and termination; gameplay-readable under overlap.
- Source/Target Context: The projectile actor is spawned by the source combat component. Receiver binding is server-side.
- Friendly/Hostile Requirement: The selected scout.torpor fixture is hostile-targeted. Do not infer faction colors or generalized ally behavior.
- Cast Phase: Not supplied by this source.
- Travel Phase: Follow replicated actor transform only.
- Pre-impact Phase: Do not add a warning or expand its footprint.
- Impact Phase: The separate authoritative receiver outcome may provide a short impact cue.
- Persistent Phase: None.
- Termination: Remove trail when projectile actor is destroyed or its short terminal visual lifetime ends.
- Readability Goal: Keep active direction and path visible without drawing a new trajectory.
- Shape/Motion Intent: Directional trace aligned to the runtime transform. WORLDART_INPUT_REQUIRED for final palette and surface treatment.
- Accessibility Requirement: Direction remains legible through silhouette and motion, not color alone.
- Proposed Niagara Pattern: Trail/ribbon candidate attached to actor transform; reduce strand count and ornament first.
- Proposed Material Pattern: WORLDART_INPUT_REQUIRED. No production material is selected in this gate.
- Potential Mesh/Texture Needs: No new mesh or texture required by current evidence.
- Scalability Plan: HERO/NORMAL may include more trail detail; REDUCED/MASS_COMBAT keep a minimal directional trace and termination.
- Density Risk: Simultaneous projectiles and broad ribbons compete for screen space.
- Performance Risk: Ribbon overdraw, trail lifetime, particle spawn rate, and concurrency require target profiling.
- Known Missing Inputs: Exact-SHA runtime validation; client-visible skill identity if a skill-specific family treatment is later required.
- Implementation Boundary: Never set projectile speed, trajectory, collision, hit detection, targeting, or termination.
- Readiness: READY_FOR_LOCAL_LOOKDEV; READY_FOR_UE_IMPLEMENTATION_PENDING_AUTHORITY after exact-SHA runtime verification.
