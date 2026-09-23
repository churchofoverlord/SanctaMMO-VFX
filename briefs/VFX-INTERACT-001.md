# VFX-INTERACT-001 — Interaction feedback

## Purpose

Validate bounded feedback for a real manual processing request and its owner result. This binding covers submission only, not production progress or completion.

## Source Binding

- VFX_ID: VFX-INTERACT-001
- Source Repository: SanctaMMO-Foundation-5.8; read-only local checkout C:\Dev\SanctaMMO-SKILL-001
- Source Revision: 2cd9457349379106516b9785f0a19230a85c6342
- Source Path: Source/SanctaMMO/Private/Game/SanctaPlayerController.cpp; Source/SanctaMMO/Private/Game/SanctaGameMode.cpp; Source/SanctaMMO/Public/Economy/SanctaProcessingStation.h; Source/SanctaMMO/Private/Economy/SanctaProcessingStation.cpp
- Semantic/Game/System ID: Phase3P manual processing; Station.Tailoring.HideProcessing; Recipe.Tailoring.HideProcessing.G1 (development fixture identity)
- Source Status: SOURCE_STABLE and TECHNICALLY_PROVEN at the exact runtime SHA. The evidence record is Docs/PHASE3P_MANUAL_PROCESSING_INTERACTION.md at aee025b6c2089c88f6006c1aa6051b7a59ea2e38 and identifies runtime implementation commit 2cd9457349379106516b9785f0a19230a85c6342. It records 94/94 multiplayer harness checks, 13/13 durable-admission checks, one accepted request and owner-only result; the order remained Queued. FORMALLY_ACCEPTED=NO; CANONICAL=NO.
- Runtime Event / Entry Point: Local processing request selects a replicated operational station, sends StationInstanceId and feedback sequence to the owning server RPC, and receives Pending/Accepted/Rejected/ResultUnknown feedback.
- Available Runtime Parameters: StationInstanceId and transform; local requester; request feedback sequence; owner-only result state; the server validates character, station, range, profession, and recipe.
- Missing Parameters: No progress or production completion lifecycle in this source. The client response does not echo StationInstanceId; the requesting client must retain its request target to associate the result.
- Lifecycle: Key press/request → server validation and submission → pending → accepted or rejected/unknown result. The accepted order remains Queued; no processing progress, cancel, or completion is proven.
- Replication / Authority Notes: Station identity and transform replicate. The server owns admission. Request outcome is returned only to the requesting owner.
- Presentation Hook Candidate: RequestNearestProcessingStation and ClientPhase3ProcessingResult, correlated by FeedbackSequence while retaining the selected StationInstanceId locally.
- Why This Source Was Selected: It is a real owning-client interaction with a specific world target and a server result, while keeping unimplemented processing timing out of scope.

## Production Brief

- Gameplay Meaning: A request was sent to a processing station and received an owner result. Accepted means queue admission, not that processing started or completed.
- Presentation Inputs: Local request start, target station, and the actual owner result (`Pending`, `Accepted`, `Rejected`, or `ResultUnknown`). No production progress or completion event is available.
- Viewer Priority: Local requester and target station; keep feedback associated with the station.
- Source/Target Context: Player Controller submits the request to a ProcessingStation actor identified by StationInstanceId.
- Friendly/Hostile Requirement: Not applicable; this is a non-combat interaction.
- Cast Phase: Not applicable.
- Travel Phase: Not applicable.
- Pre-impact Phase: Not applicable.
- Impact Phase: Not applicable.
- Persistent Phase: None. Request feedback is short-lived and owner-only.
- Termination: End the pending station cue when the owner result arrives. Give each result a short visual-only envelope; no timeout, retry, or queue duration is invented. Do not show production completion for a Queued order.
- Readability Goal: Distinguish pending, queue-admitted, rejected, and unknown results by shape and motion as well as value. Do not depict production progress or completion.
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
- Readiness: PROTOTYPE_LOCAL_TEMPLATE_SEED; visual/graph review OPEN; owner result and station/request correlation are not bound to the asset.

## Isolated design / prototype readiness

- Name / Domain: Manual Processing request/result / Interaction.
- Readability Role / Importance: Supplement the owner-facing result with a spatial cue at the selected station. UI remains responsible for text and authoritative explanation.
- Self / Ally / Enemy: Owner-only request feedback; combat relationships do not apply.
- Silhouette: Pending is an open station bracket; accepted queue admission closes/tightens the bracket without a success burst; rejection breaks it; unknown remains hollow/incomplete and distinct from rejection.
- Motion: One compact transition at the real result. Any pulse/fade envelope is `LOOKDEV_ONLY — NOT GAMEPLAY AUTHORITY`; pending animation must not look like a progress bar or countdown.
- Timing / Events: Show pending only after the real request is sent; map only the real owner result. The station ID must be retained locally for correlation. No crafting/processing completion phase exists in this source.
- OPEN / Must Not Assume: Production progress, completion, cancel, queue timing, new station behavior, or a station-ID echo from the server.
- Architecture: Follow `NS_VFX_INTERACT_001_ProcessingFeedback` and the shared module/material decisions in [VFX_VSLICE_001_DESIGN_SPEC_V1.md](../VFX_VSLICE_001_DESIGN_SPEC_V1.md). Do not turn this first use into a general interaction framework.

## Isolated UE prototype seed

- Asset: `/Game/VFX/Interaction/NS_VFX_INTERACT_001_Result` in `UEVFXSandbox/SanctaMMO_VFXSandbox.uproject`.
- Basis: stock UE 5.8.2 `DirectionalBurstLightweight` system duplicated without graph changes.
- State: loadable `NiagaraSystem`; not connected to the owner result. It does not encode request correlation, Pending, Accepted/Queued, Rejected, or ResultUnknown, and has no progress/completion behavior. The static station bracket remains unimplemented in Niagara.
- Use: local one-shot template inspection only. No order or station logic is present; triggers are `LOOKDEV_ONLY — NOT GAMEPLAY AUTHORITY`.
