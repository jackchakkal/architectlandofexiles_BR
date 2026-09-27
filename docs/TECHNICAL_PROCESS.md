# Tradução PT-BR do Architect — procedimento reproduzível

Este documento descreve, para mantenedores, como extrair e comparar as tabelas do jogo, editar a tradução, auditar, gerar o PAK e publicar uma versão. O procedimento foi preparado para Windows/PowerShell. Para o mecanismo de carregamento e os testes que levaram à solução atual, veja [COMO-A-TRADUCAO-E-CARREGADA.md](COMO-A-TRADUCAO-E-CARREGADA.md); para o que o jogador recebe, [TRANSPARENCIA.md](TRANSPARENCIA.md).

## Estado técnico

- Snapshot publicado: `v12-corrections` (227 CSVs). Em preparação: `v13` (293 rótulos de interface encurtados + `SupportLanguage_Name.csv` corrigida), gerado por `tools/apply_overrides.py` a partir de `changes/v12-to-v13/overrides.json`.
- **Distribuição: um único PAK de override**, `pakchunk9999-Windows_21474835_P.pak`, instalado em `ProjectTT/Content/Paks/`. Contém só os 227 CSVs. O método antigo do "par" (substituir o `pakchunk0` do `DownloadContent`) está obsoleto; os scripts ficaram em `tools/legacy/` apenas como histórico.
- Ferramenta de PAK: `repak_cli 0.2.3` (`../work/repak/target/release/repak.exe`). Formato: Unreal PAK V11, índice criptografado, mount point `../../../`, path hash seed `E92532A4` (decimal 3911529124), entradas sem compressão.
- Build e empacotamento para jogadores: `tools/build_release.ps1`. Instalação (mantenedor ou jogador): `tools/player-installer/install.ps1`.
- Auditoria reproduzível: `tools/audit_translation.py`; relatório da v12 em `docs/AUDIT-v12.json`; resumo por versão em `releases/<versão>/manifest.json`.
- Backups de testes e originais ficam em `../work/backups/` (fora do repositório).

## Aplicativos e dependências

- Windows e PowerShell (os exemplos usam caminhos e comandos PowerShell).
- Python 3.11 ou compatível; os scripts usam a biblioteca padrão, sem pacote Python adicional.
- `repak_cli 0.2.3` para manipular os PAKs.
- `tools/locres_export.py` exporta recursos binários LocRes UE v0–v3 para CSV/JSON na investigação de strings fora das tabelas CSV customizadas.
- Rust/Cargo somente se precisar compilar o repak a partir do código-fonte. Na pasta `../work/repak`, execute `cargo build --release -p repak_cli`; o executável será `../work/repak/target/release/repak.exe`.
- Não é necessário abrir o Unreal Editor para editar essas tabelas CSV.
- O jogo foi compilado com Unreal Engine 5.5 (indicado pelo relatório de crash fornecido); seus arquivos PAK usam versão V11. Confirme a versão do PAK com `repak info` depois de atualizações do jogo.

## Arquivos e função de cada um

| Arquivo ou pasta | Função |
| --- | --- |
| `work/.architect-aes-key` | Credencial local AES-256 (64 hex). Necessária para ler os PAKs do jogo e gerar o override no formato validado. Nunca publicar. |
| `../work/repak/target/release/repak.exe` | Extrai, lista, inspeciona e empacota `.pak`. |
| `../work/download-pak0-original/ProjectTT/Content/TT/Data/CSV/L10N/en/` | Referência dos 227 CSVs originais em inglês da versão em que a tradução foi feita. Base de comparação por ID. |
| `translations/<versão>/ProjectTT/Content/TT/Data/CSV/L10N/en/` | Snapshot PT-BR. Cada versão é imutável; correções vão para uma pasta nova. |
| `changes/<de>-to-<para>/overrides.json` | Alterações por ID aplicadas sobre o snapshot anterior (`tools/apply_overrides.py`). `changes.json` é o diff resultante. |
| `tools/player-installer/` | Instalador para jogadores; entra no ZIP da Release. |
| `../outputs/<versão>/` | PAK, `release.json` e ZIP gerados pelo build (não versionados). |
| `ProjectTT/Content/Paks/pakchunk9999-Windows_21474835_P.pak` (no jogo) | Destino do override. Único arquivo que a tradução acrescenta ao jogo. |

