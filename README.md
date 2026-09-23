# SanctaMMO VFX Foundation V1

Status: LOCAL FOUNDATION; not integrated, not formally accepted, no production effects created.

This repository defines a small operating and design baseline for SanctaMMO VFX. It supports later authorized VFX design and implementation while keeping gameplay meaning, WorldArt authority, and Unreal integration boundaries explicit.

## Workspace

- Repository type: local Git checkout with configured GitHub remote `origin` (`churchofoverlord/SanctaMMO-VFX`).
- Branch: main.
- The VFX foundation and source-binding history is published on `origin/main`; current work remains VFX-only and is not Unreal-integrated.

## Read-only baseline

Evidence labels are scoped to what was actually inspected. An asset name or file presence does not prove the asset graph, runtime behavior, visual approval, or production suitability.

| Source | Revision / evidence | Finding |
|---|---|---|
| SanctaMMO-Repo | committed local main at 404f39ad798eb935273ccc95fc1982cf4ad72ae0; clean at inspection | Unreal project descriptor, source, Config, and Content names inspected read-only. No VFX semantic contract was selected for the slice. |
| Installed Unreal Engine | Engine/Build/Build.version reports 5.8.2, changelist 56702186 | Niagara plugin descriptor exists under Engine/Plugins/FX/Niagara and is EnabledByDefault. This proves local engine installation evidence, not that the project was opened or cooked with that engine. |
| SanctaMMO.uproject | EngineAssociation is {879D9D6C-4F90-4BD2-533F-CD9F03C78B21}; project lists VisualStudioTools only | The association GUID was not mapped to an engine install. Exact project-to-engine version remains OPEN. |
| SanctaMMO-Repo Content | NS_JumpPad.uasset and nearby M_SimpleGlow, M_GradientGlow, MI_GlowNT names observed | Asset type, Niagara graph, material connections, use, and acceptance were not inspected. These are OBSERVED only, not a VFX direction. |
| SanctaMMO-WorldArt | committed local main at a6b3be7fe42d5cd6c6820efda5ae3c04d4acff7f; clean at inspection | Stable local WorldArt rules constrain compatibility. See the source paths below. |
| SanctaMMO-Control | C:\Dev\SanctaMMO-Control\ORACLE_OPERATING_PROFILE.md at local master 1b39164c80354ba3060c3addee98030ebd411585 | Consulted read-only only for transversal evidence, review, concurrency, and integration discipline. |

WorldArt inputs used:

- CANON/WORLD_ART_BIBLE.md
- CANON/MATERIAL_LANGUAGE.md
- CANON/VISUAL_DETAIL_STANDARD.md

## Foundation documents

- VFX_OPERATING_PROFILE.md defines scope, boundaries, evidence, local versus canonical work, and gates.
- VFX_TAXONOMY.md defines production domains and ID prefixes.
- VFX_BIBLE.md defines readable effect structure, accessibility, scalability intent, and WorldArt compatibility.
- NIAGARA_ARCHITECTURE.md defines reusable patterns and the minimum material strategy.
- VFX_PERFORMANCE.md defines profiling scenarios and evidence to collect; it sets no numeric budgets.
- VFX_REGISTRY.csv tracks only the five VSLICE_001 items.
- VFX_VSLICE_001.md records the source bindings and current gate state.
- VFX_VSLICE_001_DESIGN_SPEC_V1.md records isolated design, prototype architecture, scalability, readability, evidence, and open inputs.
- lookdev/VFX_VSLICE_001_LOOKDEV_V1.html is a local, non-semantic vector blockout for the four source-bound items; it is not a Niagara prototype.
- VFX_VSLICE_001_REVIEW.md records the source-binding review and exact target SHA.
- briefs/ contains one source-bound production brief per selected VFX item and the deferred area-warning brief.
- CROSS_PROJECT_FINDINGS.md records the two bounded presentation-hook findings opened by VSLICE_001.

## Current evidence state

- OBSERVED: committed Unreal source snapshot and named assets at the revision above; this VFX workspace contains no isolated `.uproject` sandbox.
- TECHNICALLY_PROVEN: the installed UE 5.8.2 directory contains the Niagara plugin descriptor and the reported build version.
- TECHNICALLY_PROVEN: VFX source-binding review passed at its recorded SHA; the selected processing request/result was proven at its exact runtime SHA.
- OBSERVED: the standalone HTML lookdev is a vector mockup only; no VFX Niagara prototype has been created.
- OPEN / DEFERRED_SOURCE: project-to-engine association, an isolated VFX sandbox, Niagara module/asset behavior in a target project, current combat-cue and projectile runtime validation, client-visible Slow state, approved relationship treatment, and any permanent production VFX direction.
- FORMALLY_ACCEPTED: none of the VFX Foundation documents or VSLICE_001 items. Existing WorldArt statements remain scoped to their own source authority and are not VFX acceptance.

Next gate: visual readability review of the local blockout. The isolated UE sandbox remains OPEN and the main Unreal project remains out of scope.
