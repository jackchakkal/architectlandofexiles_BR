# Transparência: o que a tradução faz no seu computador

Este documento descreve, sem omissões, tudo que o pacote de tradução contém e tudo que o instalador executa. O código está aberto: `tools/player-installer/install.ps1` é o mesmo arquivo que vai dentro do ZIP.

## O que vem no ZIP

| Arquivo | O que é |
| --- | --- |
| `pakchunk9999-Windows_21474835_P.pak` (~12 MB) | Um contêiner no formato PAK do Unreal Engine com **227 arquivos CSV** de texto traduzido, todos no caminho interno `ProjectTT/Content/TT/Data/CSV/L10N/en/`. Não contém executáveis, DLLs, modelos, texturas, sons nem qualquer outro conteúdo do jogo. |
| `release.json` | Versão da tradução, nome do PAK e seu SHA-256. O instalador usa esse hash para conferir a integridade antes de copiar. |
| `install.ps1` | O instalador/desinstalador (PowerShell, texto puro, ~120 linhas). |
| `Instalar-Traducao-PTBR.bat` / `Desinstalar-Traducao-PTBR.bat` | Atalhos de dois cliques que chamam `install.ps1` com `-ExecutionPolicy Bypass` (necessário porque o Windows bloqueia scripts PowerShell por padrão; o bypass vale só para essa execução). |
| `LEIA-ME.txt` | Instruções resumidas. |

## O que o instalador faz, passo a passo

1. **Lê `release.json`** na própria pasta para saber o nome do PAK e o hash esperado.
2. **Procura a pasta do jogo.** Consulta as chaves de programas instalados do Windows (`HKLM\...\Uninstall`, `HKCU\...\Uninstall`) procurando um nome contendo "Architect", e testa pastas comuns em todas as unidades (`Games\Architect`, `DRIMAGE\Architect`, `Program Files\Architect`…). Uma pasta só é aceita se contiver `Architect.exe` **e** `ProjectTT\Content\Paks\pakchunk0-Windows.pak`. Se nada for encontrado, pergunta o caminho a você. Nenhuma outra pasta do computador é lida.
3. **Verifica se o jogo está aberto** (processos `Architect`, `Architect-Win64-Shipping`, `ProjectTT`, `DRIMAGE*`). Se estiver, para sem alterar nada.
4. **Confere o SHA-256 do PAK** que veio no ZIP contra o `release.json`. Se não bater (download corrompido ou arquivo trocado), para sem alterar nada.
5. **Remove versões anteriores da tradução**: apaga em `ProjectTT\Content\Paks\` qualquer arquivo com o padrão `pakchunk9999-Windows*_P.pak`. Esse padrão é exclusivo deste projeto; nenhum arquivo do jogo usa o número 9999.
6. **Copia o PAK** para `ProjectTT\Content\Paks\` com o nome temporário `.tmp`, confere o hash da cópia e só então a renomeia para o nome definitivo. Se a verificação falhar, o `.tmp` é apagado.
7. **Grava `ProjectTT\Content\Paks\traducao-ptbr.json`** com versão, nome do PAK, hash e data de instalação — para o desinstalador e para diagnóstico.

O que ele **não** faz: não modifica, renomeia nem apaga nenhum arquivo original do jogo; não acessa a internet; não altera o registro do Windows (só lê); não instala serviços, tarefas agendadas ou programas; não pede privilégios de administrador (a menos que a pasta do jogo exija permissão de escrita, caso em que o Windows pedirá).

## O que o desinstalador faz

Localiza a pasta do jogo do mesmo modo e apaga os arquivos `pakchunk9999-Windows*_P.pak` e `traducao-ptbr.json` em `ProjectTT\Content\Paks\`. Nada mais.

## Como o jogo usa o arquivo

O Unreal Engine monta todos os `.pak` da pasta `Content\Paks` ao iniciar. Quando dois PAKs contêm um arquivo de mesmo caminho, vence o de maior prioridade; o sufixo `_<número>_P` no nome define essa prioridade. O jogo baixa suas tabelas de texto originais para `ProjectTT\Saved\PersistentDownloadDir\DownloadContent\` e as monta com prioridade alta — por isso o nosso PAK usa um número de patch muito alto (21474835), para ficar acima delas. O resultado é que, ao pedir `L10N/en/Quest_Name.csv`, o jogo recebe a versão em português. Explicação completa em [COMO-A-TRADUCAO-E-CARREGADA.md](COMO-A-TRADUCAO-E-CARREGADA.md).

Consequência prática: como o arquivo original continua intacto no lugar, **basta apagar o PAK para voltar ao inglês**, e uma atualização do jogo nunca "quebra" o jogo por causa da tradução — no pior caso, textos novos aparecem em inglês.

## Como conferir por conta própria

- **Integridade do download:** no PowerShell, `Get-FileHash .\pakchunk9999-Windows_21474835_P.pak` deve mostrar o mesmo SHA-256 publicado na Release e em `release.json`.
- **Conteúdo do PAK:** a lista dos 227 arquivos está em [CONTEUDO-DA-TRADUCAO.md](CONTEUDO-DA-TRADUCAO.md); os CSVs em si estão em `translations/<versão>/` neste repositório. O índice do PAK é criptografado com a chave do próprio jogo (exigência do formato usado pelo Architect), então ferramentas genéricas não o abrem sem essa chave.
- **Código do instalador:** `tools/player-installer/install.ps1`.

## Riscos que você deve conhecer

- O jogo é online e usa anticheat (XIGNCODE3). Acrescentar um PAK de texto é uma modificação passiva de dados, não de código, e não temos nenhum relato de sanção — mas a decisão de permitir ou não é da publisher, e pode mudar. Use por sua conta e risco.
- Traduções feitas por voluntários, com apoio de ferramentas automáticas e revisão humana, podem conter erros de sentido. Em dúvida sobre uma regra do jogo, consulte o texto original (basta desinstalar).
