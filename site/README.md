# Site público Architect Atlas

Esta é a versão leve e pública da wiki local. Contém 76 guias adaptados, as capturas enviadas pelo jogador e uma página dedicada à tradução. O acervo de arquivos originais extraídos do jogo, milhares de ícones e os ZIPs de tabelas originais permanecem somente na área de trabalho local.

## Publicar na Vercel

1. Importe `jackchakkal/architectlandofexiles_BR` na Vercel.
2. Defina **Root Directory** como `site`.
3. Escolha **Other** como framework; não há comando de build nem variáveis de ambiente.
4. Publique a branch `main`. A Vercel servirá `index.html` e os arquivos estáticos desta pasta.
5. Confirme que `https://SEU-DOMINIO/style.css`, `/app.js` e `/images/lena-dialogo.webp` abrem. Se a página aparecer sem estilo, confira **Root Directory = site** e faça um novo deploy da branch `main`.

O site não instala nada no computador do visitante. A busca dos guias roda somente no navegador. O formulário de feedback abre uma Issue pública no GitHub após revisão do visitante. O formulário privado da página de contato envia os campos preenchidos ao Formspree, que os entrega ao responsável pelo projeto. O e-mail de destino fica configurado no painel do Formspree e não consta no código do site. Fontes Google Fonts são carregadas externamente; se indisponíveis, o site usa fontes locais do sistema.

## Contato privado

- Endpoint público do formulário: `https://formspree.io/f/mnpnownn`. Ele identifica o formulário, não o endereço de e-mail destinatário.
- O responsável deve conferir no painel do Formspree que o formulário está ativo e que recebe mensagens. Nenhuma mensagem real de teste é enviada automaticamente por este projeto.
- Para trocar o destinatário, altere apenas a configuração privada no Formspree. Para trocar o formulário, atualize o atributo `action` em `contato.html`.
- Não inclua o endereço de e-mail destinatário, tokens ou credenciais no repositório ou em variáveis de JavaScript público.

## Atualização

- Capturas em `images/` foram convertidas das imagens fornecidas pelo jogador para WebP. Capturas repetidas aparecem uma vez.
- O código de amigo aparece na faixa de `index.html` e `contato.html`, na seção `#convite` e no README da raiz. Revise a disponibilidade do evento e atualize ou remova essas referências quando ele terminar. As três capturas `convite-*.webp` mostram onde registrar o código.
- `guides.js` contém apenas os 76 guias adaptados do acervo local da wiki. Cada guia oferece link para sua fonte oficial.
- Atualize links de download e manifestos quando uma nova release for publicada.
