# Continuar a conversão para Niagara noutra máquina

## Ponto atual — catálogo Manny completo, 6 de outubro de 2026

**331 componentes / 340 cenários**, quatro poses de template e escalas 0,8× / 1× / 1,2×. **8160 amostras, 4080 pares efeito/baseline em três vistas e 24 imagens de braços isolados**. Nove lotes UE encerraram com código 0. A inspeção cobre uma representação de cada cenário e frames completos com flags; não todos os 4080 frames manualmente.

**Ver-Capturas-Manny.cmd** abre a galeria completa, pesquisável, sem servidor. **Ver-Manny-VFX.cmd** abre as animações a 1×: P pose, E escala, V vista, B braços. Ler **MANNY_VFX_TODOS.md**, **MANNY_VFX.md** e `Evidence/gameplay-manny-full-checkpoint.json`.

Cobertura inclui 14 famílias de armas, Guard/Dodge/Sprint, chão/corpo, mãos, contactos, marcas Severing, projéteis, beams e Iceberg. Blink e Dodge receberam correções de posicionamento no fixture. Foundation, Engine, fontes/ assets runtime e rig original preservados por hashes. Não repetir capturas sem alterações relevantes; a retoma preserva lotes com configurações iguais.

As dimensões de armas e poses Unarmed são provisórias. Guard fica discreto de perfil; certas poses/vistas ocultam projéteis ou põem o muzzle Staff abaixo do chão. Essas flags continuam registadas. Faltam armas/animações/notifies finais, câmara/roupa/oclusão/Low, promoção do adaptador ao runtime, eventos confirmados de gameplay, autoridade/replicação e Shipping. Glacial/Iceberg aguardam feedback de forma. Não declarar aprovação de produção ou integração concluída no jogo.

Capturas e assets Epic/MannyLab são locais, fora do Git/ZIP. O ZIP contém assets runtime e documentação/receitas, sem o módulo editor Manny. A passagem de 21 cenários é histórica em `Saved/MannyPass2-20261006` e `Evidence/MannyReview`. Não alterar Foundation sem nova autorização.

**Catálogo Manny completo publicado:** commit `598cdd3`, verificado em `origin/main`. Capturas/Epic mantêm-se locais.

**Pacote de integração publicado no GitHub:** integration/vfx-runtime-ue5.8.3/Sancta-VFX-Runtime.zip, com plugin standalone, 1786 packages e guia INTEGRAR_NO_PROJETO.md. Commit b7032c2 verificado em origin/main. Promoção do adaptador Manny e ligação ao gameplay continuam pendentes.

## Estado atual — integração VFX validada no laboratório em 5 de outubro de 2026

**331/331 componentes atuais compilados, simulados, capturados e inspecionados**, 401 definições com bindings verificados, 572 checks de contratos, 34 testes nativos de eventos e 56 combinações classe/arma passaram. Inclui básicos de 14 famílias de armas, Guard/Dodge/Sprint e fases separadas de casts, voos, contactos, procs, recursos e estados. As 441 referências/assets anteriores preservam os hashes. Foundation e Engine continuam sem alterações.

O visualizador tem **332 cenas** e começa a **1×**. Os testes de pausa, mudança de velocidade, avanço, repetição e limpeza da fase anterior passaram; o envio físico dos controlos ainda pode ser conferido pelo utilizador. Fazer duplo clique em `Ver-Fases-Integracao.cmd`. `Ver-Capturas-Integracao.cmd` abre a galeria estática atual, com pesquisa por componente, sem servidor.

O plano corrente de **867 capturas** está completo e registado por hashes. As 28 folhas e os 331 melhores frames foram inspecionados. Também estão concluídos os 94 casos de contraste/Low/terreno e 27 casos de recursos/hold. Mist já não tem cortes retos no chão; Sand Shot distingue a nuvem legível do contacto confirmado por alvo. Fireball e o gelo Frost Lance aprovado permanecem preservados; Tempest reutiliza esse gelo. Os lotes anteriores e o lote interrompido são histórico, não validação corrente.

A medição de concorrência cobriu 0/1/16/48 instâncias de Arcane Weaving II, com 120 amostras por caso. Mede o frame GPU total do palco PIE e inclui o custo de base; não certifica custo isolado de cada VFX nem orçamento Shipping no hardware alvo. Ver `Evidence/gameplay-runtime-performance-validation.json`.

