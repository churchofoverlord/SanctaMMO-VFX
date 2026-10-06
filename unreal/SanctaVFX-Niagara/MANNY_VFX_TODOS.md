# Manny — índice completo dos VFX

**331 componentes / 340 cenários.** Capturas auditadas deste catálogo: **340/340**. O estado detalhado está em `Evidence/gameplay-manny-full-validation.json`; aprovação de produção e integração no jogo continuam pendentes.

Presença medida em **4044/4080 pares**; **138 flags de diagnóstico** de tamanho, margem/enquadramento ou oclusão. Cada cenário tem de ter uma representação visível para passar a auditoria. Isso não certifica todas as poses/vistas nem qualidade final de gameplay.

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
| 1 | [Bleed — mão direita ao cotovelo](Evidence/MannyFullReview/galeria.html#BleedRight) | `BleedStanceActive` | Active | hand_elbow |
| 2 | [Bleed — mão esquerda ao cotovelo](Evidence/MannyFullReview/galeria.html#BleedLeft) | `BleedStanceActive` | Active | hand_elbow |
| 3 | [Poison — mão direita ao cotovelo](Evidence/MannyFullReview/galeria.html#PoisonRight) | `PoisonStanceActive` | Active | hand_elbow |
| 4 | [Poison — mão esquerda ao cotovelo](Evidence/MannyFullReview/galeria.html#PoisonLeft) | `PoisonStanceActive` | Active | hand_elbow |
| 5 | [Bleed — ambos os braços](Evidence/MannyFullReview/galeria.html#BleedBoth) | `BleedStanceActive` | Active | both_arms |
| 6 | [Poison — ambos os braços](Evidence/MannyFullReview/galeria.html#PoisonBoth) | `PoisonStanceActive` | Active | both_arms |
| 7 | [Rapid Attack — raios pelos dois braços](Evidence/MannyFullReview/galeria.html#RapidBoth) | `RapidAttackCast` | Cast | both_arms |
| 8 | [Espada física — haste de calibração](Evidence/MannyFullReview/galeria.html#SwordPhysical) | `BasicSwordPhysicalTrail` | Trail | weapon |
| 9 | [Espada mágica — haste de calibração](Evidence/MannyFullReview/galeria.html#SwordMagical) | `BasicSwordMagicalTrail` | Trail | weapon |
| 10 | [Guard — alinhamento no tronco](Evidence/MannyFullReview/galeria.html#Guard) | `GuardActive` | Active | chest |
| 11 | [Tank Stance — cintura](Evidence/MannyFullReview/galeria.html#Tank) | `TankStanceActive` | Active | waist |
| 12 | [Warrior Stance — cintura](Evidence/MannyFullReview/galeria.html#Warrior) | `WarriorStanceActive` | Active | waist |
| 13 | [Stun — acima da cabeça do alvo](Evidence/MannyFullReview/galeria.html#Stun) | `CCStunActive` | Active | head |
| 14 | [Root — pés do alvo](Evidence/MannyFullReview/galeria.html#Root) | `CCRootActive` | Active | target_root |
| 15 | [Severing — marca no tronco do alvo](Evidence/MannyFullReview/galeria.html#SeveringMark) | `SeveringMark1` | Apply | target_chest |
| 16 | [Severing — duas marcas no tronco](Evidence/MannyFullReview/galeria.html#SeveringMark2) | `SeveringMark2` | Apply | target_chest |
| 17 | [Severing — terceira marca no tronco](Evidence/MannyFullReview/galeria.html#SeveringMark3) | `SeveringMark3` | Apply | target_chest |
| 18 | [Laser — mão ao tronco do alvo](Evidence/MannyFullReview/galeria.html#LaserBeam) | `LaserActive` | Active | beam |
| 19 | [Laser — origem na mão](Evidence/MannyFullReview/galeria.html#LaserCast) | `LaserCast` | Cast | cast_hand |
| 20 | [Contacto do pé — pedra](Evidence/MannyFullReview/galeria.html#FootStone) | `FootContactStone` | FootContact | foot |
| 21 | [Arcane Weaving II — recurso no corpo](Evidence/MannyFullReview/galeria.html#ArcaneResource) | `ArcaneWeavingIiResource` | Active | root |
| 22 | [Contact Physical](Evidence/MannyFullReview/galeria.html#ContactPhysical) | `ContactPhysical` | Impact | target_contact |
| 23 | [Contact Magical](Evidence/MannyFullReview/galeria.html#ContactMagical) | `ContactMagical` | Impact | target_contact |
| 24 | [Basic Axe Physical Trail](Evidence/MannyFullReview/galeria.html#BasicAxePhysicalTrail) | `BasicAxePhysicalTrail` | Trail | weapon |
| 25 | [Basic Axe Magical Trail](Evidence/MannyFullReview/galeria.html#BasicAxeMagicalTrail) | `BasicAxeMagicalTrail` | Trail | weapon |
| 26 | [Basic Club Physical Trail](Evidence/MannyFullReview/galeria.html#BasicClubPhysicalTrail) | `BasicClubPhysicalTrail` | Trail | weapon |
| 27 | [Basic Club Magical Trail](Evidence/MannyFullReview/galeria.html#BasicClubMagicalTrail) | `BasicClubMagicalTrail` | Trail | weapon |
| 28 | [Basic Wand Physical Flight](Evidence/MannyFullReview/galeria.html#BasicWandPhysicalFlight) | `BasicWandPhysicalFlight` | Flight | projectile |
| 29 | [Basic Wand Physical Release](Evidence/MannyFullReview/galeria.html#BasicWandPhysicalRelease) | `BasicWandPhysicalRelease` | Release | weapon_muzzle |
| 30 | [Basic Wand Magical Flight](Evidence/MannyFullReview/galeria.html#BasicWandMagicalFlight) | `BasicWandMagicalFlight` | Flight | projectile |
| 31 | [Basic Wand Magical Release](Evidence/MannyFullReview/galeria.html#BasicWandMagicalRelease) | `BasicWandMagicalRelease` | Release | weapon_muzzle |
| 32 | [Basic Rapier Physical Trail](Evidence/MannyFullReview/galeria.html#BasicRapierPhysicalTrail) | `BasicRapierPhysicalTrail` | Trail | weapon |
| 33 | [Basic Rapier Magical Trail](Evidence/MannyFullReview/galeria.html#BasicRapierMagicalTrail) | `BasicRapierMagicalTrail` | Trail | weapon |
| 34 | [Basic Dual Daggers Physical Trail](Evidence/MannyFullReview/galeria.html#BasicDualDaggersPhysicalTrail) | `BasicDualDaggersPhysicalTrail` | Trail | weapon |
| 35 | [Basic Dual Daggers Magical Trail](Evidence/MannyFullReview/galeria.html#BasicDualDaggersMagicalTrail) | `BasicDualDaggersMagicalTrail` | Trail | weapon |
| 36 | [Basic Fists Gauntlets Physical Trail](Evidence/MannyFullReview/galeria.html#BasicFistsGauntletsPhysicalTrail) | `BasicFistsGauntletsPhysicalTrail` | Trail | weapon |
| 37 | [Basic Fists Gauntlets Magical Trail](Evidence/MannyFullReview/galeria.html#BasicFistsGauntletsMagicalTrail) | `BasicFistsGauntletsMagicalTrail` | Trail | weapon |
| 38 | [Basic Great Club Physical Trail](Evidence/MannyFullReview/galeria.html#BasicGreatClubPhysicalTrail) | `BasicGreatClubPhysicalTrail` | Trail | weapon |
| 39 | [Basic Great Club Magical Trail](Evidence/MannyFullReview/galeria.html#BasicGreatClubMagicalTrail) | `BasicGreatClubMagicalTrail` | Trail | weapon |
| 40 | [Basic Staff Physical Flight](Evidence/MannyFullReview/galeria.html#BasicStaffPhysicalFlight) | `BasicStaffPhysicalFlight` | Flight | projectile |
| 41 | [Basic Staff Physical Release](Evidence/MannyFullReview/galeria.html#BasicStaffPhysicalRelease) | `BasicStaffPhysicalRelease` | Release | weapon_muzzle |
| 42 | [Basic Staff Magical Flight](Evidence/MannyFullReview/galeria.html#BasicStaffMagicalFlight) | `BasicStaffMagicalFlight` | Flight | projectile |
| 43 | [Basic Staff Magical Release](Evidence/MannyFullReview/galeria.html#BasicStaffMagicalRelease) | `BasicStaffMagicalRelease` | Release | weapon_muzzle |
| 44 | [Basic Crossbow Physical Flight](Evidence/MannyFullReview/galeria.html#BasicCrossbowPhysicalFlight) | `BasicCrossbowPhysicalFlight` | Flight | projectile |
| 45 | [Basic Crossbow Physical Release](Evidence/MannyFullReview/galeria.html#BasicCrossbowPhysicalRelease) | `BasicCrossbowPhysicalRelease` | Release | weapon_muzzle |
| 46 | [Basic Crossbow Magical Flight](Evidence/MannyFullReview/galeria.html#BasicCrossbowMagicalFlight) | `BasicCrossbowMagicalFlight` | Flight | projectile |
| 47 | [Basic Crossbow Magical Release](Evidence/MannyFullReview/galeria.html#BasicCrossbowMagicalRelease) | `BasicCrossbowMagicalRelease` | Release | weapon_muzzle |
| 48 | [Basic Greatsword Physical Trail](Evidence/MannyFullReview/galeria.html#BasicGreatswordPhysicalTrail) | `BasicGreatswordPhysicalTrail` | Trail | weapon |
| 49 | [Basic Greatsword Magical Trail](Evidence/MannyFullReview/galeria.html#BasicGreatswordMagicalTrail) | `BasicGreatswordMagicalTrail` | Trail | weapon |
| 50 | [Basic Greataxe Physical Trail](Evidence/MannyFullReview/galeria.html#BasicGreataxePhysicalTrail) | `BasicGreataxePhysicalTrail` | Trail | weapon |
| 51 | [Basic Greataxe Magical Trail](Evidence/MannyFullReview/galeria.html#BasicGreataxeMagicalTrail) | `BasicGreataxeMagicalTrail` | Trail | weapon |
| 52 | [Basic Bow Physical Flight](Evidence/MannyFullReview/galeria.html#BasicBowPhysicalFlight) | `BasicBowPhysicalFlight` | Flight | projectile |
| 53 | [Basic Bow Physical Release](Evidence/MannyFullReview/galeria.html#BasicBowPhysicalRelease) | `BasicBowPhysicalRelease` | Release | weapon_muzzle |
| 54 | [Basic Bow Magical Flight](Evidence/MannyFullReview/galeria.html#BasicBowMagicalFlight) | `BasicBowMagicalFlight` | Flight | projectile |
| 55 | [Basic Bow Magical Release](Evidence/MannyFullReview/galeria.html#BasicBowMagicalRelease) | `BasicBowMagicalRelease` | Release | weapon_muzzle |
| 56 | [Basic Spear Physical Trail](Evidence/MannyFullReview/galeria.html#BasicSpearPhysicalTrail) | `BasicSpearPhysicalTrail` | Trail | weapon |
| 57 | [Basic Spear Magical Trail](Evidence/MannyFullReview/galeria.html#BasicSpearMagicalTrail) | `BasicSpearMagicalTrail` | Trail | weapon |
| 58 | [Exploit I Delivery](Evidence/MannyFullReview/galeria.html#ExploitIDelivery) | `ExploitIDelivery` | Flight | projectile |
| 59 | [Exploit II Delivery](Evidence/MannyFullReview/galeria.html#ExploitIIDelivery) | `ExploitIIDelivery` | Flight | projectile |
| 60 | [Exploit III Delivery](Evidence/MannyFullReview/galeria.html#ExploitIIIDelivery) | `ExploitIIIDelivery` | Flight | projectile |
| 61 | [Full Moon Delivery](Evidence/MannyFullReview/galeria.html#FullMoonDelivery) | `FullMoonDelivery` | Flight | projectile |
| 62 | [Cosmic Ray I Delivery](Evidence/MannyFullReview/galeria.html#CosmicRayIDelivery) | `CosmicRayIDelivery` | Flight | projectile |
| 63 | [Cosmic Ray II Delivery](Evidence/MannyFullReview/galeria.html#CosmicRayIIDelivery) | `CosmicRayIIDelivery` | Flight | projectile |
| 64 | [Sickness Delivery](Evidence/MannyFullReview/galeria.html#SicknessDelivery) | `SicknessDelivery` | Flight | projectile |
| 65 | [CC Disarm Active](Evidence/MannyFullReview/galeria.html#CCDisarmActive) | `CCDisarmActive` | Active | head |
| 66 | [CC Disarm Apply](Evidence/MannyFullReview/galeria.html#CCDisarmApply) | `CCDisarmApply` | Apply | head |
| 67 | [CC Disarm Natural End](Evidence/MannyFullReview/galeria.html#CCDisarmNaturalEnd) | `CCDisarmNaturalEnd` | NaturalEnd | head |
| 68 | [CC Disarm Cleanse](Evidence/MannyFullReview/galeria.html#CCDisarmCleanse) | `CCDisarmCleanse` | Cleanse | head |
| 69 | [Guard Mitigation](Evidence/MannyFullReview/galeria.html#GuardMitigation) | `GuardMitigation` | Mitigation | chest |
| 70 | [Guard Depletion](Evidence/MannyFullReview/galeria.html#GuardDepletion) | `GuardDepletion` | Depletion | chest |
| 71 | [Foot Contact Snow](Evidence/MannyFullReview/galeria.html#FootContactSnow) | `FootContactSnow` | FootContact | foot |
| 72 | [Foot Contact Mud](Evidence/MannyFullReview/galeria.html#FootContactMud) | `FootContactMud` | FootContact | foot |
| 73 | [Foot Contact Water](Evidence/MannyFullReview/galeria.html#FootContactWater) | `FootContactWater` | FootContact | foot |
| 74 | [Dodge Start](Evidence/MannyFullReview/galeria.html#DodgeStart) | `DodgeStart` | Start | root |
| 75 | [Dodge Avoided](Evidence/MannyFullReview/galeria.html#DodgeAvoided) | `DodgeAvoided` | Avoided | chest |
| 76 | [CC Stun Natural End](Evidence/MannyFullReview/galeria.html#CCStunNaturalEnd) | `CCStunNaturalEnd` | NaturalEnd | head |
| 77 | [CC Stun Cleanse](Evidence/MannyFullReview/galeria.html#CCStunCleanse) | `CCStunCleanse` | Cleanse | head |
| 78 | [CC Sleep Active](Evidence/MannyFullReview/galeria.html#CCSleepActive) | `CCSleepActive` | Active | head |
| 79 | [CC Sleep Natural End](Evidence/MannyFullReview/galeria.html#CCSleepNaturalEnd) | `CCSleepNaturalEnd` | NaturalEnd | head |
| 80 | [CC Sleep Cleanse](Evidence/MannyFullReview/galeria.html#CCSleepCleanse) | `CCSleepCleanse` | Cleanse | head |
| 81 | [CC Silence Active](Evidence/MannyFullReview/galeria.html#CCSilenceActive) | `CCSilenceActive` | Active | head |
| 82 | [CC Silence Natural End](Evidence/MannyFullReview/galeria.html#CCSilenceNaturalEnd) | `CCSilenceNaturalEnd` | NaturalEnd | head |
| 83 | [CC Silence Cleanse](Evidence/MannyFullReview/galeria.html#CCSilenceCleanse) | `CCSilenceCleanse` | Cleanse | head |
| 84 | [CC Taunt Active](Evidence/MannyFullReview/galeria.html#CCTauntActive) | `CCTauntActive` | Active | head |
| 85 | [CC Taunt Natural End](Evidence/MannyFullReview/galeria.html#CCTauntNaturalEnd) | `CCTauntNaturalEnd` | NaturalEnd | head |
| 86 | [CC Taunt Cleanse](Evidence/MannyFullReview/galeria.html#CCTauntCleanse) | `CCTauntCleanse` | Cleanse | head |
| 87 | [CC Fear Active](Evidence/MannyFullReview/galeria.html#CCFearActive) | `CCFearActive` | Active | head |
| 88 | [CC Fear Natural End](Evidence/MannyFullReview/galeria.html#CCFearNaturalEnd) | `CCFearNaturalEnd` | NaturalEnd | head |
| 89 | [CC Fear Cleanse](Evidence/MannyFullReview/galeria.html#CCFearCleanse) | `CCFearCleanse` | Cleanse | head |
| 90 | [CC Root Natural End](Evidence/MannyFullReview/galeria.html#CCRootNaturalEnd) | `CCRootNaturalEnd` | NaturalEnd | target_root |
| 91 | [CC Root Cleanse](Evidence/MannyFullReview/galeria.html#CCRootCleanse) | `CCRootCleanse` | Cleanse | target_root |
| 92 | [CC Taunt Apply](Evidence/MannyFullReview/galeria.html#CCTauntApply) | `CCTauntApply` | Apply | head |
| 93 | [CC Forced Push](Evidence/MannyFullReview/galeria.html#CCForcedPush) | `CCForcedPush` | Apply | target_root |
| 94 | [CC Forced Pull](Evidence/MannyFullReview/galeria.html#CCForcedPull) | `CCForcedPull` | Apply | target_root |
| 95 | [CC Forced Slow Pull](Evidence/MannyFullReview/galeria.html#CCForcedSlowPull) | `CCForcedSlowPull` | Apply | target_root |
| 96 | [Severing Cast I](Evidence/MannyFullReview/galeria.html#SeveringCastI) | `SeveringCastI` | Cast | source_body |
| 97 | [Severing Cast II](Evidence/MannyFullReview/galeria.html#SeveringCastII) | `SeveringCastII` | Cast | source_body |
| 98 | [Severing Cast III](Evidence/MannyFullReview/galeria.html#SeveringCastIII) | `SeveringCastIII` | Cast | source_body |
| 99 | [Fire Bolt I Flight](Evidence/MannyFullReview/galeria.html#FireBoltIFlight) | `FireBoltIFlight` | Flight | projectile |
| 100 | [Fire Bolt I Impact](Evidence/MannyFullReview/galeria.html#FireBoltIImpact) | `FireBoltIImpact` | Impact | target_root |
| 101 | [Fire Bolt II Flight](Evidence/MannyFullReview/galeria.html#FireBoltIIFlight) | `FireBoltIIFlight` | Flight | projectile |
| 102 | [Fire Bolt II Impact](Evidence/MannyFullReview/galeria.html#FireBoltIIImpact) | `FireBoltIIImpact` | Impact | target_root |
| 103 | [Volley I Bleed Flight](Evidence/MannyFullReview/galeria.html#VolleyIBleedFlight) | `VolleyIBleedFlight` | Flight | projectile |
| 104 | [Volley I Bleed Hit](Evidence/MannyFullReview/galeria.html#VolleyIBleedHit) | `VolleyIBleedHit` | Impact | target_body |
| 105 | [Volley I Poison Flight](Evidence/MannyFullReview/galeria.html#VolleyIPoisonFlight) | `VolleyIPoisonFlight` | Flight | projectile |
| 106 | [Volley I Poison Hit](Evidence/MannyFullReview/galeria.html#VolleyIPoisonHit) | `VolleyIPoisonHit` | Impact | target_body |
| 107 | [Volley II Bleed Fan Flight](Evidence/MannyFullReview/galeria.html#VolleyIIBleedFanFlight) | `VolleyIIBleedFanFlight` | Flight | projectile |
| 108 | [Volley II Bleed Hit](Evidence/MannyFullReview/galeria.html#VolleyIIBleedHit) | `VolleyIIBleedHit` | Impact | target_body |
| 109 | [Volley II Bleed Piercing Flight](Evidence/MannyFullReview/galeria.html#VolleyIIBleedPiercingFlight) | `VolleyIIBleedPiercingFlight` | Flight | projectile |
| 110 | [Volley II Bleed Aim](Evidence/MannyFullReview/galeria.html#VolleyIIBleedAim) | `VolleyIIBleedAim` | Hold | root |
| 111 | [Volley II Bleed Aim End](Evidence/MannyFullReview/galeria.html#VolleyIIBleedAimEnd) | `VolleyIIBleedAimEnd` | End | root |
| 112 | [Volley II Poison Fan Flight](Evidence/MannyFullReview/galeria.html#VolleyIIPoisonFanFlight) | `VolleyIIPoisonFanFlight` | Flight | projectile |
| 113 | [Volley II Poison Hit](Evidence/MannyFullReview/galeria.html#VolleyIIPoisonHit) | `VolleyIIPoisonHit` | Impact | target_body |
| 114 | [Volley II Poison Piercing Flight](Evidence/MannyFullReview/galeria.html#VolleyIIPoisonPiercingFlight) | `VolleyIIPoisonPiercingFlight` | Flight | projectile |
| 115 | [Volley II Poison Aim](Evidence/MannyFullReview/galeria.html#VolleyIIPoisonAim) | `VolleyIIPoisonAim` | Hold | root |
| 116 | [Volley II Poison Aim End](Evidence/MannyFullReview/galeria.html#VolleyIIPoisonAimEnd) | `VolleyIIPoisonAimEnd` | End | root |
| 117 | [Chains I Flight](Evidence/MannyFullReview/galeria.html#ChainsIFlight) | `ChainsIFlight` | Flight | beam |
| 118 | [Chains I Latched Link](Evidence/MannyFullReview/galeria.html#ChainsILatchedLink) | `ChainsILatchedLink` | Active | beam |
| 119 | [Chains I Hit](Evidence/MannyFullReview/galeria.html#ChainsIHit) | `ChainsIHit` | Impact | target_root |
| 120 | [Chains I End](Evidence/MannyFullReview/galeria.html#ChainsIEnd) | `ChainsIEnd` | End | beam |
| 121 | [Chains II Flight](Evidence/MannyFullReview/galeria.html#ChainsIIFlight) | `ChainsIIFlight` | Flight | beam |
| 122 | [Chains II Latched Link](Evidence/MannyFullReview/galeria.html#ChainsIILatchedLink) | `ChainsIILatchedLink` | Active | beam |
| 123 | [Chains II Hit](Evidence/MannyFullReview/galeria.html#ChainsIIHit) | `ChainsIIHit` | Impact | target_root |
| 124 | [Chains II End](Evidence/MannyFullReview/galeria.html#ChainsIIEnd) | `ChainsIIEnd` | End | beam |
| 125 | [Chains II Target Wrap](Evidence/MannyFullReview/galeria.html#ChainsIITargetWrap) | `ChainsIITargetWrap` | Active | target_root |
| 126 | [Chains II Pull](Evidence/MannyFullReview/galeria.html#ChainsIIPull) | `ChainsIIPull` | Recast | beam |
| 127 | [Chains II Interrupt](Evidence/MannyFullReview/galeria.html#ChainsIIInterrupt) | `ChainsIIInterrupt` | Interrupt | target_root |
| 128 | [Fire Bolt II Spread](Evidence/MannyFullReview/galeria.html#FireBoltIISpread) | `FireBoltIISpread` | Apply | target_body |
| 129 | [Challenge II Root Apply](Evidence/MannyFullReview/galeria.html#ChallengeIIRootApply) | `ChallengeIIRootApply` | Apply | target_root |
| 130 | [Rally I Tank Affected](Evidence/MannyFullReview/galeria.html#RallyITankAffected) | `RallyITankAffected` | Apply | target_root |
| 131 | [Rally I Warrior Affected](Evidence/MannyFullReview/galeria.html#RallyIWarriorAffected) | `RallyIWarriorAffected` | Apply | target_root |
| 132 | [Rally II Tank Affected](Evidence/MannyFullReview/galeria.html#RallyIiTankAffected) | `RallyIiTankAffected` | Apply | target_root |
| 133 | [Rally II Warrior Affected](Evidence/MannyFullReview/galeria.html#RallyIiWarriorAffected) | `RallyIiWarriorAffected` | Apply | target_root |
| 134 | [Resurrect Complete](Evidence/MannyFullReview/galeria.html#ResurrectComplete) | `ResurrectComplete` | Complete | target_root |
| 135 | [Frost Lance I Impact](Evidence/MannyFullReview/galeria.html#FrostLanceIImpact) | `FrostLanceIImpact` | Impact | target_root |
| 136 | [Frost Lance II Impact](Evidence/MannyFullReview/galeria.html#FrostLanceIiImpact) | `FrostLanceIiImpact` | Impact | target_root |
| 137 | [Frost Lance II Conditional Control](Evidence/MannyFullReview/galeria.html#FrostLanceIiConditionalControl) | `FrostLanceIiConditionalControl` | Apply | target_root |
| 138 | [Glacial Spike I Ground Area](Evidence/MannyFullReview/galeria.html#GlacialSpikeIGroundArea) | `GlacialSpikeIGroundArea` | AreaImpact | world |
| 139 | [Glacial Spike I Impact](Evidence/MannyFullReview/galeria.html#GlacialSpikeIImpact) | `GlacialSpikeIImpact` | Impact | target_root |
| 140 | [Glacial Spike II Ground Area](Evidence/MannyFullReview/galeria.html#GlacialSpikeIiGroundArea) | `GlacialSpikeIiGroundArea` | AreaImpact | world |
| 141 | [Glacial Spike II Impact](Evidence/MannyFullReview/galeria.html#GlacialSpikeIiImpact) | `GlacialSpikeIiImpact` | Impact | target_root |
| 142 | [Glacial Spike II Conditional Control](Evidence/MannyFullReview/galeria.html#GlacialSpikeIiConditionalControl) | `GlacialSpikeIiConditionalControl` | Apply | target_root |
| 143 | [Ether I Ally Heal](Evidence/MannyFullReview/galeria.html#EtherIAllyHeal) | `EtherIAllyHeal` | Heal | target_root |
| 144 | [Ether I Enemy Confirmed Damage](Evidence/MannyFullReview/galeria.html#EtherIEnemyConfirmedDamage) | `EtherIEnemyConfirmedDamage` | Impact | target_root |
| 145 | [Ether II Ally Heal](Evidence/MannyFullReview/galeria.html#EtherIiAllyHeal) | `EtherIiAllyHeal` | Heal | target_root |
| 146 | [Ether II Ally Conditional Buff](Evidence/MannyFullReview/galeria.html#EtherIiAllyConditionalBuff) | `EtherIiAllyConditionalBuff` | Apply | target_root |
| 147 | [Ether II Enemy Confirmed Damage](Evidence/MannyFullReview/galeria.html#EtherIiEnemyConfirmedDamage) | `EtherIiEnemyConfirmedDamage` | Impact | target_root |
| 148 | [Bright Star Shield Apply](Evidence/MannyFullReview/galeria.html#BrightStarShieldApply) | `BrightStarShieldApply` | ShieldApply | target_body |
| 149 | [Bright Star Caster Proc](Evidence/MannyFullReview/galeria.html#BrightStarCasterProc) | `BrightStarCasterProc` | Proc | root |
| 150 | [Serenity Heal](Evidence/MannyFullReview/galeria.html#SerenityHeal) | `SerenityHeal` | Heal | target_root |
| 151 | [Serenity Sleep Apply](Evidence/MannyFullReview/galeria.html#SerenitySleepApply) | `SerenitySleepApply` | Apply | target_root |
| 152 | [Backstab II Confirmed Hit](Evidence/MannyFullReview/galeria.html#BackstabIIConfirmedHit) | `BackstabIIConfirmedHit` | Impact | target_root |
| 153 | [Backstab II Stun Apply](Evidence/MannyFullReview/galeria.html#BackstabIIStunApply) | `BackstabIIStunApply` | Apply | target_root |
| 154 | [Backstab II Poison Apply](Evidence/MannyFullReview/galeria.html#BackstabIIPoisonApply) | `BackstabIIPoisonApply` | Apply | target_root |
| 155 | [Backstab II Bleed Apply](Evidence/MannyFullReview/galeria.html#BackstabIIBleedApply) | `BackstabIIBleedApply` | Apply | target_root |
| 156 | [Laser Contact](Evidence/MannyFullReview/galeria.html#LaserContact) | `LaserContact` | Impact | target_root |
| 157 | [Static Bolt I Hit](Evidence/MannyFullReview/galeria.html#StaticBoltIHit) | `StaticBoltIHit` | Impact | target_root |
| 158 | [Static Bolt I Chain](Evidence/MannyFullReview/galeria.html#StaticBoltIChain) | `StaticBoltIChain` | Chain | beam |
| 159 | [Static Bolt II Hit](Evidence/MannyFullReview/galeria.html#StaticBoltIiHit) | `StaticBoltIiHit` | Impact | target_root |
| 160 | [Static Bolt II Chain](Evidence/MannyFullReview/galeria.html#StaticBoltIiChain) | `StaticBoltIiChain` | Chain | beam |
| 161 | [Coil Hit](Evidence/MannyFullReview/galeria.html#CoilHit) | `CoilHit` | Impact | target_root |
| 162 | [Coil Proc7](Evidence/MannyFullReview/galeria.html#CoilProc7) | `CoilProc7` | Apply | target_root |
| 163 | [Coil Chain](Evidence/MannyFullReview/galeria.html#CoilChain) | `CoilChain` | Chain | beam |
| 164 | [Thunderstrike I Hit](Evidence/MannyFullReview/galeria.html#ThunderstrikeIHit) | `ThunderstrikeIHit` | Impact | target_root |
| 165 | [Thunderstrike II Hit](Evidence/MannyFullReview/galeria.html#ThunderstrikeIiHit) | `ThunderstrikeIiHit` | Impact | target_root |
| 166 | [Tempest Ice](Evidence/MannyFullReview/galeria.html#TempestIce) | `TempestIce` | Strike | world |
| 167 | [Tempest Lightning](Evidence/MannyFullReview/galeria.html#TempestLightning) | `TempestLightning` | Strike | world |
| 168 | [Tempest Ground Impact](Evidence/MannyFullReview/galeria.html#TempestGroundImpact) | `TempestGroundImpact` | AreaImpact | world |
| 169 | [Tempest Frost Impact](Evidence/MannyFullReview/galeria.html#TempestFrostImpact) | `TempestFrostImpact` | AreaImpact | world |
| 170 | [Tempest Storm Area](Evidence/MannyFullReview/galeria.html#TempestStormArea) | `TempestStormArea` | Active | world |
| 171 | [Tempest Telegraph](Evidence/MannyFullReview/galeria.html#TempestTelegraph) | `TempestTelegraph` | Telegraph | world |
| 172 | [Tempest Lightning Hit](Evidence/MannyFullReview/galeria.html#TempestLightningHit) | `TempestLightningHit` | Impact | target_root |
| 173 | [Static Bolt I Ground Area](Evidence/MannyFullReview/galeria.html#StaticBoltIGroundArea) | `StaticBoltIGroundArea` | AreaImpact | world |
| 174 | [Static Bolt II Ground Area](Evidence/MannyFullReview/galeria.html#StaticBoltIiGroundArea) | `StaticBoltIiGroundArea` | AreaImpact | world |
| 175 | [Thunderstrike II Splash Area](Evidence/MannyFullReview/galeria.html#ThunderstrikeIiSplashArea) | `ThunderstrikeIiSplashArea` | AreaImpact | world |
| 176 | [Thunderstrike II Splash](Evidence/MannyFullReview/galeria.html#ThunderstrikeIISplash) | `ThunderstrikeIISplash` | Proc | world |
| 177 | [Tempest Sapped Proc](Evidence/MannyFullReview/galeria.html#TempestSappedProc) | `TempestSappedProc` | Apply | target_root |
| 178 | [Arcane Weaving I Resource](Evidence/MannyFullReview/galeria.html#ArcaneWeavingIResource) | `ArcaneWeavingIResource` | Active | root |
| 179 | [Elemental Weaver I Resource](Evidence/MannyFullReview/galeria.html#ElementalWeaverIResource) | `ElementalWeaverIResource` | Active | root |
| 180 | [Elemental Weaver II Resource](Evidence/MannyFullReview/galeria.html#ElementalWeaverIiResource) | `ElementalWeaverIiResource` | Active | root |
| 181 | [Spirit Of The Comet Moon State](Evidence/MannyFullReview/galeria.html#SpiritOfTheCometMoonState) | `SpiritOfTheCometMoonState` | Active | target_body |
| 182 | [Spirit Of The Comet Sun State](Evidence/MannyFullReview/galeria.html#SpiritOfTheCometSunState) | `SpiritOfTheCometSunState` | Active | target_body |
| 183 | [Spirit Of The Orbit Moon State](Evidence/MannyFullReview/galeria.html#SpiritOfTheOrbitMoonState) | `SpiritOfTheOrbitMoonState` | Active | target_body |
| 184 | [Spirit Of The Orbit Sun State](Evidence/MannyFullReview/galeria.html#SpiritOfTheOrbitSunState) | `SpiritOfTheOrbitSunState` | Active | target_body |
| 185 | [Spirit Of The Star Moon State](Evidence/MannyFullReview/galeria.html#SpiritOfTheStarMoonState) | `SpiritOfTheStarMoonState` | Active | target_body |
| 186 | [Spirit Of The Star Sun State](Evidence/MannyFullReview/galeria.html#SpiritOfTheStarSunState) | `SpiritOfTheStarSunState` | Active | target_body |
| 187 | [Mana Barrier I Hold](Evidence/MannyFullReview/galeria.html#ManaBarrierIHold) | `ManaBarrierIHold` | Hold | root |
| 188 | [Mana Barrier I Release](Evidence/MannyFullReview/galeria.html#ManaBarrierIRelease) | `ManaBarrierIRelease` | Release | source_body |
| 189 | [Mana Barrier II Overcharge Hold](Evidence/MannyFullReview/galeria.html#ManaBarrierIiOverchargeHold) | `ManaBarrierIiOverchargeHold` | Hold | root |
| 190 | [Mana Barrier II Overcharge Release](Evidence/MannyFullReview/galeria.html#ManaBarrierIiOverchargeRelease) | `ManaBarrierIiOverchargeRelease` | Release | source_body |
| 191 | [Connection I Ally Active](Evidence/MannyFullReview/galeria.html#ConnectionIAllyActive) | `ConnectionIAllyActive` | Active | beam |
| 192 | [Connection I Ally Natural End](Evidence/MannyFullReview/galeria.html#ConnectionIAllyNaturalEnd) | `ConnectionIAllyNaturalEnd` | NaturalEnd | beam |
| 193 | [Connection I Enemy Active](Evidence/MannyFullReview/galeria.html#ConnectionIEnemyActive) | `ConnectionIEnemyActive` | Active | beam |
| 194 | [Connection I Enemy Natural End](Evidence/MannyFullReview/galeria.html#ConnectionIEnemyNaturalEnd) | `ConnectionIEnemyNaturalEnd` | NaturalEnd | beam |
| 195 | [Connection II Ally Active](Evidence/MannyFullReview/galeria.html#ConnectionIiAllyActive) | `ConnectionIiAllyActive` | Active | beam |
| 196 | [Connection II Ally Natural End](Evidence/MannyFullReview/galeria.html#ConnectionIiAllyNaturalEnd) | `ConnectionIiAllyNaturalEnd` | NaturalEnd | beam |
| 197 | [Connection II Enemy Active](Evidence/MannyFullReview/galeria.html#ConnectionIiEnemyActive) | `ConnectionIiEnemyActive` | Active | beam |
| 198 | [Connection II Enemy Natural End](Evidence/MannyFullReview/galeria.html#ConnectionIiEnemyNaturalEnd) | `ConnectionIiEnemyNaturalEnd` | NaturalEnd | beam |
| 199 | [Battlecry Challenge I Tank Cast](Evidence/MannyFullReview/galeria.html#BattlecryChallengeITankCast) | `BattlecryChallengeITankCast` | Cast | root |
| 200 | [Battlecry Challenge I Warrior Cast](Evidence/MannyFullReview/galeria.html#BattlecryChallengeIWarriorCast) | `BattlecryChallengeIWarriorCast` | Cast | root |
| 201 | [Battlecry Challenge II Tank Cast](Evidence/MannyFullReview/galeria.html#BattlecryChallengeIiTankCast) | `BattlecryChallengeIiTankCast` | Cast | root |
| 202 | [Battlecry Challenge II Warrior Cast](Evidence/MannyFullReview/galeria.html#BattlecryChallengeIiWarriorCast) | `BattlecryChallengeIiWarriorCast` | Cast | root |
| 203 | [Bulwark Apply](Evidence/MannyFullReview/galeria.html#BulwarkApply) | `BulwarkApply` | Apply | waist |
| 204 | [Cleanse Apply](Evidence/MannyFullReview/galeria.html#CleanseApply) | `CleanseApply` | Apply | target_body |
| 205 | [Crushing Blow Area Impact](Evidence/MannyFullReview/galeria.html#CrushingBlowAreaImpact) | `CrushingBlowAreaImpact` | AreaImpact | world |
| 206 | [Crushing Blow II Area Impact](Evidence/MannyFullReview/galeria.html#CrushingBlowIiAreaImpact) | `CrushingBlowIiAreaImpact` | AreaImpact | world |
| 207 | [Defiant Presence Active](Evidence/MannyFullReview/galeria.html#DefiantPresenceActive) | `DefiantPresenceActive` | Active | world |
| 208 | [Momentum Mastery Resource Gain](Evidence/MannyFullReview/galeria.html#MomentumMasteryResourceGain) | `MomentumMasteryResourceGain` | ResourceGain | source_body |
| 209 | [Piercing Strike Cast](Evidence/MannyFullReview/galeria.html#PiercingStrikeCast) | `PiercingStrikeCast` | Cast | source_body |
| 210 | [Piercing Strike Impact](Evidence/MannyFullReview/galeria.html#PiercingStrikeImpact) | `PiercingStrikeImpact` | Impact | target_root |
| 211 | [Piercing Strike II Tank Cast](Evidence/MannyFullReview/galeria.html#PiercingStrikeIiTankCast) | `PiercingStrikeIiTankCast` | Cast | source_body |
| 212 | [Piercing Strike II Tank Impact](Evidence/MannyFullReview/galeria.html#PiercingStrikeIiTankImpact) | `PiercingStrikeIiTankImpact` | Impact | target_root |
| 213 | [Piercing Strike II Warrior Cast](Evidence/MannyFullReview/galeria.html#PiercingStrikeIiWarriorCast) | `PiercingStrikeIiWarriorCast` | Cast | source_body |
| 214 | [Piercing Strike II Warrior Impact](Evidence/MannyFullReview/galeria.html#PiercingStrikeIiWarriorImpact) | `PiercingStrikeIiWarriorImpact` | Impact | target_root |
| 215 | [Pressure Provoke Cast](Evidence/MannyFullReview/galeria.html#PressureProvokeCast) | `PressureProvokeCast` | Cast | beam |
| 216 | [Pressure Provoke Tank Cast](Evidence/MannyFullReview/galeria.html#PressureProvokeTankCast) | `PressureProvokeTankCast` | Cast | beam |
| 217 | [Pressure Provoke Impact](Evidence/MannyFullReview/galeria.html#PressureProvokeImpact) | `PressureProvokeImpact` | Impact | target_contact |
| 218 | [Pressure Provoke Tank Impact](Evidence/MannyFullReview/galeria.html#PressureProvokeTankImpact) | `PressureProvokeTankImpact` | Impact | target_contact |
| 219 | [Rage Apply](Evidence/MannyFullReview/galeria.html#RageApply) | `RageApply` | Apply | waist |
| 220 | [Rally I Tank Cast](Evidence/MannyFullReview/galeria.html#RallyITankCast) | `RallyITankCast` | Cast | root |
| 221 | [Rally I Warrior Cast](Evidence/MannyFullReview/galeria.html#RallyIWarriorCast) | `RallyIWarriorCast` | Cast | root |
| 222 | [Rally II Tank Cast](Evidence/MannyFullReview/galeria.html#RallyIiTankCast) | `RallyIiTankCast` | Cast | root |
| 223 | [Rally II Warrior Cast](Evidence/MannyFullReview/galeria.html#RallyIiWarriorCast) | `RallyIiWarriorCast` | Cast | root |
| 224 | [Second Wind Heal](Evidence/MannyFullReview/galeria.html#SecondWindHeal) | `SecondWindHeal` | Heal | source_body |
| 225 | [Shoulder Rush Movement](Evidence/MannyFullReview/galeria.html#ShoulderRushMovement) | `ShoulderRushMovement` | Movement | root |
| 226 | [Shoulder Rush Impact](Evidence/MannyFullReview/galeria.html#ShoulderRushImpact) | `ShoulderRushImpact` | Impact | target_root |
| 227 | [Shoulder Rush II Tank Movement](Evidence/MannyFullReview/galeria.html#ShoulderRushIiTankMovement) | `ShoulderRushIiTankMovement` | Movement | root |
| 228 | [Shoulder Rush II Tank Impact](Evidence/MannyFullReview/galeria.html#ShoulderRushIiTankImpact) | `ShoulderRushIiTankImpact` | Impact | target_root |
| 229 | [Shoulder Rush II Warrior Movement](Evidence/MannyFullReview/galeria.html#ShoulderRushIiWarriorMovement) | `ShoulderRushIiWarriorMovement` | Movement | root |
| 230 | [Shoulder Rush II Warrior Impact](Evidence/MannyFullReview/galeria.html#ShoulderRushIiWarriorImpact) | `ShoulderRushIiWarriorImpact` | Impact | target_root |
| 231 | [Tank Stance Cast](Evidence/MannyFullReview/galeria.html#TankStanceCast) | `TankStanceCast` | Cast | waist |
| 232 | [War Leap Movement](Evidence/MannyFullReview/galeria.html#WarLeapMovement) | `WarLeapMovement` | Movement | root |
| 233 | [War Leap Area Impact](Evidence/MannyFullReview/galeria.html#WarLeapAreaImpact) | `WarLeapAreaImpact` | AreaImpact | world |
| 234 | [War Leap Telegraph](Evidence/MannyFullReview/galeria.html#WarLeapTelegraph) | `WarLeapTelegraph` | Telegraph | world |
| 235 | [Warrior Stance Cast](Evidence/MannyFullReview/galeria.html#WarriorStanceCast) | `WarriorStanceCast` | Cast | waist |
| 236 | [Arcane Burst Flight](Evidence/MannyFullReview/galeria.html#ArcaneBurstFlight) | `ArcaneBurstFlight` | Flight | projectile |
| 237 | [Arcane Burst Proc](Evidence/MannyFullReview/galeria.html#ArcaneBurstProc) | `ArcaneBurstProc` | Proc | target_root |
| 238 | [Blink Proc](Evidence/MannyFullReview/galeria.html#BlinkProc) | `BlinkProc` | Proc | target_root |
| 239 | [Blink Cast](Evidence/MannyFullReview/galeria.html#BlinkCast) | `BlinkCast` | Cast | root |
| 240 | [Cleansemage Apply](Evidence/MannyFullReview/galeria.html#CleansemageApply) | `CleansemageApply` | Apply | target_root |
| 241 | [Coil Cast](Evidence/MannyFullReview/galeria.html#CoilCast) | `CoilCast` | Cast | source_body |
| 242 | [Combust I Proc](Evidence/MannyFullReview/galeria.html#CombustIProc) | `CombustIProc` | Proc | target_root |
| 243 | [Combust II Proc](Evidence/MannyFullReview/galeria.html#CombustIiProc) | `CombustIiProc` | Proc | target_root |
| 244 | [Combust II Area Impact](Evidence/MannyFullReview/galeria.html#CombustIiAreaImpact) | `CombustIiAreaImpact` | AreaImpact | world |
| 245 | [Frost Lance I Flight](Evidence/MannyFullReview/galeria.html#FrostLanceIFlight) | `FrostLanceIFlight` | Flight | projectile |
| 246 | [Frost Lance II Flight](Evidence/MannyFullReview/galeria.html#FrostLanceIiFlight) | `FrostLanceIiFlight` | Flight | projectile |
| 247 | [Glacial Spike I Area Impact](Evidence/MannyFullReview/galeria.html#GlacialSpikeIAreaImpact) | `GlacialSpikeIAreaImpact` | AreaImpact | world |
| 248 | [Glacial Spike II Area Impact](Evidence/MannyFullReview/galeria.html#GlacialSpikeIiAreaImpact) | `GlacialSpikeIiAreaImpact` | AreaImpact | world |
| 249 | [Iceberg Flight](Evidence/MannyFullReview/galeria.html#IcebergFlight) | `IcebergFlight` | Flight | projectile |
| 250 | [Iceberg Proc](Evidence/MannyFullReview/galeria.html#IcebergProc) | `IcebergProc` | Proc | target_root |
| 251 | [Mana Storm Active](Evidence/MannyFullReview/galeria.html#ManaStormActive) | `ManaStormActive` | Active | world |
| 252 | [Manifest Active](Evidence/MannyFullReview/galeria.html#ManifestActive) | `ManifestActive` | Active | root |
| 253 | [Mist Active](Evidence/MannyFullReview/galeria.html#MistActive) | `MistActive` | Active | world |
| 254 | [Static Bolt I Flight](Evidence/MannyFullReview/galeria.html#StaticBoltIFlight) | `StaticBoltIFlight` | Flight | projectile |
| 255 | [Static Bolt II Flight](Evidence/MannyFullReview/galeria.html#StaticBoltIiFlight) | `StaticBoltIiFlight` | Flight | projectile |
| 256 | [Thunderstrike I Strike](Evidence/MannyFullReview/galeria.html#ThunderstrikeIStrike) | `ThunderstrikeIStrike` | Strike | world |
| 257 | [Thunderstrike II Strike](Evidence/MannyFullReview/galeria.html#ThunderstrikeIiStrike) | `ThunderstrikeIiStrike` | Strike | world |
| 258 | [Vortex Flight](Evidence/MannyFullReview/galeria.html#VortexFlight) | `VortexFlight` | Flight | projectile |
| 259 | [Vortex Displacement](Evidence/MannyFullReview/galeria.html#VortexDisplacement) | `VortexDisplacement` | Displacement | target_root |
| 260 | [Weave Cast](Evidence/MannyFullReview/galeria.html#WeaveCast) | `WeaveCast` | Cast | root |
| 261 | [Weave Active](Evidence/MannyFullReview/galeria.html#WeaveActive) | `WeaveActive` | Active | root |
| 262 | [Astral Aura Moon Active](Evidence/MannyFullReview/galeria.html#AstralAuraMoonActive) | `AstralAuraMoonActive` | Active | root |
| 263 | [Astral Aura Sun Active](Evidence/MannyFullReview/galeria.html#AstralAuraSunActive) | `AstralAuraSunActive` | Active | root |
| 264 | [Astral Pull Area Impact](Evidence/MannyFullReview/galeria.html#AstralPullAreaImpact) | `AstralPullAreaImpact` | AreaImpact | world |
| 265 | [Astral Pull Relocate](Evidence/MannyFullReview/galeria.html#AstralPullRelocate) | `AstralPullRelocate` | Relocate | target_root |
| 266 | [Astral Pull Link](Evidence/MannyFullReview/galeria.html#AstralPullLink) | `AstralPullLink` | Link | beam |
| 267 | [Astral Step Proc](Evidence/MannyFullReview/galeria.html#AstralStepProc) | `AstralStepProc` | Proc | target_root |
| 268 | [Astral Step Cast](Evidence/MannyFullReview/galeria.html#AstralStepCast) | `AstralStepCast` | Cast | source_body |
| 269 | [Astral Veil Active](Evidence/MannyFullReview/galeria.html#AstralVeilActive) | `AstralVeilActive` | Active | world |
| 270 | [Black Hole I Active](Evidence/MannyFullReview/galeria.html#BlackHoleIActive) | `BlackHoleIActive` | Active | world |
| 271 | [Black Hole II Active](Evidence/MannyFullReview/galeria.html#BlackHoleIiActive) | `BlackHoleIiActive` | Active | world |
| 272 | [Bright Star Cast](Evidence/MannyFullReview/galeria.html#BrightStarCast) | `BrightStarCast` | Cast | root |
| 273 | [Cleansemystic Apply](Evidence/MannyFullReview/galeria.html#CleansemysticApply) | `CleansemysticApply` | Apply | target_root |
| 274 | [Cosmic Ray I Pending](Evidence/MannyFullReview/galeria.html#CosmicRayIPending) | `CosmicRayIPending` | Pending | target_body |
| 275 | [Cosmic Ray I Resolve](Evidence/MannyFullReview/galeria.html#CosmicRayIResolve) | `CosmicRayIResolve` | Resolve | target_root |
| 276 | [Cosmic Ray II Pending](Evidence/MannyFullReview/galeria.html#CosmicRayIiPending) | `CosmicRayIiPending` | Pending | target_body |
| 277 | [Cosmic Ray II Resolve](Evidence/MannyFullReview/galeria.html#CosmicRayIiResolve) | `CosmicRayIiResolve` | Resolve | target_root |
| 278 | [Eclipse Area Impact](Evidence/MannyFullReview/galeria.html#EclipseAreaImpact) | `EclipseAreaImpact` | AreaImpact | world |
| 279 | [Ether I Ally Flight](Evidence/MannyFullReview/galeria.html#EtherIAllyFlight) | `EtherIAllyFlight` | Flight | projectile |
| 280 | [Ether I Enemy Flight](Evidence/MannyFullReview/galeria.html#EtherIEnemyFlight) | `EtherIEnemyFlight` | Flight | projectile |
| 281 | [Ether II Ally Flight](Evidence/MannyFullReview/galeria.html#EtherIiAllyFlight) | `EtherIiAllyFlight` | Flight | projectile |
| 282 | [Ether II Enemy Flight](Evidence/MannyFullReview/galeria.html#EtherIiEnemyFlight) | `EtherIiEnemyFlight` | Flight | projectile |
| 283 | [Full Moon Area Impact](Evidence/MannyFullReview/galeria.html#FullMoonAreaImpact) | `FullMoonAreaImpact` | AreaImpact | world |
| 284 | [Lullaby Flight](Evidence/MannyFullReview/galeria.html#LullabyFlight) | `LullabyFlight` | Flight | projectile |
| 285 | [Lullaby Proc](Evidence/MannyFullReview/galeria.html#LullabyProc) | `LullabyProc` | Proc | target_body |
| 286 | [Lullaby II Nightmare Flight](Evidence/MannyFullReview/galeria.html#LullabyIiNightmareFlight) | `LullabyIiNightmareFlight` | Flight | projectile |
| 287 | [Lullaby II Nightmare Proc](Evidence/MannyFullReview/galeria.html#LullabyIiNightmareProc) | `LullabyIiNightmareProc` | Proc | target_body |
| 288 | [Moon Stance Cast](Evidence/MannyFullReview/galeria.html#MoonStanceCast) | `MoonStanceCast` | Cast | root |
| 289 | [Moon Stance Active](Evidence/MannyFullReview/galeria.html#MoonStanceActive) | `MoonStanceActive` | Active | root |
| 290 | [Resurrect Hold](Evidence/MannyFullReview/galeria.html#ResurrectHold) | `ResurrectHold` | Hold | target_root |
| 291 | [Sun Stance Cast](Evidence/MannyFullReview/galeria.html#SunStanceCast) | `SunStanceCast` | Cast | root |
| 292 | [Sun Stance Active](Evidence/MannyFullReview/galeria.html#SunStanceActive) | `SunStanceActive` | Active | root |
| 293 | [Backstab Flight](Evidence/MannyFullReview/galeria.html#BackstabFlight) | `BackstabFlight` | Flight | projectile |
| 294 | [Backstab Impact](Evidence/MannyFullReview/galeria.html#BackstabImpact) | `BackstabImpact` | Impact | target_root |
| 295 | [Backstab II Flight](Evidence/MannyFullReview/galeria.html#BackstabIiFlight) | `BackstabIiFlight` | Flight | projectile |
| 296 | [Basic Attack Bleed Overlay](Evidence/MannyFullReview/galeria.html#BasicAttackBleedOverlay) | `BasicAttackBleedOverlay` | Overlay | target_root |
| 297 | [Basic Attack Poison Overlay](Evidence/MannyFullReview/galeria.html#BasicAttackPoisonOverlay) | `BasicAttackPoisonOverlay` | Overlay | target_root |
| 298 | [Blinding Dart Flight](Evidence/MannyFullReview/galeria.html#BlindingDartFlight) | `BlindingDartFlight` | Flight | projectile |
| 299 | [Blinding Dart Impact](Evidence/MannyFullReview/galeria.html#BlindingDartImpact) | `BlindingDartImpact` | Impact | target_face |
| 300 | [Blinding Dart Proc](Evidence/MannyFullReview/galeria.html#BlindingDartProc) | `BlindingDartProc` | Proc | target_face |
| 301 | [Cleansescout Apply](Evidence/MannyFullReview/galeria.html#CleansescoutApply) | `CleansescoutApply` | Apply | target_root |
| 302 | [Evasion Proc](Evidence/MannyFullReview/galeria.html#EvasionProc) | `EvasionProc` | Proc | root |
| 303 | [Exploit Weakness I Impact](Evidence/MannyFullReview/galeria.html#ExploitWeaknessIImpact) | `ExploitWeaknessIImpact` | Impact | target_body |
| 304 | [Exploit Weakness I Proc](Evidence/MannyFullReview/galeria.html#ExploitWeaknessIProc) | `ExploitWeaknessIProc` | Proc | target_body |
| 305 | [Exploit Weakness II Impact](Evidence/MannyFullReview/galeria.html#ExploitWeaknessIiImpact) | `ExploitWeaknessIiImpact` | Impact | target_body |
| 306 | [Exploit Weakness II Proc](Evidence/MannyFullReview/galeria.html#ExploitWeaknessIiProc) | `ExploitWeaknessIiProc` | Proc | target_body |
| 307 | [Exploit Weakness III Impact](Evidence/MannyFullReview/galeria.html#ExploitWeaknessIiiImpact) | `ExploitWeaknessIiiImpact` | Impact | target_body |
| 308 | [Exploit Weakness III Proc](Evidence/MannyFullReview/galeria.html#ExploitWeaknessIiiProc) | `ExploitWeaknessIiiProc` | Proc | target_body |
| 309 | [Hemorrhage Payoff](Evidence/MannyFullReview/galeria.html#HemorrhagePayoff) | `HemorrhagePayoff` | Payoff | target_body |
| 310 | [Hemorrhage Consume](Evidence/MannyFullReview/galeria.html#HemorrhageConsume) | `HemorrhageConsume` | Consume | target_body |
| 311 | [Long Jump Hold](Evidence/MannyFullReview/galeria.html#LongJumpHold) | `LongJumpHold` | Hold | ground_link |
| 312 | [Long Jump Telegraph](Evidence/MannyFullReview/galeria.html#LongJumpTelegraph) | `LongJumpTelegraph` | Telegraph | world |
| 313 | [Long Jump Movement](Evidence/MannyFullReview/galeria.html#LongJumpMovement) | `LongJumpMovement` | Movement | root |
| 314 | [Poison Sac Flight](Evidence/MannyFullReview/galeria.html#PoisonSacFlight) | `PoisonSacFlight` | Flight | projectile |
| 315 | [Poison Sac Impact](Evidence/MannyFullReview/galeria.html#PoisonSacImpact) | `PoisonSacImpact` | Impact | target_root |
| 316 | [Poison Sac Active](Evidence/MannyFullReview/galeria.html#PoisonSacActive) | `PoisonSacActive` | Active | world |
| 317 | [Poison Sac Consume](Evidence/MannyFullReview/galeria.html#PoisonSacConsume) | `PoisonSacConsume` | Consume | target_body |
| 318 | [Quickstep I Movement](Evidence/MannyFullReview/galeria.html#QuickstepIMovement) | `QuickstepIMovement` | Movement | root |
| 319 | [Quickstep II Movement](Evidence/MannyFullReview/galeria.html#QuickstepIiMovement) | `QuickstepIiMovement` | Movement | root |
| 320 | [Sand Shot Cast](Evidence/MannyFullReview/galeria.html#SandShotCast) | `SandShotCast` | Cast | world |
| 321 | [Sand Shot Impact](Evidence/MannyFullReview/galeria.html#SandShotImpact) | `SandShotImpact` | Impact | target_contact |
| 322 | [Sickness Impact](Evidence/MannyFullReview/galeria.html#SicknessImpact) | `SicknessImpact` | Impact | target_body |
| 323 | [Sickness Area Impact](Evidence/MannyFullReview/galeria.html#SicknessAreaImpact) | `SicknessAreaImpact` | AreaImpact | world |
| 324 | [Sickness Consume](Evidence/MannyFullReview/galeria.html#SicknessConsume) | `SicknessConsume` | Consume | target_body |
| 325 | [Smoke Bomb I Flight](Evidence/MannyFullReview/galeria.html#SmokeBombIFlight) | `SmokeBombIFlight` | Flight | projectile |
| 326 | [Smoke Bomb I Area Impact](Evidence/MannyFullReview/galeria.html#SmokeBombIAreaImpact) | `SmokeBombIAreaImpact` | AreaImpact | world |
| 327 | [Smoke Bomb I Active](Evidence/MannyFullReview/galeria.html#SmokeBombIActive) | `SmokeBombIActive` | Active | world |
| 328 | [Smoke Bomb II Flight](Evidence/MannyFullReview/galeria.html#SmokeBombIiFlight) | `SmokeBombIiFlight` | Flight | projectile |
| 329 | [Smoke Bomb II Area Impact](Evidence/MannyFullReview/galeria.html#SmokeBombIiAreaImpact) | `SmokeBombIiAreaImpact` | AreaImpact | world |
| 330 | [Smoke Bomb II Active](Evidence/MannyFullReview/galeria.html#SmokeBombIiActive) | `SmokeBombIiActive` | Active | world |
| 331 | [Torpor Flight](Evidence/MannyFullReview/galeria.html#TorporFlight) | `TorporFlight` | Flight | projectile |
| 332 | [Torpor Impact](Evidence/MannyFullReview/galeria.html#TorporImpact) | `TorporImpact` | Impact | target_root |
| 333 | [Torpor Proc](Evidence/MannyFullReview/galeria.html#TorporProc) | `TorporProc` | Proc | target_body |
| 334 | [Vine Field I Active](Evidence/MannyFullReview/galeria.html#VineFieldIActive) | `VineFieldIActive` | Active | world |
| 335 | [Vine Field II Active](Evidence/MannyFullReview/galeria.html#VineFieldIiActive) | `VineFieldIiActive` | Active | world |
| 336 | [Basic Dual Daggers Physical Trail — mão esquerda](Evidence/MannyFullReview/galeria.html#BasicDualDaggersPhysicalTrailLeft) | `BasicDualDaggersPhysicalTrail` | Trail | weapon |
| 337 | [Basic Dual Daggers Magical Trail — mão esquerda](Evidence/MannyFullReview/galeria.html#BasicDualDaggersMagicalTrailLeft) | `BasicDualDaggersMagicalTrail` | Trail | weapon |
| 338 | [Basic Fists Gauntlets Physical Trail — mão esquerda](Evidence/MannyFullReview/galeria.html#BasicFistsGauntletsPhysicalTrailLeft) | `BasicFistsGauntletsPhysicalTrail` | Trail | weapon |
| 339 | [Basic Fists Gauntlets Magical Trail — mão esquerda](Evidence/MannyFullReview/galeria.html#BasicFistsGauntletsMagicalTrailLeft) | `BasicFistsGauntletsMagicalTrail` | Trail | weapon |
| 340 | [Iceberg — corpo de terreno com Manny](Evidence/MannyFullReview/galeria.html#IcebergTerrainBody) | `IcebergProc` | Proc | world |
