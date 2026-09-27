# Tradução PT-BR do Architect — procedimento reproduzível

Este documento descreve a estrutura da tradução instalada, como extrair e editar as tabelas, como gerar os arquivos `.pak`, como instalá-los e como reverter a instalação. O procedimento foi preparado para Windows/PowerShell.

## Estado técnico e cautela de distribuição

- Snapshot de tradução: `v12-corrections` (227 CSVs auditados). Dois PAKs foram preparados e instalados temporariamente em 2026-09-27, mas o teste com apenas o PAK de override traduziu somente a tela inicial. O jogo foi então restaurado ao estado limpo. A distribuição v12 está bloqueada até a investigação em `docs/INVESTIGACAO-CARREGAMENTO-PAK.md` concluir a matriz de testes.
- Ferramenta de PAK: `repak_cli 0.2.3`, código-fonte em `work/repak` e executável em `work/repak/target/release/repak.exe`.
- O pacote principal contém 6.749 arquivos; o pacote de localização contém 227 tabelas CSV.
- Os dois arquivos usam formato Unreal PAK V11, índice criptografado, mount point `../../../` e path hash seed `E92532A4`.
- O pacote principal usa compressão Zlib. O pacote de localização usa entradas sem compressão, como a versão funcional anterior.
- Os arquivos preparados estão em `outputs/v12-corrections/pakchunk0-Windows-ptbr.pak` e `outputs/v12-corrections/pakchunk9999-Windows_1_P-ptbr.pak`.
- SHA-256 do pacote principal v12: `91c7e1993d51d36cd028886e75edc529aa6faf477a5a8f31e58347526bfc79b1`.
- SHA-256 do pacote de localização v12: `2711910e4b57b5d57a26d81cdf2d2256cab851b357786fd9ab3ece86de50c197`.
- Backups de testes e originais estão em `work/backups/`; confira os hashes e leia o manifesto antes de restaurar qualquer arquivo.
- A auditoria reproduzível da v12 está em `docs/AUDIT-v12.json`; o resumo está em `releases/v12-corrections/manifest.json`.
- O manifesto da v12 preparada está em `releases/v12-corrections/manifest.json`. Ele registra os hashes dos PAKs de manutenção; eles não são um pacote de jogador validado.

## Aplicativos e dependências

- Windows e PowerShell (os exemplos usam caminhos e comandos PowerShell).
- Python 3.11 ou compatível; os scripts usam a biblioteca padrão, sem pacote Python adicional.
- `repak_cli 0.2.3` para manipular os PAKs.
- `tools/locres_export.py` exporta recursos binários LocRes UE v0–v3 para CSV/JSON na investigação de strings fora das tabelas CSV customizadas.
- Rust/Cargo somente se precisar compilar o repak a partir do código-fonte. Na pasta `work/repak`, execute `cargo build --release -p repak_cli`; o executável será `work/repak/target/release/repak.exe`.
- Não é necessário abrir o Unreal Editor para editar essas tabelas CSV.
- O jogo foi compilado com Unreal Engine 5.5 (indicado pelo relatório de crash fornecido); seus arquivos PAK usam versão V11. Confirme a versão do PAK com `repak info` depois de atualizações do jogo.

## Arquivos e função de cada um

| Arquivo ou pasta | Função |
| --- | --- |
| `work/.architect-aes-key` | Credencial local AES-256, em 64 caracteres hexadecimais. É necessária para ler e criar estes PAKs. Não publicar, enviar por chat, incluir em documentação compartilhada ou commitar no Git. |
| `work/repak/target/release/repak.exe` | Extrai, lista, inspeciona e empacota arquivos `.pak`. |
| `work/download-pak0-original/ProjectTT/Content/TT/Data/CSV/L10N/en/` | Cópia de referência das 227 tabelas originais em inglês, extraídas antes das traduções. Serve para comparar IDs, nomes oficiais, parâmetros de nomes, placeholders e texto-fonte. |
| `translations/v12-corrections/ProjectTT/Content/TT/Data/CSV/L10N/en/` no repositório (snapshot público e fonte local atual) | Tabelas PT-BR finais editáveis. É a fonte do pacote de localização. |
| `work/download-pak0-full-v11/` | Árvore completa de 6.749 arquivos que forma o pacote principal. Foi derivada da árvore integral v10 e recebeu as tabelas PT-BR v11. |
| `work/v12-override/` | Árvore de 227 tabelas para o pacote de localização de prioridade alta. Recebe as mesmas tabelas v11. |
| `outputs/` | PAKs preparados, antes de instalá-los no jogo. |
| `ProjectTT/Saved/PersistentDownloadDir/DownloadContent/pakchunk0-Windows.pak` | Destino experimental do pacote principal; a versão preparada é uma cópia integral da árvore do jogo com as tabelas editadas. Não substituir o original sem backup verificado. |
| `ProjectTT/Content/Paks/pakchunk9999-Windows_1_P.pak` | Destino experimental do PAK com as tabelas de localização de prioridade alta. Sozinho, não traduziu toda a interface. |

