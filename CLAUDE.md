# SanctaMMO VFX — contexto para agentes

- Idioma: português europeu em toda a documentação, UI dos protótipos e mensagens ao utilizador.
- Motor alvo: Unreal Engine 5 com GAS e Niagara. Os protótipos HTML servem só para validar aspeto e arquitetura; não são o produto.
- Fonte de verdade da direção visual: `docs/VFX_Skills_SanctaMMO.docx` (dados em `docs/skills.json`, ícones em `docs/icons/`).
- Git: trabalhar sempre em `main` e fazer push logo a seguir ao commit. Sem branches paralelos — uma única versão dos ficheiros, local e no GitHub.
- Regras de implementação e orçamentos: `docs/ue-vfx-tech-spec.html`. Qualquer VFX novo tem de caber no orçamento do seu tipo de skill.

## Direção visual
- Dark fantasy realista: cenário frio e dessaturado, VFX quente e saturado. Preferir simples a carregado — uma forma dominante, poucas camadas.
- Paleta vem do ícone da skill; dourado não domina (reservado à UI).
- Cues condicionais (procs, "havia debuffs") só aparecem quando a condição é verdadeira.
- Estilo aprovado (referência: `prototypes/fighter/warrior-tank-stance/`): traços finos caligráficos com pontas afiladas, núcleo quente quase branco + halo suave na cor da skill, energia a correr devagar, emblemas desenhados em linha com preenchimento ténue, luz suave no chão. Evitar formas chapadas, blocos facetados e arestas duras.

## Protótipos (`prototypes/<classe>/<skill>/`)
- Um ficheiro HTML autónomo por skill; Three.js r128 do cdnjs + postprocessing de `cdn.jsdelivr.net/npm/three@0.128.0/examples/js/`.
- Arquitetura obrigatória: cada camada é UM sistema instanciado partilhado por todos os casts; o CPU só escreve dados de spawn; a GPU calcula tudo a partir da idade (`uTime - aT`). Incluir níveis de qualidade, stress test e contadores (draw calls, partículas, CPU).
- Lições do Severing Strike (aplicar por defeito):
  - Menos brilho: a forma principal vale por si. Sem halos largos, preenchimentos ou fios decorativos à volta; bloom contido. Brilho forte só no núcleo estreito.
  - Perfil das formas: fino nas pontas, grosso no meio (tipo `sin(πs)`), com o centro reforçado. Fades das pontas em curva (`pow(sin, <1)`), nunca lineares.
  - Todo o brilho de um quad tem de chegar a zero antes da borda do quad (fade radial pela meia-largura); senão o `discard` recorta a luz e vê-se um quadrado.
  - Máscaras sempre suaves: nada de `discard` ou cortes duros nos limites (criam linhas retas no chão).
  - Leitura do movimento: cresce no sentido da ação → segura no tamanho máximo → apaga a partir da origem; a parte mais importante (o centro) desaparece por último. Não encurtar demasiado: a forma principal fica ~0,5–0,7 s.
  - A animação do corpo (torção, preparação) tem de ir no mesmo sentido do VFX.
  - Quads construídos à mão no vertex shader: usar `side: DoubleSide` (a orientação dos triângulos pode ficar invertida e o quad desaparece).
  - Rastos/efeitos presos ao corpo seguem a silhueta da personagem (mais alta que larga) e fundem-se nela com fade suave — nunca terminam num corte ou numa ponta cónica junto ao corpo (lê-se como escape de míssil).
  - Faixas presas ao corpo ficam verticais (orientação dominada pelo eixo Y, só ligeiramente viradas para a câmara): altas de lado, estreitas vistas de cima. Nunca billboard total, que de cima fica deitado e largo.
  - Fumo/névoa: vários fiapos finos independentes, cada um a ondular e a interromper-se com ruído — uma faixa única (gaussiana ou achatada) lê-se sempre como barra/linha ao meio.
  - Efeitos que envolvem o corpo (cilindros/conchas): raio irregular com ruído, 2 camadas a profundidades diferentes (mesma draw call via atributo) e fade onde a superfície fica de perfil (|n·v| baixo) — senão lê-se o cilindro.
  - Enquadrar a câmara do protótipo para a leitura da skill (linhas e investidas lêem-se de lado/3/4, não de trás).
- Skill ≠ status: o VFX da skill cobre só o cast/impacto. Estados resultantes (Shield, heal-over-time, buffs, debuffs, CC persistente) são cues de status próprios (`GameplayCue.Status.*`, Looping), partilhados por todas as fontes — não os animar no protótipo da skill. Isto inclui marcadores de aplicação nos alvos (Silence, Taunt, Slow, etc.): a skill mostra o próprio golpe/pulso e o impacto; o que indica o estado no alvo é do cue de status. Exceção: contadores de sequência/carga da própria skill mantêm-se no alvo, breves. Marca de sequência Severing: 1 = uma linha, 2 = duas linhas cruzadas, 3 = círculo à volta das linhas cruzadas. Arco Severing cresce por nível: I raio 1,25 m / ~140°, II 1,6 m / ~170°, III 2,05 m / ~190°.
- Efeitos de chão (convergências, pulsos, anéis) ficam deitados no plano do chão, não em billboards virados para o ecrã; billboards só para emblemas pequenos no corpo.
- Pools instanciados: inicializar TODOS os componentes de `aT` com -1e5 (slots por usar têm de estar "mortos"), senão aparecem instâncias fantasma no arranque.
- Evitar: PMREM/env maps (satura os metais neste setup), sprites individuais por partícula, luz dinâmica fora de Epic.
- Iterações antigas vão para `archive/`.
- Teste no painel do browser: se o painel estiver escondido o `requestAnimationFrame` não corre (o tempo da simulação para); cada screenshot força frames, por isso usar screenshots para avançar a animação.
- Hook de teste nos protótipos: `window.__freezeAt = <segundos>` congela a animação nesse instante do cast local (útil para capturar um momento exato).
- Testar com `python -m http.server 8766` na raiz (`.claude/launch.json` já tem a configuração `sancta-vfx`).
