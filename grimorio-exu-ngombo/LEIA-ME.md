# Grimório dos meus Exus · Emilly

Mesmo formato do "Grimório dos Exus" do Cauã (estrutura, tipografia, molduras, quadros "quem é", ficha, conselhos, o que fazer e o que comprar), com o conteúdo e as imagens do grimório da Emilly. 36 páginas A5.

## Arquivos
- `Grimorio_Emilly_A5_leitura.pdf` — modo de leitura: páginas A5 soltas, fundo claro com marcas de papel envelhecido em branco.
- `Grimorio_Emilly_A4_construcao.pdf` — modo de construção, para imprimir: 9 folhas A4 deitadas, frente e verso, cada folha dobrada guarda 4 páginas seguidas. Sem fundo (o papel pardo claro aparece), com faixa de 27 mm livre na dobra para os furos.
- `faces-A4/` — as 18 faces de impressão em JPEG, caso o PDF não abra.
- `paginas-leitura/` e `paginas-construcao/` — cada página em PNG.
- `fonte/` — HTML, fontes (IM Fell DW Pica, Tangerine, Fondamento, La Belle Aurore), imagens e scripts.
- `versao-anterior/` — a versão anterior do grimório (32 páginas).

## Capa
O centro do medalhão é a arte do Gemini: `fonte/img/emblema.png`, com fundo transparente. O original está em `fonte/img_raw/emblema_gemini.webp`.

## Montagem das folhas (modo de construção)
| Folha | Frente (esq. \| dir.) | Verso (esq. \| dir.) |
|---|---|---|
| 1 | 4 \| 1 | 2 \| 3 |
| 2 | 8 \| 5 | 6 \| 7 |
| 3 | 12 \| 9 | 10 \| 11 |
| 4 | 16 \| 13 | 14 \| 15 |
| 5 | 20 \| 17 | 18 \| 19 |
| 6 | 24 \| 21 | 22 \| 23 |
| 7 | 28 \| 25 | 26 \| 27 |
| 8 | 32 \| 29 | 30 \| 31 |
| 9 | 36 \| 33 | 34 \| 35 |

## Impressão sem frente e verso automático
O PDF de construção tem 18 páginas: em cada par, a primeira é a frente da folha e a segunda o verso. Teste com 2 folhas: imprima as páginas 1 e 3, marque a lápis o verso, vire como página de livro e imprima as páginas 2 e 4. Confira se o verso saiu de pé e se a folha 1 recebeu a página 2. Depois: frentes 1, 3, 5, ..., 17 e versos 2, 4, 6, ..., 18. Se a pilha sair invertida, use "ordem inversa" nos versos. A4 paisagem, escala 100%.

## Para refazer
`node fonte/render.mjs leitura` e `node fonte/render.mjs construcao` geram as páginas; `python3 -I fonte/fazer_folha_a_folha.py <pasta-construcao> Grimorio_Emilly_A4_construcao.pdf faces-A4` refaz a montagem.
