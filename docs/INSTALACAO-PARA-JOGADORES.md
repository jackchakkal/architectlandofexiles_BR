# Instalar a tradução (guia do jogador)

## O que você deverá fazer

Quando uma versão instalável for publicada, o processo será:

1. Abra a página **Releases** do projeto e baixe o instalador da versão mais recente. Não baixe o código-fonte nem as pastas `translations/`.
2. Feche Architect: Land of Exiles.
3. Abra o arquivo do instalador e clique em **Instalar tradução**. O instalador tentará localizar o jogo sozinho. Se não encontrar, ele mostrará uma janela para você selecionar a pasta do jogo.
4. Aguarde a confirmação de instalação e abra o jogo.

Para voltar ao original, abra o mesmo instalador e escolha **Restaurar versão anterior / Remover tradução**. O instalador guarda cópias dos arquivos substituídos e verifica os arquivos copiados.

Você não deverá precisar instalar Python, Git, Unreal Engine, repak, usar PowerShell, editar arquivos, obter uma chave AES ou conversar com uma IA. O instalador baixado de uma Release oficial deve conter tudo o que o jogador precisa.

## Situação atual

**Ainda não há instalador para o público nesta página.** A versão v12 foi aplicada e verificada no computador dos mantenedores, mas o repositório contém as tabelas e as ferramentas de desenvolvimento, não um pacote de instalação pronto para jogadores. Não tente instalar baixando ou copiando arquivos da pasta `translations/`.

Antes de publicar o instalador, precisamos validar uma forma de distribuir somente o patch de tradução sem incluir arquivos originais do jogo. O pacote principal usado para a instalação de desenvolvimento reúne milhares de arquivos do jogo e não deve ser anexado a uma Release pública. Também precisamos validar o método de instalação em uma instalação limpa do jogo e testar atualização e restauração.

Quando esses requisitos forem concluídos, esta seção será atualizada com o link e as instruções finais da Release.

## Se precisar pedir ajuda após a publicação

Informe a versão da tradução, a loja usada para instalar o jogo e uma captura da mensagem de erro. Não envie arquivos do jogo, credenciais, chaves ou dados da sua conta.