"""Generate navigation from current definitions, never from historical asset filenames."""
import collections, datetime, hashlib, html, json, pathlib

R = pathlib.Path(__file__).resolve().parents[1]
read = lambda p: json.loads((R / p).read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256((R / p).read_bytes()).hexdigest()
esc = lambda value: html.escape(str(value), quote=True)
jobs = read('Evidence/gameplay-runtime-build-jobs.json')['jobs']
definitions = {d['presentation_id']: d for d in read('Evidence/gameplay-runtime-definitions.json')['definitions']}
routes = read('Evidence/gameplay-runtime-form-routes.json')['routes']
native = read('Evidence/gameplay-runtime-native-assets.json')['assets']
viewer = read('Evidence/runtime-viewer-cases.json')
scenes = {c['name']: {**c, 'number': i + 1} for i, c in enumerate(viewer)}
captures = {r['slug']: r for r in read('Evidence/gameplay-runtime-capture-audit.json')['rows']}
canonical = collections.defaultdict(list)
for route in routes:
    for phase in definitions[route['form_id']]['phase_details']:
        canonical[phase['component_key']].append({'form_id': route['form_id'], 'phase': phase['phase']})

groups = ['Básicos e ações', 'Fighter', 'Mage', 'Mystic', 'Scout', 'Estados e CC']
gates = {'Admission': 'Execução admitida', 'ConfirmedHit': 'Contacto confirmado',
         'Applied': 'Resultado aplicado', 'NaturalEnd': 'Fim natural confirmado',
         'Cleanse': 'Remoção por cleanse', 'Cosmetic': 'Contacto cosmético real'}
anchors = {'Source': 'Caster / origem', 'Target': 'Alvo', 'World': 'Ponto / área no mundo',
           'Projectile': 'Projétil real', 'Link': 'Ligação entre duas pontas'}
rows = []
for job in jobs:
    slug = job['slug']
    if job['form'].startswith('Combat.') or any(c['form_id'].startswith('universal.basic-attack.') for c in canonical[slug]):
        group = groups[0]
    elif job['form'].startswith('Status.') or slug.startswith('CC'):
        group = groups[-1]
    else:
        classes = {c['form_id'].split('.')[0].title() for c in canonical[slug]}
        if len(classes) != 1 or not classes.issubset(set(groups)):
            raise RuntimeError('Unresolved class: ' + slug)
        group = classes.pop()
    best = max(captures[slug]['samples'], key=lambda s: s['changed_pixels_over_12'])
    if sha(best['gallery_preview']) != best['gallery_preview_sha256']:
        raise RuntimeError('Gallery preview changed: ' + slug)
    definition = definitions[job['form']]
    matches = [p for p in definition['phase_details'] if p['component_key'] == slug]
    if len(matches) != 1 or matches[0]['phase'] != job['phase']:
        raise RuntimeError('Incorrect isolated phase: ' + slug)
    rows.append({'component': slug, 'title': scenes[slug]['title'], 'group': group,
                 'scene': scenes[slug]['number'], 'presentation_id': job['form'],
                 'phase': job['phase'], 'gate': job['gate'], 'anchor': job['anchor'],
                 'persistent': job['persistent'], 'importance': job['importance'],
                 'family': job.get('parent_skill') or job['form'],
                 'source': job['source'], 'definition': definition['asset'],
                 'system': native[slug]['asset'], 'canonical': canonical[slug],
                 'preview': best['gallery_preview'], 'preview_sha256': best['gallery_preview_sha256'],
                 'gallery': 'Evidence/RuntimeReview/galeria.html#vfx-' + slug,
                 'shape_feedback_pending': slug.startswith(('GlacialSpike', 'Iceberg'))})
if len(rows) != 331 or len(viewer) != 332 or len(routes) != 136:
    raise RuntimeError('Refresh guide counts when the validated catalog changes')
rows.sort(key=lambda r: (groups.index(r['group']), r['family'].casefold(), r['scene']))
index = {'generated_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'scope': 'Current isolated components and exact canonical Phase names. No game integration approval.',
         'components': len(rows), 'viewer_scenes': len(viewer), 'canonical_forms': len(routes),
         'group_counts': dict(collections.Counter(r['group'] for r in rows)),
         'inputs': {p: sha(p) for p in ['Evidence/gameplay-runtime-build-jobs.json',
                   'Evidence/gameplay-runtime-definitions.json', 'Evidence/gameplay-runtime-form-routes.json',
                   'Evidence/runtime-viewer-cases.json', 'Evidence/gameplay-runtime-capture-audit.json']},
         'rows': rows}
(R / 'Evidence/gameplay-runtime-index.json').write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding='utf-8')

