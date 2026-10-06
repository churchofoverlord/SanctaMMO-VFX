"""Audit measured rig results and same-frame effect/baseline pixels, without game approval."""
import datetime, hashlib, html, json, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

R = pathlib.Path(__file__).resolve().parents[1]
read = lambda p: json.loads((R / p).read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256((R / p).read_bytes()).hexdigest()
raw = read('Saved/MannyCaptures/rig-results.json')
cases = read('Evidence/gameplay-manny-cases.json')
samples = raw['samples']
expected = {(c['name'], pose, scale, sample) for c in cases for pose in range(4)
            for scale in (.8, 1., 1.2) for sample in range(2)}
actual = {(s['case'], int(s['pose']), round(s['scale'], 1), int(s['sample'])) for s in samples}
if actual != expected or len(samples) != len(expected):
    raise RuntimeError('Missing or duplicate rig samples')
out = R / 'Evidence/MannyReview'
out.mkdir(parents=True, exist_ok=True)
font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 16)
titlefont = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 19)
poses = ['Repouso', 'Ataque', 'Corrida', 'Esquiva']
views = ['3/4', 'Frente', 'Lado']
rows = []
for sample in samples:
    for capture in sample.get('images', []):
        name = capture['image']
        baseline = name.replace('.png', '_baseline.png')
        image = Image.open(R / name).convert('RGB')
        a = np.asarray(image, dtype=np.int16); b = np.asarray(Image.open(R / baseline).convert('RGB'), dtype=np.int16)
        delta = np.max(np.abs(a - b), axis=2)
        # Both captures keep the same pose, camera and HUD. Limit presence to the scene.
        delta[:105, :] = 0; delta[-90:, :] = 0
        count = int(np.count_nonzero(delta > 12))
        jpg = '%s_pose%d_view%d.webp' % (sample['case'], sample['pose'], capture['view'])
        image.resize((640, 360)).save(out / jpg, quality=90)
        arms = []
        for isolated in capture.get('isolated_arms', []):
            arm = np.asarray(Image.open(R / isolated['image']).convert('RGB'), dtype=np.int16)
            arm_delta = np.max(np.abs(arm - b), axis=2); arm_delta[:105, :] = 0; arm_delta[-90:, :] = 0
            arm_preview = pathlib.PurePosixPath(isolated['image']).stem + '.webp'
            Image.open(R / isolated['image']).convert('RGB').resize((640, 360)).save(out / arm_preview, quality=90)
            arms.append({**isolated, 'sha256': sha(isolated['image']),
                         'preview': 'Evidence/MannyReview/' + arm_preview,
                         'changed_pixels_over_12': int(np.count_nonzero(arm_delta > 12)),
                         'visible': int(np.count_nonzero(arm_delta > 12)) > 10})
        rows.append({'case': sample['case'], 'pose': sample['pose'], 'view': capture['view'], 'image': name,
                     'image_sha256': sha(name), 'baseline_sha256': sha(baseline), 'isolated_arms': arms,
                     'preview': 'Evidence/MannyReview/' + jpg, 'changed_pixels_over_12': count,
                     'peak_difference': int(delta.max()), 'visible': count > 10 and int(delta.max()) > 15})
