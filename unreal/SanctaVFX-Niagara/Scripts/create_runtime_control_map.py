import os,pathlib
import unreal as u
root=pathlib.Path(u.Paths.project_dir())
os.environ['SANCTA_RUNTIME_REVIEW_MAP']='/Game/Sancta/VFX/Review/L_RuntimeControlAudit'
os.environ['SANCTA_RUNTIME_CASE_FILE']='Evidence/runtime-control-cases.json'
exec(compile((root/'Scripts/create_runtime_review.py').read_text(encoding='utf-8'),'create_runtime_review.py','exec'))