INTRO_MD = """# SanctaMMO — guia e índice VFX

Ponto de entrada para rever a arte e preparar a integração. Estado de 5 de outubro de 2026: **331 componentes, 332 cenas e 136 FormIds canónicos**. UE 5.8.3; reprodução base 1×. A revisão interna do laboratório está concluída. A aprovação no jogo depende da câmara, Manny animado e regras reais.

## Começar aqui

1. Abrir [GUIA_VFX.html](GUIA_VFX.html) ou fazer duplo clique em **Abrir-Guia-VFX.cmd**. O índice permite procurar por skill, componente ou FormId e filtrar por classe e ciclo.
2. Para imagens, abrir [a galeria](Evidence/RuntimeReview/galeria.html). Cada componente no índice tem um link para as suas capturas.
3. Para animações UE, fazer duplo clique em **Ver-Fases-Integracao.cmd** no Explorador. No visualizador, escolher **Todas as skills** e o nome/número de cena indicado no índice. Seguinte/Anterior mudam a cena; Espaço pausa, R repete e S alterna 1× / 1/3. Voltar a 1× para avaliar o timing.
4. Anotar nome do componente, número da cena, momento e alteração pretendida. Um print ajuda a distinguir arte, enquadramento e ligação à personagem.

O índice cobre os derivados atuais de integração. **Ver-Skills.cmd** e **/Game/VFXLab/** conservam a revisão artística anterior. A cena adicional 332 mostra o corpo de terreno Iceberg; esse actor não é um componente Niagara.

## Como montar uma skill

Escolher o **FormId canónico** da variante admitida e copiar o nome de **Phase canónica** do índice. Os nomes das fases numa definição canónica podem diferir dos nomes curtos usados na demonstração isolada. Por exemplo, Fire Bolt I usa a fase canónica <code>FireBoltIFlight</code>, enquanto o componente isolado usa <code>Flight</code>.

| Parte | Quando apresentar | Ligação |
| --- | --- | --- |
| Cast / Hold / Telegraph | Execução admitida e preparação ainda válida | Caster, socket ou zona real |
| Flight / Movement | Durante o voo ou movimento real | Actor do projétil/movimento; atualizar a posição |
| Impact / Contact | Após contacto confirmado | Ponto atingido e vida atual do alvo |
| Proc / Heal / ShieldApply / Mark | Após confirmar a condição e aplicar o resultado | Alvo/caster efetivamente afetado |
| Active / Resource / Link | Enquanto o estado dono existir | Corpo, contador, área ou endpoints reais |
| NaturalEnd / Cleanse | Encerramento com essa causa confirmada | Mesmo owner; cancelar/consumir não é fim natural |

Não combinar uma demonstração completa antiga com as fases derivadas: repetiria resultados. O shader desenha; gameplay decide hits, alvos, procs, CC e duração dos estados. Um miss não gera hit/proc. O índice mostra o gate e o owner de cada componente.

Usar <code>ExecutionId</code> + <code>EventSequence</code> e, quando aplicável, <code>StateId</code> e <code>LifeId</code>. Atualizações seguem a instância existente; fins são explícitos. Uma fase de voo pode terminar sem encerrar toda a execução. Ver [GUIA_EXECUCAO_VFX.md](GUIA_EXECUCAO_VFX.md) para a API, deduplicação, causas de fim e reconstrução por relevância.

## Casos que exigem atenção

- **Severing:** rank escolhe o corte; sequência confirmada escolhe marca 1/2/3. Os flashes redundantes foram retirados. As marcas não são um temporizador de dano.
- **Fire Bolt / Frost / Glacial / Lightning / Ether:** voo, impacto e procs são eventos separados. Spread, chain e resultados condicionais exigem confirmação; não inventar alvos ou saltos no shader.
- **Rally:** caster e cada afetado têm fases próprias. **Tempest:** área, telegraph, strike de gelo/lightning e resultados estão separados; reutiliza o gelo Frost Lance aprovado.
- **Mana Barrier / Volley:** Hold acompanha o progresso real. Release/cancel/interrupt terminam preparação; o tempo gravado da referência não liberta a skill.
- **Recursos:** Arcane usa count/max; Elemental usa slots ocupados, Fire/Ice/Lightning e consumo/substituição reais; Spirits usa o contador e Pending do owner. Não contar casts/hits dentro do VFX.
- **Básicos:** 14 famílias de armas × Physical/Magical. Fighter/Scout usam Physical, Mage/Mystic Magical. Melee segue base/ponta da arma; ranged segue projétil real. Contacto é confirmado à parte.
- **Guard / Dodge / Sprint:** Guard Active é estado; Mitigation e Depletion são resultados distintos. Dodge Start e Avoided estão separados. Sprint usa FootContact Stone/Snow/Mud/Water em contactos reais.

## Referência Manny

Manny do UE é a referência base confirmada pelo utilizador. Resolver no asset do jogo os bones/sockets existentes; validar transforms na pose animada e escala do actor. Cues de corpo conservam alturas authored sobre o root, sem somar novamente a altura de um socket do peito. Bleed/Poison ligam mão–cotovelo; melee liga base–ponta da arma; beams/links ligam origem–endpoint. CC de cabeça e Root nos pés precisam de leitura com roupa e câmara reais.

O visualizador geral conserva o manequim estático para rever a forma. A primeira passagem no Manny tem um palco separado: **Ver-Manny-VFX.cmd**, com 16 cenários, quatro poses de teste e três escalas. P muda a pose; E muda a escala. Ver [orientações Manny](MANNY_VFX.md) e [perfil de rig](Evidence/gameplay-runtime-rig-reference.json). As armas/animações finais e a câmara de gameplay continuam pendentes.

Esta passagem cobre **14 componentes**: 384 amostras de ligação/escala e 64 pares de capturas efeito/baseline passaram. A inspeção visual identificou leitura fraca da espada/Guard nesta vista. Os braços são avaliados separadamente; composição bilateral, Rapid Attack e marcas Severing 2/3 ainda precisam de calibração. A galeria Manny fica localmente em `Evidence/MannyReview/galeria.html`; as imagens e assets Manny estão excluídos do Git/ZIP.

## Onde estão os ficheiros

| Local | Utilização |
| --- | --- |
| /Game/Sancta/VFX/Definitions | Definições, variantes e fases |
| /Game/Sancta/VFX/Skills, Combat, Status | Sistemas atuais por apresentação |
| /Game/Sancta/VFX/Common | Materiais, meshes, texturas e escalabilidade partilhados |
| /Game/Sancta/VFX/Terrain | Corpo Iceberg, colisão, integridade e remoção |
| /Game/Sancta/VFX/Review | Palcos de QA; ficam fora do runtime do jogo |
| Source/GameplayRuntime | Fontes editáveis dos derivados atuais |
| Evidence/gameplay-runtime-index.json | Índice gerado, cenas, assets e fases canónicas exatas |
| Evidence/gameplay-runtime-form-routes.json | Identidade canónica e snapshots da variante admitida |
| Evidence/RuntimeReview | Galeria, thumbnails, folhas e contraste/recursos |
| Plugins/SanctaVFXBridge/Source/SanctaVFXRuntime | Fonte do módulo local de apresentação |
| Exports/Sancta-VFX-Runtime.zip | Pacote de migração e documentação |

Hashes nos nomes conservam revisões. Usar o sistema/definição do índice atual, em vez de escolher um asset antigo pela semelhança do nome. O ZIP contém o plugin standalone **SanctaVFXRuntime**; o Bridge é ferramenta de authoring do laboratório.

## Próximos passos no jogo

1. Rever formas Glacial Spike/Iceberg e as novas apresentações no visualizador.
2. Alargar a primeira passagem Manny: braços, leitura espada/Guard, armas/animações finais, sockets e câmara.
3. Ligar GAS/abilities, autoridade e transporte de eventos, vida/respawn e replicação.
4. Ligar terreno, canais de colisão/navegação e ciclo de vida dos hosts.
5. Fazer cook Shipping e medir escalabilidade/overdraw/concorrência no hardware alvo.

Foundation continua protegido por instrução do utilizador. A migração ainda não foi aplicada nesse projeto. As 867 capturas, 94 casos Low/contraste/terreno e 27 de recursos/hold verificam o laboratório. A medição 0/1/16/48 cobre Arcane Weaving II no frame total do palco PIE; não é orçamento isolado de todos os efeitos.

## Índice dos componentes

Os números abaixo correspondem à ordem atual do visualizador. A versão HTML permite pesquisa e mostra detalhes de integração por componente.

"""
markdown = [INTRO_MD]
for group in groups:
    markdown += ['### ' + group + '\n\n| Cena | Componente | Fase isolada | Owner |\n| --- | --- | --- | --- |\n']
    for row in rows:
        if row['group'] == group:
            markdown.append('| ' + str(row['scene']) + ' | [' + row['component'] + '](' + row['gallery'] + ') | ' + row['phase'] + ' | ' + anchors[row['anchor']] + ' |\n')
    markdown.append('\n')
