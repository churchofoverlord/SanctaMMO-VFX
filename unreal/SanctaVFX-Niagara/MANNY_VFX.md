# Manny — laboratório de calibração VFX

Esta segunda passagem usa o **SKM_Manny_Simple** e o esqueleto **SK_Mannequin** existentes no projeto do jogo, copiados apenas para o laboratório. O código nativo atual do jogo aponta para **SKM_Quinn_Simple**; a referência escolhida pelo utilizador para este trabalho é Manny. Foundation, Engine, sockets originais e VFX aprovados foram preservados.

O palco separado contém **21 cenários / 17 componentes distintos**, quatro poses e escalas 0,8× / 1× / 1,2×. A auditoria cobre **504 amostras**, **252 pares efeito/baseline** em três vistas e **24 imagens de braços isolados**. O resultado corrente e a inspeção das imagens ficam em `Evidence/gameplay-manny-validation.json`; o ponto de retoma está em `Evidence/gameplay-manny-checkpoint.json`. Esta cobertura não certifica os 331 componentes no Manny nem a integração no jogo.

## Ver e comparar

Para ver os prints, fazer duplo clique em **Ver-Capturas-Manny.cmd**. Abre uma galeria local sem servidor ou UE. Escolher **3/4**, **Frente**, **Lado** ou **Todas**. Cada cenário apresenta repouso, ataque, corrida e esquiva.

Para ver as animações, fazer duplo clique em **Ver-Manny-VFX.cmd**, depois selecionar um dos 21 cenários em **Todas as skills**. A velocidade inicial é **1×**.

| Controlo | Função |
| --- | --- |
| Anterior / Seguinte, ou setas | Mudar o cenário |
| P | Alternar repouso, ataque, corrida e esquiva |
| E | Alternar escala 0,8×, 1× e 1,2× |
| V | Alternar vista 3/4, frente e lado |
| B | Nos cenários de braços, mostrar ambos, direito ou esquerdo |
| Espaço | Pausar / continuar |
| R | Reiniciar |
| S | Alternar 1× e 1/3 |

A galeria fica em `Evidence/MannyReview/galeria.html`; as 12 folhas `manny-pose0-view0.jpg` a `manny-pose3-view2.jpg` estão na mesma pasta. Os PNG completos e as imagens `_right` / `_left` ficam em `Saved/MannyCaptures`. Estes ficheiros locais não fazem parte do ZIP de migração ou do Git. As folhas antigas sem `view` pertencem à primeira passagem, não à validação corrente.

As poses vêm das animações Unarmed locais do UE: MM_Idle, MM_Attack_01, MF_Unarmed_Jog_Fwd e MM_Dash. Verificam que uma ligação acompanha um osso em movimento; **não substituem as animações finais de cada skill ou arma**. Corrida/esquiva são amostradas sem locomotion, colisão ou root-motion de gameplay.

## Ligações e variantes

| Parte | Origem no rig | Tratamento |
| --- | --- | --- |
| Bleed / Poison / Rapid Attack | hand_r → lowerarm_r e hand_l → lowerarm_l | Quatro posições da mesma pose, com identidade e máscara independentes por braço |
| Espada | HandGrip_R → extremidade de 75 cm | Haste de calibração; só os extremos têm marcadores cinzentos, para não tapar o rasto |
| Stances | pelvis | Compensar a altura já desenhada no shader |
| Guard | spine_03 | Plano à frente do peito, com cor ajustada para leitura no Manny |
| Stun | head no alvo | Centro acima da cabeça, compensando a altura gravada |
| Root | root no alvo | Zona dos pés alinhada com o mesh, não com a cápsula |
| Severing 1 / 2 / 3 | spine_03 no alvo | Compensar os 162 cm gravados; marca separada do corte e escolhida pela sequência no alvo |
| Laser | hand_r → spine_03 do alvo | Endpoints atualizados a partir de ambas as poses |
| Contacto do pé | foot_r projetado no chão do laboratório | Chão plano; o jogo exige contacto confirmado com a superfície |
| Arcane | root | Referência de corpo, sem adicionar uma segunda altura de peito |

