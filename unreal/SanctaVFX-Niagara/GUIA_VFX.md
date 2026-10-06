# SanctaMMO — guia e índice VFX

Ponto de entrada para rever a arte e preparar a integração. Estado de 6 de outubro de 2026: **331 componentes, 332 cenas e 136 FormIds canónicos**. UE 5.8.3; reprodução base 1×. A revisão interna do laboratório está concluída. A aprovação no jogo depende da câmara, Manny animado e regras reais.

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

O visualizador geral conserva o manequim estático para rever a forma. O palco separado **Ver-Manny-VFX.cmd** tem 340 cenários, quatro poses de teste e três escalas. P muda a pose; E muda a escala; V muda a vista; B isola os braços. Ver [orientações Manny](MANNY_VFX.md) e [perfil de rig](Evidence/gameplay-runtime-rig-reference.json).

O catálogo completo tem **331 componentes / 340 cenários** em **Ver-Manny-Todos-VFX.cmd**. Ver [índice Manny completo](MANNY_VFX_TODOS.md) para o estado atual de capturas, ligações e pendentes. **Ver-Capturas-Manny-Todos.cmd** abre a galeria local pesquisável; estas capturas e o módulo editor permanecem no laboratório.

A passagem completa cobre **331 componentes**: 8160 amostras de ligação/escala, 4080 pares efeito/baseline em três vistas e 24 imagens de braços isolados. Consultar a validação atual e o índice para resultados e flags. Bleed/Poison/Rapid Attack usam ligações independentes dos dois braços; as marcas Severing 1/2/3 estão no palco. **Ver-Capturas-Manny.cmd** abre a galeria completa sem servidor. Os inputs dos braços e o adaptador de escala ainda precisam de promoção ao runtime; armas/animações finais e câmara de gameplay continuam pendentes. Imagens, módulo editor e assets Manny ficam fora do ZIP runtime.

## Onde estão os ficheiros

| Local | Utilização |
| --- | --- |
| /Game/Sancta/VFX/Definitions | Definições, variantes e fases |
| /Game/Sancta/VFX/Skills, Combat, Status | Sistemas atuais por apresentação |
| /Game/Sancta/VFX/Common | Materiais, meshes, texturas e escalabilidade partilhados |
| /Game/Sancta/VFX/Terrain | Corpo Iceberg, colisão, integridade e remoção |
| /Game/Sancta/VFX/Review | Palcos de QA; ficam fora do runtime do jogo |
| Source/GameplayRuntime | Fontes editáveis dos derivados atuais |
| Source/MannyCalibration | Seis variantes locais de ligação/leitura no Manny; separadas do runtime atual |
| Evidence/gameplay-runtime-index.json | Índice gerado, cenas, assets e fases canónicas exatas |
| Evidence/gameplay-runtime-form-routes.json | Identidade canónica e snapshots da variante admitida |
| Evidence/RuntimeReview | Galeria, thumbnails, folhas e contraste/recursos |
| Plugins/SanctaVFXBridge/Source/SanctaVFXRuntime | Fonte do módulo local de apresentação |
| Exports/Sancta-VFX-Runtime.zip | Pacote de migração e documentação |

Hashes nos nomes conservam revisões. Usar o sistema/definição do índice atual, em vez de escolher um asset antigo pela semelhança do nome. O ZIP contém o plugin standalone **SanctaVFXRuntime**; o Bridge é ferramenta de authoring do laboratório.

## Próximos passos no jogo

1. Rever formas Glacial Spike/Iceberg e as novas apresentações no visualizador.
2. Calibrar armas/animações/notifies finais no Manny; promover os inputs independentes de braços/escala e conferir a câmara real.
3. Ligar GAS/abilities, autoridade e transporte de eventos, vida/respawn e replicação.
4. Ligar terreno, canais de colisão/navegação e ciclo de vida dos hosts.
5. Fazer cook Shipping e medir escalabilidade/overdraw/concorrência no hardware alvo.

Foundation continua protegido por instrução do utilizador. A migração ainda não foi aplicada nesse projeto. As 867 capturas, 94 casos Low/contraste/terreno e 27 de recursos/hold verificam o laboratório. A medição 0/1/16/48 cobre Arcane Weaving II no frame total do palco PIE; não é orçamento isolado de todos os efeitos.

## Índice dos componentes

Os números abaixo correspondem à ordem atual do visualizador. A versão HTML permite pesquisa e mostra detalhes de integração por componente.

### Básicos e ações

