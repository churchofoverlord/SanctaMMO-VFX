# VFX-CHARACTER-001 — Persistent state

## Purpose

Prototype a state-associated actor cue while keeping active state, duration, and cleanup owned by gameplay.

## Source Binding

- VFX_ID: VFX-CHARACTER-001
- Source Repository: SanctaMMO-Foundation-5.8; read-only local checkout C:\Dev\SanctaMMO-SKILL-001
- Source Revision: b5cf12a64ffd971b195c0d6406d6ed1c93326916
- Source Path: Source/SanctaMMO/Private/Skills/SanctaT1SkillDefinitions.cpp; Source/SanctaMMO/Private/Combat/SanctaCombatComponent.cpp; Source/SanctaMMO/Public/Combat/SanctaAttributeComponent.h; Source/SanctaMMO/Private/Combat/SanctaAttributeComponent.cpp; Source/SanctaMMO/Public/Combat/SanctaStatusEffectModel.h; Source/SanctaMMO/Private/Combat/SanctaStatusEffectModel.cpp; Source/SanctaMMO/Private/Skills/SanctaCombatReceiver.cpp
- Semantic/Game/System ID: scout.torpor applying ESanctaCoreEffectType::Slow
- Source Status: SOURCE_STABLE; server-side apply/expiry/cleanup is code-observed at the pinned SHA. The standalone deterministic status model was proven at bb3f39b3e2cf043cf695a73b342a0834519db86d; that evidence did not prove live client replication. FORMALLY_ACCEPTED=NO; CANONICAL=NO.
- Runtime Event / Entry Point: Skill outcome applies a status to the receiver's authoritative AttributeComponent; the status model expires or removes it, and death clears active statuses.
- Available Runtime Parameters: Status/effect identity, source entity/incarnation, affected actor through receiver, active/inactive state, and expiry are available on the server.
- Missing Parameters: Replicated read-only active status identity/lifecycle for observing clients. The short SlowOutcome cue on application is not an active-state stream.
- Lifecycle: Authoritative application or replacement; remains active according to the source; expiry, removal/cleanse, or death cleanup terminates it.
- Replication / Authority Notes: StatusEffects is a server-owned member, not a replicated property. Health, mana, and death state replicate separately. VFX must not become state authority.
- Presentation Hook Candidate: Bounded read-only status presentation event/view sourced from the existing authoritative status set. CF-VFX-0002 records the needed handoff.
- Why This Source Was Selected: Slow is an implemented persistent actor state with a bounded identity and cleanup lifecycle; it validates state association without selecting a new permanent visual language.

## Production Brief

- Gameplay Meaning: The selected status is active on the affected actor until its authoritative lifecycle ends.
- Presentation Inputs: State identity, affected actor, active/inactive transition, and source lifecycle. Do not duplicate duration.
- Viewer Priority: State association and active/inactive status; readability must survive reduced effects.
- Source/Target Context: scout.torpor is the source skill; the affected receiver owns the state.
- Friendly/Hostile Requirement: The selected test skill targets a hostile receiver. Do not generalize relation colors or faction identity.
- Cast Phase: Not part of this persistent-state item.
- Travel Phase: Separate projectile phase; do not conflate travel with state activation.
- Pre-impact Phase: None.
- Impact Phase: A separate short outcome may indicate successful application, but it cannot stand in for the persistent state.
- Persistent Phase: Show a compact cue only while the authoritative state is active.
- Termination: Stop promptly on replicated inactive/removal/expiry; do not hold longer to finish a visual animation.
- Readability Goal: Make active/inactive state and actor association clear at gameplay distance.
- Shape/Motion Intent: One stable actor-associated cue with restrained motion. WORLDART_INPUT_REQUIRED for final palette and material language.
- Accessibility Requirement: State cannot depend only on color; combine silhouette, placement, and motion/timing.
- Proposed Niagara Pattern: Loop activated and deactivated from an authoritative state presentation hook; cleanup tied to the source.
- Proposed Material Pattern: WORLDART_INPUT_REQUIRED. No production material is selected in this gate.
- Potential Mesh/Texture Needs: None established.
- Scalability Plan: HERO/NORMAL may include secondary detail; REDUCED/MASS_COMBAT retain one compact actor cue.
- Density Risk: Long-lived effects multiply across many actors.
- Performance Risk: Persistent component count, material cost, and simultaneous actors require profiling.
- Known Missing Inputs: Client-visible status lifecycle; exact-SHA runtime proof for live state integration; permanent status visual language.
- Implementation Boundary: VFX reads state. It does not apply, extend, cleanse, or author duration.
- Readiness: READY_FOR_LOCAL_LOOKDEV; DEFERRED_GAMEPLAY_INPUT for a persistent client visual.
