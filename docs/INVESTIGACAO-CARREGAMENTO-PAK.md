# Investigação: por que foram usados dois arquivos PAK?

## Conclusão atual

Ainda não está provado que a tradução precise de dois arquivos, nem que um PAK único seja suficiente. O teste já feito prova somente que um PAK de prioridade alta, colocado em `ProjectTT/Content/Paks`, pode ser aberto pelo jogo sem crash e traduz a tela inicial. O mesmo teste deixou a tela de carregamento e textos vistos dentro do jogo em inglês. Portanto, esse ZIP de um arquivo não é uma instalação completa e não deve ser distribuído como tal.

O nome “dois arquivos” descreve a arquitetura que vinha sendo usada no computador de desenvolvimento:

1. `pakchunk0-Windows.pak` substitui o PAK da pasta `Saved/PersistentDownloadDir/DownloadContent`. A cópia preparada inclui a árvore original completa do PAK e as tabelas de localização alteradas.
2. `pakchunk9999-Windows_1_P.pak` é um PAK adicional com as 227 tabelas localizadas, instalado em `Content/Paks` com sufixo `_P`, que o Unreal usa para dar prioridade a patches.

As mesmas tabelas aparecem nos dois PAKs. Isso foi uma medida para cobrir duas fontes/camadas de conteúdo que já vinham sendo atualizadas separadamente durante os testes anteriores. Ainda não há prova suficiente de que o cliente do jogo sempre carregue ambas essas fontes, nem de qual delas serve cada tela. Não se deve explicar aos jogadores que os dois são indispensáveis até terminar a matriz de testes abaixo.

## Evidências coletadas

| Teste / evidência | Resultado | O que permite concluir |
| --- | --- | --- |
| Instalação sem tradução, com o PAK original restaurado | A tela inicial apareceu em inglês. | A localização vista depois não era uma preferência persistente de idioma do perfil do jogador. |
| Apenas `pakchunk9999-Windows_1_P.pak` em `Content/Paks` | O jogo iniciou sem erro de índice PAK; a tela inicial apareceu em português. | O índice e o caminho do pacote eram legíveis e ao menos parte das tabelas foi usada. |
| Mesmo teste, depois de entrar no jogo | A tela de carregamento `Pulsing Ridge` e vários textos de interface continuaram em inglês. | O override isolado não entrega a tradução completa. O teste não prova sozinho se a causa é precedência de conteúdo, carregamento tardio ou strings ainda não traduzidas. |
| Conteúdo do override | O pacote contém 227 CSVs e a extração conferiu com o snapshot da versão. `ClientString_Name.csv` contém traduções para `DISCONNECTED_PLAY_RESULT`, `DISCONNECTED_PLAY_TIME`, `DISCONNECTED_PLAY_ACQUIRED_EXP`, `DISCONNECTED_PLAY_ACQUIRED_GOLD` e `DISCONNECTED_PLAY_ACQUIRED_ITEM`. | Pelo menos aqueles rótulos em inglês não se explicam por ausência dessas linhas na fonte do patch. Ainda falta provar qual tabela o runtime usou após entrar no mundo. |
| Fonte de `Loading_Name.csv` | Entradas de `Pulsing Ridge` continuam em inglês. | Parte da tela mostrada na imagem não poderia ficar traduzida com o snapshot atual, mesmo que o PAK certo tivesse sido carregado. É uma lacuna de tradução separada do problema de carregamento. |
| Texto descritivo da tela de carregamento | A frase exibida na imagem (`A place where you can admire Ridges with bizarre elevations.`) não foi encontrada nos 227 CSVs do snapshot. | A descrição também precisa ser localizada em outro asset/tabela antes de usá-la como teste de precedência. Não está demonstrado ainda se esse texto é extraível/editável pelo método atual. |
| Inspeção das chaves inglesas de contador | `AUCTION_MENU_LEFTTIME`, `CLAN_EXCHANGE_LEFT_TIME`, `CLAN_RESEARCH_TOGGLE_ACTIVATE_LEFT_TIME`, `COMMON_LEFT` e `COMMON_LEFT_TIME` usam “Tempo/quantidade restante(s)” na fonte v12. | A correção de `left` como tempo restante está presente nos CSVs atuais. As antigas imagens com “à esquerda” vieram de um pacote anterior ou de conteúdo que o override testado não substituiu; só um teste de interface dessas chaves pode determinar qual. |
| Recursos binários de localização Unreal | `tools/locres_export.py` exporta LocRes UE v0–v3 para CSV/JSON. O arquivo `Game.locres` extraído não contém entradas e o `Engine.locres` analisado não contém os rótulos exatos de modo IA offline. | Os rótulos testados pertencem às tabelas CSV customizadas do jogo, não ao conjunto de strings genéricas de `Engine.locres`. A localização dos textos ausentes da tela de carregamento segue em aberto. |
| Arquivos do jogo | O jogo possui um PAK em `Saved/PersistentDownloadDir/DownloadContent`, além de PAKs e contêineres IoStore em `Content/Paks`. | Existem diretórios e formatos diferentes a considerar; isto, sozinho, não demonstra a precedência real das tabelas do jogo. |

