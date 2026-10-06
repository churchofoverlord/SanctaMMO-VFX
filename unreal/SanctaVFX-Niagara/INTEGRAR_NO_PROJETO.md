# Integrar os VFX no projeto principal

Pacote para **UE 5.8.3**: 331 componentes atuais, 136 FormIds canónicos e 1786 packages com dependências verificadas. Inclui fontes do plugin standalone **SanctaVFXRuntime**, assets em `Content`, guias e índice. As decisões de combate e o transporte de eventos pertencem ao jogo.

## Instalar

1. Descompactar `Sancta-VFX-Runtime.zip` numa pasta temporária e conferir `PACOTE.json`.
2. Com o Editor fechado, copiar a pasta `Plugins/SanctaVFXRuntime` para a pasta `Plugins` do projeto principal.
3. Copiar o conteúdo da pasta `Content` para a pasta `Content` do projeto principal, conservando todos os caminhos relativos. As referências dos assets dependem destes caminhos; não mover apenas os Niagara Systems.
4. Ativar `SanctaVFXRuntime` no projeto. O plugin declara a dependência de Niagara. Regenerar os ficheiros do projeto e compilar o target Editor com UE 5.8.3 e a toolchain C++ do projeto; o ZIP contém fontes, não DLLs do laboratório.
5. Abrir o projeto e conferir as definições em `/Game/Sancta/VFX/Definitions`. Usar [GUIA_VFX.html](GUIA_VFX.html) e [índice de componentes](Evidence/gameplay-runtime-index.json) para encontrar os sistemas e as fases exatas.

Se o projeto já tiver este plugin ou assets nos mesmos caminhos, comparar a versão e os hashes antes de substituir ficheiros. Conservar uma revisão recuperável do projeto.

## Ligar às skills

Adicionar `USanctaVFXPresentationComponent` ao host de apresentação e preencher `Definitions` com as definições necessárias. Para chamadas em C++, acrescentar `SanctaVFXRuntime` às dependências do módulo consumidor.

Usar os FormIds de [gameplay-runtime-form-routes.json](Evidence/gameplay-runtime-form-routes.json) e os nomes de fase da definição. Enviar `FSanctaVFXEvent` com os actores, sockets, `LifeId`, `ExecutionId`, `EventSequence` e `StateId` reais. Cast/hold, projétil, contacto, proc e estado são fases distintas. Um contacto exige hit confirmado; um proc exige aplicação confirmada. Um Anim Notify sincroniza a apresentação, não decide dano ou CC.

O jogo fornece posição/normal de contacto, endpoint, raio, alcance, cone, progresso de cast e recursos. Ligar cancelamento, interrupção, fim da fase, remoção de estado, morte e respawn através da API documentada em [GUIA_EXECUCAO_VFX.md](GUIA_EXECUCAO_VFX.md). Beams seguem as duas pontas; cada projétil de Volley recebe o seu voo próprio. Iceberg exige ligação aos canais de colisão e à navegação reais do jogo.

## Manny e limites atuais

O laboratório cobriu os 331 componentes em 340 cenários animados. As [receitas de ligação](Evidence/gameplay-manny-full-binding-index.json) e [orientações Manny](MANNY_VFX_TODOS.md) acompanham o pacote. Os comprimentos de armas e poses de template são referências de teste: substituir por armas, sockets, animações e notifies finais.

**As seis variantes `Source/MannyCalibration` e os inputs independentes dos dois braços/escala usam um adaptador privado do laboratório. A promoção destas variantes e do adaptador ao runtime ainda está pendente.** As fontes estão no repositório VFX para esse trabalho; o ZIP não instala automaticamente as alterações do laboratório no jogo. O módulo editor `SanctaVFXMannyLab`, os assets Manny/animações do UE e as capturas Manny são locais e não fazem parte desta instalação.

Persistem alertas de oclusão/enquadramento e feedback de forma para Glacial/Iceberg. Testar na câmara real, com roupa/armadura, Low, autoridade e replicação, seguida de cook Shipping e medição no hardware alvo. A validação do laboratório não é aprovação de produção.

## Ficheiros a consultar

| Ficheiro no ZIP | Uso |
| --- | --- |
| `PACOTE.json` | Versão, contagens e âmbito |
| `Plugins/SanctaVFXRuntime` | Plugin runtime e fontes C++ |
| `Content` | Assets e dependências nos caminhos originais |
| `GUIA_VFX.html` | Guia pesquisável de componentes e fases |
| `GUIA_EXECUCAO_VFX.md` | API, eventos e contratos de integração |
| `Evidence/gameplay-runtime-migration-manifest.json` | Lista explícita de packages e hashes |
| `Evidence/gameplay-runtime-form-routes.json` | FormIds e encaminhamento |
| `Evidence/gameplay-runtime-definitions.json` | Definições e fases |
| `Evidence/gameplay-manny-full-binding-index.json` | Receitas de ligação ao rig e requisitos pendentes |

Esta entrega prepara a integração. Não altera o projeto principal/Foundation.