O pacote de migração fica em `Exports/Sancta-VFX-Runtime.zip`; a fonte de verdade é `Evidence/gameplay-vfx-implementation-checkpoint-20261004.json`, juntamente com o guia `GUIA_EXECUCAO_VFX.md`. A referência de rig confirmada pelo utilizador é **Manny do UE**. O perfil `Evidence/gameplay-runtime-rig-reference.json` distingue a primeira calibração animada de laboratório da calibração final no jogo.

Ficam pendentes o feedback de forma de Glacial/Iceberg e das novas apresentações, calibração no Manny/câmara real, ligação GAS/autoridade/replicação, colisão/navegação, cook Shipping e orçamento real. Não alterar Foundation sem nova autorização. Não repetir a compilação/capturas correntes sem alterações que invalidem os respetivos hashes. O checkpoint indica o estado de Git/push; não há execução UE ativa desta tarefa.

**Runtime publicado:** o commit `2d1ea92` chegou a `origin/main`. O utilizador autorizou o envio e pediu o guia. `Abrir-Guia-VFX.cmd` abre `GUIA_VFX.html`, com orientações e índice pesquisável de 331 componentes, 136 FormIds canónicos e 332 cenas. `GUIA_VFX.md` é a versão para Git; o ZIP inclui guia/índice/capturas. O guia e índice foram publicados no commit <code>c9553ef</code>. O checkpoint conserva o commit verificado que contém ambos.

Os estados abaixo são histórico e não substituem o ponto atual.

## Ponto de retoma atual — revisão interna concluída em 4 de outubro de 2026

**148/148 versões atuais compiladas/simuladas** (71 skills +77 componentes), **247 cenários** (124 skills +123 componentes), 2470 imagens de efeitos e 247 baselines. Capturas atuais e inspeção interna completas, sem alertas de presença/enquadramento. Os cinco cenários finais e a correção dos eventos Tempest estão verificados. Não repetir builds/capturas sem novas alterações.

Ler [RETOMA_REVISAO_20261003.md](RETOMA_REVISAO_20261003.md), `Evidence/art-revision-resumed-checkpoint-20261003.json` e `Evidence/quality-art-review.json`. O estado da paragem por bateria foi ultrapassado. Foundation/Engine e os 187 sistemas anteriores preservados; quatro testes runtime atuais passaram.

O controlo da janela foi interrompido pelo Escape físico do utilizador e autorizado novamente por “retorma”. Falta conferir seleção no catálogo e Repetir; evidência dos controlos em `Evidence/review-controls-validation.json`. O novo pedido Fire Bolt foi aplicado e capturado em I/II e nos voos separados: perfil circular e rasto ligado ao contorno da esfera, afilado para trás. Comparação em `Saved/QualityContactSheets/fire-contour-before-after.png`; não foi acrescentada uma concha volumétrica 3D. O visualizador começa à velocidade normal (1×), com arranque interativo confirmado em `Evidence/review-startup-speed-validation.json`; 1/3 é uma opção manual. Aprovação visual final de Fire Bolt, Glacial e Iceberg depende do feedback do utilizador.

Fire Bolt/Fire Ball: a esfera e o rasto atuais foram aprovados pelo utilizador em 4 de outubro; registo ligado aos hashes em `Evidence/user-art-approvals.json`. Glacial/Iceberg continuam a precisar de feedback de forma. A avaliação seguinte da integração/combate está concluída em `REVISAO_INTEGRACAO_VFX_20261004.md`, com 60 famílias, os 124 cenários/123 componentes, 14 armas e Guard/Dodge/Sprint. É uma proposta de integração e lacunas, sem novos VFX ou alterações ao Foundation. Usar a matriz/evidência ligada nesse documento como ponto de partida; não repetir a conversão do catálogo.

Os relatórios e contagens abaixo são histórico; não substituem este estado atual.

## Nova revisão artística pedida em 3 de outubro de 2026

O utilizador reviu o visualizador e pediu 38 grupos de correções, incluindo projéteis, gelo, stances, áreas completas e separação de procs. O registo autoritativo deste lote está em `Evidence/art-revision-20261003.json`. A revisão anterior de 187 cenas está preservada em `Evidence/ArtReview20261003/Before`; não certifica estas novas alterações. Usar assets com versão própria e conferir novas capturas reais do UE antes de marcar qualquer pedido concluído. Não alterar Foundation ou Engine.

## Segundo lote de componentes — 3 de outubro de 2026

