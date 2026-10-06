# Execução dos VFX no laboratório

Para instalar o pacote no projeto principal, começar em [INTEGRAR_NO_PROJETO.md](INTEGRAR_NO_PROJETO.md). O ZIP publicado em `integration/vfx-runtime-ue5.8.3` contém o plugin standalone, os assets e os guias.

Para navegação, orientações e pesquisa dos componentes/cenas/fases canónicas, começar em [GUIA_VFX.html](GUIA_VFX.html) ou [GUIA_VFX.md](GUIA_VFX.md). Fazer duplo clique em <code>Abrir-Guia-VFX.cmd</code> no laboratório.

O módulo `SanctaVFXRuntime` apresenta os resultados recebidos do jogo. As fontes históricas de arte e o visualizador existente ficam separados dos derivados em `/Game/Sancta/VFX`. O checkpoint distingue compilação, bindings, capturas e revisão interna; a existência de uma fonte JSON não significa que o respetivo asset esteja pronto. A integração no jogo e a aprovação artística do utilizador têm evidência própria.

## Entrada das skills

Adicionar `USanctaVFXPresentationComponent` ao host de apresentação e preencher `Definitions` com as definições necessárias. `LifeId` representa a vida atual da entidade, fornecida pelo jogo, coerente nos clientes. Usar os `FormId` estáveis de `Evidence/gameplay-runtime-form-routes.json`. O campo `Phase` deve corresponder à fase da definição: os componentes isolados conservam nomes explícitos, como `FireBoltIFlight`, `FireBoltIIImpact` ou `FireBoltIISpread`. Não tocar o cast completo do visualizador em conjunto com esses componentes.

Enviar um `FSanctaVFXEvent` com `ExecutionId`, `EventSequence` e os snapshots da admissão. Estados, links, voo e hold têm também `StateId` próprio. Enviar Source/Target/Projectile reais, sockets existentes, vida do alvo, ponto de contacto, orientação e dimensões reais. O componente segue os owners; o shader conserva a forma de arte, sem usar a trajetória gravada como gameplay.

`bAdmitted` permite preparação e delivery. `bConfirmedHit` permite contacto. `bApplied` representa uma aplicação efetiva de Shield, Heal, recurso, CC ou outro resultado. Targeted Miss não apresenta os resultados de hit. As queries de AoE mantêm o seu contrato de resolução; não devem receber um Miss de outro alvo. Os procs separados só são enviados quando a autoridade confirmou o respetivo resultado, nunca por um temporizador de animação. Cleanse usa Apply no alvo que perdeu efeitos, com `bApplied` apenas se houve remoção; Evasion usa Proc no Scout após a esquiva confirmada. Estes resultados não são eventos de Anim Notify.

`EndPhase` termina hold/voo/fase de movimento quando o owner o indicar. `EndExecution` refere-se à conclusão da execução inteira, incluindo resoluções de projéteis; não é automaticamente sinónimo de GAS EndAbility ao terminar o gesto de cast. Fim natural conserva a cauda visual dos impactos finitos já confirmados. Estados persistentes independentes sobrevivem e terminam por `EndState`. Remover um estado não sintetiza um proc: NaturalEnd e Cleanse só podem ser apresentados depois de um encerramento com a causa correspondente. Cancel, Interrupt, RangeBreak, Death, Consumed e Replaced não são fins naturais.

`UpdatePresentation` atualiza a fase indicada sem repetir o burst de entrada. Reconstrução por relevância usa `bReconstructActive`; reset/respawn usa `ResetForLife`. O transporte do jogo deve filtrar mensagens antigas e fornecer o tempo de evento no relógio de apresentação compatível com a janela de deduplicação. Esta API local não implementa replicação ou decisões de combate.

Um estado pode ter várias ocorrências finitas confirmadas; cada uma recebe `EventSequence` distinto. O estado persistente conserva uma única instância. A primeira causa de encerramento é definitiva: repetir `EndState`/`EndExecution` não muda a causa nem corta um efeito terminal já admitido. O âmbito de um `StateId` deve corresponder ao owner real, não a todas as fases da ability.

