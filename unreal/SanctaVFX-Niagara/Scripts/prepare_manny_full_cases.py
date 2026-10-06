"""All current components on Manny; exact event gates and explicit provisional attachments."""
import copy, hashlib, json, math, pathlib, re, statistics

R = pathlib.Path(__file__).resolve().parents[1]
read = lambda p: json.loads((R/p).read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256((R/p).read_bytes()).hexdigest()
jobs = read('Evidence/gameplay-runtime-build-jobs.json')['jobs']
definitions = {d['presentation_id']: d for d in read('Evidence/gameplay-runtime-definitions.json')['definitions']}
viewer = {c['name']: c for c in read('Evidence/runtime-viewer-cases.json')}
plan = {c['name']: c for c in read('Evidence/runtime-capture-plan.json')}
captures = {r['slug']: r for r in read('Evidence/gameplay-runtime-capture-audit.json')['rows']}
cases = copy.deepcopy(read('Evidence/gameplay-manny-cases.json'))
covered = {c['component'] for c in cases}
lengths = {'Sword':75, 'Axe':65, 'Club':65, 'Rapier':95, 'DualDaggers':30,
           'FistsGauntlets':18, 'GreatClub':120, 'Greatsword':130, 'Greataxe':120,
           'Spear':150, 'Wand':35, 'Staff':120, 'Crossbow':45, 'Bow':55}

def authored_height(data):
    # Attribute heights are in metres. Horizontal runtime anchors deliberately
    # retain the original body height; compensate that height once at the bone.
    heights = [v[1] for l in data['layers'] for v in l.get('attributes',{}).get('aO',{}).get('values',[]) if len(v)>1 and v[1]>.1]
    if heights:
        return statistics.median(heights)*100
    code = '\n'.join(l['vertex'] for l in data['layers'])
    if re.search(r'vec3\(0\.?\s*,\s*1\.2[05]?\s*,\s*0\.?\)', code):
        return 125.
    return 100.

def make(j):
    key=j['slug']; data=read(j['source']); anchor=j['anchor']; phase=j['phase']
    binding={'Source':'source_body','Target':'target_body','World':'world','Link':'beam','Projectile':'projectile'}[anchor]
    height=authored_height(data); bone=''; length=75
    if anchor=='Source' and (phase in ('Movement','Hold','Telegraph') or key.startswith(('Volley','BrightStar','Manifest','DefiantPresence'))):
        binding='root'
    if j['form'].startswith('Combat.Basic.'):
        family=key.removeprefix('Basic').removesuffix(phase)
        family=re.sub(r'(Physical|Magical)$','',family)
        length=lengths[family]
        if phase=='Trail':binding='weapon';bone='HandGrip_R'
        if phase=='Release':binding='weapon_muzzle';bone='HandGrip_R'
    if key.startswith('Guard'):binding='chest';height=0
    if key.startswith('FootContact'):binding='foot'
    if key=='DodgeStart':binding='root'
    if key=='DodgeAvoided':binding='chest';height=0
    if key=='BlinkCast':binding='root'
    if key.startswith('CC'):
        binding='head' if key.startswith(('CCStun','CCSleep','CCSilence','CCTaunt','CCFear','CCDisarm')) else 'target_root'
    if key.startswith('SeveringMark'):binding='target_chest';height=162
    if key.startswith('BlindingDart') and anchor=='Target':binding='target_face'
    if key.startswith(('ChallengeIIRoot','ChainsIITargetWrap','Resurrect')):binding='target_root'
    if key=='LongJumpHold':binding='ground_link'
    if anchor=='World' and j.get('contact') and phase=='Impact':binding='target_contact';height=0
    if key.startswith(('TankStance','WarriorStance','Rage','Bulwark')):binding='waist';height=100
    if key.startswith(('SunStance','MoonStance','AstralAura','ArcaneWeaving','ElementalWeaver','Weave')):binding='root'
    # A component may combine a body cue with a floor ring. Moving its whole
    # origin to the chest would lift that ring; retain the authored root basis.
    code='\n'.join(l['vertex'] for l in data['layers'])
    floor_layer=bool(re.search(r'vec3\([^;{}\n]*,\s*\.0[1-9][0-9]*\s*,',code))
    whole_body=key=='EvasionProc' or key.startswith(('Cleansemage','Cleansemystic','Cleansescout'))
    if binding in ('source_body','target_body') and (floor_layer or whole_body):
        binding='target_root' if anchor=='Target' else 'root'
    return {'name':key,'component':key,'title':viewer[key]['title'],'binding':binding,
            'bone':bone,'endpoint_bone':'','definition':definitions[j['form']]['asset'],
            'phase':phase,'persistent':j['persistent'],'source':j['source'],
            'system_override':'','rig_source':'','arm_mask':3,'fixture_only':True,
            'authored_height_cm':height,'weapon_length_cm':length}

for j in jobs:
    if j['slug'] not in covered:cases.append(make(j))
byjob={j['slug']:j for j in jobs}
for c in cases:
    j=byjob[c['component']]; original=viewer[c['component']]
    best=max(captures[c['component']]['samples'],key=lambda s:s['changed_pixels_over_12'])
    recorded=plan[pathlib.PurePosixPath(best['file']).stem]
    c.update(full_catalog=True,anchor=j['anchor'],gate=j['gate'],audit_age=recorded['age'],
             duration=j['duration'],loop_duration=max(.3,j['duration']+.25),
             camera_horizontal_cm=max(515,math.hypot(original.get('camera_x',230),original.get('camera_y',-480))),
             camera_elevation_cm=original.get('camera_z',270)-original.get('look_z',85),
             camera_focus_forward_cm=original.get('look_x',0),camera_focus_height_cm=original.get('look_z',105),
             fixture_inputs={k:recorded[k] for k in ('count','max','occupied','element_a','element_b','hold','release','surface','range','cone') if k in recorded},
             authored_height_cm=c.get('authored_height_cm',162 if c['binding']=='target_chest' else 100),
             weapon_length_cm=c.get('weapon_length_cm',75),
             attachment_status='provisional_weapon_dimensions' if c['binding'] in ('weapon','weapon_muzzle') else 'live_bone_or_explicit_world_fixture')
    if c['component']=='BlinkCast':c['audit_age']=.4
    if c['component']=='SecondWindHeal':
        c['camera_horizontal_cm']*=1.55
        c['camera_focus_height_cm']=190
    if c['component'].startswith('ShoulderRush') and c['phase']=='Movement':
        c['camera_horizontal_cm']*=1.7
        c['camera_focus_forward_cm']=-130
    if c['component']=='AstralPullRelocate':
        c['camera_horizontal_cm']*=1.8
        c['camera_focus_height_cm']=175

# Off-hand fixtures use the same material with a distinct component origin;
# never pretend one endpoint is a simultaneous pair of weapons.
for c in list(cases):
    if c['component'].startswith(('BasicDualDaggers','BasicFistsGauntlets')):
        left=copy.deepcopy(c);left.update(name=c['name']+'Left',title=c['title']+' — mão esquerda',bone='HandGrip_L')
        cases.append(left)
ice=copy.deepcopy(next(c for c in cases if c['component']=='IcebergProc'))
ice.update(name='IcebergTerrainBody',title='Iceberg — corpo de terreno com Manny',terrain=True,binding='world')
cases.append(ice)
assert {c['component'] for c in cases} == set(byjob)
assert len({c['name'] for c in cases})==len(cases)
path='Evidence/gameplay-manny-full-cases.json'
(R/path).write_text(json.dumps(cases,indent=2,ensure_ascii=False),encoding='utf-8')
report={'current_components':len(jobs),'covered_components':len(byjob),'scenarios':len(cases),
        'new_components_after_pass2':len(set(byjob)-covered),'poses':4,'scales':[.8,1.,1.2],'views':3,
        'expected_samples':len(cases)*24,'expected_effect_baseline_pairs':len(cases)*12,
        'catalog':path,'catalog_sha256':sha(path),'weapons_final':False,'gameplay_poses_final':False,
        'runtime_adapter_promoted':False,'production_approved':False,
        'scope':'Every current component, plus isolated hands and Iceberg body. Explicit lab events; no fabricated gameplay authority.'}
(R/'Evidence/gameplay-manny-full-plan.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
