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
| Fighter · Rage / Bulwark | Otimizado (convergência em espiral no chão, pulso de cura ou de escudo, 2 draw calls) | [prototypes/fighter/rage-bulwark/rage-bulwark-vfx.html](prototypes/fighter/rage-bulwark/rage-bulwark-vfx.html) |
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
| Fighter · Battlecry / Challenge I | Otimizado (pulso radial no chão: cristas ou anel ancorado, 1 draw call, 0 partículas) | [prototypes/fighter/battlecry-challenge/battlecry-challenge-vfx.html](prototypes/fighter/battlecry-challenge/battlecry-challenge-vfx.html) |
| Fighter · Pressure / Provoke | Otimizado (fio de fumo rápido arma→alvo, golfadas ou onda contínua, 2 draw calls, 0 partículas) | [prototypes/fighter/pressure-provoke/pressure-provoke-vfx.html](prototypes/fighter/pressure-provoke/pressure-provoke-vfx.html) |
| Fighter · Second Wind | Otimizado (brisa de 10 fiapos em hélice à volta do corpo, 2 camadas irregulares, 1 draw call, 0 partículas) | [prototypes/fighter/second-wind/second-wind-vfx.html](prototypes/fighter/second-wind/second-wind-vfx.html) |
| Fighter · Severing Strike II | Otimizado (arco do I; marca de sequência linha → linhas cruzadas no 2.º acerto, 3 draw calls) | [prototypes/fighter/severing-strike-ii/severing-strike-ii-vfx.html](prototypes/fighter/severing-strike-ii/severing-strike-ii-vfx.html) |
| Fighter · Severing Strike III | Otimizado (arco maior; marca linha → cruz → cruz + círculo no 3.º acerto, 3 draw calls) | [prototypes/fighter/severing-strike-iii/severing-strike-iii-vfx.html](prototypes/fighter/severing-strike-iii/severing-strike-iii-vfx.html) |

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
