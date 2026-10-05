"""Assessment of current lab assets, not a build or a gameplay migration.

Family decisions below are design proposals grounded in current product rules.
Counts and hashes are collected from the current asset/source manifests.
"""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
FOUNDATION = Path('C:/Dev/SanctaMMO-Foundation-5.8')

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

# Each current catalogue row belongs to one manually reviewed functional family.
FAMILIES = []
def family(name, slugs, priority, events, adjustment, cuts, tests):
    FAMILIES.append(dict(name=name, slugs=slugs.split(), priority=priority,
        required_events=events, adjustment=adjustment, cuts=cuts, acceptance_tests=tests))

family('Cleanse', 'cleanse cleansemage cleansemystic cleansescout', 'P1',
    'Remoção confirmada de Debuff/CC ou cancelamento de ForcedDisplacement; alvo real elegível.',
    'Um burst por resolução efetiva; partilhar módulos e distinguir paletas. Mystic suporta aliado; os outros são self-only. Remover apenas os cues dos estados realmente removidos.',
    'Retirar sucesso em tentativa sem remoção e apagar a ideia de limpar Burn/Bleed/Poison, HoT, Shield ou recursos por defeito.',
    'Zero estados removidos; vários CC; ForcedDisplacement; DoT continua; alvo Mystic inválido.')
family('Stances Fighter', 'warrior-stance tank-stance', 'P1',
    'Entrada/saída/swap de stance; consumo/limpeza de Momentum confirmado.',
    'Separar transição curta do marcador persistente na cintura. Preservar a identidade magenta/ciano e manter visível durante Skills compatíveis com Dodge/Guard.',
    'Não acrescentar anel no chão; não repetir a transição em cada frame nem renovar a janela defensiva de Dodge.',
    'Swap limpa Momentum; Guard+Skill sem movimento; Guard cancelado por Skill com movimento; diferentes proporções de personagem.')
family('Battlecry e Challenge', 'battlecry-challenge-i-tank battlecry-challenge-i-warrior battlecry-challenge-ii-tank battlecry-challenge-ii-warrior', 'P1',
    'Pulso de cast; resultados por alvo; pre-Silence em Battlecry II; fim natural do Taunt concreto em Challenge II.',
    'Manter pulso simples e diferença de intensidade aprovada. Ligar Silence/Fear/Taunt/Root aos cues partilhados; conservar a forma snapshot após swap.',
    'Nunca agendar Fear/Root por tempo do preview. Taunt ignorado, remoção precoce ou Cleanse não disparam Root.',
    'Pre-Silence verdadeiro/falso; Taunt aplicado/ignorado; natural expiry vs Cleanse/morte; swap depois do cast.')
family('Momentum e payoffs', 'rage bulwark momentum-mastery', 'P1',
    'Consumo confirmado de Momentum; Heal ou Shield efetivo; restituição de Stamina de Momentum Mastery.',
    'Separar consumo, resposta no caster e marcador de recurso. Fornecer quantidade consumida, magnitude efetiva e fim do estado; não inferir magnitude do rank.',
    'Não manter uma aura de Heal. Não apresentar Momentum Mastery em Rally nem num ganho de Momentum.',
    '0/máximo/intermédio; HP cheio; Shield existente; consumo por Rage/Bulwark vs Rally; UI consistente.')
family('Chains', 'chains chains-ii', 'P1',
    'Launch, primeiro hit válido, ligação, Root concreto, recast aceite, Interrupt resolvido, tentativa de Pull e remoção.',
    'A separação já existe. Substituir endpoints gravados por sockets reais; conservar uma ligação no recast e uma oportunidade associada ao Root da mesma fonte.',
    'Não reaplicar Root na chegada. Não mostrar movimento quando o Pull é rejeitado; o Interrupt já resolvido pode manter o seu cue.',
    'Outro caster; Root ignorado; recast único; alvo morre; endpoint móvel; Pull rejeitado; colisão bloqueante.')
family('Crushing Blow e Crushing Combo', 'crushing-blow crushing-blow-ii', 'P1',
    'Bash AoE; hit; pre-Slow; Stun condicional antes do novo Slow.',
    'Decompor chão de cast e feedback por alvo; reutilizar impacto físico e CC. Aumentar o II por payoff confirmado, não por partículas permanentes.',
    'Retirar Stun predefinido e anéis individuais nos alvos; evitar segundo flash se o impacto já confirma contacto.',
    'Pre-Slow falso/verdadeiro; alvos diferentes no mesmo cast; AoE sem gate de Accuracy/Evasion.')
family('Defiant Presence', 'defiant-presence', 'P1',
    'Estado defensivo ativo/removido; avaliação de nova origem hostil pela regra de distância.',
    'Manter só a cúpula azul aprovada; controlar duração e origem usada na regra. A cúpula comunica o estado, não calcula a elegibilidade.',
    'Excluir os projéteis da demonstração e reações decorativas a hits. Não sugerir que remove efeitos hostis já existentes.',
    'Origem dentro/fora do limite; efeito preexistente; caster muda posição; fim antecipado.')
family('Piercing e Breaching', 'piercing-strike piercing-strike-ii-tank piercing-strike-ii-warrior', 'P1',
    'Linha curta de cast; cada alvo atingido; pre-Slow; payoff Warrior/Tank; Slow normal.',
    'Preservar a linha e ligar a origem à mão/corpo adequado a qualquer arma. Separar payoff por alvo e snapshot de stance.',
    'Não usar slow criado pelo próprio hit para habilitar o payoff; não trocar a forma já executada depois de stance swap.',
    'Multi-target; sem alvo; pre-Slow; swap; Sword/Bow/Staff sem requisito de arma inventado.')
family('Pressure e Provoke', 'pressure-provoke', 'P1',
    'Targeted hit; dano; Hindered em Warrior ou Taunt em Tank; stance da execução.',
    'Separar ataque, confirmação de hit e aplicação de estado. Auditar a cobertura das duas formas no mesmo protótipo; usar IDs de forma distintos se a leitura muda.',
    'Não fazer hit/proc após Miss ou target inválido; não usar apenas recoloração para a relação de alvo.',
    'Duas stances; targeted Miss; alvo morre; Taunt já ativo; alcance real.')
family('Rally', 'rally-i-tank rally-i-warrior rally-ii-tank rally-ii-warrior', 'P1',
    'Consumo de Max Momentum; pulso do caster; aplicação efetiva em cada membro elegível da Party.',
    'Componentes de afetados já separados. A integração decide a lista; base Vigor e upgrades dependem da forma snapshot.',
    'Não percorrer manequins gravados nem incluir toda a Raid por defeito. Não manter quatro auras de buffs no corpo.',
    'Fora da Party; borda do raio; ally/self; aplicação ignorada; swap depois de consumo.')
family('Second Wind', 'second-wind', 'P1',
    'Heal confirmado a partir do dano que reduziu HP na janela authored, limitado por MissingHP.',
    'Manter burst mais intenso; alimentar magnitude efetiva e presa ao corpo. O valor não deve vir do brilho nem de dano absorvido pelo Shield.',
    'Evitar pulse persistente ou cue forte de cura quando Heal efetivo é zero.',
    'HP cheio; dano só no Shield; dano na janela; missing HP reduzido; cast cancelado.')