O laboratório tem agora **187 cenários: 124 skills e 63 componentes isolados**. Este lote acrescentou 25 sistemas independentes: 14 de Volley e 11 de Chains. As versões Bleed e Poison mantêm assets próprios. Volley II distingue o voo em leque do projétil único maior de carga completa; mira, fim da mira e hit por alvo também estão separados. Chains distingue lançamento, ligação, contacto e dissolução; Chains II tem ainda enrolamento no alvo, contração no recast e interrupt independentes.

Os novos dados de carga completa e recast vêm das ações executadas na referência aprovada, com hashes conferidos. Os 162 sistemas guardados antes deste lote mantêm os seus hashes. O Foundation e o Engine continuam preservados. Os 63 componentes passaram compilação, presença/expiração e ligação dos índices/idade no dataset CPU; os 86 materiais passaram a validação.

A recolha final cobre os **187 cenários, com 1885 imagens de efeitos: 1511 amostras e 374 vistas adicionais**, além de 187 imagens sem VFX. Os 25 cenários novos acrescentaram 231 imagens de efeitos. Foram inspecionadas as vistas principais e os dois ângulos, com capturas completas nos quatro casos corrigidos. Não ficaram alertas de presença/enquadramento nem amostras relevantes a tocar nos limites da imagem. As execuções internas encerraram sem erros críticos. `Evidence/quality-pass.json` e `Evidence/quality-art-review.json` são a evidência atual; a primeira passagem está preservada em `Evidence/ReferencePreviewRevisions`.

O inventário atual fica em `Evidence/separation-inventory.json`; `Evidence/volley-chains-separation-contracts.json` regista as condições e os owners dos 25 novos componentes. São demonstrações finitas editáveis. A implementação no jogo ainda tem de ligar hold/release, targets/sockets, colisão, alcance, refresh, remoção, cancelamento e pooling à autoridade de gameplay. O hit de Volley é por alvo confirmado; não contém um timer de DoT. O recast de Chains II exige o Root das Chains da mesma fonte, confirma o interrupt antes do deslocamento e reutiliza a ligação existente.

As duas cenas de ancoragem usam um manequim semitransparente para revelar as pequenas estacas junto aos pés. Isso permite inspecionar a forma isolada; a oclusão pelas botas da personagem real continua a exigir validação. Os manequins do palco são estáticos: o recast mostra a deformação gravada do VFX e não certifica a animação/deslocamento da personagem no jogo. Os bounds guardados são os da demonstração finita; os endpoints e o alcance reais exigem bounds próprios na integração.

**Em 3 de outubro, o utilizador pediu “mostra”, autorizando abrir o visualizador para verificar agora.** Este pedido substitui a instrução anterior de deixar a verificação para amanhã. Os 63 componentes surgem depois das 124 skills em `Ver-Skills.cmd`, cada um num cenário próprio. O próximo lote a decompor inclui barreiras/áreas e recursos/procs dos spirits. A aprovação de produção continua a exigir a câmara real, cenários claros, casts concorrentes e medições GPU.

## Primeira passagem visual e 38 componentes — 3 de outubro de 2026

O laboratório tem **162 cenários guardados: 124 skills e 38 componentes isolados**, cada um num mapa próprio. Os sistemas anteriores, o Foundation e o Engine estão preservados. A reprodução corre no mundo de jogo através da ponte nativa; não depende de callbacks Python.

A passagem interna carregou os 162 sistemas e produziu **1654 imagens de efeitos: 1330 amostras e 324 vistas adicionais**, além das 162 imagens sem VFX usadas na comparação. Foram corrigidos os enquadramentos das áreas maiores, das chamas de Combust II e dos cues de cabeça/pés; Fear estava fora da câmara. Chains e Volley II têm agora vistas numa fase visível. A inspeção direta das folhas principais e dos dois ângulos está concluída; a medição final não deixou alertas de presença/enquadramento. `Evidence/quality-pass.json` é a evidência atual, com os mapas efetivamente testados, imagens, hashes e comparação contra uma imagem sem VFX. `Evidence/quality-art-review.json` contém a inspeção e os limites da aprovação. Isto confirma a primeira revisão visual no palco neutro; a aprovação final de produção continua pendente.

Fire Bolt I usa agora geometria e shaders da referência; a cabeça e o rasto aparecem nas vistas adicionais sem os cortes diagonais anteriores. As formas orientadas no espaço continuam a ser diferentes de uma simulação volumétrica de fogo. Evasion captura os dados enquanto estão vivos e mostra a silhueta/pulso. As seis aproximações antigas de Piercing/Shoulder foram substituídas no catálogo por versões `PreviewV2` que usam geometria e shaders da referência. Os assets anteriores continuam guardados.

