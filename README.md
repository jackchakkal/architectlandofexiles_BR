# Architect: Land of Exiles — Tradução para português do Brasil

Tradução comunitária, não oficial, dos textos do jogo **Architect: Land of Exiles** (PC) para PT-BR. Cobre interface, missões, diálogos, tutoriais, descrições de itens, Skills, efeitos e conquistas — cerca de 133 mil células de texto em 227 tabelas.

> Este projeto não tem vínculo com a desenvolvedora nem com a publisher do jogo. Os textos originais pertencem aos seus detentores; aqui estão apenas as traduções e as ferramentas para aplicá-las.

## Quero jogar em português

1. Baixe o ZIP da versão mais recente na página de **Releases** deste repositório.
2. Extraia o ZIP inteiro e execute `Instalar-Traducao-PTBR.bat`.
3. Abra o jogo. No seletor de idioma, a opção **Português (Brasil)** substitui "English".

Guia completo, com o que acontece no seu computador e como remover: [docs/INSTALACAO-PARA-JOGADORES.md](docs/INSTALACAO-PARA-JOGADORES.md).

Se você prefere não executar scripts, o guia mostra como **copiar o PAK manualmente**. A [wiki pública e página da tradução](site/) ficam na pasta `site/`, pronta para publicação na Vercel.

- [Abrir o site Architect Atlas](https://architect-br.vercel.app/) · [enviar feedback](https://architect-br.vercel.app/#feedback) · [contato e parcerias](https://architect-br.vercel.app/contato)
- [Baixar a versão v13](https://github.com/jackchakkal/architectlandofexiles_BR/releases/tag/v13)

- **O que exatamente o instalador faz** (transparência total): [docs/TRANSPARENCIA.md](docs/TRANSPARENCIA.md)
- **O que está e o que não está traduzido**: [docs/CONTEUDO-DA-TRADUCAO.md](docs/CONTEUDO-DA-TRADUCAO.md)
- Erros de tradução, texto cortado, sugestões: use o [formulário do site](https://architect-br.vercel.app/#feedback) ou abra uma *Issue* com uma captura de tela.

## Como funciona

A tradução é um único arquivo de ~12 MB (`pakchunk9999-Windows_21474835_P.pak`) copiado para `ProjectTT\Content\Paks\` dentro da pasta do jogo. Ele contém somente as 227 tabelas de texto traduzidas e é carregado pelo Unreal Engine com prioridade sobre as tabelas originais. Nenhum arquivo do jogo é modificado; remover a tradução é apagar esse arquivo. Detalhes: [docs/COMO-A-TRADUCAO-E-CARREGADA.md](docs/COMO-A-TRADUCAO-E-CARREGADA.md).

## Para colaboradores e mantenedores

- Snapshots publicados: [`translations/v12-corrections/`](translations/v12-corrections/) e [`translations/v13/`](translations/v13/) (correções de textos que estouravam a tela).
- Cada versão tem pasta própria e imutável; as diferenças ficam em `changes/`.
- Regras de tradução e glossário: [docs/GLOSSARIO-E-REGRAS.md](docs/GLOSSARIO-E-REGRAS.md).
- Processo técnico (extração, comparação após atualização do jogo, auditoria, build do PAK): [docs/TECHNICAL_PROCESS.md](docs/TECHNICAL_PROCESS.md).
- Auditoria reproduzível: [`docs/AUDIT-v12.json`](docs/AUDIT-v12.json); resumo em [`releases/`](releases/).

Nomes próprios de itens, monstros, NPCs, chefes e masmorras permanecem no idioma original de propósito (busca no Marketplace e comunicação com outros jogadores). `Giant's Tower`, `Skill` e `Codex` também permanecem em inglês.

A chave AES do jogo, necessária para gerar o PAK, é segredo de mantenedor e nunca entra neste repositório.

## Contato e independência

Consulte [CONTACT.md](CONTACT.md) para sugestões, colaboração, pedidos de revisão ou remoção e propostas institucionais. Mensagens em Issues são públicas; o site identifica claramente o canal disponível.

Projeto independente feito por fã. A wiki e a tradução não são oficiais e não têm relação, aprovação ou suporte da desenvolvedora, da editora ou de qualquer empresa responsável por Architect: Land of Exiles.

Independent fan project. This wiki and translation are unofficial and are not affiliated with, endorsed by, or supported by the game developer, publisher, or any company responsible for Architect: Land of Exiles.