family('Severing', 'severing-strike severing-strike-ii severing-strike-iii', 'P1',
    'Corte escolhido pelo rank; hit por alvo; sequência de cada par fonte/alvo; aplicação efetiva dos payoffs.',
    'Cortes, hits e marcas existem. Parametrizar as marcas e o fim/consumo/reset da sequência; alinhar corte com a animação real sem o transformar num ataque básico de arma.',
    'Rever SeveringHit + marca para retirar confirmação duplicada; rank III não significa marca 3. Não gerar nova marca em Miss.',
    'Ranks 1/2/3 × sequências 1/2/3; dois alvos/dois casters; reset; morte; aplicação de estados ignorada.')
family('Shoulder Rush', 'shoulder-rush shoulder-rush-ii-tank shoulder-rush-ii-warrior', 'P1',
    'Rush iniciado; deslocamento real; chegada válida; hit; resultado contextual; cancelamento.',
    'Decompor preparação/travel/arrival. Ajustar rasto à velocidade real e proteger a leitura em Guard/Dodge e com qualquer arma.',
    'Não agendar hit de chegada após colisão, abandono ou ForcedDisplacement. Shield Rush não ganha requisito de Shield só pelo nome.',
    'Chegada válida vs interrompida; colisão; deslocamento externo; tank cancela Guard ao mover; stance snapshot.')
family('War Leap', 'war-leap', 'P1',
    'Channel pré-salto; release; trajetória; aterragem ofensiva válida; hit/Slow.',
    'Faltam estados controláveis de channel e componentes de takeoff/landing separados do cast completo.',
    'Não usar contacto tardio com chão como autorização de aterragem ofensiva de leap abandonado.',
    'Channel cancelado; duração variável; teto/colisão; ForcedDisplacement; aterragem válida.')
family('Mage Manifest e Weave', 'manifest weave', 'P0',
    'Modo ativo; evento Manifest ou Weave elegível; recurso real ganho/consumido.',
    'Separar swap, marcador persistente, recurso e ganho. Retirar a gravação de casts auxiliares e permitir contagem real de Shards e máximo data-driven.',
    'Não mostrar Burn/Slow/Sapped em Weave. Um cast com muitos hits dá no máximo um evento de recurso.',
    '0/1/máximo de Shards; swap; multi-hit; Miss; modo capturado no ponto definido pela ability.')
family('Arcane Burst', 'arcane-burst', 'P1',
    'Consumo de todos os Shards na admissão; launch; flight; hit e AoE confirmados.',
    'Um projétil com raio/intensidade alimentados pelo consumo real. Separar recurso consumido, voo e impacto, sem exigir nova skill por contagem.',
    'Não criar um projétil por Shard nem ganhos de recurso a partir dos callbacks de impacto.',
    'Consumo baixo/máximo; target móvel; Miss; impacto perto de parede; câmara do jogo.')
family('Arcane Weaving', 'arcane-weaving-i arcane-weaving-ii', 'P0',
    'Contagem real, ganho de Shards capped 10 e redução de cooldown uma vez por execução elegível no máximo.',
    'A órbita restaurada deve persistir sem Shards. Expor Count/MaxCount e evento Gain/Consume/MaxProc; os dados aV/aG atuais são gravados.',
    'Retirar estados hardcoded e qualquer aura de cooldown. Arcane Master não produz um evento por impacto.',
    '0/1/2/9/10; ganho capped; consumir; já máximo; múltiplos hits e entrada em relevância tardia.')
family('Elemental Weaver', 'elemental-weaver-i elemental-weaver-ii', 'P0',
    'Memória vazia/um elemento/dois; gain/replace/consume; par elegível e syntheses da especialização.',
    'Cores já controláveis e testadas. Falta mask/count de ocupação, GainAge por slot e ReadyPair. No I um segundo elemento diferente substitui a preparação incompleta; II habilita pares mistos.',
    'Não manter sempre dois cristais; não oferecer Mist/Laser/Tempest no I; não criar seis sistemas só para as combinações de cor.',
    'Vazio, F, FF, FI antes/depois de Master, LL, consume, replace e pooling sem memória anterior.')
family('Fire Bolt e Fire Ball', 'fire-bolt-i fire-bolt-ii', 'P1',
    'Launch; voo homing/dirigido conforme ability; hit confirmado; pre-Burn; spread elegível em Manifest; novo Burn ou evento Weave.',
    'Esfera/rasto atuais aprovados pelo utilizador. Preservar a forma e substituir trajetória fixa por owner real; impactos/spread já separados.',
    'Cortar spread em Weave, Burn automático em Miss e destinos gravados. Não voltar a alterar a silhueta aprovada por iniciativa genérica de polish.',
    'Miss; parede; alvo móvel/morto; pre-Burn false/true; Manifest/Weave; alvos secundários limitados e deduplicados.')
family('Combust', 'combust-i combust-ii', 'P1',
    'Targeted hit; pre-Burn/consumo; burst; assinatura Manifest ou evento Weave.',
    'Separar contacto e payoff de consumo no alvo. O círculo de fogo pedido pelo utilizador é composição no alvo, não uma nova área de dano.',
    'Retirar qualquer interpretação do círculo como hazard persistente; não representar consumo de Burn inexistente.',
    'Pre-Burn 0/máximo; Weave; alvo move; targeted Miss; consumo atómico e aplicação posterior.')
family('Frost Lance e Permafrost', 'frost-lance-i frost-lance-ii', 'P1',
    'Voo; hit; pre-Slow; debuffs condicionais; Slow Manifest ou recurso Weave.',
    'Gelo aprovado preservado. Impactos/condicional já separados; parametrizar flight endpoints e controlar a magnitude do segundo efeito pelo resultado.',
    'Não confundir Hindered/Dazed com Stun nem manter gelo no alvo como estado persistente.',
    'Pre-Slow true/false; Miss; Weave; mudanças de fundo e vistas próximas/distantes.')
family('Glacial Spike', 'glacial-spike-i glacial-spike-ii', 'P1',
    'Cone confirmado; área visual; cada alvo atingido; pre-Slow e Stun do II; assinatura Manifest/Weave.',
    'Conservar proposta B com caos/inclinação/neve até feedback. Usar cone/range/posição reais e nunca tirar o limite útil na qualidade baixa.',
    'Retirar procs agendados e colisão dos meshes de neve/spikes decorativos; Stun só no II e pre-Slow verdadeiro.',
    'Borda cone; targets fora; múltiplos hits; terreno inclinado; visão do limite com névoa e outros VFX.')
