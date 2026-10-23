# Grimório do Tarot · Arcanos Menores

As "Fichas Rápidas" da Prof. Edite Pedro (60 páginas) reorganizadas no formato dos meus grimórios: mesma tipografia, papel envelhecido, molduras e faixa de furos. 124 páginas A5.

## Como está organizado
- **1** capa · **2** sobre estas fichas (texto da Edite) · **3** como ler a ficha e os quatro naipes
- Cada naipe abre com duas páginas: o naipe (elemento e tema) e o índice das 14 cartas, com a primeira palavra de luz, sim/não e a página.
  Copas p. 4 · Paus p. 34 · Espadas p. 64 · Ouros p. 94
- **Cada carta ocupa duas páginas, uma de frente para a outra** (par à esquerda, ímpar à direita):
  - esquerda, *leitura rápida*: a carta, sim/não circulado, elemento, planeta, signo, tempo, a afirmação na moldura, luz (positivos) e sombra (negativos);
  - direita, *para aprofundar*: arquétipo, os símbolos da carta, as cores, numerologia, ervas e cristais.
  - Nas fichas com muito texto, as cores ou a numerologia passam para a página da esquerda, para a letra não ficar pequena.
- Ordem dentro do naipe: Ás ao 10, Valete, Cavaleiro, Rainha, Rei.
- **124** sobre a Edite Pedro e anotações.

## Arquivos
- `Grimorio_Tarot_A5_leitura.pdf` — modo de leitura: páginas A5 soltas, fundo de papel envelhecido.
- `Grimorio_Tarot_A4_construcao.pdf` — modo de construção, para imprimir: 31 folhas A4 deitadas, frente e verso. Cada folha dobrada guarda 4 páginas seguidas. Sem fundo (o papel aparece), com faixa de 27 mm livre na dobra para os furos do fichário.
- `faces-A4/` — as 62 faces de impressão em JPEG, caso o PDF não abra.
- `fonte/` — gerador (`build.py`, `modelo.html`), dados das fichas (`dados/*.json`), imagens das cartas, fontes e scripts.

## Montagem das folhas (modo de construção)
Folha *k*: frente = páginas [4k | 4k−3], verso = [4k−2 | 4k−1]. Exemplo: folha 1 = frente 4|1, verso 2|3; folha 2 = frente 8|5, verso 6|7 (o Ás de Copas). Empilhe as folhas dobradas na ordem e fure na dobra. Como cada folha é independente, dá para tirar e recolocar uma carta no fichário.

## Impressão sem frente e verso automático
O PDF de construção tem 62 páginas: em cada par, a primeira é a frente da folha e a segunda o verso. Teste com 2 folhas: imprima as páginas 1 e 3, marque a lápis o verso, vire como página de livro e imprima as páginas 2 e 4. Confira se o verso saiu de pé e se a folha 1 recebeu a página 2. Depois: frentes 1, 3, 5, ..., 61 e versos 2, 4, 6, ..., 62. Se a pilha sair invertida, use "ordem inversa" nos versos. A4 paisagem, escala 100%.

## O que mudei no conteúdo
O texto das fichas foi mantido. Só corrigi digitação (ex.: "Agua", "Júpter", "Magericão", "Gemgibre", "Talvés", "As" → "Ás") e estes rótulos de cor que não batiam com a bolinha nem com o texto:
- 7 de Paus: a primeira cor "Azul" (bolinha marrom, "conexão com a terra") → Marrom
- 6 e 7 de Ouros: "Preto" na bolinha laranja → Laranja
- 8 de Ouros: o primeiro "Preto" (bolinha branca, "resultado iluminado") → Branco
- Ás de Ouros: tirei o rótulo solto "Solo", que não tinha texto.

## Pontos do original para conferir
Ficaram como estão no PDF da Edite:
- 3 de Paus: a afirmação ("Reconheço o fim de um ciclo.") parece de outra carta.
- 2 de Espadas: a numerologia é a mesma do Ás.
- 6 de Espadas: o tempo é igual ao do 5 de Espadas.
- 2 de Paus e 7 de Copas: a resposta circulada é "Dúvida" (aparece no lugar do "Talvez").
- Valete de Espadas: "Roxo" com bolinha azul. Valete de Ouros: "Laranja" com bolinha branca.
- 6 de Ouros: os cristais Citrino e Pirita estão com as fotos trocadas no original. 3 de Ouros: o Quartzo Verde está com a foto de uma pedra vermelha.
- Textos que parecem cortados: tempo do 8 de Copas ("...mais que cartas"), do Cavaleiro de Copas e do Rei de Copas; último positivo do 9 de Espadas; cor vermelha do 9 de Ouros.

## Para refazer
```
cd fonte
python3 -I build.py                 # gera grimorio.html a partir de dados/*.json
node render.mjs leitura             # páginas em fonte/out/leitura (avisa se alguma estourar)
node render.mjs construcao
cd ..
python3 -I fonte/fazer_pdf_leitura.py fonte/out/leitura Grimorio_Tarot_A5_leitura.pdf
python3 -I fonte/fazer_folha_a_folha.py fonte/out/construcao Grimorio_Tarot_A4_construcao.pdf faces-A4
```
Para corrigir um texto, edite a carta em `fonte/dados/<naipe>.json` e rode de novo.
