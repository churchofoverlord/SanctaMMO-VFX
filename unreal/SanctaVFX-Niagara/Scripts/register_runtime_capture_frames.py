"""Accept only completed direct game-viewport frames from the current build."""
import pathlib,json,hashlib,argparse,datetime,re
from PIL import Image
from runtime_capture_signatures import CaptureSignatures
root=pathlib.Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--log',required=True);parser.add_argument('--case-file',required=True);parser.add_argument('--profile',default='Default');args=parser.parse_args()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
context={'jobs':sha(root/'Evidence/gameplay-runtime-build-jobs.json'),'runtime':sha(root/'Plugins/SanctaVFXBridge/Binaries/Win64/UnrealEditor-SanctaVFXRuntime.dll'),'bridge':sha(root/'Plugins/SanctaVFXBridge/Binaries/Win64/UnrealEditor-SanctaVFXBridge.dll')}
path=root/'Evidence/gameplay-runtime-capture-frames.json'
previous=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
signatures=CaptureSignatures(root)
frames={name:row for name,row in previous.get('frames',{}).items() if signatures.valid(row)} if previous.get('render_context')==signatures.render_context else {}
current=json.loads((root/'Saved/RuntimeCaptures/capture-frames.json').read_text(encoding='utf-8-sig'))
log=(root/args.log).read_text(encoding='utf-8-sig',errors='replace')
logged={name:(int(particles),int(active)) for name,particles,active in re.findall(r'capture: ([\w.-]+)\.png saved=1 particles=(\d+) active=(\d+)',log)}
if not current or len({row['case'] for row in current})!=len(current):raise RuntimeError('Empty or duplicate capture metadata')
if args.case_file:
    expected=json.loads((root/args.case_file).read_text(encoding='utf-8-sig'))
    if {row['name'] for row in expected}!={row['case'] for row in current}:raise RuntimeError('Capture batch is incomplete or belongs to a different case plan')
by_name={row['name']:row for row in expected}
for row in current:
    file=root/'Saved/RuntimeCaptures'/(row['case']+'.png')
    if not row['saved'] or row['viewport']!='Owning PIE world GameViewport':raise RuntimeError('Invalid capture '+row['case'])
    if logged.get(row['case'])!=(row['particles'],row['active_components']):raise RuntimeError('Capture metadata is absent from this run log: '+row['case'])
    with Image.open(file) as picture:
        if picture.size!=(row['width'],row['height']):raise RuntimeError('Viewport size differs from PNG')
        picture.verify()
    case=by_name[row['case']]
    frames[row['case']]={**row,'file':file.relative_to(root).as_posix(),'sha256':sha(file),'run_log':args.log,'capture_input':case,'profile':args.profile,'component_signature':signatures.signature(case,args.profile)}
report={'context':context,'render_context':signatures.render_context,'frames':frames,'updated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Direct owning-PIE viewport readback. Exact PNG, input, selected-phase, material/mesh/texture and build hashes; changing one component invalidates that component. Visual quality is reviewed separately.'}
path.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'accepted_frames':len(frames),'current_run':len(current)}))
