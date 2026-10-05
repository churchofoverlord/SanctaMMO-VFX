"""Verify exact accepted PNG pairs for quality or control snapshots."""
import argparse,hashlib,json,pathlib
from PIL import Image,ImageChops,ImageDraw
from runtime_capture_signatures import CaptureSignatures
root=pathlib.Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--cases',required=True);parser.add_argument('--report',required=True);parser.add_argument('--label',required=True);args=parser.parse_args()
plan=json.loads((root/args.cases).read_text(encoding='utf-8-sig'))
registry=json.loads((root/'Evidence/gameplay-runtime-capture-frames.json').read_text(encoding='utf-8-sig'))
frames=registry['frames'];sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
signatures=CaptureSignatures(root)
if registry.get('render_context')!=signatures.render_context:raise RuntimeError('Capture renderer changed')
for case in plan:
    frame=frames.get(case['name'],{})
    if frame.get('component_signature')!=signatures.signature(case,frame.get('profile','Default')):raise RuntimeError('Capture inputs changed: '+case['name'])
rows=[]
for case in plan:
    name=case['name']
    if name.endswith('_baseline'):continue
    baseline_name=name+'_baseline' if name+'_baseline' in frames else name.rsplit('_',1)[0]+'_baseline'
    picture_path=root/frames[name]['file'];baseline_path=root/frames[baseline_name]['file']
    for path,key in [(picture_path,name),(baseline_path,baseline_name)]:
        if sha(path)!=frames[key]['sha256']:raise RuntimeError('Accepted image changed: '+key)
    picture=Image.open(picture_path).convert('RGB');baseline=Image.open(baseline_path).convert('RGB')
    channels=ImageChops.difference(picture,baseline).split()
    histogram=ImageChops.lighter(ImageChops.lighter(channels[0],channels[1]),channels[2]).histogram()
    rows.append({'name':name,'file':frames[name]['file'],'sha256':frames[name]['sha256'],'baseline':frames[baseline_name]['file'],'baseline_sha256':frames[baseline_name]['sha256'],'changed_pixels_over_12':sum(histogram[13:]),'max_channel_delta':max(index for index,count in enumerate(histogram) if count),'input':case,'visual_review':'pending'})
report={'scope':'Paired, hash-verified native snapshots. Empty resources can intentionally have no visible crystals; pixel presence does not certify final art or shipping budgets.','capture_context':registry['context'],'cases':len(plan),'sample_count':len(rows),'rows':rows,'manual_visual_review':'pending'}
(root/args.report).write_text(json.dumps(report,indent=2),encoding='utf-8')
out=root/'Evidence/RuntimeReview';out.mkdir(exist_ok=True)
for offset in range(0,len(rows),12):
    sheet=Image.new('RGB',(1280,1000),(24,28,34));draw=ImageDraw.Draw(sheet)
    for index,row in enumerate(rows[offset:offset+12]):
        picture=Image.open(root/row['file']).convert('RGB');picture.thumbnail((420,224));x=index%3*426;y=index//3*250
        sheet.paste(picture,(x,y+24));draw.text((x+6,y+5),row['name'],fill=(235,240,245))
    sheet.save(out/(args.label+'_'+str(offset//12+1).zfill(3)+'.png'))
print(json.dumps({'cases':len(plan),'sample_count':len(rows),'low_delta_samples':[row['name'] for row in rows if row['changed_pixels_over_12']<6]}))
