# EMS · carrossel "o que chega antes do logo?" (6 × 1080 × 1350)

Carrossel da @itsemsdesign no pilar **bastidor e processo**. Ponto de partida: post da @daimaass.design
("o que você recebe ao se tornar minha cliente?", 12/11/2026), em `referencias/post-daimaass/`.
Dela ficou a ideia (mostrar o que o cliente recebe além da arte pronta) e a linguagem: foto de flor
desfocada no fundo, cartão de cor chapada e pílulas por cima. Texto, conceito e objetos são da EMS.

**Status:** v1, esperando aprovação. Finais em `entrega/` (`lamina-01..06.png` + `visao-geral.jpg`), legenda em `legenda.md`.

## Conceito

"Chega" vira correspondência: a caixa de correio na capa, e cada lâmina é uma coisa que chega antes da marca.
O campo de flor da referência virou lavanda, glicínia, amor-perfeito e hortênsia, tudo na família de roxo da EMS.

| Lâmina | O que chega | Título | Foto | Gráfico |
| --- | --- | --- | --- | --- |
| 1 | capa | o que chega antes do *logo?* | caixa de correio no campo de lavanda (inteira) | letra gigante, pílula, @ |
| 2 | contrato | combinado não sai *caro.* | prancheta no banco, glicínias | faixa violeta com retícula; o contrato impresso na folha |
| 3 | briefing | perguntas que ninguém te *fez.* | caderno sobre amores-perfeitos | cartão ameixa; perguntas sentadas na pauta |
| 4 | direção criativa | o rumo antes do *desenho.* | varal de cartões no campo | amostras nos cartões (cor, letra, matéria, voz), faixa clara |
| 5 | andamento | sem sumiço, sem *suspense.* | celular entre hortênsias | cartão claro; etapas na tela; dois balões |
| 6 | chamada | e só então chega a *marca.* | envelope com lacre (inteira) | pergunta em balão, etiqueta da dm, @ |

## Pedidos do Cauã nesta rodada (12/11/2026)

- **Sem pessoas nas lâminas**, nem mãos: as cenas da folha e do celular foram refeitas com o objeto apoiado.
- **Equilíbrio entre foto e gráfico**: nem tudo vetor, nem 100% imagem. Capa e chamada são foto inteira; no miolo
  a foto divide a lâmina com cartão de cor, pílulas, retícula e o texto impresso no próprio objeto.

## Como foi feito

- Fotos geradas no Canva (Freepik, Figma, Higgsfield e ElevenLabs estavam sem crédito em 12/11), objeto já no
  cenário e nas cores da paleta em hex, superfícies em branco. O texto entra por cima em HTML, com `multiply`.
- Estrela em retícula atravessando cada corte, em cor e opacidade diferentes; grão por cima da faixa inteira.
- `node projeto/render.mjs` exporta; `--guia` desenha a margem de 90px; `--saida previa` exporta em outra pasta.
- `node projeto/scripts/conferir-palavra-curta.js projeto/carrossel.html` confere a regra da palavra curta.

## Pendências

- **Conferir o conteúdo com a Emi**: contrato, briefing, direção criativa e acompanhamento por etapa foram
  escritos a partir do design system; os itens do contrato (prazo, valor, rodadas de ajuste, entregas) e a
  tela de andamento precisam bater com o que ela realmente entrega.
- Fotos com 1136 × 1408 de origem: dá para ampliar se a Emi quiser mais nitidez no objeto.
