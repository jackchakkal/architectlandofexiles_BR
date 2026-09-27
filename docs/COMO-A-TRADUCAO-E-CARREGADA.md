# Como a tradução é carregada pelo jogo

Registro técnico do mecanismo, do que foi testado e do porquê da solução atual. Substitui a investigação anterior (`INVESTIGACAO-CARREGAMENTO-PAK.md`), cujas conclusões intermediárias ficaram obsoletas.

## Onde ficam os textos

O jogo (Unreal Engine 5.5) lê os textos de tabelas CSV, uma por tipo de conteúdo, no caminho virtual `ProjectTT/Content/TT/Data/CSV/L10N/<cultura>/<Tabela>_Name.csv` (função `FTtInfoLoader`, formato `Data/CSV/L10N/%s/%s` no executável). As culturas presentes no PAK original são `dev` (229 arquivos, texto-fonte), `en` (227), `zh-TW`, `zh-CN`, `id`, `th`, `jp` e `ko` (apenas 9 — o jogo tolera arquivos ausentes por cultura). `SupportLanguage.csv` (fora de `L10N`) define os idiomas selecionáveis; não há entrada para português, por isso a tradução ocupa a posição de `en`.

Os CSVs estão em dois lugares no PC do jogador:

| Local | Conteúdo | Quem coloca |
| --- | --- | --- |
| `ProjectTT/Content/Paks/pakchunk0-Windows.pak` (~56 MB) | Build base, com as tabelas da versão instalada pelo launcher | Launcher |
| `ProjectTT/Saved/PersistentDownloadDir/DownloadContent/pakchunk0-Windows.pak` (~60 MB) | Tabelas atualizadas, baixadas pelo próprio jogo | O jogo, via plugin **MobilePatchingUtils** (BuildPatchServices). O `default_<n>.manifest` ao lado lista os arquivos com hashes SHA-1. |

Os dois têm o índice criptografado com a chave AES do jogo e compressão Oodle.

## Prioridade de PAKs no Unreal

Quando vários PAKs contêm o mesmo caminho, o Unreal usa o de maior *PakOrder*:

- PAKs em `Content/Paks` recebem ordem base 4;
- o sufixo `_<N>_P` no nome soma `100 × (N + 1)`;
- PAKs montados por código (caso do `DownloadContent`, montado por Blueprint do MobilePatchingUtils) recebem a ordem que o código passar — desconhecida, mas comprovadamente maior que 204.

## O que foi testado

| Configuração | Resultado |
| --- | --- |
| Override `pakchunk9999-Windows_1_P.pak` em `Content/Paks` (ordem ≈ 204) | Só a tela inicial traduzida: o `DownloadContent` vence depois de montado. |
| Par: `pakchunk0` do `DownloadContent` reconstruído com as tabelas PT-BR + override `_1_P` | Tudo traduzido, mas exige distribuir um PAK de 77 MB com conteúdo original do jogo e é desfeito em cada atualização. **Descartado.** |
| Override renomeado `pakchunk9999-Windows_21474835_P.pak` em `Content/Paks` (ordem ≈ 2,1 bilhões), `DownloadContent` original | **Tudo traduzido** (tela inicial, menus, missões, modo IA). Solução adotada em 2026-09-27. |

O último teste foi feito com o `pakchunk0` do `DownloadContent` comprovadamente original: SHA-1 presente no manifesto da publisher, compressão Oodle (o repak gera Zlib) e os 227 CSVs `en` com tamanho idêntico aos originais em inglês.

O número 21474835 foi escolhido para que `100 × (N + 1)` fique abaixo de 2.147.483.647 (maior `int32`), evitando qualquer overflow no cálculo da ordem, e ainda assim acima de qualquer valor plausível passado pelo Blueprint.

## Consequências

- **Distribuição:** um único arquivo de 12 MB com apenas os 227 CSVs. Nenhum conteúdo original do jogo é redistribuído.
- **Atualizações do jogo:** o `DownloadContent` é atualizado pelo jogo sem tocar em `Content/Paks`; a tradução continua ativa. Tabelas novas/alteradas aparecem em inglês até a próxima versão da tradução. Se uma tabela mudar de estrutura (colunas/IDs), a versão em português dela continuará sendo usada por ter prioridade — por isso é preciso reextrair e comparar após cada atualização (ver `TECHNICAL_PROCESS.md`).
- **Formato do PAK:** V11, mount point `../../../`, path hash seed `E92532A4`, índice criptografado com a chave do jogo, entradas sem compressão. O índice criptografado não é obrigatório para o Unreal montar o PAK, mas foi mantido por ser o formato já validado.

## O que ainda não sabemos

- Se o launcher, numa atualização grande, apaga arquivos desconhecidos em `Content/Paks`. Até agora não apagou. Se acontecer, a solução é executar o instalador de novo.
- O valor exato de PakOrder passado pelo Blueprint do `DownloadContent`. Não é necessário conhecê-lo.
