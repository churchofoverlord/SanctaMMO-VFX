"""Reconcile current source hashes and verified evidence; safe while a batch runs."""
import json,pathlib,hashlib,datetime,argparse
from runtime_capture_signatures import CaptureSignatures
R=pathlib.Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--running',default='');parser.add_argument('--paused',action='store_true');parser.add_argument('--lab-complete',action='store_true');parser.add_argument('--git-saved',default='');args=parser.parse_args()
if args.paused and args.running:parser.error('A paused checkpoint cannot have a running task.')
def read(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def write(p,d):(R/p).write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();jobs=read('Evidence/gameplay-runtime-build-jobs.json')['jobs'];native=read('Evidence/gameplay-runtime-native-assets.json');current=[];pending=[]
compiled_manifest=read('Evidence/gameplay-runtime-compiled-sources.json') if (R/'Evidence/gameplay-runtime-compiled-sources.json').exists() else {'files':{}}
source_matches_compiled=bool(compiled_manifest['files']) and all((R/p).is_file() and sha(R/p)==h for p,h in compiled_manifest['files'].items())
for job in jobs:
 p=R/job['source'];data=json.loads(p.with_suffix('.port.json').read_text(encoding='utf-8'));data['runtime_emitter_revision']='identity_orientation_persistent_v2'
 for layer in data['layers']:layer['native_shared_root']='/Game/Sancta/VFX/Common'
 entry=native['assets'].get(job['slug'],{});asset=R/'Content'/(entry.get('asset','').removeprefix('/Game/').split('.')[0]+'.uasset')
 valid=entry.get('source_sha256')==sha(p) and entry.get('port_sha256')==hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest() and asset.is_file()
 if valid:current.append({'slug':job['slug'],'source':job['source'],'asset':entry['asset'],'asset_sha256':sha(asset)})
 else:pending.append(job['slug'])
baseline=read('Evidence/gameplay-implementation-preservation-baseline.json');mismatches=[]
for group in ['current_editable_sources','native_assets']:
 for path,digest in baseline[group].items():
  p=R/path
  if not p.is_file() or sha(p)!=digest:mismatches.append(path)
preservation={'checked_at_utc':stamp,'source_count':len(baseline['current_editable_sources']),'asset_count':len(baseline['native_assets']),'passed':not mismatches,'mismatches':mismatches}
write('Evidence/gameplay-runtime-preservation-validation.json',preservation)
tests=read('Evidence/gameplay-runtime-native-validation.json');basic=read('Evidence/gameplay-basic-routing-validation.json') if (R/'Evidence/gameplay-basic-routing-validation.json').exists() else {}
defs=read('Evidence/gameplay-runtime-definitions.json');materials=read('Evidence/gameplay-runtime-material-validation.json')
files=[]
for directory in ['Plugins/SanctaVFXBridge/Source/SanctaVFXRuntime']:
 for path in (R/directory).rglob('*'):
  if path.is_file():files.append({'path':path.relative_to(R).as_posix(),'sha256':sha(path),'bytes':path.stat().st_size})
checkpoint={'schema':'sancta-gameplay-vfx-implementation-checkpoint/v2','updated_at_utc':stamp,'status':'in_progress','user_request':'retoma','objective':'Aplicar a avaliação às skills, básicos das 14 armas e Guard/Dodge/Sprint no laboratório independente.','compiled':True,'native_event_tests_passed':tests.get('passed',False),'native_event_cases':len(tests.get('tests',[])),'native_basic_routing_passed':basic.get('passed',False),'basic_cases':basic.get('cases',0),'material_definitions_tested':materials.get('definitions_tested',0),'material_tests_passed':materials.get('passed',False),'runtime_job_count':len(jobs),'current_native_count':len(current),'pending_native_count':len(pending),'current_native_assets':current,'pending_native_slugs':pending,'definition_count':len(defs['definitions']),'canonical_pending':defs['canonical_pending'],'background_running':bool(args.running),'background_task':args.running,'files_written':files,'preservation':preservation,'completed_this_run':['Runtime registado e compilado: eventos, anchors/sockets, materiais privados, estados, remoção, LifeId e deduplicação.','Anim Notify e seleção nativa de 14 armas × 4 Primaries.','Fontes derivadas separadas para skills, recursos, casts/links/áreas e CC, sem modificar arte aprovada.','Terreno Iceberg com colisão nativa e integridade/remoção, validado no laboratório.','136 FormIds canónicos com snapshot de modo/stance e aliases de componentes.','Effect Types Essential/Gameplay/Decorative criados no Unreal.','Capturas PIE reais e medição preliminar 0/1/16/48 instâncias; sem aprovação de orçamento.'],'remaining':['Concluir todas as fontes atuais no Niagara e resolver as falhas do lote.','Concluir e auditar todas as composições e bindings; manifest de migration/cook explícito.','Rever as capturas GPU atuais, incluindo fases breves, áreas, estados e fundos claros; verificar Low/High.','Concluir orçamento/performance na câmara e hardware alvo.','Integração do Foundation, transporte de eventos/replicação e rigs reais continuam fora do laboratório e sem autorização para modificar o projeto protegido.'],'production_approved':False,'foundation_modified':False,'viewer_default_speed':1.0}
previous=read('Evidence/gameplay-vfx-implementation-checkpoint-20261004.json')
checkpoint['uncompiled_changes']=[] if source_matches_compiled else ['Source differs from the recorded deployed build.']
checkpoint['next_commands_after_active_batch']=['Audit current game-viewport captures.','Complete bright/Low/terrain/performance checks.','Review and save the explicit migration package.']
checkpoint['source_matches_compiled']=source_matches_compiled
checkpoint['compiled_binary_available']=True
checkpoint['compiled']=source_matches_compiled
capture_registry=read('Evidence/gameplay-runtime-capture-frames.json')
capture_frames=capture_registry.get('frames',{})
signatures=CaptureSignatures(R)
capture_context_matches=capture_registry.get('render_context')==signatures.render_context
accepted={name:row for name,row in capture_frames.items() if signatures.valid(row) and (R/row['file']).is_file() and sha(R/row['file'])==row['sha256']} if capture_context_matches else {}
full_plan=read('Evidence/runtime-capture-plan.json')
accepted_all=sum(case['name'] in accepted and accepted[case['name']]['component_signature']==signatures.signature(case) for case in full_plan)
checkpoint['capture_acceptance']={'context_matches_current_build':capture_context_matches,'accepted_frames':len(accepted),'accepted_all_frames':accepted_all,'planned_all_frames':len(full_plan),'quality_approved':False}
checkpoint['phase_repair_plan']='Evidence/runtime-phase-repair-plan-20261005.json'
checkpoint['export_requires_refresh']=True
checkpoint['git_commit_push_pending']=True
checkpoint['completed_this_run'] += [f'{len(current)}/{len(jobs)} fontes atuais compiladas e simuladas; {len(pending)} pendentes.',f'{materials.get("definitions_tested",0)} resultados de bindings guardados; conferir assinaturas após as alterações.',f'{len(tests.get("tests",[]))} testes de eventos e {basic.get("cases",0)} combinações classe/arma; arranque a 1×.']
checkpoint['remaining']=['Concluir e inspecionar as capturas correntes das fases; preservar o lote anterior com os respetivos hashes.','Concluir 94 casos de contraste/Low/terreno, 27 casos de recursos/hold, quatro medições de performance e controlos do visualizador.','Atualizar o pacote de migração após QA e guardar a revisão em Git com scope explícito, seguida de push.','Aprovação da forma de Glacial/Iceberg, rigs e orçamento no hardware alvo continuam pendentes.','Integração Foundation e transporte de eventos/replicação continuam fora do laboratório protegido.']
checkpoint['next_commands_after_active_batch']=['Register only the exact completed capture batch after UE exit 0.','Audit and inspect the current full plan, Low/bright/terrain and resource/hold captures.','Record performance and viewer checks, then refresh export and explicit Git scope.']
if args.lab_complete:
 if pending or mismatches or not source_matches_compiled or accepted_all!=len(full_plan):raise RuntimeError('Current native sources/preservation/captures incomplete')
 for file in ['gameplay-runtime-phase-contracts.json','gameplay-runtime-viewer-validation.json','gameplay-runtime-art-review.json','gameplay-runtime-performance-validation.json']:
  if not read('Evidence/'+file).get('passed'):raise RuntimeError('Incomplete lab validation: '+file)
 for file in ['gameplay-runtime-quality-captures.json','gameplay-runtime-control-captures.json']:
  if read('Evidence/'+file).get('manual_visual_review')!='completed':raise RuntimeError('Unreviewed captures: '+file)
 export=read('Evidence/gameplay-runtime-export.json')
 if export.get('current_components')!=len(jobs) or sha(R/export['file'])!=export['sha256']:raise RuntimeError('Export missing or stale')
 checkpoint.update(status='lab_verified_awaiting_user_review',background_running=False,background_task='',export_requires_refresh=False)
 checkpoint['remaining']=['Feedback do utilizador sobre as formas Glacial/Iceberg e as novas apresentações.','Calibrar sockets/rigs, câmaras, colisão, transporte de eventos/replicação e cook Shipping no projeto do jogo quando autorizado.','Validar orçamento e concorrência na câmara/hardware alvo; não extrapolar timings do palco PIE.','Guardar a revisão atual em Git e push imediato.']
 if args.git_saved:
  import subprocess
  local=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
  remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=R,text=True).split()[0]
  if args.git_saved!=local or local!=remote:raise RuntimeError('Git save has not reached origin/main')
  checkpoint['git_commit_push_pending']=False
  checkpoint['git_saved_commit']=local
  checkpoint['remaining']=checkpoint['remaining'][:-1]
