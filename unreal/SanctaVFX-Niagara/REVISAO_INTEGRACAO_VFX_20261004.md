# Avaliação dos VFX para integração nas skills e no combate

4 de outubro de 2026. Avaliação de design e integração para o laboratório SanctaMMO VFX, destinada ao responsável pelo jogo e a quem implementar as abilities, animações e GameplayCues.

A biblioteca tem uma base visual aproveitável, mas precisa de passar de demonstrações de casts para apresentações dirigidas pelos resultados reais do jogo. Recomendo preservar os visuais aprovados, completar as entregas e estados em falta, reduzir feedback redundante e criar uma biblioteca discreta para ataques básicos, guard, dodge e sprint. O Fire Bolt e Fire Ball atuais ficam aprovados na esfera e no rasto; Frost Lance conserva o gelo aprovado. Glacial Spike e Iceberg continuam a precisar do feedback de forma já identificado.

Esta avaliação cobre **124 linhas do catálogo de skills, incluindo variantes, dois overlays de Basic Attack e o laboratório CC; 123 componentes isolados; 247 cenários de inspeção**. Não são 124 abilities únicas. Foram revistas 60 famílias funcionais contra as regras atuais. As capturas e simulações anteriores continuam válidas para o aspeto no palco; não provam integração em combate. Não foram alterados assets Niagara, Engine ou Foundation nesta avaliação.

## Fontes e precedência

O funcionamento do jogo foi conferido em `C:/Dev/SanctaMMO-Foundation-5.8/Docs/Canon-Current/02-combate-controlo.md`, `03-classes.md` e `04-equipamento.md`, incluindo as decisões completas ligadas quando necessárias. A direção visual de produção está em `Docs/Art/VISUAL_LEDGER.md`: Grounded Stylized Fantasy with Graphic Readability, com prioridade à informação de gameplay e à silhueta. A aprovação de fogo/gelo e os pedidos específicos desta conversa são preservados.

`docs/skills.json`, o snapshot de protótipos e a ficha técnica VFX ajudam a avaliar a aparência e a proveniência, mas contêm decisões históricas. Por exemplo, a ficha antiga põe stances nos pés; a direção VFX posterior coloca-as na cintura. A ficha proíbe refração enquanto o gelo aprovado exige leitura vítrea. Estas divergências devem ser reconciliadas explicitamente, sem substituir silenciosamente os efeitos aprovados nem assumir que todo o efeito vítreo necessita de refração real da cena.

O inventário antigo de FormIds ainda diz que não há assets UE e marca muitas linhas como MISSING. Isso é histórico anterior à conversão. O inventário de separação antigo declara 63 componentes; existem agora 123. **Não usar esses MISSING ou essa contagem como backlog atual.** A nova evidência regista paths e hashes dos ficheiros efetivamente lidos; o HEAD do Foundation é apenas contexto, não prova que todos os ficheiros estejam iguais ao commit.

## O que deve ser preservado

- Fire Bolt I e Fire Ball: cabeça e rasto atuais aprovados. A integração modifica posição, orientação e duração do voo, preservando a silhueta.
- Frost Lance e o gelo partilhado com Tempest: preservar material, proporções e leitura; preparar qualidade reduzida sem regressão para pedra azul.
- Separação já realizada de Fire, Rally, Severing, Volley, Chains, impactos/procs elementais e Tempest: reutilizar esses componentes em vez de duplicar os casts completos.
- Glacial Spike: conservar a proposta de espigões maiores ao longe, inclinados e irregulares com neve ligeira até à revisão final do utilizador.
- Linguagem fina de stances, órbitas e recursos; diferenças de forma entre Ether aliado/inimigo e Poison/Bleed. A cor ajuda, mas não deve ser a única distinção.

## Lacunas que impedem uma integração correta