family('Static Bolt', 'static-bolt-i static-bolt-ii', 'P0',
    'Voo primário; impacto AoE; pre-Sapped de cada elo em II; lista autoritativa deduplicada; Manifest/Weave.',
    'Hit, chão e links existem. StaticBoltIChain é nome ambíguo: auditar a forma para classificar contacto caster-alvo vs propagação, que só o II habilita.',
    'Não tratar StaticBoltIChain como permissão de chain no I. Sapped criado no mesmo hit não autoriza encadeamento; um recurso Weave por execução.',
    'Sem pre-Sapped; chain termina no primeiro alvo não elegível; dedup; morte; empate por Entity ID; nenhum link fantasma.')
family('Thunderstrike', 'thunderstrike-i thunderstrike-ii', 'P1',
    'Strike instantâneo; hit ST; pre-Sapped habilita splash; pre-Stunned habilita burst ST; ambos podem coexistir.',
    'Há splash separado; assegurar cue específico/ramo do burst pre-Stunned, sem o esconder numa animação automática do cast.',
    'Não aplicar Root nem misturar splash com pre-Stun. Em Weave não há nova assinatura Sapped.',
    'Quatro combinações de pre-Sapped/pre-Stun; alvo único e splash; Weave; alvo morre antes da resolução.')
family('Mana Barrier e Overcharge', 'mana-barrier-i mana-barrier-ii-overcharge', 'P0',
    'Channel variável; Shield final único; recast Overcharge só com Shield elegível; consumo de todo Shield atual.',
    'Hold já testado. Separar visual de channel/barreira de formação de Shield e Overcharge. Low/High são fixtures, não quatro skills adicionais.',
    'Não repetir channel ou produzir Shield por tick; não agendar Overcharge no preview de Barrier; não manter esfera universal de Shield.',
    'Hold curto/longo; cancel/Interrupt; MP gasto variável; Shield de outra fonte; consumo total; pooling reset.')
family('Mana Storm', 'mana-storm', 'P0',
    'Área fixa em origem self; admissão de Skill dentro; owner e duração; proc no caster da Skill elegível.',
    'Círculo completo já revisto. Falta pulso da área + resposta de admission separados e parametrizados; preservar a posição inicial quando o Mage se move.',
    'Não pulsar em loop, em Basic Attack/Guard/Dodge/Sprint, nem representar buff de Heal/Shield/CC que a regra não concede.',
    'Dentro/fora à admissão; caster sai depois; Basic Attack; duas áreas não suportadas; cancelamento e fim.')
family('Blink', 'blink', 'P1',
    'Preparação local prevista; relocation confirmada; origem/destino; cancelamento/rejeição.',
    'Preservar smoothness revista. Separar partida/chegada e ligar ao resultado; o cast/channel em curso pode continuar sem reiniciar a origem da outra skill.',
    'Não apresentar chegada em teleport recusado nem renovar Dodge/Guard/Shield por visual.',
    'Root no instante da relocation; LOS; Cast/Channel em curso; deslocamento externo; destino inválido.')
family('Coil', 'coil', 'P1',
    'Synthesis LL; Shield no Mage; AoE Lightning; Root apenas sobre pre-Sapped; novo Sapped.',
    'Preservar separação e alimentar os alvos reais. CoilChain não autoriza uma cadeia de ataques não definida; classificar como ligações do cast/AoE.',
    'Não criar Root base, chain sem regra, pulse de hit persistente no Shield ou novo SkillCount por alvo.',
    'Pre-Sapped; Shield sem alvos; forma LL; múltiplos alvos; remoção do Root.')
family('Iceberg', 'iceberg', 'P0',
    'Spawn de terreno temporário destrutível; estado por segmento/objeto; dano/destroy/expiry; área Slow.',
    'VFX atual é referência de aparência. Necessita owner de terreno, malha/colisão/LOS/projéteis reais e estados de dano/destruição alinhados; ângulo ainda por aprovar.',
    'Não usar um Niagara decorativo como único terreno bloqueante; não manter blockers invisíveis após dissolução.',
    'Caminho/LOS/projétil bloqueados; ataque ao terreno; destruição parcial authored; expiry; sem omnivamp não autorizado.')
family('Laser', 'laser', 'P1',
    'Beam ativo; aim steerable; endpoint real; contacto entra/sai; ticks autoritativos; cancelamento.',
    'Origem e contacto já existem. Parametrizar direção, endpoint e intensidade; manter origem legível e contacto apenas enquanto validado.',
    'Não mostrar sparks permanentes num extremo vazio nem resolver dano com colisão visual; ticks não são novas Skills.',
    'Mover aim; perder alvo; parede; atingir outro alvo; cancelamento; endpoint em superfície inclinada.')
family('Mist', 'mist', 'P1',
    'Área estacionária FI; concealment/target denial ativo; entrada/saída e remoção.',
    'Área e névoa têm de usar a geometria/duração reais. Definir leitura owner/aliado/inimigo sem esconder limites de hazards concorrentes.',
    'Não sugerir dano, Blind ou Slow sem autoria; reduzir sprites que enchem o ecrã perto da câmara.',
    'Câmara dentro; alvo entra/sai; relevância tardia; quality Low; outra área hostil sobreposta.')
family('Tempest', 'tempest', 'P1',
    'Área persistente; telegraph por impacto; strike Ice/Lightning; hit; payoff pre-Slow/pre-Sapped; remoção.',
    'Manter correção 8/9/10 e gelo Frost aprovado. Componentes separados precisam de um impacto por evento, posições/cores snapshot e duração de aviso real.',
    'Nunca reativar TempestRootApply nem loop gravado de hits/procs. O cue Ice não deve arrastar Lightning e vice-versa.',
    'Gelo vs Lightning; pre-states; cancel depois do aviso; área expira; carga de impactos concorrentes; sinal legível em Low.')
family('Vortex', 'vortex', 'P1',
    'Synthesis FF; grande projectile linear; hits; Burn; ForcedDisplacement lateral confirmado.',
    'Separar voo/passagem, impacto e movimento lateral de cada alvo; preservar melhoria atual da forma.',
    'Não deslocar visualmente um target sem comando aceite; Burn e movimento não são CC Root.',
    'Vários alvos; obstáculo; comando de deslocamento rejeitado; fim da viagem; câmara junto do projétil.')
family('Mystic stances', 'sun-stance moon-stance', 'P1',
    'Stance ativa; ChargeGrantEvent elegível; pools Sun e Moon; consume; swap.',
    'Separar toggle, marcador persistente e recurso. Os dois pools conservam identidade e não devem ser confundidos com Spirit variante.',
    'Sem cooldown/resource timer no VFX; não transformar troca de stance em mudança dos Spirits já colocados.',
    'Pools 0/máximo; swaps; ganho qualificado; consumo atomic; outra raça/proporção.')
family('Sun Aura e Moon Aura', 'astral-aura-sun astral-aura-moon', 'P1',
    'Toggle independente da stance; aura ativa; upkeep válido; membros elegíveis.',
    'Manter IDs de aura próprios e diferenciar toggle/área de alcance/resposta de membros. Parametrizar owner e alcance.',
    'Não inferir aura a partir da stance nem desenhar uma aura extra por Buff concedido.',
    'Aura igual/diferente da stance; MP termina; ally sai; toggle rápido; repetição de relevância.')
