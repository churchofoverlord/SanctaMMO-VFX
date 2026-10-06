# VFX — entrega para integração no projeto principal

**UE 5.8.3 · 331 componentes · 136 FormIds · 1786 packages.**

Descarregar [Sancta-VFX-Runtime.zip](Sancta-VFX-Runtime.zip) através de **Download raw** no GitHub. Descompactar e começar em **INTEGRAR_NO_PROJETO.md**, incluído no ZIP e [disponível no repositório](../../unreal/SanctaVFX-Niagara/INTEGRAR_NO_PROJETO.md).

O ZIP contém `Content`, o plugin standalone `Plugins/SanctaVFXRuntime` com fontes C++, guia pesquisável, contratos, índice e receitas Manny. Copiar Content/Plugins para os caminhos correspondentes do projeto e compilar com UE 5.8.3. Ligar os eventos, actores, sockets e fases através da API documentada.

`SHA256SUMS` permite conferir o download. `manifest.json` regista a validação dos hashes de todos os packages, das fontes compiladas e da integridade do ZIP.

As ligações ao gameplay, armas/animações finais e promoção do adaptador privado Manny continuam pendentes. O ZIP não inclui Foundation, Engine, DLLs do laboratório, módulo editor Manny ou assets Epic da personagem. Nenhuma alteração foi aplicada ao projeto principal.

As fontes editáveis de calibração ficam em [Source/MannyCalibration](../../unreal/SanctaVFX-Niagara/Source/MannyCalibration); a implementação do adaptador de referência fica no [módulo editor do laboratório](../../unreal/SanctaVFX-Niagara/Plugins/SanctaVFXMannyLab/Source). Servem de referência para a promoção ao runtime, não de plugin Shipping a instalar.
