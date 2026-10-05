import os,pathlib,unreal as u
R=pathlib.Path(u.Paths.project_dir())
os.environ['SANCTA_RUNTIME_VIEWER']='1'
exec(compile((R/'Scripts/create_runtime_review.py').read_text(encoding='utf-8'),'create_runtime_viewer.py','exec'))