family('Astral relocation', 'astral-pull astral-step', 'P1',
    'Start/delay quando authored; recheck final; relocation real; partida e chegada; falha.',
    'Step move só Mystic; Pull move só aliado válido Party/Raid. Usar origem/destino confirmados e identidade da vida/encarnação quando exigida.',
    'Não desenhar o ally a mover no Step nem chegada em Pull inválido. Não tratar teleport como ForcedDisplacement.',
    'Quem se move; aliado morreu/respawnou; checks finais; Root; cancelamento.')
family('Astral Veil', 'astral-veil', 'P1',
    'Área/barreira ativa; gameplay Projectile Intercepted; remoção.',
    'Separar estado e burst pequeno de interceção. VFX deve coincidir com a superfície autoritativa, dos dois lados.',
    'Não bloquear visualmente personagens, LOS, beams, cones ou ground AoE; não mostrar fraturas por HP porque Veil não tem HP.',
    'Projétil aliado/hostil; beam atravessa; character atravessa; expiry; latência e evento Intercepted único.')
family('Black Hole', 'black-hole-i black-hole-ii', 'P1',
    'Spawn; query inicial única e Pull útil; expiry; nova query independente do II; Damage/Silence.',
    'Separar área, displacement inicial e payoff final; lista final não é a lista capturada no começo.',
    'Retirar pull contínuo/repetido e dano agendado de alvos que já saíram. Não manter lock por tempo do visual.',
    'Entra depois; sai antes; no centro; deslocamento bloqueado; query final independente; Cleanse durante Pull.')
family('Bright Star Full Moon e Eclipse', 'bright-star full-moon eclipse', 'P0',
    'Consumo de recurso; Shield Instant AoE Bright Star; GroundPoint Projectile Full Moon; payoff misto Eclipse.',
    'BrightStarHeal é spark de Shield e deve ser identificado como ShieldApply. Full Moon atual conserva chão/pilares, mas falta flight separado. Eclipse distingue aliado Shield e hostil Damage/Silence.',
    'Retirar interpretação de heal e atraso de gameplay pela frente do pulso Bright Star. Não mostrar Shield como invulnerabilidade; não disparar Eclipse automático em pools cheios.',
    'Ally/enemy; consumo máximo/insuficiente; flight Full Moon; dispel/removal; instant targets vs cosmetic pulse.')
family('Connection', 'connection-i-ally connection-i-enemy connection-ii-ally connection-ii-enemy', 'P0',
    'Instant attach; tether válido; ticks reais; quebra de range; expiry natural; payoff e spread do II.',
    'Manter intensidade II; separar Attach/Link/Tick/NaturalEnd/Break/Spread com endpoints móveis. O link representa a instância da fonte, não um buff genérico.',
    'Não produzir ritual final em range break, morte ou remoção precoce. Não combinar heal/damage periódico com uma duração fixa de preview.',
    'Ally/enemy; natural vs early end; range; life binding; spread elegível; dois casters e câmara cruzando link.')
family('Cosmic Ray', 'cosmic-ray-i cosmic-ray-ii', 'P0',
    'Projectile de entrega; pending ResolveAt; heal atrasado por charge; life/encarnation original válida.',
    'Fonte atual mostra manifestação/pending/heal gravados. Falta flight de entrega independente e Pending/Resolve/Cancel orientados por vida original e relógio do owner.',
    'Não curar nova encarnação nem recontar charge no VFX; charges e recharge são HUD.',
    'Dois resolves independentes; alvo morre/respawna; deslocamento; validade final; cancel sem Heal.')
family('Ether', 'ether-i-ally ether-i-enemy ether-ii-ally ether-ii-enemy', 'P1',
    'Flight; heal aliado/damage hostil confirmado; Buff ou Debuff preexistente para proc do II.',
    'Preservar formas de esfera/crescente e procs separados. Auditar cobertura do proc inimigo II e expor a trajetória real em ambos.',
    'Não habilitar proc com o estado criado no mesmo hit. Não acrescentar spill/chain e não resolver dano num alvo inelegível.',
    'Buff/Debuff false/true; ally/enemy; Miss hostil; target móvel; pooling entre relações diferentes.')
family('Lullaby e Nightmare', 'lullaby lullaby-ii-nightmare', 'P1',
    'Flight; hit; Sleep atrasado; follow-up Projectile contra inimigo atualmente Sleeping; damage/Fear.',
    'Separar Travel/Hit/PendingSleep/Apply e os eventos do follow-up; ligar ao estado real do alvo na validação.',
    'Não aplicar Sleep por timer se o hit falhou; Nightmare não é obrigado a usar o mesmo alvo da Lullaby inicial.',
    'Sleep removido antes do follow-up; outro alvo Sleeping; Miss; delay; Fear ignorado; morte.')
family('Resurrect', 'resurrect', 'P1',
    'Cast longo; alvo morto elegível; progress; cancel/Interrupt; ressurreição bem-sucedida.',
    'Chão restaurado e Complete separado. Falta hold/cancel guiado por cast real; o cue de sucesso acompanha o resultado, não a pose final do montage.',
    'Não usar barreira que sugira invulnerabilidade nem sucesso após cast falhado.',
    'Cast speed aplicável; interrupt; alvo já ressuscitado; alcance; efeito de chão e sucesso uma vez.')
family('Serenity', 'serenity', 'P1',
    'Telegraph no ponto; ResolveAt único; uma query/resolução; Heal aliado e Sleep hostil.',
    'Componentes Heal/Sleep existem. Parametrizar ponto, raio e duração de aviso, e resolver em alvos reais.',
    'Não manter zona curativa/pulsos depois da resolução nem aplicar Sleep persistentemente pelo material da área.',
    'Entra/sai antes do resolve; owner cancelado segundo contrato; miss não aplicável à AoE; limites e câmara.')
family('Spirits', 'spirit-of-the-comet-moon spirit-of-the-comet-sun spirit-of-the-orbit-moon spirit-of-the-orbit-sun spirit-of-the-star-moon spirit-of-the-star-sun', 'P0',
    'Attach no host; variante Sun/Moon do cast; counter qualificado; Pending; ticks authored; replace/remove/life binding.',
    'Separar Spirit persistente e procs por host/alvo. Comet conta Basics; Star conta Skills elegíveis uma vez; Orbit usa sua cadence e threshold de inimigos válidos.',
    'Retirar duração fixa inferida, forma que muda com stance atual, procs de terceiro golpe animados sem resultado e um contador por impacto.',
    'Mudança de stance; 2→3 eventos; multi-hit; Star Pending; host morto/respawn; replace; Orbit threshold; range de grupo.')
family('Scout stances', 'bleed-stance poison-stance', 'P1',
    'Stance ativa; transição; snapshot por Basic Attack e Volley no ponto authored.',
    'Manter cones mão→cotovelo aprovados, mas ancorar em sockets reais e integrar compatibilidade com armas que tapam a mão.',
    'Não reinterpretar flechas já lançadas depois do swap nem converter a stance em DoT visual contínuo em cada inimigo.',
    'Bow/Crossbow/duas mãos; mãos diferentes; troca durante projectile; arm proportions e layering com Rapid Attack.')
