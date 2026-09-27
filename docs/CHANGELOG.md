# Histórico de versões

Cada pasta `translations/vN-.../` preserva um snapshot completo e imutável. As mudanças entre snapshots ficam em `changes/`.

## v12-corrections

- 227 tabelas; nenhum ID ausente ou novo em comparação à extração original.
- Auditoria: sem placeholders/tags divergentes, campos traduzíveis vazios, alterações de nome/template/parâmetros de itens ou menções detectadas de Giant's Tower traduzidas.
- Reparo de tags e placeholders em diálogos, quests, tutoriais e descrições de Skills. Traduções preenchidas em rótulos e ações de interface que estavam vazios. Nomes próprios de itens foram mantidos em inglês para preservar busca no Marketplace.
- Dez alertas de `left` foram revisados como instruções/referências direcionais; nenhum é contador de tempo restante.
- Os arquivos v12 foram extraídos do PAK override construído e todos os 227 hashes coincidem com o snapshot.
- Pacotes preparados e descritos no manifesto; instalação no jogo pendente porque o processo estava ativo durante a verificação.

## v11-quality e anteriores

- Snapshots `v0-upload` a `v11-quality` preservados integralmente para histórico. Algumas versões anteriores contêm defeitos corrigidos na v12.
- Consulte `changes/v11-to-v12-corrections/changes.json` para o diff célula a célula e `docs/AUDIT-v12.json` para as verificações reproduzíveis.
