# Glossário e decisões editoriais

| Original/termo | Tratamento PT-BR |
| --- | --- |
| Item names/títulos próprios de itens | Sempre manter a string original, inclusive fragmentos `ParamN` usados no título. |
| Giant's Tower | Manter nome oficial original; traduzir o restante da frase. |
| Skill | Manter `Skill`. |
| Codex | Manter `Codex`. |
| Dungeon/masmorra com nome oficial | Manter nome original. |
| Monster/NPC/boss names | Manter nomes próprios originais. |
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
