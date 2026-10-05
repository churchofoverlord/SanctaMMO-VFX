"""Explicit commit scope: current runtime closure and authoring dependencies, no archives/Engine."""
import pathlib,json,hashlib
root=pathlib.Path(__file__).resolve().parents[1]
read=lambda p:json.loads((root/p).read_text(encoding='utf-8-sig'))
groups={}
def add(group,path):
    path=pathlib.Path(path)
    if path.is_absolute():path=path.relative_to(root)
    if not (root/path).is_file():raise RuntimeError('Commit dependency missing: '+str(path))
    groups.setdefault(group,set()).add(path.as_posix())
for row in read('Evidence/gameplay-runtime-migration-manifest.json')['packages']:add('native_current',row['file'])
for path in read('Evidence/gameplay-runtime-compiled-sources.json')['files']:add('own_cpp',path)
for job in read('Evidence/gameplay-runtime-build-jobs.json')['jobs']:
    add('current_sources',job['source']);port=pathlib.Path(job['source']).with_suffix('.port.json');add('current_sources',port)
    for layer in read(port)['layers']:
        add('generated_import_inputs',layer['mesh_source'])
        if layer.get('attribute_texture'):add('generated_import_inputs',layer['attribute_texture']['source'])
        for uniform in layer['uniforms'].values():
            if uniform.get('texture_source'):add('generated_import_inputs',uniform['texture_source'])
add('current_sources','Source/GameplayRuntime/IcebergBody.obj')
# These are actual inputs used to author current derivatives, not previous native demonstrations.
for path in read('Evidence/gameplay-implementation-preservation-baseline.json')['current_editable_sources']:
    add('approved_authoring_inputs',path)
    port=pathlib.Path(path).with_suffix('.port.json')
    if (root/port).exists():add('approved_authoring_inputs',port)
for path in ['VFX-catalog.json','VFX-separated-components.json','VFX-reference-layers.json','VFX-native-port-report.json']:add('authoring_metadata',path)
for name in ['assess_gameplay_vfx_20261004.py','art_review_geometry.py','reference_shader_port.py','runtime_shader_bindings.py','prepare_gameplay_vfx.py','prepare_runtime_routes.py','build_gameplay_vfx.py','build_runtime_definitions.py','build_runtime_scalability.py','build_gameplay_terrain.py','validate_gameplay_runtime.py','validate_basic_routing.py','validate_runtime_materials.py','validate_runtime_complete.py','finalize_runtime_review_package.py','prepare_review_stage.py','build_reference_ports.py','build_firebolt.py','prepare_runtime_capture_batch.py','prepare_runtime_viewer.py','create_runtime_review.py','create_runtime_viewer.py','prepare_runtime_quality_cases.py','create_runtime_quality_maps.py','record_runtime_compilation.py','register_runtime_capture_frames.py','resume_runtime_capture_plan.py','audit_runtime_captures.py','save_gameplay_checkpoint.py','export_runtime_package.py','prepare_runtime_version_control.py','make_runtime_progress_sheets.py','prepare_runtime_render_diagnostic.py','Unreal-Lab.ps1','Run-LabScript.ps1','Run-RuntimeMaterialValidation.ps1','Run-RuntimeCaptures.ps1','Open-RuntimeViewer.ps1']:
    add('authoring_scripts','Scripts/'+name)
for name in ['audit_runtime_migration.py','prepare_runtime_shader_diagnostic.py','create_runtime_shader_diagnostic_map.py','audit_runtime_shader_diagnostic.py','save_runtime_capture_shutdown.py','runtime_capture_signatures.py','reconcile_runtime_materials.py','prepare_runtime_control_cases.py','create_runtime_control_map.py','create_runtime_pending_qa_maps.py','validate_runtime_result_bindings.py','audit_runtime_quality_captures.py','audit_runtime_phase_contracts.py','audit_runtime_authoring_costs.py','audit_runtime_performance.py']:
    add('authoring_scripts','Scripts/'+name)
for path in ['.gitignore','AGENTS.md','CONTINUAR.md','Config/DefaultEngine.ini','SanctaVFXLab.uproject','BuildHost/VFXBuild.uproject','Plugins/SanctaVFXBridge/SanctaVFXBridge.uplugin','VFX-status.json','Ver-Fases-Integracao.cmd','Ver-Capturas-Integracao.cmd','GUIA_EXECUCAO_VFX.md','REVISAO_INTEGRACAO_VFX_20261004.md','MATRIZ_SKILLS_VFX_20261004.md','RETOMAR_INTEGRACAO_20261004.md']:
    add('configuration_docs',path)
for name in ['L_RuntimeAudit','L_RuntimeViewer','L_RuntimeQualityAudit','L_RuntimePerformanceAudit','L_RuntimeControlAudit']:add('review_fixtures','Content/Sancta/VFX/Review/'+name+'.umap')
for name in ['M_ReviewFloor','M_ReviewBody','M_ReviewBodyGhost']:add('review_fixtures','Content/VFXLab/Review/Fixtures/'+name+'.uasset')
add('review_fixtures','Content/Sancta/VFX/Review/Common/M_RuntimeFloorBright.uasset')
body=read('Source/ReferencePorts/scout-evasion.port.json')['layers'][0]['mesh_name']
add('review_fixtures','Content/VFXLab/ReferenceShared/Meshes/'+body+'.uasset')
for path in (root/'Evidence').glob('gameplay-*.json'):
    if 'pilot' not in path.name:add('current_evidence',path)
for name in ['runtime-capture-plan.json','runtime-review-cases.json','runtime-viewer-cases.json','runtime-quality-cases.json','runtime-performance-cases.json','user-art-approvals.json','runtime-capture-interruption-20261005.json']:add('current_evidence','Evidence/'+name)
for name in ['runtime-capture-partial-shutdown-20261005.json','runtime-capture-provisional-shutdown-20261005.json','runtime-shader-diagnostic-cases.json','runtime-shader-diagnostic-result.json','runtime-control-cases.json','runtime-phase-repair-plan-20261005.json','runtime-material-bindings-before-phase-repairs.json']:add('current_evidence','Evidence/'+name)
add('review_images','Evidence/RuntimeReview/shader-ready-comparison.png')
for path in (root/'Evidence/RuntimeReview').glob('sheet_*.png'):add('review_images',path)
for row in read('Evidence/gameplay-runtime-capture-audit.json')['rows']:
    for sample in row['samples']:add('review_images',sample['gallery_preview'])
for label in ['controls','quality']:
    for path in (root/'Evidence/RuntimeReview').glob(label+'_*.png'):add('review_images',path)
add('review_images','Evidence/RuntimeReview/galeria.html')
files=sorted(set().union(*groups.values()))
report={'groups':{key:sorted(value) for key,value in groups.items()},'files':files,'file_count':len(files),'bytes':sum((root/p).stat().st_size for p in files),'excludes':['Engine sources/binaries','Foundation changes','Prior native demonstrations, historical derivatives and archives','Saved logs/captures and exported zip'],'scope':'Explicit current runtime closure plus exact authoring/review dependencies; no blanket repository staging.'}
(root/'Evidence/runtime-version-control-scope.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({key:report[key] for key in ['file_count','bytes']}))
