# Inventário VFX por FormId

Este inventário relaciona cada `formId` do handoff de 136 forms com o estado observado no pipeline de `SanctaMMO-VFX`. A identidade e mecânica vêm do Canon/handoff; prototypes e fichas VFX são evidência de produção e não redefinem gameplay.

## Snapshots e método

- Canon snapshot/handoff commit: `757f8441f4b9e58e1c616b20bd0c79270ee68de7`; handoff: `generated/CONTEXTUAL_EXECUTION_FORMS_HANDOFF.json`.
- O handoff declara como fonte Canon `d0342374bd5b8b9d5aae305fc0fd60d42e16474d` e SkillTree `6a63c5db4f45328627e26eb72f07d26ed82067cd`.
- SkillTree source: `6a63c5db4f45328627e26eb72f07d26ed82067cd`.
- Base indicada: `3f2755de782b4b2f0f399709bc29c78949e48d11` (ancestral do HEAD revalidado). VFX `origin/main` final revalidado: `ff13b9f3b52758bbc1166246f8d2a50f37923016`; inventário baseado nesse snapshot.
- O pipeline observado tem 23 prototypes HTML/Three.js activos apenas sob `prototypes/fighter/` (mais 2 revisions arquivadas); não foram encontrados assets Unreal/Niagara correspondentes. `sourceAsset: null` significa que nenhum asset executável foi evidenciado. Ícones e `docs/skills.json` não contam como VFX.
- A matriz de contexto de execução do handoff foi preservada em cada linha no JSON para distinguir variants sem colapsar `formId`.

## Resumo

| Estado | FormIds |
|---|---:|
| `EXISTING_EXACT` | 18 |
| `EXISTING_SHARED` | 7 |
| `NEEDS_SPLIT` | 0 |
| `LEGACY_NAME_MATCH` | 0 |
| `MISSING` | 111 |
| `NOT_APPLICABLE` | 0 |

Não existe `NEEDS_SPLIT` neste snapshot: os prototypes combinados auditados já declaram branches distintas, e os restantes casos sem implementação são `MISSING`. Isto não afirma equivalência mecânica entre branches.

## Casos partilhados auditados

- **Rage / Bulwark** (`fighter.granted.rage-bulwark.warrior`, `.tank`): um prototype, dois caminhos explícitos com resolução visual própria (cura vs casca/estilhaços de escudo); `EXISTING_SHARED`, split físico não necessário no estado atual.
- **Battlecry I / Challenge I**: um prototype, cristas de Battlecry e anel ancorado de Challenge; branches estão explícitas.
- **Pressure I / Provoke I**: um prototype, trajecto reverso/contínuo distinto entre branches; sem split físico pendente.
- **Rally I**: um FormId default servido por prototypes dedicados Warrior e Tank; ambas referências estão registadas na mesma entrada JSON.
- **Shoulder Rush II Warrior/Tank** e **Piercing Strike II Warrior/Tank**: entradas distintas por FormId; os prototypes Shoulder Rush II são separados, Piercing Strike II Warrior e Tank têm prototypes dedicados no snapshot `ff13b9f3b52758bbc1166246f8d2a50f37923016`. As duas variantes de Piercing Strike II reutilizam a estocada visual do I e acrescentam payoffs contextuais distintos em prototypes próprios.
- As relações `sharedVisualBaseWith` para forms Scout/Mage/Mystic marcam reutilização candidata de motivo comum com resolução/contexto por FormId. Não declaram VFX existente.

## Aliases legacy

A coluna de identidade continua a usar `displayName` e `formId` do handoff. Aliases ficam em `legacyNames`/`legacyAliasAudit` como provenance.

