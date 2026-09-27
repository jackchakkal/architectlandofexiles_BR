# Glossário e decisões editoriais

| Original/termo | Tratamento PT-BR |
| --- | --- |
| Item names/títulos próprios de itens | Sempre manter a string original, inclusive fragmentos `ParamN` usados no título — **e em qualquer menção ao item dentro de outros textos** (missões, diálogos, conquistas, tutoriais, loja): "Compre uma Rejuvenation Potion", "Fabricar Weapon Enhancement Stone". |
| Nomes de Skills (`Skill_Name.Name`, `SkillDescription_Name.Title`) e efeitos/buffs com o mesmo nome | **Manter em inglês**, em qualquer menção. Motivo: os livros de Skill são itens (`Skillbook [{Param1}]`, com o nome da Skill em inglês) e o jogador precisa relacionar o livro à Skill. Descrições das Skills são traduzidas. |
| Nomes de masmorras (`Dungeon_Name.Name`/`Param`, `DungeonSection_Name.Name`/`StringParam`) | **Manter em inglês em qualquer lugar mencionado**: tabela da masmorra, objetivos de missão, descrições de efeitos ("Aplica-se apenas dentro de Ancient Ruins"), menus. |
| Giant's Tower | Manter nome oficial original; traduzir o restante da frase. |
| Skill | Manter `Skill`. |
| Codex | Manter `Codex`. |
| Dungeon/masmorra com nome oficial | Manter nome original. |
| Monster/NPC/boss names | Manter nomes próprios originais, em qualquer menção ("Derrote o Guardian of the Treasure"). |
| left em contador de tempo/quantidade | “restante(s)”. |
| left em instrução espacial | “à esquerda”, conforme o contexto. |
| Finger accessory slot | “Acessório equipado no dedo.” |
| Neck accessory slot | “Acessório equipado no pescoço.” |
| Ear accessory slot | “Acessório equipado na orelha.” |
| Arm accessory slot | “Acessório equipado no braço.” |

## Revisão de diálogos

Use o gênero da pessoa que fala para auto-referências (“obrigado/obrigada”) e o gênero do interlocutor para tratamentos diretos (“aventureiro/aventureira”). Não aplique substituições globais sem contexto: uma fala pode mencionar outro personagem ou usar o termo genericamente.

## Integridade técnica

Não altere IDs, cabeçalhos, placeholders, tags de cor/formatação, códigos de controle ou capitalização de nomes próprios sem comparar o texto original e testar a saída extraída do PAK.

## Comprimento dos textos de interface (a partir da v13)

A interface foi desenhada para o inglês. Regra para rótulos, títulos de janela, botões e abas (`ClientString_Name.csv` e afins): **o português não deve exceder o inglês em mais de ~20%**; quando exceder, encurtar em vez de traduzir literalmente. Preferências de termos curtos:

| Inglês | Preferir | Evitar |
| --- | --- | --- |
| Settings | Ajustes | Configurações |
| Info | Info | Informações sobre… |
| Stats | Atributos | Estatísticas |
| Rank / Ranking (placar) | Ranking | Classificação |
| Rank (cargo no clã) | Cargo | Classificação de membro |
| Auto-… | … auto. / … automático (se couber) | … de forma automática |
| Claim (reward) | Receber | Reivindicar |
| No … found. | Nenhum … . | Nenhum … foi encontrado. |
| Reward Info | Info de recompensa | Informações de recompensa |
| Scan | Varredura | Verificação |

Mensagens de corpo (descrições, diálogos, tooltips longos) não têm essa restrição, mas devem evitar duplicações e enchimento. A fila de candidatos a encurtar é gerada comparando o comprimento com o inglês (ver `TECHNICAL_PROCESS.md`).

## Nomes em inglês dentro de frases: como o processo garante

- `tools/apply_overrides.py` aplica duas regras automáticas a cada versão (`__restore_exact_names__` e `__replace_translated_names__` em `changes/<de>-to-<para>/overrides.json`): células cujo original é exatamente um nome de Skill/item/masmorra voltam ao inglês, e traduções conhecidas de nomes de Skill dentro de frases são trocadas pelo nome em inglês.
- Frases que citam itens/masmorras precisam de reescrita manual; o rastreador dessas menções é o script de varredura descrito em `TECHNICAL_PROCESS.md` (seção "Nomes que devem ficar em inglês"). Falsos positivos conhecidos (skills passivas com nome descritivo como "Increases Evasion", "Blessing") podem ser ignorados.
- Em português, o nome em inglês entra sem tradução e sem aspas, com artigo quando a frase pedir: "a Replica Seed", "o Baba Liquor", "em Ancient Ruins".