Uma atualização finita só altera a ocorrência com o mesmo `EventSequence`. Os projéteis de um leque conservam componentes distintos, mesmo partilhando o cast; o efeito de voo de Volley segue **um** projétil. A autoridade cria os nove projéteis sincronizados e apresenta o voo em cada owner real. Não juntar nove sistemas que já contêm nove setas de demonstração.

## Recursos, hold e resultados

Arcane Shards recebe `ResourceCount` e `ResourceMax` reais: 2 no core base, 10 com a especialização. Elemental usa `OccupiedMask` 0/1/3, ElementA e ElementB (Fire=0, Ice=1, Lightning=2), GainAge e alterações confirmadas de preparação/substituição/consumo. Estes valores não contam hits nem skills. Spirits recebe o contador e Pending do owner; a variante Sun/Moon é a do cast e o fim vem do contrato de host/vida/grupo.

Mana Barrier usa `CastProgress` durante o hold, `ReleaseAge` na libertação e encerramento explícito em cancel/interrupt. A duração do hold vem do jogo. Os testes de imagem incluem oito segundos com o progresso ainda retido. Links recebem sockets reais das duas pontas. Connection não cria um projétil adicional; o ritual terminal depende de NaturalEnd confirmado.

`ReleaseAge` e `GainAge` são idades visuais à receção (`-1` significa ausente). Avançam localmente entre updates. Um snapshot novo deve trazer as idades correntes; repetir zero em cada frame reiniciaria a leitura visual. Para seguir uma ponta de arma sem republificar estados de recursos, usar `EndpointActor`/`EndpointSocket`; os transforms e sockets são lidos em cada tick.

Volley II recebe `CastProgress`, `ReleaseAge` e `GainAge` desde o instante em que a carga completa foi confirmada, para a mira e o seu brilho breve. Um cancelamento termina a mira através do owner. Nas cadeias de lightning, emitir um evento `Chain` por ligação confirmada: Source/socket é a origem dessa ligação, Target/vida e Endpoint/socket são o destino. Não existe seleção de alvos ou salto temporizado no shader.

Severing recebe eventos de cast, hit e marca 1/2/3 separados. Rally separa caster e afetados. CC partilha sete famílias, com Disarm distinto de Stun. Bright Star apresenta ShieldApply. Tempest separa área/telegraph/strike de gelo e lightning, impacto e resultado Sapped. Fire II spread, conditional Permafrost/Glacial, chains de lightning, Serenity, Backstab e resultados Ether dependem dos respetivos eventos explícitos. Um debuff aplicado neste hit não pode auto-habilitar o proc que consulta o estado anterior.

Na composição de Severing, a marca breve da sequência já confirma o hit. O rank escolhe o corte; o índice confirmado da sequência escolhe a marca. Os flashes `SeveringHit*` foram retirados dos jobs, definições e pacote correntes; as referências históricas continuam guardadas.

## Básicos e ações

`SanctaVFXCombatLibrary::BasicPresentationId` escolhe um dos 28 perfis das 14 famílias. Fighter/Scout usam Physical e Mage/Mystic Magical, independentemente da arma. A arma escolhe apresentação, não novas regras de dano/cadência. Os dez perfis melee usam sockets da base e ponta; os quatro ranged seguem o projétil homing real. Não criar um segundo básico por Offhand. O contacto recebe o ponto de impacto na superfície, não a origem do actor.

Guard Active pertence ao estado de guard válido; Mitigation só segue mitigação frontal confirmada e Depletion não representa Stun ou parry. Dodge Start acompanha a ação e Avoided só é enviado pelo resultado correspondente; não comunica i-frames. Sprint partilha FootContact Stone/Snow/Mud/Water em contactos reais. O Anim Notify sincroniza Cast/Release/Trail/FootContact/Start a partir de uma execução admitida; não confirma dano, CC ou procs e não altera SkillCount.

## Terreno, organização e integração

