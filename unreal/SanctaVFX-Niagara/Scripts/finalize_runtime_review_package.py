"""Generate, verify and save review maps sequentially, without overlapping UE runs."""
import pathlib,os,unreal as u
root=pathlib.Path(u.Paths.project_dir())
os.environ['SANCTA_SKIP_MATERIAL_VALIDATION']='1'
# Material bindings run in bounded, individually verified UE processes through
# Run-RuntimeMaterialValidation.ps1; do not accumulate their transient actors here.
for name in ['build_runtime_definitions.py','validate_runtime_complete.py']:
    namespace={'__name__':'__main__'}
    exec(compile((root/'Scripts'/name).read_text(encoding='utf-8'),name,'exec'),namespace)
for interactive in [False,True]:
    os.environ['SANCTA_RUNTIME_VIEWER']='1' if interactive else '0'
    namespace={'__name__':'__main__'}
    code=(root/'Scripts/create_runtime_review.py').read_text(encoding='utf-8').replace('u.SystemLibrary.quit_editor()','')
    exec(compile(code,'create_runtime_review.py','exec'),namespace)
u.log('SanctaRuntime final package verified and review maps saved')