Os CSVs permanecem no diretório `L10N/en` porque o jogo não tem entrada para português em `SupportLanguage.csv`; a tradução ocupa a posição do inglês e `SupportLanguage_Name.csv` mostra "Português (Brasil)" no seletor.

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

O PAK integral deve estar disponível localmente. O backup limpo conhecido está em `../work/backups/download-pakchunk0-Windows-original-before-v5.pak`. Preserve uma cópia intocada do pacote original antes de qualquer nova extração ou instalação.

Confira o índice e o formato:

```powershell
$key = (Get-Content work/.architect-aes-key -Raw).Trim()
..\work\repak\target\release\repak.exe --aes-key $key info ..\work\backups\download-pakchunk0-Windows-original-before-v5.pak
```

### 2. Extrair um PAK inteiro

```powershell
$key = (Get-Content work/.architect-aes-key -Raw).Trim()
..\work\repak\target\release\repak.exe --aes-key $key unpack `
  -o ..\work\extracted-original `
  ..\work\backups\download-pakchunk0-Windows-original-before-v5.pak
Remove-Variable key
```

O prefixo `../../../` é removido por padrão. As tabelas ficam então em `../work/extracted-original/ProjectTT/Content/TT/Data/CSV/L10N/en/`.

Para extrair somente tabelas selecionadas, use `-i` repetidamente:

```powershell
$key = (Get-Content work/.architect-aes-key -Raw).Trim()
..\work\repak\target\release\repak.exe --aes-key $key unpack `
  -o ..\work\extracted-selected `
  -i ProjectTT/Content/TT/Data/CSV/L10N/en/Item_Name.csv `
  -i ProjectTT/Content/TT/Data/CSV/L10N/en/QuestTask_Name.csv `
  ..\work\backups\download-pakchunk0-Windows-original-before-v5.pak
Remove-Variable key
```

Use `repak list` para consultar caminhos de arquivos do pacote. `repak info` mostra versão, compressão, seed e quantidade de entradas.

### 3. Manter a referência original

Não edite a árvore original. Guarde a cópia limpa das tabelas em `../work/download-pak0-original/ProjectTT/Content/TT/Data/CSV/L10N/en/`. Compare por ID, nunca apenas pela posição da linha. Antes de cada instalação, faça cópia de segurança dos dois PAKs ativos.

## Edição e preparação da tradução

### 1. Editar as tabelas

Edite os arquivos em `translations/v12-corrections/ProjectTT/Content/TT/Data/CSV/L10N/en/` no repositório (snapshot público e fonte local atual). Cada tabela contém IDs e tipos de texto diferentes; não renomeie tabelas ou colunas.

As correções históricas da v11 foram preparadas por um script local que dependia de arquivos de pesquisa não publicados; esse script não faz parte do repositório e não é necessário para continuar. Para reproduzir o estado atual, use o snapshot v12 versionado e confira o diff de 91 células em `changes/v11-to-v12-corrections/changes.json`. Para versões futuras, o fluxo reproduzível está nos scripts `tools/compare_localization.py`, `tools/merge_updated_tables.py`, `tools/audit_translation.py`, `tools/apply_overrides.py` e `tools/build_release.ps1`.

### 2. Gerar um snapshot novo a partir de overrides

Não edite `translations/vN/` publicado. Registre as mudanças em `changes/vN-to-vM/overrides.json` (`{"Tabela.csv": {"ID": "novo texto"}}`) e gere o snapshot:

