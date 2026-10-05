"""Resume the current immutable plan, retaining only complete PNGs."""
import pathlib, json, hashlib
from PIL import Image
from runtime_capture_signatures import CaptureSignatures
root = pathlib.Path(__file__).resolve().parents[1]
plan = root/'Evidence/runtime-review-cases.json'
full = root/'Evidence/runtime-capture-plan.json'
if not full.exists():
    full.write_bytes(plan.read_bytes())
cases = json.loads(full.read_text(encoding='utf-8'))
accepted_path=root/'Evidence/gameplay-runtime-capture-frames.json'
registry=json.loads(accepted_path.read_text(encoding='utf-8')) if accepted_path.exists() else {}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
context={'jobs':sha(root/'Evidence/gameplay-runtime-build-jobs.json'),'runtime':sha(root/'Plugins/SanctaVFXBridge/Binaries/Win64/UnrealEditor-SanctaVFXRuntime.dll'),'bridge':sha(root/'Plugins/SanctaVFXBridge/Binaries/Win64/UnrealEditor-SanctaVFXBridge.dll')}
signatures=CaptureSignatures(root)
accepted=registry.get('frames',{}) if registry.get('render_context')==signatures.render_context else {}
pending = []
for case in cases:
    path = root/'Saved/RuntimeCaptures'/(case['name']+'.png')
    try:
        if case['name'] not in accepted:raise ValueError('No accepted direct viewport frame')
        if accepted[case['name']].get('component_signature')!=signatures.signature(case):raise ValueError('Inputs or selected phase dependencies changed')
        if sha(path)!=accepted[case['name']]['sha256']:raise ValueError('Accepted PNG changed')
        with Image.open(path) as picture:
            picture.verify()
    except (OSError, ValueError):
        pending.append(case)
plan.write_text(json.dumps(pending, indent=2), encoding='utf-8')
print(json.dumps({'total': len(cases), 'completed': len(cases)-len(pending), 'pending': len(pending)}))
