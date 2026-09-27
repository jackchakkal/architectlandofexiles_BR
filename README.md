# Architect: Land of Exiles — Português brasileiro

**Quer jogar em português?** O projeto está preparando um instalador simples para jogadores. Consulte [Instalação para jogadores](docs/INSTALACAO-PARA-JOGADORES.md) para ver o processo planejado e o estado atual.

> **Ainda não há um instalador público.** A v12 está aplicada e validada no computador dos mantenedores. Esta página contém os arquivos de tradução e as ferramentas do projeto; não é um download pronto para instalar no jogo. Não é preciso que jogadores comuns usem Git, Python, PowerShell, chaves AES ou ferramentas de modificação.

## Para jogadores

Quando a versão distribuível estiver pronta, será publicada em **Releases** como um instalador do Windows. A instalação deverá localizar o jogo, fazer backup automático e oferecer restauração. A chave AES e os arquivos originais do jogo não serão distribuídos.

## Para colaboradores e mantenedores

- Snapshot atual: [`translations/v12-corrections/`](translations/v12-corrections/), com 227 tabelas CSV.
- Auditoria: [`docs/AUDIT-v12.json`](docs/AUDIT-v12.json).
- Processo técnico de extração, comparação, empacotamento e manutenção: [`docs/TECHNICAL_PROCESS.md`](docs/TECHNICAL_PROCESS.md).
- Regras de localização: [`docs/GLOSSARIO-E-REGRAS.md`](docs/GLOSSARIO-E-REGRAS.md).
- Cada versão publicada deve ganhar uma pasta própria; não sobrescreva snapshots anteriores.

Os nomes oficiais de itens, monstros, NPCs, chefes e masmorras permanecem no idioma original. `Giant's Tower`, `Skill` e `Codex` também permanecem em inglês. O projeto mantém placeholders e tags do jogo e revisa o português, a concordância e o gênero dos diálogos.

A chave AES é segredo de mantenedor e fica apenas em armazenamento local privado; nunca a inclua em commits, Releases, capturas ou mensagens públicas.