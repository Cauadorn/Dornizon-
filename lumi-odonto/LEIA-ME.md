# Lumi Odonto: identidade visual (projeto conceitual)

Marca inventada para o carrossel de portfólio no formato "E se uma clínica odontológica me contratasse para criar seus posts?". A Lumi não existe e não tem relação com nenhuma clínica real.

Referências:
- **Formato:** post de 07/11/2026 da @rafaelalimadesigner_ (o pet shop "Mundo Pet").
- **Nível de acabamento:** Oliva Club, da @sand.design.studio.

## v2: por que mudou

A v1 (guardada em `_v1/`) tinha cara de template: fonte da moda, um arco genérico, bege com sálvia e pêssego, tudo liso e sem textura. A Oliva Club funciona porque:

1. **O logo é desenhado a partir da coisa real:** o O é uma azeitona, e o corte da folha passa por todas as letras.
2. **Tem matéria:** foto de perto, grão, papel.
3. **Tem mão:** setas e círculos desenhados, e um recado escrito à mão.
4. **A tipografia é gigante e brinca com o produto.**
5. **As cores contam história:** cada produto tem a sua.

A v2 leva essas cinco coisas para a odontologia.

## O lettering

"lumi" foi desenhado do zero, sem fonte pronta. A palavra é uma arcada:

- **o m é um molar:** duas cúspides em cima e três raízes embaixo, e as raízes de fora abrem um pouco;
- **o l e o i são dentes de uma raiz só:** toda perna termina afinando, como raiz;
- **o u não tem raiz:** o u é o sorriso;
- **o pingo do i é cor de gengiva.**

O m sozinho vira o símbolo e a foto de perfil.

Slogan: ***pode vir com medo.*** (a gente cuida.)

## Briefing fictício (texto do slide "A ideia")

**Sobre a marca**
- Nome: Lumi Odonto.
- Segmento: clínica odontológica (clínico geral, clareamento, alinhadores e implantes).
- Público: adultos de 25 a 45 anos que adiam o dentista por medo ou falta de tempo.

**O que estou procurando**
Quero uma marca que tire o medo do dentista. Calorosa, com humor, com cara de gente e não de hospital. Nada de clínica de estética nem de spa.

**Estilo**
- Feito à mão onde der, com textura e foto de verdade.
- Nada de dente 3D, nada de sorriso de banco de imagem.

**Cores**
Quero cores que lembrem a boca e o cuidado: verde de hortelã, um rosado e tons quentes. Não quero azul nem branco de consultório.

**Tipografia**
Um logo com personalidade própria, títulos que falem alto e algo escrito à mão.

## Sistema

| Cor | Hex | A história |
|---|---|---|
| Esmalte | `#F6F1E6` | dente de verdade não é branco puro |
| Hortelã | `#2E8C68` | gosto de boca limpa |
| Menta | `#CFE8D8` | o frescor, de fundo |
| Gengiva | `#EE7F73` | a parte que todo mundo esquece de cuidar |
| Café | `#3B2A22` | a cor que mancha o dente; aqui, só mancha o papel |

- **Contraste:**
  - Café sobre esmalte dá 12:1, e todo texto corrido vai em café.
  - Esmalte sobre hortelã dá 3,7:1, então só em título grande.
  - Gengiva nunca vai como texto sobre hortelã.
- **Fontes** (todas gratuitas, em `_fontes/`):
  - **Archivo Expanded ExtraBold:** títulos em caixa-alta, apertados, com ponto final ("ESCOVA. FIO. SORRIA.").
  - **Archivo:** texto.
  - **Caveat:** o recado à mão, como o dentista escreve no cartão.
- **Grafismos:**
  - Grão de papel em tudo.
  - Setas e círculos desenhados à mão.
  - Fita adesiva.
  - Listras de pasta de dente na apresentação das cores.
