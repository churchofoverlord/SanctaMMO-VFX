# VFX-COMBAT-001 — Direct impact

## Purpose

Create a compact confirmation for a successful direct Basic Attack. Communicate event occurrence and target-relative location. Never use effect intensity to communicate damage amount.

## Source Binding

- VFX_ID: VFX-COMBAT-001
- Source Repository: SanctaMMO-Foundation-5.8; read-only local checkout C:\Dev\SanctaMMO-SKILL-001
- Source Revision: b5cf12a64ffd971b195c0d6406d6ed1c93326916
- Source Path: Source/SanctaMMO/Private/Game/SanctaPlayerController.cpp; Source/SanctaMMO/Private/Combat/SanctaCombatComponent.cpp; Source/SanctaMMO/Public/Skills/SanctaCombatReceiver.h; Source/SanctaMMO/Private/Skills/SanctaCombatReceiver.cpp; Source/SanctaMMO/Public/Skills/SanctaPresentationCue.h; Source/SanctaMMO/Private/Skills/SanctaPresentationCue.cpp
- Semantic/Game/System ID: Phase2.BasicAttack.IFV; CombatPlay.BasicAttack.IFV
- Source Status: SOURCE_STABLE at the pinned clean commit. The Basic Attack client/server path was runtime-proven at 61a02eada2632fce7a03f512fb9004ac91b5d9d6. The cue and receiver path at the pinned source revision is code-observed, not runtime-proven at that SHA. FORMALLY_ACCEPTED=NO; CANONICAL=NO.
- Runtime Event / Entry Point: Owning PlayerController request → server-side combat validation → authoritative hit/miss result → receiver outcome/cue path for the inspected non-player receiver.
- Available Runtime Parameters: Basic Attack identity; authoritative source and receiver identities on the server; success/hit result; receiver actor transform; replicated short-lived cue kind, radius, world location, and rotation on the current cue path.
- Missing Parameters: Measured contact point and surface normal; a replicated source/receiver event payload; this inspected Basic Attack path does not emit the same cue for player receivers.
- Lifecycle: Request, server validation, hit or miss, authoritative result, then a short-lived cue on the observed non-player path. A miss does not imply impact.
- Replication / Authority Notes: The owning Controller submits the command; the server validates and resolves it. The native outcome event is server-side. ASanctaPresentationCue replicates its event fields. The Phase 2F test explicitly kept PvP disabled.
- Presentation Hook Candidate: ASanctaCombatReceiverComponent::OnOutcome and ASanctaPresentationCue::Spawn. Treat the cue position as actor-relative event location, not physical contact.
- Why This Source Was Selected: It is the simplest demonstrated direct Basic Attack path with a real owning-client request and authoritative target result. It keeps VFX independent of damage magnitude.

## Production Brief

- Gameplay Meaning: A successful direct hit occurred at the supplied receiver-relative location.
- Presentation Inputs: Event kind and world location. Direction is optional and unavailable in this binding. Damage magnitude is excluded.
- Viewer Priority: Event confirmation; preserve primary cue at REDUCED and MASS_COMBAT.
- Source/Target Context: Attacking actor and receiving actor are distinct in the server event. The replicated cue does not expose both identities.
- Friendly/Hostile Requirement: The evidence path uses an NPC target. PvP and ally relation are not established by this binding; do not encode them.
- Cast Phase: Not supplied by this source.
- Travel Phase: Not applicable to the selected direct path.
- Pre-impact Phase: None.
- Impact Phase: One-shot cue at supplied receiver-relative position when the authoritative result is a hit.
- Persistent Phase: None.
- Termination: Short presentation-only cue lifetime; no gameplay state is extended.
- Readability Goal: One compact silhouette marks occurrence and location without implying severity.
- Shape/Motion Intent: Use a restrained single pulse or compact burst around the event location. WORLDART_INPUT_REQUIRED for final color, material language, and detail.
- Accessibility Requirement: Event occurrence must remain readable without color; preserve shape and brief timing contrast.
- Proposed Niagara Pattern: Short one-shot event pattern. Keep initialization and cleanup local to this effect.
- Proposed Material Pattern: WORLDART_INPUT_REQUIRED. No production material is selected in this gate.
- Potential Mesh/Texture Needs: None established. Reuse a simple prototype shape only for local composition if needed.
- Scalability Plan: HERO/NORMAL may add only approved secondary detail; REDUCED/MASS_COMBAT retain event occurrence and location.
- Density Risk: Competing hit cues can obscure actors; remove secondary detail first.
- Performance Risk: Burst count, translucent coverage, and concurrent impacts require profiling.
- Known Missing Inputs: Exact-SHA runtime evidence for the current cue path; general player-target cue; contact point/normal; approved relationship language.
- Implementation Boundary: VFX consumes the hit outcome. It does not choose damage, hit detection, target, or gameplay severity.
- Readiness: READY_FOR_LOCAL_LOOKDEV; READY_FOR_UE_IMPLEMENTATION_PENDING_AUTHORITY after exact-SHA runtime verification of the current cue path, bounded to the inspected NPC hit path.