| Cena | Componente | Fase isolada | Owner |
| --- | --- | --- | --- |
| 289 | [BasicAttackBleedOverlay](Evidence/RuntimeReview/galeria.html#vfx-BasicAttackBleedOverlay) | Overlay | Alvo |
| 290 | [BasicAttackPoisonOverlay](Evidence/RuntimeReview/galeria.html#vfx-BasicAttackPoisonOverlay) | Overlay | Alvo |
| 6 | [BasicAxeMagicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicAxeMagicalTrail) | Trail | Caster / origem |
| 5 | [BasicAxePhysicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicAxePhysicalTrail) | Trail | Caster / origem |
| 35 | [BasicBowMagicalFlight](Evidence/RuntimeReview/galeria.html#vfx-BasicBowMagicalFlight) | Flight | Projétil real |
| 36 | [BasicBowMagicalRelease](Evidence/RuntimeReview/galeria.html#vfx-BasicBowMagicalRelease) | Release | Caster / origem |
| 33 | [BasicBowPhysicalFlight](Evidence/RuntimeReview/galeria.html#vfx-BasicBowPhysicalFlight) | Flight | Projétil real |
| 34 | [BasicBowPhysicalRelease](Evidence/RuntimeReview/galeria.html#vfx-BasicBowPhysicalRelease) | Release | Caster / origem |
| 8 | [BasicClubMagicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicClubMagicalTrail) | Trail | Caster / origem |
| 7 | [BasicClubPhysicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicClubPhysicalTrail) | Trail | Caster / origem |
| 27 | [BasicCrossbowMagicalFlight](Evidence/RuntimeReview/galeria.html#vfx-BasicCrossbowMagicalFlight) | Flight | Projétil real |
| 28 | [BasicCrossbowMagicalRelease](Evidence/RuntimeReview/galeria.html#vfx-BasicCrossbowMagicalRelease) | Release | Caster / origem |
| 25 | [BasicCrossbowPhysicalFlight](Evidence/RuntimeReview/galeria.html#vfx-BasicCrossbowPhysicalFlight) | Flight | Projétil real |
| 26 | [BasicCrossbowPhysicalRelease](Evidence/RuntimeReview/galeria.html#vfx-BasicCrossbowPhysicalRelease) | Release | Caster / origem |
| 16 | [BasicDualDaggersMagicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicDualDaggersMagicalTrail) | Trail | Caster / origem |
| 15 | [BasicDualDaggersPhysicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicDualDaggersPhysicalTrail) | Trail | Caster / origem |
| 18 | [BasicFistsGauntletsMagicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicFistsGauntletsMagicalTrail) | Trail | Caster / origem |
| 17 | [BasicFistsGauntletsPhysicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicFistsGauntletsPhysicalTrail) | Trail | Caster / origem |
| 32 | [BasicGreataxeMagicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicGreataxeMagicalTrail) | Trail | Caster / origem |
| 31 | [BasicGreataxePhysicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicGreataxePhysicalTrail) | Trail | Caster / origem |
| 20 | [BasicGreatClubMagicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicGreatClubMagicalTrail) | Trail | Caster / origem |
| 19 | [BasicGreatClubPhysicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicGreatClubPhysicalTrail) | Trail | Caster / origem |
| 30 | [BasicGreatswordMagicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicGreatswordMagicalTrail) | Trail | Caster / origem |
| 29 | [BasicGreatswordPhysicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicGreatswordPhysicalTrail) | Trail | Caster / origem |
| 14 | [BasicRapierMagicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicRapierMagicalTrail) | Trail | Caster / origem |
| 13 | [BasicRapierPhysicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicRapierPhysicalTrail) | Trail | Caster / origem |
| 38 | [BasicSpearMagicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicSpearMagicalTrail) | Trail | Caster / origem |
| 37 | [BasicSpearPhysicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicSpearPhysicalTrail) | Trail | Caster / origem |
| 23 | [BasicStaffMagicalFlight](Evidence/RuntimeReview/galeria.html#vfx-BasicStaffMagicalFlight) | Flight | Projétil real |
| 24 | [BasicStaffMagicalRelease](Evidence/RuntimeReview/galeria.html#vfx-BasicStaffMagicalRelease) | Release | Caster / origem |
| 21 | [BasicStaffPhysicalFlight](Evidence/RuntimeReview/galeria.html#vfx-BasicStaffPhysicalFlight) | Flight | Projétil real |
| 22 | [BasicStaffPhysicalRelease](Evidence/RuntimeReview/galeria.html#vfx-BasicStaffPhysicalRelease) | Release | Caster / origem |
| 4 | [BasicSwordMagicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicSwordMagicalTrail) | Trail | Caster / origem |
| 3 | [BasicSwordPhysicalTrail](Evidence/RuntimeReview/galeria.html#vfx-BasicSwordPhysicalTrail) | Trail | Caster / origem |
| 11 | [BasicWandMagicalFlight](Evidence/RuntimeReview/galeria.html#vfx-BasicWandMagicalFlight) | Flight | Projétil real |
| 12 | [BasicWandMagicalRelease](Evidence/RuntimeReview/galeria.html#vfx-BasicWandMagicalRelease) | Release | Caster / origem |
| 9 | [BasicWandPhysicalFlight](Evidence/RuntimeReview/galeria.html#vfx-BasicWandPhysicalFlight) | Flight | Projétil real |
| 10 | [BasicWandPhysicalRelease](Evidence/RuntimeReview/galeria.html#vfx-BasicWandPhysicalRelease) | Release | Caster / origem |
| 2 | [ContactMagical](Evidence/RuntimeReview/galeria.html#vfx-ContactMagical) | Impact | Ponto / área no mundo |
| 1 | [ContactPhysical](Evidence/RuntimeReview/galeria.html#vfx-ContactPhysical) | Impact | Ponto / área no mundo |
| 57 | [DodgeStart](Evidence/RuntimeReview/galeria.html#vfx-DodgeStart) | Start | Caster / origem |
| 58 | [DodgeAvoided](Evidence/RuntimeReview/galeria.html#vfx-DodgeAvoided) | Avoided | Caster / origem |
| 50 | [GuardActive](Evidence/RuntimeReview/galeria.html#vfx-GuardActive) | Active | Caster / origem |
| 51 | [GuardMitigation](Evidence/RuntimeReview/galeria.html#vfx-GuardMitigation) | Mitigation | Caster / origem |
| 52 | [GuardDepletion](Evidence/RuntimeReview/galeria.html#vfx-GuardDepletion) | Depletion | Caster / origem |
| 55 | [FootContactMud](Evidence/RuntimeReview/galeria.html#vfx-FootContactMud) | FootContact | Ponto / área no mundo |
| 54 | [FootContactSnow](Evidence/RuntimeReview/galeria.html#vfx-FootContactSnow) | FootContact | Ponto / área no mundo |
| 53 | [FootContactStone](Evidence/RuntimeReview/galeria.html#vfx-FootContactStone) | FootContact | Ponto / área no mundo |
| 56 | [FootContactWater](Evidence/RuntimeReview/galeria.html#vfx-FootContactWater) | FootContact | Ponto / área no mundo |

### Fighter

| Cena | Componente | Fase isolada | Owner |
| --- | --- | --- | --- |
| 188 | [BattlecryChallengeITankCast](Evidence/RuntimeReview/galeria.html#vfx-BattlecryChallengeITankCast) | Cast | Caster / origem |
| 189 | [BattlecryChallengeIWarriorCast](Evidence/RuntimeReview/galeria.html#vfx-BattlecryChallengeIWarriorCast) | Cast | Caster / origem |
| 117 | [ChallengeIIRootApply](Evidence/RuntimeReview/galeria.html#vfx-ChallengeIIRootApply) | Apply | Alvo |
| 190 | [BattlecryChallengeIiTankCast](Evidence/RuntimeReview/galeria.html#vfx-BattlecryChallengeIiTankCast) | Cast | Caster / origem |
| 191 | [BattlecryChallengeIiWarriorCast](Evidence/RuntimeReview/galeria.html#vfx-BattlecryChallengeIiWarriorCast) | Cast | Caster / origem |
| 192 | [BulwarkApply](Evidence/RuntimeReview/galeria.html#vfx-BulwarkApply) | Apply | Caster / origem |
| 105 | [ChainsIFlight](Evidence/RuntimeReview/galeria.html#vfx-ChainsIFlight) | Flight | Ligação entre duas pontas |
| 106 | [ChainsILatchedLink](Evidence/RuntimeReview/galeria.html#vfx-ChainsILatchedLink) | Active | Ligação entre duas pontas |
| 107 | [ChainsIHit](Evidence/RuntimeReview/galeria.html#vfx-ChainsIHit) | Impact | Alvo |
| 108 | [ChainsIEnd](Evidence/RuntimeReview/galeria.html#vfx-ChainsIEnd) | End | Ligação entre duas pontas |
| 109 | [ChainsIIFlight](Evidence/RuntimeReview/galeria.html#vfx-ChainsIIFlight) | Flight | Ligação entre duas pontas |
| 110 | [ChainsIILatchedLink](Evidence/RuntimeReview/galeria.html#vfx-ChainsIILatchedLink) | Active | Ligação entre duas pontas |
| 111 | [ChainsIIHit](Evidence/RuntimeReview/galeria.html#vfx-ChainsIIHit) | Impact | Alvo |
| 112 | [ChainsIIEnd](Evidence/RuntimeReview/galeria.html#vfx-ChainsIIEnd) | End | Ligação entre duas pontas |
| 113 | [ChainsIITargetWrap](Evidence/RuntimeReview/galeria.html#vfx-ChainsIITargetWrap) | Active | Alvo |
| 114 | [ChainsIIPull](Evidence/RuntimeReview/galeria.html#vfx-ChainsIIPull) | Recast | Ligação entre duas pontas |
| 115 | [ChainsIIInterrupt](Evidence/RuntimeReview/galeria.html#vfx-ChainsIIInterrupt) | Interrupt | Alvo |
| 193 | [CleanseApply](Evidence/RuntimeReview/galeria.html#vfx-CleanseApply) | Apply | Alvo |
| 81 | [SeveringMark1](Evidence/RuntimeReview/galeria.html#vfx-SeveringMark1) | Apply | Alvo |
| 82 | [SeveringMark2](Evidence/RuntimeReview/galeria.html#vfx-SeveringMark2) | Apply | Alvo |
| 83 | [SeveringMark3](Evidence/RuntimeReview/galeria.html#vfx-SeveringMark3) | Apply | Alvo |
| 194 | [CrushingBlowAreaImpact](Evidence/RuntimeReview/galeria.html#vfx-CrushingBlowAreaImpact) | AreaImpact | Ponto / área no mundo |
| 195 | [CrushingBlowIiAreaImpact](Evidence/RuntimeReview/galeria.html#vfx-CrushingBlowIiAreaImpact) | AreaImpact | Ponto / área no mundo |
| 196 | [DefiantPresenceActive](Evidence/RuntimeReview/galeria.html#vfx-DefiantPresenceActive) | Active | Ponto / área no mundo |
| 197 | [MomentumMasteryResourceGain](Evidence/RuntimeReview/galeria.html#vfx-MomentumMasteryResourceGain) | ResourceGain | Caster / origem |
| 198 | [PiercingStrikeCast](Evidence/RuntimeReview/galeria.html#vfx-PiercingStrikeCast) | Cast | Caster / origem |
| 199 | [PiercingStrikeImpact](Evidence/RuntimeReview/galeria.html#vfx-PiercingStrikeImpact) | Impact | Alvo |
| 200 | [PiercingStrikeIiTankCast](Evidence/RuntimeReview/galeria.html#vfx-PiercingStrikeIiTankCast) | Cast | Caster / origem |
| 201 | [PiercingStrikeIiTankImpact](Evidence/RuntimeReview/galeria.html#vfx-PiercingStrikeIiTankImpact) | Impact | Alvo |
| 202 | [PiercingStrikeIiWarriorCast](Evidence/RuntimeReview/galeria.html#vfx-PiercingStrikeIiWarriorCast) | Cast | Caster / origem |
| 203 | [PiercingStrikeIiWarriorImpact](Evidence/RuntimeReview/galeria.html#vfx-PiercingStrikeIiWarriorImpact) | Impact | Alvo |
| 204 | [PressureProvokeCast](Evidence/RuntimeReview/galeria.html#vfx-PressureProvokeCast) | Cast | Ligação entre duas pontas |
| 206 | [PressureProvokeImpact](Evidence/RuntimeReview/galeria.html#vfx-PressureProvokeImpact) | Impact | Ponto / área no mundo |
| 205 | [PressureProvokeTankCast](Evidence/RuntimeReview/galeria.html#vfx-PressureProvokeTankCast) | Cast | Ligação entre duas pontas |
| 207 | [PressureProvokeTankImpact](Evidence/RuntimeReview/galeria.html#vfx-PressureProvokeTankImpact) | Impact | Ponto / área no mundo |
| 208 | [RageApply](Evidence/RuntimeReview/galeria.html#vfx-RageApply) | Apply | Caster / origem |
| 118 | [RallyITankAffected](Evidence/RuntimeReview/galeria.html#vfx-RallyITankAffected) | Apply | Alvo |
| 209 | [RallyITankCast](Evidence/RuntimeReview/galeria.html#vfx-RallyITankCast) | Cast | Caster / origem |
| 119 | [RallyIWarriorAffected](Evidence/RuntimeReview/galeria.html#vfx-RallyIWarriorAffected) | Apply | Alvo |
| 210 | [RallyIWarriorCast](Evidence/RuntimeReview/galeria.html#vfx-RallyIWarriorCast) | Cast | Caster / origem |
| 120 | [RallyIiTankAffected](Evidence/RuntimeReview/galeria.html#vfx-RallyIiTankAffected) | Apply | Alvo |
| 211 | [RallyIiTankCast](Evidence/RuntimeReview/galeria.html#vfx-RallyIiTankCast) | Cast | Caster / origem |
| 121 | [RallyIiWarriorAffected](Evidence/RuntimeReview/galeria.html#vfx-RallyIiWarriorAffected) | Apply | Alvo |
| 212 | [RallyIiWarriorCast](Evidence/RuntimeReview/galeria.html#vfx-RallyIiWarriorCast) | Cast | Caster / origem |
| 213 | [SecondWindHeal](Evidence/RuntimeReview/galeria.html#vfx-SecondWindHeal) | Heal | Caster / origem |
| 84 | [SeveringCastI](Evidence/RuntimeReview/galeria.html#vfx-SeveringCastI) | Cast | Caster / origem |
| 85 | [SeveringCastII](Evidence/RuntimeReview/galeria.html#vfx-SeveringCastII) | Cast | Caster / origem |
| 86 | [SeveringCastIII](Evidence/RuntimeReview/galeria.html#vfx-SeveringCastIII) | Cast | Caster / origem |
| 214 | [ShoulderRushMovement](Evidence/RuntimeReview/galeria.html#vfx-ShoulderRushMovement) | Movement | Caster / origem |
| 215 | [ShoulderRushImpact](Evidence/RuntimeReview/galeria.html#vfx-ShoulderRushImpact) | Impact | Alvo |
| 216 | [ShoulderRushIiTankMovement](Evidence/RuntimeReview/galeria.html#vfx-ShoulderRushIiTankMovement) | Movement | Caster / origem |
| 217 | [ShoulderRushIiTankImpact](Evidence/RuntimeReview/galeria.html#vfx-ShoulderRushIiTankImpact) | Impact | Alvo |
| 218 | [ShoulderRushIiWarriorMovement](Evidence/RuntimeReview/galeria.html#vfx-ShoulderRushIiWarriorMovement) | Movement | Caster / origem |
| 219 | [ShoulderRushIiWarriorImpact](Evidence/RuntimeReview/galeria.html#vfx-ShoulderRushIiWarriorImpact) | Impact | Alvo |
| 220 | [TankStanceActive](Evidence/RuntimeReview/galeria.html#vfx-TankStanceActive) | Active | Caster / origem |
| 221 | [TankStanceCast](Evidence/RuntimeReview/galeria.html#vfx-TankStanceCast) | Cast | Caster / origem |
| 222 | [WarLeapMovement](Evidence/RuntimeReview/galeria.html#vfx-WarLeapMovement) | Movement | Caster / origem |
| 223 | [WarLeapAreaImpact](Evidence/RuntimeReview/galeria.html#vfx-WarLeapAreaImpact) | AreaImpact | Ponto / área no mundo |
| 224 | [WarLeapTelegraph](Evidence/RuntimeReview/galeria.html#vfx-WarLeapTelegraph) | Telegraph | Ponto / área no mundo |
| 225 | [WarriorStanceActive](Evidence/RuntimeReview/galeria.html#vfx-WarriorStanceActive) | Active | Caster / origem |
| 226 | [WarriorStanceCast](Evidence/RuntimeReview/galeria.html#vfx-WarriorStanceCast) | Cast | Caster / origem |

### Mage

| Cena | Componente | Fase isolada | Owner |
| --- | --- | --- | --- |
| 227 | [ArcaneBurstFlight](Evidence/RuntimeReview/galeria.html#vfx-ArcaneBurstFlight) | Flight | Projétil real |
| 228 | [ArcaneBurstProc](Evidence/RuntimeReview/galeria.html#vfx-ArcaneBurstProc) | Proc | Alvo |
| 166 | [ArcaneWeavingIResource](Evidence/RuntimeReview/galeria.html#vfx-ArcaneWeavingIResource) | Active | Caster / origem |
| 167 | [ArcaneWeavingIiResource](Evidence/RuntimeReview/galeria.html#vfx-ArcaneWeavingIiResource) | Active | Caster / origem |
| 229 | [BlinkProc](Evidence/RuntimeReview/galeria.html#vfx-BlinkProc) | Proc | Alvo |
| 230 | [BlinkCast](Evidence/RuntimeReview/galeria.html#vfx-BlinkCast) | Cast | Caster / origem |
| 231 | [CleansemageApply](Evidence/RuntimeReview/galeria.html#vfx-CleansemageApply) | Apply | Alvo |
| 149 | [CoilHit](Evidence/RuntimeReview/galeria.html#vfx-CoilHit) | Impact | Alvo |
| 150 | [CoilProc7](Evidence/RuntimeReview/galeria.html#vfx-CoilProc7) | Apply | Alvo |
| 151 | [CoilChain](Evidence/RuntimeReview/galeria.html#vfx-CoilChain) | Chain | Ligação entre duas pontas |
| 232 | [CoilCast](Evidence/RuntimeReview/galeria.html#vfx-CoilCast) | Cast | Caster / origem |
| 233 | [CombustIProc](Evidence/RuntimeReview/galeria.html#vfx-CombustIProc) | Proc | Alvo |
| 234 | [CombustIiProc](Evidence/RuntimeReview/galeria.html#vfx-CombustIiProc) | Proc | Alvo |
| 235 | [CombustIiAreaImpact](Evidence/RuntimeReview/galeria.html#vfx-CombustIiAreaImpact) | AreaImpact | Ponto / área no mundo |
| 168 | [ElementalWeaverIResource](Evidence/RuntimeReview/galeria.html#vfx-ElementalWeaverIResource) | Active | Caster / origem |
| 169 | [ElementalWeaverIiResource](Evidence/RuntimeReview/galeria.html#vfx-ElementalWeaverIiResource) | Active | Caster / origem |
| 87 | [FireBoltIFlight](Evidence/RuntimeReview/galeria.html#vfx-FireBoltIFlight) | Flight | Projétil real |
| 88 | [FireBoltIImpact](Evidence/RuntimeReview/galeria.html#vfx-FireBoltIImpact) | Impact | Alvo |
| 89 | [FireBoltIIFlight](Evidence/RuntimeReview/galeria.html#vfx-FireBoltIIFlight) | Flight | Projétil real |
| 90 | [FireBoltIIImpact](Evidence/RuntimeReview/galeria.html#vfx-FireBoltIIImpact) | Impact | Alvo |
| 116 | [FireBoltIISpread](Evidence/RuntimeReview/galeria.html#vfx-FireBoltIISpread) | Apply | Alvo |
| 123 | [FrostLanceIImpact](Evidence/RuntimeReview/galeria.html#vfx-FrostLanceIImpact) | Impact | Alvo |
| 236 | [FrostLanceIFlight](Evidence/RuntimeReview/galeria.html#vfx-FrostLanceIFlight) | Flight | Projétil real |
| 124 | [FrostLanceIiImpact](Evidence/RuntimeReview/galeria.html#vfx-FrostLanceIiImpact) | Impact | Alvo |
| 125 | [FrostLanceIiConditionalControl](Evidence/RuntimeReview/galeria.html#vfx-FrostLanceIiConditionalControl) | Apply | Alvo |
| 237 | [FrostLanceIiFlight](Evidence/RuntimeReview/galeria.html#vfx-FrostLanceIiFlight) | Flight | Projétil real |
| 126 | [GlacialSpikeIGroundArea](Evidence/RuntimeReview/galeria.html#vfx-GlacialSpikeIGroundArea) | AreaImpact | Ponto / área no mundo |
| 127 | [GlacialSpikeIImpact](Evidence/RuntimeReview/galeria.html#vfx-GlacialSpikeIImpact) | Impact | Alvo |
| 238 | [GlacialSpikeIAreaImpact](Evidence/RuntimeReview/galeria.html#vfx-GlacialSpikeIAreaImpact) | AreaImpact | Ponto / área no mundo |
| 128 | [GlacialSpikeIiGroundArea](Evidence/RuntimeReview/galeria.html#vfx-GlacialSpikeIiGroundArea) | AreaImpact | Ponto / área no mundo |
| 129 | [GlacialSpikeIiImpact](Evidence/RuntimeReview/galeria.html#vfx-GlacialSpikeIiImpact) | Impact | Alvo |
| 130 | [GlacialSpikeIiConditionalControl](Evidence/RuntimeReview/galeria.html#vfx-GlacialSpikeIiConditionalControl) | Apply | Alvo |
| 239 | [GlacialSpikeIiAreaImpact](Evidence/RuntimeReview/galeria.html#vfx-GlacialSpikeIiAreaImpact) | AreaImpact | Ponto / área no mundo |
| 240 | [IcebergFlight](Evidence/RuntimeReview/galeria.html#vfx-IcebergFlight) | Flight | Projétil real |
| 241 | [IcebergProc](Evidence/RuntimeReview/galeria.html#vfx-IcebergProc) | Proc | Alvo |
| 144 | [LaserContact](Evidence/RuntimeReview/galeria.html#vfx-LaserContact) | Impact | Alvo |
| 242 | [LaserActive](Evidence/RuntimeReview/galeria.html#vfx-LaserActive) | Active | Ligação entre duas pontas |
| 243 | [LaserCast](Evidence/RuntimeReview/galeria.html#vfx-LaserCast) | Cast | Caster / origem |
| 176 | [ManaBarrierIHold](Evidence/RuntimeReview/galeria.html#vfx-ManaBarrierIHold) | Hold | Caster / origem |
| 177 | [ManaBarrierIRelease](Evidence/RuntimeReview/galeria.html#vfx-ManaBarrierIRelease) | Release | Caster / origem |
| 178 | [ManaBarrierIiOverchargeHold](Evidence/RuntimeReview/galeria.html#vfx-ManaBarrierIiOverchargeHold) | Hold | Caster / origem |
| 179 | [ManaBarrierIiOverchargeRelease](Evidence/RuntimeReview/galeria.html#vfx-ManaBarrierIiOverchargeRelease) | Release | Caster / origem |
| 244 | [ManaStormActive](Evidence/RuntimeReview/galeria.html#vfx-ManaStormActive) | Active | Ponto / área no mundo |
| 245 | [ManifestActive](Evidence/RuntimeReview/galeria.html#vfx-ManifestActive) | Active | Caster / origem |
| 246 | [MistActive](Evidence/RuntimeReview/galeria.html#vfx-MistActive) | Active | Ponto / área no mundo |
| 145 | [StaticBoltIHit](Evidence/RuntimeReview/galeria.html#vfx-StaticBoltIHit) | Impact | Alvo |
| 146 | [StaticBoltIChain](Evidence/RuntimeReview/galeria.html#vfx-StaticBoltIChain) | Chain | Ligação entre duas pontas |
| 161 | [StaticBoltIGroundArea](Evidence/RuntimeReview/galeria.html#vfx-StaticBoltIGroundArea) | AreaImpact | Ponto / área no mundo |
| 247 | [StaticBoltIFlight](Evidence/RuntimeReview/galeria.html#vfx-StaticBoltIFlight) | Flight | Projétil real |
| 147 | [StaticBoltIiHit](Evidence/RuntimeReview/galeria.html#vfx-StaticBoltIiHit) | Impact | Alvo |
| 148 | [StaticBoltIiChain](Evidence/RuntimeReview/galeria.html#vfx-StaticBoltIiChain) | Chain | Ligação entre duas pontas |
| 162 | [StaticBoltIiGroundArea](Evidence/RuntimeReview/galeria.html#vfx-StaticBoltIiGroundArea) | AreaImpact | Ponto / área no mundo |
| 248 | [StaticBoltIiFlight](Evidence/RuntimeReview/galeria.html#vfx-StaticBoltIiFlight) | Flight | Projétil real |
| 154 | [TempestIce](Evidence/RuntimeReview/galeria.html#vfx-TempestIce) | Strike | Ponto / área no mundo |
| 155 | [TempestLightning](Evidence/RuntimeReview/galeria.html#vfx-TempestLightning) | Strike | Ponto / área no mundo |
| 156 | [TempestGroundImpact](Evidence/RuntimeReview/galeria.html#vfx-TempestGroundImpact) | AreaImpact | Ponto / área no mundo |
| 157 | [TempestFrostImpact](Evidence/RuntimeReview/galeria.html#vfx-TempestFrostImpact) | AreaImpact | Ponto / área no mundo |
| 158 | [TempestStormArea](Evidence/RuntimeReview/galeria.html#vfx-TempestStormArea) | Active | Ponto / área no mundo |
| 159 | [TempestTelegraph](Evidence/RuntimeReview/galeria.html#vfx-TempestTelegraph) | Telegraph | Ponto / área no mundo |
| 160 | [TempestLightningHit](Evidence/RuntimeReview/galeria.html#vfx-TempestLightningHit) | Impact | Alvo |
| 165 | [TempestSappedProc](Evidence/RuntimeReview/galeria.html#vfx-TempestSappedProc) | Apply | Alvo |
| 152 | [ThunderstrikeIHit](Evidence/RuntimeReview/galeria.html#vfx-ThunderstrikeIHit) | Impact | Alvo |
| 249 | [ThunderstrikeIStrike](Evidence/RuntimeReview/galeria.html#vfx-ThunderstrikeIStrike) | Strike | Ponto / área no mundo |
| 153 | [ThunderstrikeIiHit](Evidence/RuntimeReview/galeria.html#vfx-ThunderstrikeIiHit) | Impact | Alvo |
| 163 | [ThunderstrikeIiSplashArea](Evidence/RuntimeReview/galeria.html#vfx-ThunderstrikeIiSplashArea) | AreaImpact | Ponto / área no mundo |
| 164 | [ThunderstrikeIISplash](Evidence/RuntimeReview/galeria.html#vfx-ThunderstrikeIISplash) | Proc | Ponto / área no mundo |
| 250 | [ThunderstrikeIiStrike](Evidence/RuntimeReview/galeria.html#vfx-ThunderstrikeIiStrike) | Strike | Ponto / área no mundo |
| 251 | [VortexFlight](Evidence/RuntimeReview/galeria.html#vfx-VortexFlight) | Flight | Projétil real |
| 252 | [VortexDisplacement](Evidence/RuntimeReview/galeria.html#vfx-VortexDisplacement) | Displacement | Alvo |
| 253 | [WeaveCast](Evidence/RuntimeReview/galeria.html#vfx-WeaveCast) | Cast | Caster / origem |
| 254 | [WeaveActive](Evidence/RuntimeReview/galeria.html#vfx-WeaveActive) | Active | Caster / origem |

### Mystic

| Cena | Componente | Fase isolada | Owner |
| --- | --- | --- | --- |
| 255 | [AstralAuraMoonActive](Evidence/RuntimeReview/galeria.html#vfx-AstralAuraMoonActive) | Active | Caster / origem |
| 256 | [AstralAuraSunActive](Evidence/RuntimeReview/galeria.html#vfx-AstralAuraSunActive) | Active | Caster / origem |
| 257 | [AstralPullAreaImpact](Evidence/RuntimeReview/galeria.html#vfx-AstralPullAreaImpact) | AreaImpact | Ponto / área no mundo |
| 258 | [AstralPullRelocate](Evidence/RuntimeReview/galeria.html#vfx-AstralPullRelocate) | Relocate | Alvo |
| 259 | [AstralPullLink](Evidence/RuntimeReview/galeria.html#vfx-AstralPullLink) | Link | Ligação entre duas pontas |
| 260 | [AstralStepProc](Evidence/RuntimeReview/galeria.html#vfx-AstralStepProc) | Proc | Alvo |
| 261 | [AstralStepCast](Evidence/RuntimeReview/galeria.html#vfx-AstralStepCast) | Cast | Caster / origem |
| 262 | [AstralVeilActive](Evidence/RuntimeReview/galeria.html#vfx-AstralVeilActive) | Active | Ponto / área no mundo |
| 263 | [BlackHoleIActive](Evidence/RuntimeReview/galeria.html#vfx-BlackHoleIActive) | Active | Ponto / área no mundo |
| 264 | [BlackHoleIiActive](Evidence/RuntimeReview/galeria.html#vfx-BlackHoleIiActive) | Active | Ponto / área no mundo |
| 136 | [BrightStarShieldApply](Evidence/RuntimeReview/galeria.html#vfx-BrightStarShieldApply) | ShieldApply | Alvo |
| 137 | [BrightStarCasterProc](Evidence/RuntimeReview/galeria.html#vfx-BrightStarCasterProc) | Proc | Caster / origem |
| 265 | [BrightStarCast](Evidence/RuntimeReview/galeria.html#vfx-BrightStarCast) | Cast | Caster / origem |
| 266 | [CleansemysticApply](Evidence/RuntimeReview/galeria.html#vfx-CleansemysticApply) | Apply | Alvo |
| 180 | [ConnectionIAllyActive](Evidence/RuntimeReview/galeria.html#vfx-ConnectionIAllyActive) | Active | Ligação entre duas pontas |
| 181 | [ConnectionIAllyNaturalEnd](Evidence/RuntimeReview/galeria.html#vfx-ConnectionIAllyNaturalEnd) | NaturalEnd | Ligação entre duas pontas |
| 182 | [ConnectionIEnemyActive](Evidence/RuntimeReview/galeria.html#vfx-ConnectionIEnemyActive) | Active | Ligação entre duas pontas |
| 183 | [ConnectionIEnemyNaturalEnd](Evidence/RuntimeReview/galeria.html#vfx-ConnectionIEnemyNaturalEnd) | NaturalEnd | Ligação entre duas pontas |
| 184 | [ConnectionIiAllyActive](Evidence/RuntimeReview/galeria.html#vfx-ConnectionIiAllyActive) | Active | Ligação entre duas pontas |
| 185 | [ConnectionIiAllyNaturalEnd](Evidence/RuntimeReview/galeria.html#vfx-ConnectionIiAllyNaturalEnd) | NaturalEnd | Ligação entre duas pontas |
| 186 | [ConnectionIiEnemyActive](Evidence/RuntimeReview/galeria.html#vfx-ConnectionIiEnemyActive) | Active | Ligação entre duas pontas |
| 187 | [ConnectionIiEnemyNaturalEnd](Evidence/RuntimeReview/galeria.html#vfx-ConnectionIiEnemyNaturalEnd) | NaturalEnd | Ligação entre duas pontas |
| 43 | [CosmicRayIDelivery](Evidence/RuntimeReview/galeria.html#vfx-CosmicRayIDelivery) | Flight | Projétil real |
| 267 | [CosmicRayIPending](Evidence/RuntimeReview/galeria.html#vfx-CosmicRayIPending) | Pending | Alvo |
| 268 | [CosmicRayIResolve](Evidence/RuntimeReview/galeria.html#vfx-CosmicRayIResolve) | Resolve | Alvo |
| 44 | [CosmicRayIIDelivery](Evidence/RuntimeReview/galeria.html#vfx-CosmicRayIIDelivery) | Flight | Projétil real |
| 269 | [CosmicRayIiPending](Evidence/RuntimeReview/galeria.html#vfx-CosmicRayIiPending) | Pending | Alvo |
| 270 | [CosmicRayIiResolve](Evidence/RuntimeReview/galeria.html#vfx-CosmicRayIiResolve) | Resolve | Alvo |
| 271 | [EclipseAreaImpact](Evidence/RuntimeReview/galeria.html#vfx-EclipseAreaImpact) | AreaImpact | Ponto / área no mundo |
| 131 | [EtherIAllyHeal](Evidence/RuntimeReview/galeria.html#vfx-EtherIAllyHeal) | Heal | Alvo |
| 272 | [EtherIAllyFlight](Evidence/RuntimeReview/galeria.html#vfx-EtherIAllyFlight) | Flight | Projétil real |
| 132 | [EtherIEnemyConfirmedDamage](Evidence/RuntimeReview/galeria.html#vfx-EtherIEnemyConfirmedDamage) | Impact | Alvo |
| 273 | [EtherIEnemyFlight](Evidence/RuntimeReview/galeria.html#vfx-EtherIEnemyFlight) | Flight | Projétil real |
| 133 | [EtherIiAllyHeal](Evidence/RuntimeReview/galeria.html#vfx-EtherIiAllyHeal) | Heal | Alvo |
| 134 | [EtherIiAllyConditionalBuff](Evidence/RuntimeReview/galeria.html#vfx-EtherIiAllyConditionalBuff) | Apply | Alvo |
| 274 | [EtherIiAllyFlight](Evidence/RuntimeReview/galeria.html#vfx-EtherIiAllyFlight) | Flight | Projétil real |
| 135 | [EtherIiEnemyConfirmedDamage](Evidence/RuntimeReview/galeria.html#vfx-EtherIiEnemyConfirmedDamage) | Impact | Alvo |
| 275 | [EtherIiEnemyFlight](Evidence/RuntimeReview/galeria.html#vfx-EtherIiEnemyFlight) | Flight | Projétil real |
| 42 | [FullMoonDelivery](Evidence/RuntimeReview/galeria.html#vfx-FullMoonDelivery) | Flight | Projétil real |
| 276 | [FullMoonAreaImpact](Evidence/RuntimeReview/galeria.html#vfx-FullMoonAreaImpact) | AreaImpact | Ponto / área no mundo |
| 277 | [LullabyFlight](Evidence/RuntimeReview/galeria.html#vfx-LullabyFlight) | Flight | Projétil real |
| 278 | [LullabyProc](Evidence/RuntimeReview/galeria.html#vfx-LullabyProc) | Proc | Alvo |
| 279 | [LullabyIiNightmareFlight](Evidence/RuntimeReview/galeria.html#vfx-LullabyIiNightmareFlight) | Flight | Projétil real |
| 280 | [LullabyIiNightmareProc](Evidence/RuntimeReview/galeria.html#vfx-LullabyIiNightmareProc) | Proc | Alvo |
| 281 | [MoonStanceCast](Evidence/RuntimeReview/galeria.html#vfx-MoonStanceCast) | Cast | Caster / origem |
| 282 | [MoonStanceActive](Evidence/RuntimeReview/galeria.html#vfx-MoonStanceActive) | Active | Caster / origem |
| 122 | [ResurrectComplete](Evidence/RuntimeReview/galeria.html#vfx-ResurrectComplete) | Complete | Alvo |
| 283 | [ResurrectHold](Evidence/RuntimeReview/galeria.html#vfx-ResurrectHold) | Hold | Alvo |
| 138 | [SerenityHeal](Evidence/RuntimeReview/galeria.html#vfx-SerenityHeal) | Heal | Alvo |
| 139 | [SerenitySleepApply](Evidence/RuntimeReview/galeria.html#vfx-SerenitySleepApply) | Apply | Alvo |
| 170 | [SpiritOfTheCometMoonState](Evidence/RuntimeReview/galeria.html#vfx-SpiritOfTheCometMoonState) | Active | Alvo |
| 171 | [SpiritOfTheCometSunState](Evidence/RuntimeReview/galeria.html#vfx-SpiritOfTheCometSunState) | Active | Alvo |
| 172 | [SpiritOfTheOrbitMoonState](Evidence/RuntimeReview/galeria.html#vfx-SpiritOfTheOrbitMoonState) | Active | Alvo |
| 173 | [SpiritOfTheOrbitSunState](Evidence/RuntimeReview/galeria.html#vfx-SpiritOfTheOrbitSunState) | Active | Alvo |
| 174 | [SpiritOfTheStarMoonState](Evidence/RuntimeReview/galeria.html#vfx-SpiritOfTheStarMoonState) | Active | Alvo |
| 175 | [SpiritOfTheStarSunState](Evidence/RuntimeReview/galeria.html#vfx-SpiritOfTheStarSunState) | Active | Alvo |
| 284 | [SunStanceCast](Evidence/RuntimeReview/galeria.html#vfx-SunStanceCast) | Cast | Caster / origem |
| 285 | [SunStanceActive](Evidence/RuntimeReview/galeria.html#vfx-SunStanceActive) | Active | Caster / origem |

### Scout

| Cena | Componente | Fase isolada | Owner |
| --- | --- | --- | --- |
| 286 | [BackstabFlight](Evidence/RuntimeReview/galeria.html#vfx-BackstabFlight) | Flight | Projétil real |
| 287 | [BackstabImpact](Evidence/RuntimeReview/galeria.html#vfx-BackstabImpact) | Impact | Alvo |
| 140 | [BackstabIIConfirmedHit](Evidence/RuntimeReview/galeria.html#vfx-BackstabIIConfirmedHit) | Impact | Alvo |
| 141 | [BackstabIIStunApply](Evidence/RuntimeReview/galeria.html#vfx-BackstabIIStunApply) | Apply | Alvo |
| 142 | [BackstabIIPoisonApply](Evidence/RuntimeReview/galeria.html#vfx-BackstabIIPoisonApply) | Apply | Alvo |
| 143 | [BackstabIIBleedApply](Evidence/RuntimeReview/galeria.html#vfx-BackstabIIBleedApply) | Apply | Alvo |
| 288 | [BackstabIiFlight](Evidence/RuntimeReview/galeria.html#vfx-BackstabIiFlight) | Flight | Projétil real |
| 291 | [BleedStanceActive](Evidence/RuntimeReview/galeria.html#vfx-BleedStanceActive) | Active | Ligação entre duas pontas |
| 292 | [BlindingDartFlight](Evidence/RuntimeReview/galeria.html#vfx-BlindingDartFlight) | Flight | Projétil real |
| 293 | [BlindingDartImpact](Evidence/RuntimeReview/galeria.html#vfx-BlindingDartImpact) | Impact | Alvo |
| 294 | [BlindingDartProc](Evidence/RuntimeReview/galeria.html#vfx-BlindingDartProc) | Proc | Alvo |
| 295 | [CleansescoutApply](Evidence/RuntimeReview/galeria.html#vfx-CleansescoutApply) | Apply | Alvo |
| 296 | [EvasionProc](Evidence/RuntimeReview/galeria.html#vfx-EvasionProc) | Proc | Caster / origem |
| 39 | [ExploitIDelivery](Evidence/RuntimeReview/galeria.html#vfx-ExploitIDelivery) | Flight | Projétil real |
| 297 | [ExploitWeaknessIImpact](Evidence/RuntimeReview/galeria.html#vfx-ExploitWeaknessIImpact) | Impact | Alvo |
| 298 | [ExploitWeaknessIProc](Evidence/RuntimeReview/galeria.html#vfx-ExploitWeaknessIProc) | Proc | Alvo |
| 40 | [ExploitIIDelivery](Evidence/RuntimeReview/galeria.html#vfx-ExploitIIDelivery) | Flight | Projétil real |
| 299 | [ExploitWeaknessIiImpact](Evidence/RuntimeReview/galeria.html#vfx-ExploitWeaknessIiImpact) | Impact | Alvo |
| 300 | [ExploitWeaknessIiProc](Evidence/RuntimeReview/galeria.html#vfx-ExploitWeaknessIiProc) | Proc | Alvo |
| 41 | [ExploitIIIDelivery](Evidence/RuntimeReview/galeria.html#vfx-ExploitIIIDelivery) | Flight | Projétil real |
| 301 | [ExploitWeaknessIiiImpact](Evidence/RuntimeReview/galeria.html#vfx-ExploitWeaknessIiiImpact) | Impact | Alvo |
| 302 | [ExploitWeaknessIiiProc](Evidence/RuntimeReview/galeria.html#vfx-ExploitWeaknessIiiProc) | Proc | Alvo |
| 303 | [HemorrhagePayoff](Evidence/RuntimeReview/galeria.html#vfx-HemorrhagePayoff) | Payoff | Alvo |
| 304 | [HemorrhageConsume](Evidence/RuntimeReview/galeria.html#vfx-HemorrhageConsume) | Consume | Alvo |
| 305 | [LongJumpHold](Evidence/RuntimeReview/galeria.html#vfx-LongJumpHold) | Hold | Ligação entre duas pontas |
| 306 | [LongJumpTelegraph](Evidence/RuntimeReview/galeria.html#vfx-LongJumpTelegraph) | Telegraph | Ponto / área no mundo |
| 307 | [LongJumpMovement](Evidence/RuntimeReview/galeria.html#vfx-LongJumpMovement) | Movement | Caster / origem |
| 308 | [PoisonSacFlight](Evidence/RuntimeReview/galeria.html#vfx-PoisonSacFlight) | Flight | Projétil real |
| 309 | [PoisonSacImpact](Evidence/RuntimeReview/galeria.html#vfx-PoisonSacImpact) | Impact | Alvo |
| 310 | [PoisonSacActive](Evidence/RuntimeReview/galeria.html#vfx-PoisonSacActive) | Active | Ponto / área no mundo |
| 311 | [PoisonSacConsume](Evidence/RuntimeReview/galeria.html#vfx-PoisonSacConsume) | Consume | Alvo |
| 312 | [PoisonStanceActive](Evidence/RuntimeReview/galeria.html#vfx-PoisonStanceActive) | Active | Ligação entre duas pontas |
| 313 | [QuickstepIMovement](Evidence/RuntimeReview/galeria.html#vfx-QuickstepIMovement) | Movement | Caster / origem |
| 314 | [QuickstepIiMovement](Evidence/RuntimeReview/galeria.html#vfx-QuickstepIiMovement) | Movement | Caster / origem |
| 315 | [RapidAttackCast](Evidence/RuntimeReview/galeria.html#vfx-RapidAttackCast) | Cast | Caster / origem |
| 316 | [SandShotCast](Evidence/RuntimeReview/galeria.html#vfx-SandShotCast) | Cast | Ponto / área no mundo |
| 317 | [SandShotImpact](Evidence/RuntimeReview/galeria.html#vfx-SandShotImpact) | Impact | Ponto / área no mundo |
| 45 | [SicknessDelivery](Evidence/RuntimeReview/galeria.html#vfx-SicknessDelivery) | Flight | Projétil real |
| 318 | [SicknessImpact](Evidence/RuntimeReview/galeria.html#vfx-SicknessImpact) | Impact | Alvo |
| 319 | [SicknessAreaImpact](Evidence/RuntimeReview/galeria.html#vfx-SicknessAreaImpact) | AreaImpact | Ponto / área no mundo |
| 320 | [SicknessConsume](Evidence/RuntimeReview/galeria.html#vfx-SicknessConsume) | Consume | Alvo |
| 321 | [SmokeBombIFlight](Evidence/RuntimeReview/galeria.html#vfx-SmokeBombIFlight) | Flight | Projétil real |
| 322 | [SmokeBombIAreaImpact](Evidence/RuntimeReview/galeria.html#vfx-SmokeBombIAreaImpact) | AreaImpact | Ponto / área no mundo |
| 323 | [SmokeBombIActive](Evidence/RuntimeReview/galeria.html#vfx-SmokeBombIActive) | Active | Ponto / área no mundo |
| 324 | [SmokeBombIiFlight](Evidence/RuntimeReview/galeria.html#vfx-SmokeBombIiFlight) | Flight | Projétil real |
| 325 | [SmokeBombIiAreaImpact](Evidence/RuntimeReview/galeria.html#vfx-SmokeBombIiAreaImpact) | AreaImpact | Ponto / área no mundo |
| 326 | [SmokeBombIiActive](Evidence/RuntimeReview/galeria.html#vfx-SmokeBombIiActive) | Active | Ponto / área no mundo |
| 327 | [TorporFlight](Evidence/RuntimeReview/galeria.html#vfx-TorporFlight) | Flight | Projétil real |
| 328 | [TorporImpact](Evidence/RuntimeReview/galeria.html#vfx-TorporImpact) | Impact | Alvo |
| 329 | [TorporProc](Evidence/RuntimeReview/galeria.html#vfx-TorporProc) | Proc | Alvo |
| 330 | [VineFieldIActive](Evidence/RuntimeReview/galeria.html#vfx-VineFieldIActive) | Active | Ponto / área no mundo |
| 331 | [VineFieldIiActive](Evidence/RuntimeReview/galeria.html#vfx-VineFieldIiActive) | Active | Ponto / área no mundo |
| 91 | [VolleyIBleedFlight](Evidence/RuntimeReview/galeria.html#vfx-VolleyIBleedFlight) | Flight | Projétil real |
| 92 | [VolleyIBleedHit](Evidence/RuntimeReview/galeria.html#vfx-VolleyIBleedHit) | Impact | Alvo |
| 93 | [VolleyIPoisonFlight](Evidence/RuntimeReview/galeria.html#vfx-VolleyIPoisonFlight) | Flight | Projétil real |
| 94 | [VolleyIPoisonHit](Evidence/RuntimeReview/galeria.html#vfx-VolleyIPoisonHit) | Impact | Alvo |
| 95 | [VolleyIIBleedFanFlight](Evidence/RuntimeReview/galeria.html#vfx-VolleyIIBleedFanFlight) | Flight | Projétil real |
| 96 | [VolleyIIBleedHit](Evidence/RuntimeReview/galeria.html#vfx-VolleyIIBleedHit) | Impact | Alvo |
| 97 | [VolleyIIBleedPiercingFlight](Evidence/RuntimeReview/galeria.html#vfx-VolleyIIBleedPiercingFlight) | Flight | Projétil real |
| 98 | [VolleyIIBleedAim](Evidence/RuntimeReview/galeria.html#vfx-VolleyIIBleedAim) | Hold | Caster / origem |
| 99 | [VolleyIIBleedAimEnd](Evidence/RuntimeReview/galeria.html#vfx-VolleyIIBleedAimEnd) | End | Caster / origem |
| 100 | [VolleyIIPoisonFanFlight](Evidence/RuntimeReview/galeria.html#vfx-VolleyIIPoisonFanFlight) | Flight | Projétil real |
| 101 | [VolleyIIPoisonHit](Evidence/RuntimeReview/galeria.html#vfx-VolleyIIPoisonHit) | Impact | Alvo |
| 102 | [VolleyIIPoisonPiercingFlight](Evidence/RuntimeReview/galeria.html#vfx-VolleyIIPoisonPiercingFlight) | Flight | Projétil real |
| 103 | [VolleyIIPoisonAim](Evidence/RuntimeReview/galeria.html#vfx-VolleyIIPoisonAim) | Hold | Caster / origem |
| 104 | [VolleyIIPoisonAimEnd](Evidence/RuntimeReview/galeria.html#vfx-VolleyIIPoisonAimEnd) | End | Caster / origem |

### Estados e CC

| Cena | Componente | Fase isolada | Owner |
| --- | --- | --- | --- |
| 71 | [CCFearActive](Evidence/RuntimeReview/galeria.html#vfx-CCFearActive) | Active | Alvo |
| 73 | [CCFearCleanse](Evidence/RuntimeReview/galeria.html#vfx-CCFearCleanse) | Cleanse | Alvo |
| 72 | [CCFearNaturalEnd](Evidence/RuntimeReview/galeria.html#vfx-CCFearNaturalEnd) | NaturalEnd | Alvo |
| 79 | [CCForcedPull](Evidence/RuntimeReview/galeria.html#vfx-CCForcedPull) | Apply | Alvo |
| 78 | [CCForcedPush](Evidence/RuntimeReview/galeria.html#vfx-CCForcedPush) | Apply | Alvo |
| 80 | [CCForcedSlowPull](Evidence/RuntimeReview/galeria.html#vfx-CCForcedSlowPull) | Apply | Alvo |
| 65 | [CCSilenceActive](Evidence/RuntimeReview/galeria.html#vfx-CCSilenceActive) | Active | Alvo |
| 67 | [CCSilenceCleanse](Evidence/RuntimeReview/galeria.html#vfx-CCSilenceCleanse) | Cleanse | Alvo |
| 66 | [CCSilenceNaturalEnd](Evidence/RuntimeReview/galeria.html#vfx-CCSilenceNaturalEnd) | NaturalEnd | Alvo |
| 62 | [CCSleepActive](Evidence/RuntimeReview/galeria.html#vfx-CCSleepActive) | Active | Alvo |
| 64 | [CCSleepCleanse](Evidence/RuntimeReview/galeria.html#vfx-CCSleepCleanse) | Cleanse | Alvo |
| 63 | [CCSleepNaturalEnd](Evidence/RuntimeReview/galeria.html#vfx-CCSleepNaturalEnd) | NaturalEnd | Alvo |
| 59 | [CCStunActive](Evidence/RuntimeReview/galeria.html#vfx-CCStunActive) | Active | Alvo |
| 61 | [CCStunCleanse](Evidence/RuntimeReview/galeria.html#vfx-CCStunCleanse) | Cleanse | Alvo |
| 60 | [CCStunNaturalEnd](Evidence/RuntimeReview/galeria.html#vfx-CCStunNaturalEnd) | NaturalEnd | Alvo |
| 68 | [CCTauntActive](Evidence/RuntimeReview/galeria.html#vfx-CCTauntActive) | Active | Alvo |
| 77 | [CCTauntApply](Evidence/RuntimeReview/galeria.html#vfx-CCTauntApply) | Apply | Alvo |
| 70 | [CCTauntCleanse](Evidence/RuntimeReview/galeria.html#vfx-CCTauntCleanse) | Cleanse | Alvo |
| 69 | [CCTauntNaturalEnd](Evidence/RuntimeReview/galeria.html#vfx-CCTauntNaturalEnd) | NaturalEnd | Alvo |
| 74 | [CCRootActive](Evidence/RuntimeReview/galeria.html#vfx-CCRootActive) | Active | Alvo |
| 75 | [CCRootNaturalEnd](Evidence/RuntimeReview/galeria.html#vfx-CCRootNaturalEnd) | NaturalEnd | Alvo |
| 76 | [CCRootCleanse](Evidence/RuntimeReview/galeria.html#vfx-CCRootCleanse) | Cleanse | Alvo |
| 46 | [CCDisarmActive](Evidence/RuntimeReview/galeria.html#vfx-CCDisarmActive) | Active | Alvo |
| 47 | [CCDisarmApply](Evidence/RuntimeReview/galeria.html#vfx-CCDisarmApply) | Apply | Alvo |
| 48 | [CCDisarmNaturalEnd](Evidence/RuntimeReview/galeria.html#vfx-CCDisarmNaturalEnd) | NaturalEnd | Alvo |
| 49 | [CCDisarmCleanse](Evidence/RuntimeReview/galeria.html#vfx-CCDisarmCleanse) | Cleanse | Alvo |
