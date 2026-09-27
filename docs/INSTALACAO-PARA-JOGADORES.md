# Instalação para jogadores

## Antes de começar

- Funciona na versão para PC (Windows) do Architect: Land of Exiles instalada pelo launcher oficial.
- É um projeto comunitário, sem vínculo com a publisher. Modificar arquivos na pasta de um jogo online pode contrariar os termos de uso do serviço; o jogo usa um sistema anticheat. Não temos relato de problemas — a tradução não altera nenhum arquivo do jogo, só acrescenta um — mas **o uso é por sua conta e risco**.
- Se quiser saber exatamente o que o instalador faz antes de executá-lo, leia [TRANSPARENCIA.md](TRANSPARENCIA.md).

## Instalar

1. Baixe `Architect-PTBR-<versão>.zip` na página de Releases.
2. Extraia o ZIP inteiro em qualquer pasta (Área de Trabalho, Downloads…). Não execute de dentro do ZIP.
3. Feche o jogo e o launcher.
4. Dê dois cliques em **`Instalar-Traducao-PTBR.bat`**.
   - O Windows pode mostrar o aviso "SmartScreen" por ser um script sem assinatura digital. Clique em *Mais informações* → *Executar assim mesmo*. Se preferir, leia o `install.ps1` antes — é texto puro.
   - O instalador procura a pasta do jogo sozinho. Se não encontrar, cole o caminho da pasta que contém `Architect.exe` (por exemplo `H:\Games\Architect`).
5. Abra o jogo. No seletor de idioma, escolha **Português (Brasil)** (é a posição que antes era "English").

## Remover

Dê dois cliques em **`Desinstalar-Traducao-PTBR.bat`**. Ele apaga o arquivo da tradução e o jogo volta ao original. Também é possível apagar manualmente `ProjectTT\Content\Paks\pakchunk9999-Windows_21474835_P.pak` (e `traducao-ptbr.json`) na pasta do jogo.

## Atualizar a tradução

Baixe o ZIP da nova versão e execute o instalador de novo. Ele remove a versão anterior automaticamente.

## Perguntas frequentes

**O jogo atualizou e a tradução sumiu / apareceram textos em inglês.**
Uma atualização do jogo pode acrescentar textos novos (ficam em inglês até a próxima versão da tradução) ou, em casos raros, remover arquivos desconhecidos da pasta `Paks`. Em ambos os casos, rode o instalador de novo e verifique se há versão nova nas Releases.

**Preciso instalar algo mais? Python, .NET, Visual C++?**
Não. O instalador usa apenas o PowerShell, que já vem com o Windows.

**O antivírus reclamou.**
Scripts `.bat`/`.ps1` sem assinatura às vezes disparam alertas heurísticos. O código está aberto neste repositório; compare o hash SHA-256 do PAK com o publicado na Release se quiser conferir a integridade.

**Alguns textos aparecem cortados ou saindo da caixa.**
A interface foi desenhada para o inglês, que é mais curto. Estamos encurtando rótulos versão a versão; mande uma captura de tela numa Issue.

**Nomes de itens e monstros continuam em inglês. É um erro?**
Não, é decisão de projeto: preserva a busca no Marketplace e a comunicação com jogadores de outros idiomas. Veja [CONTEUDO-DA-TRADUCAO.md](CONTEUDO-DA-TRADUCAO.md).

**Posso usar em outra plataforma ou no celular?**
Não. Só a versão Windows do launcher oficial foi testada.
