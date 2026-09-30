# Histórico de versões

Cada tag de Release preserva o código e o pacote publicados naquela data. O snapshot atual está em `translations/v15/`; as alterações ficam documentadas em `changes/`.

## v15 — atualização do jogo de 30/09/2026

- Atualizadas as 227 tabelas de texto a partir da instalação original recém-atualizada: 584 registros adicionados, 5 removidos e 27 textos existentes alterados. O total passou a 129.177 registros e 128.038 células traduzidas.
- Traduzidas as novas missões da Explorers Guild e da pesquisa da Replica Seed, com objetivos específicos para Orica, Bailiegh, Nicolas, Karugura e Tagar. Nomes próprios permanecem como no jogo; os nomes de missão, instruções e descrições estão em português.
- Incorporados eventos e recompensas da Arena, do Naruru Dice Festival e das Incursões, além de novas coleções, descrições de itens e instruções da loja. Produtos da loja e nomes de itens seguem em inglês conforme o glossário.
- A nomenclatura atual do torneio passou de “apostas” para **“torcida”** nos textos que o jogo alterou. Corrigida a mensagem de correio que dizia incorretamente que uma previsão errada estava certa.
- Revisada a mesclagem de tabelas com IDs repetidos e dos parâmetros de nome de item; nenhum texto antigo foi associado a outra linha. Auditoria final: nenhuma tabela, ID, tradução obrigatória ou marcador ausente; nenhuma menção a nome próprio perdido.

## v14.1

