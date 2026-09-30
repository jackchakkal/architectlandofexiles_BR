"""Registra a revisão editorial da atualização do jogo de 30/09/2026."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
previous = json.loads((root / 'changes/v13-to-v14/overrides.json').read_text(encoding='utf-8'))
rules = {key: value for key, value in previous.items() if key.startswith('__')}
overrides = {'_comment': 'v15: revisão manual dos conteúdos novos e dos 27 textos-fonte alterados. Nomes próprios, produtos e eventos nomeados permanecem em inglês.'}
overrides.update(rules)

def add(table, ident, **columns):
    overrides.setdefault(table, {}).setdefault(str(ident), {}).update(columns)

def phrase(table, column, english, portuguese):
    overrides.setdefault('__by_text__', {}).setdefault(table, {}).setdefault(column, {})[english] = portuguese

# Novos títulos e coleções. Os nomes de itens e produtos comerciais continuam em inglês.
for ident, desc in [
    (6001, 'Campeão do Monolith Clan Tournament'),
    (6002, '2º lugar no Monolith Clan Tournament'),
    (6003, '3º lugar no Monolith Clan Tournament'),
    (6004, '4º lugar no Monolith Clan Tournament'),
]: add('CharacterTitle_Name.csv', ident, Description=desc)
for ident, name in [
    (310262, 'Destino da Profecia Ressonante {Param}'),
    (732072, 'Coleção do Explorer'),
    (732073, 'Item estimado do Explorer'),
    (732074, 'Tesouro do Explorer'),
    (732075, 'Espólios do Explorer'),
    (732076, 'Legado do Explorer'),
]: add('CollectionMain_Name.csv', ident, Name=name)

# Interface dos eventos novos: títulos descritivos traduzidos; Naruru Dice Festival é nome de evento.
add('EventAttendance_Name.csv', 20340, PageName='Check-in da 1ª temporada da Arena', PageDesc='Faça check-in todos os dias para receber recompensas exclusivas.')
banner = ('Uma anomalia causada pela Incursão alterou a frequência de aparecimento dos monstros e a obtenção de itens.\r\n\r\n'
          ' : Grande Incursão adicional (todos os dias às 18h, UTC+9)\r\n'
          ' : Mais Incursões simultâneas\r\n'
          ' : Obtenha restos que podem ser trocados nas Incursões\r\n\r\n'
          'Troque os restos da Incursão por recompensas no evento de troca.')
add('EventBanner_Name.csv', 5065, Desc=banner)
add('EventBanner_Name.csv', 5031, Desc=('Uma anomalia de Incursão alterou a frequência de aparecimento dos monstros e a obtenção de itens.\r\n\r\n'
    '; Grande Incursão adicional (todos os dias às 18h, UTC+9)\r\n'
    ': Mais Incursões simultâneas:\r\n'
    '; Obtenha restos que podem ser trocados nas Incursões\r\n'
    '; Evento Double Unknown Fragments ativado.\r\n\r\n'
    'Troque os restos da Incursão por recompensas no evento de troca.'))
add('EventDice_Name.csv', 1006, ToolTipString=("Colete até 20 <Yellow>[Name]</> por dia na Forsaken Land e na Giant's Tower.\r\n"
    'Se tirar <Yellow>[6], você ganha uma jogada extra</>!'))
add('EventDrop_Name.csv', 1017, PageName='Obtendo Naruru Dice', PageDesc=("Derrote monstros na Forsaken Land e na Giant's Tower!\r\n"
    'Você poderá obter Naruru Dice como recompensa.'))
add('EventMission_Name.csv', 11070, PageName='Missões da Replica Seed', PageDesc='Participe da Replica Seed e resgate suas recompensas!')
add('EventMission_Name.csv', 11110, PageName='Missões da Arena')
for ident, name in [
    (137, 'Check-in da 1ª temporada da Arena'), (1107, 'Missões da Replica Seed'),
    (1111, 'Missões da Arena'), (6018, 'Obtendo Naruru Dice'),
]: add('EventTab_Name.csv', ident, TabName=name)
phrase('EventMissionRecord_Name.csv','Name','Participate in Replica Seed','Participe da Replica Seed')
phrase('EventMissionRecord_Name.csv','Desc','Participate in Replica Seed {RequiredStackCount} time(s)','Participe da Replica Seed {RequiredStackCount} vez(es)')
phrase('EventMissionRecord_Name.csv','Name','Defeat Incursion/Grand Incursion Monsters','Derrote monstros de Incursão ou Grande Incursão')
add('QuestFactionGroup_Name.csv', 15, Desc='Visão geral da Explorers Guild')

# A narrativa apresenta Orica, Bailiegh, Nicolas e a pesquisa da Replica Seed.
for ident, name, desc in [
    (515010, 'Uma presa fácil', 'A pedido de Orica, o aventureiro visita a Explorers Guild.\r\nEle concorda em ajudar em troca de informações sobre o grupo de mercenários.'),
    (515020, 'Faça o que mandam', 'O aventureiro conhece Bailiegh, vice-mestre da Explorers Guild, e o ajuda na pesquisa da Replica Seed.'),
    (515030, 'Entre o real e o falso', 'Nicolas se arrisca para impressionar Bailiegh.\r\nO aventureiro o ajuda a coletar essências de Karugura.'),
    (515040, 'Vamos com calma', 'O aventureiro e Bailiegh seguem para Great Arbor Domain em busca de essências de Tagar.'),
    (515050, 'Terapia do espelho', 'Apesar da confusão causada por Nicolas, o aventureiro consegue manifestar Tagar com a Replica Seed.'),
]: add('Quest_Name.csv', ident, Name=name, DescNotCompleted=desc)

tasks = {
 'Speak with Orica':'Fale com Orica',
 'Wait for Orica to finish the call':'Espere Orica terminar a ligação',
 'Go to the Magobi Encampment':'Vá para Magobi Encampment',
 'Observe Surroundings':'Observe os arredores',
 'Speak with Zeyhan':'Fale com Zeyhan',
 'Pass through the Valley of Beasts':'Atravesse Valley of Beasts',
 'Go to the Gorge of Perdition':'Vá para Gorge of Perdition',
 'Go towards the voice':'Siga na direção da voz',
 'Observe quietly':'Observe em silêncio',
 'Speak with Bailiegh':'Fale com Bailiegh',
 'Sign the document on an impulse':'Assine o documento sem pensar muito',
 'Go with Bailiegh':'Acompanhe Bailiegh',
 'Go to the area where essences can be found':'Vá até onde há essências',
 'Defeat incoming monsters':'Derrote os monstros que se aproximam',
 'Collect essence fragments':'Colete fragmentos de essência',
 'Climb the ruins':'Suba pelas ruínas',
 'Return to Bailiegh':'Volte até Bailiegh',
 'Go to the frightened guild member':'Vá até o membro assustado da guilda',
 'Speak with the frightened guild member':'Fale com o membro assustado da guilda',
 'Move in the direction Nicolas indicated':'Siga na direção indicada por Nicolas',
 'Defeat the interfering monsters':'Derrote os monstros que atrapalham a busca',
 'Collect Factor':'Colete o fator',
 'Go to Bailiegh':'Vá até Bailiegh',
 'Go to the place Bailiegh mentioned':'Vá ao local indicado por Bailiegh',
 'Manipulate Replica Seed':'Ative a Replica Seed',
 'Manipulate the Replica Seed again':'Ative a Replica Seed novamente',
 'Go to the Great Arbor Domain':'Vá para Great Arbor Domain',
 'Go to the Kuduru Territory':'Vá para Kuduru Territory',
 'Go to Nicolas':'Vá até Nicolas',
 'Speak with Nicolas':'Fale com Nicolas',
 'Descend to the ground':'Desça até o chão',
 'Follow the traces of the Naruru':'Siga os rastros do Naruru',
 'Comfort the sobbing Naruru':'Conforte o Naruru que está chorando',
 'Speak with the sobbing Naruru':'Fale com o Naruru que está chorando',
 'Move near the water':'Aproxime-se da água',
 'Collect Tagar essences':'Colete essências de Tagar',
 'Defeat the monsters interfering with collection':'Derrote os monstros que atrapalham a coleta',
 'Appearance of Nicolas and the Naruru':'Nicolas e o Naruru aparecem',
 'Hand over the Replica Seed':'Entregue a Replica Seed',
 'Observe Bailiegh':'Observe Bailiegh',
 'Go to the area with essences':'Vá até a área das essências',
 'Go to the Tagar essence':'Vá até a essência de Tagar',
 'Use the Replica Seed':'Use a Replica Seed',
 'Defeat the Tagar replica':'Derrote a réplica de Tagar',
 'Reach Babylon':'Chegue a Babylon',
 'Go to the Explorers’ Guild':'Vá para Explorers Guild',
}
for en,pt in tasks.items(): phrase('QuestTask_Name.csv','TaskName',en,pt)

# Descrições de itens novos. O nome comercial do item continua como consta no jogo.
add('Item_Name.csv', 8021001, Desc='Caixa concedida ao alcançar {Param1} pontos ou mais na previsão de rodadas do torneio de clãs.')
add('Item_Name.csv', 9000065, Desc='{Param1} dado(s).\r\nDerrote monstros para obtê-los\r\ne use-os no evento Naruru Dice Festival.')
add('Item_Name.csv', 9000066, Desc='Fragmentos caídos dos portais da Grande Incursão.\r\nTroque-os por recompensas no evento de troca de restos da Incursão.')
add('Item_Name.csv', 9000067, Desc='Tesseract of Silence {Param1}.\r\nPode ser trocado por recompensas no evento de troca de restos da Incursão.')
add('RewardAcquisitionLimit_Name.csv', 1020, RewardLimitGroupDesc="Obtido diariamente ao derrotar monstros na Forsaken Land e na Giant's Tower")
add('ShopAccumSetting_Name.csv', 112002, Name='Loja diária')
add('ShopTab_Name.csv', 112002, TabName='Loja diária')

# Mudanças de texto da atualização: o próprio jogo passou a chamar apostas de "Cheer".
add('BadgeNotification_Name.csv', 'AirVehicle_PossibleSummon', Param='Planador')
add('BadgeNotification_Name.csv', 'ViewUI_BattlefieldTournamentBetResult', Message='Torcida da rodada {Param}: abertura e resultados')
add('BadgeTask_Name.csv', 10157, Name='Aviso de abertura da torcida da rodada')
add('BadgeTask_Name.csv', 10158, Name='Aviso dos resultados da torcida da rodada')
cheer = {
 'BATTLEFIELD_TOURNAMENT_MENU_ROUND_BETTING':'Torcida do torneio',
 'BATTLEFIELD_TOURNAMENT_PREDICT_BET_TITLE':'Torcida do torneio [Round]',
 'BATTLEFIELD_TOURNAMENT_PREDICT_BET_LEFT_TIME':'Torcida encerra em: [Time]',
 'BATTLEFIELD_TOURNAMENT_PREDICT_BET_END':'Torcida encerrada',
 'BATTLEFIELD_TOURNAMENT_PREDICT_BET__ROUND_ALL_CLANS_SELECT_REQUIRED':'Preveja o resultado de todas as partidas listadas para participar da torcida do torneio.',
 'BATTLEFIELD_TOURNAMENT_PREDICT_BET_RESULT_NOT_YET_AVAILABLE':'O resultado da torcida não está disponível porque a partida desta rodada não foi disputada.',
 'BATTLEFIELD_TOURNAMENT_BETTING_RULE_DESC_1':'Pague a taxa de inscrição para torcer pelo clã que, na sua previsão, vencerá cada partida das rodadas de qualificação.\r\n(Todas as taxas de inscrição entram no prêmio total, junto com prêmios extras do sistema.)',
 'BATTLEFIELD_TOURNAMENT_BETTING_RULE_DESC_2':'Você pode participar da torcida até o início da partida da rodada. Durante o período de participação, pode cancelar a escolha e receber a taxa de inscrição de volta.',
 'BATTLEFIELD_TOURNAMENT_BETTING_RULE_DESC_7':'Se houver uma nova rodada de escolha, quem já participou pode fazer outra previsão sem pagar. Se não escolher novamente, sua torcida irá para o clã com a maior porcentagem de votos.',
 'BATTLEFIELD_TOURNAMENT_BET_REWARD':'Recompensas da torcida do torneio',
 'BATTLEFIELD_TOURNAMENT_BET_RULE':'Regras da torcida',
 'BATTLEFIELD_TOURNAMENT_BETTING_ENTRY':'Participar da torcida',
 'BATTLEFIELD_TOURNAMENT_BETTING_CANCEL':'Cancelar torcida',
 'BATTLEFIELD_TOURNAMENT_BETTING_COST':'Custo da torcida',
 'BATTLEFIELD_TOURNAMENT_PREDICT_BET_BEFORE_BRACKET_CONFIRMATION':'Antes do início da torcida',
 'GM_NICKNAME_PREFIX':'0',
}
for ident,value in cheer.items(): add('ClientString_Name.csv',ident,Value=value)
add('Mail_Name.csv',1057, Title='Recompensa da torcida do torneio: #[Rank]', Content=('Sua recompensa pelo #[Rank] lugar nos resultados da torcida de [TournamentName] foi enviada pelo correio.\r\n'
    'Recompensa total: [TotalReward]\r\nTaxa de distribuição do #[Rank] lugar: [Rate]%\r\nParticipantes no #[Rank] lugar: [Count]\r\n'
    '※ Se não houver jogadores classificados em uma posição, a parte correspondente do prêmio será dividida igualmente entre as demais posições válidas. A distribuição final pode diferir da taxa inicial.'))
add('Mail_Name.csv',1059, Content=('Sua previsão do clã campeão de [TournamentName] estava incorreta. Sua recompensa foi enviada pelo correio.\r\n'
    'Sua previsão: [PickClanName]\r\nClã campeão: [WinnerClanName]'))
add('QuestWorldSeason_Name.csv','Dungeon/InterServer/InterServer01/InterServer',SeasonLockMessage=('A temporada de Abyssal Battlefield terminou.\r\nVocê poderá entrar quando a próxima temporada começar.'))
add('ResultCodeString_Name.csv',30405,Value='Você já participou da torcida deste torneio.')
add('ResultCodeString_Name.csv',30406,Value='Você não participou da torcida do torneio Monolith War.')
add('ResultCodeString_Name.csv',30407,Value='O custo da torcida do torneio Monolith War ainda não foi definido.')

target = Path(__file__).with_name('overrides.json')
target.write_text(json.dumps(overrides,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(target, 'tabelas:', len([x for x in overrides if not x.startswith('_')]))
