# Matriz de revisão das skills e componentes

4 de outubro de 2026. Propostas de integração e composição, com assets atuais preservados. Cada linha do catálogo ativo está coberta; variantes não equivalem a skills únicas. FormIds e aliases exigem reconciliação com o canon atual.

A análise usa fontes/capturas já validadas e contratos de gameplay. Não certifica uma nova execução integrada em combate.

| Prioridade | Família | Cenários | Ajustar ou acrescentar | Cortar ou impedir |
| --- | --- | ---: | --- | --- |
| P1 | Cleanse | 4 | Um burst por resolução efetiva; partilhar módulos e distinguir paletas. Mystic suporta aliado; os outros são self-only. Remover apenas os cues dos estados realmente removidos. | Retirar sucesso em tentativa sem remoção e apagar a ideia de limpar Burn/Bleed/Poison, HoT, Shield ou recursos por defeito. |
| P1 | Stances Fighter | 2 | Separar transição curta do marcador persistente na cintura. Preservar a identidade magenta/ciano e manter visível durante Skills compatíveis com Dodge/Guard. | Não acrescentar anel no chão; não repetir a transição em cada frame nem renovar a janela defensiva de Dodge. |
| P1 | Battlecry e Challenge | 4 | Manter pulso simples e diferença de intensidade aprovada. Ligar Silence/Fear/Taunt/Root aos cues partilhados; conservar a forma snapshot após swap. | Nunca agendar Fear/Root por tempo do preview. Taunt ignorado, remoção precoce ou Cleanse não disparam Root. |
| P1 | Momentum e payoffs | 3 | Separar consumo, resposta no caster e marcador de recurso. Fornecer quantidade consumida, magnitude efetiva e fim do estado; não inferir magnitude do rank. | Não manter uma aura de Heal. Não apresentar Momentum Mastery em Rally nem num ganho de Momentum. |
| P1 | Chains | 2 | A separação já existe. Substituir endpoints gravados por sockets reais; conservar uma ligação no recast e uma oportunidade associada ao Root da mesma fonte. | Não reaplicar Root na chegada. Não mostrar movimento quando o Pull é rejeitado; o Interrupt já resolvido pode manter o seu cue. |
| P1 | Crushing Blow e Crushing Combo | 2 | Decompor chão de cast e feedback por alvo; reutilizar impacto físico e CC. Aumentar o II por payoff confirmado, não por partículas permanentes. | Retirar Stun predefinido e anéis individuais nos alvos; evitar segundo flash se o impacto já confirma contacto. |
| P1 | Defiant Presence | 1 | Manter só a cúpula azul aprovada; controlar duração e origem usada na regra. A cúpula comunica o estado, não calcula a elegibilidade. | Excluir os projéteis da demonstração e reações decorativas a hits. Não sugerir que remove efeitos hostis já existentes. |
| P1 | Piercing e Breaching | 3 | Preservar a linha e ligar a origem à mão/corpo adequado a qualquer arma. Separar payoff por alvo e snapshot de stance. | Não usar slow criado pelo próprio hit para habilitar o payoff; não trocar a forma já executada depois de stance swap. |
| P1 | Pressure e Provoke | 1 | Separar ataque, confirmação de hit e aplicação de estado. Auditar a cobertura das duas formas no mesmo protótipo; usar IDs de forma distintos se a leitura muda. | Não fazer hit/proc após Miss ou target inválido; não usar apenas recoloração para a relação de alvo. |
| P1 | Rally | 4 | Componentes de afetados já separados. A integração decide a lista; base Vigor e upgrades dependem da forma snapshot. | Não percorrer manequins gravados nem incluir toda a Raid por defeito. Não manter quatro auras de buffs no corpo. |
| P1 | Second Wind | 1 | Manter burst mais intenso; alimentar magnitude efetiva e presa ao corpo. O valor não deve vir do brilho nem de dano absorvido pelo Shield. | Evitar pulse persistente ou cue forte de cura quando Heal efetivo é zero. |
| P1 | Severing | 3 | Cortes, hits e marcas existem. Parametrizar as marcas e o fim/consumo/reset da sequência; alinhar corte com a animação real sem o transformar num ataque básico de arma. | Rever SeveringHit + marca para retirar confirmação duplicada; rank III não significa marca 3. Não gerar nova marca em Miss. |
| P1 | Shoulder Rush | 3 | Decompor preparação/travel/arrival. Ajustar rasto à velocidade real e proteger a leitura em Guard/Dodge e com qualquer arma. | Não agendar hit de chegada após colisão, abandono ou ForcedDisplacement. Shield Rush não ganha requisito de Shield só pelo nome. |
| P1 | War Leap | 1 | Faltam estados controláveis de channel e componentes de takeoff/landing separados do cast completo. | Não usar contacto tardio com chão como autorização de aterragem ofensiva de leap abandonado. |
| P0 | Mage Manifest e Weave | 2 | Separar swap, marcador persistente, recurso e ganho. Retirar a gravação de casts auxiliares e permitir contagem real de Shards e máximo data-driven. | Não mostrar Burn/Slow/Sapped em Weave. Um cast com muitos hits dá no máximo um evento de recurso. |
| P1 | Arcane Burst | 1 | Um projétil com raio/intensidade alimentados pelo consumo real. Separar recurso consumido, voo e impacto, sem exigir nova skill por contagem. | Não criar um projétil por Shard nem ganhos de recurso a partir dos callbacks de impacto. |
| P0 | Arcane Weaving | 2 | A órbita restaurada deve persistir sem Shards. Expor Count/MaxCount e evento Gain/Consume/MaxProc; os dados aV/aG atuais são gravados. | Retirar estados hardcoded e qualquer aura de cooldown. Arcane Master não produz um evento por impacto. |
| P0 | Elemental Weaver | 2 | Cores já controláveis e testadas. Falta mask/count de ocupação, GainAge por slot e ReadyPair. No I um segundo elemento diferente substitui a preparação incompleta; II habilita pares mistos. | Não manter sempre dois cristais; não oferecer Mist/Laser/Tempest no I; não criar seis sistemas só para as combinações de cor. |
| P1 | Fire Bolt e Fire Ball | 2 | Esfera/rasto atuais aprovados pelo utilizador. Preservar a forma e substituir trajetória fixa por owner real; impactos/spread já separados. | Cortar spread em Weave, Burn automático em Miss e destinos gravados. Não voltar a alterar a silhueta aprovada por iniciativa genérica de polish. |
| P1 | Combust | 2 | Separar contacto e payoff de consumo no alvo. O círculo de fogo pedido pelo utilizador é composição no alvo, não uma nova área de dano. | Retirar qualquer interpretação do círculo como hazard persistente; não representar consumo de Burn inexistente. |
| P1 | Frost Lance e Permafrost | 2 | Gelo aprovado preservado. Impactos/condicional já separados; parametrizar flight endpoints e controlar a magnitude do segundo efeito pelo resultado. | Não confundir Hindered/Dazed com Stun nem manter gelo no alvo como estado persistente. |
| P1 | Glacial Spike | 2 | Conservar proposta B com caos/inclinação/neve até feedback. Usar cone/range/posição reais e nunca tirar o limite útil na qualidade baixa. | Retirar procs agendados e colisão dos meshes de neve/spikes decorativos; Stun só no II e pre-Slow verdadeiro. |
| P0 | Static Bolt | 2 | Hit, chão e links existem. StaticBoltIChain é nome ambíguo: auditar a forma para classificar contacto caster-alvo vs propagação, que só o II habilita. | Não tratar StaticBoltIChain como permissão de chain no I. Sapped criado no mesmo hit não autoriza encadeamento; um recurso Weave por execução. |
| P1 | Thunderstrike | 2 | Há splash separado; assegurar cue específico/ramo do burst pre-Stunned, sem o esconder numa animação automática do cast. | Não aplicar Root nem misturar splash com pre-Stun. Em Weave não há nova assinatura Sapped. |
| P0 | Mana Barrier e Overcharge | 2 | Hold já testado. Separar visual de channel/barreira de formação de Shield e Overcharge. Low/High são fixtures, não quatro skills adicionais. | Não repetir channel ou produzir Shield por tick; não agendar Overcharge no preview de Barrier; não manter esfera universal de Shield. |
| P0 | Mana Storm | 1 | Círculo completo já revisto. Falta pulso da área + resposta de admission separados e parametrizados; preservar a posição inicial quando o Mage se move. | Não pulsar em loop, em Basic Attack/Guard/Dodge/Sprint, nem representar buff de Heal/Shield/CC que a regra não concede. |
| P1 | Blink | 1 | Preservar smoothness revista. Separar partida/chegada e ligar ao resultado; o cast/channel em curso pode continuar sem reiniciar a origem da outra skill. | Não apresentar chegada em teleport recusado nem renovar Dodge/Guard/Shield por visual. |
| P1 | Coil | 1 | Preservar separação e alimentar os alvos reais. CoilChain não autoriza uma cadeia de ataques não definida; classificar como ligações do cast/AoE. | Não criar Root base, chain sem regra, pulse de hit persistente no Shield ou novo SkillCount por alvo. |
| P0 | Iceberg | 1 | VFX atual é referência de aparência. Necessita owner de terreno, malha/colisão/LOS/projéteis reais e estados de dano/destruição alinhados; ângulo ainda por aprovar. | Não usar um Niagara decorativo como único terreno bloqueante; não manter blockers invisíveis após dissolução. |
| P1 | Laser | 1 | Origem e contacto já existem. Parametrizar direção, endpoint e intensidade; manter origem legível e contacto apenas enquanto validado. | Não mostrar sparks permanentes num extremo vazio nem resolver dano com colisão visual; ticks não são novas Skills. |
| P1 | Mist | 1 | Área e névoa têm de usar a geometria/duração reais. Definir leitura owner/aliado/inimigo sem esconder limites de hazards concorrentes. | Não sugerir dano, Blind ou Slow sem autoria; reduzir sprites que enchem o ecrã perto da câmara. |
| P1 | Tempest | 1 | Manter correção 8/9/10 e gelo Frost aprovado. Componentes separados precisam de um impacto por evento, posições/cores snapshot e duração de aviso real. | Nunca reativar TempestRootApply nem loop gravado de hits/procs. O cue Ice não deve arrastar Lightning e vice-versa. |
| P1 | Vortex | 1 | Separar voo/passagem, impacto e movimento lateral de cada alvo; preservar melhoria atual da forma. | Não deslocar visualmente um target sem comando aceite; Burn e movimento não são CC Root. |
| P1 | Mystic stances | 2 | Separar toggle, marcador persistente e recurso. Os dois pools conservam identidade e não devem ser confundidos com Spirit variante. | Sem cooldown/resource timer no VFX; não transformar troca de stance em mudança dos Spirits já colocados. |
| P1 | Sun Aura e Moon Aura | 2 | Manter IDs de aura próprios e diferenciar toggle/área de alcance/resposta de membros. Parametrizar owner e alcance. | Não inferir aura a partir da stance nem desenhar uma aura extra por Buff concedido. |
| P1 | Astral relocation | 2 | Step move só Mystic; Pull move só aliado válido Party/Raid. Usar origem/destino confirmados e identidade da vida/encarnação quando exigida. | Não desenhar o ally a mover no Step nem chegada em Pull inválido. Não tratar teleport como ForcedDisplacement. |
| P1 | Astral Veil | 1 | Separar estado e burst pequeno de interceção. VFX deve coincidir com a superfície autoritativa, dos dois lados. | Não bloquear visualmente personagens, LOS, beams, cones ou ground AoE; não mostrar fraturas por HP porque Veil não tem HP. |
| P1 | Black Hole | 2 | Separar área, displacement inicial e payoff final; lista final não é a lista capturada no começo. | Retirar pull contínuo/repetido e dano agendado de alvos que já saíram. Não manter lock por tempo do visual. |
| P0 | Bright Star Full Moon e Eclipse | 3 | BrightStarHeal é spark de Shield e deve ser identificado como ShieldApply. Full Moon atual conserva chão/pilares, mas falta flight separado. Eclipse distingue aliado Shield e hostil Damage/Silence. | Retirar interpretação de heal e atraso de gameplay pela frente do pulso Bright Star. Não mostrar Shield como invulnerabilidade; não disparar Eclipse automático em pools cheios. |
| P0 | Connection | 4 | Manter intensidade II; separar Attach/Link/Tick/NaturalEnd/Break/Spread com endpoints móveis. O link representa a instância da fonte, não um buff genérico. | Não produzir ritual final em range break, morte ou remoção precoce. Não combinar heal/damage periódico com uma duração fixa de preview. |
| P0 | Cosmic Ray | 2 | Fonte atual mostra manifestação/pending/heal gravados. Falta flight de entrega independente e Pending/Resolve/Cancel orientados por vida original e relógio do owner. | Não curar nova encarnação nem recontar charge no VFX; charges e recharge são HUD. |
| P1 | Ether | 4 | Preservar formas de esfera/crescente e procs separados. Auditar cobertura do proc inimigo II e expor a trajetória real em ambos. | Não habilitar proc com o estado criado no mesmo hit. Não acrescentar spill/chain e não resolver dano num alvo inelegível. |
| P1 | Lullaby e Nightmare | 2 | Separar Travel/Hit/PendingSleep/Apply e os eventos do follow-up; ligar ao estado real do alvo na validação. | Não aplicar Sleep por timer se o hit falhou; Nightmare não é obrigado a usar o mesmo alvo da Lullaby inicial. |
| P1 | Resurrect | 1 | Chão restaurado e Complete separado. Falta hold/cancel guiado por cast real; o cue de sucesso acompanha o resultado, não a pose final do montage. | Não usar barreira que sugira invulnerabilidade nem sucesso após cast falhado. |
| P1 | Serenity | 1 | Componentes Heal/Sleep existem. Parametrizar ponto, raio e duração de aviso, e resolver em alvos reais. | Não manter zona curativa/pulsos depois da resolução nem aplicar Sleep persistentemente pelo material da área. |
| P0 | Spirits | 6 | Separar Spirit persistente e procs por host/alvo. Comet conta Basics; Star conta Skills elegíveis uma vez; Orbit usa sua cadence e threshold de inimigos válidos. | Retirar duração fixa inferida, forma que muda com stance atual, procs de terceiro golpe animados sem resultado e um contador por impacto. |
| P1 | Scout stances | 2 | Manter cones mão→cotovelo aprovados, mas ancorar em sockets reais e integrar compatibilidade com armas que tapam a mão. | Não reinterpretar flechas já lançadas depois do swap nem converter a stance em DoT visual contínuo em cada inimigo. |
| P1 | Basic Attack DoT existente | 2 | São apenas overlays de hit já existentes, independentes da arma. Reutilizar sobre o impacto base sem os contar como pacote de Basic Attack completo. | Não aplicar em Miss ou só no finisher da animação; não triplicar impacto com base + overlay + aura de status. |
| P1 | Backstab e Ambush | 2 | A fonte já tem viagem de adaga; não a converter num melee por causa do nome. Completar separação de flight/hit do I e composição compacta do II. | Rever até cinco componentes de hit/proc/sparks para evitar flashes redundantes. Extras do rear nunca aparecem num hit frontal. |
| P1 | Blinding Dart e Torpor | 2 | Separar flight e impacto/state apply, manter pequenas silhuetas distintas sem criar halo contínuo no alvo. | Não acrescentar chão/hazard/chain; não aplicar debuff depois de Miss. |
| P1 | Evasion | 1 | Manter manto/transparência sem forma de manequim. Separar activation de feedback de Miss/Evasion e respeitar a janela real. | Não sugerir invulnerabilidade, phased collision ou proteção AoE; AoE continua counter posicional. |
| P0 | Exploit Sentence Executioner | 3 | A fonte atual tem apenas vortex/hit no alvo, sem endpoints de voo. Preservar o vortex bronze e acrescentar uma entrega legível + reset local/HUD qualificado. | Não aumentar espetáculo por cada debuff individual; não repetir o dano no reset nem inferir Takedown do desaparecimento do target. |
| P1 | Hemorrhage Poison Sac Sickness | 3 | Preservar sangue/viscosidade/bolhas revistos. Separar cast/flight quando authored, consumption/target burst, area active e end; radius/duration fornecidos pelo owner. | Não manter pool de sangue como hazard de Hemorrhage ST. Não usar chão de Poison como aplicação automática fora do volume. |
| P1 | Long Jump e Quickstep | 3 | Separar preview local de landing, travel e arrival; alinhar com trajetória efetiva. Quickstep é skill diferente de Dodge Action. | Não mostrar arrival de leap abandonado; não usar VFX para contar/recarregar charges nem renovar defesa de Dodge. |
| P0 | Rapid Attack | 1 | Preservar ativação mais lenta e traços que sobem pelo braço. Separar Activation/PerBasicPulse/End; a versão atual é uma demonstração curta gravada. | Não manter raios permanentes, disparar para a frente nem gerar um proc por cada swing de um Basic lógico. |
| P1 | Sand Shot | 1 | Manter ritmo artístico mais lento, mas encaixar no tempo de ataque real; granularidade/debris subordinados ao cone. | Não deixar poeira durar como Blind/Slow/área persistente sem regra; Interrupt não usa cue de Stun. |
| P1 | Smoke Bomb | 2 | Conservar diferença de cor aprovada e acrescentar distinção de densidade/forma subtil. Separar flight/impact/area e Mist owner de Shroud. | Não mostrar concealment de Shroud em aliados/inimigos nem num Scout fora da sua zona; não bloquear o ecrã com fumo próximo. |
| P1 | Vine Field e Entangle | 2 | Manter vinhas on-theme e separar telegraph/area/RootApply/End; usar o volume autoritativo. | Não Root contínuo nem check repetido por pulso de vine; Root visual partilhado evita nova aura por skill. |
| P1 | Volley e Narrowing Volley | 4 | Separação de aim/fan/piercing/hit existe. Parametrizar ChargeProgress/ConeAngle/Range; confirmar o ponto de snapshot no contrato da ability. | Não usar as nove flechas visuais para dar nove DoTs no mesmo alvo; sem curva de gravidade/piercing fora da forma de carga completa authored. |
| P0 | CC partilhados | 1 | Seis CC persistentes têm variantes de inspeção. Falta Disarm canónico e binding de duração/removal. Preservar a composição conjunta e UI para a duração. | O mapa control é demonstração e não uma skill que aplica seis CC. Não empilhar visual duas vezes quando apply e active usam a mesma forma; não inventar refresh de CC. |

