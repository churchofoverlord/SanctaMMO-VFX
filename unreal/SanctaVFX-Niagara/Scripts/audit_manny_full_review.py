"""Audit resumable full-catalog Manny batches and produce a searchable local gallery.

Pixel presence is a diagnostic, not an artistic or gameplay approval.
"""
import argparse, datetime, hashlib, html, json, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

R = pathlib.Path(__file__).resolve().parents[1]
def read(p):
    data=(R / p).read_bytes()
    return json.loads(data.decode('utf-16' if data.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig'))
sha = lambda p: hashlib.sha256((R / p).read_bytes()).hexdigest()
parser = argparse.ArgumentParser()
parser.add_argument('--partial', action='store_true')
args = parser.parse_args()
cases = read('Evidence/gameplay-manny-full-cases.json')
out = R / 'Evidence/MannyFullReview'
out.mkdir(parents=True, exist_ok=True)
samples, batches, covered = [], [], set()
for path in sorted((R / 'Saved/MannyFullCaptures').glob('rig-results-*.json')):
    raw = read(path)
    meta_path = path.with_name(path.name.replace('rig-results-', 'batch-').replace('.json', '-inputs.json'))
    if not raw.get('complete') or not meta_path.exists():
        continue
    meta = read(meta_path)
    if meta.get('exit_code') != 0:
        continue
    first, end = raw['first'], raw['end']
    recorded = json.loads(raw['catalog_json'])
    if recorded[first:end] != cases[first:end]:
        raise RuntimeError(f'Stale case configuration: {path.name}')
    for p, h in meta['inputs'].items():
        if p.endswith('.umap') and sha(p)!=h:
            archived=R/'Saved/MannyFullMapArchive'/(h+'.umap')
            if not archived.exists() or sha(archived)!=h:
                raise RuntimeError('Captured map missing: '+p)
        elif p.endswith(('.cpp', '.h', '.cs', '.dll', '.ps1')) and sha(p) != h:
            raise RuntimeError('Stale compiled/map input: ' + p)
    if covered & set(range(first, end)):
        raise RuntimeError('Overlapping batches')
    expected = {(c['name'], p, s, t) for c in cases[first:end] for p in range(4)
                for s in (.8, 1., 1.2) for t in range(2)}
    actual = {(s['case'], int(s['pose']), round(s['scale'], 1), int(s['sample'])) for s in raw['samples']}
    if expected != actual or len(raw['samples']) != len(expected):
        raise RuntimeError('Missing/duplicate samples: ' + path.name)
    if not raw['passed'] or not raw['cleanup_passed']:
        raise RuntimeError('Native rig or cleanup failed: ' + path.name)
    covered.update(range(first, end))
    samples.extend(raw['samples'])
    batches.append({'file': path.relative_to(R).as_posix(), 'sha256': sha(path),
                    'metadata': meta_path.relative_to(R).as_posix(), 'metadata_sha256': sha(meta_path),
                    'first': first, 'end': end, 'exit_code': 0})
if not covered:
    raise RuntimeError('No completed batches')
complete = len(covered) == len(cases)
if not complete and not args.partial:
    raise RuntimeError('Incomplete catalog; use --partial for progress evidence')
poses = ['Repouso', 'Ataque', 'Corrida', 'Esquiva']
views = ['3/4', 'Frente', 'Lado']
font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 16)
titlefont = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 19)
prior_path = R/'Evidence/gameplay-manny-full-validation.json'
prior = read(prior_path) if prior_path.exists() else {}
cached = {(r['case'],r['pose'],r['view']): r for r in prior.get('frames', [])}
rows, isolated = [], []
for sample in samples:
    for capture in sample.get('images', []):
        name = capture['image']
        baseline = name.replace('.png', '_baseline.png')
        ih, bh = sha(name), sha(baseline)
        old = cached.get((sample['case'],sample['pose'],capture['view']))
        if old and old.get('analysis_mask')=='actual_ui_83_66' and old['image_sha256']==ih and old['baseline_sha256']==bh and (out/old['preview']).exists():
            arms_current = all(sha(a['image'])==a['sha256'] and (out/a['preview']).exists() for a in old.get('isolated_arms',[]))
            preview_current = not old.get('preview_sha256') or sha(out/old['preview'])==old['preview_sha256']
            if arms_current and preview_current:
                old['preview_sha256']=sha(out/old['preview'])
                with Image.open(R/name) as cached_image:
                    old['vertical_edge_flag']=bool(old['bounds'] and (old['bounds'][1]<=83 or old['bounds'][3]>=cached_image.height-67))
                rows.append(old);isolated.extend(old.get('isolated_arms',[]));continue
        with Image.open(R / name) as im:
            image = im.convert('RGB')
        with Image.open(R / baseline) as im:
            b = np.asarray(im.convert('RGB'), dtype=np.int16)
        delta = np.max(np.abs(np.asarray(image, dtype=np.int16) - b), axis=2)
        delta[:83, :] = 0; delta[-66:, :] = 0
        yy, xx = np.nonzero(delta > 12)
        count, peak = len(xx), int(delta.max())
        bounds = [int(xx.min()), int(yy.min()), int(xx.max()), int(yy.max())] if count else None
        jpg = f"{sample['case']}_pose{sample['pose']}_view{capture['view']}.webp"
        image.resize((640, 360)).save(out / jpg, quality=90)
        row = {'case': sample['case'], 'pose': sample['pose'], 'view': capture['view'], 'image': name,
               'image_sha256': ih, 'baseline_sha256': bh, 'preview': jpg, 'preview_sha256': sha(out/jpg),
               'changed_pixels_over_12': count, 'peak_difference': peak, 'bounds': bounds,
               'visible': count > 10 and peak > 15,
               'analysis_mask':'actual_ui_83_66',
               'edge_flag': bool(count and (xx.min() < 4 or xx.max() >= image.width-4)),
               'vertical_edge_flag':bool(count and (yy.min()<=83 or yy.max()>=image.height-67)),
               'small_flag': count < 100, 'isolated_arms': []}
        for arm in capture.get('isolated_arms', []):
            with Image.open(R / arm['image']) as im:
                aim = im.convert('RGB')
            d = np.max(np.abs(np.asarray(aim, dtype=np.int16) - b), axis=2)
            d[:83, :] = 0; d[-66:, :] = 0
            preview = pathlib.PurePosixPath(arm['image']).stem + '.webp'
            aim.resize((640, 360)).save(out / preview, quality=90)
            a = {**arm, 'sha256': sha(arm['image']), 'preview': preview,
                 'visible': int(np.count_nonzero(d > 12)) > 10}
            row['isolated_arms'].append(a); isolated.append(a)
        rows.append(row)
