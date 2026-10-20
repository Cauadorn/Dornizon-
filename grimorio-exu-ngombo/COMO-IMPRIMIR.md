# Grimório · Consulta ao Oráculo de Exu Ngombo

## Arquivos
- `grimorio-caderninho-A4.pdf` — **use este para imprimir**. 8 folhas A4 paisagem, 16 faces, duas páginas A5 por face, já na ordem de caderno dobrado.
- `grimorio-exu-ngombo.pdf` — as 32 páginas soltas em A5, na ordem de leitura (para ver na tela ou mandar para gráfica).
- `paginas/` — cada página em PNG.
- `visao-folhas-A4.jpg` — prévia das 10 faces impressas; `visao-geral.jpg` — prévia das páginas.

## Como imprimir o caderninho
1. Abra `grimorio-caderninho-A4.pdf`.
2. Papel A4, orientação **paisagem**, escala **100% / tamanho real** (não use "ajustar à página").
3. Frente e verso (duplex) com **virar na borda curta** ("flip on short edge").
   Se a impressora não tiver duplex: imprima só as páginas ímpares (1, 3, 5, 7, 9, 11, 13, 15), recoloque as folhas e imprima as pares (2, 4, 6, 8, 10, 12, 14, 16) no verso.
4. Teste com a primeira folha antes de rodar tudo: a frente deve ter a contracapa à esquerda e a capa à direita; o verso, a página "Este grimório pertence a" à esquerda e "Anotações" à direita.
5. Empilhe as 8 folhas na ordem e dobre o maço ao meio pela marquinha no centro (topo e base).
6. **Furos:** toda página tem uma faixa livre padronizada de 27 mm junto à dobra, marcada por uma linha pontilhada a lápis. Fure o maço dobrado dentro dessa faixa com o seu furador (um furador comum fura a 12 mm da borda, bem no meio dela) e prenda nas argolas. Nada de texto, ornamento ou ilustração entra nessa faixa.

## Margens pensadas para impressora caseira
- Borda externa, topo e base: nada a menos de 8 mm da borda do papel (as impressoras não imprimem nos últimos 4 a 5 mm, então vai sobrar um filete branco de papel em volta do pergaminho; se a impressora tiver modo "sem borda", pode usar).
- Lado da dobra: 27 mm livres para os furos, com linha de margem pontilhada.
- Cantoneiras rabiscadas só nos cantos externos, a 8 mm da borda.

Ordem das faces (esquerda | direita): 32|1, 2|31, 30|3, 4|29, 28|5, 6|27, 26|7, 8|25, 24|9, 10|23, 22|11, 12|21, 20|13, 14|19, 18|15, 16|17.

## Páginas de pesquisa
Páginas escritas a partir de pesquisa, para complementar a consulta: "O banho, erva por erva" (9 e 10), "Sobre Dona Maria Caveira" (16 e 17), "Sobre Seu Cobra Coral" (20 e 21) e "De onde eles vêm" (25 e 26). A página 13 é a ilustração dos dois juntos, e as páginas 28 a 30 são pautadas para anotações., mais as notas sobre o Reino da Lira, ngombo, mutuê, bacuro, padê e guia, e Exu Caveira.
Fontes principais: axeumbanda.com.br (ervas, Cobra Coral, Maria Caveira), bonsfluidos.com.br (ervas frias), axedanfeero.com.br e joiamisticalaroye.com.br (reinos e povos da Quimbanda), quimbandanago.com (Reino da Lira), Terra/UFF e Nei Lopes (etimologia de Quimbanda), Revista de Antropologia da USP e dissertações da UFRGS e da UnB (Quimbanda gaúcha, Mãe Ieda do Ogum), Câmara de Porto Alegre (Lei 13.088/2022), Wikipédia (Pombagira, Quimbanda), Carlos Museum e MBAM (ngombo), significados.com.br (calunga), artigos da UFPB e USP (Jurema), InfoEscola e Fiocruz (cobra coral), digitei.com e artigos acadêmicos (padê).
Onde as fontes divergem, a página diz que divergem. Cada casa tem seu fundamento; o da sacerdotisa vem primeiro.

## Se o PDF não abrir no celular
Os dois PDFs são "leves" (cerca de 15 MB): cada página é uma imagem comprimida, o que abre bem no celular, no WhatsApp e em qualquer leitor. A impressão fica com cerca de 240 dpi, suficiente para o traço a lápis.

## Para editar
O texto está em `fonte/grimorio.html`. Depois de mexer: `node fonte/render.mjs` gera o A5 e os PNGs; `python3 -I fonte/fazer_pdf_leve.py paginas grimorio-exu-ngombo.pdf grimorio-caderninho-A4.pdf` refaz os dois PDFs a partir das imagens em `paginas/`.
