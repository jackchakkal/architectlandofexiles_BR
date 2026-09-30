# Glossário e decisões editoriais

> Este arquivo é a fonte de verdade das decisões de tradução. Qualquer pessoa ou IA que continue o projeto deve ler este documento antes de traduzir ou revisar, e registrar aqui toda decisão nova. Última consolidação: 2026-09-30 (v15).

## Decisões da v15

- **Tournament Cheer** é **Torcida do torneio**; *Cheer* em botões e avisos é **torcida**. O jogo substituiu a nomenclatura anterior de *Betting*. A mecânica ainda usa previsões e taxa de inscrição; traduza esses termos literalmente quando aparecem no texto.
- **Factor** isolado em objetivos de coleta é **fator**, como em `GadgetInteraction_Name.csv` e `Gadget_Name.csv` da versão anterior. **Replica Seed**, **Explorers Guild**, **Naruru Dice Festival** e nomes de lugares continuam em inglês por serem nomes próprios.
- Bailiegh é referido no texto original do novo diálogo com pronome masculino; nas descrições novas, use **vice-mestre** e pronomes masculinos para ele.
- **Incursion / Grand Incursion** em texto genérico seguem como **Incursão / Grande Incursão**, conforme a regra anterior. Preserve nomes próprios completos que contenham esses termos.

## Regra número 1: nome próprio não se traduz — em lugar nenhum

**Tudo que for nome próprio de algo fica no original em inglês, em qualquer tabela, frase, menu, diálogo, missão, descrição ou tooltip.** Traduz-se o que está em volta do nome. Categorias e tabelas de origem (as regras automáticas em `changes/<de>-to-<para>/overrides.json` usam exatamente estas fontes):

