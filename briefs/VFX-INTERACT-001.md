# VFX-INTERACT-001 — Interaction feedback

## Purpose

Validate bounded feedback for a real manual processing request and its owner result. This binding covers submission only, not production progress or completion.

## Source Binding

- VFX_ID: VFX-INTERACT-001
- Source Repository: SanctaMMO-Foundation-5.8; read-only local checkout C:\Dev\SanctaMMO-SKILL-001
- Source Revision: 2cd9457349379106516b9785f0a19230a85c6342
- Source Path: Source/SanctaMMO/Private/Game/SanctaPlayerController.cpp; Source/SanctaMMO/Private/Game/SanctaGameMode.cpp; Source/SanctaMMO/Public/Economy/SanctaProcessingStation.h; Source/SanctaMMO/Private/Economy/SanctaProcessingStation.cpp; Docs/PHASE3P_MANUAL_PROCESSING_INTERACTION.md
- Semantic/Game/System ID: Phase3P manual processing; Station.Tailoring.HideProcessing; Recipe.Tailoring.HideProcessing.G1 (development fixture identity)
- Source Status: SOURCE_STABLE and TECHNICALLY_PROVEN at the exact runtime SHA. Recorded evidence: 94/94 multiplayer harness checks, 13/13 durable-admission checks, one accepted request and owner-only result; the order remained Queued. FORMALLY_ACCEPTED=NO; CANONICAL=NO.
- Runtime Event / Entry Point: Local processing request selects a replicated operational station, sends StationInstanceId and feedback sequence to the owning server RPC, and receives Pending/Accepted/Rejected/ResultUnknown feedback.
- Available Runtime Parameters: StationInstanceId and transform; local requester; request feedback sequence; owner-only result state; the server validates character, station, range, profession, and recipe.
- Missing Parameters: No progress or production completion lifecycle in this source. The client response does not echo StationInstanceId; the requesting client must retain its request target to associate the result.
- Lifecycle: Key press/request → server validation and submission → pending → accepted or rejected/unknown result. The accepted order remains Queued; no processing progress, cancel, or completion is proven.
- Replication / Authority Notes: Station identity and transform replicate. The server owns admission. Request outcome is returned only to the requesting owner.
- Presentation Hook Candidate: RequestNearestProcessingStation and ClientPhase3ProcessingResult, correlated by FeedbackSequence while retaining the selected StationInstanceId locally.
- Why This Source Was Selected: It is a real owning-client interaction with a specific world target and a server result, while keeping unimplemented processing timing out of scope.

## Production Brief

- Gameplay Meaning: A request was sent to a processing station and received a server result. Accepted means the order was queued, not that processing completed.
- Presentation Inputs: Local request start, target station, and owner result state. No progress percentage or completion event is available.
- Viewer Priority: Local requester and target station; keep feedback associated with the station.
- Source/Target Context: Player Controller submits the request to a ProcessingStation actor identified by StationInstanceId.
- Friendly/Hostile Requirement: Not applicable; this is a non-combat interaction.
- Cast Phase: Not applicable.
- Travel Phase: Not applicable.
- Pre-impact Phase: Not applicable.
- Impact Phase: Not applicable.
- Persistent Phase: None. Request feedback is short-lived and owner-only.
- Termination: End request cue on server result. Do not show a production completion effect for a Queued order.
- Readability Goal: Distinguish request pending from accepted and rejected/unknown without depending on color.
- Shape/Motion Intent: A compact station-associated pulse or state change. WORLDART_INPUT_REQUIRED for final palette/material treatment; do not redraw station identity.
- Accessibility Requirement: Use shape, placement, or timing in addition to color.
- Proposed Niagara Pattern: Short request/result event pattern, locally associated with the station and requester.
- Proposed Material Pattern: WORLDART_INPUT_REQUIRED. No production material is selected in this gate.
- Potential Mesh/Texture Needs: None established.
- Scalability Plan: Keep one compact cue per request/result; suppress ornament at REDUCED and MASS_COMBAT.
- Density Risk: Multiple nearby requests can compete; correlate each result to its request before displaying.
- Performance Risk: Repeated request cues are low-to-medium risk; avoid unnecessary persistent components.
- Known Missing Inputs: Dedicated VFX event/delegate and station ID in owner response; processing progress/completion does not exist in this binding.
- Implementation Boundary: VFX does not create orders, change station rules, or imply production completion.
- Readiness: READY_FOR_LOCAL_LOOKDEV; READY_FOR_UE_IMPLEMENTATION_PENDING_AUTHORITY for request/result only.