expected_frames = len(cases) * 4 * 3
assert len(rows) == expected_frames, (len(rows), expected_frames)
for pose, view in [(p, v) for p in range(4) for v in range(3)]:
    sheet = Image.new('RGB', (1920, 50 + 290 * ((len(cases) + 3) // 4)), '#111821')
    draw = ImageDraw.Draw(sheet)
    draw.text((18, 10), 'Manny — %s — %s — escala 1×' % (poses[pose], views[view]), font=titlefont, fill='white')
    for index, case in enumerate(cases):
        row = next(r for r in rows if r['case'] == case['name'] and r['pose'] == pose and r['view'] == view)
        x, y = (index % 4) * 480, 50 + (index // 4) * 290
        thumb = Image.open(R / row['preview']).resize((480, 270))
        sheet.paste(thumb, (x, y + 20))
        draw.text((x + 8, y), case['title'], font=font, fill='white')
    sheet.save(out / ('manny-pose%d-view%d.jpg' % (pose, view)), quality=94)
cards = []
for case in cases:
    pictures = ''.join('<figure data-view="%d"><img loading="lazy" src="%s_pose%d_view%d.webp"><figcaption>%s · %s</figcaption></figure>' %
                       (v, case['name'], p, v, poses[p], views[v]) for p in range(4) for v in range(3))
    for row in rows:
        if row['case'] != case['name']:
            continue
        for arm in row['isolated_arms']:
            side = 'direito' if arm['mask'] == 1 else 'esquerdo'
            pictures += '<figure data-view="0"><img loading="lazy" src="%s"><figcaption>%s · braço %s isolado</figcaption></figure>' % (pathlib.PurePosixPath(arm['preview']).name, poses[row['pose']], side)
    cards.append('<article><h2>%s</h2><code>%s</code><div>%s</div></article>' %
                 (html.escape(case['title']), case['component'], pictures))
(out / 'galeria.html').write_text('''<!doctype html><html lang="pt-PT"><meta charset="utf-8"><title>Manny — calibração VFX</title>
<style>body{background:#111821;color:#edf4fb;font:16px Segoe UI;margin:24px}a{color:#7ed5ff}article{border-top:1px solid #394551;padding:16px 0}article div{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}figure{margin:8px}figure[hidden]{display:none}img{width:100%}code{color:#a5c4dc}select{font:inherit;padding:8px;background:#19232c;color:white}</style>
<h1>Manny — calibração VFX</h1><p>''' + str(len(cases)) + ''' cenários · quatro poses UE de teste · três vistas · escala 1× nas imagens. Variantes de ligação locais; armas/animações finais e integração no jogo pendentes.</p>
<label>Vista <select id="view"><option value="0">3/4</option><option value="1">Frente</option><option value="2">Lado</option><option value="all">Todas</option></select></label>
<p><a href="../../MANNY_VFX.md">Orientações e limites</a> · <a href="../../GUIA_VFX.html">Índice geral</a></p>''' + ''.join(cards) + '''<script>const view=document.querySelector('#view');function update(){document.querySelectorAll('[data-view]').forEach(x=>x.hidden=view.value!=='all'&&x.dataset.view!==view.value)}view.addEventListener('change',update);update();</script></html>''', encoding='utf-8')
motion = []
for case in cases:
    for pose in range(4):
        pair = [s for s in samples if s['case'] == case['name'] and s['pose'] == pose and round(s['scale'], 1) == 1]
        distance = float(np.linalg.norm(np.asarray(pair[0]['hand_r']) - pair[1]['hand_r']))
        local = []
        for sample in pair:
            # The explicit fixture rotates sample 0 by 0° and sample 1 by 73°.
            # Remove actor translation/rotation so motion cannot be passed by moving the actor alone.
            yaw = np.deg2rad(sample['sample'] * 73)
            rotation = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                                 [np.sin(yaw), np.cos(yaw), 0], [0, 0, 1]])
            local.append(rotation.T @ (np.asarray(sample['hand_r']) - sample['actor_origin']) / sample['scale'])
        local_distance = float(np.linalg.norm(local[0] - local[1]))
        motion.append({'case': case['name'], 'pose': pose, 'hand_world_delta_cm': distance,
                       'hand_pose_delta_cm': local_distance})
compiled = read('Evidence/gameplay-runtime-compiled-sources.json')
preserved = all(sha(path) == value for path, value in compiled['modules'].items())
reference = read('Evidence/gameplay-manny-local-reference.json')
local_assets = all(sha(row['path']) == row['sha256'] for row in reference['files'])
own_sources = {}
for file in (R / 'Plugins/SanctaVFXMannyLab/Source').rglob('*'):
    if file.is_file():
        path = file.relative_to(R).as_posix()
        if sha(path) != hashlib.sha256((R / 'BuildHost' / path).read_bytes()).hexdigest():
            raise RuntimeError('Uncompiled Manny source: ' + path)
        own_sources[path] = sha(path)
if sha('Plugins/SanctaVFXMannyLab/Binaries/Win64/UnrealEditor-SanctaVFXMannyLab.dll') != sha('BuildHost/Plugins/SanctaVFXMannyLab/Binaries/Win64/UnrealEditor-SanctaVFXMannyLab.dll'):
    raise RuntimeError('Manny deployment differs from the successful host build')
dependencies = {}
for case in cases:
    for path in [case['source'], str(pathlib.PurePosixPath(case['source']).with_suffix('.port.json')),
                 'Content/' + case['definition'].removeprefix('/Game/').split('.')[0] + '.uasset']:
        dependencies[path] = sha(path)
    if case.get('rig_source'):
        for path in [case['rig_source'], str(pathlib.PurePosixPath(case['rig_source']).with_suffix('.port.json')),
                     'Content/' + case['system_override'].removeprefix('/Game/').split('.')[0] + '.uasset']:
            dependencies[path] = sha(path)
variant_inputs = read('Evidence/gameplay-manny-binding-sources.json')
base_sources_preserved = all(sha(row['base_source']) == row['base_source_sha256'] for row in variant_inputs['rows'])
variant_assets = read('Evidence/gameplay-manny-binding-assets.json')
lab_assets = {p.relative_to(R).as_posix(): sha(p.relative_to(R))
              for p in (R / 'Content/Sancta/VFX/MannyLab').rglob('*.uasset')}
runtime_manifest = read('Evidence/gameplay-runtime-migration-manifest.json')
runtime_assets_preserved = all(sha(row['file']) == row['sha256'] for row in runtime_manifest['packages'])
arm_samples = [s for s in samples if 'arm_binding_error_m' in s]
arms_valid = all(s['arm_binding_error_m'] < .001 and s['arm_separation_cm'] > 1 for s in arm_samples)
isolated = [a for row in rows for a in row['isolated_arms']]
expected_isolated = sum(c['binding'] == 'both_arms' for c in cases) * 4 * 2
arms_visible = len(isolated) == expected_isolated and all(a['visible'] for a in isolated)
expected_arm_samples = sum(c['binding'] in ('both_arms', 'hand_elbow') for c in cases) * 4 * 3 * 2
assert len(arm_samples) == expected_arm_samples
report = {'recorded_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'cases': len(cases), 'distinct_components': len({c['component'] for c in cases}),
          'measured_samples': len(samples), 'poses': poses, 'scales': [.8, 1., 1.2],
          'views': views,
          'raw_passed': raw['passed'], 'cleanup_passed': raw['cleanup_passed'],
          'current_vfx_modules_preserved': preserved, 'local_rig_assets_preserved': local_assets,
          'base_sources_preserved': base_sources_preserved, 'independent_arm_bindings_passed': arms_valid,
          'current_runtime_assets_preserved': runtime_assets_preserved,
          'calibration_build_passed': variant_assets['passed'], 'calibration_asset_hashes': lab_assets,
          'arm_binding_samples': len(arm_samples), 'isolated_arm_frames': len(isolated), 'isolated_arms_visible': arms_visible,
          'screenshots': len(rows), 'visible_screenshots': sum(r['visible'] for r in rows),
          'maximum_origin_error_cm': max(s['origin_error_cm'] for s in samples),
          'compiled_manny_sources': own_sources, 'selected_effect_inputs': dependencies,
          'motion': motion, 'frames': rows,
          'inputs': {p: sha(p) for p in ['Evidence/gameplay-manny-cases.json', 'Evidence/gameplay-manny-discovery.json',
                                         'Evidence/gameplay-manny-local-reference.json', 'Evidence/gameplay-runtime-migration-manifest.json',
                                         'Evidence/gameplay-manny-binding-sources.json', 'Evidence/gameplay-manny-binding-assets.json',
                                         'Plugins/SanctaVFXMannyLab/Binaries/Win64/UnrealEditor-SanctaVFXMannyLab.dll']},
          'visual_inspection': 'pending', 'production_approved': False, 'foundation_modified': False,
          'scope': 'Live evaluated Manny bone transforms in separate PIE lab; template poses, proxy attachment and material scale adapter.',
          'remaining': ['Promote independent arm inputs from the lab adapter to runtime', 'Final weapons and skill animations/notifies',
                        'Promote rig scale and attachment adapter to runtime after approval', 'Actual gameplay camera, terrain, authority and multiplayer']}
animated = all(m['hand_pose_delta_cm'] > 1 for m in motion if m['pose'] in (1, 2))
report['animation_motion_verified'] = animated
report['passed'] = raw['passed'] and raw['cleanup_passed'] and preserved and runtime_assets_preserved and local_assets and base_sources_preserved and variant_assets['passed'] and animated and arms_valid and arms_visible and all(r['visible'] for r in rows)
(R / 'Evidence/gameplay-manny-validation.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({k: report[k] for k in ['passed', 'cases', 'measured_samples', 'screenshots', 'visible_screenshots']}))