```powershell
python tools/apply_overrides.py --base translations/v12-corrections --overrides changes/v12-to-v13/overrides.json `
  --source ..\work\download-pak0-original --out translations/v13 --report changes/v12-to-v13/changes.json
```

O script só altera a coluna de valor, preserva BOM/CRLF/IDs e falha se placeholders ou tags do novo texto não coincidirem com o inglês. Para tabelas com várias colunas de texto, edite o CSV do snapshot novo diretamente e registre no changelog.

## Empacotamento e pacote para jogadores

```powershell
pwsh -File tools/build_release.ps1 -Version v13 -TranslationRoot translations/v13
```

Sem repak.exe (ou em Linux/macOS), o PAK pode ser gerado por `tools/build_pak.py --input <pasta com ProjectTT/...> --output <pak> --key-file <chave>`; ele reproduz o formato do repak (V11, índice criptografado, sem compressão) e foi validado contra a saída do repak entrada por entrada. Nesse caso monte `release.json` e o ZIP manualmente (ver `releases/v13/manifest.json` para os campos).

Gera em `../outputs/v13/`: o PAK (`pakchunk9999-Windows_21474835_P.pak`, V11, mount `../../../`, seed `E92532A4`, índice criptografado, sem compressão), `release.json` (versão + SHA-256, lido pelo instalador) e `Architect-PTBR-v13.zip` com o instalador. O script imprime os hashes do PAK e do ZIP para a Release.

O nome do PAK importa: `pakchunk9999` (número inexistente no jogo) e `_21474835_P` (prioridade acima do conteúdo baixado). Não renomeie.

## Fila de rótulos longos (estouro de tela)

`tools/find_overflow_candidates.py` compara o comprimento de cada célula com o inglês e lista rótulos curtos que cresceram demais:

```powershell
python tools/find_overflow_candidates.py --source ..\work\download-pak0-original --translation translations/v13 --out ..\work\overflow-candidates.json
```

Revise a lista, escreva as versões curtas em `changes/<de>-to-<para>/overrides.json` e gere o snapshot com `apply_overrides.py`. Regras de estilo em `GLOSSARIO-E-REGRAS.md`.

## Completude por cruzamento com outra cultura

O jogo traz as mesmas tabelas em `zh-CN`, `zh-TW`, `id`, `th`, `jp`. Uma célula em que o PT-BR continua igual ao inglês, mas o chinês difere do inglês, é provavelmente uma lacuna (ou um nome mantido de propósito). `tools/check_completeness.py` lista essas células por tabela/coluna:

```powershell
python tools/check_completeness.py --game-l10n ..\work\download-pak0-full-v11\ProjectTT\Content\TT\Data\CSV\L10N `
  --en-dir ..\work\download-pak0-original\ProjectTT\Content\TT\Data\CSV\L10N\en --translation translations/v13 --out ..\work\completeness.json
```

Passe `--en-dir` com o inglês ORIGINAL (a árvore extraída pode já conter a tradução no lugar de `en`). Colunas de nomes próprios (`Item_Name.Name`, `Npc_Name.Name`, masmorras, áreas) são ignoradas. Traduza as lacunas reais com a seção `__by_text__` do `overrides.json` (um texto em inglês → um texto PT-BR, aplicado em todas as células idênticas daquela coluna).

## Nomes que devem ficar em inglês

`tools/scan_name_mentions.py` compara cada célula com o inglês original e lista (a) células cujo valor inteiro é um nome de Skill/item/masmorra mas foi traduzido e (b) frases em que o nome apareceu no inglês e não aparece no PT-BR:

```powershell
python tools/scan_name_mentions.py --source ..\work\download-pak0-original --translation translations/v14 --out ..\work\name-mentions.json
```

O caso (a) é corrigido automaticamente pelas regras `__restore_exact_names__`/`__replace_translated_names__` do `overrides.json`; o caso (b) vira reescritas em `__by_text__` (chave = frase em inglês) ou por ID+coluna.