- **Aplicações:**
  - Cartão de retorno escrito à mão.
  - Adesivo "vim com medo. saí sorrindo".
  - Adesivo "hoje eu fui corajoso" (pra adulto também).
- **Voz:**
  - Fala como gente, explica antes de mexer e nunca dá bronca. Exemplos: "Vai dar uma pressãozinha, não dor. Se doer, levanta a mão." e "Sumiu faz tempo? Tudo bem. Volta que a gente recomeça."
  - Evitar "sorriso perfeito", "procedimentos de excelência" e "agende já!!!".

## Fotos a gerar

O conector do Magnific aqui está com 2 créditos e sem o ilimitado. Por isso, o melhor é rodar no Space, que tem o ilimitado da 4D. Os prompts estão em inglês porque os modelos respondem melhor assim.

1. **Capa do perfil.** *Two bamboo toothbrushes in a small clear glass on a bathroom windowsill, early morning sunlight with soft window shadows, mint green tiles, warm cream tones, shot on 35mm film, visible grain, shallow depth of field, editorial, no text.*
2. **Fundo de post.** *Extreme close-up of fresh mint leaves with tiny water droplets, soft natural light, deep green and cream tones, 35mm film grain, editorial still life, no text.*
3. **Dica do dia.** *Macro shot of mint toothpaste being squeezed onto a toothbrush, cream background, soft daylight from the left, film grain, playful editorial still life, no text.*
4. **Post de agendamento.** *A hand holding a blank cream paper card, sunlit small dental clinic reception out of focus behind, warm tones, 35mm film grain, candid, no text.* Depois, aplicar o verso do cartão de retorno por cima do cartão em branco.
5. **Post de boas-vindas.** *Candid photo of a Brazilian woman in her 30s laughing mid-conversation, sitting in a mint green dental chair, dentist seen from behind, warm window light, real skin texture, 35mm film grain, documentary style, no text.*
6. **Bastidor da clínica.** *Empty mint green dental chair in a small cozy clinic, morning sun through a window with plants, cream walls, warm film tones, grain, calm, no people, no text.*

Antes de usar, conferir:
- mãos com cinco dedos;
- pele sem cara de cera;
- uma sombra só, coerente com a janela;
- nenhum texto inventado na imagem.

## Arquivos

| Pasta | O que tem |
|---|---|
| `01-marca/svg/` | Lettering em vetor: `lumi-*` (só a palavra), `lumi-odonto-*` (com ODONTO), `lumi-molar-*` (símbolo) e `lumi-avatar.svg`. Cores: `hortela`, `esmalte` (para fundo escuro), `cafe` e `branco`. |
| `01-marca/png/` | Os mesmos arquivos em PNG transparente (4x), para Canva ou Figma. |
| `02-identidade/identidade.html` | As 8 pranchas (1080 x 1350). |
| `02-identidade/png/` | Capa, lettering, versões, cores, tipografia, aplicações, fotos e voz. |
| `_v1/` | A primeira versão, descartada. |
| `_fontes/`, `_ferramentas/` | Fontes (OFL) e os scripts que geram tudo. |

Para gerar tudo de novo:

```
pip install shapely fonttools
python3 lumi-odonto/_ferramentas/marca.py        # lettering SVG
node lumi-odonto/_ferramentas/logos_png.js       # logos PNG
node lumi-odonto/_ferramentas/render.js          # pranchas PNG
```

## Próximo passo: os 6 posts do grid

1. **Foto 1 (escovas no copo)** com o lettering em esmalte por cima.
2. **Tipo gigante**, como o "FINISHING / EVERYDAY" da Oliva: "CLAREAMENTO." com a foto 3 atrás.
3. **"Sumiu faz tempo? Tudo bem."** em café sobre menta, com recado à mão.
4. **Mito ou verdade** sobre fundo hortelã, com a foto 2.
5. **Foto 5 (paciente rindo):** "Pode vir com medo."
6. **Foto 4 (cartão de retorno):** "Seu retorno. Dia 12, às 9h30."
