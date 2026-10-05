"""Pixel presence paired with the same native scene; never substitutes art review."""
import pathlib,json,hashlib,html
from PIL import Image,ImageChops,ImageDraw
from runtime_capture_signatures import CaptureSignatures
R=pathlib.Path(__file__).resolve().parents[1];images=R/'Saved/RuntimeCaptures';out=R/'Evidence/RuntimeReview';out.mkdir(parents=True,exist_ok=True)
registry=json.loads((R/'Evidence/gameplay-runtime-capture-frames.json').read_text(encoding='utf-8'))
signatures=CaptureSignatures(R)
plan={case['name']:case for case in json.loads((R/'Evidence/runtime-capture-plan.json').read_text(encoding='utf-8'))}
accepted={name:row for name,row in registry['frames'].items() if name in plan and row.get('component_signature')==signatures.signature(plan[name])} if registry.get('render_context')==signatures.render_context else {}
jobs=json.loads((R/'Evidence/gameplay-runtime-build-jobs.json').read_text(encoding='utf-8'))['jobs'];rows=[]
for job in jobs:
 baseline=images/('All_'+job['slug']+'_baseline.png');shots=sorted(images.glob('All_'+job['slug']+'_[0-9].png'));samples=[]
 if baseline.is_file() and baseline.stem in accepted:
  if hashlib.sha256(baseline.read_bytes()).hexdigest()!=accepted[baseline.stem]['sha256']:raise RuntimeError('Accepted baseline changed: '+baseline.name)
  base=Image.open(baseline).convert('RGB')
  for path in shots:
   if path.stem not in accepted:continue
   if hashlib.sha256(path.read_bytes()).hexdigest()!=accepted[path.stem]['sha256']:raise RuntimeError('Accepted PNG changed: '+path.name)
   pic=Image.open(path).convert('RGB');diff=ImageChops.difference(base,pic);r,g,b=diff.split();hist=ImageChops.lighter(ImageChops.lighter(r,g),b).histogram();changed=sum(hist[13:])
   mask=ImageChops.lighter(ImageChops.lighter(r,g),b).point(lambda value:255 if value>12 else 0);box=mask.getbbox()
   samples.append({'file':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'changed_pixels_over_12':changed,'max_channel_delta':max(i for i,n in enumerate(hist) if n),'presence_flag':changed>=6,'changed_pixel_bounds':box,'touches_image_edge':bool(box and (box[0]<=2 or box[1]<=2 or box[2]>=pic.width-2 or box[3]>=pic.height-2))})
 rows.append({'slug':job['slug'],'form':job['form'],'phase':job['phase'],'anchor':job['anchor'],'persistent':job['persistent'],'samples':samples,'baseline':baseline.relative_to(R).as_posix() if baseline.exists() else None,'presence_flag':any(s['presence_flag'] for s in samples),'art_review':'pending'})
report={'scope':'Paired native screenshot difference on a neutral stage. Pixel presence is a diagnostic, not visual quality, correct gameplay wiring or budget approval.','jobs':len(rows),'captured':sum(bool(r['samples']) for r in rows),'presence_flags':sum(r['presence_flag'] for r in rows),'needs_check':[r['slug'] for r in rows if r['samples'] and not r['presence_flag']],'pending_capture':[r['slug'] for r in rows if not r['samples']],'rows':rows}
report['module_sha256']=hashlib.sha256((R/'Plugins/SanctaVFXBridge/Binaries/Win64/UnrealEditor-SanctaVFXRuntime.dll').read_bytes()).hexdigest()
report['jobs_manifest_sha256']=hashlib.sha256((R/'Evidence/gameplay-runtime-build-jobs.json').read_bytes()).hexdigest()
report['capture_context']=registry['context'];report['render_context']=registry.get('render_context',{})
report['framing_checks']=[r['slug'] for r in rows if any(sample['touches_image_edge'] for sample in r['samples'] if sample['presence_flag'])]
(R/'Evidence/gameplay-runtime-capture-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
usable=[r for r in rows if r['samples']]
thumbs=out/'Thumbs';thumbs.mkdir(exist_ok=True)
for row in usable:
 for sample in row['samples']:
  picture=Image.open(R/sample['file']).convert('RGB');picture.thumbnail((960,540))
  preview=thumbs/(pathlib.Path(sample['file']).stem+'.webp');picture.save(preview,'WEBP',quality=90)
  sample['gallery_preview']=preview.relative_to(R).as_posix();sample['gallery_preview_sha256']=hashlib.sha256(preview.read_bytes()).hexdigest()
(R/'Evidence/gameplay-runtime-capture-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
for offset in range(0,len(usable),12):
 group=usable[offset:offset+12];sheet=Image.new('RGB',(1280,4*250),(24,28,34));draw=ImageDraw.Draw(sheet)
 for i,row in enumerate(group):
  sample=max(row['samples'],key=lambda s:s['changed_pixels_over_12']);pic=Image.open(R/sample['file']).convert('RGB');pic.thumbnail((420,224))
  x=i%3*426;y=i//3*250;sheet.paste(pic,(x,y+24));draw.text((x+6,y+5),row['slug']+(' [CHECK]' if not row['presence_flag'] else ''),fill=(235,240,245))
 sheet.save(out/('sheet_'+str(offset//12+1).zfill(3)+'.png'))
cards=[]
for row in usable:
 imgs=''.join('<a href="../../'+html.escape(s['gallery_preview'],quote=True)+'"><img loading="lazy" src="../../'+html.escape(s['gallery_preview'],quote=True)+'"></a>' for s in row['samples'])
 cards.append('<article id="vfx-'+html.escape(row['slug'],quote=True)+'" data-name="'+html.escape(row['slug'].lower(),quote=True)+'"><h2>'+html.escape(row['slug'])+'</h2><p>'+html.escape(row['form']+' / '+row['phase']+' / '+row['anchor'])+'</p>'+imgs+'</article>')
page='<!doctype html><meta charset="utf-8"><title>Sancta — capturas runtime</title><style>body{background:#151a20;color:#e4e9ee;font:16px system-ui;margin:24px}input{padding:12px;width:50%;position:sticky;top:0}article{margin:24px 0;padding:12px;background:#202832}img{width:min(48%,640px)}h2{font-size:18px}p{color:#b5c1cc}</style><h1>Capturas da apresentação nativa</h1><p>Imagens de teste por fase. Aprovação artística, rigs e integração no jogo continuam separados.</p><input placeholder="Procurar efeito" oninput="document.querySelectorAll(\'article\').forEach(a=>a.hidden=!a.dataset.name.includes(this.value.toLowerCase()))">'+''.join(cards)
(out/'galeria.html').write_text(page,encoding='utf-8')
print(json.dumps({k:report[k] for k in ['jobs','captured','presence_flags','needs_check']}))