family('Basic Attack DoT existente', 'basic-attack-bleed basic-attack-poison', 'P1',
    'Hit válido de Basic Attack; aplicação efetiva de um Bleed/Poison da stance snapshot.',
    'São apenas overlays de hit já existentes, independentes da arma. Reutilizar sobre o impacto base sem os contar como pacote de Basic Attack completo.',
    'Não aplicar em Miss ou só no finisher da animação; não triplicar impacto com base + overlay + aura de status.',
    'Todas as armas Scout; miss; multi-target cleave; stance swap depois do launch; exatamente um DoT por hit elegível.')
family('Backstab e Ambush', 'backstab backstab-ii', 'P1',
    'Projectile ST; targeted hit; rear arc no hit autoritativo; Interrupt I ou Stun+1 Poison+1 Bleed no II.',
    'A fonte já tem viagem de adaga; não a converter num melee por causa do nome. Completar separação de flight/hit do I e composição compacta do II.',
    'Rever até cinco componentes de hit/proc/sparks para evitar flashes redundantes. Extras do rear nunca aparecem num hit frontal.',
    'Rear/front no hit, não no launch; alvo roda; Miss; vários casters; Stun ignorado mas dano válido.')
family('Blinding Dart e Torpor', 'blinding-dart torpor', 'P1',
    'Projectile ST; hit válido; Blind/Slow efetivo.',
    'Separar flight e impacto/state apply, manter pequenas silhuetas distintas sem criar halo contínuo no alvo.',
    'Não acrescentar chão/hazard/chain; não aplicar debuff depois de Miss.',
    'Range; target móvel; Miss; hit sem nova aplicação por regra de prioridade; fundo claro.')
family('Evasion', 'evasion', 'P1',
    'Ativação do buff; evasão real de targeted hit; expiry/removal.',
    'Manter manto/transparência sem forma de manequim. Separar activation de feedback de Miss/Evasion e respeitar a janela real.',
    'Não sugerir invulnerabilidade, phased collision ou proteção AoE; AoE continua counter posicional.',
    'Targeted Miss; AoE acerta; fim antecipado; outra raça; overlap com Dodge.')
family('Exploit Sentence Executioner', 'exploit-weakness-i exploit-weakness-ii exploit-weakness-iii', 'P0',
    'Projectile ST; pacote pre-hit de Negative States/HP; hit; TakedownQualified e reset da família.',
    'A fonte atual tem apenas vortex/hit no alvo, sem endpoints de voo. Preservar o vortex bronze e acrescentar uma entrega legível + reset local/HUD qualificado.',
    'Não aumentar espetáculo por cada debuff individual; não repetir o dano no reset nem inferir Takedown do desaparecimento do target.',
    'Pre-states; HP% snapshot; flight; Miss; Takedown de fonte qualificada; shared cooldown; reset sem novo hit.')
family('Hemorrhage Poison Sac Sickness', 'hemorrhage poison-sac sickness', 'P1',
    'Elegibilidade de stacks; consumo atómico; entrega authored; burst ST; área de Poison/Sickness; resultados por alvo.',
    'Preservar sangue/viscosidade/bolhas revistos. Separar cast/flight quando authored, consumption/target burst, area active e end; radius/duration fornecidos pelo owner.',
    'Não manter pool de sangue como hazard de Hemorrhage ST. Não usar chão de Poison como aplicação automática fora do volume.',
    'Stacks insuficientes; recheck na resolução; consumo dos dois em Sickness; alvo sai da pool; expiry e cancel.')
family('Long Jump e Quickstep', 'long-jump quickstep-i quickstep-ii', 'P1',
    'Hold do Jump; release fixa landing; trajetória; chegada; dash; charge grant qualificado.',
    'Separar preview local de landing, travel e arrival; alinhar com trajetória efetiva. Quickstep é skill diferente de Dodge Action.',
    'Não mostrar arrival de leap abandonado; não usar VFX para contar/recarregar charges nem renovar defesa de Dodge.',
    'Hold/release/cancel; charges; root; collision; ForcedDisplacement; Takedown grant capped.')
family('Rapid Attack', 'rapid-attack', 'P0',
    'Buff ativo por limite de Basics/expiry; cada Basic qualificado; mão que efetivamente golpeia.',
    'Preservar ativação mais lenta e traços que sobem pelo braço. Separar Activation/PerBasicPulse/End; a versão atual é uma demonstração curta gravada.',
    'Não manter raios permanentes, disparar para a frente nem gerar um proc por cada swing de um Basic lógico.',
    'Basics vs Skills; mãos alternadas; Bow/Staff; Attack Speed; limite de ataques; expiry; Miss conforme regra authored do buff.')
family('Sand Shot', 'sand-shot', 'P1',
    'Cone melee confirmado; hits válidos; Interrupts efetivos por alvo.',
    'Manter ritmo artístico mais lento, mas encaixar no tempo de ataque real; granularidade/debris subordinados ao cone.',
    'Não deixar poeira durar como Blind/Slow/área persistente sem regra; Interrupt não usa cue de Stun.',
    'Alvos no cone/fora; channel alvo interrompido; target sem cast; fundo claro; stress de poeira.')
family('Smoke Bomb', 'smoke-bomb-i smoke-bomb-ii', 'P1',
    'GroundPoint Projectile; impacto inicial; área persistente; entrada/retry; estado owner dentro do próprio fumo em II.',
    'Conservar diferença de cor aprovada e acrescentar distinção de densidade/forma subtil. Separar flight/impact/area e Mist owner de Shroud.',
    'Não mostrar concealment de Shroud em aliados/inimigos nem num Scout fora da sua zona; não bloquear o ecrã com fumo próximo.',
    'Owner entra/sai; outro Scout; retry válido; ground collision; dois fumos; Low preserva perímetro.')
family('Vine Field e Entangle', 'vine-field-i vine-field-ii', 'P1',
    'Área persistente; Slow; check atrasado único de Entangle; Root por inimigo ainda dentro e Slowed.',
    'Manter vinhas on-theme e separar telegraph/area/RootApply/End; usar o volume autoritativo.',
    'Não Root contínuo nem check repetido por pulso de vine; Root visual partilhado evita nova aura por skill.',
    'Sai antes; entra depois; Slow removido; Root já ativo; área em terreno inclinado e efeitos sobrepostos.')
family('Volley e Narrowing Volley', 'volley-i-bleed volley-i-poison volley-ii-bleed volley-ii-poison', 'P1',
    'Aim/hold; shape/range reais; release; stance snapshot; fan simultâneo ou linha fully charged; hit por alvo.',
    'Separação de aim/fan/piercing/hit existe. Parametrizar ChargeProgress/ConeAngle/Range; confirmar o ponto de snapshot no contrato da ability.',
    'Não usar as nove flechas visuais para dar nove DoTs no mesmo alvo; sem curva de gravidade/piercing fora da forma de carga completa authored.',
    'Carga 0/intermédia/máxima; cancelar; stance swap; simultaneidade e direção; alvo dedup; primeira colisão por fan arrow.')
