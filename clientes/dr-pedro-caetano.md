# Dr. Pedro Caetano

Cardiologista, intensivista e cardiologista do esporte. Assinatura: **Dr. Pedro Caetano · CRM MG 57332 | RQE 58785**.

## Onde está cada coisa

- **Figma**: arquivo "SOCIAL MEDIA CLIENTES 4D" (`ZzrH9wPx7VqPrAZxHcLbi5`), página "Dr. Pedro Caetano" (`9280:2`). Não fica no "Criativos CREDFRANCO - 4D". Os frames são nomeados `#<card> <título> — lâmina N vX`.
- **Drive**: a pasta raiz é "DR PEDRO CAETANO" (`10tZchCND_Fjj7Y0tPJumYWVvo1FonDUJ`).
  - Logos: "Arquivos - logotipo Pedro Caetano".
  - Fotos: "Fotos e vídeos" (`17iM1l76FWeInhx8fAPkXG08Jl9fOMf6J`).
    - "Fotos - Dr. Pedro" tem o retrato de estúdio (terno cinza, fundo escuro, mãos livres, olhando para a câmera), arquivo `1M_2IacOZFMIyQvMpTkF-67s1tz9Ct5mb`, com 1112x1600.
    - "Julho/26 > Fotos" tem fotos de celular.
    - Os originais do ensaio profissional estão em "Março/2026 > FOTOS" (DSC*, de 8 a 10 MB cada). Esses arquivos são grandes demais para o conector do Drive e precisam ser baixados à mão.
- **Magnific**: o projeto da 4D tem a ficha de personagem "Prancha Dr Pedro", que serve de referência do rosto. As imagens do carrossel são geradas no Nano Banana Pro 2K, que é ilimitado no login da 4D. Pelo conector MCP a geração dá "limite de uso" (o ilimitado não vale lá), então o Cauã roda o nó no Space e eu confiro o resultado.
- **Design System no Claude**: ainda não existe (conferido em 09/11/2026). Os artifacts "Design System" sem nome estão vazios.

## Visual (carrosséis de 11/2026)

- O carrossel é contínuo: o fundo de uma lâmina emenda na seguinte. Ao trocar a imagem de uma lâmina, a faixa da borda que encosta na lâmina vizinha fica intacta.
- A paleta é vinho e vermelho, com luz de janela quente vinda da esquerda e uma textura de pontinhos (halftone) no fundo.
- O texto fica na coluna da esquerda e o Dr. Pedro fica à direita.
- O Dr. Pedro dos carrosséis é gerado no Magnific a partir da "Prancha Dr Pedro" e precisa parecer foto real.
- No slide de CTA ele aparece sem objeto nas mãos e olhando para a câmera (pedido do Emanuel no card 6898), mas mantendo a cena de atendimento: de frente para o paciente do slide anterior.
- Antes de entregar uma imagem gerada, conferir de perto:
  - **Dedos:** cinco dedos, juntos e naturais, polegar coerente.
  - **Rosto:** realista, sem aspecto de cera.
  - **Sombra:** uma só, presa ao corpo e coerente com a luz da janela vinda do alto à esquerda.
  - **Bordas:** sem listras ou faixas.
  - **Emenda:** batendo com a lâmina vizinha.

## Histórico

- **#6898 Frequência cardíaca de repouso**: o slide 5 aprovado é a **v6**, frame `19880:2`. A imagem veio do Space "#6898 Dr Pedro · lâmina 5 CTA", em duas passadas: a primeira tirou o tablet e virou o olhar para a câmera, a segunda corrigiu as mãos, a pele com aspecto de cera, a sombra solta e as listras na borda.
- **#6898 (tentativa anterior, descartada)**: o slide 5 passou para a v5, com o retrato de estúdio recortado e tratado em tons quentes e vinho. O fundo da parede foi recomposto a partir da própria parede da v4 (script em `dr-pedro-caetano/6898-frequencia-cardiaca-repouso/projeto/`). O frame v5 é o `19874:71`, abaixo da fileira v4.
