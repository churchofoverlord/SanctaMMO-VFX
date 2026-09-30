# Continuar a conversão para Niagara noutra máquina

## Estado em 30 de setembro de 2026

O objetivo é editar os protótipos de VFX do SanctaMMO no Unreal/Niagara. A primeira conversão é o **Fire Bolt I**. O Foundation original não foi alterado e continua protegido: trabalhar num laboratório ou numa cópia.

**A conversão ainda não está concluída.** Existem seis assets de materiais/instâncias e dois sistemas antigos vazios, preservados em `Content/VFXLab/FireBoltI`. `NS_FireBoltI` ainda não foi guardado. A montagem dos três emissores e dos nove parâmetros está definida em `Scripts/build_firebolt.py`. O plugin de montagem foi compilado com sucesso na máquina anterior; a verificação com renderização foi interrompida durante a compilação inicial de shaders porque o utilizador precisava do UE noutro projeto. A simulação e a imagem não estão verificadas.

`VFX-status.json` regista esse ponto de paragem. `Evidence/previous-nullrhi-build-report.json` é um relatório anterior de uma tentativa falhada, conservado para diagnóstico; **não certifica o resultado final**.

## Preparar a nova máquina

1. Clonar este repositório, de preferência num caminho curto como `C:\Dev\SanctaMMO-VFX`. Abrir `unreal\SanctaVFX-Niagara`.
2. Transferir separadamente a instalação **UE 5.8.2** usada antes. Incluir o Editor, os binários de desenvolvimento/precompilados, UnrealBuildTool, o runtime DotNet 10.0 e os fontes do plugin `Engine/Plugins/FX/CascadeToNiagaraConverter`. São necessários Visual Studio Build Tools C++ e Windows SDK compatíveis com esta instalação. Não atualizar nem recompilar o Engine como solução automática.
3. Se o Engine não estiver em `C:\UE582`, indicar o caminho em cada comando. Exemplo em PowerShell:

   ```powershell
   .\Verificar-Ambiente.cmd -EngineRoot 'D:\UE582'
   .\Compilar-Ponte.cmd -EngineRoot 'D:\UE582'
   .\Retomar-Preparacao.cmd -EngineRoot 'D:\UE582'
   .\Abrir-Laboratorio.cmd -EngineRoot 'D:\UE582'
   ```

   Também é possível definir `$env:UE_ENGINE_ROOT = 'D:\UE582'` nessa sessão. `Verificar-Ambiente.cmd` apenas verifica ficheiros; não abre o editor nem inicia compilação.
4. `Compilar-Ponte.cmd` recupera três fontes do conversor a partir do Engine local, monta o plugin em `BuildHost` e compila **VFXBuildEditor** com `-NoEngineChanges -UsePrecompiled`. Copia o plugin resultante para o laboratório. Não altera os fontes do Engine nem força BuildIds. Os fontes recuperados e todos os binários/caches ficam ignorados pelo Git.
5. `Retomar-Preparacao.cmd` cria `NS_FireBoltI`, espera pela compilação de Niagara, guarda o sistema e executa os testes de simulação e as capturas. Se o sistema já existir, executa a validação sem o recriar. A primeira compilação de shaders pode demorar e consumir CPU; iniciar quando o UE estiver disponível.
6. Confirmar `VFX-validation-report.json` com `status: passed`, inspecionar as imagens em `Previews` e abrir o efeito. O relatório prova a simulação; a fidelidade visual exige inspeção e comparação com o HTML.

Os caminhos do Engine são configuráveis; os caches ficam em `Saved` dentro do laboratório. O `.uproject` usa o GUID partilhado `{879D9D6C-4F90-4BD2-533F-CD9F03C78B21}`, que cada máquina regista no Windows a apontar para o seu motor (ver `Docs/Engineering/UE_LAPTOP_ENGINE.md` no SanctaMMO-Foundation-5.8); os comandos continuam a chamar explicitamente o editor indicado. Não foram incluídos Engine, Editor, DLLs/PDBs, caches, histórico Git do Foundation ou a cópia antiga do jogo.

