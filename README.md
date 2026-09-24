# SanctaMMO · VFX

VFX das skills do SanctaMMO (Unreal Engine 5, GAS + Niagara): direção visual, regras de performance e protótipos interativos no browser.

## Estrutura

```
docs/
  VFX_Skills_SanctaMMO.docx   Guia original de VFX das skills (fonte de verdade da direção visual)
  skills.json                 As 98 fichas do guia em dados estruturados (classe, paleta, efeito, visual, implementação, ícones)
  icons/<classe>/<skill>.jpg  Ícones do guia, com o nome da skill
  ue-vfx-tech-spec.html       Ficha técnica UE5: GameplayCues, Niagara, materiais, orçamentos por tipo de skill
prototypes/
  <classe>/<skill>/<skill>-vfx.html   Protótipo interativo (Three.js, abre direto no browser)
  <classe>/<skill>/archive/           Iterações anteriores
```

## Protótipos

| Skill | Estado | Ficheiro |
|---|---|---|
| Fighter · Cleanse | Otimizado (GPU, instanciado, níveis de qualidade, stress test) | [prototypes/fighter/cleanse/cleanse-vfx.html](prototypes/fighter/cleanse/cleanse-vfx.html) |
| Fighter · Warrior Stance | Otimizado (marcador magenta num só quad, emblema de lâmina, pulso de entrada de 2 frames, stress test) | [prototypes/fighter/warrior-stance/warrior-stance-vfx.html](prototypes/fighter/warrior-stance/warrior-stance-vfx.html) |
| Fighter · Tank Stance | Otimizado (marcador ciano num só quad, emblema de escudo, pulso de entrada de 2 frames, stress test) | [prototypes/fighter/tank-stance/tank-stance-vfx.html](prototypes/fighter/tank-stance/tank-stance-vfx.html) |
| Fighter · Rage | Otimizado (convergência + pulsos de cura em magenta-avermelhado, emblema cruz) | [prototypes/fighter/rage/rage-vfx.html](prototypes/fighter/rage/rage-vfx.html) |
| Fighter · Bulwark | Otimizado (convergência + pulso em ciano, emblema escudo; o Shield é cue de status) | [prototypes/fighter/bulwark/bulwark-vfx.html](prototypes/fighter/bulwark/bulwark-vfx.html) |
| Fighter · Severing Strike I | Otimizado (arco em snap num quad, impacto + marca de sequência, faíscas GPU, 3 draw calls) | [prototypes/fighter/severing-strike/severing-strike-vfx.html](prototypes/fighter/severing-strike/severing-strike-vfx.html) |
| Fighter · Piercing Strike I | Otimizado (linha perfurante num quad, impacto, faíscas GPU, 3 draw calls) | [prototypes/fighter/piercing-strike/piercing-strike-vfx.html](prototypes/fighter/piercing-strike/piercing-strike-vfx.html) |
| Fighter · Shoulder Rush I | Otimizado (rasto à altura do tronco atrás do Fighter, impacto leve, hit stop, 3 draw calls) | [prototypes/fighter/shoulder-rush/shoulder-rush-vfx.html](prototypes/fighter/shoulder-rush/shoulder-rush-vfx.html) |
| Fighter · Shoulder Rush II · Warrior | Otimizado (rasto e impacto nas cores da Warrior Stance, anel magenta no chão à chegada, hit stop 2 frames, 3 draw calls) | [prototypes/fighter/shoulder-rush-ii-warrior/shoulder-rush-ii-warrior-vfx.html](prototypes/fighter/shoulder-rush-ii-warrior/shoulder-rush-ii-warrior-vfx.html) |
| Fighter · Shoulder Rush II · Tank | Otimizado (rasto e impacto nas cores da Tank Stance, anel ciano duplo e firme no chão, hit stop 2 frames, 3 draw calls) | [prototypes/fighter/shoulder-rush-ii-tank/shoulder-rush-ii-tank-vfx.html](prototypes/fighter/shoulder-rush-ii-tank/shoulder-rush-ii-tank-vfx.html) |
| Fighter · Crushing Blow I | Otimizado (telegraph + rachas + onda num quad, traço vertical, fragmentos GPU, 3 draw calls) | [prototypes/fighter/crushing-blow/crushing-blow-vfx.html](prototypes/fighter/crushing-blow/crushing-blow-vfx.html) |
| Fighter · Crushing Blow II | Otimizado (impacto muito mais forte: 14 rachas grossas com ramificações, 3× as pedras, tremor de câmara; anel de Slow no mesmo quad; trava de Stun no chão só se o alvo já tinha Slow, 3–4 draw calls) | [prototypes/fighter/crushing-blow-ii/crushing-blow-ii-vfx.html](prototypes/fighter/crushing-blow-ii/crushing-blow-ii-vfx.html) |
| Fighter · Chains I | Otimizado (duas correntes de energia, uma por mão: elos de luz instanciados + aura, arranque lento, hit stop, ancoragem no chão, dissolve da mão, 4 draw calls) | [prototypes/fighter/chains/chains-vfx.html](prototypes/fighter/chains/chains-vfx.html) |
| Fighter · War Leap | Otimizado (decalque estático no channel, rasto em arco que segue o Fighter, squash + resolução radial única na aterragem, 4 draw calls) | [prototypes/fighter/war-leap/war-leap-vfx.html](prototypes/fighter/war-leap/war-leap-vfx.html) |
| Fighter · Rally I · Warrior | Otimizado (consome Momentum; anel de grupo magenta linear a partir do Fighter, pulsos só nos aliados em alcance, 2 draw calls) | [prototypes/fighter/rally-i-warrior/rally-i-warrior-vfx.html](prototypes/fighter/rally-i-warrior/rally-i-warrior-vfx.html) |
| Fighter · Rally I · Tank | Otimizado (consome Momentum; anel de grupo ciano linear a partir do Fighter, pulsos só nos aliados em alcance, 2 draw calls) | [prototypes/fighter/rally-i-tank/rally-i-tank-vfx.html](prototypes/fighter/rally-i-tank/rally-i-tank-vfx.html) |
| Fighter · Chains II / Chain Pull | Otimizado (no hit cada corrente enrola 1 volta à volta do alvo e só solta quando ele chega; recast no mesmo slot; o CPU escreve só o instante do Pull nos elos vivos: pulso de Interrupt + contração ease-in na GPU, 4–5 draw calls) | [prototypes/fighter/chains-ii/chains-ii-vfx.html](prototypes/fighter/chains-ii/chains-ii-vfx.html) |
| Fighter · Piercing Strike II · Warrior | Otimizado (estocada do I em magenta; flash direcional magenta só em alvos que já tinham Slow, 3–4 draw calls) | [prototypes/fighter/piercing-strike-ii-warrior/piercing-strike-ii-warrior-vfx.html](prototypes/fighter/piercing-strike-ii-warrior/piercing-strike-ii-warrior-vfx.html) |
| Fighter · Piercing Strike II · Tank | Otimizado (estocada do I em ciano; marcador Weakened estático em ciano no chão só em alvos que já tinham Slow, 3–4 draw calls) | [prototypes/fighter/piercing-strike-ii-tank/piercing-strike-ii-tank-vfx.html](prototypes/fighter/piercing-strike-ii-tank/piercing-strike-ii-tank-vfx.html) |
| Fighter · Defiant Presence | Otimizado (cúpula baixa de plasma ténue com o raio da distância-limite, veios de ruído; não reage a golpes; 1 draw call) | [prototypes/fighter/defiant-presence/defiant-presence-vfx.html](prototypes/fighter/defiant-presence/defiant-presence-vfx.html) |
| Fighter · Battlecry II · Warrior | Otimizado (pulso do I em magenta; contra-onda de Fear em reverse ease-in só em inimigos já Silenced, 1–2 draw calls) | [prototypes/fighter/battlecry-challenge-ii-warrior/battlecry-challenge-ii-warrior-vfx.html](prototypes/fighter/battlecry-challenge-ii-warrior/battlecry-challenge-ii-warrior-vfx.html) |
| Fighter · Challenge II · Tank | Otimizado (anel do I em ciano; raízes a partir dos pés só no expiry natural do Taunt, 1–2 draw calls) | [prototypes/fighter/battlecry-challenge-ii-tank/battlecry-challenge-ii-tank-vfx.html](prototypes/fighter/battlecry-challenge-ii-tank/battlecry-challenge-ii-tank-vfx.html) |
| Fighter · Momentum Mastery | Otimizado (só no consumo: 1 crescente verde de Stamina por Momentum, igual em Rage e Bulwark, 1 draw call, 0 fora do proc) | [prototypes/fighter/momentum-mastery/momentum-mastery-vfx.html](prototypes/fighter/momentum-mastery/momentum-mastery-vfx.html) |
| Fighter · Rally II · Warrior | Otimizado (anel do I + 2.º anel magenta com chevrons, no mesmo quad, 2 draw calls) | [prototypes/fighter/rally-ii-warrior/rally-ii-warrior-vfx.html](prototypes/fighter/rally-ii-warrior/rally-ii-warrior-vfx.html) |
| Fighter · Rally II · Tank | Otimizado (anel do I + 2.º anel ciano com losangos, no mesmo quad, 2 draw calls) | [prototypes/fighter/rally-ii-tank/rally-ii-tank-vfx.html](prototypes/fighter/rally-ii-tank/rally-ii-tank-vfx.html) |
| Fighter · Battlecry I · Warrior | Otimizado (pulso radial agressivo em magenta, 3 cristas, 1 draw call) | [prototypes/fighter/battlecry-challenge-i-warrior/battlecry-challenge-i-warrior-vfx.html](prototypes/fighter/battlecry-challenge-i-warrior/battlecry-challenge-i-warrior-vfx.html) |
| Fighter · Challenge I · Tank | Otimizado (pulso radial em ciano, anel ancorado na borda, 1 draw call) | [prototypes/fighter/battlecry-challenge-i-tank/battlecry-challenge-i-tank-vfx.html](prototypes/fighter/battlecry-challenge-i-tank/battlecry-challenge-i-tank-vfx.html) |
| Fighter · Pressure / Provoke | Otimizado (fio de fumo rápido arma→alvo, golfadas ou onda contínua, 2 draw calls, 0 partículas) | [prototypes/fighter/pressure-provoke/pressure-provoke-vfx.html](prototypes/fighter/pressure-provoke/pressure-provoke-vfx.html) |
| Fighter · Second Wind | Otimizado (brisa de 10 fiapos em hélice à volta do corpo, 2 camadas irregulares, 1 draw call, 0 partículas) | [prototypes/fighter/second-wind/second-wind-vfx.html](prototypes/fighter/second-wind/second-wind-vfx.html) |
| Fighter · Severing Strike II | Otimizado (arco do I; marca de sequência linha → linhas cruzadas no 2.º acerto, 3 draw calls) | [prototypes/fighter/severing-strike-ii/severing-strike-ii-vfx.html](prototypes/fighter/severing-strike-ii/severing-strike-ii-vfx.html) |
| Fighter · Severing Strike III | Otimizado (arco maior; marca linha → cruz → cruz + círculo no 3.º acerto, 3 draw calls) | [prototypes/fighter/severing-strike-iii/severing-strike-iii-vfx.html](prototypes/fighter/severing-strike-iii/severing-strike-iii-vfx.html) |
| Scout · Backstab I | Otimizado (adaga atirada com rasto fino, melee ou range; flash pequeno só no acerto pelas costas = Interrupt, 2–4 draw calls) | [prototypes/scout/backstab/backstab-vfx.html](prototypes/scout/backstab/backstab-vfx.html) |
| Scout · Torpor | Otimizado (seta sólida rápida + anel de lentidão estático nos pés, 2–4 draw calls) | [prototypes/scout/torpor/torpor-vfx.html](prototypes/scout/torpor/torpor-vfx.html) |
| Mystic · Ether I · Ally | Otimizado (estrela astral + cometa curto; anel abre e luz sobe em ease-out, dourado, 2–3 draw calls) | [prototypes/mystic/ether-i-ally/ether-i-ally-vfx.html](prototypes/mystic/ether-i-ally/ether-i-ally-vfx.html) |
| Mystic · Ether I · Enemy | Otimizado (estrela astral + cometa curto; anel fecha e colapsa em ease-in com pop, violeta, 2–3 draw calls) | [prototypes/mystic/ether-i-enemy/ether-i-enemy-vfx.html](prototypes/mystic/ether-i-enemy/ether-i-enemy-vfx.html) |
| Mystic · Lullaby I | Otimizado (orbe lento a ondular com crescente; absorção sem hit stop; anel de Sleep após 1 s de delay, 1–3 draw calls) | [prototypes/mystic/lullaby/lullaby-vfx.html](prototypes/mystic/lullaby/lullaby-vfx.html) |
| Mage · Combust I | Otimizado (orbe de fogo direto, rasto curto; impacto compacto + marca de chama; igual em Manifest e Weave, 2–3 draw calls) | [prototypes/mage/combust-i/combust-i-vfx.html](prototypes/mage/combust-i/combust-i-vfx.html) |
| Mage · Blink | Otimizado (linha roxa horizontal sobe pés→cabeça na origem, vira beam cabeça→cabeça e desce cabeça→pés no destino; anel em cada ponto, 3 draw calls) | [prototypes/mage/blink/blink-vfx.html](prototypes/mage/blink/blink-vfx.html) |

