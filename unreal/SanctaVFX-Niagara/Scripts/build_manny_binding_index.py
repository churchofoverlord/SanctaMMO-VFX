"""Export all measured lab attachment recipes, with explicit game integration gaps."""
import datetime, hashlib, json, pathlib
R=pathlib.Path(__file__).resolve().parents[1]
read=lambda p:json.loads((R/p).read_text(encoding='utf-8-sig'))
cases=read('Evidence/gameplay-manny-full-cases.json')
catalog_sha=hashlib.sha256((R/'Evidence/gameplay-manny-full-cases.json').read_bytes()).hexdigest()
validation=read('Evidence/gameplay-manny-full-validation.json') if (R/'Evidence/gameplay-manny-full-validation.json').exists() else {}
validated=validation.get('passed',False) and validation.get('visual_reviewed_scenarios')==len(cases) and validation.get('inputs',{}).get('Evidence/gameplay-manny-full-cases.json')==catalog_sha
recipes={
 'both_arms':(['hand_r','lowerarm_r','hand_l','lowerarm_l'],'Independent hand/lowerarm vectors; arm identity and mask'),
 'hand_elbow':(['hand_r','lowerarm_r','hand_l','lowerarm_l'],'Independent hand/lowerarm vectors; select arm explicitly'),
 'weapon':(['HandGrip_R','HandGrip_L'],'Replace provisional blade length/direction with actual weapon base/tip sockets'),
 'weapon_muzzle':(['HandGrip_R'],'Replace provisional muzzle with actual weapon muzzle socket'),
 'projectile':(['hand_r','spine_03'],'Game projectile transform; lab interpolation is a fixture only'),
 'source_body':(['spine_03'],'Source chest minus authored height once'),
 'target_body':(['spine_03'],'Target chest minus authored height once'),
 'target_chest':(['spine_03'],'Target chest minus authored height once'),
 'target_face':(['head'],'Target head minus authored height once'),
 'head':(['head'],'Target head plus 20 cm, compensating 180 cm authored height'),
 'waist':(['pelvis'],'Pelvis minus authored 100 cm'),
 'chest':(['spine_03'],'Source chest, 25 cm forward; Guard plane rotated 90 degrees'),
 'root':(['root'],'Source skeletal root'),
 'target_root':(['root'],'Target skeletal root'),
 'foot':(['foot_r'],'Confirmed ground contact required; lab projects onto Z=0'),
 'cast_hand':(['hand_r'],'Source hand'),
 'beam':(['hand_r','spine_03'],'Source hand to current target chest'),
 'ground_link':(['root'],'Source root to target root'),
 'target_contact':(['spine_03'],'Lab: 30 cm in front of target chest; game: confirmed surface hit position/normal'),
 'world':([], 'World position independent of moving bones and character scale'),
}
rows=[]
for c in cases:
    bones,rule=recipes[c['binding']]
    rows.append({'scenario':c['name'],'component':c['component'],'phase':c['phase'],
                 'anchor':c['anchor'],'binding':c['binding'],'bone_requirements':bones,
                 'attachment_bone_fixture':c.get('bone',''),
                 'placement':rule,'authored_height_cm':c['authored_height_cm'],
                 'world_size_inherits_character_scale':False if c['anchor']=='World' else True,
                 'gate':c['gate'],'definition':c['definition'],
                 'weapon_length_cm_fixture':c['weapon_length_cm'] if c['binding'] in ('weapon','weapon_muzzle') else None,
                 'status':'lab_recipe_verified_game_integration_pending' if validated else 'lab_recipe_pending_full_visual_validation',
                 'final_weapon_required':c['binding'] in ('weapon','weapon_muzzle'),
                 'runtime_shader_variant_promotion_required':bool(c.get('rig_source')),
                 'gameplay_events_authoritative':False})
report={'recorded_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'reference':'UE Manny','components':len({c['component'] for c in cases}),
        'scenarios':len(cases),'recipes':rows,'runtime_adapter_promoted':False,
        'source_catalog':'Evidence/gameplay-manny-full-cases.json',
        'source_catalog_sha256':catalog_sha,
        'final_animations_available':False,'final_weapon_assets_available':False,
        'integration_requirements':['Resolve actual game actors and life/execution/state IDs',
                                    'Use final weapon socket transforms, never provisional lengths',
                                    'Evaluate skeletal endpoints after the animation pose',
                                    'Preserve authoritative world radius/range/cone and hit normal',
                                    'Promote private arm/scale adapter with runtime variant dependencies',
                                    'Drive phases from ability/notifies and confirmed state events'],
        'foundation_modified':False,'production_approved':False}
(R/'Evidence/gameplay-manny-full-binding-index.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'components':report['components'],'scenarios':report['scenarios']}))
