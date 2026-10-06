"""Prepare a verified downloadable handoff without changing the game project."""
import datetime, hashlib, json, pathlib, shutil, zipfile

R=pathlib.Path(__file__).resolve().parents[1]
read=lambda p:json.loads((R/p).read_text(encoding='utf-8-sig'))
digest=lambda b:hashlib.sha256(b).hexdigest()
export=read('Evidence/gameplay-runtime-export.json')
closure=read('Evidence/gameplay-runtime-migration-manifest.json')
compiled=read('Evidence/gameplay-runtime-compiled-sources.json')
archive=R/export['file']
assert digest(archive.read_bytes())==export['sha256']
assert closure['dependency_isolation_passed'] and not closure['pending_components'] and not closure['canonical_pending']
assert export['current_components']==331 and export['canonical_forms']==136 and export['packages']==1786
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    names=z.namelist()
    assert len(names)==len(set(names))
    assert not any(n.startswith('/') or '..' in pathlib.PurePosixPath(n).parts for n in names)
    assert not any('Characters/Mannequins/' in n or 'MannyLab/' in n or '/Binaries/' in n or '/Intermediate/' in n or 'SanctaVFXBridge.uplugin' in n for n in names)
    assert len([n for n in names if n.endswith(('.uasset','.umap'))])==1786
    for row in closure['packages']:
        assert digest(z.read(row['file']))==row['sha256'],row['file']
    source=R/'Plugins/SanctaVFXBridge/Source/SanctaVFXRuntime'
    runtime_sources={}
    for file in source.rglob('*'):
        if file.is_file():
            original=file.relative_to(R).as_posix()
            target='Plugins/SanctaVFXRuntime/Source/SanctaVFXRuntime/'+file.relative_to(source).as_posix()
            assert z.read(target)==file.read_bytes(),target
            assert digest(file.read_bytes())==compiled['files'][original],original
            runtime_sources[target]=digest(file.read_bytes())
    descriptor=json.loads(z.read('Plugins/SanctaVFXRuntime/SanctaVFXRuntime.uplugin'))
    assert descriptor['Modules']==[{'Name':'SanctaVFXRuntime','Type':'Runtime','LoadingPhase':'Default'}]
    assert descriptor['Plugins']==[{'Name':'Niagara','Enabled':True}]
    for p in ['INTEGRAR_NO_PROJETO.md','GUIA_EXECUCAO_VFX.md','GUIA_VFX.html','GUIA_VFX.md','MANNY_VFX.md','MANNY_VFX_TODOS.md','Evidence/gameplay-manny-full-binding-index.json']:
        assert z.read(p)==(R/p).read_bytes(),p

destination=R.parents[1]/'integration/vfx-runtime-ue5.8.3'
destination.mkdir(parents=True,exist_ok=True)
shutil.copy2(archive,destination/archive.name)
report={**export,'prepared_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'file':archive.name,'runtime_source_files':runtime_sources,
        'archive_crc_passed':True,'package_hashes_passed':True,'runtime_sources_match_compiled':True,
        'foundation_modified':False,'runtime_manny_adapter_promoted':False,
        'runtime_build_jobs_sha256':digest((R/'Evidence/gameplay-runtime-build-jobs.json').read_bytes()),
        'manny_binding_index_sha256':digest((R/'Evidence/gameplay-manny-full-binding-index.json').read_bytes())}
(destination/'manifest.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
(destination/'SHA256SUMS').write_text(f"{export['sha256']}  {archive.name}\n",encoding='ascii')
(destination/'README.md').write_text('''# VFX — entrega para integração no projeto principal

**UE 5.8.3 · 331 componentes · 136 FormIds · 1786 packages.**

Descarregar [Sancta-VFX-Runtime.zip](Sancta-VFX-Runtime.zip) através de **Download raw** no GitHub. Descompactar e começar em **INTEGRAR_NO_PROJETO.md**, incluído no ZIP e [disponível no repositório](../../unreal/SanctaVFX-Niagara/INTEGRAR_NO_PROJETO.md).

O ZIP contém `Content`, o plugin standalone `Plugins/SanctaVFXRuntime` com fontes C++, guia pesquisável, contratos, índice e receitas Manny. Copiar Content/Plugins para os caminhos correspondentes do projeto e compilar com UE 5.8.3. Ligar os eventos, actores, sockets e fases através da API documentada.

`SHA256SUMS` permite conferir o download. `manifest.json` regista a validação dos hashes de todos os packages, das fontes compiladas e da integridade do ZIP.

As ligações ao gameplay, armas/animações finais e promoção do adaptador privado Manny continuam pendentes. O ZIP não inclui Foundation, Engine, DLLs do laboratório, módulo editor Manny ou assets Epic da personagem. Nenhuma alteração foi aplicada ao projeto principal.

As fontes editáveis de calibração ficam em [Source/MannyCalibration](../../unreal/SanctaVFX-Niagara/Source/MannyCalibration); a implementação do adaptador de referência fica no [módulo editor do laboratório](../../unreal/SanctaVFX-Niagara/Plugins/SanctaVFXMannyLab/Source). Servem de referência para a promoção ao runtime, não de plugin Shipping a instalar.
''',encoding='utf-8')
print(json.dumps({'directory':str(destination),'bytes':export['bytes'],'packages':1786,'components':331,'sha256':export['sha256'],'verified':True}))
