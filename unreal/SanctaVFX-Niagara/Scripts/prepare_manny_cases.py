"""Small explicit calibration set; template poses are not final skill animations."""
import json, pathlib

R = pathlib.Path(__file__).resolve().parents[1]
read = lambda p: json.loads((R / p).read_text(encoding='utf-8-sig'))
jobs = {j['slug']: j for j in read('Evidence/gameplay-runtime-build-jobs.json')['jobs']}
definitions = {d['presentation_id']: d for d in read('Evidence/gameplay-runtime-definitions.json')['definitions']}
specs = [
    ('BleedRight', 'BleedStanceActive', 'Bleed — mão direita ao cotovelo', 'hand_elbow', 'hand_r', 'lowerarm_r'),
    ('BleedLeft', 'BleedStanceActive', 'Bleed — mão esquerda ao cotovelo', 'hand_elbow', 'hand_l', 'lowerarm_l'),
    ('PoisonRight', 'PoisonStanceActive', 'Poison — mão direita ao cotovelo', 'hand_elbow', 'hand_r', 'lowerarm_r'),
    ('PoisonLeft', 'PoisonStanceActive', 'Poison — mão esquerda ao cotovelo', 'hand_elbow', 'hand_l', 'lowerarm_l'),
    ('SwordPhysical', 'BasicSwordPhysicalTrail', 'Espada física — haste de calibração', 'weapon', '', ''),
    ('SwordMagical', 'BasicSwordMagicalTrail', 'Espada mágica — haste de calibração', 'weapon', '', ''),
    ('Guard', 'GuardActive', 'Guard — alinhamento no tronco', 'chest', '', ''),
    ('Tank', 'TankStanceActive', 'Tank Stance — cintura', 'waist', '', ''),
    ('Warrior', 'WarriorStanceActive', 'Warrior Stance — cintura', 'waist', '', ''),
    ('Stun', 'CCStunActive', 'Stun — acima da cabeça do alvo', 'head', '', ''),
    ('Root', 'CCRootActive', 'Root — pés do alvo', 'target_root', '', ''),
    ('SeveringMark', 'SeveringMark1', 'Severing — marca no tronco do alvo', 'target_chest', '', ''),
    ('LaserBeam', 'LaserActive', 'Laser — mão ao tronco do alvo', 'beam', '', ''),
    ('LaserCast', 'LaserCast', 'Laser — origem na mão', 'cast_hand', '', ''),
    ('FootStone', 'FootContactStone', 'Contacto do pé — pedra', 'foot', '', ''),
    ('ArcaneResource', 'ArcaneWeavingIiResource', 'Arcane Weaving II — recurso no corpo', 'root', '', ''),
]
cases = []
for name, component, title, binding, bone, endpoint_bone in specs:
    j = jobs[component]
    cases.append({'name': name, 'component': component, 'title': title, 'binding': binding,
                  'bone': bone, 'endpoint_bone': endpoint_bone, 'definition': definitions[j['form']]['asset'],
                  'phase': j['phase'], 'persistent': j['persistent'], 'source': j['source'],
                  'fixture_only': True})
(R / 'Evidence/gameplay-manny-cases.json').write_text(json.dumps(cases, indent=2, ensure_ascii=False), encoding='utf-8')
print('Manny: %d cenários, quatro poses e três escalas' % len(cases))
