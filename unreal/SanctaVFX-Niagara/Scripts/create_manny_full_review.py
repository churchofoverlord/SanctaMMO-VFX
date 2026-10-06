"""Prepare the full catalog in a separate local map; leave the 21-case map intact."""
import hashlib, pathlib, shutil, unreal as u
R=pathlib.Path(u.Paths.project_dir())
# Preserve the exact fixture used by earlier unchanged cases. A new catalog
# can change one attachment without erasing evidence for the remaining cases.
old=R/'Content/Sancta/VFX/MannyLab/L_MannyFullReview.umap'
if old.exists():
    digest=hashlib.sha256(old.read_bytes()).hexdigest()
    archive=R/'Saved/MannyFullMapArchive';archive.mkdir(parents=True,exist_ok=True)
    snapshot=archive/(digest+'.umap')
    if not snapshot.exists():shutil.copy2(old,snapshot)
source=(R/'Scripts/create_manny_review.py').read_text(encoding='utf-8-sig')
assert source.count("'/Game/Sancta/VFX/MannyLab/L_MannyReview'")==1
assert source.count("'Evidence/gameplay-manny-cases.json'")==1
source=source.replace("'/Game/Sancta/VFX/MannyLab/L_MannyReview'","'/Game/Sancta/VFX/MannyLab/L_MannyFullReview'")
source=source.replace("'Evidence/gameplay-manny-cases.json'","'Evidence/gameplay-manny-full-cases.json'")
exec(compile(source,'full_manny_map','exec'))