`ASanctaVFXTerrain` usa `SM_IcebergBody` e `M_IcebergBody`, escala física explícita, colisão, integridade visual e remoção. A autoridade de terreno determina criação, vida e destruição; a apresentação não calcula HP. O teste nativo valida LOS/Visibility e bloqueio de Pawn/WorldDynamic. O canal concreto de projéteis e a atualização de navegação do Foundation exigem ligação no projeto do jogo.

As pastas Combat, Skills, Status, Terrain, Common e Definitions ficam dentro de `/Game/Sancta/VFX`. Hashes nos assets preservam revisões; o inventário atual distingue-as de versões piloto antigas. Fixtures, cenas de revisão e demonstrações do laboratório não fazem parte do pacote de execução. Low desliga componentes Decorative através de `bDecorativeEnabled`; a silhueta mecânica deve conservar-se. O custo de materiais/translucência e os limites do alvo de produção só ficam aprovados depois da medição nativa.

`NET_Essential` e `NET_Gameplay` não impõem corte por distância/quantidade. `NET_Decorative` tem limites iniciais editáveis por qualidade, ainda sem aprovação de orçamento. A migração usa a lista explícita de packages e dependências, sem recorrer a um cook recursivo das pastas do laboratório.

Os bounds de links e áreas parametrizadas acompanham endpoint, raio e alcance, em vez de conservar só a extensão da demonstração. As dimensões de referência das áreas foram identificadas nas fontes e são guardadas nas definições. `Radius`, `Range` e `ConeAngle` do evento vêm sempre da query/estado real; os valores de referência servem apenas para converter a forma visual, nunca como regras de alcance do gameplay.

Poison Sac distingue Flight, Impact, Consume e Active. Active é uma zona World com StateId e Radius reais, independente da vida do alvo original; só termina pelo owner. Sickness distingue Flight, Consume, Impact no alvo primário e AreaImpact World. O AoE de Sickness é instantâneo e recebe uma resolução própria; não criar uma zona persistente. Hemorrhage distingue o consumo do payoff. Os resultados só são apresentados depois do recheck e consumo atómico confirmados pelo gameplay.

Os cues World que devem sobreviver ao caster precisam de um host de apresentação que conserve essa duração, como o gestor local de cues ou o actor da área. A vida do componente host termina as suas instâncias. As apresentações no corpo conservam alturas de referência sobre o root do manequim; os sockets/proporções de rigs reais ainda precisam de calibração, evitando somar uma altura de corpo já authored a um socket do peito.

O utilizador confirmou em 5 de outubro que a referência base do jogo é **Manny do UE**. Usar o Manny do projeto para calibrar escala e attachment: root para cues de corpo com alturas já authored; mão/cotovelo para Bleed/Poison; base/ponta da arma para básicos e Rapid Attack; origem do cast e endpoint para beams/links. Confirmar os nomes e transforms dos bones/sockets no asset efetivamente utilizado, incluindo pose e escala do actor. Um bone não substitui automaticamente o socket de gameplay. A figura estática do laboratório continua a servir apenas para leitura da forma; a passagem animada de laboratório cobre 340 cenários / 331 componentes; armas/animações finais e promoção do adaptador ao runtime continuam pendentes. O perfil de referência está em `Evidence/gameplay-runtime-rig-reference.json`.

War Leap distingue Telegraph no destino durante a preparação, Movement preso ao owner do salto e AreaImpact no ponto de aterragem **válida**. O impacto reúne o anel, fissuras e traço vertical; não é um cast automático. Crushing Blow reúne o anel e traço vertical em AreaImpact. Shoulder Rush usa Impact no alvo confirmado. Smoke Bomb e Combust II resolvem as partes de chão em AreaImpact World, separadas dos voos, zonas persistentes e resultados no corpo. Thunderstrike usa Strike World a partir do ponto atingido; o raio conserva a extensão para o céu.