O fixture reproduz a transformação do jogo: origem do actor a 96 cm do chão, mesh filho a −96 cm e yaw −90°. Os helpers leem os ossos depois de avaliar a pose. Rotação e escala são aplicadas às instâncias privadas de material.

As seis variantes editáveis estão em **Source/MannyCalibration**: Bleed, Poison, Rapid Attack, Guard e rastos de espada física/mágica. Os respetivos Niagara/materials estão localmente em `/Game/Sancta/VFX/MannyLab`. Os componentes gerais conservam as suas fontes e assets anteriores.

Nos braços, `aArm` conserva a identidade direita/esquerda do slot. O adaptador fornece `RuntimeRightOrigin`, `RuntimeRightEndpoint`, `RuntimeLeftOrigin` e `RuntimeLeftEndpoint` no espaço local do owner; `RuntimeArmMask` seleciona direito (1), esquerdo (2) ou ambos (3). Rapid Attack parte da mão em direção ao antebraço. Bleed/Poison mantêm esfera e cone por mão. Não aumentaram as camadas ou os slots de partículas. O rasto de espada foi ligeiramente alargado e o Guard recebeu uma cor mais legível.

**Estes inputs independentes e o adaptador de escala ainda pertencem ao laboratório.** Precisam de ser promovidos para o runtime e verificados na integração autorizada. Não instalar o módulo editor Manny no jogo Shipping nem assumir que o ZIP já contém essas ligações.

## Limites e trabalho seguinte

As vistas adicionais permitem rever espada/Guard e as marcas Severing 1/2/3 no rig. A espada continua a ser uma referência de 75 cm, sem mesh ou eixos da arma final. Guard precisa da pose final de defesa. O contacto do pé é discreto e usa chão plano. Roupa, armadura, oclusão, câmara de gameplay e qualidade Low ainda precisam de comparação neste rig.

O próximo passo é calibrar base/ponta/muzzle das armas finais e os notifies das skills, alargar a cobertura às restantes fases e promover as ligações ao runtime. Sweeps, contactos, projéteis, guard/dodge/sprint, duração e remoção dependem de eventos confirmados do jogo. Este palco usa inputs explícitos de teste; não confirma dano, hits, CC, recursos ou procs de gameplay.

## Preparação noutra máquina

Os assets Manny/animações do UE são locais e estão excluídos do Git e do ZIP VFX. Mantêm o path original, com hashes em `Evidence/gameplay-manny-local-reference.json`. São necessários os assets atuais do laboratório e a ponte já compilada.

1. Executar `Scripts/prepare_manny_reference.py --game-root <pasta-do-jogo>` com Python.
2. Executar `Scripts/prepare_manny_bindings.py` para gerar as seis fontes de calibração.
3. Executar `Scripts/Build-MannyLab.ps1 -EngineRoot <pasta-UE-5.8>`.
4. Executar **`Scripts/Run-LabScript.ps1 -Script build_manny_bindings.py -LogName Manny-bindings-build.log`** para criar e simular os seis sistemas. Usar o commandlet: o harness de simulação manual não produziu partículas num Editor completo e essas tentativas estão registadas como falhadas.
5. Executar `Scripts/prepare_manny_cases.py`.
6. Executar `Scripts/Run-LabEditorScript.ps1 -Script create_manny_review.py -LogName Manny-prepare.log` para guardar o palco.
7. Executar `Scripts/Open-MannyLab.ps1 -Audit` para recolher evidência; ou abrir `Ver-Manny-VFX.cmd` para revisão.
8. Executar `Scripts/audit_manny_review.py` para medir as amostras e gerar a galeria. Inspecionar as capturas atuais antes de registar aprovação visual.

Só o módulo separado **SanctaVFXMannyLab** é instalado por esta preparação. As DLLs da ponte VFX existente são preservadas. Os mapas Manny são fixtures locais reproduzíveis pelo script.