## Registo por cenário

| Cenário | Nome atual no canon ou alias de leitura | Família | Prioridade | Componentes associados |
| --- | --- | --- | --- | --- |
| Challenge I (battlecry-challenge-i-tank) | Challenge I | Battlecry e Challenge | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Battlecry I (battlecry-challenge-i-warrior) | Battlecry I | Battlecry e Challenge | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Challenge II (battlecry-challenge-ii-tank) | Chain Challenge | Battlecry e Challenge | P1 | ChallengeIIRootApply |
| Battlecry II (battlecry-challenge-ii-warrior) | Battlerage | Battlecry e Challenge | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Bulwark (bulwark) | Bulwark | Momentum e payoffs | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Chains I (chains) | Chains I | Chains | P1 | ChainsIFlight, ChainsILatchedLink, ChainsIHit, ChainsIEnd |
| Chains II Pull (chains-ii) | Chain Pull | Chains | P1 | ChainsIIFlight, ChainsIILatchedLink, ChainsIIHit, ChainsIIEnd, ChainsIITargetWrap, ChainsIIPull, ChainsIIInterrupt |
| Cleanse Fighter (cleanse) | Cleanse Fighter | Cleanse | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Crushing Blow I (crushing-blow) | Crushing Blow I | Crushing Blow e Crushing Combo | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Crushing Blow II (crushing-blow-ii) | Crushing Combo | Crushing Blow e Crushing Combo | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Defiant Presence (defiant-presence) | Defiant Presence | Defiant Presence | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Momentum Mastery (momentum-mastery) | Momentum Mastery | Momentum e payoffs | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Piercing Strike I (piercing-strike) | Piercing Strike I | Piercing e Breaching | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Piercing Strike II Tank (piercing-strike-ii-tank) | Breaching Strike Tank | Piercing e Breaching | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Piercing Strike II Warrior (piercing-strike-ii-warrior) | Breaching Strike Warrior | Piercing e Breaching | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Pressure / Provoke (pressure-provoke) | Pressure / Provoke | Pressure e Provoke | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Rage (rage) | Rage | Momentum e payoffs | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Rally I Tank (rally-i-tank) | Rally I Tank | Rally | P1 | RallyITankAffected |
| Rally I Warrior (rally-i-warrior) | Rally I Warrior | Rally | P1 | RallyIWarriorAffected |
| Rally II Tank (rally-ii-tank) | Inspiration | Rally | P1 | RallyIiTankAffected |
| Rally II Warrior (rally-ii-warrior) | Bloodlust | Rally | P1 | RallyIiWarriorAffected |
| Second Wind (second-wind) | Second Wind | Second Wind | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Severing Strike I (severing-strike) | Severing Strike I | Severing | P1 | SeveringCastI, SeveringHitI |
| Severing Strike II (severing-strike-ii) | Severing Strike II | Severing | P1 | SeveringCastII, SeveringHitII |
| Severing Strike III (severing-strike-iii) | Severing Strike III | Severing | P1 | SeveringCastIII, SeveringHitIII |
| Shoulder Rush I (shoulder-rush) | Shoulder Rush I | Shoulder Rush | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Shoulder Rush II Tank (shoulder-rush-ii-tank) | Shield Rush | Shoulder Rush | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Shoulder Rush II Warrior (shoulder-rush-ii-warrior) | Blade Rush | Shoulder Rush | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Tank Stance (tank-stance) | Tank Stance | Stances Fighter | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| War Leap (war-leap) | War Leap | War Leap | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Warrior Stance (warrior-stance) | Warrior Stance | Stances Fighter | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Arcane Burst (arcane-burst) | Arcane Burst | Arcane Burst | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Arcane Weaving I (arcane-weaving-i) | Arcane Weaving I | Arcane Weaving | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Arcane Weaving II (arcane-weaving-ii) | Arcane Master | Arcane Weaving | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Blink (blink) | Blink | Blink | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Cleanse Mage (cleansemage) | Cleanse Mage | Cleanse | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Coil (coil) | Coil | Coil | P1 | CoilHit, CoilProc7, CoilChain |
| Combust I (combust-i) | Combust I | Combust | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Combust II (combust-ii) | Combust Combo | Combust | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Elemental Weaver I (elemental-weaver-i) | Elemental Weaver I | Elemental Weaver | P0 | ElementalWeaverILightningMemory |
| Elemental Weaver II (elemental-weaver-ii) | Elemental Master | Elemental Weaver | P0 | ElementalWeaverIiLightningMemory |
| Fire Bolt I (fire-bolt-i) | Fire Bolt I | Fire Bolt e Fire Ball | P1 | FireBoltIFlight, FireBoltIImpact |
| Fire Bolt II (fire-bolt-ii) | Fire Ball | Fire Bolt e Fire Ball | P1 | FireBoltIIFlight, FireBoltIIImpact, FireBoltIISpread |
| Frost Lance I (frost-lance-i) | Frost Lance I | Frost Lance e Permafrost | P1 | FrostLanceIImpact |
| Frost Lance II (frost-lance-ii) | Permafrost | Frost Lance e Permafrost | P1 | FrostLanceIiImpact, FrostLanceIiConditionalControl |
| Glacial Spike I (glacial-spike-i) | Glacial Spike I | Glacial Spike | P1 | GlacialSpikeIGroundArea, GlacialSpikeIImpact |
| Glacial Spike II (glacial-spike-ii) | Glacial Spike Combo | Glacial Spike | P1 | GlacialSpikeIiGroundArea, GlacialSpikeIiImpact, GlacialSpikeIiConditionalControl |
| Iceberg (iceberg) | Iceberg | Iceberg | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Laser (laser) | Laser | Laser | P1 | LaserContact |
| Mana Barrier I (mana-barrier-i) | Mana Barrier I | Mana Barrier e Overcharge | P0 | ManaBarrierIHoldLow, ManaBarrierIHoldHigh |
| Mana Barrier II Overcharge (mana-barrier-ii-overcharge) | Overcharge | Mana Barrier e Overcharge | P0 | ManaBarrierIiOverchargeHoldLow, ManaBarrierIiOverchargeHoldHigh |
| Mana Storm (mana-storm) | Mana Storm | Mana Storm | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Manifest (manifest) | Manifest | Mage Manifest e Weave | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Mist (mist) | Mist | Mist | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Static Bolt I (static-bolt-i) | Static Bolt I | Static Bolt | P0 | StaticBoltIHit, StaticBoltIChain, StaticBoltIGroundArea |
| Static Bolt II (static-bolt-ii) | Conductive Lightning | Static Bolt | P0 | StaticBoltIiHit, StaticBoltIiChain, StaticBoltIiGroundArea |
| Tempest (tempest) | Tempest | Tempest | P1 | TempestIce, TempestLightning, TempestGroundImpact, TempestFrostImpact, TempestStormArea, TempestTelegraph, TempestLightningHit, TempestSappedProc |
| Thunderstrike I (thunderstrike-i) | Thunderstrike I | Thunderstrike | P1 | ThunderstrikeIHit |
| Thunderstrike II (thunderstrike-ii) | Thunderstrike Combo | Thunderstrike | P1 | ThunderstrikeIiHit, ThunderstrikeIiSplashArea, ThunderstrikeIISplash |
| Vortex (vortex) | Vortex | Vortex | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Weave (weave) | Weave | Mage Manifest e Weave | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Astral Aura Moon (astral-aura-moon) | Moon Aura | Sun Aura e Moon Aura | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Astral Aura Sun (astral-aura-sun) | Sun Aura | Sun Aura e Moon Aura | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Astral Pull (astral-pull) | Astral Pull | Astral relocation | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Astral Step (astral-step) | Astral Step | Astral relocation | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Astral Veil (astral-veil) | Astral Veil | Astral Veil | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Black Hole I (black-hole-i) | Black Hole I | Black Hole | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Black Hole II (black-hole-ii) | Black Hole II | Black Hole | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Bright Star (bright-star) | Bright Star | Bright Star Full Moon e Eclipse | P0 | BrightStarHeal, BrightStarCasterProc |
| Cleanse Mystic (cleansemystic) | Cleanse Mystic | Cleanse | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Connection I Ally (connection-i-ally) | Connection I Ally | Connection | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Connection I Enemy (connection-i-enemy) | Connection I Enemy | Connection | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Connection II Ally (connection-ii-ally) | Connection II Ally | Connection | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Connection II Enemy (connection-ii-enemy) | Connection II Enemy | Connection | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Cosmic Ray I (cosmic-ray-i) | Cosmic Ray I | Cosmic Ray | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Cosmic Ray II (cosmic-ray-ii) | Cosmic Ray II | Cosmic Ray | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Eclipse (eclipse) | Eclipse | Bright Star Full Moon e Eclipse | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Ether I Ally (ether-i-ally) | Ether I Ally | Ether | P1 | EtherIAllyHeal |
| Ether I Enemy (ether-i-enemy) | Ether I Enemy | Ether | P1 | EtherIEnemyConfirmedDamage |
| Ether II Ally (ether-ii-ally) | Ether II Ally | Ether | P1 | EtherIiAllyHeal, EtherIiAllyConditionalBuff |
| Ether II Enemy (ether-ii-enemy) | Ether II Enemy | Ether | P1 | EtherIiEnemyConfirmedDamage |
| Full Moon (full-moon) | Full Moon | Bright Star Full Moon e Eclipse | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Lullaby I (lullaby) | Lullaby I | Lullaby e Nightmare | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Lullaby II Nightmare (lullaby-ii-nightmare) | Lullaby II Nightmare | Lullaby e Nightmare | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Moon Stance (moon-stance) | Moon Stance | Mystic stances | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Resurrect (resurrect) | Resurrect | Resurrect | P1 | ResurrectComplete |
| Serenity (serenity) | Serenity | Serenity | P1 | SerenityHeal, SerenitySleepApply |
| Spirit of the Comet Moon (spirit-of-the-comet-moon) | Spirit of the Comet Moon | Spirits | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Spirit of the Comet Sun (spirit-of-the-comet-sun) | Spirit of the Comet Sun | Spirits | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Spirit of the Orbit Moon (spirit-of-the-orbit-moon) | Spirit of the Orbit Moon | Spirits | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Spirit of the Orbit Sun (spirit-of-the-orbit-sun) | Spirit of the Orbit Sun | Spirits | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Spirit of the Star Moon (spirit-of-the-star-moon) | Spirit of the Star Moon | Spirits | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Spirit of the Star Sun (spirit-of-the-star-sun) | Spirit of the Star Sun | Spirits | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Sun Stance (sun-stance) | Sun Stance | Mystic stances | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Backstab I (backstab) | Backstab I | Backstab e Ambush | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Backstab II (backstab-ii) | Ambush | Backstab e Ambush | P1 | BackstabIIConfirmedHit, BackstabIIStunApply, BackstabIIPoisonApply, BackstabIIBleedApply, BackstabIIHitSparks |
| Basic Attack — Bleed (basic-attack-bleed) | Basic Attack — Bleed | Basic Attack DoT existente | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Basic Attack — Poison (basic-attack-poison) | Basic Attack — Poison | Basic Attack DoT existente | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Bleed Stance (bleed-stance) | Bleed Stance | Scout stances | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Blinding Dart (blinding-dart) | Blinding Dart | Blinding Dart e Torpor | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Cleanse Scout (cleansescout) | Cleanse Scout | Cleanse | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Evasion (evasion) | Evasion | Evasion | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Exploit Weakness I (exploit-weakness-i) | Exploit Weakness I | Exploit Sentence Executioner | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Exploit Weakness II (exploit-weakness-ii) | Sentence | Exploit Sentence Executioner | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Exploit Weakness III (exploit-weakness-iii) | Executioner | Exploit Sentence Executioner | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Hemorrhage (hemorrhage) | Hemorrhage | Hemorrhage Poison Sac Sickness | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Long Jump (long-jump) | Long Jump | Long Jump e Quickstep | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Poison Sac (poison-sac) | Poison Sac | Hemorrhage Poison Sac Sickness | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Poison Stance (poison-stance) | Poison Stance | Scout stances | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Quickstep I (quickstep-i) | Quickstep I | Long Jump e Quickstep | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Quickstep II (quickstep-ii) | Quickstep II | Long Jump e Quickstep | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Rapid Attack (rapid-attack) | Rapid Attack | Rapid Attack | P0 | Sem componente independente associado no inventário atual; rever decomposição. |
| Sand Shot (sand-shot) | Sand Shot | Sand Shot | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Sickness (sickness) | Sickness | Hemorrhage Poison Sac Sickness | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Smoke Bomb I (smoke-bomb-i) | Smoke Bomb I | Smoke Bomb | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Smoke Bomb II (smoke-bomb-ii) | Shroud Bomb | Smoke Bomb | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Torpor (torpor) | Torpor | Blinding Dart e Torpor | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Vine Field I (vine-field-i) | Vine Field I | Vine Field e Entangle | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Vine Field II (vine-field-ii) | Entangle | Vine Field e Entangle | P1 | Sem componente independente associado no inventário atual; rever decomposição. |
| Volley I · Bleed (volley-i-bleed) | Volley I · Bleed | Volley e Narrowing Volley | P1 | VolleyIBleedFlight, VolleyIBleedHit |
| Volley I · Poison (volley-i-poison) | Volley I · Poison | Volley e Narrowing Volley | P1 | VolleyIPoisonFlight, VolleyIPoisonHit |
| Volley II · Bleed (volley-ii-bleed) | Narrowing Volley Bleed | Volley e Narrowing Volley | P1 | VolleyIIBleedFanFlight, VolleyIIBleedHit, VolleyIIBleedPiercingFlight, VolleyIIBleedAim, VolleyIIBleedAimEnd |
| Volley II · Poison (volley-ii-poison) | Narrowing Volley Poison | Volley e Narrowing Volley | P1 | VolleyIIPoisonFanFlight, VolleyIIPoisonHit, VolleyIIPoisonPiercingFlight, VolleyIIPoisonAim, VolleyIIPoisonAimEnd |
| Controlo — Laboratório (control) | Controlo — Laboratório | CC partilhados | P0 | CCRootActive, CCRootNaturalEnd, CCRootCleanse, CCRootDeath |

Os detalhes por linha, eventos, testes, paths, hashes e contagens estáticas encontram-se em `Evidence/gameplay-vfx-assessment-20261004.json`.
