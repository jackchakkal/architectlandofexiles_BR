# Site público Architect Atlas

Esta é a versão leve e pública da wiki local. Contém 76 guias adaptados, as capturas enviadas pelo jogador e uma página dedicada à tradução. O acervo de arquivos originais extraídos do jogo, milhares de ícones e os ZIPs de tabelas originais permanecem somente na área de trabalho local.

## Publicar na Vercel

1. Importe `jackchakkal/architectlandofexiles_BR` na Vercel.
2. Defina **Root Directory** como `site`.
3. Escolha **Other** como framework; não há comando de build nem variáveis de ambiente.
4. Publique a branch `main`. A Vercel servirá `index.html` e os arquivos estáticos desta pasta.

O site não executa código no computador do visitante, não usa backend nem coleta dados. A busca dos guias roda somente no navegador. Fontes Google Fonts são carregadas externamente; se indisponíveis, o site usa fontes locais do sistema.

## Atualização

- Capturas em `images/` foram convertidas das imagens fornecidas pelo jogador para WebP. Capturas repetidas aparecem uma vez.
- `guides.js` contém apenas os 76 guias adaptados do acervo local da wiki. Cada guia oferece link para sua fonte oficial.
- Atualize links de download e manifestos quando uma nova release for publicada.
