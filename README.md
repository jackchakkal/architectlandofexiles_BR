# Architect: Land of Exiles — Português brasileiro

**Quer jogar em português?** Consulte [Instalação para jogadores](docs/INSTALACAO-PARA-JOGADORES.md). A versão v12 completa foi reaplicada no computador do mantenedor usando o par de PAKs e teve os dois hashes conferidos.

## Para jogadores

O ZIP de um arquivo que foi testado continha somente o PAK de override; ele não era a instalação v12 completa. O par correto consiste no PAK principal modificado e no override de alta prioridade, instalados em duas pastas específicas. A instalação pública ainda não está pronta: o PAK principal inclui conteúdo original do jogo e não deve ser publicado. Veja [o processo técnico](docs/TECHNICAL_PROCESS.md) e [o registro do teste de um arquivo](docs/INVESTIGACAO-CARREGAMENTO-PAK.md).

## Para colaboradores e mantenedores

- Snapshot atual: [`translations/v12-corrections/`](translations/v12-corrections/), com 227 tabelas, 128.598 registros e 486.563 células (368.441 não vazias).
- Auditoria: [`docs/AUDIT-v12.json`](docs/AUDIT-v12.json).
- Processo técnico de extração, comparação, empacotamento e manutenção: [`docs/TECHNICAL_PROCESS.md`](docs/TECHNICAL_PROCESS.md).
- Regras de localização: [`docs/GLOSSARIO-E-REGRAS.md`](docs/GLOSSARIO-E-REGRAS.md).
- Cada versão publicada deve ganhar uma pasta própria; não sobrescreva snapshots anteriores.

Os nomes oficiais de itens, monstros, NPCs, chefes e masmorras permanecem no idioma original. `Giant's Tower`, `Skill` e `Codex` também permanecem em inglês. O projeto mantém placeholders e tags do jogo e revisa o português, a concordância e o gênero dos diálogos.

A chave AES é segredo de mantenedor e fica apenas em armazenamento local privado; nunca a inclua em commits, Releases, capturas ou mensagens públicas.
