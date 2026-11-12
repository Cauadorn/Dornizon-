# EMS · "5 direções criativas pra marcas pet"

Carrossel 1080 × 1350 (7 lâminas) para o @itsemsdesign, no formato novo `PostCuradoria` do design system EMS.

**Referência:** post da @pivocriativo "5 direções criativas para marcas de beleza fora do padrão" (11/11/2026). O que veio de lá: a capa com número gigante + título + adesivo, as lâminas em grade 3 × 3 com um cartão escuro no meio (número, nome da direção, descrição "pra marcas que...") e a chamada final com pergunta. O que mudou: outro nicho (pet), identidade EMS no lugar da do Pivô, e o moodboard é **criado** (fotos geradas + marcas fictícias desenhadas), não curadoria de marcas reais.

**Por que pet:** mercado enorme de marca pequena (petshop, petisco, banho e tosa, acessório), conversa com o lado cpf da Emi (os gatos são a "diretoria criativa") e rende o trocadilho do adesivo, "fora da casinha".

## Lâminas

| # | Lâmina | Cartão (cor da série) | Marca fictícia no quadro selecionado | Fonte da direção |
|---|---|---|---|---|
| 1 | Capa: gato preto, "5 direções criativas pra marcas *pet*", adesivo "fora da casinha" | `violeta` | — | — |
| 2 | 01 pop de *gibi* | `violeta` | AU! petiscaria (balão de gibi) | Bagel Fat One |
| 3 | 02 clube de *grife* | `plum` | Maison Caramelo, pet couture | Bodoni Moda |
| 4 | 03 retrô *setentinha* | `wine` | pelo solto, banho & tosa | Shrikhand |
| 5 | 04 modo *atleta* | `creative-purple` | AU running club | Graduate |
| 6 | 05 ciência *fofa* | `ameixa` | miau.lab, fórmula nº 07 | Space Mono |
| 7 | Chamada: "quer uma marca pet que dá pra *reconhecer* até sem o nome?" + me chama na dm + selo | `plum` | — | — |

Legenda pronta em `legenda.md`.

**Onde está:** Figma editável https://www.figma.com/design/elmpB2QlAid4OFWruJL31H · Drive https://drive.google.com/drive/folders/1BihRkZXTpaY704VBm0gmCygNapc3i9SP · Design System EMS (grupo Posts e componente `PostCuradoria`) https://claude.ai/artifact/DNhPwJnJSH9f4gih32oQGa

## Arquivos

- `entrega/lamina-01..07.png` e `entrega/visao-geral.jpg`: arte final.
- `projeto/carrossel.html` + `estilo.css` + `direcoes.js`: a peça em código. Todo o conteúdo das direções (cores, quadros, posição de cada foto) fica em `direcoes.js`.
- `projeto/render.mjs`: `node render.mjs` exporta para `entrega/`; `node render.mjs --previa` exporta para `previa/` (fora do git).
- `projeto/img/`: fotos recortadas (fundo transparente) e o selo original.
- `projeto/figma/`: `exporta.mjs` (HTML → cena de camadas), `montador.js` (monta no Figma com `use_figma`), `sobe.sh` (envia as imagens para os nós). `figma/saida/` é gerada e fica fora do git.
- `projeto/fonts/`: Poppins e Instrument Serif (EMS) + as cinco fontes das direções (Google Fonts, licença OFL).

## Como as fotos foram feitas

- **Nano Banana Pro** (`gemini-3-pro-image` no ElevenLabs, porque o Magnific estava sem créditos), prompt em português, fundo liso **#E9E9E9** e "sem texto" em todos, como pede o DS. 11 prompts × 4 variações (gato da capa e, por direção, um prompt do bicho e um do produto). Fluxo no ElevenLabs: "EMS · 5 direções criativas pra marcas pet".
- Saída 1376 × 768 (16:9, 1K). Os dois gatos (capa e chamada) passaram por upscale 2x no Topaz (ElevenLabs) antes do recorte; o resto dos quadros usa a foto no tamanho original.
- **Recorte local** com `rembg`: ISNet (`isnet-general-use`, rápido) para a maioria e BiRefNet (`birefnet-general`) para o que tem branco perto do cinza do fundo (rótulos, tênis, suéter, tigela, gatos). O BiRefNet estoura a memória se processar várias imagens no mesmo processo: rodar uma imagem por processo.
- Montagem: cada recorte pousa na cor da direção, com sombra suave em `tinta` e, às vezes, um padrão (retícula de gibi, grade de laboratório, faixa de pista).

### Prompts usados

1. Capa/chamada: "Fotografia de estúdio de um gato preto de pelo curto e brilhante, sentado, olhando para cima e para o lado com uma expressão travessa e divertida, bochechas cheias, uma pata levantada perto do rosto, olhos amarelos grandes, bigodes nítidos, luz de estúdio suave vinda da esquerda, textura realista do pelo, leve grão de filme, enquadramento da cabeça até o peito com respiro nas bordas, fundo liso #E9E9E9, sem sombra projetada, sem texto, sem outros objetos."
2. 01 bicho: vira-lata caramelo sorrindo, bandana vermelha #F2542D com bolinhas, pulando, luz dura e alegre, fundo #E9E9E9.
3. 01 produto: osso amarelo #FFD23F, bola azul #2B59C3 e pote vermelho #F2542D de borracha fosca, três quartos, fundo #E9E9E9.
4. 02 bicho: whippet com suéter de tricô trançado creme #F3E9D7 e coleira caramelo com fivela dourada, campanha de luxo, fundo #E9E9E9.
5. 02 produto: bolsa de transporte de couro caramelo #C08A4F, coleira café #4A2E21 e pote de cerâmica creme, natureza-morta de grife, fundo #E9E9E9.
6. 03 bicho: lhasa apso caramelo com lenço de seda laranja #E2701E e mostarda #E9B03B, "estrela de cinema dos anos 70", grão de filme, fundo #E9E9E9.
7. 03 produto: pote de cerâmica mostarda com ondas laranja e marrom #6B3A1F + margarida de crochê, fundo #E9E9E9.
8. 04 bicho: border collie saltando para pegar frisbee azul royal #1F3FBF, peitoral verde-limão #C7F23E, fundo #E9E9E9.
9. 04 produto: peitoral azul royal com verde-limão, guia de corda trançada e tênis de corrida, sem logotipo, fundo #E9E9E9.
10. 05 bicho: gato tigrado cinza sentado de frente, coleira azul clínico #2F6BFF com pingente, luz branca de laboratório, fundo #E9E9E9.
11. 05 produto: ração em placa de petri, frascos âmbar com tampa azul clínico e conta-gotas, rótulos em branco, fundo #E9E9E9.
