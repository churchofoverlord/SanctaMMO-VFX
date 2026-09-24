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

## Protótipos (`prototypes/<classe>/<skill>/`)
- Um ficheiro HTML autónomo por skill; Three.js r128 do cdnjs + postprocessing de `cdn.jsdelivr.net/npm/three@0.128.0/examples/js/`.
- Arquitetura obrigatória: cada camada é UM sistema instanciado partilhado por todos os casts; o CPU só escreve dados de spawn; a GPU calcula tudo a partir da idade (`uTime - aT`). Incluir níveis de qualidade, stress test e contadores (draw calls, partículas, CPU).
- Evitar: PMREM/env maps (satura os metais neste setup), sprites individuais por partícula, luz dinâmica fora de Epic.
- Iterações antigas vão para `archive/`.
- Testar com `python -m http.server 8765` na raiz (`.claude/launch.json` já tem a configuração `vfx`).
