"""Exercise the compiled routing API against canonical primary/weapon rules."""
import unreal as u,json,pathlib
R=pathlib.Path(u.Paths.project_dir())
weapons={
 'SWORD':'Sword','AXE':'Axe','CLUB':'Club','WAND':'Wand','RAPIER':'Rapier',
 'DUAL_DAGGERS':'DualDaggers','FISTS_GAUNTLETS':'FistsGauntlets','GREAT_CLUB':'GreatClub',
 'STAFF':'Staff','CROSSBOW':'Crossbow','GREATSWORD':'Greatsword','GREATAXE':'Greataxe','BOW':'Bow','SPEAR':'Spear'}
primaries={'FIGHTER':'Physical','SCOUT':'Physical','MAGE':'Magical','MYSTIC':'Magical'}
ranged={'WAND','STAFF','BOW','CROSSBOW'}
tests=[]
for key,name in weapons.items():
 weapon=getattr(u.SanctaVFXWeapon,key)
 for primary,channel in primaries.items():
  actual=str(u.SanctaVFXCombatLibrary.basic_presentation_id(weapon,getattr(u.SanctaVFXPrimary,primary)))
  expected='Combat.Basic.'+name+'.'+channel
  asset='/Game/Sancta/VFX/Definitions/DA_'+expected.replace('.','_')
  definition=u.load_asset(asset)
  phases=definition.get_editor_property('phases') if definition else []
  delivery='Flight' if key in ranged else 'Trail'
  delivery_phases=[p for p in phases if str(p.get_editor_property('phase'))==delivery]
  hits=[p for p in phases if str(p.get_editor_property('phase'))=='Impact']
  passed=actual==expected and u.SanctaVFXCombatLibrary.is_ranged_presentation(weapon)==(key in ranged) and len(delivery_phases)==1 and len(hits)==1
  if delivery_phases:
   p=delivery_phases[0]
   passed=passed and p.get_editor_property('anchor')==(u.SanctaVFXAnchor.PROJECTILE if key in ranged else u.SanctaVFXAnchor.SOURCE)
  if hits:passed=passed and hits[0].get_editor_property('gate')==u.SanctaVFXGate.CONFIRMED_HIT
  tests.append({'weapon':name,'primary':primary,'expected':expected,'actual':actual,'asset':asset,'passed':bool(passed)})
report={'passed':all(t['passed'] for t in tests),'cases':len(tests),'tests':tests,'scope':'Compiled native routing and real DataAsset compositions; no weapon rig or Foundation gameplay transport implied.'}
(R/'Evidence/gameplay-basic-routing-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
if not report['passed']:raise RuntimeError('Native basic routing/composition test failed')
u.log('SanctaBasicRouting 56/56 passed')
u.SystemLibrary.quit_editor()