| Prioridade | Observação confirmada | Trabalho necessário |
| --- | --- | --- |
| P0 | Origens, destinos, tempos e eventos estão frequentemente gravados para um cast demonstrativo. | Adaptadores para sockets, trajetórias, eventos confirmados e remoção; o material não decide gameplay. |
| P0 | Elemental Weaver controla cores, mas os dois cristais têm ocupação fixa. Shards/counters são gravados. | Estados vazio, um e dois elementos; contagem real, ganho, substituição, consumo e par pronto. |
| P0 | Exploit atuais só mostram vortex/hit no alvo; Full Moon atual mostra chão/pilares; Cosmic Ray mostra manifestação/pending/heal. | Flight de entrega próprio nas três famílias conforme Projectile do canon. Backstab já contém viagem de adaga na fonte. |
| P0 | `BrightStarHeal` está etiquetado como Heal, mas Bright Star concede Shield Instant AoE. | Identidade de produção ShieldApply e evento de aplicação efetiva; o pulso cosmético não atrasa gameplay. |
| P0 | Connection, Spirits, Cosmic Ray e efeitos diferidos têm condições de owner, vida original ou fim natural. | Instâncias com source/target/life binding e causas de remoção distintas; procs finais separados. |
| P0 | Disarm é o sétimo CC persistente canónico e não está no conjunto visual ativo. | Cue barato de aplicação, estado e remoção de Disarm; sem sugerir Stun ou desequipar a arma. |
| P0 | Iceberg bloqueia movimento, LOS e projéteis e é destrutível. | Owner de terreno com geometria e colisão reais; apresentação de spawn/damage/destroy/expiry ligada a esse owner. |
| P0 | Faltam básicos de arma e as três Actions de combate. | Biblioteca de apresentação para 14 famílias, Guard, Dodge e Sprint. |
| P1 | Hold/cancel só tem testes live específicos em Elemental/Mana; muitos outros efeitos têm inputs próprios. | Volley, War Leap, Long Jump, Resurrect, Laser, links e áreas controlados pelo tempo e resultado reais. |
| P1 | Há várias confirmações possíveis para o mesmo hit. | Composição compacta, sem acumular flashes de base + proc + status + sparks. |
| P2 | O audit de custos antigo lê fontes anteriores e não mede GPU. | Reavaliar fontes atuais e medir em combate com muitos casts; separar qualidade essencial e decoração. |

P0 significa necessário antes de integrar essa família; P1 completa a composição e o comportamento; P2 trata escala, legibilidade e custo. Não são tempos estimados de execução.

## Contrato entre a skill e o efeito

Cada componente deve ter um evento de entrada, uma âncora, uma origem de tempo e uma regra de saída. Proponho as fases `Cast`, `Hold`, `Release`, `Flight`, `Telegraph`, `Impact`, `Proc`, `Active` e `End`, usando apenas as fases de que a família precisa. Não é necessário criar nove Niagara Systems por skill.

A ability ou o owner de projectile/estado/área fornece os resultados. Anim Notifies sincronizam o gesto e os sockets; não confirmam acerto, Shield, Heal, debuff ou chegada. Um alvo que faz Miss ou é inelegível não recebe um impacto de sucesso nem os seus procs. AoE segue a própria regra, sem introduzir o gate targeted de Accuracy/Evasion.

Um cast mantém a sua forma contextual e os snapshots definidos na admissão/execução. Um swap posterior não recolore projéteis já lançados nem altera Spirits existentes. Consultas pre-Burn/pre-Slow/pre-Sapped/pre-Stun usam o resultado fornecido pelo gameplay; o novo estado aplicado pelo mesmo hit não habilita retroativamente o payoff.

Os componentes de longa duração precisam de owner real e de uma saída em expiry, cancelamento, morte, perda de relevância ou mudança de estado, conforme o contrato da família. **Fim natural, Cleanse, quebra de range e morte não são o mesmo evento.** Refresh visual não é autorização para refrescar CC quando a regra do jogo o proíbe.

Uma execução elegível conta uma Skill uma vez; hits, spreads, ticks e procs não criam contagens adicionais. Basics, Guard, Dodge e Sprint são Actions e não contam como Skills por defeito. Isto afeta diretamente Mana Storm, Momentum, Star e Comet.

