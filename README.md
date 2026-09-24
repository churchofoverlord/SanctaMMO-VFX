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
| Fighter · Warrior / Tank Stance | Otimizado (marcador num só quad, pulso de 2 frames, stress test) | [prototypes/fighter/warrior-tank-stance/warrior-tank-stance-vfx.html](prototypes/fighter/warrior-tank-stance/warrior-tank-stance-vfx.html) |
| Fighter · Rage / Bulwark | Otimizado (convergência em espiral no chão, pulso de cura ou de escudo, 2 draw calls) | [prototypes/fighter/rage-bulwark/rage-bulwark-vfx.html](prototypes/fighter/rage-bulwark/rage-bulwark-vfx.html) |
| Fighter · Severing Strike I | Otimizado (arco em snap num quad, impacto + marca de sequência, faíscas GPU, 3 draw calls) | [prototypes/fighter/severing-strike/severing-strike-vfx.html](prototypes/fighter/severing-strike/severing-strike-vfx.html) |
| Fighter · Piercing Strike I | Otimizado (linha perfurante num quad, impacto + cue breve de Slow, faíscas GPU, 3 draw calls) | [prototypes/fighter/piercing-strike/piercing-strike-vfx.html](prototypes/fighter/piercing-strike/piercing-strike-vfx.html) |
| Fighter · Shoulder Rush I | Otimizado (rasto à altura do tronco atrás do Fighter, impacto leve, hit stop, 3 draw calls) | [prototypes/fighter/shoulder-rush/shoulder-rush-vfx.html](prototypes/fighter/shoulder-rush/shoulder-rush-vfx.html) |
| Fighter · Crushing Blow I | Otimizado (telegraph + rachas + onda num quad, traço vertical, fragmentos GPU, 3 draw calls) | [prototypes/fighter/crushing-blow/crushing-blow-vfx.html](prototypes/fighter/crushing-blow/crushing-blow-vfx.html) |

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