(R / 'GUIA_VFX.md').write_text(''.join(markdown).rstrip() + '\n', encoding='utf-8')

cards = []
for row in rows:
    canon = ''.join('<li><code>' + esc(c['form_id']) + '</code> → Phase <code>' + esc(c['phase']) + '</code></li>' for c in row['canonical'])
    if not canon:
        canon = '<li>Apresentação partilhada: usar o PresentationId e Phase isolada acima.</li>'
    search = ' '.join(str(row[k]) for k in ['component', 'title', 'family', 'presentation_id', 'phase', 'anchor', 'scene']) + ' ' + ' '.join(c['form_id'] for c in row['canonical'])
    pending = '<span class="pending">Forma a rever pelo utilizador</span>' if row['shape_feedback_pending'] else ''
    cards.append('<article id="component-' + esc(row['component']) + '" class="effect" data-group="' + esc(row['group']) + '" data-cycle="' + ('persistent' if row['persistent'] else 'finite') + '" data-search="' + esc(search) + '">'
      '<a class="preview" href="' + esc(row['gallery']) + '"><img loading="lazy" src="' + esc(row['preview']) + '" alt="Captura de ' + esc(row['title']) + '"></a>'
      '<div class="effect-body"><div class="eyebrow">' + esc(row['group']) + ' · Cena ' + str(row['scene']) + '</div><h3>' + esc(row['title']) + '</h3>'
      '<p>' + esc(row['phase']) + ' · ' + esc(anchors[row['anchor']]) + '</p>'
      '<p class="small">' + esc(gates[row['gate']]) + ' · ' + ('Persistente, fim pelo owner' if row['persistent'] else 'Finito') + '</p>' + pending +
      '<a href="' + esc(row['gallery']) + '">Ver capturas →</a>'
      '<details><summary>Integração e ficheiros</summary><p>Componente: <code>' + esc(row['component']) + '</code></p>'
      '<p>PresentationId isolado: <code>' + esc(row['presentation_id']) + '</code><br>Phase isolada: <code>' + esc(row['phase']) + '</code></p>'
      '<p>Usar as fases canónicas seguintes ao integrar a skill:</p><ul class="codes">' + canon + '</ul>'
      '<p>Definição UE: <code>' + esc(row['definition']) + '</code></p><p>Sistema UE: <code>' + esc(row['system']) + '</code></p>'
      '<p>Fonte no laboratório: <code>' + esc(row['source']) + '</code><br>Prioridade visual: ' + esc(row['importance']) + '</p></details></div></article>')

