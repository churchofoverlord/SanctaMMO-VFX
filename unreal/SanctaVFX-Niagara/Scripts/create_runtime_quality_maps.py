import unreal as u,pathlib,os
root=pathlib.Path(u.Paths.project_dir())
for label,case_file in [('Quality','runtime-quality-cases.json'),('Performance','runtime-performance-cases.json')]:
    os.environ['SANCTA_RUNTIME_REVIEW_MAP']='/Game/Sancta/VFX/Review/L_Runtime'+label+'Audit'
    os.environ['SANCTA_RUNTIME_CASE_FILE']='Evidence/'+case_file
    code=(root/'Scripts/create_runtime_review.py').read_text(encoding='utf-8').replace('u.SystemLibrary.quit_editor()','')
    exec(compile(code,'create_runtime_review.py','exec'),{'__name__':'__main__'})
os.environ.pop('SANCTA_RUNTIME_REVIEW_MAP',None)
os.environ.pop('SANCTA_RUNTIME_CASE_FILE',None)
u.log('SanctaRuntime quality and performance maps saved')
