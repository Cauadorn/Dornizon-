# EMS · "5 direções criativas pra marcas pet"

Carrossel 1080 × 1350 (7 lâminas) para o @itsemsdesign, no formato `PostCuradoria` do design system EMS.

**Referência:** post da @pivocriativo "5 direções criativas para marcas de beleza fora do padrão" (11/11/2026). Dele fica só a **ideia**: 5 universos visuais para um nicho, cada um com cor, letra, foto e marca. A **estrutura** não se copia (v3, 12/11). A referência repete a mesma grade 3 × 3 com cartão no meio em todas as lâminas, e a capa tem "5" gigante + pílula. Aqui cada lâmina tem um layout próprio, e capa e chamada são outras.

**Por que pet:** mercado enorme de marca pequena (petshop, petisco, banho e tosa, acessório), conversa com o lado cpf da Emi e rende o gancho da capa: "marca pet sem *patinha*".

## Versões

1. **v1:** fotos recortadas pousadas em cor chapada. Reprovada: "os recortes não se encaixam, parece copia e cola".
2. **v2:** fotos inteiras na cena. A Emi amou, mas apontou dois problemas: "as imagens se repetem" (5 variações da mesma cena por lâmina, e uma foto literalmente duas vezes) e "queria que fosse menos cópia da ref" (grade 3 × 3 idêntica em todas, capa e chamada iguais às da referência).
3. **v3 (atual):** mesmo vocabulário visual da v2, com estas mudanças:
   - Um layout por direção.
   - Cada foto aparece uma vez só no carrossel.
   - Uma cena nova por direção, gerada para dar variedade.
   - Capa com índice.
   - Chamada que pede o número nos comentários.

## Lâminas

| # | Lâmina | Layout | Cor do cartão | Fotos | Marca fictícia · fonte |
|---|---|---|---|---|---|
| 1 | Capa: "marca pet sem *patinha*" | título em serifa no topo, índice das 5 direções à esquerda, gato preto em quadro à direita | marfim | capa-2 | — |
| 2 | 01 pop de *gibi* | **tirinha**: 3 faixas com quadros de larguras diferentes | `violeta` | vira-lata pulando, osso e pote, corgi e petisco | AU! petiscaria · Bagel Fat One |
| 3 | 02 clube de *grife* | **revista**: uma foto gigante, coluna lateral e faixa de baixo | `plum` | whippet de suéter, bolsa de couro, tricô com plaquinha MC | Maison Caramelo · Bodoni Moda |
| 4 | 03 retrô *setentinha* | **arcos**: quadros com topo em arco, anos 70 | `wine` | lhasa no tapete, pote e margarida, poodle no secador | pelo solto · Shrikhand |
| 5 | 04 modo *atleta* | **ação**: foto de ponta a ponta com o patch do clube por cima; paleta em chips no cartão | `creative-purple` | border collie e frisbee, peitoral na pista, corredor e vizsla | AU running club · Graduate |
| 6 | 05 ciência *fofa* | **ficha**: cartão em faixa no topo, foto em cápsula, grade de prontuário | `ameixa` | gato tigrado, frascos e ração, filhote no veterinário | miau.lab · Space Mono |
| 7 | Chamada: "qual das 5 é a *sua*?" | as 5 paletas em fichas numeradas, "comenta o número", dm, selo | `plum` | — | — |

Legenda pronta em `legenda.md`.

**Onde está:** Figma editável https://www.figma.com/design/elmpB2QlAid4OFWruJL31H · Drive https://drive.google.com/drive/folders/1BihRkZXTpaY704VBm0gmCygNapc3i9SP · Design System EMS (grupo Posts e componente `PostCuradoria`) https://claude.ai/artifact/DNhPwJnJSH9f4gih32oQGa

## Arquivos

- `entrega/lamina-01..07.png` e `entrega/visao-geral.jpg`: arte final.
- `projeto/carrossel.html` + `estilo.css` + `direcoes.js`: a peça em código. `direcoes.js` concentra o conteúdo e o layout de cada lâmina: retângulos `[x, y, w, h]`, forma (`arco`, `capsula`), patch flutuante e seleção.
- `projeto/render.mjs`: `node render.mjs` exporta para `entrega/`; `node render.mjs --previa` exporta para `previa/` (fora do git).
- `projeto/img/`: só as 16 fotos usadas e o selo original.
- `projeto/figma/`: `exporta.mjs` (HTML → cena de camadas), `montador.js` (monta no Figma com `use_figma`), `sobe.sh` (envia as imagens para os nós). `figma/saida/` é gerada e fica fora do git.
- `projeto/fonts/`: Poppins e Instrument Serif (EMS) + as cinco fontes das direções (Google Fonts, licença OFL).

## Como as fotos foram feitas

- **Fotos da v2** (pet e produto de cada direção, capa): Nano Banana Pro (`gemini-3-pro-image` no ElevenLabs), 3:4, 2K. Cena inteira no cenário e na cor da direção, nada de recorte. Prompt em português, "sem texto".
- **Cenas novas da v3** (`d1extra` a `d5extra`): gerador de imagem do Figma (`gemini-3.1-flash-image`). A ElevenLabs ficou sem crédito, e o Freepik recusa geração pelo conector ("limite de uso"), mesmo com plano ilimitado no site. Os 5 prompts estão no Space "EMS · carrossel pet v3 · fotos novas" do Freepik, prontos para rodar no Nano Banana Pro 2K pelo site, se quiser trocar por versões em 2K.
  - `d1extra` (16:9): corgi pulando para pegar um biscoito em formato de osso, fundo vermelho-tomate com retícula amarela, flash duro.
  - `d2extra` (9:16): suéter creme de tricô trançado dobrado em prateleira de nogueira, plaquinha de latão "MC", guia de couro conhaque, parede verde-garrafa.
  - `d3extra` (3:4): poodle branco sob secador de capacete cromado, salão de banho e tosa anos 70, azulejos laranja e mostarda, grão de filme.
  - `d4extra` (9:16): pernas de corredor (short azul royal, tênis verde-limão) e vizsla de peitoral azul na rua ao nascer do sol.
  - `d5extra` (9:16): filhote de golden na mesa de exame, mãos de luva menta com estetoscópio, parede menta.
- Regra para não repetir: variações da mesma cena (mesmo bicho, mesmo cenário) contam como a mesma foto. Por direção, uma foto de cada cena.
