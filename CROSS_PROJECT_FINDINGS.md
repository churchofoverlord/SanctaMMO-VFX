# Cross-Project Finding Handoff

Use this record when VFX needs an input, clarification, or change owned by another domain. The VFX Project does not resolve a finding by writing into that domain.

## Required fields

- CROSS_PROJECT_FINDING_ID: local tracking ID, such as CF-VFX-0001.
- Source_VFX_ID: relevant registry item, or NONE for a system-level question.
- Target_Domain: GAMEPLAY, WORLDART, BLENDER, UI, AUDIO, CANON, or OTHER.
- Observed_Constraint: precise fact and source revision/path.
- Required_Input_or_Change: smallest input or decision needed.
- Evidence: file, revision, capture, or event contract supporting the finding.
- Blocking: YES or NO for the named VFX task.
- Reason: impact of the missing input and the next safe action.

## Record template

CROSS_PROJECT_FINDING_ID:
Source_VFX_ID:
Target_Domain:
Observed_Constraint:
Required_Input_or_Change:
Evidence:
Blocking: YES/NO
Reason:

Foundation V1 opened no cross-project findings. VFX_VSLICE_001 opens the two evidence-backed findings below; other missing semantics remain deferred until a relevant authorized slice needs them.

## CF-VFX-0001

CROSS_PROJECT_FINDING_ID: CF-VFX-0001
Source_VFX_ID: VFX-SKILL-002
Target_Domain: GAMEPLAY
Observed_Constraint: At SanctaMMO-Foundation-5.8 revision 9a09ac6769db9d8e3a87f50eb4f8231b60a810ff, Phase2.GroundArea.IFV validates and resolves a ground-area action at execution. Its recorded runtime evidence does not expose a pre-impact warning lifecycle. At b5cf12a64ffd971b195c0d6406d6ed1c93326916, fighter.crushing_1 emits an impact-area cue after selecting its authoritative center and radius. Neither source supplies an authoritative telegraph start/end contract for this VFX item.
Required_Input_or_Change: If an existing runtime ability already has a pre-impact warning, expose its existing authoritative footprint, position/orientation, and active lifecycle through a bounded presentation hook. Do not add a cast time, warning duration, radius, shape, or gameplay rule.
Evidence: Docs/PHASE2K_GROUND_AREA_ABILITY.md at 3fd284b443474b7563a13482151fce82d5df489d (the document identifies runtime commit 9a09ac6769db9d8e3a87f50eb4f8231b60a810ff); Source/SanctaMMO/Private/Combat/SanctaCombatComponent.cpp and Source/SanctaMMO/Private/Skills/SanctaPresentationCue.cpp at b5cf12a64ffd971b195c0d6406d6ed1c93326916.
Blocking: YES for telegraph implementation; NO for local lookdev.
Classification: BLOCKING_IMPLEMENTATION; NON_BLOCKING_LOOKDEV.
Reason: Without a real pre-impact source, a Niagara telegraph would invent a warning and might misstate gameplay. The generic pattern can still be composed with preview-only controls.

## CF-VFX-0002

CROSS_PROJECT_FINDING_ID: CF-VFX-0002
Source_VFX_ID: VFX-CHARACTER-001
Target_Domain: GAMEPLAY
Observed_Constraint: At SanctaMMO-Foundation-5.8 revision b5cf12a64ffd971b195c0d6406d6ed1c93326916, USanctaAttributeComponent owns the active status set on the server and applies/removes/clears it. The status set is not among the replicated properties. A short-lived SlowOutcome cue can be emitted on application, but it does not carry the authoritative status expiry/termination lifecycle.
Required_Input_or_Change: Provide a bounded client presentation hook or replicated read-only status view for the existing status identity and active/inactive lifecycle, affected actor, and source context where appropriate. Keep status authority, duration, application rules, and gameplay behavior unchanged.
Evidence: Source/SanctaMMO/Public/Combat/SanctaAttributeComponent.h; Source/SanctaMMO/Private/Combat/SanctaAttributeComponent.cpp; Source/SanctaMMO/Public/Combat/SanctaStatusEffectModel.h; Source/SanctaMMO/Private/Skills/SanctaCombatReceiver.cpp at b5cf12a64ffd971b195c0d6406d6ed1c93326916. The earlier deterministic model evidence at bb3f39b3e2cf043cf695a73b342a0834519db86d does not prove live client replication.
Blocking: YES for a persistent state visual; NO for local lookdev.
Classification: BLOCKING_IMPLEMENTATION; NON_BLOCKING_LOOKDEV.
Reason: A replicated application cue alone cannot keep a loop aligned with actual activation and cleanup. Exposing existing state is sufficient; no gameplay-semantic change is requested.
