# Retomar a aplicação da avaliação VFX

## Manny — primeira passagem atual

Palco **Ver-Manny-VFX.cmd**: 16 cenários/14 componentes, quatro poses e três escalas; velocidade inicial 1×. P muda pose; E muda escala. 384 amostras e 64 pares efeito/baseline passaram; a execução final encerrou com código 0. A inspeção das capturas identificou leitura fraca da espada/Guard nesta vista.

Ler **MANNY_VFX.md** e `Evidence/gameplay-manny-checkpoint.json`. Galeria local: `Evidence/MannyReview/galeria.html`. A composição dos braços/Rapid Attack, armas e animações finais, marcas Severing 2/3 e câmara real continuam pendentes. O adaptador de escala é local; não declarar calibração dos 331 componentes no Manny. Foundation/Engine preservados; UE desta tarefa encerrado.

Checkpoint atualizado em 2026-10-05T13:18:10.697172+00:00. Estado: **lab_verified_awaiting_user_review**. Foundation e Engine preservados.

Runtime compilado, 34 testes nativos de eventos e 56 combinações classe/arma. Materiais privados testados em 401 definições. Estes testes não certificam integração no jogo nem aprovação artística final.

Fontes iguais à última compilação: **True**. Se for False, há correções C++ ainda por compilar/testar; os resultados acima pertencem ao DLL anterior. Aguardar o fim de qualquer execução UE deste laboratório antes de substituir o DLL.

Niagara atual: **331/331** fontes compiladas e simuladas com hashes correspondentes; **0** pendentes. Versões piloto antigas não entram nesta contagem. Preservação: 194 fontes e 247 assets anteriores, resultado True.

Tarefa em execução no momento do checkpoint: nenhuma. Conferir processos/logs ao retomar; o checkpoint não garante que um processo ainda esteja vivo.

Fonte de verdade: `Evidence/gameplay-vfx-implementation-checkpoint-20261004.json`. API: `GUIA_EXECUCAO_VFX.md`. Lote: `Scripts/build_gameplay_vfx.py`, pausa segura entre jobs por `Saved/Stop-gameplay-build.request`. Remover apenas esse ficheiro para retomar.

Estado corrente: 331/331 fontes nativas com hashes correspondentes; 401 resultados de bindings guardados. Conferir o contrato e a assinatura de cada fase após regenerar as definições. O visualizador inicia a 1×. Fireball aprovado e visualizador original de 247 cenas permanecem preservados.

Capturas aceites da compilação atual: **1004**, incluindo **867** do plano completo. O lote anterior interrompido está registado separadamente em `Evidence/runtime-capture-partial-shutdown-20261005.json` (469 imagens, sem aceitação final). A espera pelos shaders dos materiais corrigiu os seis efeitos do diagnóstico atual; evidência em `Evidence/runtime-shader-diagnostic-result.json`. A galeria corrente fica em `Evidence/RuntimeReview/galeria.html`; as folhas `Saved/RuntimeCaptures/Progress` são provisórias.

Validação interna do laboratório concluída. Galeria e ZIP atuais; falta o feedback do utilizador, a calibração no jogo e o orçamento no hardware alvo. Foundation continua protegido. A validação do laboratório não certifica integração Foundation ou qualidade final no jogo. Nenhuma captura ou execução UE desta tarefa permanece ativa.

Git: primeira passagem Manny, guia e registos publicados em origin/main; commit de conteúdo confirmado: 48ccc28e9fb58fb6a8d49576737e9609300de5df
