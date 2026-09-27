import re, os, json, html
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
readme = open('README.md', encoding='utf8').read()
rows = re.findall(r'^\| (Fighter|Mage|Mystic|Scout) · (.+?) \| .*?\| \[(prototypes/[^\]]+)\]', readme, re.M)
icons = {c: sorted(os.listdir(f'docs/icons/{c}')) for c in ['fighter', 'mage', 'mystic', 'scout']}
def toks(s): return [t for t in re.split(r'[^a-z0-9]+', s.lower()) if t]
OVR = {'bulwark':'rage-bulwark-2.jpg', 'weave':'manifest-weave-2.jpg', 'poison-stance':'poison-bleed-stance-1.jpg', 'bleed-stance':'poison-bleed-stance-2.jpg',
       'poison-sac':'poison-sac-hemorrhage-1.jpg', 'hemorrhage':'poison-sac-hemorrhage-2.jpg', 'basic-attack-poison':'poison-bleed-stance-1.jpg', 'basic-attack-bleed':'poison-bleed-stance-2.jpg'}
def icon_for(cls, folder):
    if folder in OVR: return f'docs/icons/{cls}/{OVR[folder]}'
    ft = toks(folder); best, score = None, 0
    for ic in icons[cls]:
        it = toks(ic[:-4])
        sc = sum(1 for t in ft if t in it) - .01*len(it)
        if it and it[0] != ft[0]: sc -= 1.5
        if sc > score: best, score = ic, sc
    # variants: *-tank / *-moon / *-enemy -> second icon when there is a pair
    if best and best[:-4].endswith('-1') and any(k in folder for k in ['tank', 'moon', 'enemy', 'poison']):
        alt = best[:-6] + '-2.jpg'
        if alt in icons[cls]: best = alt
    return f'docs/icons/{cls}/{best}' if best else ''
CLS = {'Fighter': ('fighter', 'Fighter'), 'Mage': ('mage', 'Mage'), 'Mystic': ('mystic', 'Mystic'), 'Scout': ('scout', 'Scout')}
done = {c: [] for c in CLS}
for c, name, path in rows:
    folder = path.split('/')[2]
    done[c].append((name, path, icon_for(CLS[c][0], folder)))
# missing skills (from the guide), per class
d = json.load(open('docs/skills.json', encoding='utf8'))
MISSING = {'Mage': [],
           'Scout': ['Vine Field II', 'Backstab II', 'Rapid Attack', 'Blinding Dart', 'Long Jump', 'Evasion', 'Sand Shot', 'Sickness']}
ic_by_name = {x['nome']: x['icones'][0] for x in d}
ACC = {'Fighter': '#ff3d7f', 'Mage': '#8b6fd6', 'Mystic': '#ffb52e', 'Scout': '#7fbf8a'}
total = sum(len(v) for v in done.values()); miss = sum(len(v) for v in MISSING.values())

def card(name, path, icon):
    return f'''<a class="card" href="{html.escape(path)}" data-q="{html.escape(name.lower())}"><img src="{html.escape(icon)}" alt="" loading="lazy" width="56" height="56"><span>{html.escape(name)}</span></a>'''
# most recent prototypes (last commit touching the file; uncommitted = now), shown on top
import subprocess, time
def mtime(path):
    r = subprocess.run(['git', 'log', '-1', '--format=%ct', '--', path], capture_output=True, text=True)
    changed = subprocess.run(['git', 'status', '--porcelain', '--', path], capture_output=True, text=True).stdout.strip()
    return time.time() if changed or not r.stdout.strip() else int(r.stdout.strip())
allp = [(mtime(p), c, n, p, i) for c in CLS for n, p, i in done[c]]
recent = sorted(allp, key=lambda x: -x[0])[:8]
sections = [f'''<section id="recentes" style="--acc:var(--gold)">
    <header class="sh"><h2>Recentes</h2><span class="count">últimos {len(recent)} protótipos</span></header>
    <div class="grid">{''.join(card(f"{c} · {n}", p, i) for _, c, n, p, i in recent)}</div>
  </section>''']
for c in CLS:
    items = ''.join(card(n, p, i) for n, p, i in done[c])
    ms = MISSING.get(c, [])
    mitems = ''.join(f'<div class="card todo" data-q="{html.escape(n.lower())}"><img src="docs/{html.escape(ic_by_name.get(n, ""))}" alt="" loading="lazy" width="56" height="56"><span>{html.escape(n)}</span><small>por fazer</small></div>' for n in ms)
    sections.append(f'''<section id="{CLS[c][0]}" style="--acc:{ACC[c]}">
    <header class="sh"><h2>{c}</h2><span class="count">{len(done[c])} protótipos{f" · {len(ms)} por fazer" if ms else " · completo"}</span></header>
    <div class="grid">{items}{mitems}</div>
  </section>''')