family('CC partilhados', 'control', 'P0',
    'Aplicação efetiva; estado ativo; remoção natural/early/Cleanse/death; fonte e life binding; relevância tardia.',
    'Seis CC persistentes têm variantes de inspeção. Falta Disarm canónico e binding de duração/removal. Preservar a composição conjunta e UI para a duração.',
    'O mapa control é demonstração e não uma skill que aplica seis CC. Não empilhar visual duas vezes quando apply e active usam a mesma forma; não inventar refresh de CC.',
    'Sete tipos combinados; ordem locomotion independente; CC aplicação ignorada; Sleep quebrado; death; join/relevancy e remoção limpa.')

FINDINGS = [
 ('P0','INTEG-01','Dados de demonstração ainda dirigem o efeito',
  'Origins/endpoints/aT/aV e eventos recuperados da referência são gravados; os builders criam um cast finito. As quatro skills com controlos live testados não certificam todas as trajetórias, loops e condições.',
  'Criar adaptadores de eventos/anchors/lifecycle por família e promover componentes; preservar o aspeto aprovado.',
  ['Scripts/build_reference_ports.py','Scripts/build_art_review_20261003.py','Evidence/art-runtime-control-validation.json']),
 ('P0','INTEG-02','Elemental Memory e Shards não cobrem os estados reais',
  'User.ElementA/B escolhem cores, mas aV dos dois cristais está fixo a 1. Contagem/ocupação/gain age dos recursos continuam gravados. O canon atual inclui estado vazio/uma memória e Arcane Weaving capped 10.',
  'Expor ocupação, contagem, eventos gain/replace/consume/ready; manter módulos/meshes partilhados.',
  ['Scripts/prepare_art_review_20261003.py','Source/ArtReview20261003/mage-elemental-weaver-i.json']),
 ('P0','INTEG-03','Algumas entregas faltam à composição atual',
  'Exploit I/II/III atuais só têm camadas no alvo; Full Moon atual só tem chão/pilares; Cosmic Ray mostra manifestação/pending/heal. O canon de classe define Projectile nestas famílias.',
  'Acrescentar ou recuperar Flight separado com trajetória real; manter os impactos existentes. Backstab já tem Projectile na fonte e não precisa de ser redesenhado como melee.',
  ['Source/ArtReview20261003/scout-exploit-weakness-i.json','Source/ArtReview20261003/mystic-full-moon.json','Source/ReferencePorts/mystic-cosmic-ray-i.json']),
 ('P0','INTEG-04','Bright Star está etiquetado como Heal',
  'BrightStarHeal/eligible_target_heal contradiz Shield Instant AoE; a referência descreve spark de Shield. A frente do pulso é estética, não uma resolução de gameplay atrasada.',
  'Na composição de produção usar ShieldApply e eventos de aplicação efetiva. Criar alias de migração; preservar asset/histórico sem renomeação cega.',
  ['Source/ArtReview20261003/BrightStarHeal.json','Evidence/art-revision-integration-contracts.json']),
 ('P0','INTEG-05','Links e efeitos diferidos precisam de causas de fim distintas',
  'Connection, Spirits, Cosmic Ray, Challenge e Black Hole têm condições de natural expiry, fonte, host, vida original ou queries finais; a inspeção finita não as implementa.',
  'Contratos de instância com ExecutionId/Source/TargetLifeId/EndReason; separar loops, procs e payoff final.',
  ['INTEGRAR_REVISAO_VFX.md','VFX-catalog.json']),
 ('P0','INTEG-06','Disarm não está no conjunto CC ativo',
  'Inventário ativo tem Stun/Sleep/Silence/Taunt/Fear/Root; Canon-Current inclui também Disarm.',
  'Criar cue Disarm legível e barato com aplicação/estado/remoção; não sugerir unequip físico ou Stun.',
  ['VFX-separated-components.json']),
 ('P0','INTEG-07','Iceberg precisa de terreno autoritativo',
  'A aparência de blocos Niagara não prova colisão, LOS, blocking de gameplay Projectiles ou destruição.',
  'Um owner de terreno controla geometria/collision/damage/destroy/expiry; VFX segue esse owner.',
  ['VFX-catalog.json','Scripts/prepare_art_review_20261003.py']),
 ('P0','INTEG-08','Ataques básicos por arma e Actions universais em falta',
  'Basic Attack Bleed/Poison são apenas overlays de impacto. Não há pacote por 14 weapon families nem Guard/Dodge/Sprint no catálogo ativo.',
  'Criar perfis de apresentação de ataque e pacote discreto das três Actions, sobre as regras existentes.',
  ['VFX-catalog.json','VFX-separated-components.json']),
 ('P1','INTEG-09','Nomes de components não são permissões de gameplay',
  'StaticBoltIChain e CoilChain podem descrever links de apresentação; os nomes não autorizam propagação no I ou nova cadeia de Coil. As fontes contêm aK 1/2 e endpoints.',
  'Classificar Beam/Contact/ChainHop a partir do shader + evento real, retirar o termo Chain da identidade de produção onde não existe propagação.',
  ['Source/ArtReview20261003/StaticBoltIChain.json','Source/ArtReview20261003/CoilChain.json']),
 ('P1','INTEG-10','Confirmações de hit podem acumular brilho redundante',
  'Backstab II tem hit, stun, poison, bleed e sparks separados; Severing tem hit e marcas. Separação de owners não exige executar todos os flashes simultaneamente.',
  'Compor um contacto dominante, adicionar apenas o payoff elegível e a marca necessária; agrupar triggers do mesmo hit sem fundir lifecycles diferentes.',
  ['VFX-separated-components.json','Scripts/prepare_art_review_20261003.py']),
 ('P1','INTEG-11','Hold e cancel ainda precisam de cobertura além de Mana Barrier',
  'Os quatro testes atuais cobrem Elemental I/II e Mana I/II. War Leap, Long Jump, Volley, Resurrect, Laser e áreas têm clocks/inputs próprios.',
  'Adaptar progresso/phase/owner time e impedir arrival/success em falha; testar sem mudar regras de cast ou refund.',
  ['Evidence/art-runtime-control-validation.json']),
 ('P1','INTEG-12','Rapid Attack e Spirits precisam de procs reais',
  'Rapid é uma animação curta; Spirits usam aS/aV/aT gravados. Basic logical e SkillExecution têm contagens distintas.',
  'Separar activation/active/per-event/end e usar os eventos qualificados do gameplay, mantendo snapshot e Pending.',
  ['Source/ArtReview20261003/scout-rapid-attack.json','VFX-catalog.json']),
 ('P1','INTEG-13','Documentos de inventário antigos estão desatualizados',
  'separation-inventory.json declara 63 jobs; o catálogo ativo tem 123. FORMID inventory ainda descreve ausência de assets UE e muitos MISSING anteriores à conversão.',
  'Manter história e produzir manifest autoritativo atual com FormId validado + evento + asset + hash; não contar MISSING histórico como lacuna atual.',
  ['Evidence/separation-inventory.json','../../docs/formid-vfx-inventory.json']),
 ('P2','INTEG-14','Custo atual não é o custo dos protótipos',
  'O audit antigo lê Source/ReferencePorts, não as revisões atuais. Um emitter/material/layer não equivale automaticamente a uma draw call partilhada entre jogadores.',
  'Inventariar fontes ativas e medir instâncias/emissores/triângulos/translucência. Separar Essential/Gameplay/Decorative Effect Types e perfis de qualidade.',
  ['Scripts/audit_authoring_budgets.py','Evidence/authoring-budget-review.json']),
 ('P2','INTEG-15','Há conflitos entre especificações históricas e a direção aprovada',
  'Tech spec antiga põe stances nos pés e proíbe refração; regras VFX posteriores põem stances na cintura e o gelo aprovado tem tratamento vítreo. Fire trail aprovado usa 64 segmentos vs teto histórico de 16.',
  'Registar exceções de aparência e promover política reconciliada: preservar aprovações do utilizador; testar LOD/custos sem trocar silenciosamente o gelo/fogo.',
  ['../../docs/ue-vfx-tech-spec.html','Scripts/prepare_art_review_20261003.py','Evidence/fire-trail-contour-revision.json']),
]