Long Jump usa Hold entre o Source e o destino real (Target/TargetSocket ou EndpointActor/EndpointSocket), e Telegraph World no destino projetado. Atualizar ambos a partir do input confirmado. A trajetória de preparação não determina navegação nem alcance. EndPhase termina a preparação quando começa o salto; cancelar a execução também remove Hold/Telegraph. Não gerar um hit ofensivo por chegar ao chão.

Bleed/Poison Stance usam Active persistente entre a mão e o cotovelo: SourceSocket na mão e EndpointActor/EndpointSocket no cotovelo da mesma personagem, ou Source/Target iguais com sockets diferentes. A esfera e cone partem da mão; o shader conserva o fade para o cotovelo. Terminar pelo StateId da stance. CCTaunt fica no alvo taunted; EndpointActor/EndpointSocket identifica o taunter real. Laser liga a origem ao endpoint atual e conserva Contact como resultado separado; o comprimento gravado e o sweep do protótipo não comandam o beam.

Os contactos de Piercing são emitidos uma vez por alvo confirmado. Severing conserva apenas corte e marca de sequência 1/2/3; os três flashes redundantes SeveringHit ficam nas referências históricas. Vortex inclui os braços da forma revista no voo; Displacement só aparece depois do deslocamento confirmado. Astral Pull distingue a ligação, relocação no receiver e resolução no destino; só emitir os resultados após TeleportResolve válido. Sun/Moon Aura segue o Source, mantém o modo próprio e recebe Radius do estado, sem reinterpretar a stance atual.

Pressure/Provoke conserva Cast ligado ao alvo e Impact World breve no `Position` de contacto confirmado. O impacto recebe Target/TargetLifeId para rejeitar resultados de outra vida, mas não soma a altura gravada do protótipo ao ponto real. Connection NaturalEnd usa o relógio próprio da fase terminal: dissolve uma ligação já formada, com tempo adicional para a resolução da versão II.

Sand Shot apresenta o cone e os detritos em Cast World na origem/orientação confirmada, com Range/ConeAngle da execução. O contacto é uma fase Impact World independente por hit válido, com Target/TargetLifeId e Position; os três flashes de alvos gravados foram retirados do cast. O Interrupt vem do resultado de gameplay e não cria um Stun persistente.

Os derivados de anéis, recursos e ligações que perderam cor em fundo claro usam mistura premultiplicada com opacidade obtida da máscara de luz existente. Os traços e as bordas continuam suaves; o Fireball aprovado conserva as suas fontes. Conferir exposição/contraste na câmara real do jogo antes de aprovar materiais para produção.

O componente recusa Present/Update em DedicatedServer e o seu tick não corre nesse modo. A colisão do terreno continua a pertencer à autoridade. Isto não substitui a integração do transporte e do servidor no projeto do jogo.

## Ver as fases

Abrir `Ver-Fases-Integracao.cmd`. Cada componente tem uma cena própria. Usar Anterior/Seguinte ou a lista; Espaço pausa, R repete, S alterna entre 1× e 1/3. O arranque é a 1× e o relógio da animação começa depois do aquecimento de render, conservando os flashes breves. Os inputs e movimentos são exemplos de teste; o visualizador original continua em `Ver-Skills.cmd`.

As capturas aceites usam leitura direta da GameViewport do mundo PIE. O visualizador espera tanto pelo Niagara como pelos shaders assíncronos dos materiais; depois aquece o render antes de iniciar a reprodução ou capturar. O modo de snapshot prolonga a vida das partículas e conserva a idade de material pedida, mantendo a simulação a atualizar os dados de render; os testes separados de Niagara verificam a duração real dos sistemas. As imagens antigas obtidas por screenshot global, com render parado ou antes de os shaders estarem prontos não certificam presença dos efeitos. A galeria fica em `Evidence/RuntimeReview/galeria.html`; a aceitação das imagens e a revisão artística estão registadas separadamente nos relatórios.

O Foundation mantém-se sem alterações por instrução existente do utilizador. A ligação final GAS/abilities, transporte multiplayer, sockets do rig e canais de colisão faz-se no projeto do jogo quando essa restrição for levantada. Não apresentar o laboratório como uma integração Foundation já concluída.
