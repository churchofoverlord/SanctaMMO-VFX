"""Compare paired diagnostic PNGs; presence is separate from art approval."""
import hashlib,json,pathlib
from PIL import Image,ImageChops,ImageDraw
root=pathlib.Path(__file__).resolve().parents[1]
plan=json.loads((root/'Evidence/runtime-shader-diagnostic-cases.json').read_text(encoding='utf-8'))
metadata=json.loads((root/'Saved/RuntimeCaptures/capture-frames.json').read_text(encoding='utf-8-sig'))
actual={row['case']:row for row in metadata}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for case in plan:
    name=case['name']
    if name.endswith('_baseline'):continue
    group=name.rsplit('_',1)[0]
    path=root/'Saved/RuntimeCaptures'/(name+'.png')
    baseline=root/'Saved/RuntimeCaptures'/(group+'_baseline.png')
    if name not in actual or group+'_baseline' not in actual:raise RuntimeError('Missing capture metadata: '+name)
    picture=Image.open(path).convert('RGB');base=Image.open(baseline).convert('RGB')
    channels=ImageChops.difference(base,picture).split()
    hist=ImageChops.lighter(ImageChops.lighter(channels[0],channels[1]),channels[2]).histogram()
    rows.append({'name':name,'age':case['age'],'file':path.relative_to(root).as_posix(),'sha256':sha(path),'baseline_sha256':sha(baseline),'changed_pixels_over_12':sum(hist[13:]),'particles':actual[name]['particles'],'active_components':actual[name]['active_components']})
report={'scope':'Paired screenshots after waiting for Niagara and asynchronously compiled material shaders. Pixel presence does not certify final art.','cases':len(plan),'rows':rows,'groups_without_presence':[group for group in sorted({r['name'].rsplit('_',1)[0] for r in rows}) if not any(r['changed_pixels_over_12']>=6 for r in rows if r['name'].rsplit('_',1)[0]==group)],'bridge_sha256':sha(root/'Plugins/SanctaVFXBridge/Binaries/Win64/UnrealEditor-SanctaVFXBridge.dll')}
(root/'Evidence/runtime-shader-diagnostic-result.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
groups=sorted({r['name'].rsplit('_',1)[0] for r in rows})
sheet=Image.new('RGB',(1280,250*len(groups)),(24,28,34));draw=ImageDraw.Draw(sheet)
for index,group in enumerate(groups):
    best=max((r for r in rows if r['name'].rsplit('_',1)[0]==group),key=lambda r:r['changed_pixels_over_12'])
    old=root/'Saved/RuntimeCaptures'/(best['name'].replace('ShaderReady_','All_',1)+'.png')
    for column,path in enumerate([old,root/best['file']]):
        if path.exists():
            pic=Image.open(path).convert('RGB');pic.thumbnail((630,220));sheet.paste(pic,(column*640,index*250+25))
        draw.text((column*640+8,index*250+5),('Before / ' if column==0 else 'Shader ready / ')+group.removeprefix('ShaderReady_'),fill=(235,240,245))
sheet_path=root/'Evidence/RuntimeReview/shader-ready-comparison.png'
sheet.save(sheet_path)
report['comparison_sheet']=sheet_path.relative_to(root).as_posix()
(root/'Evidence/runtime-shader-diagnostic-result.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