| Nome legacy | Resolução no snapshot | FormId atual |
|---|---|---|
| Blade Rush | `PROVENANCE_ALIAS` | `fighter.shoulder-rush-ii.warrior` |
| Shield Rush | `PROVENANCE_ALIAS` | `fighter.shoulder-rush-ii.tank` |
| Crushing Combo | `PROVENANCE_ALIAS` | `fighter.crushing-blow-ii.default` |
| Chain Pull | `PROVENANCE_ALIAS` | `fighter.chains-ii.default` |
| Breaching Strike | `PROVENANCE_ALIAS` | `fighter.piercing-strike-ii.warrior`, `fighter.piercing-strike-ii.tank` |
| Battlerage | `PROVENANCE_ALIAS` | `fighter.battlecry-challenge-ii.warrior` |
| Chain Challenge | `PROVENANCE_ALIAS` | `fighter.battlecry-challenge-ii.tank` |
| Bloodlust | `PROVENANCE_ALIAS` | `fighter.rally-ii.warrior`, `fighter.rally-ii.tank` |
| Inspiration | `PROVENANCE_ALIAS` | `fighter.rally-ii.warrior`, `fighter.rally-ii.tank` |
| Sentence | `PROVENANCE_ALIAS` | `scout.exploit-weakness-ii.default` |
| Ambush | `PROVENANCE_ALIAS` | `scout.backstab-ii.default` |
| Entangle | `PROVENANCE_ALIAS` | `scout.vine-field-ii.default` |
| Narrowing Volley | `PROVENANCE_ALIAS` | `scout.volley-ii.poison`, `scout.volley-ii.bleed` |
| Executioner | `PROVENANCE_ALIAS` | `scout.exploit-weakness-iii.default` |
| Shroud Bomb | `PROVENANCE_ALIAS` | `scout.smoke-bomb-ii.default` |
| Sickness | `PROVENANCE_ALIAS` | `scout.poison-sac-hemorrhage-ii.poison`, `scout.poison-sac-hemorrhage-ii.bleed` |
| Fire Ball | `PROVENANCE_ALIAS` | `mage.fire-bolt-ii.manifest`, `mage.fire-bolt-ii.weave` |
| Permafrost | `PROVENANCE_ALIAS` | `mage.frost-lance-ii.manifest`, `mage.frost-lance-ii.weave` |
| Conductive Lightning | `PROVENANCE_ALIAS` | `mage.static-bolt-ii.manifest`, `mage.static-bolt-ii.weave` |
| Overcharge | `PROVENANCE_ALIAS` | `mage.mana-barrier-ii.default` |
| Arcane Master | `PROVENANCE_ALIAS` | `mage.arcane-weaving-ii.default` |
| Elemental Master | `PROVENANCE_ALIAS` | `mage.elemental-weaver-ii.default` |
| Tick | `PROVENANCE_ALIAS` | `mystic.ether-ii.ally` |
| Tack | `PROVENANCE_ALIAS` | `mystic.ether-ii.enemy` |
| Nightmare | `PROVENANCE_ALIAS` | `mystic.lullaby-ii.default` |
| White Hole | `PROVENANCE_ALIAS` | `mystic.black-hole-ii.default` |

Os nomes legacy desta tabela são provenance de identidade: cada um aponta para os FormIds actuais acima, sem alterar display name ou gameplay. Os prototypes usam os nomes correntes (excepto o rótulo descritivo `Chains II Pull`); as fichas e ícones com aliases não são VFX executáveis. A cobertura é dada pelo status individual de cada FormId.

## Performance e qualidade

Os prototypes existentes declaram expectativas por nível de qualidade, draw calls, partículas e, em alguns casos, controlo de stress. Esses valores estão copiados por referência no `performanceEvidence` de cada entrada correspondente. São dados declarados pelo prototype HTML; não são medições do runtime UE/Niagara. Para forms sem prototype, os campos de evidência estão vazios. Standards e budgets não foram alterados.

## Inventário completo

A tabela seguinte tem exactamente uma linha por `formId`. Os detalhes de contexto, referências de evidência, campos de desempenho e aliases estão no JSON machine-readable.