| Categoria | Exemplos | Tabelas/colunas de origem |
| --- | --- | --- |
| Pessoas: NPCs, chefes, personagens | Naruru, Katrina, Halpasiam the Frozen Blade | `Npc_Name.Name`, `GuideBoss_Name.Name`, `DungeonGlobalBoss_Name.BossName`, `ClanBossRaid_Name.Name`, `ReplicaSeed_Name.Name` |
| Lugares, regiões, pontos do mapa, acampamentos, postos | Forsaken Land, Scything Barrens, Giant's Garden, Ancient Ruins, Verzard Outpost, Magobi Encampment, Lake of Spirits | `World_Name.Name`, `WorldMapArea_Name.PlaceName`, `WorldSpot_Name.SpotName`, `Area_Name.PlaceName/Param`, `ViewPoint_Name.Name`, `Loading_Name.WorldName`, `InterServer*`, `GuideBoss/ClanBossRaid.PlaceName`, `TowerOfTitan_Name.SubName`, `OOPartsWishList_Name.Name` |
| Masmorras e Trial Gates — **o mesmo nome em todo lugar** | Trial Gate(s), Halo Rift, Infinite Spire, Hall of Proof, Unbending Will, Arbiter’s Ordeal, Trial of Leap / Flight / Wisdom / Combat, Enhancement Barrier | `Dungeon_Name.Name/Param`, `DungeonSection_Name.Name/StringParam`, `TrialGateGroup_Name`, `DungeonClanTrialGateType_Name.Name`, `DungeonTrialGatePartyType_Name.Name`, `TreasureBoxGroup_Name.Name` |
| Conteúdos e modos com nome próprio (menu ESC, aba de conteúdos, ícones do mapa, carregamento, guia) | Ethereal Sanctum, Temporal Barrier, Arbiter’s Secret Vault, Ordeal Token, Rift Boss, Gold Dungeon, Clan Perpetual Corridor, Abnormal Rift, Fortress Siege, Sentinel Conquest, Monolith War, Abyss Battlefield | lista explícita `__restore_exact_names__.names` (+ `__term_map__`); aparecem em `MainMenu_Name`, `DungeonType_Name`, `GuideContents_Name`, `MapIconCategory_Name`, `ContentsLock_Name`, `Loading_Name`… |
| Sistemas de progressão com nome próprio | Grace of the Constellations, Gudua's Memories, Crest of the Ancients, Emperor's Gallery, Emperor's Armory | lista explícita |
| Eventos, festivais e colaborações com nome | Aburu's Bounty Festival, Halo Festival, Harvest Festival, Architect x Attack on Titan (nunca "Ataque a Titan") | lista explícita |
| Marcos e estruturas do mapa com nome | Abyss Fortress, Guardian Tower of the Abyss, Sentinel's Resonance, Ashur's Torch, Giant's Remnants, Monolith, Angbar Arena, Ancient Imperial Institute, Forsaken Mine Territory | lista explícita, `MapIconCategory_Name` |
| Itens e tudo que se equipa/coleciona | Rejuvenation Potion, Weapon Enhancement Stone, Skillbook, Replica Seed, Treasure Chest, Relic of Loyalty, Elixir of Attack, Server Transfer Ticket | `Item_Name.Name` (+ `ParamN` do título), `Dialog_Name.ItemName`, `GiantPiece_Name.GroupName`, `SeasonCollectionMain_Name.DisplayName`, `FactionLevelShortcut_Name.Param` |
| Trajes e **decorações** (óculos, fones, orelhas, acessórios cosméticos), montarias, chaveiros, títulos, cartas | Stormkel Pioneer, Pink Meow Headset, Golden Glasses, Plain Rappie, Star of the West, Water's Wizard | `Costume_Name` (Name **e** `Param`: o nome é montado como `{Param}‘s Wizard`, então o `Param` também fica em inglês — nunca "Água's Wizard"), `CostumeGroup_Name` (+Param), `CostumeSlotEffect_Name`, `Vehicle_Name`, `Keiring_Name`, `CharacterTitle_Name`, `BlessingCard_Name`, `BlessingCardGroup_Name`, `SeasonCollectionMain_Name.Param`, `Crest_Name.Param` |
| Produtos e pacotes da loja, assinaturas | Successor's Privilege | `ShopItem_Name.Name`, `Subscribe_Name.Name` |
| Skills e efeitos/buffs com nome de Skill | Shadow Surge, Wings of Fate | `Skill_Name.Name`, `SkillDescription_Name.Title` (descrições traduzidas) |
| Adventurers Alliance, facções, guildas | Merchant, Blacksmith, Artisan, Appraiser, Hunter, Explorer, Wayfinder; Hunters Guild, Blacksmiths Guild | `Faction_Name.Name`, `QuestFactionGroup_Name.Name` |
| Vendedores e balcões da cidade | Stash Keeper, Healer Priest, General Merchant, Skillbook Merchant, Commission House, Ancient Coin Shop | `TownQuickMenu_Name.Name` |
| Organizações e grupos com nome | Bardad Expedition, Paradise Advent Society, Shadow Wolf Clan, Ironblood Brigade, Defense Force, Pioneer Corps | (termo fixo, `__term_map__`) |
| Modos e sistemas | Abyss Battlefield, Monolith War, Season Pass, Marketplace, Stash, Powerstone, OOParts, Tesseract, Codex, Giant's Tower, Giant's Blessing, Attunement, Stardust, Keyring | (termo fixo) |

