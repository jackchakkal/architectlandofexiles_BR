# Architect: Land of Exiles — Português brasileiro

**Quer jogar em português?** Consulte [Instalação para jogadores](docs/INSTALACAO-PARA-JOGADORES.md). No momento, ainda não há um pacote de distribuição validado para jogadores.

## Para jogadores

O ZIP experimental anterior foi retirado: instalado sozinho em `Content/Paks`, traduziu a tela inicial, mas telas de carregamento e textos durante o jogo continuaram em inglês. Não o distribua como tradução completa. O diagnóstico e o plano para testar a necessidade de um ou dois arquivos estão em [Investigação de carregamento dos PAKs](docs/INVESTIGACAO-CARREGAMENTO-PAK.md).

## Para colaboradores e mantenedores

- Snapshot atual: [`translations/v12-corrections/`](translations/v12-corrections/), com 227 tabelas CSV.
- Auditoria: [`docs/AUDIT-v12.json`](docs/AUDIT-v12.json).
- Processo técnico de extração, comparação, empacotamento e manutenção: [`docs/TECHNICAL_PROCESS.md`](docs/TECHNICAL_PROCESS.md).
- Regras de localização: [`docs/GLOSSARIO-E-REGRAS.md`](docs/GLOSSARIO-E-REGRAS.md).
- Cada versão publicada deve ganhar uma pasta própria; não sobrescreva snapshots anteriores.

Os nomes oficiais de itens, monstros, NPCs, chefes e masmorras permanecem no idioma original. `Giant's Tower`, `Skill` e `Codex` também permanecem em inglês. O projeto mantém placeholders e tags do jogo e revisa o português, a concordância e o gênero dos diálogos.

A chave AES é segredo de mantenedor e fica apenas em armazenamento local privado; nunca a inclua em commits, Releases, capturas ou mensagens públicas.