page = f'''<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>SanctaMMO VFX</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=IBM+Plex+Sans:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{color-scheme:dark;--ground:#0b0c0e;--panel:#131416;--line:#26272a;--ink:#e9e3d8;--muted:#8f8a82;--gold:#f2b53a}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--ink);font:14px/1.5 "IBM Plex Sans",system-ui,sans-serif;padding-inline:16px;padding-block:28px 48px}}
.wrap{{max-width:1180px;margin:0 auto;display:grid;gap:28px}}
.top{{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:12px 24px}}
.eyebrow{{font:500 11px/1 "IBM Plex Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:10px}}
h1{{font:700 clamp(30px,5vw,46px)/1 "Cinzel",Georgia,serif;margin:0;letter-spacing:.04em}}
h1 span{{color:var(--gold)}}
.lead{{max-width:60ch;color:var(--muted);margin:10px 0 0}}
.stats{{font:500 12px "IBM Plex Mono",monospace;color:var(--muted);font-variant-numeric:tabular-nums}}
.stats b{{color:var(--ink);font-weight:500}}
.bar{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;position:sticky;top:0;z-index:2;background:var(--ground);padding-block:10px;border-bottom:1px solid var(--line)}}
.bar a{{font:500 12px "IBM Plex Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);text-decoration:none;border:1px solid var(--line);padding:6px 10px}}
.bar a:hover{{color:var(--ink);border-color:var(--muted)}}
.bar input{{flex:1 1 200px;min-width:0;background:var(--panel);border:1px solid var(--line);color:var(--ink);font:inherit;padding:7px 10px}}
.bar input:focus-visible,.card:focus-visible,.bar a:focus-visible{{outline:2px solid var(--gold);outline-offset:2px}}
section{{display:grid;gap:12px;scroll-margin-top:64px}}
.sh{{display:flex;align-items:baseline;gap:14px;border-bottom:1px solid var(--line);padding-bottom:8px}}
h2{{font:700 18px "Cinzel",Georgia,serif;letter-spacing:.1em;text-transform:uppercase;margin:0;color:var(--acc)}}
.count{{font:500 11px "IBM Plex Mono",monospace;color:var(--muted);letter-spacing:.08em}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:8px}}
.card{{display:flex;align-items:center;gap:12px;padding:8px;background:var(--panel);border:1px solid var(--line);color:var(--ink);text-decoration:none;min-width:0;position:relative}}
a.card:hover{{border-color:var(--acc)}}
a.card:hover span{{color:var(--acc)}}
.card img{{width:56px;height:56px;object-fit:cover;flex:none;border:1px solid var(--line);background:#000}}
.card span{{font-weight:500;line-height:1.25;overflow-wrap:anywhere}}
.card.todo{{opacity:.42}}
.card.todo img{{filter:grayscale(1)}}
.card small{{position:absolute;right:8px;bottom:6px;font:500 10px "IBM Plex Mono",monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}}
.hide{{display:none!important}}
footer{{color:var(--muted);font-size:12px;border-top:1px solid var(--line);padding-top:12px}}
</style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <div>
      <div class="eyebrow">SanctaMMO · VFX das skills · Protótipos no browser</div>
      <h1><span>Sancta</span>MMO VFX</h1>
      <p class="lead">Protótipos interativos dos VFX das skills (Three.js) para validar aspeto e arquitetura antes do Unreal Engine 5 (GAS + Niagara). Clica numa skill para abrir o protótipo.</p>
    </div>
    <div class="stats"><b>{total}</b> protótipos · <b>{miss}</b> por fazer</div>
  </div>
  <nav class="bar" aria-label="Classes">
    <a href="#recentes">Recentes</a><a href="#fighter">Fighter</a><a href="#mage">Mage</a><a href="#mystic">Mystic</a><a href="#scout">Scout</a>
    <input id="q" type="search" placeholder="Procurar skill…" aria-label="Procurar skill">
  </nav>
  {"".join(sections)}
  <footer>Direção visual: docs/VFX_Skills_SanctaMMO.docx · Regras e orçamentos: <a href="docs/ue-vfx-tech-spec.html" style="color:inherit">ficha técnica UE5</a></footer>
</div>
<script>
const q = document.getElementById('q');
q.addEventListener('input', () => {{ const v = q.value.trim().toLowerCase();
  document.querySelectorAll('.card').forEach(c => c.classList.toggle('hide', !!v && !c.dataset.q.includes(v)));
  document.querySelectorAll('section').forEach(s => s.classList.toggle('hide', !!v && !s.querySelector('.card:not(.hide)'))); }});
</script>
</body>
</html>
'''
open('index.html', 'w', encoding='utf8').write(page)
print(total, miss)
for c in CLS:
    for n, p, i in done[c]:
        if not i or not os.path.exists(i) or not os.path.exists(p): print('!!', c, n, p, i)
