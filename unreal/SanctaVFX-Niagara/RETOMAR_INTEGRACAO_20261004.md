# Retomar a aplicação da avaliação VFX

## Ponto atual — segunda calibração Manny, 6 de outubro de 2026

**21 cenários / 17 componentes**, quatro poses de teste e três escalas. **504 amostras, 252 pares efeito/baseline em três vistas e 24 imagens de braços isolados passaram**; encerramento UE 0. As 12 folhas correntes e 13 frames completos representativos foram inspecionados. Bleed/Poison/Rapid Attack usam posições independentes das duas mãos/antebraços; espada/Guard têm variantes locais mais legíveis. Marcas Severing 1/2/3 incluídas. Nenhuma execução UE desta tarefa permanece ativa.

**Ver-Capturas-Manny.cmd** abre os prints sem servidor. **Ver-Manny-VFX.cmd** abre as animações a 1×: P muda pose, E escala, V vista e B isola os braços. Ler **MANNY_VFX.md** e `Evidence/gameplay-manny-checkpoint.json`.

As seis variantes estão em **Source/MannyCalibration**, separadas dos componentes gerais. Os novos inputs dos braços e a escala ainda precisam de promoção ao runtime. Espada de 75 cm e poses Unarmed são fixtures: armas/animações/notifies finais, guard/dodge/sprint, roupa/oclusão, câmara real e restantes fases continuam pendentes. Guard planar fica discreto de perfil. Não declarar os 331 componentes calibrados no Manny ou aprovação de produção.

Foundation, Engine, rig original, DLLs Bridge/runtime e assets atuais preservados por hashes. O build de variantes e a preparação do mapa terminaram com código 0; duas tentativas anteriores do harness em Editor completo falharam na simulação e estão registadas. A primeira passagem fica em `Saved/MannyPass1-20261005`. Fontes, guia e registos da segunda passagem publicados no commit `266e13b`, verificado em `origin/main`; capturas e assets Epic/MannyLab continuam locais.

Próximo trabalho: calibração de armas/poses/notifies finais e restantes fases, seguida da promoção autorizada dos adaptadores para o runtime. Não alterar Foundation sem nova autorização.

Checkpoint atualizado em 2026-10-05T13:18:10.697172+00:00. Estado: **lab_verified_awaiting_user_review**. Foundation e Engine preservados.

Runtime compilado, 34 testes nativos de eventos e 56 combinações classe/arma. Materiais privados testados em 401 definições. Estes testes não certificam integração no jogo nem aprovação artística final.

Fontes iguais à última compilação: **True**. Se for False, há correções C++ ainda por compilar/testar; os resultados acima pertencem ao DLL anterior. Aguardar o fim de qualquer execução UE deste laboratório antes de substituir o DLL.

Niagara atual: **331/331** fontes compiladas e simuladas com hashes correspondentes; **0** pendentes. Versões piloto antigas não entram nesta contagem. Preservação: 194 fontes e 247 assets anteriores, resultado True.

Tarefa em execução no momento do checkpoint: nenhuma. Conferir processos/logs ao retomar; o checkpoint não garante que um processo ainda esteja vivo.

Fonte de verdade: `Evidence/gameplay-vfx-implementation-checkpoint-20261004.json`. API: `GUIA_EXECUCAO_VFX.md`. Lote: `Scripts/build_gameplay_vfx.py`, pausa segura entre jobs por `Saved/Stop-gameplay-build.request`. Remover apenas esse ficheiro para retomar.

Estado corrente: 331/331 fontes nativas com hashes correspondentes; 401 resultados de bindings guardados. Conferir o contrato e a assinatura de cada fase após regenerar as definições. O visualizador inicia a 1×. Fireball aprovado e visualizador original de 247 cenas permanecem preservados.

Capturas aceites da compilação atual: **1004**, incluindo **867** do plano completo. O lote anterior interrompido está registado separadamente em `Evidence/runtime-capture-partial-shutdown-20261005.json` (469 imagens, sem aceitação final). A espera pelos shaders dos materiais corrigiu os seis efeitos do diagnóstico atual; evidência em `Evidence/runtime-shader-diagnostic-result.json`. A galeria corrente fica em `Evidence/RuntimeReview/galeria.html`; as folhas `Saved/RuntimeCaptures/Progress` são provisórias.

Validação interna do laboratório concluída. Galeria e ZIP atuais; falta o feedback do utilizador, a calibração no jogo e o orçamento no hardware alvo. Foundation continua protegido. A validação do laboratório não certifica integração Foundation ou qualidade final no jogo. Nenhuma captura ou execução UE desta tarefa permanece ativa.

Git: segunda passagem Manny publicada em origin/main; commit de conteúdo confirmado: 266e13b15eb3c044edb45a2fe0aa6469e3c82a95
