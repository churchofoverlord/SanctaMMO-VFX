"""Export the verified explicit dependency closure and the independent runtime module."""
import pathlib, json, hashlib, zipfile, datetime
root=pathlib.Path(__file__).resolve().parents[1]
read=lambda p:json.loads((root/p).read_text(encoding='utf-8-sig'))
manifest=read('Evidence/gameplay-runtime-migration-manifest.json')
if not manifest['dependency_isolation_passed'] or manifest['pending_components'] or manifest['canonical_pending']:
    raise RuntimeError('Dependency closure is incomplete')
compiled=read('Evidence/gameplay-runtime-compiled-sources.json')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for path,digest in compiled['files'].items():
    if sha(root/path)!=digest:raise RuntimeError('Uncompiled source change: '+path)
out=root/'Exports';out.mkdir(exist_ok=True)
destination=out/'Sancta-VFX-Runtime.zip'
plugin={'FileVersion':3,'Version':1,'VersionName':'2026.10.05-lab','FriendlyName':'Sancta VFX Runtime','Description':'Local event-driven presentation; gameplay transport is supplied by the game.','Category':'VFX','CanContainContent':False,'Plugins':[{'Name':'Niagara','Enabled':True}],'Modules':[{'Name':'SanctaVFXRuntime','Type':'Runtime','LoadingPhase':'Default'}]}
metadata={'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'engine':'UE 5.8.3','packages':len(manifest['packages']),'canonical_forms':len(read('Evidence/gameplay-runtime-form-routes.json')['routes']),'current_components':len(read('Evidence/gameplay-runtime-build-jobs.json')['jobs']),'production_approved':False,'foundation_modified':False,'remaining_game_work':['Ability/event transport and authority integration','Actual rig sockets and ground placement','Foundation projectile/terrain channels and navigation','Shipping cook and performance budget on target hardware'],'layout':'Merge Content into game Content; install standalone Plugins/SanctaVFXRuntime. Do not install the authoring Bridge in the shipping game.'}
with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as bundle:
    for row in manifest['packages']:
        file=root/row['file']
        if not file.is_file() or sha(file)!=row['sha256']:raise RuntimeError('Package changed since closure audit: '+row['file'])
        bundle.write(file,row['file'])
    source=root/'Plugins/SanctaVFXBridge/Source/SanctaVFXRuntime'
    for file in source.rglob('*'):
        if file.is_file():bundle.write(file,'Plugins/SanctaVFXRuntime/Source/SanctaVFXRuntime/'+file.relative_to(source).as_posix())
    bundle.writestr('Plugins/SanctaVFXRuntime/SanctaVFXRuntime.uplugin',json.dumps(plugin,indent=2))
    for path in ['GUIA_EXECUCAO_VFX.md','Evidence/gameplay-runtime-migration-manifest.json','Evidence/gameplay-runtime-form-routes.json','Evidence/gameplay-runtime-definitions.json','Evidence/gameplay-runtime-rig-reference.json']:
        bundle.write(root/path,path)
    bundle.writestr('PACOTE.json',json.dumps(metadata,indent=2,ensure_ascii=False))
report={**metadata,'file':destination.relative_to(root).as_posix(),'sha256':sha(destination),'bytes':destination.stat().st_size}
(root/'Evidence/gameplay-runtime-export.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'export':report['file'],'packages':report['packages'],'bytes':report['bytes']}))