**Exceções e limites (decididos pelo mantenedor):**
- Rótulos descritivos de quem fala num diálogo ficam em português: *Vovô*, *Aventureira Misteriosa*, *Voz desconhecida*, *Morador aflito*. Apelidos usados como nome ficam em inglês: *Shrewd Merchant*. Nomes e organizações dentro do rótulo ficam em inglês (*Membro da Defense Force*, *Vovó Kuren*).
- Moedas ficam em português: *Ouro*, *Diamantes*.
- **Masmorra tem um nome só.** O nome que aparece no menu ESC, na aba de conteúdos, no ícone do mapa, na tela de carregamento e na tela da masmorra é o mesmo, em inglês. Errado (v13): menu "Cofre Secreto do Árbitro" e, na tela seguinte, "Arbiter's Ordeal"; "Santuário Etéreo" no menu e "Ethereal Sanctum" na missão. Certo: *Arbiter’s Secret Vault* no menu, *Arbiter’s Ordeal* na tela (são os nomes originais de cada tela), *Ethereal Sanctum* em todo lugar, *Trial of Wisdom / Trial of Leap / Trial of Combat* nas provas do santuário, *Ordeal Token* para o item de entrada.
- Modos genéricos, descritos por palavra comum, ficam em português: *Incursão* / *Grande Incursão* (Incursion / Grand Incursion), *Chefe de Campo* / *Chefe Mundial* / *Chefe Guardião* (Field / World / Guardian Boss), *Despertar*, *Ressonância*, *Ajuste*, *Avanço*, *Infusão*, *Vínculo*, *Anel de Harmonia*, *Arma Fantasma*, *Montaria*, *Planador*, *Traje*, *Decorações*. *Rift Boss* fica em inglês (Rift é lugar/conceito próprio: Abnormal Rift, Halo Rift).
- As "provas" da história dos Naruru (*Prova de Coragem*, *Prova de Perseverança*: Trial of Courage / Trial of Perseverance) são títulos de missão, não masmorras — ficam em português. Só as quatro provas do Ethereal Sanctum são masmorras.
- "Upgrade" no menu Crescimento e no Arbiter's Ordeal é *Atualização* ("Atualização de Skill Ativo", "Atualização de Traje"), nunca "Ativo Skill Atualização" nem "Traje de atualização". *Skill Ativo* / *Skill Passivo* (não "Ativo Skill"). Botão "Receive All" → *Receber Todos*; botão "Enter" → *Entrar* (a tecla do teclado continua *Enter*).
- Títulos de missões, conquistas, eventos e tutoriais são frases e são traduzidos (*Cavaleiros do Vento Gélido* como título de missão; mas a ordem *Knights of the Frostwind* citada num diálogo fica em inglês).
- Palavra comum que coincide com um nome não é nome: "um caçador qualquer", "o comerciante da esquina" ficam em português; só *Hunter*/*Merchant* como facção ou como parte de um nome ficam em inglês.
- Nomes de efeitos genéricos (*Robusto*, *Imortal*, *Atordoamento*) são traduzidos, exceto quando o efeito tem o nome de uma Skill.
- Em português, o nome em inglês entra sem aspas, com o artigo que a frase pedir: "a Replica Seed", "o Baba Liquor", "em Ancient Ruins", "vá para o Verzard Outpost".

## Interface: On/Off

`On` → **Ligado**, `Off` → **Desligado**. Nunca "Em".

| Original/termo | Tratamento PT-BR |
| --- | --- |
| Item names/títulos próprios de itens | Sempre manter a string original, inclusive fragmentos `ParamN` usados no título — **e em qualquer menção ao item dentro de outros textos** (missões, diálogos, conquistas, tutoriais, loja): "Compre uma Rejuvenation Potion", "Fabricar Weapon Enhancement Stone". |
| Nomes de Skills (`Skill_Name.Name`, `SkillDescription_Name.Title`) e efeitos/buffs com o mesmo nome | **Manter em inglês**, em qualquer menção. Motivo: os livros de Skill são itens (`Skillbook [{Param1}]`, com o nome da Skill em inglês) e o jogador precisa relacionar o livro à Skill. Descrições das Skills são traduzidas. |
| Nomes de masmorras e Trial Gates (`Dungeon_Name.Name`/`Param`, `DungeonSection_Name.*`, `TrialGateGroup_Name`, `DungeonClanTrialGateType_Name.Name`, `DungeonTrialGatePartyType_Name.Name`) | **Manter em inglês em qualquer lugar mencionado**: tabela da masmorra, objetivos de missão, descrições de efeitos ("Aplica-se apenas dentro de Ancient Ruins"), menus. |
| Adventurers Alliance, facções (`Faction_Name.Name`) e vendedores da cidade (`TownQuickMenu_Name.Name`) | Manter em inglês em qualquer lugar mencionado. |
| Trajes, montarias, chaveiros, títulos, cartas, produtos da loja (`Costume_Name`, `Vehicle_Name`, `Keiring_Name`, `CharacterTitle_Name`, `BlessingCard*`, `ShopItem_Name`, `Subscribe_Name`, `GiantPiece`, `SeasonCollectionMain.DisplayName`, `Dialog_Name.ItemName`) | Manter em inglês em qualquer lugar mencionado; descrições traduzidas. |
| Nome de quem fala (`Dialog_Name.Name`, `MiniDialog_Name.Name`, `DialogSubtitle_Name.Speaker`) | Nomes próprios em inglês (restaurados automaticamente); rótulos descritivos retraduzidos à mão em `__by_text__` (*Vovô*, *Aventureira Misteriosa*, *Voz desconhecida*). |
| Regiões e locais (`World_Name`, `WorldMapArea_Name.PlaceName`, `WorldSpot_Name`, `Area_Name.PlaceName`/`Param`, `InterServer*`) | Manter em inglês em qualquer lugar mencionado. |
| Giant's Tower | Manter nome oficial original; traduzir o restante da frase. |
| Skill | Manter `Skill`. |
| Codex | Manter `Codex`. |
| Dungeon/masmorra com nome oficial | Manter nome original. |
| Monster/NPC/boss names | Manter nomes próprios originais, em qualquer menção ("Derrote o Guardian of the Treasure"). |
| left em contador de tempo/quantidade | “restante(s)”. |
| left em instrução espacial | “à esquerda”, conforme o contexto. |
| Finger accessory slot | “Acessório equipado no dedo.” |
| Neck accessory slot | “Acessório equipado no pescoço.” |
| Ear accessory slot | “Acessório equipado na orelha.” |
| Arm accessory slot | “Acessório equipado no braço.” |

## Revisão de diálogos

Use o gênero da pessoa que fala para auto-referências (“obrigado/obrigada”) e o gênero do interlocutor para tratamentos diretos (“aventureiro/aventureira”). Não aplique substituições globais sem contexto: uma fala pode mencionar outro personagem ou usar o termo genericamente.

## Integridade técnica

Não altere IDs, cabeçalhos, placeholders, tags de cor/formatação, códigos de controle ou capitalização de nomes próprios sem comparar o texto original e testar a saída extraída do PAK.

## Comprimento dos textos de interface (a partir da v13)

A interface foi desenhada para o inglês. Regra para rótulos, títulos de janela, botões e abas (`ClientString_Name.csv` e afins): **o português não deve exceder o inglês em mais de ~20%**; quando exceder, encurtar em vez de traduzir literalmente. Preferências de termos curtos:

| Inglês | Preferir | Evitar |
| --- | --- | --- |
| Settings | Ajustes | Configurações |
| Info | Info | Informações sobre… |
| Stats | Atributos | Estatísticas |
| Rank / Ranking (placar) | Ranking | Classificação |
| Rank (cargo no clã) | Cargo | Classificação de membro |
| Auto-… | … auto. / … automático (se couber) | … de forma automática |
| Claim (reward) | Receber | Reivindicar |
| No … found. | Nenhum … . | Nenhum … foi encontrado. |
| Reward Info | Info de recompensa | Informações de recompensa |
| Scan | Varredura | Verificação |

Mensagens de corpo (descrições, diálogos, tooltips longos) não têm essa restrição, mas devem evitar duplicações e enchimento. A fila de candidatos a encurtar é gerada comparando o comprimento com o inglês (ver `TECHNICAL_PROCESS.md`).

## Nomes em inglês dentro de frases: como o processo garante (leia antes de gerar uma versão)

- `tools/apply_overrides.py` aplica quatro regras automáticas (`__restore_columns__` restaura colunas inteiras, como o nome de quem fala) — três delas a cada versão (`__restore_exact_names__`, `__replace_translated_names__` e `__term_map__` em `changes/<de>-to-<para>/overrides.json`): células cujo original é exatamente um nome (Skill, item, masmorra, facção, vendedor, região, chefe, NPC) voltam ao inglês; traduções conhecidas de nomes com 2+ palavras dentro de frases são trocadas pelo nome em inglês; e variantes em português de termos fixos ("Aliança dos Aventureiros", "Portão de Teste", "Terra Abandonada", "Guilda dos Ferreiros"…) são trocadas pelo termo original, só quando o inglês da célula contém o termo. Termos de uma palavra (Hunter, Merchant…) só são trocados em rótulos curtos, para não atingir frases genéricas.
- Desde a v14 (revisão de 2026-09-27): `__restore_exact_names__` aceita `names` (lista explícita de nomes que não vêm de tabela: Ethereal Sanctum, Temporal Barrier…); nome de 2+ palavras que é a célula inteira volta ao inglês **em qualquer coluna** (descrição, título de correio, aba, tooltip), e nomes de 1 palavra só nas colunas de nome; nomes com placeholder valem também sem ele ("Trial of Leap {StringParam}" → "Trial of Leap"); a troca de traduções conhecidas ignora maiúsculas; `__restore_columns__` restaura colunas que compõem nomes (`Costume_Name.Param`, `CostumeGroup_Name.Param`, `SeasonCollectionMain_Name.Param`, `Quest_Name.PlaceParam`, `PassMission_Name.Param`, `Crest_Name.Param`, `TreasureBoxGroup_Name.Name`, `FactionLevelShortcut_Name.Param`); `__sync_by_text__` copia a tradução de uma coluna para outra quando o inglês é o mesmo (`ShopMissionReward_Name.Param` ← `Quest_Name.Name`, para "Concluir a missão [X]" mostrar o mesmo título da missão).
- Tabelas com ID repetido (`Quest_Name`, `EventMissionGroup`, `Icon_Name`, `BadgeTask`, `CostumeSlotEffect`, `SkillAction`, `ContentsChance`): as ferramentas casam a linha em inglês pela posição, não só pelo ID.
- **Verificação obrigatória:** `tools/scan_name_mentions.py` tem de terminar com `0 células-nome ainda traduzidas` e `0 frases com nome perdido` (código de saída 0). Ele confere todas as colunas de todas as tabelas contra todas as fontes de nomes acima. Falsos positivos revisados ficam em `__scan_ignore__` (`"Tabela.csv:ID": "motivo"`), e decisões explícitas em `__by_text__` não contam como pendência. Só se declara uma versão "conferida" com esse resultado.
- Em português, o nome em inglês entra sem tradução e sem aspas, com artigo quando a frase pedir: "a Replica Seed", "o Baba Liquor", "em Ancient Ruins".

## Fluxo obrigatório para uma versão nova (resumo para quem continuar)

1. Nunca edite um snapshot publicado. Crie `changes/<vAnterior>-to-<vNova>/overrides.json` copiando as seções automáticas (`__restore_exact_names__`, `__replace_translated_names__`, `__term_map__`, `__literal_brackets__`) da versão anterior — elas são cumulativas — e acrescente as correções novas por ID (`{"Tabela.csv": {"ID": "texto"}}` ou `{"ID": {"Coluna": "texto"}}`) ou por texto (`__by_text__`).
2. Gere o snapshot: `python tools/apply_overrides.py --base translations/<vAnterior> --overrides changes/.../overrides.json --source <inglês original> --out translations/<vNova> --report changes/.../changes.json`. Zero erros é obrigatório.
3. Rode `tools/audit_translation.py` (0 issues), `tools/scan_name_mentions.py` (saída 0: nenhuma célula-nome traduzida, nenhuma frase com nome perdido) e `tools/find_overflow_candidates.py`.
4. Gere o PAK (`tools/build_pak.py` ou `tools/build_release.ps1`), verifique 227/227 entradas contra o snapshot, teste no jogo, registre `releases/<vNova>/manifest.json` e o `CHANGELOG.md`.
5. Toda decisão editorial nova entra neste arquivo, na seção correspondente, com data.