Os documentos da Unreal explicam que PAKs de patch são montados com prioridade maior e que arquivos em diretórios de busca podem ser montados automaticamente. A documentação também descreve carregamento/montagem assíncrona de chunks. Isso torna plausível que conteúdo carregado depois do menu afete a observação, mas **não comprova** que Architect usa exatamente esse fluxo para estas tabelas: o projeto fonte e os logs detalhados de montagem do jogo não estão disponíveis. [Como criar um patch no Unreal Engine](https://dev.epicgames.com/documentation/unreal-engine/how-to-create-a-patch-platform-agnostic?application_version=4.27), [API de montagem de PAK](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/PakFile/FPakMountArgs), [ChunkDownloader](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/ChunkDownloader/FChunkDownloader).

## Testes que faltam para decidir entre um e dois PAKs

Executar cada caso com cópias limpas e fazer hash antes/depois. Fechar o jogo e o launcher antes de cada troca; restaurar os arquivos originais ao fim. Capturar tela do menu, carregamento e os mesmos textos dentro do mundo.

| Caso | Arquivo alterado | Pergunta respondida |
| --- | --- | --- |
| A | Apenas o PAK completo traduzido no lugar do `pakchunk0-Windows.pak` de `DownloadContent`; nenhum override | O arquivo completo cobre sozinho o menu e o runtime? |
| B | Apenas o override localizado em `Content/Paks`, com o PAK original limpo em `DownloadContent` | Resultado de referência já observado; repetir com a mesma conta e registrar exatamente quais telas mudam. |
| C | PAK completo traduzido em `DownloadContent` + override localizado em `Content/Paks` | O par resolve o runtime, ou continua havendo textos ingleses? |
| D | Apenas um PAK localizado em `DownloadContent`, sem copiar o conteúdo original do jogo | O scanner considera PAK adicional naquele caminho e usa sua tabela? Este teste deve ser feito em ambiente reversível, pois o nome `pakchunk0-Windows.pak` colide com o pacote base. |

Usar como sondas strings exatas que já têm tradução no CSV (`Resultado do modo IA offline`, `Tempo de jogo`, `Recursos obtidos`) e uma tela de carregamento cuja região tenha tradução feita de propósito. Hoje, `Pulsing Ridge` ainda está inglês em `Loading_Name.csv`, então essa string não serve para decidir precedência até que a fonte seja corrigida. Registrar se o idioma se altera após login, troca de mapa e reinício. Se o caso A já traduzir as interfaces após entrar no mundo, um arquivo pode bastar para distribuição, embora o pacote tenha 77 MB e contenha o conteúdo completo do jogo. Se só C funcionar, são necessários dois arquivos, ou uma forma segura de combinar os dois conteúdos num único PAK.

## O que não fazer

- Não publicar o ZIP experimental `Architect-PTBR-v12-beta.zip` como tradução completa. Foi retirado da pasta pública de releases; a cópia de trabalho original permanece em `outputs` para análise.
- Não distribuir o PAK completo de 77 MB sem antes revisar os direitos e o conteúdo: ele inclui milhares de arquivos originais do jogo, além das tabelas alteradas.
- Não substituir o PAK original do jogador durante a investigação sem backup verificável e plano de restauração.
- Não publicar a chave AES. Ela só serve às tarefas de manutenção do PAK e permanece em `work/.architect-aes-key`, fora do repositório.
- Não considerar “o jogo abriu sem crash” como validação da tradução. Isso só confirma que o caso testado não falhou ao iniciar.

## Regra para a próxima distribuição

Só oferecer instruções de instalação quando o pacote resultante passar pelos casos mínimos de carregamento, contiver uma tradução para as sondas de menu, carregamento e partida, e tiver sido removido/restaurado com sucesso. Até lá, a página de instalação informa claramente que nenhum download está pronto.
