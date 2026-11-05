# Direção de arte

## As 10 referências (`referencias/`)

| Arquivo | O que tirar dela |
|---|---|
| ref-01 · caju | guache digital solto, sombra em 2 tons, fruta vazando a borda |
| ref-02 · castanha-do-pará | pincel seco, sol em círculo chapado, formas simplificadas |
| ref-03 · mico-leão-dourado | moldura de carta, pelo em pinceladas direcionais, fundo único |
| ref-04 · açaí | fundo terracota, folhas em faixas de 3 tons, frutos com variação |
| ref-05 · arara | formas facetadas, contorno branco recortado |
| ref-06 · jacaré | arte folk chapada, moldura ondulada listrada, ornamentos suaves, 4 cores |
| ref-07 · pavão | padrão do leque simplificado e repetido, fundo liso |
| ref-08 · bananeira | colagem de planos, respingos e linhas finas, contraste alto |
| ref-09 · cacau | fundo escuro, composição de papel de parede |
| ref-10 · onça rosa | hachura fina, animal monocromático, fundo amarelo liso |

As referências são estudo de linguagem: identificar e creditar a autoria antes de publicar; não usar como imagem de entrada em IA.

## O método (validado no lote 1: MG, BA, PE, GO)

Cada estado tem **duas peças unidas pelos mesmos elementos**:

| | Ilustração (campanha) | Chinelo (produto) |
|---|---|---|
| Papel | mostrar o **lugar**: bater o olho e saber o estado | levar os **elementos**, como no modelo Ararinhas da collab |
| Forma | cena **centralizada e simétrica** (conferida por medição) | **díptico**: palmilha esquerda + direita, fundo chapado |
| Texto | nenhum | nenhum (letreiro só se o estado precisar, como o R\|J da collab) |
| Base | faixa chapada de cor da paleta para o logo | respiro no calcanhar para o logo |

- O chinelo precisa de **uma âncora**: um elemento que é daquele estado e de nenhum outro (fita do Bonfim, sombrinha de frevo, talha do barroco mineiro, cavalo da Cavalhada). O resto dá a beleza.
- A ilustração reaproveita os elementos do chinelo (coroa barroca e guirlanda em MG, cacau e fitas na BA, sombrinha e buganvília em PE, cavalo e pequi em GO).
- **Variedade entre estados:** cada lugar com um tipo de cena diferente. **Igreja não é a solução padrão** (o lote 1 já tem as quatro); nos próximos, buscar mercado, rio, praia, duna, festa, ofício, mesa, barco, ponte, paisagem.

## As regras do traço

1. Guache digital: pincelada visível, borda seca, 2 a 3 tons chapados por forma, sem degradê nem brilho plástico.
2. Paleta curta (5 a 7 cores) tirada das fotos de campo; a tira do chinelo repete uma cor da estampa.
3. Elementos grandes, recortados pela borda da palmilha; cheio, mas com respiro.
4. Nada de cena dentro do chinelo; nada de pessoa com rosto.

## O coração (o que une a coleção)

- **Formado pelos próprios elementos**, nunca desenhado em cima deles: duas folhas que se encontram, duas volutas espelhadas, o vão entre duas fitas, dois frutos de pontas encostadas, as pontinhas da franja da sombrinha, a sombra da veneziana.
- **Proibido:** coração pintado em fruta, brilho em forma de coração, confete de coração, coração grande no centro da cena, coração carimbado ou emoji.
- **Sutil:** no primeiro olhar se vê o estado; no segundo, o coração. Um ou dois por peça.

## O logo

Sempre a assinatura oficial da collab (FARM RIO / coração / havaianas), em vetor, aplicada depois:
- **chinelo:** centralizado no calcanhar (eixo medido nas linhas do calcanhar), tom sobre tom, com um fio fino na cor do fundo quando passa sobre um elemento;
- **ilustração:** centralizado na faixa da base, com a mesma folga em cima e embaixo.

## Bicho

Só onde ele é identidade do estado: MS (onça), AM (boto), MA (guará), GO (cavalo das Cavalhadas), PR (gralha-azul), SC (baleia-franca), RS (quero-quero, coadjuvante).

## O que denuncia IA (e a revisão barra)

Detalhe demais por toda parte · brilho e degradê · paisagem realista dentro do chinelo · anatomia errada · coração carimbado ou desenhado em objeto · composição torta (eixo fora do centro) · texto gerado (o logo é sempre aplicado depois, em vetor). Exemplos em `testes-descartados/`.

## Prompt-base

Ver `prompt-base.txt` (dois moldes: chinelo e ilustração). Uma geração por peça, só com o briefing aprovado; ajustes por edição da própria imagem.