WEAPONS = [
 ('Sword','melee','Traço de lâmina curto seguindo edge/tip; corte claro no contacto.'),
 ('Axe','melee','Arco curto mais pesado e fragmento de contacto; sem explosão por defeito.'),
 ('Club','melee','Movimento da cabeça; impacto compacto/poeira material, sem slash luminoso obrigatório.'),
 ('Wand','ranged','Ponto de emissão na ponta; núcleo pequeno e cauda curta.'),
 ('Rapier','melee','Estocada fina seguindo a ponta; a linha não altera o cleave comum.'),
 ('Dual Daggers','melee','Traços curtos alternados nas duas lâminas; um Basic lógico não se duplica por swings.'),
 ('Fists/Gauntlets','melee','Traço compacto no punho ativo e contacto seco; sem aura de ambos os braços permanente.'),
 ('Great Club','melee','Cabeça pesada e impacto compacto mais encorpado; sem AoE/shockwave funcional extra.'),
 ('Staff','ranged','Emissão no foco do staff; projectile de núcleo mais ritual, perfil comum de homing.'),
 ('Crossbow','ranged','Bolt visual, flash de release mínimo; seguir projectile autoritativo sem hitscan/gravity extra.'),
 ('Greatsword','melee','Arco amplo da lâmina na animação; alcance e número de hits seguem perfil melee comum.'),
 ('Greataxe','melee','Arco pesado assimétrico; contacto material sem nova área de dano.'),
 ('Bow','ranged','Flecha visual e release discreto; trajetória homing comum, sem queda física inventada.'),
 ('Spear','melee','Estocada comprida legível; comprimento da malha não concede reach extra.'),
]

ALIASES = {
 'fire-bolt-ii':'Fire Ball', 'frost-lance-ii':'Permafrost', 'combust-ii':'Combust Combo',
 'glacial-spike-ii':'Glacial Spike Combo','static-bolt-ii':'Conductive Lightning',
 'thunderstrike-ii':'Thunderstrike Combo','mana-barrier-ii-overcharge':'Overcharge',
 'arcane-weaving-ii':'Arcane Master','elemental-weaver-ii':'Elemental Master',
 'crushing-blow-ii':'Crushing Combo','chains-ii':'Chain Pull',
 'piercing-strike-ii-tank':'Breaching Strike Tank','piercing-strike-ii-warrior':'Breaching Strike Warrior',
 'shoulder-rush-ii-tank':'Shield Rush','shoulder-rush-ii-warrior':'Blade Rush',
 'rally-ii-tank':'Inspiration','rally-ii-warrior':'Bloodlust',
 'battlecry-challenge-ii-warrior':'Battlerage','battlecry-challenge-ii-tank':'Chain Challenge',
 'exploit-weakness-ii':'Sentence','exploit-weakness-iii':'Executioner','backstab-ii':'Ambush',
 'vine-field-ii':'Entangle','smoke-bomb-ii':'Shroud Bomb',
 'volley-ii-bleed':'Narrowing Volley Bleed','volley-ii-poison':'Narrowing Volley Poison',
 'astral-aura-sun':'Sun Aura','astral-aura-moon':'Moon Aura',
}

def infer_parent(component):
    if component.get('parent_skill'):
        return component['parent_skill']
    slug=component['slug']
    if slug.startswith('Chains'):
        return 'chains-ii' if slug.startswith('ChainsII') else 'chains'
    if slug.startswith('Volley'):
        tier='ii' if slug.startswith('VolleyII') else 'i'
        return f"volley-{tier}-{'poison' if 'Poison' in slug else 'bleed'}"
    if slug.startswith('SeveringMark') or slug.startswith('CC'):
        return 'shared'
    return 'unassigned_requires_review'

def stats(path):
    data=read(path);layers=data['layers']
    triangles=0
    for layer in layers:
        geometry=layer.get('geometry',{})
        tri=len(geometry.get('index',[]))//3 if geometry.get('index') else len(geometry.get('position',[]))//9
        triangles+=tri*layer['count']
    return dict(source=str(path.relative_to(ROOT)).replace('\\','/'),sha256=digest(path),
        layer_groups=len(layers),recorded_rows=sum(l['count'] for l in layers),
        potential_recorded_mesh_triangles=triangles,runtime_parameters=data.get('runtime_parameters',{}),
        live_uniform_layers=sum(bool(l.get('runtime_uniforms')) for l in layers),
        notes='Contagens estáticas de demonstração; não são draw calls, partículas visíveis simultaneamente ou timings GPU.')

