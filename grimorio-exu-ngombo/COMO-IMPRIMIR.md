# Grimório · Consulta ao Oráculo de Exu Ngombo

## Arquivos
- `grimorio-caderninho-A4.pdf` — **use este para imprimir**. 5 folhas A4 paisagem, 10 faces, duas páginas A5 por face, já na ordem de caderno dobrado.
- `grimorio-exu-ngombo.pdf` — as 20 páginas soltas em A5, na ordem de leitura (para ver na tela ou mandar para gráfica).
- `paginas/` — cada página em PNG.
- `visao-folhas-A4.jpg` — prévia das 10 faces impressas; `visao-geral.jpg` — prévia das páginas.

## Como imprimir o caderninho
1. Abra `grimorio-caderninho-A4.pdf`.
2. Papel A4, orientação **paisagem**, escala **100% / tamanho real** (não use "ajustar à página").
3. Frente e verso (duplex) com **virar na borda curta** ("flip on short edge").
   Se a impressora não tiver duplex: imprima só as páginas ímpares (1, 3, 5, 7, 9), recoloque as folhas e imprima as pares (2, 4, 6, 8, 10) no verso.
4. Teste com a primeira folha antes de rodar tudo: a frente deve ter a contracapa à esquerda e a capa à direita; o verso, a página "Este grimório pertence a" à esquerda e "Anotações" à direita.
5. Empilhe as 5 folhas na ordem, dobre o maço ao meio pela marquinha no centro (topo e base) e grampeie na dobra (grampeador de braço longo) ou costure com linha.

Ordem das faces (esquerda | direita): 20|1, 2|19, 18|3, 4|17, 16|5, 6|15, 14|7, 8|13, 12|9, 10|11.

## Para editar
O texto está em `fonte/grimorio.html`. Depois de mexer: `node fonte/render.mjs` gera o A5 e os PNGs; `python3 fonte/impor-caderninho.py grimorio-exu-ngombo.pdf grimorio-caderninho-A4.pdf` refaz a imposição.