Os CSVs permanecem no diretório `L10N/en` porque esse é o caminho de localização usado pelo pacote original e pela instalação atual. O jogo carrega os textos dessas tabelas em runtime.

## Credencial AES e acesso por outra IA

A chave local é uma credencial do jogo para criptografar e descriptografar o índice dos PAKs. Ela está em `work/.architect-aes-key`, em hexadecimal (64 caracteres, 32 bytes). Uma IA que execute o processo neste mesmo workspace pode ler esse arquivo localmente. Para outro computador ou workspace, transfira a credencial por um canal privado e seguro e grave-a nesse caminho; não copie o valor da chave para este documento, para o histórico de conversa ou para repositório público.

A chave correta foi identificada como o candidato de índice `650` na lista local `work/content-key-candidates.json` e confirmada tentando ler PAKs conhecidos com `repak info`/extração. Essa lista e os arquivos de sondagem são material local de trabalho e não estão no repositório. Não use uma chave de outro jogo: a primeira tentativa de empacotamento com uma chave alheia produziu índice inválido e o Unreal encerrou o jogo com `Corrupt pak index detected`. A chave deve sempre ser validada em um PAK que abre corretamente antes de gerar um pacote instalável.

No PowerShell, carregue-a apenas durante os comandos que precisam dela e remova a variável ao terminar:

```powershell
$key = (Get-Content work/.architect-aes-key -Raw).Trim()
# comandos repak que usam --aes-key $key
Remove-Variable key
```

Não é necessário login, senha de conta ou token de serviço para editar e empacotar os CSVs. A credencial necessária é a chave AES acima. A chave não deve ser confundida com uma chave de API.

## Formato das tabelas

- CSV em UTF-8 com BOM e finais de linha CRLF.
- Aspas e vírgulas seguem o escape CSV padrão; textos com vírgulas ou quebras de linha ficam entre aspas.
- Os nomes dos arquivos e das colunas, a ordem dos campos, os IDs e os placeholders devem ser preservados.
- Os placeholders (`{Param1}`, `{IntParam}`, `[Time]`, `[Value]`, `[Name]` etc.) são variáveis do jogo. Não os traduza nem remova.
- Tags como `<Orange>texto</>`, `<Yellow>texto</>` e `<EpicMain>texto</>` controlam cor/formatação. Mantenha a tag de abertura e o fechamento, sem inserir espaços que alterem sua sintaxe.
- Grave as tabelas com BOM; não converta para ANSI/Windows-1252.

## Regras editoriais obrigatórias