- Regra editorial consolidada (2026-09-27, tabela completa no `GLOSSARIO-E-REGRAS.md`): **todo nome próprio fica em inglês, em qualquer lugar** — Skills (casam com os `Skillbook [{Param1}]`), itens, trajes, montarias, chaveiros, títulos, cartas, produtos da loja, masmorras e Trial Gates, regiões, NPCs/chefes, nomes de quem fala nos diálogos, a Adventurers Alliance e suas facções (Merchant, Blacksmith, Artisan, Appraiser, Hunter, Explorer, Wayfinder), vendedores e balcões da cidade. `On` → "Ligado" (era "Em"). Regras no `GLOSSARIO-E-REGRAS.md`.
- 18.337 células alteradas sobre a v13 (`changes/v13-to-v14/`): 7.800+ células-nome restauradas ao original (Skills, itens, trajes, montarias, chaveiros, títulos, cartas, produtos da loja, facções, vendedores, Trial Gates, regiões/pontos do mapa, chefes…), ~5.400 trocas de termos fixos em frases (Adventurers Alliance, Forsaken Land, Trial Gate, Bardad Expedition, Paradise Advent Society, guildas, acampamentos e postos…), 142 rótulos de falante retraduzidos (descritivos em PT: Vovô, Aventureira Misteriosa; apelidos em EN: Shrewd Merchant), ~270 frases de itens/lugares reescritas à mão ("Compre uma Rejuvenation Potion", "Derrote o Guardian of the Treasure", "Ativar Replica Seed"…). Corrigidas de passagem tags vazias `<Orange></>` herdadas da v12 em tutoriais e diálogos.
- Revisão final da v14 (2026-09-28), depois das capturas de tela do mantenedor: `Costume_Name.Param` e outras colunas que compõem nomes voltam ao inglês (era "Água's Wizard", "Vitória's Warrior", "Intermediário Executor"); conteúdos e masmorras com o **mesmo nome em todo lugar** — menu ESC, aba de conteúdos, ícones do mapa, carregamento, correio, tutoriais (Ethereal Sanctum, Temporal Barrier, Arbiter’s Secret Vault / Arbiter’s Ordeal, Ordeal Token, Trial of Leap / Wisdom / Combat, Rift Boss, Gold Dungeon, Clan Perpetual Corridor, Fortress Siege, Sentinel Conquest), sistemas com nome próprio (Grace of the Constellations, Gudua's Memories, Crest of the Ancients, Emperor's Gallery/Armory), eventos e colaborações (Aburu's Bounty Festival, Halo Festival, Harvest Festival, Architect x Attack on Titan), marcos do mapa (Abyss Fortress, Guardian Tower of the Abyss, Ashur's Torch, Giant's Remnants, Monolith) e ~40 itens citados em frases (Treasure Chest, Relic of Loyalty/Subjugation/Infinity/Abyss, Elixir of Attack…, Server Transfer Ticket, Lucky Chest, Anniversary Coin). Frases quebradas por trocas parciais corrigidas ("Rift chefe", "Remanescentes de Giant", "Ataque em Titan", "Giant Morcego", "Vitória Recompensa Privada", "Monolith War Inscrição de entrada").
- Menu Crescimento (`GuideGrowth_Name`, `GuideGrowthMethod_Name`) e categorias do Arbiter's Ordeal (`DungeonModularType_Name`) reescritos em português natural ("Atualização de Skill Ativo", "Atualizar suas Skills aumenta o desempenho geral delas…", "Os Planadores permitem…"). Botão "Receive All" → "Receber Todos"; "Enter" (botão) → "Entrar"; "Complete Mission Immediately" → "Concluir Missão Agora".
- Ferramentas: `__restore_exact_names__.names` (lista explícita), restauração de nome inteiro em qualquer coluna para nomes de 2+ palavras, nomes sem placeholder, troca sem distinção de maiúsculas, `__restore_columns__` para colunas de composição, `__sync_by_text__`, `__scan_ignore__`; linhas casadas por posição em tabelas com ID repetido (`Quest_Name` tem 343). `tools/scan_name_mentions.py` agora verifica todas as colunas de todas as tabelas e termina com 0 pendências na v14 (critério obrigatório, ver GLOSSARIO).
- `tools/apply_overrides.py`: overrides por ID+coluna, regras `__restore_exact_names__`, `__replace_translated_names__` (só nomes de 2+ palavras não descritivos) e `__term_map__` (variantes PT → termo EN, com `max_len` para termos de 1 palavra), substituição por texto em células já traduzidas. Novo `tools/scan_name_mentions.py`.

## v14 (Release inicial)

- Primeira versão publicada da v14 em 2026-09-27, com nomes de Skills, itens e masmorras em inglês nas menções identificadas (5.970 células ajustadas em relação à v13). O código e o manifesto originais podem ser consultados na [tag v14](https://github.com/jackchakkal/architectlandofexiles_BR/tree/v14).
- A v14.1 amplia a regra a todos os nomes próprios identificados e preserva o ZIP inicial da v14 para comparação.

## v13

- Distribuição refeita: um único PAK de override `pakchunk9999-Windows_21474835_P.pak` em `Content/Paks`, com prioridade acima do conteúdo baixado. Sem substituição do `pakchunk0`; sem conteúdo original do jogo no pacote. Ver `docs/COMO-A-TRADUCAO-E-CARREGADA.md`.
- Instalador para jogadores (`tools/player-installer/`) e `tools/build_release.ps1`, que gera PAK + `release.json` + ZIP.
- Total: 4.420 células alteradas (`changes/v12-to-v13/changes.json`).
- 293 rótulos de `ClientString_Name.csv` encurtados/corrigidos para não estourar a interface (ex.: "Só é possível recuperar na Vila.", "Recuperações grátis restantes: [Count]", "Capacidade de recuperação"); removidas duplicações ("Recompensas da temporada Recompensas da temporada") e resíduos ("perceptível Configurações…", "Slayer"). Lista completa em `changes/v12-to-v13/changes.json`.
- "Giant's Blessing" padronizado como "Bênção do Gigante" em 6 tabelas (antes "Bênção de Giant" e variações quebradas).
- `SupportLanguage_Name.csv`: linhas `ko` e `id` restauradas ao original (estavam parcialmente traduzidas); linha `en` exibe "Português (Brasil)" no seletor de idioma e usa "Transferir Servidor" (verbo) em vez de "Servidor de transferência".
- Novo `tools/check_completeness.py`: usa outra cultura do jogo (zh-CN) como referência para achar células que ficaram iguais ao inglês onde o chinês foi traduzido. Revelou lacunas invisíveis à auditoria antiga; 4.127 células foram traduzidas a partir dessa lista (descrições e níveis de masmorras, balcões da cidade — "Guardião do depósito", "Sacerdote curandeiro" —, 200+ rótulos de UI como "Batalha", "Trocar", "Rolar tudo", títulos de missões e conquistas, efeitos genéricos como "Empurrão"/"Derrubada"). Nomes de modos/sistemas continuam em inglês por convenção (Abyss Battlefield, Monolith War, Powerstone, OOParts, Marketplace…). Restam ~500 títulos de NPC (`Npc_Name.Title`) para revisão.
- Novos `tools/apply_overrides.py` (snapshot a partir de `overrides.json`, por ID ou por texto, com validação de placeholders/tags), `tools/build_pak.py` (gera o PAK V11 sem repak.exe; validado contra a saída do repak) e `tools/find_overflow_candidates.py`.

## v12-corrections

- 227 tabelas; nenhum ID ausente ou novo em comparação à extração original.
- Auditoria: sem placeholders/tags divergentes, campos traduzíveis vazios, alterações de nome/template/parâmetros de itens ou menções detectadas de Giant's Tower traduzidas.
- Reparo de tags e placeholders em diálogos, quests, tutoriais e descrições de Skills. Traduções preenchidas em rótulos e ações de interface que estavam vazios. Nomes próprios de itens foram mantidos em inglês para preservar busca no Marketplace.
- A busca automática produziu dez alertas com `left`; a lista contém tanto direções reais quanto contadores restantes. No snapshot v12, chaves de contador como `AUCTION_MENU_LEFTTIME`, `CLAN_EXCHANGE_LEFT_TIME`, `CLAN_RESEARCH_TOGGLE_ACTIVATE_LEFT_TIME`, `COMMON_LEFT` e `COMMON_LEFT_TIME` estão traduzidas com “restante(s)”.
- Os arquivos v12 foram extraídos do PAK override construído e todos os 227 hashes coincidem com o snapshot.
- Em 2026-09-27 o override `_1_P` sozinho traduziu só a tela inicial; o par de PAKs traduziu tudo, mas não era distribuível. A causa (prioridade de montagem) foi identificada e resolvida na v13 com o sufixo `_21474835_P`; ver `docs/COMO-A-TRADUCAO-E-CARREGADA.md`.

## v11-quality e anteriores

- Snapshots `v0-upload` a `v11-quality` preservados integralmente para histórico. Algumas versões anteriores contêm defeitos corrigidos na v12.
- Consulte `changes/v11-to-v12-corrections/changes.json` para o diff célula a célula e `docs/AUDIT-v12.json` para as verificações reproduzíveis.