if args.paused:
 checkpoint.update(status='paused_by_user',user_request='prepara-te que vou ter de desligar',background_running=False,background_task='',shutdown_safe=True)
 checkpoint['partial_capture_evidence']='Evidence/runtime-capture-partial-shutdown-20261005.json'
 checkpoint['export_requires_refresh']=True
 checkpoint['git_commit_push_pending']=True
write('Evidence/gameplay-vfx-implementation-checkpoint-20261004.json',checkpoint)
status=read('VFX-status.json');status['gameplay_vfx_implementation']={'status':'in_progress','checkpoint':'Evidence/gameplay-vfx-implementation-checkpoint-20261004.json','source_files_created':len(files),'compiled':source_matches_compiled,'source_matches_compiled':source_matches_compiled,'native_event_tests_passed':tests.get('passed',False),'basic_routing_tests_passed':basic.get('passed',False),'runtime_jobs':len(jobs),'current_native_assets':len(current),'pending_native_assets':len(pending),'assets_modified':True,'background_running':bool(args.running),'updated_at_utc':stamp,'production_approved':False,'foundation_modified':False};write('VFX-status.json',status)
status['gameplay_vfx_implementation']['status']=checkpoint['status']
status['gameplay_vfx_implementation']['background_task']=checkpoint['background_task']
write('VFX-status.json',status)
final_status = ('Validação interna do laboratório concluída. Galeria e ZIP atuais; falta o feedback do utilizador, '
 'a calibração no jogo e o orçamento no hardware alvo. Foundation continua protegido.' if args.lab_complete else
 f"Falta concluir o plano completo de {checkpoint['capture_acceptance']['planned_all_frames']} imagens corrente, "
 'contraste/Low/terreno, recursos/hold e performance. Atualizar o ZIP de migração, rever o scope explícito '
 'de Git, fazer commit em main e push imediato.')