1. **Nomes próprios de itens:** todo valor de `Item_Name.Name` deve ser copiado da tabela original. Quando o nome contém placeholders, os valores `ParamN` referenciados pelo campo `Name` também devem ficar iguais ao original. Isso mantém nomes de equipamento, consumíveis, materiais e demais itens iguais no inventário e no Marketplace, inclusive para pesquisa.
2. **Nomes de monstros, chefes e NPCs:** preserve os campos de nome próprios nas tabelas correspondentes (`Npc_Name`, `GuideBoss_Name`, `DungeonGlobalBoss_Name` e parâmetros de nomes). Traduza descrições, objetivos e explicações ao redor, não os nomes.
3. **Giant's Tower:** preserve o nome original `Giant's Tower` em todas as menções (alguns campos originais usam apóstrofo tipográfico `’`). Traduza o restante da frase e os andares, mantendo tags e variáveis.
4. **Nomes de masmorras:** mantenha os nomes oficiais originais das masmorras.
5. **Termos fixos:** mantenha `Skill` e `Codex` em inglês.
6. **Tempo restante:** em formatos de contador, o inglês `left` significa tempo/quantidade restante. Use `restante(s)`, nunca `à esquerda`. Preserve traduções direcionais como “à esquerda” quando o contexto realmente indicar direção.
7. **Acessórios:** traduza a posição de forma natural e com contração correta: “equipado no dedo”, “equipado no pescoço”, “equipado na orelha”, “equipado no braço”.
8. **Gênero e concordância:** ajuste gênero em falas de NPCs que se dirigem à personagem feminina mostrada pelo usuário. Não mude automaticamente referências a personagens de outro gênero nem usos genéricos.
9. **Português:** revisar ordem das palavras, regência, concordância e pontuação; não fazer tradução literal palavra por palavra.

## Extração de arquivos

### 1. Confirmar os arquivos de origem

O PAK integral deve estar disponível localmente. A instalação tem um backup anterior às traduções em `work/backups/download-pakchunk0-Windows-original-before-v5.pak`. Preserve uma cópia intocada do pacote original antes de qualquer nova extração ou instalação.

Confira o índice e o formato:

```powershell
$key = (Get-Content work/.architect-aes-key -Raw).Trim()
work/repak/target/release/repak.exe --aes-key $key info work/backups/download-pakchunk0-Windows-original-before-v5.pak
```

### 2. Extrair um PAK inteiro

```powershell
$key = (Get-Content work/.architect-aes-key -Raw).Trim()
work/repak/target/release/repak.exe --aes-key $key unpack `
  -o work/extracted-original `
  work/backups/download-pakchunk0-Windows-original-before-v5.pak
Remove-Variable key
```

O prefixo `../../../` é removido por padrão. As tabelas ficam então em `work/extracted-original/ProjectTT/Content/TT/Data/CSV/L10N/en/`.

Para extrair somente tabelas selecionadas, use `-i` repetidamente:

```powershell
$key = (Get-Content work/.architect-aes-key -Raw).Trim()
work/repak/target/release/repak.exe --aes-key $key unpack `
  -o work/extracted-selected `
  -i ProjectTT/Content/TT/Data/CSV/L10N/en/Item_Name.csv `
  -i ProjectTT/Content/TT/Data/CSV/L10N/en/QuestTask_Name.csv `
  work/backups/download-pakchunk0-Windows-original-before-v5.pak
Remove-Variable key
```

Use `repak list` para consultar caminhos de arquivos do pacote. `repak info` mostra versão, compressão, seed e quantidade de entradas.

### 3. Manter a referência original

Não edite a árvore original. Guarde a cópia limpa das tabelas em `work/download-pak0-original/ProjectTT/Content/TT/Data/CSV/L10N/en/`. Compare por ID, nunca apenas pela posição da linha. Antes de cada instalação, faça cópia de segurança dos dois PAKs ativos.

## Edição e preparação da tradução

### 1. Editar as tabelas

Edite os arquivos em `translations/v12-corrections/ProjectTT/Content/TT/Data/CSV/L10N/en/` no repositório (snapshot público e fonte local atual). Cada tabela contém IDs e tipos de texto diferentes; não renomeie tabelas ou colunas.

As correções históricas da v11 foram preparadas por um script local que dependia de arquivos de pesquisa não publicados; esse script não faz parte do repositório e não é necessário para continuar. Para reproduzir o estado atual, use o snapshot v12 versionado e confira o diff de 91 células em `changes/v11-to-v12-corrections/changes.json`. Para versões futuras, o fluxo reproduzível está nos scripts `tools/compare_localization.py`, `tools/merge_updated_tables.py`, `tools/audit_translation.py` e `tools/build_translation_paks.ps1`.

### 2. Sincronizar as duas árvores de empacotamento

O fluxo de manutenção gera os dois PAKs com as mesmas tabelas, mas ainda não está demonstrado que ambos sejam indispensáveis. O teste com o PAK de prioridade alta sozinho traduziu a tela inicial e deixou telas de jogo em inglês; não se pode atribuir esse resultado só à ordem de montagem, pois há lacunas no snapshot e possível carregamento tardio de conteúdo. Veja `docs/INVESTIGACAO-CARREGAMENTO-PAK.md` antes de instalar ou recomendar qualquer pacote.

```powershell
@'
from pathlib import Path
import shutil
w=Path('work')
rel=Path('ProjectTT/Content/TT/Data/CSV/L10N/en')
stage=w/'architect-ptbr-v11'/rel
for root in [w/'download-pak0-full-v11', w/'architect-ptbr-pakroot-v11']:
    for table in stage.glob('*.csv'):
        shutil.copy2(table, root/rel/table.name)
