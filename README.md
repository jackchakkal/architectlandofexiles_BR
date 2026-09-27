# Architect: Land of Exiles — PT-BR

Projeto comunitário de localização em português brasileiro, com snapshots imutáveis, auditoria de tabelas e fluxo reproduzível para gerar pacotes Unreal PAK.

## Versão atual

- Snapshot: [`translations/v12-corrections/`](translations/v12-corrections/). Contém 227 tabelas CSV.
- Alterações desde v11: [`changes/v11-to-v12-corrections/changes.json`](changes/v11-to-v12-corrections/changes.json).
- Auditoria: [`docs/AUDIT-v12.json`](docs/AUDIT-v12.json).
- Manifesto dos pacotes preparados: [`releases/v12-corrections/manifest.json`](releases/v12-corrections/manifest.json). Os PAKs em si ficam localmente e não são distribuídos neste repositório.
- Passo a passo técnico completo: [`docs/TECHNICAL_PROCESS.md`](docs/TECHNICAL_PROCESS.md).

## Regras editoriais

Nomes de itens, monstros, NPCs, chefes e masmorras permanecem iguais ao jogo. `Giant's Tower`, `Skill` e `Codex` não são traduzidos. Em contadores, `left` é “restante(s)”; traduções direcionais usam “à esquerda”. Textos respeitam placeholders e tags do Unreal, português brasileiro, gênero e concordância.

## Segurança e arquivos

Os CSVs são versionados; PAKs, extrações e credenciais AES ficam no computador de cada mantenedor. A chave AES de 256 bits é necessária para ler e criar PAKs com índice criptografado. Ela deve ser obtida por canal privado autorizado e guardada em `work/.architect-aes-key`, ignorada pelo Git. O repositório público não contém nem deve receber a chave.

Leia o guia técnico antes de atualizar o jogo ou gerar pacotes. Cada versão publicada ganha uma pasta própria; não edite snapshots históricos.