git_status = ('Revisão guardada em origin/main; commit confirmado: '+checkpoint['git_saved_commit'] if not checkpoint['git_commit_push_pending'] else
 'Commit/push ainda pendentes. Os ficheiros estão locais; confirmar o estado de aprovação em Evidence/runtime-phase-repair-plan-20261005.json antes de publicar.')
text=f'''# Retomar a aplicação da avaliação VFX

Checkpoint atualizado em {stamp}. Estado: **{checkpoint['status']}**. Foundation e Engine preservados.

Runtime compilado, {len(tests.get('tests',[]))} testes nativos de eventos e {basic.get('cases',0)} combinações classe/arma. Materiais privados testados em {materials.get('definitions_tested',0)} definições. Estes testes não certificam integração no jogo nem aprovação artística final.

Fontes iguais à última compilação: **{source_matches_compiled}**. Se for False, há correções C++ ainda por compilar/testar; os resultados acima pertencem ao DLL anterior. Aguardar o fim de qualquer execução UE deste laboratório antes de substituir o DLL.

Niagara atual: **{len(current)}/{len(jobs)}** fontes compiladas e simuladas com hashes correspondentes; **{len(pending)}** pendentes. Versões piloto antigas não entram nesta contagem. Preservação: {preservation['source_count']} fontes e {preservation['asset_count']} assets anteriores, resultado {preservation['passed']}.

Tarefa em execução no momento do checkpoint: {args.running or 'nenhuma'}. Conferir processos/logs ao retomar; o checkpoint não garante que um processo ainda esteja vivo.

Fonte de verdade: `Evidence/gameplay-vfx-implementation-checkpoint-20261004.json`. API: `GUIA_EXECUCAO_VFX.md`. Lote: `Scripts/build_gameplay_vfx.py`, pausa segura entre jobs por `Saved/Stop-gameplay-build.request`. Remover apenas esse ficheiro para retomar.

Estado corrente: {len(current)}/{len(jobs)} fontes nativas com hashes correspondentes; {materials.get('definitions_tested',0)} resultados de bindings guardados. Conferir o contrato e a assinatura de cada fase após regenerar as definições. O visualizador inicia a 1×. Fireball aprovado e visualizador original de 247 cenas permanecem preservados.

Capturas aceites da compilação atual: **{checkpoint['capture_acceptance']['accepted_frames']}**, incluindo **{checkpoint['capture_acceptance']['accepted_all_frames']}** do plano completo. O lote anterior interrompido está registado separadamente em `Evidence/runtime-capture-partial-shutdown-20261005.json` (469 imagens, sem aceitação final). A espera pelos shaders dos materiais corrigiu os seis efeitos do diagnóstico atual; evidência em `Evidence/runtime-shader-diagnostic-result.json`. A galeria corrente fica em `Evidence/RuntimeReview/galeria.html`; as folhas `Saved/RuntimeCaptures/Progress` são provisórias.

{final_status} A validação do laboratório não certifica integração Foundation ou qualidade final no jogo. {'Execução em curso: '+args.running if args.running else 'Nenhuma captura ou execução UE desta tarefa permanece ativa.'}

Git: {git_status}
'''
(R/'RETOMAR_INTEGRACAO_20261004.md').write_text(text,encoding='utf-8')
print(json.dumps({'current':len(current),'total':len(jobs),'pending':len(pending),'preserved':preservation['passed'],'running':args.running}))