'@ | python -
```

`download-pak0-full-v11` é a árvore integral (6.749 arquivos), derivada do conteúdo completo v10. `architect-ptbr-pakroot-v11` contém apenas as 227 tabelas de localização. Para reproduzir exatamente a versão instalada, use essas árvores já preparadas; não monte o pacote principal a partir de uma árvore incompleta de CSVs.

## Empacotamento

Use o `repak_cli 0.2.3` que acompanha o projeto e a chave AES local. O principal e o override têm configurações de compressão diferentes:

```powershell
$key = (Get-Content work/.architect-aes-key -Raw).Trim()

work/repak/target/release/repak.exe --aes-key $key pack `
  work/download-pak0-full-v11 `
  outputs/v12-corrections/pakchunk0-Windows-ptbr.pak `
  --version V11 --compression Zlib --path-hash-seed 3911529124 --quiet

work/repak/target/release/repak.exe --aes-key $key pack `
  work/architect-ptbr-pakroot-v11 `
  outputs/v12-corrections/pakchunk9999-Windows_1_P-ptbr.pak `
  --version V11 --path-hash-seed 3911529124 --quiet

Remove-Variable key
```

O seed decimal `3911529124` equivale a `E92532A4`. `repak` cria um índice criptografado quando recebe `--aes-key`. Não use compressão no pacote `pakchunk9999` sem primeiro validar com a versão de formato usada pelo jogo: o pacote funcional de correção usa compressão `None`.

## Validação antes da instalação

Inspecione ambos os arquivos e confirme V11, índice criptografado, seed `E92532A4`, mount point `../../../`, 6.749 entradas no pacote principal e 227 no override:

```powershell
$key = (Get-Content work/.architect-aes-key -Raw).Trim()
work/repak/target/release/repak.exe --aes-key $key info outputs/v12-corrections/pakchunk0-Windows-ptbr.pak
work/repak/target/release/repak.exe --aes-key $key info outputs/v12-corrections/pakchunk9999-Windows_1_P-ptbr.pak
Remove-Variable key
```

Extraia pelo menos `Item_Name.csv`, `QuestTask_Name.csv`, `TutorialWalkthrough_Name.csv`, `Dialog_Name.csv` e `ClientString_Name.csv` dos PAKs preparados. Compare os arquivos extraídos com a árvore `architectlandofexiles_BR/translations/v12-corrections/`. Confira também:

- todos os campos `Item_Name.Name` e os `ParamN` referenciados nesses nomes coincidem com o original;
- as menções à torre usam `Giant's Tower`;
- os nomes oficiais de monstros, chefes, NPCs e masmorras foram preservados;
- contadores usam “restante(s)” nos contextos de tempo/quantidade;
- placeholders e tags estão presentes e balanceados.

## Instalação e reversão

Feche o jogo antes de trocar os arquivos. Confirme que não há processo `Architect` ou `ProjectTT` em execução. Faça cópias dos dois PAKs ativos antes de sobrescrevê-los.

```powershell
$full = 'H:\Games\Architect\ProjectTT\Saved\PersistentDownloadDir\DownloadContent\pakchunk0-Windows.pak'
$patch = 'H:\Games\Architect\ProjectTT\Content\Paks\pakchunk9999-Windows_1_P.pak'
Copy-Item -LiteralPath $full -Destination work/backups/download-pakchunk0-Windows-before-next-version.pak
Copy-Item -LiteralPath $patch -Destination work/backups/pakchunk9999-Windows_1_P-before-next-version.pak
Copy-Item -LiteralPath outputs/v12-corrections/pakchunk0-Windows-ptbr.pak -Destination $full -Force
Copy-Item -LiteralPath outputs/v12-corrections/pakchunk9999-Windows_1_P-ptbr.pak -Destination $patch -Force
```

Confira os SHA-256 instalados com `Get-FileHash` e compare com os arquivos preparados. Para reverter, copie os dois arquivos de backup correspondentes de volta aos mesmos destinos. Restaure o par completo; misturar versões pode reativar textos antigos ou causar conflito entre tabelas.

## Correções aplicadas nesta versão