page = """<!doctype html><html lang="pt-PT"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SanctaMMO — guia e índice VFX</title><style>
:root{color-scheme:dark;--bg:#10161c;--panel:#19232c;--line:#32414d;--ink:#edf2f5;--muted:#b3c3ce;--accent:#78d5ee}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,sans-serif}main{max-width:1280px;margin:auto;padding:32px 28px 64px}a{color:var(--accent)}h1{font-size:clamp(30px,4vw,48px);line-height:1.2;margin:12px 0}h2{margin:0 0 14px;font-size:25px}h3{font-size:18px;margin:4px 0}p{margin:8px 0}.muted,.small,.eyebrow{color:var(--muted)}.eyebrow{font-size:12px;letter-spacing:.06em;text-transform:uppercase}.small{font-size:14px}.badges,.links{display:flex;flex-wrap:wrap;gap:12px;margin:20px 0}.badge,.button{padding:8px 14px;border:1px solid var(--line);border-radius:8px;background:var(--panel)}.button{text-decoration:none}.lead{max-width:850px;color:var(--muted)}nav{display:flex;gap:18px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding:14px 0 22px}section{scroll-margin-top:24px;margin-top:42px}.guide-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.box,.effect{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden}.box{padding:22px}.box ul,.box ol{padding-left:23px}code{font:13px/1.6 ui-monospace,Consolas,monospace;overflow-wrap:anywhere;color:#d1e9f4}table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;padding:12px;border-bottom:1px solid var(--line);vertical-align:top}th{color:var(--muted)}.table-wrap{overflow:auto}.filters{display:grid;grid-template-columns:2fr 1fr 1fr;gap:16px;padding:18px 0}label{display:block;font-size:13px;color:var(--muted)}input,select{width:100%;font:16px system-ui;padding:11px;margin-top:5px;border-radius:7px;border:1px solid #516372;background:#101820;color:var(--ink)}input:focus,select:focus,summary:focus,a:focus{outline:2px solid var(--accent);outline-offset:3px}#effects{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:18px}.effect[hidden]{display:none}.preview{display:block;background:#090e12;aspect-ratio:16/9}.preview img{width:100%;height:100%;object-fit:contain}.effect-body{padding:18px}.effect-body p{font-size:14px}.pending{display:block;color:#f2c987;font-size:12px;margin:8px 0}details{margin-top:16px;border-top:1px solid var(--line);padding-top:10px}summary{cursor:pointer;font-size:14px;color:var(--accent)}.codes{padding-left:18px}.codes li{margin:10px 0}footer{margin-top:40px;border-top:1px solid var(--line);padding-top:18px;color:var(--muted);font-size:13px}@media(max-width:900px){#effects{grid-template-columns:repeat(2,minmax(0,1fr))}.guide-grid{grid-template-columns:1fr}}@media(max-width:580px){main{padding:22px 16px}#effects,.filters{grid-template-columns:1fr}.box{padding:18px}}
</style><main>
<header><div class="eyebrow">SanctaMMO · Laboratório UE 5.8.3</div><h1>Guia e índice VFX</h1><p class="lead">Um ponto de entrada para ver os efeitos, encontrar cada fase e preparar a ligação às skills. Catálogo atual de 5 de outubro de 2026.</p>
<div class="badges"><span class="badge">331 componentes</span><span class="badge">332 cenas · 1×</span><span class="badge">136 FormIds canónicos</span><span class="badge">Referência de rig: Manny</span></div>
<div class="links"><a class="button" href="Evidence/RuntimeReview/galeria.html">Ver a galeria</a><a class="button" href="#ver">Como abrir as animações</a><a class="button" href="#indice">Procurar um efeito</a></div>
<nav aria-label="Secções do guia"><a href="#ver">Rever</a><a href="#montar">Montar uma skill</a><a href="#manny">Manny</a><a href="#ficheiros">Ficheiros</a><a href="#pendentes">Próximos passos</a><a href="#indice">Índice</a></nav></header>
<section id="ver"><h2>Começar pela revisão</h2><div class="guide-grid"><div class="box"><h3>Animações no UE</h3><ol><li>No Explorador, fazer duplo clique em <strong>Ver-Fases-Integracao.cmd</strong>.</li><li>Escolher <strong>Todas as skills</strong> e o nome/número de cena do índice.</li><li>Usar Seguinte/Anterior; <strong>Espaço</strong> pausa, <strong>R</strong> repete e <strong>S</strong> alterna 1× / 1/3.</li><li>Avaliar o timing a 1× e anotar componente, cena e alteração.</li></ol><p class="small">Ver-Skills.cmd conserva o visualizador artístico anterior. A cena 332 mostra o corpo de terreno Iceberg.</p></div>
<div class="box"><h3>Capturas e feedback</h3><p>Cada cartão do índice abre as capturas da fase. Pesquisar por skill, componente ou FormId; filtrar por classe e por ciclo.</p><p>Para pedir uma alteração: indicar nome + cena + momento + aspeto a mudar. Um print ajuda a localizar o problema.</p><p class="small">A revisão interna está concluída. A forma de Glacial Spike/Iceberg e as novas apresentações ainda dependem do feedback do utilizador.</p></div></div></section>
<section id="montar"><h2>Montar a skill por eventos</h2><p class="lead">Escolher o FormId canónico da variante admitida. Em “Integração e ficheiros”, copiar o nome exato da Phase canónica. Pode diferir da fase curta da demonstração isolada.</p>
<div class="box table-wrap"><table><thead><tr><th>Parte</th><th>Quando aparece</th><th>Owner</th></tr></thead><tbody>
<tr><td>Cast / Hold / Telegraph</td><td>Execução admitida e preparação válida</td><td>Caster, socket ou zona real</td></tr>
<tr><td>Flight / Movement</td><td>Voo/movimento real; atualizar posição</td><td>Projétil / actor de movimento</td></tr>
<tr><td>Impact / Contact</td><td>Contacto confirmado</td><td>Ponto atingido + vida atual do alvo</td></tr>
<tr><td>Proc / Heal / ShieldApply / Mark</td><td>Condição confirmada e resultado aplicado</td><td>Caster / afetado real</td></tr>
<tr><td>Active / Resource / Link</td><td>Enquanto existir o estado dono</td><td>Corpo / contador / área / endpoints</td></tr>
<tr><td>NaturalEnd / Cleanse</td><td>Encerramento com essa causa confirmada</td><td>Mesmo owner; cancel não é fim natural</td></tr>
</tbody></table><p>O shader desenha; gameplay decide hits, alvos, CC, procs e duração dos estados. Um miss não gera resultados de hit. Usar ExecutionId/EventSequence e, quando aplicável, StateId/LifeId; não reiniciar o burst em cada atualização.</p><p>Exemplo: Fire Bolt I usa a Phase canónica <code>FireBoltIFlight</code>; o componente isolado usa <code>Flight</code>. Não juntar o cast completo antigo às fases derivadas.</p><p><a href="GUIA_EXECUCAO_VFX.md">Guia técnico de execução e lifecycle →</a></p></div>
<details class="box"><summary>Orientações por família</summary><ul>
<li><strong>Severing:</strong> rank escolhe corte; sequência confirmada escolhe marca 1/2/3. Flashes redundantes retirados.</li>
<li><strong>Fire / Frost / Glacial / Lightning / Ether:</strong> voo, contacto e procs separados; spread/chain/resultados condicionais exigem eventos reais.</li>
<li><strong>Rally:</strong> caster e afetados separados. <strong>Tempest:</strong> área, telegraph, gelo/lightning e resultados separados; gelo Frost Lance aprovado.</li>
<li><strong>Mana Barrier / Volley:</strong> hold usa progresso real; release/cancel/interrupt terminam preparação.</li>
<li><strong>Recursos:</strong> count/max, slots/elementos e Pending vêm do owner. O VFX não conta casts ou hits.</li>
<li><strong>Básicos:</strong> 14 armas × Physical/Magical; Fighter/Scout Physical, Mage/Mystic Magical. Melee segue arma; ranged segue projétil real.</li>
<li><strong>Guard / Dodge / Sprint:</strong> estados e resultados separados; FootContact depende de contacto/superfície reais.</li></ul></details></section>
<section id="manny"><h2>Manny animado no laboratório</h2><div class="box"><p>O palco separado <strong>Ver-Manny-VFX.cmd</strong> usa o Manny do projeto: 16 cenários, quatro poses de teste e escalas 0,8× / 1× / 1,2×. <strong>P</strong> muda a pose e <strong>E</strong> muda a escala.</p><p>Primeira passagem de <strong>14 componentes</strong>: 384 amostras de ligação/escala e 64 pares efeito/baseline passaram. A inspeção visual identificou leitura fraca da espada/Guard nesta vista.</p><p>Bleed/Poison: mão → cotovelo, um braço de cada vez. Melee: pega → extremidade de uma haste de calibração. Beams/links: mão → endpoint. Corpo, cabeça e pés compensam as alturas já desenhadas no shader. Composição bilateral, Rapid Attack, marcas Severing 2/3, armas/animações finais e câmara de gameplay continuam pendentes.</p><p class="small">O visualizador geral conserva o manequim estático. Galeria Manny local: <code>Evidence/MannyReview/galeria.html</code>; imagens/assets Manny excluídos do Git/ZIP. <a href="MANNY_VFX.md">Orientações e preparação</a> · <a href="Evidence/gameplay-runtime-rig-reference.json">Perfil de rig</a>.</p></div></section>
<section id="ficheiros"><h2>Onde trabalhar</h2><div class="box table-wrap"><table><thead><tr><th>Local</th><th>Conteúdo</th></tr></thead><tbody>
<tr><td><code>/Game/Sancta/VFX/Definitions</code></td><td>Definições e fases</td></tr><tr><td><code>/Game/Sancta/VFX/Skills · Combat · Status</code></td><td>Sistemas atuais</td></tr><tr><td><code>/Game/Sancta/VFX/Common · Terrain</code></td><td>Assets partilhados / terreno Iceberg</td></tr><tr><td><code>/Game/Sancta/VFX/Review</code></td><td>Palcos de QA, fora do runtime do jogo</td></tr><tr><td><code>Source/GameplayRuntime</code></td><td>Fontes editáveis no laboratório</td></tr><tr><td><a href="Evidence/gameplay-runtime-index.json">Índice de integração JSON</a></td><td>Cenas, assets e nomes exatos das fases canónicas</td></tr><tr><td><a href="GUIA_EXECUCAO_VFX.md">Guia técnico</a> · <a href="GUIA_VFX.md">Guia Markdown</a></td><td>API / documentação para Git</td></tr><tr><td><code>Exports/Sancta-VFX-Runtime.zip</code></td><td>Plugin standalone SanctaVFXRuntime, Content e documentação</td></tr></tbody></table><p class="small">Usar os assets indicados no índice; hashes conservam revisões anteriores. O Bridge é ferramenta de authoring, não o plugin de execução a instalar no jogo.</p></div></section>
<section id="pendentes"><h2>Próximos passos</h2><div class="box"><ol><li>Rever Glacial Spike/Iceberg e as novas apresentações.</li><li>Calibrar Manny, sockets, pose e câmara.</li><li>Ligar GAS/abilities, autoridade, transporte/replicação e vida/respawn.</li><li>Ligar terreno, colisão/navegação e hosts de apresentação.</li><li>Fazer cook Shipping e medir concorrência/overdraw/escalabilidade no hardware alvo.</li></ol><p class="small">Foundation continua protegido. A revisão verifica o laboratório: 867 capturas, 94 casos Low/contraste/terreno e 27 de recursos/hold. A medição 0/1/16/48 cobre Arcane Weaving II no frame total do palco PIE; não certifica o orçamento isolado de todo o catálogo.</p></div></section>
<section id="indice"><h2>Índice pesquisável</h2><p class="lead">Abrir “Integração e ficheiros” para ver FormIds, Phase canónica, definição e Niagara System atuais.</p>
<div class="filters"><label>Procurar<input id="search" type="search" placeholder="Fire Bolt, Tempest, Guard, FormId…" autocomplete="off"></label><label>Classe / grupo<select id="group"><option value="">Todos os grupos</option>__OPTIONS__</select></label><label>Ciclo<select id="cycle"><option value="">Todos os ciclos</option><option value="finite">Finito</option><option value="persistent">Persistente</option></select></label></div>
<p id="count" role="status" aria-live="polite">331 componentes</p><div id="effects">__CARDS__</div><p id="empty" hidden>Nenhum efeito corresponde aos filtros. Limpar a pesquisa ou escolher outro grupo.</p></section>
<footer>Índice gerado das definições e evidência correntes; referências históricas preservadas. Nenhuma alteração ao Foundation/Engine. A documentação funciona localmente, sem servidor e sem recursos externos.</footer></main>
<script>
const search=document.getElementById('search'),group=document.getElementById('group'),cycle=document.getElementById('cycle');
const cards=Array.from(document.querySelectorAll('.effect'));
const normalize=s=>s.toLowerCase().normalize('NFD').split('').filter(c=>c.codePointAt(0)<768||c.codePointAt(0)>879).join('');
cards.forEach(c=>c.dataset.normalized=normalize(c.dataset.search));
function filter(){let n=0;const q=normalize(search.value.trim());cards.forEach(c=>{c.hidden=!(c.dataset.normalized.includes(q)&&(!group.value||c.dataset.group===group.value)&&(!cycle.value||c.dataset.cycle===cycle.value));if(!c.hidden)n++});document.getElementById('count').textContent=n+' de 331 componentes';document.getElementById('empty').hidden=n!==0;}
search.addEventListener('input',filter);group.addEventListener('change',filter);cycle.addEventListener('change',filter);filter();
</script></html>"""
page = page.replace('__OPTIONS__', ''.join('<option>' + esc(g) + '</option>' for g in groups)).replace('__CARDS__', ''.join(cards))
(R / 'GUIA_VFX.html').write_text(page, encoding='utf-8')
(R / 'Abrir-Guia-VFX.cmd').write_text('@echo off\nstart "" "%~dp0GUIA_VFX.html"\n', encoding='ascii')
print(json.dumps({'components': len(rows), 'scenes': len(viewer), 'canonical_forms': len(routes), 'groups': index['group_counts']}))
