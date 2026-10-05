"""Keep handed-off FormIds stable; presentation paths are a separate identity."""
import json,pathlib,hashlib
R=pathlib.Path(__file__).resolve().parents[1]
handoff=R.parent.parent/'docs/formid-vfx-inventory.json'
snapshot=json.loads(handoff.read_text(encoding='utf-8'))
catalog=json.loads((R/'VFX-catalog.json').read_text(encoding='utf-8'))['items']
available={i['slug'] for i in catalog}|{'pressure-provoke-tank'}
simple={'severing-strike-i':'severing-strike','piercing-strike-i':'piercing-strike',
 'shoulder-rush-i':'shoulder-rush','crushing-blow-i':'crushing-blow','chains-i':'chains',
 'backstab-i':'backstab','lullaby-i':'lullaby','lullaby-ii':'lullaby-ii-nightmare',
 'mana-barrier-ii':'mana-barrier-ii-overcharge'}
pairs={'arcane-shards':'arcane-burst','fire-fire':'vortex','ice-ice':'iceberg',
 'lightning-lightning':'coil','fire-ice':'mist','fire-lightning':'laser','ice-lightning':'tempest'}
routes=[];unresolved=[]
for e in snapshot['entries']:
    fid=e['formId'];parts=fid.split('.');primary,skill,variant=parts[0],parts[-2],parts[-1]
    sources=[];kind='execution'
    if skill=='cleanse':sources=[{'presentation':{'fighter':'cleanse','mage':'cleansemage','mystic':'cleansemystic','scout':'cleansescout'}[primary]}]
    elif skill=='warrior-stance-tank-stance':sources=[{'presentation':variant+'-stance'}]
    elif skill=='rage-bulwark':sources=[{'presentation':'rage' if variant=='warrior' else 'bulwark'}]
    elif skill=='battlecry-i-challenge-i':sources=[{'presentation':'battlecry-challenge-i-'+variant}]
    elif skill=='pressure-i-provoke-i':sources=[{'presentation':'pressure-provoke-tank' if variant=='tank' else 'pressure-provoke'}]
    elif skill=='rally-i':sources=[{'presentation':'rally-i-'+stance,'required_stance_snapshot':stance.title()} for stance in ['warrior','tank']]
    elif skill=='poison-bleed-stance':sources=[{'presentation':variant+'-stance'}]
    elif skill=='poison-sac-hemorrhage':sources=[{'presentation':'poison-sac' if variant=='poison' else 'hemorrhage'}]
    elif skill=='poison-sac-hemorrhage-ii':sources=[{'presentation':'sickness'}]
    elif skill=='basic-attack':sources=[{'presentation':'basic-attack-'+variant}];kind='confirmed_result_overlay'
    elif skill=='manifest-weave':sources=[{'presentation':variant}];kind='stance_state'
    elif skill=='arcane-burst':sources=[{'presentation':pairs[variant]}]
    elif skill=='sun-moon-stance':sources=[{'presentation':variant+'-stance'}];kind='stance_state'
    elif skill=='bright-star-full-moon':sources=[{'presentation':'bright-star' if variant=='sun' else 'full-moon'}]
    elif skill=='sun-aura-moon-aura':sources=[{'presentation':'astral-aura-'+variant}]
    else:
        base=simple.get(skill,skill)
        if base+'-'+variant in available:base+='-'+variant
        sources=[{'presentation':base}]
    for source in sources:
        if source['presentation'] not in available:unresolved.append({'form_id':fid,'presentation':source['presentation']})
    routes.append({'form_id':fid,'sources':sources,'kind':kind,
        'identity_provenance':e.get('canonSha'),
        'context_at_admission':e.get('executionContext',{}),
        'mechanics_authority':'Current Canon-Current and scoped decisions cited by gameplay assessment, not old handoff travel/timers.'})
report={'schema':'sancta-runtime-form-routing/v1','identity_handoff_sha256':hashlib.sha256(handoff.read_bytes()).hexdigest(),
 'identity_snapshot':snapshot['authority'],'routes':routes,'unresolved':unresolved,
 'policy':'No FormId rename or synthesis IDs invented. Legacy names remain provenance. Same delivery in Weave; signature/resource results only from authority.'}
(R/'Evidence/gameplay-runtime-form-routes.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
if unresolved:raise RuntimeError(str(unresolved))
print(json.dumps({'canonical_routes':len(routes),'unresolved':len(unresolved)}))
