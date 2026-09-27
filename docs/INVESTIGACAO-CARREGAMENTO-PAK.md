# Como a instalação v12 funciona

## O que foi reaplicado

A instalação v12 completa foi reaplicada em 2026-09-27, depois de conferir que o PAK principal do jogo estava limpo. Os dois arquivos instalados têm os mesmos hashes dos artefatos preparados e validados com `repak_cli`:

| Arquivo | Destino no jogo | Conteúdo | SHA-256 |
| --- | --- | --- | --- |
| `pakchunk0-Windows-ptbr.pak` | `ProjectTT/Saved/PersistentDownloadDir/DownloadContent/pakchunk0-Windows.pak` | PAK principal de 6.749 entradas, contendo o conteúdo-base extraído e as 227 tabelas PT-BR no caminho correto | `91c7e1993d51d36cd028886e75edc529aa6faf477a5a8f31e58347526bfc79b1` |
| `pakchunk9999-Windows_1_P-ptbr.pak` | `ProjectTT/Content/Paks/pakchunk9999-Windows_1_P.pak` | PAK de patch com as 227 tabelas localizadas | `2711910e4b57b5d57a26d81cdf2d2256cab851b357786fd9ab3ece86de50c197` |

O PAK limpo que estava instalado antes da cópia tinha SHA-256 `21f25c29e5c3fd1dd557f6d27252271c42329d4653e5188b0a1b96e5298fe5ec`. Ele foi preservado em `work/backups/reapply-v12-20260927-142909/` junto com um manifesto da instalação. Nenhuma chave foi incluída no repositório.

## Por que a v12 usa dois arquivos

O processo conhecido do projeto prepara um par porque há duas tarefas distintas:

1. **PAK principal (`pakchunk0-Windows.pak`)**: substitui o PAK correspondente no diretório `Saved/PersistentDownloadDir/DownloadContent`. É uma cópia do pacote completo do jogo, reconstruída com as tabelas da v12 no caminho `ProjectTT/Content/TT/Data/CSV/L10N/en/`. Tem 6.749 entradas.
2. **PAK de patch (`pakchunk9999-Windows_1_P.pak`)**: contém apenas as 227 tabelas da tradução, no diretório padrão `Content/Paks`. O sufixo `_P` sinaliza um patch de prioridade alta no carregamento PAK do Unreal.

As mesmas tabelas estão nos dois pacotes: o PAK principal garante que a versão localizada esteja também no conteúdo usado pelo diretório baixado; o segundo oferece um patch pequeno de alta prioridade sobre os dados montados do jogo. A história do projeto também registra casos de tradução parcial quando o PAK principal e o override continham versões diferentes. Por isso, a regra operacional para instalar a v12 completa é copiar os dois arquivos juntos e manter o mesmo snapshot nos dois.

**Correção de escopo do teste anterior:** o ZIP de um único arquivo testado continha somente o override de alta prioridade. Ele traduziu a tela inicial, mas deixou textos em inglês dentro do jogo. Esse teste prova que o override sozinho não equivale à instalação v12 completa. Ele não testou o par e também não testou um PAK único completo no lugar do pacote principal. A conclusão anterior de que aquele teste invalidava a v12 inteira estava errada; a documentação do projeto foi corrigida.

## Volume e conteúdo da tradução

A pasta `translations/v12-corrections/ProjectTT/Content/TT/Data/CSV/L10N/en/` tem 227 CSVs, 128.598 registros, 486.563 células e 368.441 células não vazias. O número de registros é próximo dos “130 mil textos” usados para descrever o projeto. O snapshot v12 preserva o histórico de versões e acrescenta 91 alterações em relação à v11.

Auditoria da v12 contra a extração original: 227 tabelas, zero tabelas/IDs ausentes ou novos, zero traduções vazias em campos originais não vazios, zero divergências de placeholders/tags, zero alterações nos nomes/templates/parâmetros de títulos de itens e zero menções detectadas de `Giant's Tower` traduzidas. A auditoria identificou dez contextos de `left` para revisão manual; contadores como `AUCTION_MENU_LEFTTIME`, `CLAN_EXCHANGE_LEFT_TIME`, `CLAN_RESEARCH_TOGGLE_ACTIVATE_LEFT_TIME`, `COMMON_LEFT` e `COMMON_LEFT_TIME` estão em português com “restante(s)”.

Uma tela ainda em inglês não significa automaticamente que o PAK não carregou: a imagem de loading de `Pulsing Ridge` usa uma descrição que não aparece nos 227 CSVs atuais, e o próprio nome de área permanece em inglês no snapshot. Isso é uma tarefa de localização separada. Em contraste, rótulos de interface de modo IA têm traduções presentes em `ClientString_Name.csv`.

## Formato validado dos PAKs v12

Ambos são Unreal PAK V11 com índice criptografado, mount point `../../../` e seed `E92532A4`. O principal usa Zlib e 6.749 entradas; o override não comprime as entradas e contém 227. Os dois foram abertos por `repak_cli 0.2.3` com a chave local, e os CSVs extraídos do override coincidiram byte a byte com os 227 CSVs do snapshot.

O Unreal documenta o uso de PAKs de patch montados com prioridade maior e carregamento de conteúdo em chunks; isso é compatível com o par empregado aqui, mas a confirmação desta implementação específica vem dos caminhos e dos testes do projeto. [Como criar um patch no Unreal Engine](https://dev.epicgames.com/documentation/unreal-engine/how-to-create-a-patch-platform-agnostic?application_version=4.27), [argumentos de montagem de PAK](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/PakFile/FPakMountArgs).

## Processo melhorado para manter o par

`tools/build_translation_paks.ps1` agora usa a v12, a árvore completa extraída e a pasta de saída da versão como padrões. Ele empacota ambos com a mesma fonte de CSV, verifica os índices usando a chave local e grava em `../outputs/v12-corrections/`.

```powershell
pwsh -File tools/build_translation_paks.ps1
```

`tools/install_translation.ps1` agora pré-confere as duas fontes e os destinos, guarda backup verificado de ambos os PAKs existentes, prepara e confere as cópias temporárias antes de substituir arquivos, aplica o par e grava um `install-manifest.json`. Se uma substituição falhar, tenta restaurar o par anterior; o manifesto registra sucesso ou falha da restauração.

```powershell
pwsh -File tools/install_translation.ps1
```

O script bloqueia a instalação se Architect, ProjectTT ou DRIMAGE estiverem ativos. Para atualizar o jogo, extrair novas tabelas, comparar IDs, mesclar traduções e auditar, consulte `docs/TECHNICAL_PROCESS.md`.

## Distribuição ao jogador

O PAK principal tem 77 MB e contém milhares de arquivos do próprio jogo; não o publique como download da tradução. O override de 12 MB é somente um dos dois arquivos do procedimento comprovado, portanto também não deve ser oferecido como pacote completo. O repositório mantém os CSVs e as ferramentas de manutenção; a página de instalação não aponta um download até haver um pacote que possa ser distribuído e instalado em uma instalação limpa sem compartilhar os arquivos originais do jogo.

Uma futura opção de um arquivo deve ser tratada como uma nova hipótese de empacotamento e testada separadamente. Qualquer teste deve distinguir: override sozinho em `Content/Paks`; PAK principal sozinho em `DownloadContent`; par completo. Não misture resultados desses três casos.