Abrir localmente (as bibliotecas vêm de CDN, por isso é preciso internet):

```bash
python -m http.server 8766
```

e ir a `http://localhost:8766/prototypes/fighter/cleanse/cleanse-vfx.html`.

## Regras base

1. **Servidor:** o VFX não existe no servidor. Tudo é disparado por GameplayCues de habilidades/efeitos já replicados; estados condicionais viajam nos parâmetros do cue.
2. **Cliente:** cada skill cabe no orçamento do seu tipo (ver `docs/ue-vfx-tech-spec.html`, secção 04). Sem trabalho por partícula no CPU, sem luz dinâmica por defeito, sem refração.
3. **Escalabilidade:** o próprio jogador vê a versão completa; os outros degradam por distância e quantidade até ficar só a silhueta.
4. **Visual:** dark fantasy realista mas simples — uma forma dominante por skill, paleta do ícone, brilho só no instante do impacto.
| Scout · Cleanse | Mesmo VFX do Cleanse do Fighter (laranja e dourado) | [prototypes/scout/cleanse/cleanse-vfx.html](prototypes/scout/cleanse/cleanse-vfx.html) |
| Mage · Cleanse | Mesmo VFX do Cleanse do Fighter, paleta violeta e azul | [prototypes/mage/cleanse/cleanse-vfx.html](prototypes/mage/cleanse/cleanse-vfx.html) |
| Mage · Manifest | Só um círculo à cintura: trança 3D de três fios de plasma suave (vermelho, azul, amarelo), juntos e torcidos à volta do círculo, que ondula devagar em altura; nada no chão nem em órbita (1 draw call) | [prototypes/mage/manifest/manifest-vfx.html](prototypes/mage/manifest/manifest-vfx.html) |
| Mage · Weave | Sem selo: linha de órbita fina à cintura com 0, 1 ou 2 Arcane Shards a correr sobre ela (GPU, 1 draw call); anel no chão + órbita abre do centro na entrada | [prototypes/mage/weave/weave-vfx.html](prototypes/mage/weave/weave-vfx.html) |
| Mage · Arcane Burst | 0–2 shards convergem da órbita para a mão (0,4 s); uma esfera violeta opaca que cresce com os shards, a 14 m/s com drift ligeiro (curva suave, diferente em cada cast); hit stop de 0,06 s, pop no peito e anel da AoE no chão (1,2–2,2 m), sem detritos | [prototypes/mage/arcane-burst/arcane-burst-vfx.html](prototypes/mage/arcane-burst/arcane-burst-vfx.html) |
| Mage · Vortex (Fire + Fire) | Bola de fogo central (roda com os braços) + 6 braços curvos grossos na base, com glow, cada um uma fita contínua de chama suave tipo nuvem (transições de cor esbatidas, base na cor da esfera; blending premultiplicado), rotação rápida + chamas GPU soltas; viaja deitado, lento a 5 m/s, alcance 18 m (demo a 14 m); sem explosão de fogo no hit: empurrão lateral de 1,4 m com risco de fogo no chão e marca de Burn no alvo deslocado | [prototypes/mage/vortex/vortex-vfx.html](prototypes/mage/vortex/vortex-vfx.html) |
| Mage · Iceberg (Ice + Ice) | Cristal de gelo direto até ao ponto à frente do alvo; muro de 7–13 prismas de gelo sólidos e facetados (1 draw call, shader opaco com fresnel ciano) sobe em 0,25 s do centro para as pontas, segura 3 s e afunda; linha de geada no chão marca a colisão; um anel de AoE Slow (3 m) abre uma vez; vida do muro inteiro (fissuras a 66 % e 33 %, estilhaçar a 0) e especificação do asset BP_Iceberg (colisão, nav, material) na página | [prototypes/mage/iceberg/iceberg-vfx.html](prototypes/mage/iceberg/iceberg-vfx.html) |
| Mage · Coil (Lightning + Lightning) | Quatro anéis de raio à volta do Mage (zigue-zague que volta a disparar ~20×/s, desenham-se em 0,12 s e crepitam ~3 s; sem casca de Shield, que é cue de status partilhado), anel da AoE (4 m), raios amarelos curtos e finos a sair dos anéis durante os ~3 s (0,7–1,5 m, nova direção a cada 0,32 s, ~0,1 s visíveis), descarga fractal ramificada até cada alvo com flash e faíscas; cue de Root nos pés só se o alvo já estava Sapped (seletor) | [prototypes/mage/coil/coil-vfx.html](prototypes/mage/coil/coil-vfx.html) |
| Mage · Mist (Fire + Ice) | Área estacionária (R 7 m, ~6 s): névoa de fiapos GPU até ~2,8 m de altura (premultiplicado, esconde), tingida de laranja de um lado e azul-ciano do outro; anel fino no chão meio laranja meio azul como limite; sem volutas; sem chamas nem estilhaços (não faz dano) | [prototypes/mage/mist/mist-vfx.html](prototypes/mage/mist/mist-vfx.html) |
| Mage · Laser (Fire + Lightning) | Feixe contínuo de fogo (receita Vortex) da mão até 14 m, largura estável, steerable (varre com a mira, não se prende a alvos); 3 raios dourados (receita Coil) enrolados ao longo; a cada tick (0,5 s) pulso no feixe + impacto e faíscas onde acerta | [prototypes/mage/laser/laser-vfx.html](prototypes/mage/laser/laser-vfx.html) |
| Mystic · Cleanse | Mesmo VFX do Cleanse do Fighter, paleta azul e ciano | [prototypes/mystic/cleanse/cleanse-vfx.html](prototypes/mystic/cleanse/cleanse-vfx.html) |
| Scout · Poison Stance | Glow verde nas duas mãos (persistente), pico + anel no punho na entrada, sem marcador no chão | [prototypes/scout/poison-stance/poison-stance-vfx.html](prototypes/scout/poison-stance/poison-stance-vfx.html) |
| Scout · Bleed Stance | Glow vermelho nas duas mãos (persistente), pico + anel no punho na entrada, sem marcador no chão | [prototypes/scout/bleed-stance/bleed-stance-vfx.html](prototypes/scout/bleed-stance/bleed-stance-vfx.html) |
| Scout · Poison Sac | Saco lançado em arco (8 m), 5 stacks convergem ao chão, splash + poça tóxica escura (R 1,6 m) com anel | [prototypes/scout/poison-sac/poison-sac-vfx.html](prototypes/scout/poison-sac/poison-sac-vfx.html) |
| Scout · Hemorrhage | 5 stacks de Bleed convergem ao peito e rebentam num splash de sangue viscoso, 0,7 s (single target) | [prototypes/scout/hemorrhage/hemorrhage-vfx.html](prototypes/scout/hemorrhage/hemorrhage-vfx.html) |
| Scout · Basic Attack — Poison | Só o cue de hit, independente da arma: splash verde pequeno no ponto de contacto, 0,2 s (demo com arco e adaga) | [prototypes/scout/basic-attack-poison/basic-attack-poison-vfx.html](prototypes/scout/basic-attack-poison/basic-attack-poison-vfx.html) |
| Scout · Basic Attack — Bleed | Só o cue de hit, independente da arma: corte curto vermelho + gotas, 0,2 s (demo com arco e adaga) | [prototypes/scout/basic-attack-bleed/basic-attack-bleed-vfx.html](prototypes/scout/basic-attack-bleed/basic-attack-bleed-vfx.html) |
