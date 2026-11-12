# EMS · carrossel "o que chega antes do logo?" (6 × 1080 × 1350)

Carrossel da @itsemsdesign no pilar **bastidor e processo**. Ponto de partida: post da @daimaass.design
("o que você recebe ao se tornar minha cliente?", 12/11/2026), em `referencias/post-daimaass/`.
Dela ficou a ideia (mostrar o que o cliente recebe além da arte pronta) e a linguagem: foto de flor
desfocada no fundo, cartão de cor chapada e pílulas por cima. Texto, conceito e objetos são da EMS.

**Status:** v2, esperando aprovação. Finais em `entrega/` (`lamina-01..06.png` + `visao-geral.jpg`), legenda em `legenda.md`.

## Conceito

"Chega" vira correspondência: a caixa de correio na capa, e cada lâmina é uma coisa que chega antes da marca.
Tudo no eixo central, fundo na cor da marca com matéria, objeto recortado em duotone da paleta e letra gigante
composta com o objeto (o "logo?" entra na caixa de correio; a "marca." sai do envelope).

| Lâmina | Fundo | Título | Peça principal |
| --- | --- | --- | --- |
| 1 · capa | tinta | o que chega antes do *logo?* | caixa de correio em duotone |
| 2 · contrato | violeta | combinado não sai *caro.* | só papel e letra: a folha do contrato com o selo |
| 3 · briefing | ameixa | perguntas que ninguém te *fez.* | caderno em duotone, perguntas sentadas na pauta |
| 4 · direção criativa | violeta-2 | o rumo antes do *desenho.* | varal com as amostras (cor, letra, matéria, voz) |
| 5 · andamento | plum | sem sumiço, sem *suspense.* | celular em duotone com as etapas na tela |
| 6 · chamada | violeta | e só então chega a *marca.* | envelope em duotone manteiga, pergunta e etiqueta |

## O que o Cauã reprovou na v1 (12/11/2026)

- **Pessoas nas lâminas**: nem mão segurando objeto.
- **100% imagem**: foto crua de fundo em toda lâmina. "Não necessariamente precisa ser utilizada imagem em tudo."
- **Falta de centralização** e cara de banco de imagem: foto fora da paleta (banco verde, folhas), cartões jogados
  por cima, texto miúdo, cada lâmina num eixo.
- **v2, primeira tentativa** ("a carta parecendo que foi queimada, tudo mal recortado"): os objetos vinham de fotos
  com cenário, com ramos na frente do envelope apagados na mão. Objeto de montagem se gera isolado em fundo liso,
  sem nada na frente, e nunca se remenda.
- **Depois do recorte limpo**: aprovadas as lâminas 1, 2, 4 e 5; reprovadas a 3 (caderno) e a 6 (envelope), sem motivo dito.
  Duas alternativas de cada em `entrega/alternativas/` (`projeto/alternativas.html`), esperando a escolha.
- **Brilhos espalhados** (o ícone de quatro pontas) saíram: "tá parecendo do Gemini". Não usar como enfeite solto.
- A régua é a qualidade dos stories "toda marca tem fase": **não copiar, chegar no mesmo nível**.

## Como foi feito

- Objetos gerados no Canva (Freepik, Figma, Higgsfield e ElevenLabs sem crédito em 12/11), **isolados em fundo
  liso #E9E9E9**, em `projeto/iso/`. As fotos de cena de `projeto/fotos/` são da v1 e não entram mais.
- Recorte com rembg (`birefnet-general`, uma foto por processo, senão falta memória) em `projeto/obj/c*.png`;
  o caderno é recortado pela cor do fundo (o rembg comia a página da direita). `python3 projeto/tratar.py` faz o
  duotone da paleta e reduz para o tamanho de uso (`o*.png`).
- Acabamento de papel e grão por cima da faixa inteira; uma matéria por lâmina; estrela em retícula em cada corte.
- `node projeto/render.mjs` exporta; `--guia` desenha a margem de 90px e o eixo central; `--saida previa` muda a pasta.
- `node projeto/scripts/conferir-palavra-curta.js projeto/carrossel.html` confere a regra da palavra curta.

## Pendências

- **Conferir o conteúdo com a Emi**: contrato, briefing, direção criativa e acompanhamento por etapa foram escritos
  a partir do design system; os quatro itens do contrato e as etapas da tela precisam bater com o que ela entrega.
