# Retomar a aplicação da avaliação VFX

Checkpoint atualizado em 2026-10-05T12:35:38.905717+00:00. Estado: **lab_verified_awaiting_user_review**. Foundation e Engine preservados.

Runtime compilado, 34 testes nativos de eventos e 56 combinações classe/arma. Materiais privados testados em 401 definições. Estes testes não certificam integração no jogo nem aprovação artística final.

Fontes iguais à última compilação: **True**. Se for False, há correções C++ ainda por compilar/testar; os resultados acima pertencem ao DLL anterior. Aguardar o fim de qualquer execução UE deste laboratório antes de substituir o DLL.

Niagara atual: **331/331** fontes compiladas e simuladas com hashes correspondentes; **0** pendentes. Versões piloto antigas não entram nesta contagem. Preservação: 194 fontes e 247 assets anteriores, resultado True.

Tarefa em execução no momento do checkpoint: nenhuma. Conferir processos/logs ao retomar; o checkpoint não garante que um processo ainda esteja vivo.

Fonte de verdade: `Evidence/gameplay-vfx-implementation-checkpoint-20261004.json`. API: `GUIA_EXECUCAO_VFX.md`. Lote: `Scripts/build_gameplay_vfx.py`, pausa segura entre jobs por `Saved/Stop-gameplay-build.request`. Remover apenas esse ficheiro para retomar.

Estado corrente: 331/331 fontes nativas com hashes correspondentes; 401 resultados de bindings guardados. Conferir o contrato e a assinatura de cada fase após regenerar as definições. O visualizador inicia a 1×. Fireball aprovado e visualizador original de 247 cenas permanecem preservados.

Capturas aceites da compilação atual: **1004**, incluindo **867** do plano completo. O lote anterior interrompido está registado separadamente em `Evidence/runtime-capture-partial-shutdown-20261005.json` (469 imagens, sem aceitação final). A espera pelos shaders dos materiais corrigiu os seis efeitos do diagnóstico atual; evidência em `Evidence/runtime-shader-diagnostic-result.json`. A galeria corrente fica em `Evidence/RuntimeReview/galeria.html`; as folhas `Saved/RuntimeCaptures/Progress` são provisórias.

Validação interna do laboratório concluída. Galeria e ZIP atuais; falta o feedback do utilizador, a calibração no jogo e o orçamento no hardware alvo. Foundation continua protegido. A validação do laboratório não certifica integração Foundation ou qualidade final no jogo. Nenhuma captura ou execução UE desta tarefa permanece ativa.

Git: Commit/push ainda pendentes. Os ficheiros estão locais; confirmar o estado de aprovação em Evidence/runtime-phase-repair-plan-20261005.json antes de publicar.
