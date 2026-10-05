"""Native Effect Types: essential/gameplay remain available; decoration has tunable limits."""
import unreal as u,pathlib,json
R=pathlib.Path(u.Paths.project_dir());tools=u.AssetToolsHelpers.get_asset_tools();report=[]
for importance in ['Essential','Gameplay','Decorative']:
 name='NET_'+importance;directory='/Game/Sancta/VFX/Common/Scalability';path=directory+'/'+name
 effect=u.load_asset(path) if u.EditorAssetLibrary.does_asset_exist(path) else tools.create_asset(name,directory,u.NiagaraEffectType,u.NiagaraEffectTypeFactoryNew())
 effect.set_editor_property('update_frequency',u.NiagaraScalabilityUpdateFrequency.HIGH)
 effect.set_editor_property('cull_reaction',u.NiagaraCullReaction.PAUSE_RESUME)
 settings=[]
 for mask,distance,maximum in [(1,1500,32),(2,2500,64),(28,4000,96)]:
  setting=u.NiagaraSystemScalabilitySettings();platform=u.NiagaraPlatformSet();platform.set_editor_property('quality_level_mask',mask);setting.set_editor_property('platforms',platform)
  decorative=importance=='Decorative'
  setting.set_editor_property('bCullByDistance',decorative);setting.set_editor_property('max_distance',distance)
  setting.set_editor_property('bCullMaxInstanceCount',decorative);setting.set_editor_property('max_instances',maximum)
  setting.set_editor_property('bCullPerSystemMaxInstanceCount',False)
  settings.append(setting)
 array=u.NiagaraSystemScalabilitySettingsArray();array.set_editor_property('settings',settings);effect.set_editor_property('system_scalability_settings',array)
 if not u.EditorAssetLibrary.save_loaded_asset(effect):raise RuntimeError('Effect Type save failed')
 report.append({'importance':importance,'asset':path,'limits_enabled':importance=='Decorative','profiles':[{'mask':m,'distance_cm':d,'maximum_instances':n} for m,d,n in [(1,1500,32),(2,2500,64),(28,4000,96)]]})
(R/'Evidence/gameplay-runtime-scalability.json').write_text(json.dumps({'effect_types':report,'budget_approval':False,'scope':'Tunable lab starting limits; essential and gameplay never suppressed by these distance/count profiles. Verify on target hardware before shipping.'},indent=2),encoding='utf-8')
u.SystemLibrary.quit_editor()