## Validação antes de publicar

1. `repak --aes-key <chave> info` no PAK gerado: V11, índice criptografado, seed `E92532A4`, mount `../../../`, 227 entradas.
2. Extraia o PAK (`repak unpack`) e compare os 227 CSVs byte a byte com o snapshot.
3. `python tools/audit_translation.py --source <en original> --translation <snapshot> --out ../work/audit-vN.json`: zero IDs ausentes/novos, zero divergências de placeholders/tags, zero nomes de itens alterados, zero `Giant's Tower` traduzido, nenhum marcador `QZXKEEP\d{5}XZQ`.
4. Instale no PC do mantenedor com o ZIP gerado (não com cópia manual) e verifique no jogo: tela inicial, menu de personagem, missões, inventário, tutorial e uma tela de modo IA.

## Instalação e reversão

Use o mesmo instalador dos jogadores, extraído do ZIP gerado pelo build:

```powershell
pwsh -File ..\outputs\v13\Architect-PTBR-v13\install.ps1 -GameRoot 'H:\Games\Architect'
pwsh -File ..\outputs\v13\Architect-PTBR-v13\install.ps1 -Uninstall
```

Ele exige o jogo fechado, confere o SHA-256 do `release.json`, remove overrides antigos (`pakchunk9999-Windows*_P.pak`) e grava `traducao-ptbr.json` ao lado do PAK. Nenhum arquivo original é tocado, portanto não há backup a restaurar.

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

O repositório guarda snapshots completos em `translations/v0-upload/`, `translations/v1/` até `translations/v11-quality/` e `translations/v12-corrections/`. O arquivo inicial enviado antes do projeto está preservado em `v0-upload`; ele é histórico e não é a versão atual. `changes/v11-to-v12-corrections/changes.json` registra as células alteradas para a v12. Não edite uma versão publicada: crie uma nova pasta `v13`, revise-a e só então publique um novo snapshot.

O repositório contém as traduções e ferramentas, não o PAK integral nem os arquivos extraídos do jogo. Extraia os pacotes localmente e mantenha os resultados em `work/`, ignorado pelo Git.

### Fluxo para uma atualização do jogo

No checkout do repositório, use os scripts `tools/`. Eles esperam a credencial local em `work/.architect-aes-key`:

```powershell
pwsh -File tools/extract_paks.ps1 `
  -Pak 'H:\Games\Architect\ProjectTT\Saved\PersistentDownloadDir\DownloadContent\pakchunk0-Windows.pak' `
  -OutputRoot ..\work\extracted-new
```

Repita a extração para os PAKs originais ou para a versão anterior, usando outro `-OutputRoot` (`work/extracted-old`). Se a instalação já contém a tradução, use os backups originais guardados antes da instalação. Extraia também o PAK de prioridade alta quando a atualização tiver mudado arquivos distribuídos por ele.

Compare as versões originais e prepare um rascunho. O script preserva traduções revisadas, usa o texto inglês novo onde a versão anterior ainda estava em inglês e põe textos alterados em uma fila de revisão. Nomes próprios protegidos são copiados do novo original:

```powershell
$old = '..\work\extracted-old\pakchunk0-Windows\ProjectTT\Content\TT\Data\CSV\L10N\en'
$new = '..\work\extracted-new\pakchunk0-Windows\ProjectTT\Content\TT\Data\CSV\L10N\en'
$previous = 'translations/v11-quality/ProjectTT/Content/TT/Data/CSV/L10N/en'
python tools/compare_localization.py --old-source $old --new-source $new --translation $previous --out ..\work\game-update-review.json
python tools/merge_updated_tables.py --old-source $old --new-source $new --old-translation $previous --out ..\work\draft-v13 --report ..\work\draft-v13-review.json
```