- Restaurados 126 valores de parâmetros interpolados nos nomes dos itens; a auditoria comparou todos os templates e parâmetros referenciados com o original.
- Restaurados 34 nomes de chefes/localidades que ainda estavam traduzidos.
- Corrigidas ocorrências de `Giant's Tower` que apareciam como “Torre do Gigante”, “Giant's Torre” ou dentro de frases malformadas, incluindo guias e objetivos de missão.
- Corrigidos 12 rótulos de tempo/quantidade restante.
- Ajustadas 37 células de falas com tratamento direto à personagem feminina.
- Mantidas as descrições naturais de posição dos acessórios já corrigidas na versão anterior: dedo, pescoço, orelha e braço.
- Confirmado zero desvio nos nomes e fragmentos de nomes dos itens, após extrair o pacote instalado.

## Observações para futuras atualizações

Uma atualização do jogo pode substituir `pakchunk0-Windows.pak`, alterar IDs/colunas ou mudar o formato e a prioridade dos PAKs. Depois de qualquer atualização, preserve novamente os arquivos originais, reextraia e compare as tabelas por ID, atualize as traduções e gere os dois pacotes. Não assuma que a chave, a versão PAK ou o seed mudaram ou permaneceram iguais: confirme-os com `repak info` e com uma extração de validação antes de instalar.

## Continuidade pelo repositório

O repositório guarda snapshots completos em `translations/v0-upload/`, `translations/v1/` até `translations/v11-quality/` e `translations/v12-corrections/`. O arquivo inicial enviado antes do projeto está preservado em `v0-upload`; ele é histórico e não é a versão atual. `changes/v11-to-v12-corrections/changes.json` registra as células alteradas para a v12. Não edite uma versão publicada: crie uma nova pasta `v13-draft`, revise-a e só então publique um novo snapshot.

O repositório contém as traduções e ferramentas, não o PAK integral nem os arquivos extraídos do jogo. Extraia os pacotes localmente e mantenha os resultados em `work/`, ignorado pelo Git.

### Fluxo para uma atualização do jogo

No checkout do repositório, use os scripts `tools/`. Eles esperam a credencial local em `work/.architect-aes-key`:

```powershell
pwsh -File tools/extract_paks.ps1 `
  -Pak 'H:\Games\Architect\ProjectTT\Saved\PersistentDownloadDir\DownloadContent\pakchunk0-Windows.pak' `
  -OutputRoot work/extracted-new
```

Repita a extração para os PAKs originais ou para a versão anterior, usando outro `-OutputRoot` (`work/extracted-old`). Se a instalação já contém a tradução, use os backups originais guardados antes da instalação. Extraia também o PAK de prioridade alta quando a atualização tiver mudado arquivos distribuídos por ele.

Compare as versões originais e prepare um rascunho. O script preserva traduções revisadas, usa o texto inglês novo onde a versão anterior ainda estava em inglês e põe textos alterados em uma fila de revisão. Nomes próprios protegidos são copiados do novo original:

```powershell
$old = 'work/extracted-old/pakchunk0-Windows/ProjectTT/Content/TT/Data/CSV/L10N/en'
$new = 'work/extracted-new/pakchunk0-Windows/ProjectTT/Content/TT/Data/CSV/L10N/en'
$previous = 'translations/v11-quality/ProjectTT/Content/TT/Data/CSV/L10N/en'
python tools/compare_localization.py --old-source $old --new-source $new --translation $previous --out work/game-update-review.json
python tools/merge_updated_tables.py --old-source $old --new-source $new --old-translation $previous --out work/draft-v12 --report work/draft-v12-review.json
```

Traduza e revise todos os IDs/células indicados nos relatórios. Rode a auditoria contra o novo inglês; revise manualmente os alertas semânticos, pois uma máquina não consegue saber sozinha se `left` é direção ou tempo restante:

```powershell
python tools/audit_translation.py --source $new --translation work/draft-v12 --out work/audit-v12.json
```

Quando a revisão estiver concluída, copie as tabelas para `translations/v12-draft/ProjectTT/Content/TT/Data/CSV/L10N/en/`, crie `changes/v11-to-v12/` com um manifesto das células revistas e atualize o changelog. Preserve todas as versões anteriores.

Extraia o PAK principal atualizado por completo e gere o novo par de pacotes. O diretório passado em `-FullPakRoot` deve ser a raiz extraída do pacote, aquela que contém `ProjectTT/`:

