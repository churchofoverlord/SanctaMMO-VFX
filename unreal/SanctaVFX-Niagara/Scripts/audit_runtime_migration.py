"""Explicit current dependency closure: reject lab demonstrations in runtime migration."""
import unreal as u,json,pathlib,hashlib
R=pathlib.Path(u.Paths.project_dir());registry=u.AssetRegistryHelpers.get_asset_registry()
report=json.loads((R/'Evidence/gameplay-runtime-definitions.json').read_text(encoding='utf-8'))
native=json.loads((R/'Evidence/gameplay-runtime-native-assets.json').read_text(encoding='utf-8'))
jobs=json.loads((R/'Evidence/gameplay-runtime-build-jobs.json').read_text(encoding='utf-8'))['jobs']
packages={d['asset'].split('.')[0] for d in report['definitions']}
packages.update(['/Game/Sancta/VFX/Terrain/Iceberg/SM_IcebergBody','/Game/Sancta/VFX/Terrain/Iceberg/M_IcebergBody'])
options=u.AssetRegistryDependencyOptions(include_soft_package_references=True,include_hard_package_references=True)
queue=list(packages);seen=set();forbidden=[]
while queue:
 package=queue.pop()
 if package in seen:continue
 seen.add(package)
 for dep in registry.get_dependencies(package,options):
  name=str(dep)
  if name.startswith('/Game/'):
   if not name.startswith('/Game/Sancta/VFX/') or name.startswith('/Game/Sancta/VFX/Review/'):forbidden.append({'from':package,'dependency':name})
   queue.append(name)
rows=[]
for package in sorted(seen):
 file=R/'Content'/(package.removeprefix('/Game/')+'.uasset')
 if file.is_file():rows.append({'package':package,'file':file.relative_to(R).as_posix(),'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
result={'schema':'sancta-runtime-migration/v1','production_approved':False,'foundation_modified':False,'packages':rows,'forbidden_dependencies':forbidden,'dependency_isolation_passed':not forbidden,'canonical_pending':report['canonical_pending'],'pending_components':report['pending_components'],'runtime_module':'Plugins/SanctaVFXBridge/Source/SanctaVFXRuntime','cook_rule':'Use this explicit current package list; do not recursively cook the lab or Review directories. Historical derivatives and orphan pilot DataAssets are excluded.','scope':'Native asset-registry dependency isolation and source/package hash manifest; shipping cook, actual game sockets and multiplayer transport remain separate.'}
(R/'Evidence/gameplay-runtime-migration-manifest.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
if forbidden:raise RuntimeError('Runtime assets still depend on lab demonstration packages')
u.log('SanctaMigration verified packages='+str(len(rows)))