Traduza e revise todos os IDs/células indicados nos relatórios. Rode a auditoria contra o novo inglês; revise manualmente os alertas semânticos, pois uma máquina não consegue saber sozinha se `left` é direção ou tempo restante:

```powershell
python tools/audit_translation.py --source $new --translation ..\work\draft-v13 --out ..\work\audit-v13.json
```

Quando a revisão estiver concluída, copie as tabelas para `translations/v13/ProjectTT/Content/TT/Data/CSV/L10N/en/`, crie `changes/v12-to-v13/` com um manifesto das células revistas e atualize o changelog. Preserve todas as versões anteriores.

Gere o PAK e o ZIP com `tools/build_release.ps1 -Version vN -TranslationRoot translations/vN-draft`, valide conforme a seção "Validação antes de publicar" e instale com o ZIP gerado. Não altere snapshots publicados retroativamente.

### Publicação da credencial para mantenedores

A chave AES é necessária para extração e empacotamento. Neste checkout ela fica em `work/.architect-aes-key` e é ignorada pelo Git. O valor bruto não deve entrar em commit público. Se for necessário permitir execução pelo GitHub Actions, um mantenedor autorizado pode cadastrar a chave nas configurações privadas do repositório como Actions secret `ARCHITECT_AES_KEY`; compartilhe a credencial diretamente apenas com pessoas autorizadas. Um fork público consegue compilar os CSVs se já tiver uma ferramenta PAK configurada, mas não deve receber a chave em texto aberto.

## Incidentes e causa raiz já encontrados

- O override com sufixo `_1_P` só traduzia a tela inicial porque o conteúdo baixado (`DownloadContent`) é montado com prioridade maior. A solução foi o sufixo `_21474835_P`; ver `docs/COMO-A-TRADUCAO-E-CARREGADA.md`. O "par" de PAKs foi uma solução intermediária e está abandonado.
- Uma checagem anterior olhava apenas para a coluna `Item_Name.Name`. Títulos montados dinamicamente também incorporam `ParamN`; 126 desses fragmentos ainda estavam traduzidos. A correção restaura os fragmentos referenciados pelo template original.
- Uma checagem da torre não reconhecia o apóstrofo curvo `’` nem marcação que dividia as palavras por tags. A correção foi comparada com cada célula-fonte e conferida após extrair o PAK instalado.
- O primeiro PAK de correção usou uma chave AES errada e foi rejeitado pelo Unreal como índice corrompido. Não reutilize o PAK rejeitado que está em `../work/backups/pakchunk9999-Windows_1_P-rejected-v10.pak`; os PAKs v12 de manutenção foram lidos e extraídos com a chave confirmada.


## Registro detalhado da v12-corrections

- Snapshot novo: `translations/v12-corrections/ProjectTT/Content/TT/Data/CSV/L10N/en/`, preservando os 227 CSVs; `v0-upload` até `v11-quality` permanecem intactos. O diff célula a célula fica em `changes/v11-to-v12-corrections/changes.json`.
- Foram corrigidos placeholders ausentes/duplicados em descrições, tags de cor quebradas em diálogos e tutoriais, nomes de interface que estavam vazios, nomes de categorias/ações e uma série de parâmetros dinâmicos. `Skill` e `Codex` permanecem em inglês. Nomes próprios de itens continuam originais; a descrição do acessório expande os parâmetros em português, mas o título e os parâmetros que formam título foram conferidos separadamente.
- Auditoria contra as tabelas originais: 227 tabelas encontradas; 0 IDs ausentes/novos; 0 traduções vazias em campos não vazios; 0 divergências de placeholders/tags verificadas; 0 alterações em nomes/templates/parâmetros de títulos de itens; 0 menções encontradas com `Giant's Tower` traduzido. O relatório contém dez alertas de busca por `left`; o alerta não classifica sozinho o significado. Foram conferidos exemplos direcionais e contadores; chaves de tempo/quantidade restantes usam “restante(s)”, como `AUCTION_MENU_LEFTTIME`, `CLAN_EXCHANGE_LEFT_TIME`, `CLAN_RESEARCH_TOGGLE_ACTIVATE_LEFT_TIME`, `COMMON_LEFT` e `COMMON_LEFT_TIME`.
- Nota (2026-09-27): os PAKs "principal" e o override `_1_P` citados nas auditorias históricas foram substituídos pelo override único `_21474835_P`; os CSVs são os mesmos.

