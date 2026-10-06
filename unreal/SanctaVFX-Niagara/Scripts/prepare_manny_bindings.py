"""Reproducible, separate Manny rig variants. Current runtime assets stay untouched."""
import copy, hashlib, json, pathlib
from reference_shader_port import prepare
from runtime_shader_bindings import bind

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'Source/MannyCalibration'
OUT.mkdir(exist_ok=True)
read = lambda path: json.loads((R / path).read_text(encoding='utf-8-sig'))
jobs = {j['slug']: j for j in read('Evidence/gameplay-runtime-build-jobs.json')['jobs']}
keys = ['BleedStanceActive', 'PoisonStanceActive', 'RapidAttackCast',
        'GuardActive', 'BasicSwordPhysicalTrail', 'BasicSwordMagicalTrail']
rows = []
for key in keys:
    source = jobs[key]['source']
    data = copy.deepcopy(read(source))
    data['slug'] = key + 'Manny'
    data['method'] = 'separate_animated_rig_calibration_variant'
    for layer in data['layers']:
        cfg = layer['runtime_binding']
        if key in keys[:3]:
            # Stable authored identity is retained after aO is replaced.
            # Branching on aO after rebasing would collapse both sides again.
            side = [1.0 if value[0] > 0 else -1.0 for value in layer['attributes']['aO']['values']]
            assert 1.0 in side and -1.0 in side
            layer['attributes']['aArm'] = {'size': 1, 'values': [[v] for v in side]}
            layer['vertex'] = 'attribute float aArm;uniform float uArmMask;\n' + layer['vertex']
            gate = ('if((aArm>0. && mod(uArmMask,2.)<.5)||(aArm<0. && uArmMask<1.5))'
                    '{gl_Position=vec4(2.,2.,2.,1.);return;}')
            layer['vertex'] = layer['vertex'].replace('void main(){', 'void main(){' + gate, 1)
            assert gate in layer['vertex']
            layer['uniforms']['uArmMask'] = {'type': 'number', 'value': 3.0}
            layer.setdefault('runtime_uniforms', {})['uArmMask'] = 'RuntimeArmMask'
            cfg['anchor'] = 'float3(0,0,0)'
            cfg['defaults'] = {**cfg.get('defaults', {}), 'RuntimeArmMask': 3.0,
                'RuntimeRightOrigin': [.46, .72, -.1, 0.], 'RuntimeRightEndpoint': [.43, 1.2, -.075, 0.],
                'RuntimeLeftOrigin': [-.46, .72, -.1, 0.], 'RuntimeLeftEndpoint': [-.43, 1.2, -.075, 0.]}
            origin = '(f.aArm>0 ? RuntimeRightOrigin.xyz : RuntimeLeftOrigin.xyz)'
            endpoint = '(f.aArm>0 ? RuntimeRightEndpoint.xyz : RuntimeLeftEndpoint.xyz)'
            cfg['attributes']['aO'] = origin
            if 'aE' in layer['attributes']:
                cfg['attributes']['aE'] = endpoint
            if 'aF' in layer['attributes']:
                cfg['attributes']['aF'] = 'normalize(' + endpoint + '-' + origin + '+float3(1e-6,0,0))'
                cfg['attributes']['aK'] = 'max(length(' + endpoint + '-' + origin + '),.02)/.42'
                layer['vertex'] = layer['vertex'].replace('(x + .04)', '(x + .01)')
        else:
            tint = {'GuardActive': [.46, .70, .84, 0.],
                    'BasicSwordPhysicalTrail': [.82, .52, .23, 0.],
                    'BasicSwordMagicalTrail': [.62, .43, .95, 0.]}[key]
            layer.setdefault('runtime_uniforms', {})['uColor'] = 'RuntimeTint.xyz'
            cfg['defaults'] = {**cfg.get('defaults', {}), 'RuntimeTint': tint}
            if key.startswith('BasicSword'):
                layer['vertex'] = layer['vertex'].replace('0.026*pow', '0.038*pow')
    target = OUT / (key + '.json')
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    rows.append({'component': key, 'source': target.relative_to(R).as_posix(),
                 'base_source': source, 'base_source_sha256': hashlib.sha256((R/source).read_bytes()).hexdigest(),
                 'job': jobs[key]})
translated = prepare(R, OUT)
assert all(row['ready'] for row in translated), translated
for row in rows:
    path = (R / row['source']).with_suffix('.port.json')
    port = json.loads(path.read_text(encoding='utf-8-sig'))
    for layer in port['layers']:
        bind(layer)
        layer['native_shared_root'] = '/Game/Sancta/VFX/MannyLab/Common'
    port['runtime_emitter_revision'] = 'manny_independent_arms_v1'
    path.write_text(json.dumps(port, indent=2, ensure_ascii=False), encoding='utf-8')
    row['port_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
(R / 'Evidence/gameplay-manny-binding-sources.json').write_text(
    json.dumps({'scope': 'Local rig calibration variants, not shipping replacements.', 'rows': rows}, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'separate_rig_variants': len(rows), 'original_runtime_sources_modified': False}))