selected = [cases[i] for i in sorted(covered)]
assert len(rows) == len(selected) * 12
by_key = {(r['case'], r['pose'], r['view']): r for r in rows}
best = {c['name']: max((by_key[c['name'], p, v] for p in range(4) for v in range(3)),
                        key=lambda r: r['changed_pixels_over_12']) for c in selected}
sheets = []
for offset in range(0, len(selected), 24):
    chunk = selected[offset:offset+24]
    modes = [(-1, -1)] if args.partial else [(-1, -1)] + [(p, v) for p in range(4) for v in range(3)]
    for pose, view in modes:
        sheet = Image.new('RGB', (1920, 50+290*((len(chunk)+3)//4)), '#111821')
        draw = ImageDraw.Draw(sheet)
        label = 'Melhor presença' if pose < 0 else f'{poses[pose]} · {views[view]}'
        draw.text((18, 10), f'Manny · {offset+1}–{offset+len(chunk)} · {label}', font=titlefont, fill='white')
        for i, c in enumerate(chunk):
            row = best[c['name']] if pose < 0 else by_key[c['name'], pose, view]
            x, y = (i % 4)*480, 50+(i//4)*290
            with Image.open(out / row['preview']) as im:
                sheet.paste(im.resize((480, 270)), (x, y+20))
            draw.text((x+8, y), c['title'][:54], font=font, fill='white' if row['visible'] else '#ff7766')
        filename = f'manny-{offset:03d}-best.jpg' if pose < 0 else f'manny-{offset:03d}-pose{pose}-view{view}.jpg'
        sheet.save(out / filename, quality=94)
        sheets.append({'file': 'Evidence/MannyFullReview/'+filename, 'first': offset, 'count': len(chunk), 'pose': pose, 'view': view})
cards = []
for c in selected:
    pictures = []
    for p in range(4):
        for v in range(3):
            row = by_key[c['name'], p, v]
            pictures.append(f'<figure data-pose="{p}" data-view="{v}"><a href="../../{row["image"]}"><img loading="lazy" src="{row["preview"]}"></a><figcaption>{poses[p]} · {views[v]} · {row["changed_pixels_over_12"]} píxeis</figcaption></figure>')
            for a in row['isolated_arms']:
                side = 'direito' if a['mask'] == 1 else 'esquerdo'
                pictures.append(f'<figure data-pose="{p}" data-view="{v}"><img loading="lazy" src="{a["preview"]}"><figcaption>Braço {side}</figcaption></figure>')
    cards.append(f'<article id="{html.escape(c["name"])}"><h2>{html.escape(c["title"])}</h2><code>{html.escape(c["component"])}</code><p>Ligação: {html.escape(c["binding"])}</p><div>{"".join(pictures)}</div></article>')
(out/'galeria.html').write_text('''<!doctype html><html lang="pt-PT"><meta charset="utf-8"><title>Manny — todos os VFX</title>
<style>body{background:#111821;color:#edf4fb;font:16px Segoe UI;margin:24px}a{color:#7ed5ff}article{border-top:1px solid #394551;padding:16px 0}article div{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}figure{margin:8px}[hidden]{display:none!important}img{width:100%}code{color:#a5c4dc}select,input{font:inherit;padding:8px;background:#19232c;color:white}nav{position:sticky;top:0;background:#111821;padding:12px}</style>
<h1>Manny — todos os VFX</h1><p>''' + f'{len(selected)}/{len(cases)} cenários · {len({c["component"] for c in selected})}/331 componentes · quatro poses de template · três vistas. Armas finais e integração no jogo pendentes.' + '''</p>
<nav><input id="search" placeholder="Pesquisar skill ou componente"><select id="pose"><option value="0">Repouso</option><option value="1">Ataque</option><option value="2">Corrida</option><option value="3">Esquiva</option><option value="all">Todas as poses</option></select><select id="view"><option value="0">3/4</option><option value="1">Frente</option><option value="2">Lado</option><option value="all">Todas as vistas</option></select></nav>
''' + ''.join(cards) + '''<script>const search=document.querySelector('#search'),pose=document.querySelector('#pose'),view=document.querySelector('#view');function update(){document.querySelectorAll('article').forEach(a=>{a.hidden=!a.querySelector('h2').textContent.toLowerCase().includes(search.value.toLowerCase())&&!a.querySelector('code').textContent.toLowerCase().includes(search.value.toLowerCase());a.querySelectorAll('figure').forEach(f=>f.hidden=(pose.value!=='all'&&f.dataset.pose!==pose.value)||(view.value!=='all'&&f.dataset.view!==view.value))})}search.addEventListener('input',update);pose.addEventListener('change',update);view.addEventListener('change',update);update();</script></html>''', encoding='utf-8')
compiled = read('Evidence/gameplay-runtime-compiled-sources.json')
modules_preserved = all(sha(p) == h for p, h in compiled['modules'].items())
manifest = read('Evidence/gameplay-runtime-migration-manifest.json')
assets_preserved = all(sha(p['file']) == p['sha256'] for p in manifest['packages'])
sources = {}
for f in (R/'Plugins/SanctaVFXMannyLab/Source').rglob('*'):
    if f.is_file():
        p = f.relative_to(R).as_posix()
        if sha(p) != sha('BuildHost/'+p):
            raise RuntimeError('Uncompiled source: '+p)
        sources[p] = sha(p)
dependencies = {}
for c in selected:
    for source in [c['source']] + ([c['rig_source']] if c.get('rig_source') else []):
        dependencies[source] = sha(source)
        port = str(pathlib.PurePosixPath(source).with_suffix('.port.json'))
        dependencies[port] = sha(port)
    definition = 'Content/'+c['definition'].removeprefix('/Game/').split('.')[0]+'.uasset'
    dependencies[definition] = sha(definition)
    if c.get('system_override'):
        system = 'Content/'+c['system_override'].removeprefix('/Game/').split('.')[0]+'.uasset'
        dependencies[system] = sha(system)
reference = read('Evidence/gameplay-manny-local-reference.json')
rig_preserved = all(sha(row['path']) == row['sha256'] for row in reference['files'])
jobs = read('Evidence/gameplay-runtime-build-jobs.json')['jobs']
base_sources_preserved = all(sha(j['source']) == j['source_sha256'] for j in jobs)
variant_inputs = read('Evidence/gameplay-manny-binding-sources.json')['rows']
variant_ports_current = all(sha(str(pathlib.PurePosixPath(j['source']).with_suffix('.port.json'))) == j['port_sha256'] for j in variant_inputs)
flags = [r for r in rows if not r['visible'] or r['edge_flag'] or r['vertical_edge_flag'] or r['small_flag']]
motion=[]
sample_index={(s['case'],s['pose'],round(s['scale'],1),s['sample']):s for s in samples}
for c in selected:
    for pose in (1,2):
        local=[]
        for t in (0,1):
            s=sample_index[c['name'],pose,1.,t]
            yaw=np.deg2rad(t*73.)
            rot=np.array([[np.cos(yaw),-np.sin(yaw),0],[np.sin(yaw),np.cos(yaw),0],[0,0,1]])
            local.append(rot.T@(np.asarray(s['hand_r'])-s['actor_origin']))
        motion.append({'case':c['name'],'pose':pose,'hand_pose_delta_cm':float(np.linalg.norm(local[1]-local[0]))})
animated=all(m['hand_pose_delta_cm']>1 for m in motion)
arm_samples=[s for s in samples if 'arm_binding_error_m' in s]
arms_valid=all(s['arm_binding_error_m']<.001 and s['arm_separation_cm']>1 for s in arm_samples)
report = {'recorded_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'complete': complete, 'cases': len(selected), 'expected_cases': len(cases),
          'distinct_components': len({c['component'] for c in selected}),
          'measured_samples': len(samples), 'screenshots': len(rows),
          'visible_screenshots': sum(r['visible'] for r in rows), 'isolated_arm_frames': len(isolated),
          'batches': batches, 'maximum_origin_error_cm': max(s['origin_error_cm'] for s in samples),
          'current_vfx_modules_preserved': modules_preserved, 'current_runtime_assets_preserved': assets_preserved,
          'local_rig_assets_preserved': rig_preserved, 'base_sources_preserved': base_sources_preserved,
          'variant_ports_current': variant_ports_current, 'selected_effect_inputs': dependencies,
          'animation_motion_verified':animated,'motion':motion,
          'arm_binding_samples':len(arm_samples),'independent_arm_bindings_passed':arms_valid,
          'compiled_manny_sources': sources, 'inputs': {'Evidence/gameplay-manny-full-cases.json': sha('Evidence/gameplay-manny-full-cases.json')},
          'pending_cases': [c['name'] for i, c in enumerate(cases) if i not in covered],
          'frames': rows, 'contact_sheets': sheets, 'diagnostic_flags': flags,
          'visual_inspection': 'pending', 'production_approved': False, 'foundation_modified': False,
          'runtime_adapter_promoted': False, 'final_weapons_and_animations': False}
report['numerical_passed'] = all(s['passed'] for s in samples)
report['presence_passed'] = all(r['visible'] for r in rows) and all(a['visible'] for a in isolated)
report['component_presence_passed'] = all(best[c['name']]['visible'] for c in selected)
report['visibility_scope'] = 'Every scenario must have a visible representative frame. All twelve views/poses are measured separately; occluded or edge-on samples remain diagnostic flags, not automatic artistic approval.'
report['passed'] = complete and report['numerical_passed'] and report['component_presence_passed'] and modules_preserved and assets_preserved and rig_preserved and base_sources_preserved and variant_ports_current and animated and arms_valid
(R/'Evidence/gameplay-manny-full-validation.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({k: report[k] for k in ('complete','passed','cases','distinct_components','measured_samples','screenshots','visible_screenshots')}))
print('Diagnostic flags:', len(flags))
