# Manny — laboratório de calibração VFX

Esta passagem usa o **SKM_Manny_Simple** e o esqueleto **SK_Mannequin** existentes no projeto do jogo, copiados apenas para o laboratório. O código nativo atual do jogo aponta para **SKM_Quinn_Simple**; a referência escolhida pelo utilizador para este trabalho é Manny. Não foram alterados o Foundation, o Engine, os sockets originais nem os VFX aprovados.

A primeira passagem está compilada e foi executada no UE 5.8.3: **384 amostras** de ligação/escala e **64 pares efeito/baseline**, com encerramento limpo. Os ossos foram avaliados em quatro poses e três escalas. A inspeção visual confirma a presença e identifica limitações de leitura; não certifica todos os 331 componentes no Manny nem a integração no jogo. Evidência: `Evidence/gameplay-manny-validation.json` e `Evidence/gameplay-manny-checkpoint.json`.

## Ver e comparar

Fazer duplo clique em **Ver-Manny-VFX.cmd**. Selecionar um dos 16 cenários em **Todas as skills**. A velocidade inicial é **1×**.

Para ver os prints sem abrir o UE, abrir o ficheiro local `Evidence/MannyReview/galeria.html`. A galeria apresenta cada cenário nas quatro poses. As folhas `manny-pose0.jpg` a `manny-pose3.jpg` ficam na mesma pasta; os PNG completos estão em `Saved/MannyCaptures`. Estas imagens locais não fazem parte do ZIP de migração ou do Git.

| Controlo | Função |
| --- | --- |
| Anterior / Seguinte, ou setas | Mudar o cenário |
| P | Alternar repouso, ataque, corrida e esquiva |
| E | Alternar escala 0,8×, 1× e 1,2× |
| Espaço | Pausar / continuar |
| R | Reiniciar |
| S | Alternar 1× e 1/3 |

As poses vêm das animações Unarmed locais do UE: MM_Idle, MM_Attack_01, MF_Unarmed_Jog_Fwd e MM_Dash. Servem para verificar que uma ligação acompanha um osso em movimento; **não substituem as animações finais de cada skill ou arma**. A corrida/esquiva são amostradas sem locomotion, colisão ou root-motion de gameplay.

## Ligações verificáveis

| Parte | Origem no rig | Tratamento |
| --- | --- | --- |
| Braço direito/esquerdo | hand_r/l → lowerarm_r/l | Origem e endpoint obtidos da mesma pose; cada braço tem cenário próprio |
| Espada | HandGrip_R → extremidade de uma haste de 75 cm | Haste de teste para fora do antebraço; a orientação final depende dos sockets da arma |
| Stances | pelvis | Compensar a altura já desenhada no shader; não somar novamente a altura da cápsula |
| Guard | spine_03 | O shader começa a altura zero: colocar à frente do peito e orientar o plano para a frente |
| Stun | head no alvo | Colocar o centro acima da cabeça; o shader já contém a altura de referência |
| Root | root no alvo | Alinhar a zona dos pés com a origem do mesh, não com a cápsula |
| Severing | spine_03 no alvo | Compensar os 162 cm já desenhados; a marca continua separada do corte |
| Laser | hand_r → spine_03 do alvo | Endpoints atualizados a partir de ambas as poses |
| Contacto do pé | foot_r projetado no chão do laboratório | Chão plano de teste; a superfície real exige um contacto confirmado |
| Arcane | root | Referência de corpo, sem acrescentar uma segunda altura de peito |

O fixture reproduz a transformação do jogo: origem do actor a 96 cm do chão, mesh filho a −96 cm e yaw −90°. Os helpers de calibração leem os ossos depois de avaliar a pose. A rotação e a escala são aplicadas às instâncias privadas de material. O **runtime nativo atual ainda não recebe a escala do rig como input próprio**; este ajuste pertence ao adaptador do laboratório e precisa de ser promovido e verificado na integração.

## Âmbito desta primeira passagem

16 cenários cobrem 14 componentes distintos. Bleed/Poison mostram um braço de cada vez; a composição simultânea dos dois braços ainda precisa de revisão, porque o binding atual reutiliza um endpoint para as duas entradas gravadas. Rapid Attack conserva coordenadas gravadas e precisa de bindings independentes por braço antes de certificar a ligação ao rig.

A espada usa uma haste cinzenta para medir a pega/extremidade. Nas capturas, o rasto e o Guard têm leitura fraca nesta vista e precisam de outro ângulo e das poses finais antes de aprovação visual. O contacto do pé é deliberadamente discreto. A presença medida por diferença de pixels não substitui esta avaliação de qualidade. A marca Severing testada é apenas a **marca 1**; as marcas 2/3 ainda não têm esta validação no rig.

Ficam para a passagem seguinte os sockets e comprimentos das armas finais, sweeps/contacts reais, notifies nas animações das skills, disparos/projéteis, poses finais de guard/dodge/sprint e comparação com a câmara de gameplay. O palco não confirma dano, hits, CC, recursos ou procs de gameplay: os inputs admitidos/aplicados são fixtures explícitos.

## Preparação noutra máquina

Os assets Manny/animações do UE são locais e estão excluídos do Git e do ZIP VFX. Mantêm o path original, com hashes registados em `Evidence/gameplay-manny-local-reference.json`.

1. Executar `Scripts/prepare_manny_reference.py --game-root <pasta-do-jogo>` com Python.
2. Executar `Scripts/prepare_manny_cases.py`.
3. Executar `Scripts/Build-MannyLab.ps1 -EngineRoot <pasta-UE-5.8>`.
4. Executar `Scripts/Run-LabEditorScript.ps1 -Script create_manny_review.py -LogName Manny-prepare.log`.
5. Executar `Scripts/Open-MannyLab.ps1 -Audit` para recolher a evidência; ou abrir `Ver-Manny-VFX.cmd` para revisão.
6. Executar `Scripts/audit_manny_review.py` para medir as amostras e gerar a galeria. Inspecionar as imagens atuais antes de registar aprovação visual.

Só o módulo separado **SanctaVFXMannyLab** é instalado por esta preparação. As DLLs da ponte VFX existente não são substituídas. Os mapas Manny são fixtures locais reproduzíveis pelo script.