O visualizador repete os efeitos breves depois da sua conclusão, com uma pausa de 0,25 s de relógio do jogo, em vez de esperar pela duração conservadora do catálogo. `Evidence/review-loop-validation.json` regista quatro repetições reais de Tank Stance em velocidade 1/3 e encerramento sem erro. Os botões testados e as interações ainda não conferidas ficam em `Evidence/review-controls-validation.json`.

**O utilizador pediu para deixar a verificação para amanhã e não abrir o visualizador hoje.** As capturas internas usam `RenderOffscreen`; a janela do utilizador permanece fechada. Quando o utilizador retomar, fazer duplo clique em **`Ver-Skills.cmd`**. Usar **Seguinte**, **Anterior** ou **Todas as skills**; **Pausa/Continuar**, **Repetir**, **Velocidade 1/3** e **Zoom** estão na barra inferior. Os 38 componentes aparecem depois das 124 skills na mesma lista. Se o Engine estiver noutro local, usar `-EngineRoot D:\UE58`.

### Separação realizada

- Stun, Sleep, Silence, Taunt, Fear e Root: ativo, fim natural, Cleanse e morte — 24 sistemas.
- Aplicação de Taunt e Push/Pull/Slow Pull — 4 sistemas.
- Marcas Severing 1/2/3 e cortes Severing Strike I/II/III — 6 sistemas.
- Fire Bolt I/II: voo e impacto confirmados, separados — 4 sistemas.

As marcas contam a sequência no alvo; o nível da skill altera o corte. Não usar o nível da skill para escolher automaticamente uma marca. `VFX-separated-components.json` e `Evidence/separated-component-validation.json` registam os assets e a compilação/simulação; `REVER_QUALIDADE.md` descreve os critérios e o contrato de integração.

### Próximo trabalho de produção

A revisão do laboratório não certifica a qualidade em combate. Ligar os componentes a alvo/socket, refresh, remoção, cancelamento e pooling; impactos/procs dependem de eventos confirmados. Manter uma origem de autoridade para a duração do gameplay. Buff/Debuff/DoT/HoT continuam na UI salvo forma de mundo explicitamente aprovada. Conferir contraste em cenários claros, câmaras do jogo e vários casts concorrentes; medir custo GPU/overdraw e preparar escalabilidade. `Evidence/authoring-budget-review.json` assinala 41 casos para revisão de custos a partir de contagens estáticas, sem os tratar como timings GPU medidos. `Evidence/separation-inventory.json` inventaria as fronteiras das 124 skills, incluindo áreas persistentes, ligações, procs, stances e spirits.

## Atualização em 1 de outubro de 2026: conversão nativa completa no laboratório

**124/124 VFX guardados no UE 5.8.3; zero conversões VFX pendentes.** Fighter: 31; Mage: 30; Mystic: 33; Scout: 29; Control: 1. Nameplates é a 125.ª referência, de UI, e não foi implementada como Niagara.

`Evidence/native-conversion-audit.json` confirma os ficheiros `.uasset`, os hashes das referências e a evidência de compilação/simulação, sem inconsistências. O lote terminou com saída UE 0 e zero falhas (`Saved/Native-remaining-6.log`). Os 117 sistemas do método experimental têm também índices e idade normalizada verificados no dataset CPU; os sete sistemas anteriores mantêm a validação própria. Weave usa agora `/Game/VFXLab/Mage/WeavePreviewV2/NS_WeavePreviewV2`, preservando a versão anterior.

**Não são 124 efeitos aprovados para produção.** A compilação foi verificada no laboratório D3D11/PCD3D_SM5. A revisão visual, a amostragem GPU dos sistemas experimentais, a integração de targets/sockets/ciclo de vida/pooling e o orçamento de custos continuam pendentes. Os sistemas experimentais representam uma demonstração de cast, com dados/shaders editáveis.

### Captura no Editor

As capturas do commandlet continuam quase pretas (RGB 0–1, alpha 255). O diagnóstico que esperou 90 frames reais do Editor exportou imagens inspecionadas: **o Fire Bolt I aparece**, assim como o cubo emissivo de controlo. Estão em `Previews/EditorDiagnostic`; `Evidence/editor-capture-diagnostic.json` regista os hashes e o resultado. A imagem de voo ainda contém um aviso do céu e não certifica fidelidade artística. Esta verificação é apenas do Fire Bolt I anterior, não dos 117 sistemas experimentais.

