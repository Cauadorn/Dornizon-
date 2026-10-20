# Grimório · Consulta ao Oráculo de Exu Ngombo

## Arquivos
- `grimorio-caderninho-A4.pdf` — **use este para imprimir**. 6 folhas A4 paisagem, 12 faces, duas páginas A5 por face, já na ordem de caderno dobrado.
- `grimorio-exu-ngombo.pdf` — as 24 páginas soltas em A5, na ordem de leitura (para ver na tela ou mandar para gráfica).
- `paginas/` — cada página em PNG.
- `visao-folhas-A4.jpg` — prévia das 10 faces impressas; `visao-geral.jpg` — prévia das páginas.

## Como imprimir o caderninho
1. Abra `grimorio-caderninho-A4.pdf`.
2. Papel A4, orientação **paisagem**, escala **100% / tamanho real** (não use "ajustar à página").
3. Frente e verso (duplex) com **virar na borda curta** ("flip on short edge").
   Se a impressora não tiver duplex: imprima só as páginas ímpares (1, 3, 5, 7, 9, 11), recoloque as folhas e imprima as pares (2, 4, 6, 8, 10, 12) no verso.
4. Teste com a primeira folha antes de rodar tudo: a frente deve ter a contracapa à esquerda e a capa à direita; o verso, a página "Este grimório pertence a" à esquerda e "Anotações" à direita.
5. Empilhe as 6 folhas na ordem e dobre o maço ao meio pela marquinha no centro (topo e base).
6. **Furos:** cada página tem 24 mm livres junto à dobra. Fure com o furador na dobra (centro dos furos a uns 10 a 12 mm da dobra) e prenda nas argolas do grimório. Nada de texto, ornamento ou ilustração entra nessa faixa.

## Margens pensadas para impressora caseira
- Borda externa, topo e base: nada a menos de 8 mm da borda do papel (as impressoras não imprimem nos últimos 4 a 5 mm, então vai sobrar um filete branco de papel em volta do pergaminho; se a impressora tiver modo "sem borda", pode usar).
- Lado da dobra: 24 mm livres para os furos.
- Cantoneiras rabiscadas só nos cantos externos, a 8 mm da borda.

Ordem das faces (esquerda | direita): 24|1, 2|23, 22|3, 4|21, 20|5, 6|19, 18|7, 8|17, 16|9, 10|15, 14|11, 12|13.

## Páginas de curiosidades
As páginas "Sobre Dona Maria Caveira" (13 e 14) e "Sobre Seu Cobra Coral" (17 e 18), mais as notas sobre o Reino da Lira, ngombo, mutuê, bacuro e Exu Caveira, foram escritas a partir de pesquisa em páginas de Umbanda e Quimbanda, museus (cesto ngombo) e guias de fauna. Fontes principais: axeumbanda.com.br (Cobra Coral e Maria Caveira), axedanfeero.com.br e joiamisticalaroye.com.br (reinos e povos da Quimbanda), quimbandanago.com (Reino da Lira), Câmara de Porto Alegre (Lei 13.088/2022, Dia da Pombagira Maria Caveira), Carlos Museum e MBAM (ngombo), InfoEscola e Fiocruz (cobra coral). Cada casa tem seu fundamento; o da sacerdotisa vem primeiro.

## Para editar
O texto está em `fonte/grimorio.html`. Depois de mexer: `node fonte/render.mjs` gera o A5 e os PNGs; `python3 fonte/impor-caderninho.py grimorio-exu-ngombo.pdf grimorio-caderninho-A4.pdf` refaz a imposição.
