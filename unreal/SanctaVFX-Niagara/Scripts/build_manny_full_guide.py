"""Navigation for every Manny scenario; capture status never implies game approval."""
import hashlib,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
read=lambda p:json.loads((R/p).read_text(encoding='utf-8-sig'))
cases=read('Evidence/gameplay-manny-full-cases.json')
index=read('Evidence/gameplay-manny-full-binding-index.json')
report=read('Evidence/gameplay-manny-full-validation.json') if (R/'Evidence/gameplay-manny-full-validation.json').exists() else {}
digest=hashlib.sha256((R/'Evidence/gameplay-manny-full-cases.json').read_bytes()).hexdigest()
current=report.get('inputs',{}).get('Evidence/gameplay-manny-full-cases.json')==digest
count=report.get('cases',0) if current else 0
measured=report.get('screenshots',0) if current else 0
visible=report.get('visible_screenshots',0) if current else 0
flags=len(report.get('diagnostic_flags',[])) if current else 0
text=f'''# Manny — índice completo dos VFX

**331 componentes / 340 cenários.** Capturas auditadas deste catálogo: **{count}/340**. O estado detalhado está em `Evidence/gameplay-manny-full-validation.json`; aprovação de produção e integração no jogo continuam pendentes.

Presença medida em **{visible}/{measured} pares**; **{flags} flags de diagnóstico** de tamanho, margem/enquadramento ou oclusão. Cada cenário tem de ter uma representação visível para passar a auditoria. Isso não certifica todas as poses/vistas nem qualidade final de gameplay.

## Ver

**Ver-Manny-Todos-VFX.cmd** abre as animações a 1×. **Ver-Capturas-Manny-Todos.cmd** abre a galeria local, sem UE ou servidor. Pesquisar a skill ou o identificador do componente; escolher pose e vista. Clicar na imagem para abrir o PNG completo.

P muda a pose, E a escala, V a vista, B os braços e as setas o cenário. Espaço pausa, R repete e S alterna 1×/⅓×. As quatro poses são de template e não substituem animações/notifies finais.

## Integrar

Usar a definição e fase indicadas no índice. Caster, alvo, projétil e ponto no mundo têm owners distintos. As fases de contacto/proc só partem de eventos confirmados; os inputs de teste do laboratório não são regras de dano ou aplicação de estados.

Efeitos que incluem chão e corpo seguem a raiz para conservar o chão nos pés. Cues isolados de peito/cabeça compensam a altura já gravada. Áreas no mundo conservam as dimensões de gameplay, independentemente da escala do personagem. Beams usam duas pontas avaliadas na pose atual; stances de mãos precisam dos quatro inputs independentes de mão/antebraço.

Os básicos cobrem 14 famílias de armas e variantes físicas/mágicas. Dimensões e orientações de armas são provisórias; a integração exige os modelos e sockets reais de base/ponta/muzzle. Guard, Dodge, Sprint e contactos dos pés usam poses de template e um chão plano. Guard planar pode desaparecer de perfil e o corpo pode tapar projéteis/contactos: conferir as três vistas, não apenas a contagem de píxeis.

O adaptador de escala/braços e seis variantes Manny permanecem no módulo editor do laboratório. O ZIP runtime não recebe automaticamente estes fixtures. Foundation e Engine mantêm-se preservados.

## Ficheiros

| Ficheiro | Uso |
| --- | --- |
| Evidence/gameplay-manny-full-cases.json | Catálogo reproduzível dos 340 cenários |
| Evidence/gameplay-manny-full-binding-index.json | Receitas de ligação e requisitos de integração |
| Evidence/gameplay-manny-full-validation.json | Medições, imagens, hashes e flags |
| Evidence/MannyFullReview/galeria.html | Galeria local pesquisável |
| Saved/MannyFullCaptures | PNG completos, baselines, resultados e logs por lote |
| Scripts/Run-MannyFullAudit.ps1 | Retoma os lotes com inputs atuais |
| Scripts/audit_manny_full_review.py | Mede e gera a galeria; --partial para lotes completos |
| MANNY_VFX.md | Preparação do rig e limites da calibração |

## Índice de cenários

| Nº | Cenário | Componente | Fase | Ligação |
| --- | --- | --- | --- | --- |
'''
for i,c in enumerate(cases,1):
    text+=f'| {i} | [{c["title"]}](Evidence/MannyFullReview/galeria.html#{c["name"]}) | `{c["component"]}` | {c["phase"]} | {c["binding"]} |\n'
(R/'MANNY_VFX_TODOS.md').write_text(text,encoding='utf-8')
print(json.dumps({'scenarios':len(cases),'audited_current_catalog':count}))