A instância temporária retornou `0xC0000005` depois de exportar as imagens e registar o encerramento. As imagens provam renderização visível; a execução do diagnóstico não foi inteiramente bem-sucedida. Os 124 sistemas guardados e o lote com saída UE 0 não foram alterados pelo diagnóstico. Resolver o encerramento e preparar capturas limpas como trabalho separado; não encerrar um Editor do utilizador.

Para revisão humana, usar `Abrir-VFX-Recentes.cmd -EngineRoot C:\UE_5.8`. O Content Browser disponibiliza todos os sistemas do catálogo; só os três últimos são carregados e abertos explicitamente. O Foundation e o Engine continuam preservados.

## Estado em 30 de setembro de 2026

O objetivo é editar os protótipos de VFX do SanctaMMO no Unreal/Niagara. A primeira conversão é o **Fire Bolt I**. O Foundation original não foi alterado e continua protegido: trabalhar num laboratório ou numa cópia.

**Estado atual no UE 5.8.3:** `NS_FireBoltI` foi criado e guardado com três emissores CPU e nove parâmetros. A ponte local compilou e os testes de simulação passaram (voo, impacto, expiração e velocidade reduzida a metade). A inspeção das capturas, a comparação visual e a medição de custo no motor são etapas separadas. Os seis materiais/instâncias e os sistemas antigos continuam preservados.

`VFX-status.json` regista o estado mais recente. `Evidence/previous-nullrhi-build-report.json` é um relatório anterior de uma tentativa falhada, conservado para diagnóstico; **não certifica o resultado final**.

## Preparar a nova máquina

### Atualização nesta máquina: UE 5.8.3

O utilizador autorizou continuar com UE 5.8.3 em `C:\UE_5.8`. O script aceita agora 5.8.2 e 5.8.3; a ponte local compilou com sucesso no 5.8.3. A validação do efeito é uma etapa separada. Editor, commandlet, DotNet e UnrealBuildTool estão presentes. O conversor nativo desta instalação tem BuildId 55116800, igual ao Editor. A ponte usa agora esse módulo nativo e compila apenas as funções locais de simulação/captura e inicialização de Slate. Os fontes privados do conversor deixaram de ser necessários. Não alterar o Engine nem os BuildIds.

Usar `-EngineRoot 'C:\UE_5.8'` nos comandos abaixo nesta máquina.

1. Clonar este repositório, de preferência num caminho curto como `C:\Dev\SanctaMMO-VFX`. Abrir `unreal\SanctaVFX-Niagara`.
2. Disponibilizar uma instalação **UE 5.8.3** (versão atual autorizada), ou UE 5.8.2 com conversor nativo compatível. Incluir o Editor, os binários de desenvolvimento/precompilados, UnrealBuildTool, o runtime DotNet 10.0 e os binários compatíveis do plugin `Engine/Plugins/FX/CascadeToNiagaraConverter`. São necessários Visual Studio Build Tools C++ e Windows SDK compatíveis com esta instalação. Não atualizar nem recompilar o Engine como solução automática.
3. Se o Engine não estiver em `C:\UE_5.8`, indicar o caminho em cada comando. Exemplo em PowerShell:

   ```powershell
   .\Verificar-Ambiente.cmd -EngineRoot 'D:\UE582'
   .\Compilar-Ponte.cmd -EngineRoot 'D:\UE582'
   .\Retomar-Preparacao.cmd -EngineRoot 'D:\UE582'
   .\Abrir-Laboratorio.cmd -EngineRoot 'D:\UE582'
   ```

   Também é possível definir `$env:UE_ENGINE_ROOT = 'D:\UE582'` nessa sessão. `Verificar-Ambiente.cmd` apenas verifica ficheiros; não abre o editor nem inicia compilação.
4. `Compilar-Ponte.cmd` monta a ponte local em `BuildHost` e compila **VFXBuildEditor** com `-NoEngineChanges -UsePrecompiled`. Copia o plugin resultante para o laboratório. Usa o conversor nativo, verifica o respetivo BuildId e não altera o Engine. Os binários/caches ficam ignorados pelo Git.
5. `Retomar-Preparacao.cmd` cria `NS_FireBoltI`, espera pela compilação de Niagara, guarda o sistema e executa os testes de simulação e as capturas. Se o sistema já existir, executa a validação sem o recriar. A primeira compilação de shaders pode demorar e consumir CPU; iniciar quando o UE estiver disponível.
6. Confirmar `VFX-validation-report.json` com `status: passed`, inspecionar as imagens em `Previews` e abrir o efeito. O relatório prova a simulação; a fidelidade visual exige inspeção e comparação com o HTML.