| FormId | Display name | Classe | Estado | Prototype | Split | Bases partilháveis |
|---|---|---|---|---|---:|---|
| `fighter.granted.cleanse.default` | Cleanse | Fighter | `EXISTING_EXACT` | `prototypes/fighter/cleanse/cleanse-vfx.html` | não | — |
| `fighter.granted.warrior-stance-tank-stance.warrior` | Warrior Stance | Fighter | `EXISTING_EXACT` | `prototypes/fighter/warrior-stance/warrior-stance-vfx.html` | não | — |
| `fighter.granted.warrior-stance-tank-stance.tank` | Tank Stance | Fighter | `EXISTING_EXACT` | `prototypes/fighter/tank-stance/tank-stance-vfx.html` | não | — |
| `fighter.granted.rage-bulwark.warrior` | Rage — Warrior | Fighter | `EXISTING_SHARED` | `prototypes/fighter/rage-bulwark/rage-bulwark-vfx.html` | não | `fighter.granted.rage-bulwark.tank` |
| `fighter.granted.rage-bulwark.tank` | Bulwark — Tank | Fighter | `EXISTING_SHARED` | `prototypes/fighter/rage-bulwark/rage-bulwark-vfx.html` | não | `fighter.granted.rage-bulwark.warrior` |
| `fighter.severing-strike-i.default` | Severing Strike I | Fighter | `EXISTING_EXACT` | `prototypes/fighter/severing-strike/severing-strike-vfx.html` | não | — |
| `fighter.piercing-strike-i.default` | Piercing Strike I | Fighter | `EXISTING_EXACT` | `prototypes/fighter/piercing-strike/piercing-strike-vfx.html` | não | `fighter.piercing-strike-ii.tank`, `fighter.piercing-strike-ii.warrior` |
| `fighter.shoulder-rush-i.default` | Shoulder Rush I | Fighter | `EXISTING_EXACT` | `prototypes/fighter/shoulder-rush/shoulder-rush-vfx.html` | não | — |
| `fighter.crushing-blow-i.default` | Crushing Blow I | Fighter | `EXISTING_EXACT` | `prototypes/fighter/crushing-blow/crushing-blow-vfx.html` | não | — |
| `fighter.battlecry-i-challenge-i.warrior` | Battlecry I — Warrior | Fighter | `EXISTING_SHARED` | `prototypes/fighter/battlecry-challenge/battlecry-challenge-vfx.html` | não | `fighter.battlecry-i-challenge-i.tank` |
| `fighter.battlecry-i-challenge-i.tank` | Challenge I — Tank | Fighter | `EXISTING_SHARED` | `prototypes/fighter/battlecry-challenge/battlecry-challenge-vfx.html` | não | `fighter.battlecry-i-challenge-i.warrior` |
| `fighter.pressure-i-provoke-i.warrior` | Pressure I — Warrior | Fighter | `EXISTING_SHARED` | `prototypes/fighter/pressure-provoke/pressure-provoke-vfx.html` | não | `fighter.pressure-i-provoke-i.tank` |
| `fighter.pressure-i-provoke-i.tank` | Provoke I — Tank | Fighter | `EXISTING_SHARED` | `prototypes/fighter/pressure-provoke/pressure-provoke-vfx.html` | não | `fighter.pressure-i-provoke-i.warrior` |
| `fighter.second-wind.default` | Second Wind | Fighter | `EXISTING_EXACT` | `prototypes/fighter/second-wind/second-wind-vfx.html` | não | — |
| `fighter.severing-strike-ii.default` | Severing Strike II | Fighter | `EXISTING_EXACT` | `prototypes/fighter/severing-strike-ii/severing-strike-ii-vfx.html` | não | — |
| `fighter.shoulder-rush-ii.warrior` | Shoulder Rush II — Warrior | Fighter | `EXISTING_EXACT` | `prototypes/fighter/shoulder-rush-ii-warrior/shoulder-rush-ii-warrior-vfx.html` | não | `fighter.shoulder-rush-ii.tank` |
| `fighter.shoulder-rush-ii.tank` | Shoulder Rush II — Tank | Fighter | `EXISTING_EXACT` | `prototypes/fighter/shoulder-rush-ii-tank/shoulder-rush-ii-tank-vfx.html` | não | `fighter.shoulder-rush-ii.warrior` |
| `fighter.crushing-blow-ii.default` | Crushing Blow II | Fighter | `EXISTING_EXACT` | `prototypes/fighter/crushing-blow-ii/crushing-blow-ii-vfx.html` | não | — |
| `fighter.chains-i.default` | Chains I | Fighter | `EXISTING_EXACT` | `prototypes/fighter/chains/chains-vfx.html` | não | — |
| `fighter.war-leap.default` | War Leap | Fighter | `EXISTING_EXACT` | `prototypes/fighter/war-leap/war-leap-vfx.html` | não | — |
| `fighter.rally-i.default` | Rally I | Fighter | `EXISTING_SHARED` | `prototypes/fighter/rally-i-warrior/rally-i-warrior-vfx.html`, `prototypes/fighter/rally-i-tank/rally-i-tank-vfx.html` | não | `fighter.rally-ii.tank`, `fighter.rally-ii.warrior` |
| `fighter.severing-strike-iii.default` | Severing Strike III | Fighter | `EXISTING_EXACT` | `prototypes/fighter/severing-strike-iii/severing-strike-iii-vfx.html` | não | — |
| `fighter.chains-ii.default` | Chains II | Fighter | `EXISTING_EXACT` | `prototypes/fighter/chains-ii/chains-ii-vfx.html` | não | — |
| `fighter.piercing-strike-ii.warrior` | Piercing Strike II — Warrior | Fighter | `EXISTING_EXACT` | `prototypes/fighter/piercing-strike-ii-warrior/piercing-strike-ii-warrior-vfx.html` | não | `fighter.piercing-strike-i.default`, `fighter.piercing-strike-ii.tank` |
| `fighter.piercing-strike-ii.tank` | Piercing Strike II — Tank | Fighter | `EXISTING_EXACT` | `prototypes/fighter/piercing-strike-ii-tank/piercing-strike-ii-tank-vfx.html` | não | `fighter.piercing-strike-i.default`, `fighter.piercing-strike-ii.warrior` |
| `fighter.defiant-presence.default` | Defiant Presence | Fighter | `MISSING` | — | não | — |
| `fighter.battlecry-challenge-ii.warrior` | Battlecry II — Warrior | Fighter | `MISSING` | — | não | — |
| `fighter.battlecry-challenge-ii.tank` | Challenge II — Tank | Fighter | `MISSING` | — | não | — |
| `fighter.momentum-mastery.default` | Momentum Mastery | Fighter | `MISSING` | — | não | — |
| `fighter.rally-ii.warrior` | Rally II — Warrior | Fighter | `MISSING` | — | não | `fighter.rally-i.default`, `fighter.rally-ii.tank` |
| `fighter.rally-ii.tank` | Rally II — Tank | Fighter | `MISSING` | — | não | `fighter.rally-i.default`, `fighter.rally-ii.warrior` |
| `scout.granted.cleanse.default` | Cleanse | Scout | `MISSING` | — | não | — |
| `scout.granted.poison-bleed-stance.poison` | Poison Stance | Scout | `MISSING` | — | não | `scout.granted.poison-bleed-stance.bleed` |
| `scout.granted.poison-bleed-stance.bleed` | Bleed Stance | Scout | `MISSING` | — | não | `scout.granted.poison-bleed-stance.poison` |
| `scout.granted.poison-sac-hemorrhage.poison` | Poison Sac | Scout | `MISSING` | — | não | `scout.granted.poison-sac-hemorrhage.bleed` |
| `scout.granted.poison-sac-hemorrhage.bleed` | Hemorrhage | Scout | `MISSING` | — | não | `scout.granted.poison-sac-hemorrhage.poison` |
| `scout.exploit-weakness-i.default` | Exploit Weakness I | Scout | `MISSING` | — | não | — |
| `scout.quickstep-i.default` | Quickstep I | Scout | `MISSING` | — | não | — |
| `scout.rapid-attack.default` | Rapid Attack | Scout | `MISSING` | — | não | — |
| `scout.backstab-i.default` | Backstab I | Scout | `MISSING` | — | não | — |
| `scout.torpor.default` | Torpor | Scout | `MISSING` | — | não | — |
| `scout.blinding-dart.default` | Blinding Dart | Scout | `MISSING` | — | não | — |
| `scout.volley-i.poison` | Volley I — Poison | Scout | `MISSING` | — | não | `scout.volley-i.bleed` |
| `scout.volley-i.bleed` | Volley I — Bleed | Scout | `MISSING` | — | não | `scout.volley-i.poison` |
| `scout.exploit-weakness-ii.default` | Exploit Weakness II | Scout | `MISSING` | — | não | — |
| `scout.quickstep-ii.default` | Quickstep II | Scout | `MISSING` | — | não | — |
| `scout.long-jump.default` | Long Jump | Scout | `MISSING` | — | não | — |
| `scout.evasion.default` | Evasion | Scout | `MISSING` | — | não | — |
| `scout.sand-shot.default` | Sand Shot | Scout | `MISSING` | — | não | — |
| `scout.vine-field-i.default` | Vine Field I | Scout | `MISSING` | — | não | — |
| `scout.backstab-ii.default` | Backstab II | Scout | `MISSING` | — | não | — |
| `scout.smoke-bomb-i.default` | Smoke Bomb I | Scout | `MISSING` | — | não | — |
| `scout.vine-field-ii.default` | Vine Field II | Scout | `MISSING` | — | não | — |
| `scout.volley-ii.poison` | Volley II — Poison | Scout | `MISSING` | — | não | `scout.volley-ii.bleed` |
| `scout.volley-ii.bleed` | Volley II — Bleed | Scout | `MISSING` | — | não | `scout.volley-ii.poison` |
| `scout.poison-sac-hemorrhage-ii.poison` | Poison Sac II — Poison | Scout | `MISSING` | — | não | `scout.poison-sac-hemorrhage-ii.bleed` |
| `scout.poison-sac-hemorrhage-ii.bleed` | Hemorrhage II — Bleed | Scout | `MISSING` | — | não | `scout.poison-sac-hemorrhage-ii.poison` |
| `scout.exploit-weakness-iii.default` | Exploit Weakness III | Scout | `MISSING` | — | não | — |
| `scout.smoke-bomb-ii.default` | Smoke Bomb II | Scout | `MISSING` | — | não | — |
| `universal.basic-attack.poison` | Basic Attack — Poison | Scout | `MISSING` | — | não | `universal.basic-attack.bleed` |
| `universal.basic-attack.bleed` | Basic Attack — Bleed | Scout | `MISSING` | — | não | `universal.basic-attack.poison` |
| `mage.granted.cleanse.default` | Cleanse | Mage | `MISSING` | — | não | — |
| `mage.granted.manifest-weave.manifest` | Manifest | Mage | `MISSING` | — | não | `mage.granted.manifest-weave.weave` |
| `mage.granted.manifest-weave.weave` | Weave | Mage | `MISSING` | — | não | `mage.granted.manifest-weave.manifest` |
| `mage.granted.arcane-burst.arcane-shards` | Arcane Burst | Mage | `MISSING` | — | não | — |
| `mage.granted.arcane-burst.fire-fire` | Vortex — Fire + Fire | Mage | `MISSING` | — | não | — |
| `mage.granted.arcane-burst.ice-ice` | Iceberg — Ice + Ice | Mage | `MISSING` | — | não | — |
| `mage.granted.arcane-burst.lightning-lightning` | Coil — Lightning + Lightning | Mage | `MISSING` | — | não | — |
| `mage.granted.arcane-burst.fire-ice` | Mist — Fire + Ice | Mage | `MISSING` | — | não | — |
| `mage.granted.arcane-burst.fire-lightning` | Laser — Fire + Lightning | Mage | `MISSING` | — | não | — |
| `mage.granted.arcane-burst.ice-lightning` | Tempest — Ice + Lightning | Mage | `MISSING` | — | não | — |
| `mage.fire-bolt-i.manifest` | Fire Bolt I — Manifest | Mage | `MISSING` | — | não | `mage.fire-bolt-i.weave` |
| `mage.fire-bolt-i.weave` | Fire Bolt I — Weave | Mage | `MISSING` | — | não | `mage.fire-bolt-i.manifest` |
| `mage.combust-i.manifest` | Combust I — Manifest | Mage | `MISSING` | — | não | `mage.combust-i.weave` |
| `mage.combust-i.weave` | Combust I — Weave | Mage | `MISSING` | — | não | `mage.combust-i.manifest` |
| `mage.frost-lance-i.manifest` | Frost Lance I — Manifest | Mage | `MISSING` | — | não | `mage.frost-lance-i.weave` |
| `mage.frost-lance-i.weave` | Frost Lance I — Weave | Mage | `MISSING` | — | não | `mage.frost-lance-i.manifest` |
| `mage.glacial-spike-i.manifest` | Glacial Spike I — Manifest | Mage | `MISSING` | — | não | `mage.glacial-spike-i.weave` |
| `mage.glacial-spike-i.weave` | Glacial Spike I — Weave | Mage | `MISSING` | — | não | `mage.glacial-spike-i.manifest` |
| `mage.static-bolt-i.manifest` | Static Bolt I — Manifest | Mage | `MISSING` | — | não | `mage.static-bolt-i.weave` |
| `mage.static-bolt-i.weave` | Static Bolt I — Weave | Mage | `MISSING` | — | não | `mage.static-bolt-i.manifest` |
| `mage.thunderstrike-i.manifest` | Thunderstrike I — Manifest | Mage | `MISSING` | — | não | `mage.thunderstrike-i.weave` |
| `mage.thunderstrike-i.weave` | Thunderstrike I — Weave | Mage | `MISSING` | — | não | `mage.thunderstrike-i.manifest` |
| `mage.blink.default` | Blink | Mage | `MISSING` | — | não | — |
| `mage.fire-bolt-ii.manifest` | Fire Bolt II — Manifest | Mage | `MISSING` | — | não | `mage.fire-bolt-ii.weave` |
| `mage.fire-bolt-ii.weave` | Fire Bolt II — Weave | Mage | `MISSING` | — | não | `mage.fire-bolt-ii.manifest` |
| `mage.combust-ii.manifest` | Combust II — Manifest | Mage | `MISSING` | — | não | `mage.combust-ii.weave` |
| `mage.combust-ii.weave` | Combust II — Weave | Mage | `MISSING` | — | não | `mage.combust-ii.manifest` |
| `mage.frost-lance-ii.manifest` | Frost Lance II — Manifest | Mage | `MISSING` | — | não | `mage.frost-lance-ii.weave` |
| `mage.frost-lance-ii.weave` | Frost Lance II — Weave | Mage | `MISSING` | — | não | `mage.frost-lance-ii.manifest` |
| `mage.glacial-spike-ii.manifest` | Glacial Spike II — Manifest | Mage | `MISSING` | — | não | `mage.glacial-spike-ii.weave` |
| `mage.glacial-spike-ii.weave` | Glacial Spike II — Weave | Mage | `MISSING` | — | não | `mage.glacial-spike-ii.manifest` |
| `mage.thunderstrike-ii.manifest` | Thunderstrike II — Manifest | Mage | `MISSING` | — | não | `mage.thunderstrike-ii.weave` |
| `mage.thunderstrike-ii.weave` | Thunderstrike II — Weave | Mage | `MISSING` | — | não | `mage.thunderstrike-ii.manifest` |
| `mage.mana-barrier-i.default` | Mana Barrier I | Mage | `MISSING` | — | não | — |
| `mage.static-bolt-ii.manifest` | Static Bolt II — Manifest | Mage | `MISSING` | — | não | `mage.static-bolt-ii.weave` |
| `mage.static-bolt-ii.weave` | Static Bolt II — Weave | Mage | `MISSING` | — | não | `mage.static-bolt-ii.manifest` |
| `mage.mana-barrier-ii.default` | Mana Barrier II | Mage | `MISSING` | — | não | — |
| `mage.arcane-weaving-i.default` | Arcane Weaving I | Mage | `MISSING` | — | não | — |
| `mage.elemental-weaver-i.default` | Elemental Weaver I | Mage | `MISSING` | — | não | — |
| `mage.arcane-weaving-ii.default` | Arcane Weaving II | Mage | `MISSING` | — | não | — |
| `mage.elemental-weaver-ii.default` | Elemental Weaver II | Mage | `MISSING` | — | não | — |
| `mage.mana-storm.default` | Mana Storm | Mage | `MISSING` | — | não | — |
| `mystic.granted.cleanse.default` | Cleanse | Mystic | `MISSING` | — | não | — |
| `mystic.granted.sun-moon-stance.sun` | Sun Stance | Mystic | `MISSING` | — | não | `mystic.granted.sun-moon-stance.moon` |
| `mystic.granted.sun-moon-stance.moon` | Moon Stance | Mystic | `MISSING` | — | não | `mystic.granted.sun-moon-stance.sun` |
| `mystic.granted.bright-star-full-moon.sun` | Bright Star | Mystic | `MISSING` | — | não | — |
| `mystic.granted.bright-star-full-moon.moon` | Full Moon | Mystic | `MISSING` | — | não | — |
| `mystic.ether-i.ally` | Ether I — Ally | Mystic | `MISSING` | — | não | `mystic.ether-i.enemy` |
| `mystic.ether-i.enemy` | Ether I — Enemy | Mystic | `MISSING` | — | não | `mystic.ether-i.ally` |
| `mystic.spirit-of-the-orbit.sun` | Spirit of the Orbit — Sun | Mystic | `MISSING` | — | não | — |
| `mystic.spirit-of-the-orbit.moon` | Spirit of the Orbit — Moon | Mystic | `MISSING` | — | não | — |
| `mystic.cosmic-ray-i.default` | Cosmic Ray I | Mystic | `MISSING` | — | não | — |
| `mystic.connection-i.ally` | Connection I — Ally | Mystic | `MISSING` | — | não | `mystic.connection-i.enemy` |
| `mystic.connection-i.enemy` | Connection I — Enemy | Mystic | `MISSING` | — | não | `mystic.connection-i.ally` |
| `mystic.lullaby-i.default` | Lullaby I | Mystic | `MISSING` | — | não | — |
| `mystic.sun-aura-moon-aura.sun` | Sun Aura | Mystic | `MISSING` | — | não | `mystic.sun-aura-moon-aura.moon` |
| `mystic.sun-aura-moon-aura.moon` | Moon Aura | Mystic | `MISSING` | — | não | `mystic.sun-aura-moon-aura.sun` |
| `mystic.astral-step.default` | Astral Step | Mystic | `MISSING` | — | não | — |
| `mystic.ether-ii.ally` | Ether II — Ally | Mystic | `MISSING` | — | não | `mystic.ether-ii.enemy` |
| `mystic.ether-ii.enemy` | Ether II — Enemy | Mystic | `MISSING` | — | não | `mystic.ether-ii.ally` |
| `mystic.resurrect.default` | Resurrect | Mystic | `MISSING` | — | não | — |
| `mystic.spirit-of-the-star.sun` | Spirit of the Star — Sun | Mystic | `MISSING` | — | não | — |
| `mystic.spirit-of-the-star.moon` | Spirit of the Star — Moon | Mystic | `MISSING` | — | não | — |
| `mystic.cosmic-ray-ii.default` | Cosmic Ray II | Mystic | `MISSING` | — | não | — |
| `mystic.serenity.default` | Serenity | Mystic | `MISSING` | — | não | — |
| `mystic.astral-pull.default` | Astral Pull | Mystic | `MISSING` | — | não | — |
| `mystic.spirit-of-the-comet.sun` | Spirit of the Comet — Sun | Mystic | `MISSING` | — | não | — |
| `mystic.spirit-of-the-comet.moon` | Spirit of the Comet — Moon | Mystic | `MISSING` | — | não | — |
| `mystic.lullaby-ii.default` | Lullaby II | Mystic | `MISSING` | — | não | — |
| `mystic.black-hole-i.default` | Black Hole I | Mystic | `MISSING` | — | não | — |
| `mystic.astral-veil.default` | Astral Veil | Mystic | `MISSING` | — | não | — |
| `mystic.eclipse.default` | Eclipse | Mystic | `MISSING` | — | não | — |
| `mystic.connection-ii.ally` | Connection II — Ally | Mystic | `MISSING` | — | não | `mystic.connection-ii.enemy` |
| `mystic.connection-ii.enemy` | Connection II — Enemy | Mystic | `MISSING` | — | não | `mystic.connection-ii.ally` |
| `mystic.black-hole-ii.default` | Black Hole II | Mystic | `MISSING` | — | não | — |

## QA de referência

- Fonte do conjunto: handoff fixado acima; não houve criação nem remoção de FormIds.
- Cada caminho `sourcePrototype`/`sourcePrototypes` aponta para um ficheiro no snapshot VFX.
- `sourceAsset` é null em todas as linhas porque não há assets Unreal/Niagara observados.
- Consulte `formid-vfx-inventory.json` para a lista completa, sem perda de detalhe por truncagem da tabela.
