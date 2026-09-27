# Histórico de versões

Cada pasta `translations/vN-.../` preserva um snapshot completo e imutável. As mudanças entre snapshots ficam em `changes/`.

## v12-corrections

- 227 tabelas; nenhum ID ausente ou novo em comparação à extração original.
- Auditoria: sem placeholders/tags divergentes, campos traduzíveis vazios, alterações de nome/template/parâmetros de itens ou menções detectadas de Giant's Tower traduzidas.
- Reparo de tags e placeholders em diálogos, quests, tutoriais e descrições de Skills. Traduções preenchidas em rótulos e ações de interface que estavam vazios. Nomes próprios de itens foram mantidos em inglês para preservar busca no Marketplace.
- A busca automática produziu dez alertas com `left`; a lista contém tanto direções reais quanto contadores restantes. No snapshot v12, chaves de contador como `AUCTION_MENU_LEFTTIME`, `CLAN_EXCHANGE_LEFT_TIME`, `CLAN_RESEARCH_TOGGLE_ACTIVATE_LEFT_TIME`, `COMMON_LEFT` e `COMMON_LEFT_TIME` estão traduzidas com “restante(s)”.
- Os arquivos v12 foram extraídos do PAK override construído e todos os 227 hashes coincidem com o snapshot.
- Dois PAKs foram instalados temporariamente em 2026-09-27 e os hashes foram conferidos. Depois, o teste de um único override mostrou tradução apenas na tela inicial. O jogo foi restaurado ao estado limpo; distribuição bloqueada até concluir a investigação documentada em `docs/INVESTIGACAO-CARREGAMENTO-PAK.md`.

## v11-quality e anteriores

- Snapshots `v0-upload` a `v11-quality` preservados integralmente para histórico. Algumas versões anteriores contêm defeitos corrigidos na v12.
- Consulte `changes/v11-to-v12-corrections/changes.json` para o diff célula a célula e `docs/AUDIT-v12.json` para as verificações reproduzíveis.
