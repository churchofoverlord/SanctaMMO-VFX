"""Record only a successful deployed build whose host copies match the source."""
import pathlib, hashlib, json, datetime
root=pathlib.Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
log=root/'Saved/Bridge-build.log'
if 'Result: Succeeded' not in log.read_text(encoding='utf-8-sig'):
    raise RuntimeError('Successful build result missing')
files={}
for p in (root/'BuildHost/Plugins/SanctaVFXBridge/Source').rglob('*'):
    if p.is_file():
        relative=p.relative_to(root/'BuildHost').as_posix()
        if not (root/relative).is_file() or sha(p)!=sha(root/relative):
            raise RuntimeError('Build host/source mismatch: '+relative)
        files[relative]=sha(p)
modules={}
for name in ['SanctaVFXBridge','SanctaVFXRuntime']:
    relative='Plugins/SanctaVFXBridge/Binaries/Win64/UnrealEditor-'+name+'.dll'
    if sha(root/relative)!=sha(root/'BuildHost'/relative):
        raise RuntimeError('Deployed DLL differs from build host')
    modules[relative]=sha(root/relative)
report={'files':files,'modules':modules,'build_log':'Saved/Bridge-build.log','build_exit_code':0,'recorded_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(root/'Evidence/gameplay-runtime-compiled-sources.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'source_files':len(files),'deployed_modules':len(modules)}))
