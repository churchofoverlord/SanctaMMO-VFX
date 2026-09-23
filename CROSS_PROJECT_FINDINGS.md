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

No cross-project finding is opened by Foundation V1. Missing slice semantics are recorded as deferred inputs in VFX_VSLICE_001.md until an authorized slice task decides whether to open a targeted handoff.