Os caminhos do Engine são configuráveis; os caches ficam em `Saved` dentro do laboratório. O `.uproject` não fixa um GUID de instalação; os comandos chamam explicitamente o editor indicado. Não foram incluídos Engine, Editor, DLLs/PDBs, caches, histórico Git do Foundation ou a cópia antiga do jogo.

## O que já está implementado

Referência: [`prototypes/mage/fire-bolt-i/fire-bolt-i-vfx.html`](../../prototypes/mage/fire-bolt-i/fire-bolt-i-vfx.html), na raiz do repositório. As regras de direção visual e orçamento continuam em `CLAUDE.md`, `docs/skills.json` e `docs/ue-vfx-tech-spec.html`.

O gerador usa módulos nativos do Niagara para três emissores CPU em espaço local: `Head`, `Tail` e `Impact`, cada um com um Sprite Renderer. O voo é na direção +X. A cauda cresce desde a origem e contrai após a chegada; o impacto começa em `CastDelay + Distance / Speed`.

| User Parameter | Valor inicial |
|---|---:|
| Speed | 1200 cm/s |
| Distance | 800 cm |
| CastDelay | 0,1 s |
| HeadSize | 57,6 cm |
| TailLength | 260 cm |
| TailWidth | 104 cm |
| TailFade | 0,2 s |
| ImpactDuration | 0,25 s |
| ImpactSize | 70 cm |

Manter velocidade, distâncias, tamanhos e durações positivos. Cores e brilho são parâmetros `HotColor`, `RedColor` e `Intensity` das instâncias `MI_FireBolt_…`. A forma procedural está num nó Custom dos materiais base: editável no Material Editor, mas exige edição da fórmula do shader. A cauda ainda é uma aproximação do HTML.

`SanctaVFXLabLibrary` permite inspecionar o sistema, alterar floats expostos, simular em instantes definidos e capturar imagens pelo Unreal. Os testes verificam presença de cabeça/cauda durante o voo, impacto à chegada, fim das partículas e a resposta à redução da velocidade para metade. Restauram a velocidade inicial antes de guardar.

## Problemas já identificados e cuidados para continuar

- Na instalação anterior, o conversor tinha BuildId incompatível. No UE 5.8.3 atual, os BuildIds coincidem e o conversor nativo está ativado. O script verifica a compatibilidade; nunca editar manifests para a fingir.
- Não usar `-nullrhi` para validar prontidão ou simulação: o Niagara devolve `IsReadyToRun=false` quando `FApp::CanEverRender()` é falso. Os comandos usam D3D11 e `-AllowCommandletRendering -RenderOffscreen`.
- O caminho de colagem do Sprite Renderer constrói widgets mesmo sem janela. A inicialização de Slate com Null Renderer no módulo local resolveu essa falha.
- Usar `unreal.load_asset` para verificar módulos do plugin: o Asset Registry nem sempre os conhece no início da sessão.
- O caminho correto de Solve Forces é `/Niagara/Modules/Solvers/SolveForcesAndVelocity.SolveForcesAndVelocity`.
- Inicializar explicitamente Age, NormalizedAge, Lifetime, Position, Velocity, SpriteSize, Color, Alive, Mass e SpriteRotation em Particle Spawn. Os setters do conversor precedem os módulos: Initialize Particle sobrescrevia duração e posição e foi retirado deste gerador.
- Em commandlet, inicializar explicitamente o componente Niagara antes da ativação e do tick manual. Ler a posição pelo nome `Position` no dataset (com fallback para `Particles.Position`); o leitor anterior devolvia zero por não encontrar o atributo.
- Fazer `ctx.cleanup()` uma única vez antes de encerrar o editor; a conversão mantida viva provocava falhas durante o descarregamento de AssetTools.
- `UE_SKIP_UBT_SDK_SETUP=1` evita a verificação inicial de SDK a competir pelo mutex de outras compilações. Os comandos já o definem.
- Não lançar a preparação pelo atalho antigo do Foundation copiado. Usar este projeto independente.

## Trabalho restante

### Conversão das referências mais recentes, iniciada em 1 de outubro de 2026