def main():
    catalogue=read(ROOT/'VFX-catalog.json')['items']
    catalogue=[x for x in catalogue if x.get('ue_asset')]
    components=read(ROOT/'VFX-separated-components.json')['items']
    quality=read(ROOT/'Evidence/quality-pass.json')
    native=read(ROOT/'Evidence/art-revision-native-validation.json')
    by_slug={s:f for f in FAMILIES for s in f['slugs']}
    assert len(by_slug)==sum(len(f['slugs']) for f in FAMILIES)==len(catalogue)==124
    assert set(by_slug)=={x['slug'] for x in catalogue}
    assert len(components)==123 and quality['total']==quality['game_pass_complete']==247
    rows=[]
    for item in catalogue:
        f=by_slug[item['slug']]
        source=ROOT/item.get('review_source',f"Source/ReferencePorts/{item['class']}-{item['slug']}.json")
        observed=stats(source)
        if item['slug'] in native['assets']:
            assert native['assets'][item['slug']]['editable_source_sha256']==observed['sha256']
        rows.append(dict(slug=item['slug'],title=item['title'],class_id=item['class'],
            current_canon_name=ALIASES.get(item['slug'],item['title']),
            current_asset=item['ue_asset'],recorded_canonical_effect=item.get('canonical_effect'),
            family=f['name'],priority=f['priority'],required_events=f['required_events'],
            proposed_adjustment=f['adjustment'],proposed_cuts=f['cuts'],acceptance_tests=f['acceptance_tests'],
            current_components=[c['slug'] for c in components if infer_parent(c)==item['slug']],
            observed_source=observed,production_readiness='gameplay_binding_and_composition_pending',
            form_id_status='Requires reconciliation against current canonical execution forms; display-name alias is not an identity migration',
            source_of_rules='Canon-Current/02-combate-controlo.md + 03-classes.md; full linked decisions resolve details'))
    component_rows=[dict(slug=c['slug'],title=c['title'],asset=c['ue_asset'],
        parent= infer_parent(c),parent_inferred=not bool(c.get('parent_skill')),
        role=c.get('component_role'),condition=c.get('condition'),cue=c.get('cue'),
        observed_source=stats(ROOT/c['component_source']),
        classification='review_fixture' if ('HoldLow' in c['slug'] or 'HoldHigh' in c['slug'] or 'LightningMemory' in c['slug']) else 'candidate_runtime_component',
        production_ready=False) for c in components]
    refs=[FOUNDATION/'Docs/Canon-Current'/name for name in ('02-combate-controlo.md','03-classes.md','04-equipamento.md','RULE_PRECEDENCE.md')]
    refs += [FOUNDATION/'Docs/Art/VISUAL_LEDGER.md',REPO/'docs/skills.json',REPO/'docs/ue-vfx-tech-spec.html',
             REPO/'docs/formid-vfx-inventory.json',ROOT/'VFX-catalog.json',ROOT/'VFX-separated-components.json',
             ROOT/'Evidence/art-revision-integration-contracts.json',ROOT/'Evidence/quality-pass.json']
    report=dict(schema='sancta-vfx-gameplay-assessment/v1',assessed_at_utc=datetime.now(timezone.utc).isoformat(),
        assessment_date_local='2026-10-04',scope='Semantic, integration, organization and missing combat presentations; design proposals, not new gameplay canon or shipped assets',
        foundation_modified=False,engine_modified=False,vfx_assets_modified=False,
        foundation_head_context='ff91574e9b0adeab9a0dceedea623b44beec217f',
        provenance=[dict(path=str(p),sha256=digest(p)) for p in refs],
        counts=dict(skill_catalogue_rows=len(rows),class_rows=dict(Counter(x['class_id'] for x in rows)),
          isolated_components=len(components),inspected_scenes=quality['total'],
          family_reviews=len(FAMILIES),current_revised_native_sources=native['validated_current_jobs'],
          weapon_families=len(WEAPONS),melee_families=sum(w[1]=='melee' for w in WEAPONS),
          ranged_families=sum(w[1]=='ranged' for w in WEAPONS),
          action_families=3,current_cc_types=6,canonical_cc_types=7,
          component_parent_unassigned=sum(c['parent']=='unassigned_requires_review' for c in component_rows)),
        findings=[dict(priority=p,id=i,title=t,observed=o,proposed_action=a,evidence=e) for p,i,t,o,a,e in FINDINGS],
        families=FAMILIES,skills=rows,components=component_rows,
        weapon_presentations=[dict(family=n,delivery=d,proposed_visual=v,
          physical='Contacto/massa/material; sem assinatura elemental de Fire/Ice/Lightning por defeito.',
          magical='Mesmo delivery da arma, com energia arcane discreta; não liga automaticamente a assinaturas Manifest.',
          gameplay='Melee Cleave comum ou ranged homing Projectile comum; Primary escolhe canal, stats/cadence; Off-Hand não cria ataque extra.',
          state='missing_weapon_basic_attack_presentation') for n,d,v in WEAPONS],
        combat_actions=[
          dict(action='Guard',state='missing',events=['Enter','Active','MitigatedContact','Release','StaminaDepleted','LockoutEnd'],
             proposal='Pose/escudo dominam; linha curta no escudo ativa e impacto direcional compacto só na mitigação confirmada. Depletion com quebra/escurecimento breve e HUD.',
             exclusions='Sem passive block, perfect block/parry, bubble de invulnerabilidade ou GuardBreak-Stun. Shield gear apropriado; Buckler não autorizado por inferência. Stamina/direção/mitigação são gameplay.'),
          dict(action='Dodge',state='missing',events=['Start','Travel','End','Cancelled'],
             proposal='Arranque curto, poeira por superfície e rasto corporal muito breve opcional; nenhuma cópia permanente do manequim. Resposta a evasão confirmada partilhada com Evasion.',
             exclusions='Dodge = deslocamento + Evasion temporária, não i-frames. Skills Warrior compatíveis não renovam janela/custo. AoE continua counter posicional.'),
          dict(action='Sprint',state='missing',events=['Enter','LocomotionFootContact','Exit','StaminaDepleted'],
             proposal='Transição legível pela animação, footprints/poeira por superfície e intensidade pequena por velocidade; sem raios ou trail de magia contínuo.',
             exclusions='Pode existir em combate; partículas não autorizam ação nem consomem Stamina. Não conta como Skill/Mana Storm admission/Star count.')],
        implementation_status='No new VFX or gameplay implementation performed in this assessment',
        measured_gpu_cost=None,production_approval=False)
    write(ROOT/'Evidence/gameplay-vfx-assessment-20261004.json',report)
    lines=['# Matriz de revisão das skills e componentes','',
      '4 de outubro de 2026. Propostas de integração e composição, com assets atuais preservados. Cada linha do catálogo ativo está coberta; variantes não equivalem a skills únicas. FormIds e aliases exigem reconciliação com o canon atual.','',
      'A análise usa fontes/capturas já validadas e contratos de gameplay. Não certifica uma nova execução integrada em combate.','',
      '| Prioridade | Família | Cenários | Ajustar ou acrescentar | Cortar ou impedir |',
      '| --- | --- | ---: | --- | --- |']
    for f in FAMILIES:
        lines.append(f"| {f['priority']} | {f['name']} | {len(f['slugs'])} | {f['adjustment']} | {f['cuts']} |")
    lines+=['','## Registo por cenário','',
      '| Cenário | Nome atual no canon ou alias de leitura | Família | Prioridade | Componentes associados |',
      '| --- | --- | --- | --- | --- |']
    for r in rows:
        lines.append(f"| {r['title']} ({r['slug']}) | {r['current_canon_name']} | {r['family']} | {r['priority']} | {', '.join(r['current_components']) or 'Sem componente independente associado no inventário atual; rever decomposição.'} |")
    lines+=['','Os detalhes por linha, eventos, testes, paths, hashes e contagens estáticas encontram-se em `Evidence/gameplay-vfx-assessment-20261004.json`.','']
    (ROOT/'MATRIZ_SKILLS_VFX_20261004.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps(report['counts'],ensure_ascii=False))

if __name__=='__main__':
    main()