## Credencial AES: continuidade segura

A chave validada foi o candidato de índice 650 em `../work/content-key-candidates.json`, validado com leitura de PAKs conhecidos usando `repak_cli 0.2.3`. O arquivo secreto correspondente neste computador está em `work/.architect-aes-key`; o arquivo tem 64 dígitos hexadecimais, representa uma chave AES-256, é ignorado por `.gitignore` e nunca deve ser gravado neste documento, em issue pública, commit ou log. O arquivo da lista de candidatos, os PAKs, dumps e saídas de diagnóstico também são locais/privados. O número 650 é índice de busca, não é a chave.

Para uma pessoa mantenedora continuar em outro computador, ela deve obter a chave por canal privado autorizado e provisionar localmente `work/.architect-aes-key`. Alternativamente, uma automação privada pode receber a variável protegida `ARCHITECT_AES_KEY` nas configurações de Actions do repositório; o valor não deve aparecer em YAML, logs, artefatos ou forks. O clone público sozinho não contém a chave e não consegue abrir PAKs criptografados. Não existe senha de conta/API necessária para esse procedimento: a credencial técnica é a chave AES do jogo.

## Falhas conhecidas que orientam o processo

1. **Crash `Corrupt pak index detected`:** ocorreu quando se empacotou com chave AES que não correspondia ao jogo. Só instalar depois de `repak info` conseguir reabrir o PAK recém-gerado com a mesma chave e formato esperado.
2. **Tradução antiga ainda aparecia em tela:** havia um override antigo com outro nome em `Content/Paks`. O instalador remove todos os `pakchunk9999-Windows*_P.pak` antes de copiar o novo.
3. **Títulos de itens traduzidos:** nomes de exibição são compostos por `Item_Name.Name` e podem incluir `ParamN`. Comparar o campo e cada parâmetro referenciado com a fonte original. Esta regra também protege a busca do Marketplace.
4. **Chaves internas sobrescritas:** uma versão anterior alterou valores da coluna `Key` em `ClientString_Name.csv` ao tratar cabeçalhos como linhas. Scripts devem alterar apenas campos de conteúdo, nunca IDs, chaves, cabeçalhos ou ordem das colunas. A v12 tem 0 IDs ausentes/novos.
5. **Marcadores temporários de tradução:** o lote antigo deixou marcadores `QZXKEEP00000XZQ` em textos. Rode a busca por `QZXKEEP\d{5}XZQ` e falhe a auditoria se encontrar qualquer ocorrência. Scripts de reparo devem fazer correspondência pelo texto-fonte/ID; não substituir tokens cegamente.
6. **Tags e variáveis:** traduções podem manter texto legível e ainda quebrar uma tag ou remover/duplicar um placeholder. Audite contagens/estrutura, faça leitura contextual dos relatórios e extraia os PAKs gerados para comparação.

## Publicar nova versão no GitHub

O repositório público é `https://github.com/jackchakkal/architectlandofexiles_BR`, branch `main`. Para publicar: atualize a nova pasta `translations/vN-...`, mantenha as pastas anteriores, gere `changes/vAnterior-to-vN/changes.json`, inclua o manifesto e changelog, verifique que `work/.architect-aes-key`, `.pak`, `.uasset`, `.uexp`, `.ubulk`, arquivos extraídos e outros segredos estão ignorados, e só então faça commit/push. A autenticação Git deve ocorrer pelo Git Credential Manager com a conta autorizada; nunca embuta token no remote ou em comandos/documentos.