`VFX-catalog.json` inventaria as 125 referências finais do pacote aprovado de 30 de setembro, com hashes verificados. Há 27 referências ajustadas na última revisão. O catálogo distingue conversões guardadas de referências ainda pendentes; não certifica fidelidade visual.

O primeiro lote acrescentou seis sistemas reais em `/Game/VFXLab/Fighter`: Piercing Strike I, II Tank, II Warrior e Shoulder Rush I, II Tank, II Warrior. Cada um tem três emissores CPU (forma principal, impacto e faíscas). Compilaram, produziram partículas e terminaram na simulação. `VFX-batch-report.json` conserva os resultados. `Scripts/build_latest_vfx.py` reproduz apenas estas seis receitas e preserva assets existentes; não é um conversor automático dos 125 HTML.

As formas principais usam as máscaras da revisão final e as variantes mantêm as suas paletas. Estas são primeiras versões Niagara, ainda com diferenças: as faíscas movem-se linearmente, o Piercing tem um alvo de demonstração em vez dos três do HTML, e o Shoulder usa 4 m em vez dos 3,75 m da demonstração HTML. Não estão ligados a sockets, eventos de acerto ou GameplayCues. Exigem inspeção no editor. `Abrir-VFX-Recentes.cmd` disponibiliza os sistemas guardados no Content Browser e abre até três. No início da continuação havia 118 referências sem conversão nativa; consultar agora o catálogo e o relatório do lote para a contagem atual. Nameplates é uma referência de UI: deve ser implementada em UMG/Slate, não como Niagara.

Em 1 de outubro de 2026, a captura de voo foi inspecionada e está preta, sem efeito visível. A exportação dos PNGs não valida a renderização; as capturas não servem para aprovação visual. A simulação continua validada, mas é preciso verificar o sistema no editor Niagara e corrigir a captura antes de apresentar novas imagens.

### Documento operacional fornecido pelo utilizador

Foi lido `//PC/Partilha com Portátil/Sancta_MMO_Pipeline_Visual_Operacional_PTPT.docx`, versão 1.0.0 de 30 de setembro. A avaliação e o hash estão em `Evidence/pipeline-document-assessment.json`. A secção 10 ajuda a ordenar o trabalho VFX: protótipo Niagara, fontes editáveis, integração, testes de ciclo de vida, bounds e escalabilidade, revisão visual e medição de casts concorrentes. A secção 13 distingue validação técnica de aprovação humana. O documento não fornece as receitas Niagara em falta.

O manual refere UE 5.8.2; permanece válida a autorização do utilizador para **UE 5.8.3**. Os standards, schemas, locks e gates descritos como propostas não passam automaticamente a regras adotadas nem constituem aprovações. Continuar no laboratório independente, preservando o Foundation e o Engine.

Está em desenvolvimento um **piloto experimental** que extrai geometria, shaders e dados de um cast dos HTML aprovados, para tradução em materiais e emissores Niagara. `Scripts/capture_reference_data.cjs`, `Scripts/reference_shader_port.py` e `Scripts/build_reference_ports.py` ainda não comprovam uma conversão automática completa. Shaders especiais, materiais com iluminação, atributos de vértice e estados persistentes precisam de tratamento próprio. Consultar `VFX-native-port-report.json` antes de declarar qualquer sistema novo válido. Não aplicar este método em produção nem contabilizar fontes extraídas como sistemas Niagara convertidos.

O piloto passou a produzir sistemas reais guardados: a continuação acrescentou **25 sistemas Fighter**, com materiais compilados e presença/expiração verificadas por simulação. Juntamente com as seis receitas anteriores, a classe Fighter tem 31 sistemas; Fire Bolt I permanece em Mage. O lote das restantes classes está em execução. Esta contagem é um ponto de situação, não uma aprovação final nem um substituto do catálogo atualizado.

As geometrias e texturas de autoria ficam em `Source`; os recursos nativos partilhados em `/Game/VFXLab/ReferenceShared`. Materiais com código e modos iguais usam um material mestre e instâncias próprias com textura de atributos e timings por efeito. Os atributos são armazenados com os bits float32 preservados em PNG RGBA8 linear sem compressão destrutiva. `Evidence/reference-port-research.json` regista o método e os seus limites. O teste do PNG verifica os dados de autoria; a renderização GPU continua a exigir revisão.