## O que já está implementado

Referência: [`prototypes/mage/fire-bolt-i/fire-bolt-i-vfx.html`](../../prototypes/mage/fire-bolt-i/fire-bolt-i-vfx.html), na raiz do repositório. As regras de direção visual e orçamento continuam em `CLAUDE.md`, `docs/skills.json` e `docs/ue-vfx-tech-spec.html`.

O gerador usa módulos nativos do Niagara para três emissores CPU em espaço local: `Head`, `Tail` e `Impact`, cada um com um Sprite Renderer. O voo é na direção +X. A cauda cresce desde a origem e contrai após a chegada; o impacto começa em `CastDelay + Distance / Speed`.

| User Parameter | Valor inicial |
|---|---:|
| Speed | 1200 cm/s |
| Distance | 800 cm |
| CastDelay | 0,1 s |
| HeadSize | 57,6 cm |
| TailLength | 260 cm |
| TailWidth | 104 cm |
| TailFade | 0,2 s |
| ImpactDuration | 0,25 s |
| ImpactSize | 70 cm |

Manter velocidade, distâncias, tamanhos e durações positivos. Cores e brilho são parâmetros `HotColor`, `RedColor` e `Intensity` das instâncias `MI_FireBolt_…`. A forma procedural está num nó Custom dos materiais base: editável no Material Editor, mas exige edição da fórmula do shader. A cauda ainda é uma aproximação do HTML.

`SanctaVFXLabLibrary` permite inspecionar o sistema, alterar floats expostos, simular em instantes definidos e capturar imagens pelo Unreal. Os testes verificam presença de cabeça/cauda durante o voo, impacto à chegada, fim das partículas e a resposta à redução da velocidade para metade. Restauram a velocidade inicial antes de guardar.

## Problemas já identificados e cuidados para continuar

- O `CascadeToNiagaraConverter` da instalação tinha um BuildId diferente do Editor. Fica explicitamente desativado. Usar o plugin local reconstruído; nunca editar manifests para fingir compatibilidade.
- Não usar `-nullrhi` para validar prontidão ou simulação: o Niagara devolve `IsReadyToRun=false` quando `FApp::CanEverRender()` é falso. Os comandos usam D3D11 e `-AllowCommandletRendering -RenderOffscreen`.
- O caminho de colagem do Sprite Renderer constrói widgets mesmo sem janela. A inicialização de Slate com Null Renderer no módulo local resolveu essa falha.
- Usar `unreal.load_asset` para verificar módulos do plugin: o Asset Registry nem sempre os conhece no início da sessão.
- O caminho correto de Solve Forces é `/Niagara/Modules/Solvers/SolveForcesAndVelocity.SolveForcesAndVelocity`.
- Inicializar explicitamente `Particles.Age` e `Particles.NormalizedAge` em Particle Spawn. Isso resolveu um erro de leitura da idade antes de ser definida na cauda.
- Fazer `ctx.cleanup()` uma única vez antes de encerrar o editor; a conversão mantida viva provocava falhas durante o descarregamento de AssetTools.
- `UE_SKIP_UBT_SDK_SETUP=1` evita a verificação inicial de SDK a competir pelo mutex de outras compilações. Os comandos já o definem.
- Não lançar a preparação pelo atalho antigo do Foundation copiado. Usar este projeto independente.

## Trabalho restante

Executar a preparação com o Engine transferido, resolver qualquer erro que os relatórios revelem, verificar a imagem no editor e comparar vista lateral e câmara de jogo com o HTML. Não declarar o efeito pronto apenas por a compilação passar. Depois, confirmar os parâmetros na UI e medir custo com vários casts. O projétil real e o evento de acerto devem controlar voo e impacto na integração futura; combate, sockets e GameplayCues ainda não foram ligados. Os restantes protótipos precisam de conversões próprias.
