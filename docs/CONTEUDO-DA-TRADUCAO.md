# O que contém a tradução

Gerado a partir do snapshot `translations/v15/`, comparado com as tabelas originais em inglês da atualização de 30/09/2026. "Células traduzidas" = células de texto cujo conteúdo difere do original; as demais são vazias no original, idênticas de propósito (nomes próprios, placeholders) ou ainda não traduzidas.

**Total: 227 tabelas, 129.177 registros, 128.038 células traduzidas.**

## O que fica em inglês de propósito

- **Nomes de itens** (`Item_Name.Name` e os fragmentos `ParamN` que compõem títulos): para a busca no Marketplace e a comunicação entre jogadores funcionarem. As *descrições* dos itens são traduzidas.
- **Nomes de monstros, chefes, NPCs, masmorras, conteúdos (Ethereal Sanctum, Temporal Barrier, Arbiter’s Ordeal, Rift Boss), áreas, trajes e decorações, montarias, chaveiros, títulos, cartas, produtos da loja, facções, vendedores da cidade, organizações, eventos e sistemas com nome próprio (Grace of the Constellations, Gudua's Memories, Crest of the Ancients)**: idem — em qualquer menção, inclusive dentro de missões, menus e descrições. A lista completa e as exceções estão em `GLOSSARIO-E-REGRAS.md`.
- **Nomes de Skills** (`Skill_Name.Name`, títulos de descrição, efeitos com o mesmo nome): para casar com os livros de Skill, que são itens com nome em inglês. As descrições são traduzidas.
- **`Giant's Tower`, `Skill`, `Codex`**: termos fixos do jogo.
- **Nomes de servidores** (ex.: High Pass).

## O que não está coberto

- Textos gravados **fora** das tabelas CSV — por exemplo, algumas descrições de telas de carregamento e textos desenhados em imagens — usam outro mecanismo (LocRes/assets) e não são alterados por esta tradução.
- Textos que o servidor envia prontos (nomes de eventos temporários, avisos de manutenção, chat).
- Textos novos adicionados por atualizações do jogo, até a próxima versão da tradução.

## Limitações conhecidas

- A interface foi desenhada para inglês; alguns rótulos em português ficam cortados. A v13 encurta 293 rótulos da interface e preenche 4.127 células que estavam em inglês; mais ajustes virão com base nas capturas enviadas pelos jogadores.
- Concordância de gênero em falas dirigidas ao jogador foi revisada para a personagem feminina em vários diálogos; falas genéricas podem soar neutras ou masculinas.

## Tabelas (ordenadas por volume traduzido)

| Tabela | Registros | Células traduzidas | Conteúdo |
| --- | ---: | ---: | --- |
| `Quest_Name.csv` | 13.004 | 24.612 | Missões: títulos e descrições (antes/depois de concluir) |
| `QuestTask_Name.csv` | 21.007 | 20.834 | Objetivos de missão |
| `Dialog_Name.csv` | 14.475 | 14.950 | Diálogos de NPCs |
| `CollectionMain_Name.csv` | 9.589 | 9.482 | Coleções (Codex) |
| `ClientString_Name.csv` | 8.568 | 8.005 | Interface: menus. botões. avisos. tooltips |
| `Item_Name.csv` | 5.674 | 7.133 | Itens: descrições (nomes mantidos em inglês) |
| `Effect_Name.csv` | 3.025 | 6.056 | Efeitos. buffs e debuffs |
| `Achievement_Name.csv` | 2.652 | 5.284 | Conquistas/troféus |
| `EventMissionRecord_Name.csv` | 2.035 | 3.912 | Missões de evento |
| `SkillDescription_Name.csv` | 1.783 | 1.767 | Descrições detalhadas de Skills |
| `GadgetInteraction_Name.csv` | 1.299 | 2.220 | Interações com objetos do mundo |
| `Skill_Name.csv` | 3.366 | 731 | Skills: descrições curtas (nomes mantidos) |
| `MiniDialog_Name.csv` | 1.396 | 1.516 | Falas curtas de NPCs |
| `DialogChoice_Name.csv` | 1.573 | 1.492 | Opções de resposta em diálogos |
| `OperationType_Name.csv` | 379 | 1.260 | Tipos de operação/atributos |
| `ResultCodeString_Name.csv` | 1.316 | 1.297 | Mensagens de erro e resultado do servidor |
| `Gadget_Name.csv` | 1.698 | 918 | Objetos interativos do mundo |
| `SpeechBalloonBundle_Name.csv` | 973 | 968 | Balões de fala |
| `AcquireAndUseViewGroup_Name.csv` | 816 | 873 | Guia "como obter/usar" |
| `Costume_Name.csv` | 624 | 40 | Trajes: descrições |
| `EventHighPassMission_Name.csv` | 429 | 842 | EventHighPassMission: Name. Desc |
| `PassMission_Name.csv` | 445 | 789 | PassMission: Name. Description. Param |
| `Option_Name.csv` | 324 | 746 | Menu de opções |
| `ShopItem_Name.csv` | 1.290 | 63 | Itens de loja: descrições |
| `TutorialWalkthrough_Name.csv` | 352 | 533 | Tutoriais |
| `Alert_Name.csv` | 454 | 580 | Alertas na tela |
| `FrontierStage_Name.csv` | 450 | 450 | FrontierStage: StageDescription. Param |
| `FlavorTextPage_Name.csv` | 454 | 414 | Textos de ambientação |
| `FlavorText_Name.csv` | 449 | 371 | FlavorText: Name |
| `ClanMission_Name.csv` | 194 | 367 | ClanMission: Name. Description |
| `BadgeTask_Name.csv` | 225 | 303 | BadgeTask: TaskParam. Name. Desc. Param |
| `Mail_Name.csv` | 120 | 344 | Mail: Sender. Title. Content |
| `SkillAction_Name.csv` | 330 | 330 | SkillAction: Name |
| `TutorialStep_Name.csv` | 376 | 268 | TutorialStep: Name. DialogText |
| `NpcSpawnDetail_Name.csv` | 274 | 276 | NpcSpawnDetail: SpawnDescription. Description |
| `EventTab_Name.csv` | 288 | 273 | EventTab: TabName |
| `ContentsLock_Name.csv` | 415 | 224 | ContentsLock: Name. Desc. LockDesc. Param |
| `ContentsFunction_Name.csv` | 199 | 239 | ContentsFunction: Desc. Param |
| `DialogSubtitle_Name.csv` | 200 | 248 | DialogSubtitle: Speaker. Message |
| `EventMission_Name.csv` | 131 | 251 | EventMission: PageName. PageDesc |
| `EventRankingMissionRecord_Name.csv` | 117 | 234 | EventRankingMissionRecord: Name. Desc. ViewParam |
| `SpeechBalloonNPC_Name.csv` | 225 | 209 | SpeechBalloonNPC: Text |
| `Ranking_Name.csv` | 111 | 191 | Ranking: Name. ScoreIndexName. ScoreDesc |
| `SpeechBalloonPC_Name.csv` | 175 | 173 | SpeechBalloonPC: Text |
| `BadgeNotification_Name.csv` | 107 | 167 | BadgeNotification: Message. Param |
| `EventMissionGroup_Name.csv` | 258 | 14 | EventMissionGroup: Order. GroupName |
| `Social_Name.csv` | 64 | 151 | Social: Name. Desc. ActionParam. Param |
| `Invasion_Name.csv` | 228 | 152 | Invasion: InvasionName |
| `MapIcon_Name.csv` | 330 | 126 | MapIcon: Name |
| `BlessingCard_Name.csv` | 150 | 0 | BlessingCard: Name. Desc |
| `ShopMissionReward_Name.csv` | 90 | 133 | ShopMissionReward: Name. Desc. Param |
| `ShopTab_Name.csv` | 139 | 84 | ShopTab: TabName. Descriptor. Desc. Param1 |
| `Icon_Name.csv` | 29 | 64 | Icon: Param. Name. StringParam. Desc |
| `TowerOfTitanAlgorithm_Name.csv` | 52 | 108 | TowerOfTitanAlgorithm: AlgorithmName. AlgorithmDesc. DetailDesc |
| `Toast_Name.csv` | 74 | 107 | Toast: Message. Button1Name. Button2Name |
| `GuideBoss_Name.csv` | 62 | 102 | GuideBoss: PlaceName. Name. Description. ContentsShortButtonText |
| `QuestGuideBookMissionGroup_Name.csv` | 50 | 100 | QuestGuideBookMissionGroup: Name. Desc |
| `CostumeSlotEffect_Name.csv` | 56 | 0 | CostumeSlotEffect: Grade. Name. Param |
| `FactionLevelShortcut_Name.csv` | 70 | 70 | FactionLevelShortcut: Desc. Param |
| `GuideContents_Name.csv` | 29 | 86 | GuideContents: Name. Description. GuideString1. GuideParam1 |
| `EventBanner_Name.csv` | 49 | 90 | EventBanner: Name. Desc |
| `EventAttendance_Name.csv` | 47 | 90 | EventAttendance: PageName. PageDesc |
| `GuideGrowthMethod_Name.csv` | 44 | 86 | GuideGrowthMethod: GrowthMethodName. GrowthMethodDesc |
| `Asset_Name.csv` | 41 | 82 | Asset: Name. Param. Desc |
| `AkashaGrade_Name.csv` | 108 | 84 | AkashaGrade: Story |
| `CharacterTitle_Name.csv` | 45 | 50 | CharacterTitle: Name. Description. Param |
| `Tutorial_Name.csv` | 115 | 63 | Tutorial: Name |
| `ViewPoint_Name.csv` | 66 | 66 | ViewPoint: Name. Desc |
| `OOPartsWishList_Name.csv` | 80 | 0 | OOPartsWishList: Name |
| `ContentsFunctionGroup_Name.csv` | 57 | 73 | ContentsFunctionGroup: Desc. Param |
| `BattlefieldSentinel_Name.csv` | 72 | 72 | BattlefieldSentinel: Name. Param |
| `BlessingCardGroup_Name.csv` | 74 | 0 | BlessingCardGroup: Name. Param |
| `Loading_Name.csv` | 282 | 3 | Loading: WorldName. Param |
| `Dungeon_Name.csv` | 815 | 1.251 | Dungeon: Name. DifficultyName. Description. Story |
| `GuideGrowth_Name.csv` | 21 | 57 | GuideGrowth: Name. ReviveComment. ContentsShortButtonText |
| `TutorialReplay_Name.csv` | 78 | 43 | TutorialReplay: Title |
| `GiantPiece_Name.csv` | 102 | 0 | GiantPiece: GroupName |
| `MainMenu_Name.csv` | 60 | 34 | MainMenu: Name |
| `ShopSubTab_Name.csv` | 64 | 13 | ShopSubTab: TabName. Descriptor. Desc. Param1 |
| `SeasonCollectionMain_Name.csv` | 55 | 0 | SeasonCollectionMain: DisplayName. Param |
| `AuctionTab_Name.csv` | 63 | 45 | AuctionTab: Name |
| `LoadingTip_Name.csv` | 51 | 50 | Dicas da tela de carregamento |
| `ContentsPoint_Name.csv` | 48 | 48 | ContentsPoint: Name. Param |
| `Pass_Name.csv` | 16 | 35 | Pass: Name. Desc. MaxLevelGuide. PaidRewardDesc |
| `DungeonSection_Name.csv` | 816 | 783 | DungeonSection: Name. Description. StringParam |
| `QuestTaskSubName_Name.csv` | 45 | 45 | QuestTaskSubName: SubName |
| `ItemCraftTab_Name.csv` | 49 | 35 | ItemCraftTab: Name |
| `ShopTabGroup_Name.csv` | 50 | 32 | ShopTabGroup: Name |
| `ChatSystemMessage_Name.csv` | 20 | 40 | ChatSystemMessage: Message. Name |
| `EventDrop_Name.csv` | 17 | 41 | EventDrop: PageName. PageDesc. ShorcutButtonName |
| `Vehicle_Name.csv` | 56 | 0 | Vehicle: Name. Desc |
| `Emoticon_Name.csv` | 22 | 39 | Emoticon: EmoticonName. EmoticonCommand. EmoticonDescription |
| `OptionView_Name.csv` | 258 | 37 | OptionView: DetailGroupName |
| `QuestEpisode_Name.csv` | 75 | 33 | QuestEpisode: Name |
| `EventRankingMissionReward_Name.csv` | 46 | 33 | EventRankingMissionReward: Desc |
| `EventRankingReward_Name.csv` | 39 | 33 | EventRankingReward: Desc |
| `AdventureRecord_Name.csv` | 1.059 | 31 | AdventureRecord: BossDesc |
| `TimeViewFormat_Name.csv` | 12 | 31 | TimeViewFormat: DayOver. DayOverNextUnit. HourOver. HourOverNextUnit |
| `ObserverCamera_Name.csv` | 36 | 30 | ObserverCamera: Name |
| `ClanBossRaid_Name.csv` | 12 | 0 | ClanBossRaid: PlaceGroupName. PlaceName. Name |
| `ClanRecord_Name.csv` | 29 | 29 | ClanRecord: ClanRecordString |
| `OperationMainType_Name.csv` | 32 | 29 | OperationMainType: GroupName |
| `ShopCategory_Name.csv` | 37 | 20 | ShopCategory: Name |
| `ClanPermission_Name.csv` | 29 | 26 | ClanPermission: Name |
| `GadgetType_Name.csv` | 32 | 21 | GadgetType: Name |
| `MapIconCategory_Name.csv` | 45 | 17 | MapIconCategory: Name |
| `RestoreCouponTab_Name.csv` | 31 | 20 | RestoreCouponTab: Name |
| `ContentsChance_Name.csv` | 22 | 21 | ContentsChance: DetailInfoId. Name |
| `EventShop_Name.csv` | 13 | 26 | EventShop: PageName. PageDesc |
| `QuestType_Name.csv` | 18 | 21 | QuestType: CommonName. ShortName |
| `ClanResearch_Name.csv` | 31 | 16 | ClanResearch: Name |
| `EventExchange_Name.csv` | 13 | 25 | EventExchange: PageName. PageDesc |
| `EventBuff_Name.csv` | 9 | 22 | EventBuff: Name. Desc. DisplayDesc |
| `League_Name.csv` | 27 | 22 | League: Name. Param |
| `OptionInputKey_Name.csv` | 101 | 22 | OptionInputKey: ViewText |
| `ShopPackageDesc_Name.csv` | 22 | 22 | ShopPackageDesc: Desc. RewardDesc |
| `Keiring_Name.csv` | 47 | 0 | Keiring: Name. Desc |
| `ReplicaSeed_Name.csv` | 19 | 0 | ReplicaSeed: PlaceName. Name |
| `AssistModeRecord_Name.csv` | 11 | 18 | AssistModeRecord: SystemMessage. HistoryString |
| `ContentsBulkSetting_Name.csv` | 20 | 18 | ContentsBulkSetting: Name |
| `DungeonMissionDesc_Name.csv` | 18 | 18 | DungeonMissionDesc: Description |
| `EventRoulette_Name.csv` | 6 | 18 | EventRoulette: PageName. PageDesc. PageDesc2 |
| `RewardAcquisitionLimit_Name.csv` | 19 | 19 | RewardAcquisitionLimit: RewardLimitGroupDesc |
| `NpcInteraction_Name.csv` | 30 | 17 | NpcInteraction: Desc |
| `CustomizeGroup_Name.csv` | 15 | 15 | CustomizeGroup: Name |
| `RingOfFateGroup_Name.csv` | 22 | 15 | RingOfFateGroup: Name |
| `ShopMission_Name.csv` | 17 | 0 | ShopMission: Name. Param |
| `SpeechBalloonGadget_Name.csv` | 20 | 15 | SpeechBalloonGadget: Text |
| `EventRanking_Name.csv` | 7 | 14 | EventRanking: PageName. PageDesc |
| `Mark_Name.csv` | 26 | 14 | Mark: Name. Param |
| `SeasonalEventMenu_Name.csv` | 20 | 13 | SeasonalEventMenu: Name |
| `ShopAccumSetting_Name.csv` | 15 | 15 | ShopAccumSetting: Name. Param |
| `CostumeGroup_Name.csv` | 7 | 0 | CostumeGroup: Name. Param |
| `ResonanceNodeDisplay_Name.csv` | 16 | 13 | ResonanceNodeDisplay: Name |
| `DungeonModularType_Name.csv` | 4 | 12 | DungeonModularType: Name. Description. Story |
| `EventDice_Name.csv` | 7 | 13 | EventDice: Name. ToolTipString |
| `FrontierRestriction_Name.csv` | 12 | 12 | FrontierRestriction: RestrictionName |
| `TowerOfTitanSpot_Name.csv` | 12 | 12 | TowerOfTitanSpot: Name |
| `TowerOfTitan_Name.csv` | 4 | 8 | TowerOfTitan: Name. SubName. Desc. BossNpcDesc |
| `EventRankingMission_Name.csv` | 6 | 11 | EventRankingMission: PageName. PageDesc |
| `FrontierPhenomenon_Name.csv` | 6 | 11 | FrontierPhenomenon: PhenomenonName. PhenomenonDesc |
| `PK_Name.csv` | 11 | 11 | PK: PKGrade. Param |
| `AuctionCategory_Name.csv` | 12 | 9 | AuctionCategory: Name |
| `ClassChangeType_Name.csv` | 5 | 10 | ClassChangeType: Name. Tip |
| `Class_Name.csv` | 5 | 10 | Class: Name. Desc. Tag |
| `EventCommonMission_Name.csv` | 6 | 10 | EventCommonMission: Name. Desc |
| `ItemCraftCategory_Name.csv` | 10 | 10 | ItemCraftCategory: Name |
| `TowerOfTitanEnterCondition_Name.csv` | 6 | 10 | TowerOfTitanEnterCondition: Name. Desc |
| `DungeonType_Name.csv` | 16 | 2 | DungeonType: Name |
| `QuestFactionGroup_Name.csv` | 7 | 7 | QuestFactionGroup: Name. Desc |
| `InterServerGrade_Name.csv` | 12 | 8 | InterServerGrade: Name |
| `QuestSubName_Name.csv` | 17 | 8 | QuestSubName: SubName |
| `BattlefieldClashSeason_Name.csv` | 7 | 7 | BattlefieldClashSeason: Name |
| `BattlefieldMonolith_Name.csv` | 3 | 6 | BattlefieldMonolith: Name. Param. Desc |
| `CharacterTitleCategory_Name.csv` | 6 | 6 | CharacterTitleCategory: Name |
| `ClanDonation_Name.csv` | 3 | 5 | ClanDonation: Name. Param |
| `EliteDungeonType_Name.csv` | 2 | 6 | EliteDungeonType: Name. Param. Story |
| `EventLuckybox_Name.csv` | 4 | 6 | EventLuckybox: PageName. PageDesc |
| `FrontierLeague_Name.csv` | 7 | 6 | FrontierLeague: FrontierLeagueName |
| `InterServerArea_Name.csv` | 34 | 6 | InterServerArea: Name. SubName. Desc |
| `NpcSpawnDetailGroup_Name.csv` | 14 | 6 | NpcSpawnDetailGroup: SpawnDetailGroupName. Param |
| `RestoreCouponCategory_Name.csv` | 6 | 6 | RestoreCouponCategory: Name |
| `Crest_Name.csv` | 4 | 4 | Crest: Name. Param |
| `CustomizeCategory_Name.csv` | 5 | 5 | CustomizeCategory: Name |
| `Gudua_Name.csv` | 6 | 5 | Gudua: Name |
| `MainMenuCategory_Name.csv` | 6 | 5 | MainMenuCategory: Name |
| `ResonancePage_Name.csv` | 8 | 5 | ResonancePage: CategoryName. SubCategoryName |
| `SeasonalEvent_Name.csv` | 3 | 3 | SeasonalEvent: Name. Desc |
| `SupportLanguage_Name.csv` | 7 | 5 | SupportLanguage: DisplayName. ClanLeaveCheck. ClanDisbandCheck. AccountMigrationCheck |
| `AkashaCategory_Name.csv` | 5 | 3 | AkashaCategory: Name |
| `ClanMemberGrade_Name.csv` | 4 | 4 | ClanMemberGrade: Name |
| `DungeonTrialGatePartyType_Name.csv` | 2 | 4 | DungeonTrialGatePartyType: Name. Description. Story. BossDesc |
| `EventTreasureHuntBasic_Name.csv` | 2 | 4 | EventTreasureHuntBasic: PageName. PageDesc |
| `GamePlayEventPopup_Name.csv` | 1 | 4 | GamePlayEventPopup: DescTitle. Desc. TimeDesc. TextMove  |
| `GuideBossCategory_Name.csv` | 4 | 4 | GuideBossCategory: Desc |
| `Subscribe_Name.csv` | 2 | 2 | Subscribe: Name. Desc |
| `TowerOfTitanAlgorithmTab_Name.csv` | 5 | 4 | TowerOfTitanAlgorithmTab: Name |
| `TutorialReplayCategory_Name.csv` | 7 | 4 | TutorialReplayCategory: Title |
| `AcquireAndUseTab_Name.csv` | 3 | 3 | AcquireAndUseTab: TabName |
| `BattlefieldClash_Name.csv` | 1 | 3 | BattlefieldClash: Name. Param. SubText. Desc |
| `ClassChangeTap_Name.csv` | 3 | 3 | ClassChangeTap: Name |
| `DungeonClanTrialGateType_Name.csv` | 2 | 2 | DungeonClanTrialGateType: Name. Description. Story |
| `Faction_Name.csv` | 7 | 0 | Faction: Name. Desc |
| `GuideContentsCategory_Name.csv` | 4 | 3 | GuideContentsCategory: Desc |
| `GuideContentsTag_Name.csv` | 3 | 3 | GuideContentsTag: Desc |
| `GuideGrowthCategory_Name.csv` | 3 | 3 | GuideGrowthCategory: Desc |
| `PKAreaType_Name.csv` | 9 | 3 | PKAreaType: Name |
| `QuestArchiveGroup_Name.csv` | 9 | 3 | QuestArchiveGroup: Name |
| `SpeechBalloonInteraction_Name.csv` | 3 | 3 | SpeechBalloonInteraction: Text |
| `TreasureBoxGroup_Name.csv` | 4 | 0 | TreasureBoxGroup: Name |
| `CollectionCategory_Name.csv` | 4 | 0 | CollectionCategory: Name |
| `ContentsBulk_Name.csv` | 2 | 2 | ContentsBulk: Name |
| `EventFriendInvite_Name.csv` | 1 | 2 | EventFriendInvite: Name. Desc |
| `FieldPointEventRepeatReward_Name.csv` | 9 | 2 | FieldPointEventRepeatReward: RepeatRewardDesc |
| `FieldPointEvent_Name.csv` | 1 | 2 | FieldPointEvent: Name. EventPointName |
| `QuestArchiveCategory_Name.csv` | 2 | 2 | QuestArchiveCategory: Name |
| `QuestCommissionType_Name.csv` | 2 | 2 | QuestCommissionType: CommonName |
| `SectorInvasionGroup_Name.csv` | 3 | 2 | SectorInvasionGroup: InvasionName |
| `Akasha_Name.csv` | 18 | 0 | Akasha: Name |
| `BattlefieldTournamentSeason_Name.csv` | 1 | 1 | BattlefieldTournamentSeason: SeasonTitle |
| `BattlefieldTournament_Name.csv` | 1 | 1 | BattlefieldTournament: Name. Param |
| `DungeonGlobalBoss_Name.csv` | 1 | 1 | DungeonGlobalBoss: BossTitle. BossName. BossDesc. BossOpen |
| `QuestWorldSeason_Name.csv` | 1 | 1 | QuestWorldSeason: SeasonLockMessage |
| `VendingMachine_Name.csv` | 2 | 1 | VendingMachine: Name |
| `WorldSpot_Name.csv` | 942 | 0 | WorldSpot: SpotName |
| `World_Name.csv` | 147 | 0 | World: Name. Param |
| `AchievementPointReward_Name.csv` | 62 | 0 | AchievementPointReward: GradeName |
| `AdventureRecordHint_Name.csv` | 0 | 0 | AdventureRecordHint: Title. HintDesc. Param |
| `Area_Name.csv` | 1.301 | 0 | Area: PlaceName. PlaceDesc. Param |
| `BattlefieldTournamentWorld_Name.csv` | 3 | 0 | BattlefieldTournamentWorld: Name. Param |
| `BattlefieldUnderground_Name.csv` | 6 | 0 | BattlefieldUnderground: Name |
| `ClanFrontierSeason_Name.csv` | 2 | 0 | ClanFrontierSeason: SeasonTitle |
| `ClassChange_Name.csv` | 221 | 0 | ClassChange: Name |
| `EliteDungeonSection_Name.csv` | 16 | 0 | EliteDungeonSection: Name |
| `EventTreasureHuntMission_Name.csv` | 0 | 0 | EventTreasureHuntMission: Desc |
| `FactionMission_Name.csv` | 0 | 0 | FactionMission: Name. Description |
| `FrontierSeason_Name.csv` | 9 | 0 | FrontierSeason: SeasonTitle |
| `GameEvent_Name.csv` | 506 | 0 | GameEvent: Value |
| `InterServerWorld_Name.csv` | 2 | 0 | InterServerWorld: Name |
| `Npc_Name.csv` | 13.516 | 0 | Npc: Title. NumberParam. Name |
| `PartyFiltering_Name.csv` | 33 | 0 | PartyFiltering: Adventure. DifficultyName. Param |
| `ShopGachaFixed_Name.csv` | 0 | 0 | ShopGachaFixed: Desc |
| `TowerOfTitanMission_Name.csv` | 0 | 0 | TowerOfTitanMission: Name. Desc |
| `TownQuickMenu_Name.csv` | 464 | 0 | TownQuickMenu: Name |
| `TrialGateDifficulty_Name.csv` | 3 | 0 | TrialGateDifficulty: DifficultyName |
| `TrialGateGroup_Name.csv` | 10 | 0 | TrialGateGroup: Name |
| `WorldMapArea_Name.csv` | 562 | 0 | WorldMapArea: PlaceName. PlaceParam. AreaDesc |