Executar `Scripts/Run-ReferencePorts.ps1` para retomar os elementos pendentes. `-Slugs chains-ii,cleanse` limita a execução; o gerador preserva sistemas existentes. O ficheiro `Saved/Stop-reference-batch.request`, quando existir, termina o lote entre efeitos. Removê-lo apenas quando se pretende retomar. Os parâmetros de preview, o cast demonstrativo, bounds, ramos opcionais, estados persistentes, sockets, interrupção/pooling e custo em jogo ainda precisam de revisão e integração.

A ponte foi recompilada em 1 de outubro depois de o Editor do utilizador deixar de estar aberto, sem o fechar por automação. A compilação local com publicação de dados dinâmicos passou (`Saved/Bridge-capture-fix-build-4.log`) e a validação da simulação foi repetida. A nova captura de voo foi inspecionada e **continua preta**. `Evidence/capture-dynamic-update-check.json` regista esse resultado; os PNGs anteriores estão preservados em `Archive/CaptureBeforeDynamicUpdate`. Não apresentar a captura como corrigida nem alterar o Foundation/Engine para contornar o problema.

O lote foi retomado com `Saved/Native-remaining-4.log` depois de chegar a 48 sistemas guardados. Inclui agora o tempo de entrada original das duas Astral Auras e a normal deformada nos materiais iluminados de Vine Field/Root. A identidade dos materiais partilhados inclui o shader da normal quando existe. Consultar o catálogo para o progresso atual; as contagens só incluem sistemas guardados com compilação e simulação verificadas.

`Saved/Native-remaining-5.log` retoma a partir de 49 sistemas, com `Run-ReferencePorts.ps1 -ShaderWorkers 2`. O limite só altera a configuração do processo, não os ficheiros do Engine. O valor por defeito continua a ser um worker. `Scripts/audit_reference_ports.py` cruza hashes, ficheiros guardados e evidência de compilação/simulação; `--write-report` guarda o resultado em `Evidence/native-conversion-audit.json`.

A leitura adicional de Age/Lifetime/NormalizedAge e dos índices DynamicMaterialParameter foi compilada e instalada depois de o lote terminar entre efeitos, com confirmação de que não havia processos UE ativos (`Saved/Bridge-attribute-readback-build-2.log`). A tentativa anterior tinha sido bloqueada pelo Live Coding; a revisão automática também rejeitou inicialmente a instalação por considerar o lote ainda ativo. A confirmação explícita da saída do processo permitiu a instalação sem concorrência. **Os 55 sistemas experimentais guardados passaram** a leitura dos índices e da idade normalizada (`Evidence/reference-binding-validation.json`, `Saved/Binding-validation.log`, saída UE 0). Esse teste lê o dataset CPU; não prova amostragem GPU nem fidelidade visual.

`Saved/Native-remaining-6.log` retoma a partir de 62 sistemas guardados, incluindo Fighter e Mage completos e Astral Aura Moon. O gerador passa a verificar os índices e a idade antes de guardar cada sistema novo. Foi corrigida a duração dos previews que combinam um burst de transição com uma camada persistente: passam a incluir uma demonstração de pelo menos 3,1 s. Weave V2 é criado em pasta própria com `-PreviewV2 weave`; o sistema e as instâncias anteriores ficam preservados e a respetiva evidência em `Evidence/ReferencePreviewRevisions`. Os previews continuam finitos; o ciclo de vida real dos estados precisa de integração em gameplay.

Inspecionar as capturas exportadas, verificar a imagem no editor e comparar vista lateral e câmara de jogo com o HTML. Para reconstruir após alterações ao gerador, executar `Scripts/Unreal-Lab.ps1 -Action Rebuild -EngineRoot C:\UE_5.8`; a versão anterior é preservada em Archive. Não declarar o efeito pronto apenas por a compilação passar. Depois, confirmar os parâmetros na UI e medir custo com vários casts. O projétil real e o evento de acerto devem controlar voo e impacto na integração futura; combate, sockets e GameplayCues ainda não foram ligados. Os restantes protótipos precisam de conversões próprias.


## Suspensão da implementação — 4 de outubro de 2026

O utilizador pediu aplicar toda a avaliação e depois suspendeu para desligar o PC. Foram criadas quatro fontes C++ de SanctaVFXRuntime, ainda sem compilação, registo no plugin, bindings ou testes. Não houve alteração de assets Niagara, Foundation ou Engine. Retomar por `RETOMAR_INTEGRACAO_20261004.md` e pelo checkpoint `Evidence/gameplay-vfx-implementation-checkpoint-20261004.json`, que conserva trabalho feito, riscos de implementação e backlog completo. Nenhuma implementação fica em segundo plano.