O GAS disponibiliza tratamento de um cue de duração visto já ativo, útil para entrada tardia em relevância; cues adicionados com duração precisam de remoção correspondente. A proposta exige que reconstruir `Active` não volte a tocar `Cast` ou um proc antigo. Ver [While Active](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/GameplayCueNotify/WhileActive) e [Add GameplayCue On Actor](https://dev.epicgames.com/documentation/unreal-engine/BlueprintAPI/GameplayCue/AddGameplayCueOnActor_Looping).

### Dados propostos para os adaptadores

| Dados | Utilização |
| --- | --- |
| VfxFormId, PhaseId e versão da composição | Identidade estável, independente de nomes de apresentação ou hashes na pasta. Validar associação ao FormId de execução canónico. |
| ExecutionId, Source, Target, TargetLifeId e ComponentKey | Deduplicação, ownership e eventos diferidos ligados à vida/encarnação correta. |
| SourceSocket/TargetSocket, Position, Direction, HitNormal e Endpoint | Origem corporal ou contacto real; beam/link móvel; orientação do impacto. |
| Radius, Range e ConeAngle | Área visual com a mesma geometria de gameplay, sem usar apenas escala não uniforme do ator. |
| OwnerTime, PhaseAge, CastProgress, ReleaseAge e EndReason | Hold, ticks, expiry e cancelamento sem timers independentes que autorizem resultados. |
| ModeSnapshot, StanceSnapshot, Relation e ProcMask | Manifest/Weave, Warrior/Tank, Sun/Moon, aliado/hostil e resultados condicionais. |
| ResourceCount/Max, ElementA/B/OccupiedMask, GainAge e Pending | Recursos reais, incluindo zero e consumo; não inventar duração de Spirit. |

São campos conceptuais propostos, não parâmetros já implementados em todos os sistemas. `User.ElementA/B` e o hold de Mana têm evidência live própria; a maior parte deste contrato ainda precisa de implementação. Posições/ranges no UE usam centímetros; tempos, segundos; progresso, 0–1. A conversão das referências em metros não deve voltar a ser aplicada sobre valores já convertidos.

Na rede, reutilizar a autoridade e os eventos de gameplay existentes. Não criar RPCs cosméticos por partícula, timers de dano no Niagara ou physics de projectile VFX a escolher os alvos. Predição local de gestos/aim pode existir, mas confirmação e reconciliação têm de evitar impactos duplicados ou sucesso após rejeição. O payload concreto e o transporte devem ser validados no Foundation quando essa integração for autorizada.

## Ataques básicos das armas

O canon lista **14 famílias: 10 melee e 4 ranged**. Todas as classes podem usar todas as armas. Fighter/Scout mantêm canal Physical e Mage/Mystic Magical mesmo quando a arma tem outra fantasia habitual. Main-Hand/Full-Hand determina delivery; Off-Hand não cria um Basic extra.

Na versão funcional inicial, melee partilha um perfil de Cleave. Wand, Staff, Bow e Crossbow partilham um projectile de homing autoritativo e perfil de range. A velocidade ranged escala com Attack Speed ou Cast Speed da Primary, conforme o canon; os valores/curvas e a geometria melee ainda não fechados devem ser dados, não constantes decididas pelo VFX. Não acrescentar piercing, gravidade, hitscan ou maior alcance por aparência.

Proponho perfis de apresentação por arma, com módulos partilhados de trail/release/projectile/contact e variantes Physical/Magical. **São 14 perfis e 28 combinações básicas de canal para avaliar, não uma obrigação de 28 sistemas duplicados.** Compatibilidade com quatro Primaries produz 56 combinações de arma/classe a verificar, além das animações e proporções corporais. Swings múltiplos de uma animação não autorizam vários Damage Results.

| Família | Apresentação proposta |
| --- | --- |
| Sword | Traço curto que segue lâmina e ponta; contacto de corte. |
| Axe | Arco pesado curto; contacto material sem explosão. |
| Club | Cabeça e massa legíveis; impacto compacto, sem slash mágico obrigatório. |
| Rapier | Estocada fina; preserva o Cleave de gameplay comum. |
| Dual Daggers | Traços alternados curtos nas duas lâminas; um Basic lógico. |
| Fists/Gauntlets | Punho que golpeia; contacto seco; sem aura permanente nos dois braços. |
| Great Club | Contacto mais encorpado; sem shockwave funcional adicional. |
| Greatsword | Arco seguindo a animação larga; sem reach/hit count adicional. |
| Greataxe | Arco pesado assimétrico; sem AoE adicional. |
| Spear | Estocada comprida visível; a malha não atribui maior alcance. |
| Wand | Emissão na ponta, núcleo pequeno e rasto breve. |
| Staff | Emissão no foco, núcleo arcane organizado; ranged comum. |
| Bow | Flecha e release discretos; acompanha homing real. |
| Crossbow | Bolt e pequeno flash de release; sem hitscan ou gravity inventada. |

Physical usa massa/contacto/material com acento quente contido; Magical conserva o delivery da arma e acrescenta energia arcane discreta. Não dar automaticamente Fire/Ice/Lightning aos básicos Mage nem Sun/Moon aos básicos Mystic. Assinaturas de skill e procs como Bleed/Poison/Comet entram como overlays quando confirmados.

Os dois efeitos Basic Attack Bleed/Poison existentes são **overlays de hit**, não ataques completos de Bow/Adaga. Reutilizá-los com um contacto dominante evita refazer trabalho e evita três flashes simultâneos. Durante um Miss pode continuar a existir o gesto/viagem, mas desaparecem contacto de sucesso e aplicação de DoT.

## Guard Dodge e Sprint

### Guard

Guard exige equipamento de shield apropriado, consome Stamina, reduz fortemente movimento e mitiga ataques compatíveis com o arco frontal. O canon não tem passive block chance, perfect block ou parry. Não atribuir elegibilidade a Buckler apenas pelo nome. O valor G1 de mitigação no Shield não deve ser tratado pelo VFX como a mitigação total do personagem.

Proponho pose e escudo como informação principal, linha curta discreta junto ao shield durante `Active`, e pequeno impacto na superfície **só na mitigação confirmada**. Depletion pode usar quebra/escurecimento breve e feedback HUD de lockout. Não acrescentar Stun, rebote ofensivo, cúpula total ou flash de perfect block.

Tank permite Skills durante Guard e mantém consumo normal de Stamina, com a modificação canónica da stance. Skills com movimento cancelam Guard; as outras conservam-no. O VFX acompanha este estado mesmo quando a animação de cast substitui parte da pose. O sistema de apresentação não decide essa permissão.

### Dodge

Dodge combina deslocamento com Evasion temporária; não é invulnerabilidade. Proponho impulso inicial curto, contacto dos pés/poeira por superfície e, apenas se necessário para leitura, um rasto corporal muito breve. A pose e o deslocamento reais devem continuar a ser reconhecíveis, sem silhuetas de manequim ou um manto que sugira proteção AoE.

Uma Fighter Skill compatível durante Dodge não renova a janela defensiva nem o custo. Evasion e Dodge podem reutilizar um pequeno feedback de ataque evitado confirmado, mas não devem tocar os dois completos no mesmo Miss. Quickstep continua uma Skill própria; não assume as propriedades de Dodge por partilhar executor de movimento.

### Sprint

Sprint funciona em combate e partilha Stamina com Guard/Dodge. A diferença deve ler-se primeiro na locomoção. Proponho footprints/poeira materiais nos contactos reais dos pés e intensidade ligeiramente maior com a velocidade, sem linhas de energia ou trail permanente. Transição, saída e depletion são eventos do estado; não criar uma nova aura de velocidade.

Footsteps/landings podem ser partilhados com a biblioteca de animação e superfície. Não fixar poeira em pisos que pedem água, lama ou neve. Guard/Dodge/Sprint devem continuar legíveis com partículas decorativas desligadas.

## O que cortar e o que apenas reorganizar

Recomendo cortes na composição de produção, preservando os assets históricos:

- Cues de alvo, procs, resource gain e payoffs disparados por tempos gravados do cast.
- Flashes redundantes de contacto: sobretudo Backstab II e Severing hit + marca. Escolher um contacto e adicionar apenas o payoff elegível.
- Fumo/névoa/debris que tapam o limite de uma área, o alvo ou o jogador. Manter contorno útil e reduzir decoração primeiro.
- Auras persistentes de buffs/debuffs/DoTs comuns sem aprovação específica de forma no mundo. UI mantém informação e duração; CC, recursos, Spirits e áreas têm contratos próprios.
- Sucesso/chegada depois de Miss, alvo inválido, teleport rejeitado ou Leap/Rush abandonado.
- Inferências erradas pelo nome: BrightStarHeal não cura; StaticBoltIChain não autoriza propagação no I; CoilChain não cria uma nova chain; TempestRootApply já foi retirado e deve continuar fora.

Há **seis fixtures adicionais** de memória Lightning e hold Low/High que são úteis para QA. Não precisam de se transformar em seis componentes de gameplay independentes: integrar os parâmetros do sistema base e manter as fixtures apenas nos testes. As demonstrações completas permanecem no visualizador; a composição de produção não as toca junto com todos os componentes separados, o que duplicaria o efeito.

Nem todas as separações precisam de um novo asset. Separar quando owner, tempo, alvo, condição ou causa de remoção mudam. Partilhar material/módulo quando só muda cor ou escala. Manter distinção de forma quando ela comunica diferença mecânica, como Ether aliado/inimigo e Warrior/Tank.

## Organização dos ficheiros e assets

`/Game/VFXLab` continua laboratório e história de revisões. Os paths com ArtR3/hash preservam proveniência; não devem ser a identidade pública da ability. Não recomendo mover ou apagar assets à força nesta fase.

Para promoção, proponho:

```text
/Game/Sancta/VFX/
  Common/Materials Textures Meshes Modules Curves EffectTypes
  Combat/BasicAttack Guard Dodge Sprint Contact
  Status/CC Resource
  Skills/Fighter Mage Mystic Scout
    <Family>/<Phase ou Component>
  Definitions/<VFX presentation definitions>
/Game/VFXLab/
  Review/Scenarios Fixtures Archive
```

Os diretórios acima são proposta; ainda não foram criados/migrados no Content Browser. Usar prefixos normais `NS_`, `NE_`, `M_`, `MI_`, `T_`, `SM_`, `NET_` e IDs de definição estáveis. A definição de apresentação deve associar o FormId/evento ao sistema, parâmetros, anchors, lifecycle, qualidade, dependências e versão aprovada. Blueprint/ability não deve procurar um path construído pelo display name.

Separar `Source` editável, arte bruta, material/módulo partilhado, runtime definition, testes e Evidence. Fontes e contratos ficam versionados; Saved/BuildHost/cache/binários de Engine ficam fora da distribuição. Fixtures, cenas e assets históricos não entram por arrasto no cook de produção. Validar referências/cook antes de mover paths; usar migração suportada pelo Editor e verificar redirectors, não renomear `.uasset` no filesystem.

Há aliases entre os nomes do visualizador e os nomes da árvore atual, por exemplo Fire Bolt II/Fire Ball, Backstab II/Ambush e Exploit II/Sentence. A matriz regista-os como **aliases de leitura**, sem mudar FormIds, árvore ou gameplay. Resolver a identidade pela definição de execução, preservando provenance dos nomes anteriores.

## Qualidade e desempenho

A prioridade de redução segue o ledger: retirar sparks, smoke, pequenos trails e decoração antes de telegraphs, limites de hazards, projéteis principais e estados necessários. Cor, forma e timing devem distinguir aliado/hostil/cura/dano mesmo em fundo claro e em qualidade baixa. Mais intensidade não deve significar mais preenchimento do ecrã.

Proponho Effect Types por importância `Essential`, `Gameplay` e `Decorative`, com qualidade por distância/instâncias e perfis Low/Medium/High. CPU/GPU deve ser escolhido por comportamento e medição; não migrar todos os pequenos meshes para GPU por princípio. A Epic documenta custo de instâncias/emissores, escalabilidade por Effect Type e pooling; pooling reduz alocações, mas não elimina reativação ou renderização. Ver [Scalability and Best Practices for Niagara](https://dev.epicgames.com/documentation/unreal-engine/scalability-and-best-practices-for-niagara).

O audit novo regista grupos de layers, rows e triângulos potenciais das fontes atuais. Não são draw calls, partículas simultaneamente visíveis nem milissegundos GPU. Por exemplo, o Fire tail aprovado tem 64 segmentos/128 triângulos e uma única row de tail; o teto antigo de 16 segmentos precisa de exceção/LOD medido, não de um corte que volte a estragar a frente aprovada. Mana Barrier tem poucas rows e bastante geometria; efeitos com muitas camadas podem custar mesmo com pouca emissão.

Não definir agora orçamento em ms sem hardware alvo e câmara do jogo. Medir uma baseline sem efeito e depois instâncias de um cast, grupo e combate denso; recolher game/render thread, Niagara, translucência/overdraw, GPU e memória. Bounds de preview com margens grandes precisam de revisão por sistema móvel/área real. Não usar bounding box de um voo gravado inteiro para cada projectile attachado a um owner.

## Ordem de execução proposta

1. **Contrato e composição:** reconciliar FormIds/aliases, resolver Bright Star, resource counts/Elemental occupancy, causas de fim e delivery em falta. Criar definições de apresentação e um adaptador pequeno por família.
2. **Piloto funcional:** Fire aprovado com target móvel, Miss, parede e cancelamento; Severing ranks/sequência; Mana hold/cancel; um link Connection com fim natural vs range break. Estes pilotos validam quatro problemas diferentes antes de aplicar o padrão ao catálogo.
3. **Combate universal:** perfis das 14 armas com módulos partilhados, depois Guard/Dodge/Sprint. Testar overlays Bleed/Poison, Rapid Attack, Comet e compatibilidade Fighter, sem novas permissões de gameplay.
4. **Famílias complexas:** Spirits/counters/Pending, áreas com entrada/saída, Tempest por impacto e Iceberg como terreno. Completar Disarm e restante composição condicional.
5. **Promoção e escala:** migration manifest com hashes; cook de runtime sem fixtures; cenário com câmara do jogo, fundo claro, vários jogadores, Low/High e perfil CPU/GPU. Só depois marcar a definição como integrada/aprovada para produção.

## Critérios de aceitação

Cada família recebe testes específicos na matriz. Os casos transversais são:

- Resultado válido e inválido; targeted Miss; aplicação de estado ignorada; pre-condição falsa/verdadeira.
- Alvo em movimento, morre/respawna, sai de range, deixa de pertencer ao grupo ou perde relevância.
- Cancelamento, Interrupt, expiry natural, remoção precoce e Cleanse; nenhum sucesso não autorizado.
- Reutilização do componente com reset de todos os parâmetros e ausência de elementos/cores da execução anterior.
- Mesmo cast com vários alvos/ticks; deduplicação e uma contagem por execução elegível.
- Forma em outras proporções de personagem, armaduras/armas e animações durante Guard/Dodge.
- Geometria de área e colisão real coincidem; Low mantém informação essencial; decoração não mascara o combate.

O resultado desta passagem é uma **avaliação concluída e um plano de integração**, não a implementação desse plano. Os visuais atuais estão preservados; as novas apresentações e contratos continuam por criar ou ligar no projeto de jogo.

## Ficheiros da avaliação

- [Matriz de famílias e de cada cenário](MATRIZ_SKILLS_VFX_20261004.md): 60 famílias e as 124 linhas do catálogo ativo.
- [Evidência estruturada](Evidence/gameplay-vfx-assessment-20261004.json): todos os 123 componentes, dados por skill, 15 achados, 14 armas, 3 Actions, hashes e contagens atuais.
- `Scripts/assess_gameplay_vfx_20261004.py`: reproduz contagens/proveniência e verifica a cobertura do catálogo; as decisões de design continuam propostas documentadas.
