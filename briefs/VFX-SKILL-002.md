# VFX-SKILL-002 — Area warning / telegraph

## Purpose

Retain the existing generic area-warning pattern until a stable source supplies an actual pre-impact lifecycle. No warning or gameplay timing is invented by this brief.

## Source Binding

- VFX_ID: VFX-SKILL-002
- Source Repository: SanctaMMO-Foundation-5.8; read-only local checkout C:\Dev\SanctaMMO-SKILL-001
- Source Revision: b5cf12a64ffd971b195c0d6406d6ed1c93326916
- Source Path: Source/SanctaMMO/Private/Game/SanctaPlayerController.cpp; Source/SanctaMMO/Private/Combat/SanctaCombatComponent.cpp; Source/SanctaMMO/Private/Skills/SanctaPresentationCue.cpp
- Semantic/Game/System ID: Candidate only: Phase2.GroundArea.IFV and fighter.crushing_1. Neither is a bound warning source.
- Source Status: SOURCE_DEFERRED. Phase2 ground-area resolution was runtime-proven at 9a09ac6769db9d8e3a87f50eb4f8231b60a810ff, but that evidence proves execution/impact only. FORMALLY_ACCEPTED=NO; CANONICAL=NO.
- Runtime Event / Entry Point: Phase2.GroundArea.IFV submits a ground point for authoritative validation and resolution. fighter.crushing_1 emits an impact-area cue after choosing its runtime center and radius.
- Available Runtime Parameters: Candidate impact center and circular radius at resolution; replicated impact cue location/radius on the inspected current code path.
- Missing Parameters: A pre-impact warning start event, active deadline/window, warning termination, and any source-specific warning shape/orientation contract.
- Lifecycle: Candidate sources resolve area effects at execution. No usable warning lifecycle is bound.
- Replication / Authority Notes: Server owns area validation and resolution. The impact cue does not establish a telegraph or gameplay duration.
- Presentation Hook Candidate: None suitable for a production telegraph yet. A future hook may expose an already-authoritative warning if a selected runtime ability has one.
- Why This Source Was Not Selected: An impact footprint is not a warning. The other observed NPC warning candidate does not expose the complete authoritative footprint/timing contract required here.

## Production Brief

- Gameplay Meaning: Generic pattern only; it may eventually communicate the actual supplied spatial warning and its active interval.
- Presentation Inputs: Placeholder-only during local lookdev. Production requires authoritative shape, position/orientation, dimensions, active start, and termination.
- Viewer Priority: Gameplay-critical warning if and when bound; its primary boundary must survive reduced effects.
- Source/Target Context: No production target or spatial ability is selected.
- Friendly/Hostile Requirement: OPEN. Do not encode relationship or danger class from an unbound source.
- Cast Phase: No cast or warning phase is established by current candidates.
- Travel Phase: None.
- Pre-impact Phase: DEFERRED_GAMEPLAY_INPUT. Do not invent onset or warning duration.
- Impact Phase: Candidate area sources provide impact resolution only; they do not authorize a telegraph.
- Persistent Phase: None.
- Termination: Must follow a future authoritative warning end/cancel event; visual fade cannot extend it.
- Readability Goal: Future supplied shape and active timing must be readable without color alone.
- Shape/Motion Intent: Preview only. If a future source supplies a circular footprint, keep the preview within that supplied shape. WORLDART_INPUT_REQUIRED for final treatment.
- Accessibility Requirement: Future critical warning needs shape, edge, placement, and timing cues; never color only or fast flicker only.
- Proposed Niagara Pattern: Parameterized footprint candidate, but do not produce Niagara until bound to an actual warning lifecycle.
- Proposed Material Pattern: WORLDART_INPUT_REQUIRED. No production material is selected in this gate.
- Potential Mesh/Texture Needs: None established.
- Scalability Plan: Local preview only; future implementation must preserve authoritative footprint and warning interval at all tiers.
- Density Risk: Overlapping warnings can hide actors and each other.
- Performance Risk: Area fill overdraw and overlapping boundaries require later measurement.
- Known Missing Inputs: An actual stable pre-impact warning source and client-visible lifecycle.
- Implementation Boundary: No radius, shape, cast time, warning time, target, or gameplay effect is invented.
- Readiness: READY_FOR_LOCAL_LOOKDEV; DEFERRED_GAMEPLAY_INPUT.
