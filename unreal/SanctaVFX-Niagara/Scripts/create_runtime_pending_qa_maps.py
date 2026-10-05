"""Save pending captures and QA maps in one sequential UE commandlet."""
import os,pathlib
import unreal as u
root=pathlib.Path(u.Paths.project_dir())
os.environ['SANCTA_RUNTIME_VIEWER']='0'
code=(root/'Scripts/create_runtime_review.py').read_text(encoding='utf-8').replace('u.SystemLibrary.quit_editor()','')
for label,case_file in [('','runtime-review-cases.json'),('Quality','runtime-quality-cases.json'),('Control','runtime-control-cases.json'),('Performance','runtime-performance-cases.json')]:
    os.environ['SANCTA_RUNTIME_REVIEW_MAP']='/Game/Sancta/VFX/Review/L_Runtime'+label+'Audit'
    os.environ['SANCTA_RUNTIME_CASE_FILE']='Evidence/'+case_file
    exec(compile(code,'create_runtime_review.py','exec'),{'__name__':'__main__'})
for key in ['SANCTA_RUNTIME_VIEWER','SANCTA_RUNTIME_REVIEW_MAP','SANCTA_RUNTIME_CASE_FILE']:os.environ.pop(key,None)
u.log('SanctaRuntime pending capture, quality, control and performance maps saved')