```powershell
pwsh -File tools/build_translation_paks.ps1 `
  -FullPakRoot work/extracted-new/pakchunk0-Windows `
  -TranslationRoot translations/v12-draft `
  -WorkRoot work/build-v12 `
  -OutputRoot outputs/v12
```

Confira `repak info`, extraia tabelas dos PAKs recém-gerados, rode `tools/audit_translation.py` no snapshot e confira os hashes. Só depois instale:

```powershell
pwsh -File tools/install_translation.ps1 `
  -MainPak outputs/v12/pakchunk0-Windows-ptbr.pak `
  -OverridePak outputs/v12/pakchunk9999-Windows_1_P-ptbr.pak
```

O instalador exige que o jogo esteja fechado, cria backups com data e compara SHA-256 depois da cópia. Não altere `translations/v11-quality/` retroativamente.

### Publicação da credencial para mantenedores

A chave AES é necessária para extração e empacotamento. Neste checkout ela fica em `work/.architect-aes-key` e é ignorada pelo Git. O valor bruto não deve entrar em commit público. Se for necessário permitir execução pelo GitHub Actions, um mantenedor autorizado pode cadastrar a chave nas configurações privadas do repositório como Actions secret `ARCHITECT_AES_KEY`; compartilhe a credencial diretamente apenas com pessoas autorizadas. Um fork público consegue compilar os CSVs se já tiver uma ferramenta PAK configurada, mas não deve receber a chave em texto aberto.

## Incidentes e causa raiz já encontrados

- Em testes históricos, foi observada uma tradução parcial quando o conteúdo do PAK principal e o do override não estavam na mesma versão. Isso justifica manter versões e hashes sincronizados, mas não prova que o jogador precise instalar dois PAKs. O teste mais recente com um override sozinho também foi parcial; as hipóteses restantes estão em `docs/INVESTIGACAO-CARREGAMENTO-PAK.md`.
- Uma checagem anterior olhava apenas para a coluna `Item_Name.Name`. Títulos montados dinamicamente também incorporam `ParamN`; 126 desses fragmentos ainda estavam traduzidos. A correção restaura os fragmentos referenciados pelo template original.
- Uma checagem da torre não reconhecia o apóstrofo curvo `’` nem marcação que dividia as palavras por tags. A correção foi comparada com cada célula-fonte e conferida após extrair o PAK instalado.
- O primeiro PAK de correção usou uma chave AES errada e foi rejeitado pelo Unreal como índice corrompido. Não reutilize o PAK rejeitado que está em `work/backups/pakchunk9999-Windows_1_P-rejected-v10.pak`; os PAKs v12 de manutenção foram lidos e extraídos com a chave confirmada.


## Registro detalhado da v12-corrections

- Snapshot novo: `translations/v12-corrections/ProjectTT/Content/TT/Data/CSV/L10N/en/`, preservando os 227 CSVs; `v0-upload` até `v11-quality` permanecem intactos. O diff célula a célula fica em `changes/v11-to-v12-corrections/changes.json`.
- Foram corrigidos placeholders ausentes/duplicados em descrições, tags de cor quebradas em diálogos e tutoriais, nomes de interface que estavam vazios, nomes de categorias/ações e uma série de parâmetros dinâmicos. `Skill` e `Codex` permanecem em inglês. Nomes próprios de itens continuam originais; a descrição do acessório expande os parâmetros em português, mas o título e os parâmetros que formam título foram conferidos separadamente.
- Auditoria contra as tabelas originais: 227 tabelas encontradas; 0 IDs ausentes/novos; 0 traduções vazias em campos não vazios; 0 divergências de placeholders/tags verificadas; 0 alterações em nomes/templates/parâmetros de títulos de itens; 0 menções encontradas com `Giant's Tower` traduzido. O relatório contém dez alertas de busca por `left`; o alerta não classifica sozinho o significado. Foram conferidos exemplos direcionais e contadores; chaves de tempo/quantidade restantes usam “restante(s)”, como `AUCTION_MENU_LEFTTIME`, `CLAN_EXCHANGE_LEFT_TIME`, `CLAN_RESEARCH_TOGGLE_ACTIVATE_LEFT_TIME`, `COMMON_LEFT` e `COMMON_LEFT_TIME`.
- Os 227 CSVs do PAK override recém-construído foram extraídos novamente para `work/validate-v12b/` e os hashes dos bytes de todos coincidiram com o snapshot v12. `repak info` confirmou 6.749 entradas no pacote principal e 227 no override; ambos V11, índice criptografado, mount `../../../`, seed `E92532A4`; compressão Zlib no principal e None no override.
- Arquivos de manutenção preparados: `outputs/v12-corrections/pakchunk0-Windows-ptbr.pak` e `outputs/v12-corrections/pakchunk9999-Windows_1_P-ptbr.pak`. Não são downloads para jogadores; hashes e tamanhos estão no manifesto.
- **Estado de instalação:** instalação local limpa depois do teste do override único. Backups dos arquivos instalados temporariamente e do PAK original estão em `work/backups/clean-test-20260927/` e `work/backups/download-pakchunk0-Windows-original-before-v5.pak`. Confirme o hash do PAK ativo antes de qualquer nova operação.

