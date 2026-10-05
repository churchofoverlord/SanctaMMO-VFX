# Continuação deste laboratório

- Ler `CONTINUAR.md` e `VFX-status.json` antes de iniciar trabalho. O sistema final foi guardado e a simulação passou no UE 5.8.3; as capturas e os custos exigem evidência própria. Preview e BeforeFix são versões antigas vazias; outros arquivos preservam tentativas anteriores.
- Respeitar a instrução do utilizador: não alterar o SanctaMMO-Foundation original. O laboratório é independente.
- Engine/Editor foram transferidos separadamente. O caminho pode mudar; usar `UE_ENGINE_ROOT` ou `-EngineRoot`. Não iniciar compilação pesada se o utilizador precisar do UE livre.
- Não publicar fontes, assets ou binários do Engine. A ponte usa o conversor nativo compatível do UE 5.8.3; não copiar fontes privados do Engine.
- Não modificar Engine, BuildIds ou substituir DLLs do Engine. Compilar apenas o plugin/host com os comandos fornecidos.
- Os relatórios antigos são evidência de tentativas falhadas. Só declarar simulação validada após os testes passarem e fidelidade visual após inspeção de capturas reais do UE.
- O Git deste repositório usa `main`, sem branches paralelos, conforme `CLAUDE.md` na raiz. Não incluir alterações de outros trabalhos nos commits do laboratório.
