"""Temporary review sheets from this run's successful capture log, never acceptance evidence."""
import pathlib,json,re,argparse
from PIL import Image,ImageDraw,ImageChops
root=pathlib.Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--log',required=True);parser.add_argument('--report');args=parser.parse_args()
log=(root/args.log).read_text(encoding='utf-8-sig',errors='replace')
names=set(re.findall(r'capture: (All_\w+)\.png saved=1',log))
jobs=json.loads((root/'Evidence/gameplay-runtime-build-jobs.json').read_text(encoding='utf-8'))['jobs']
planned=json.loads((root/'Evidence/runtime-capture-plan.json').read_text(encoding='utf-8'))
rows=[];flags=[]
for job in jobs:
    matches=sorted(name for name in names if re.fullmatch('All_'+re.escape(job['slug'])+r'_\d',name))
    if not matches:continue
    representative=matches[-1]
    baseline='All_'+job['slug']+'_baseline'
    if baseline in names:
        original=Image.open(root/'Saved/RuntimeCaptures'/(baseline+'.png')).convert('RGB')
        counts=[]
        for name in matches:
            picture=Image.open(root/'Saved/RuntimeCaptures'/(name+'.png')).convert('RGB')
            channels=ImageChops.difference(original,picture).split()
            histogram=ImageChops.lighter(ImageChops.lighter(channels[0],channels[1]),channels[2]).histogram()
            counts.append(sum(histogram[13:]))
        expected=sum(bool(re.fullmatch('All_'+re.escape(job['slug'])+r'_\d',case['name'])) for case in planned)
        if len(matches)==expected and max(counts)<6:flags.append(job['slug'])
        representative=matches[max(range(len(counts)),key=lambda index:counts[index])]
    rows.append((job['slug'],representative))
out=root/'Saved/RuntimeCaptures/Progress';out.mkdir(exist_ok=True)
for offset in range(0,len(rows),12):
    sheet=Image.new('RGB',(1280,1000),(24,28,34));draw=ImageDraw.Draw(sheet)
    for index,(slug,name) in enumerate(rows[offset:offset+12]):
        pic=Image.open(root/'Saved/RuntimeCaptures'/(name+'.png')).convert('RGB');pic.thumbnail((420,224))
        x=index%3*426;y=index//3*250;sheet.paste(pic,(x,y+24));draw.text((x+6,y+5),slug,fill=(235,240,245))
    sheet.save(out/('sheet_'+str(offset//12+1).zfill(3)+'.png'))
report={'current_run_frames':len(names),'components_with_samples':len(rows),'provisional_empty_flags':flags,'temporary_sheets':str(out),'scope':'In-progress visual inspection only; final acceptance requires completed capture registry and PNG hashes.'}
if args.report:(root/args.report).write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