## Credencial AES: continuidade segura

A chave validada foi o candidato de índice 650 em `work/content-key-candidates.json`, validado com leitura de PAKs conhecidos usando `repak_cli 0.2.3`. O arquivo secreto correspondente neste computador está em `work/.architect-aes-key`; o arquivo tem 64 dígitos hexadecimais, representa uma chave AES-256, é ignorado por `.gitignore` e nunca deve ser gravado neste documento, em issue pública, commit ou log. O arquivo da lista de candidatos, os PAKs, dumps e saídas de diagnóstico também são locais/privados. O número 650 é índice de busca, não é a chave.

Para uma pessoa mantenedora continuar em outro computador, ela deve obter a chave por canal privado autorizado e provisionar localmente `work/.architect-aes-key`. Alternativamente, uma automação privada pode receber a variável protegida `ARCHITECT_AES_KEY` nas configurações de Actions do repositório; o valor não deve aparecer em YAML, logs, artefatos ou forks. O clone público sozinho não contém a chave e não consegue abrir PAKs criptografados. Não existe senha de conta/API necessária para esse procedimento: a credencial técnica é a chave AES do jogo.

## Falhas conhecidas que orientam o processo

1. **Crash `Corrupt pak index detected`:** ocorreu quando se empacotou com chave AES que não correspondia ao jogo. Só instalar depois de `repak info` conseguir reabrir o PAK recém-gerado com a mesma chave e formato esperado.
2. **Tradução antiga ainda aparecia em tela:** só um dos dois PAKs havia sido atualizado. Sempre preparar e instalar o par junto, preservando a prioridade do override.
3. **Títulos de itens traduzidos:** nomes de exibição são compostos por `Item_Name.Name` e podem incluir `ParamN`. Comparar o campo e cada parâmetro referenciado com a fonte original. Esta regra também protege a busca do Marketplace.
4. **Chaves internas sobrescritas:** uma versão anterior alterou valores da coluna `Key` em `ClientString_Name.csv` ao tratar cabeçalhos como linhas. Scripts devem alterar apenas campos de conteúdo, nunca IDs, chaves, cabeçalhos ou ordem das colunas. A v12 tem 0 IDs ausentes/novos.
5. **Marcadores temporários de tradução:** o lote antigo deixou marcadores `QZXKEEP00000XZQ` em textos. Rode a busca por `QZXKEEP\d{5}XZQ` e falhe a auditoria se encontrar qualquer ocorrência. Scripts de reparo devem fazer correspondência pelo texto-fonte/ID; não substituir tokens cegamente.
6. **Tags e variáveis:** traduções podem manter texto legível e ainda quebrar uma tag ou remover/duplicar um placeholder. Audite contagens/estrutura, faça leitura contextual dos relatórios e extraia os PAKs gerados para comparação.

## Publicar nova versão no GitHub

O repositório público é `https://github.com/jackchakkal/architectlandofexiles_BR`, branch `main`. Para publicar: atualize a nova pasta `translations/vN-...`, mantenha as pastas anteriores, gere `changes/vAnterior-to-vN/changes.json`, inclua o manifesto e changelog, verifique que `work/.architect-aes-key`, `.pak`, `.uasset`, `.uexp`, `.ubulk`, arquivos extraídos e outros segredos estão ignorados, e só então faça commit/push. A autenticação Git deve ocorrer pelo Git Credential Manager com a conta autorizada; nunca embuta token no remote ou em comandos/documentos.
