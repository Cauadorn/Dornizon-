# EMS · "5 direções criativas pra marcas pet"

Carrossel 1080 × 1350 (7 lâminas) para o @itsemsdesign, no formato `PostCuradoria` do design system EMS.

**Referência:** post da @pivocriativo "5 direções criativas para marcas de beleza fora do padrão" (11/11/2026). Dele fica a ideia: 5 universos visuais para um nicho, cada um com cor, letra, foto e marca. A estrutura das lâminas de direção não vem de lá: a referência usa uma grade 3 × 3 com cartão escuro no meio.

**Por que pet:** mercado enorme de marca pequena (petshop, petisco, banho e tosa, acessório), conversa com o lado cpf da Emi (os gatos são a "diretoria criativa") e rende o trocadilho do adesivo, "fora da casinha".

## Versões

1. **v1:** fotos recortadas pousadas em cor chapada. Reprovada: "parece copia e cola".
2. **v2:** fotos inteiras na grade 3 × 3 da referência. "Amei, mas as imagens se repetem e queria menos cópia da ref."
3. **v3:** um layout diferente por direção, capa marfim com índice e chamada com paletas. Reprovada: a Emi quer uma estrutura só nas 5 lâminas, e "a capa anterior mil x melhor".
4. **v4:** as 5 direções numa estrutura própria da EMS, igual em todas (aprovada). Capa e chamada da v2. Reprovadas, ambas por diagramação:
   - **Capa**: o fundo e o gato ficam, mas a seleção do Figma ficou fora do rosto e o "diretoria criativa" era "cópia na cara".
   - **Chamada**: "muito xoxo, sem graça".
5. **v5 (atual):** a capa vira capa de revista e a chamada vira enquete. Diagramação pensada para este post, com referências de capa de revista e adesivo de enquete. A regra: "os posts precisam ser diferentes, senão eu postava a mesma coisa todo dia".

## Estrutura das lâminas de direção (igual nas 5)

```
┌──────────────────┬───────────┐
│                  │  marca    │  marca fictícia (SelectionBox + cursor "emi")
│   pet em         ├───────────┤
│   destaque       │  foto     │  quadrada
│   640 × 860      │  quadrada │
├─────────┬────────┼─────┬─────┤
│ cartão  │ foto   │paleta     │  cartão na cor da série: direção nn/05, título com itálico, texto
│ 520×472 │ alta   ├───────────┤
│         │260×472 │ letra (Aa)│
└─────────┴────────┴───────────┘
```

Respiro `ivory` de 18px, raio 22, sangria de 30px em quem encosta na borda. Coordenadas em `GRADE` (`carrossel.html`).

## Lâminas

| # | Lâmina | Cor do cartão | Fotos (destaque · quadrada · alta) | Marca fictícia · fonte |
|---|---|---|---|---|
| 1 | Capa de revista: nome "direções" atrás da cabeça do gato (recorte da mesma foto por cima), "criativas pra marcas *pet*" colado embaixo, chamada "5 universos pra sua marca pet sair do *óbvio*" (sem spoiler das direções), selo "nenhuma é patinha + osso", código de barras com o @ | fundo violeta da foto | capa-2 (+ recorte) | — |
| 2 | 01 pop de *gibi* | `violeta` | vira-lata pulando · corgi e petisco · osso, bola e pote | AU! petiscaria · Bagel Fat One |
| 3 | 02 clube de *grife* | `plum` | whippet de suéter · bolsa de couro · tricô com plaquinha MC | Maison Caramelo · Bodoni Moda |
| 4 | 03 retrô *setentinha* | `wine` | lhasa no tapete · pote e margarida · poodle no secador | pelo solto · Shrikhand |
| 5 | 04 modo *atleta* | `creative-purple` | border collie e frisbee · peitoral na pista · corredor e vizsla | AU running club · Graduate |
| 6 | 05 ciência *fofa* | `ameixa` | gato tigrado · frascos e ração · filhote no veterinário | miau.lab · Space Mono |
| 7 | Chamada em enquete: "qual delas tem a cara da sua *marca*?" centralizado, cartão de enquete à esquerda com o gato apertando uma opção com a pata (recorte por cima do cartão), "comenta o número da sua favorita" e dm à direita, assinatura embaixo | fundo ameixa da foto | cham-2 (+ recorte) | — |

Legenda pronta em `legenda.md`.

**Onde está:** Figma editável https://www.figma.com/design/elmpB2QlAid4OFWruJL31H · Drive https://drive.google.com/drive/folders/1BihRkZXTpaY704VBm0gmCygNapc3i9SP · Design System EMS (grupo Posts e componente `PostCuradoria`) https://claude.ai/artifact/DNhPwJnJSH9f4gih32oQGa

## Arquivos

- `entrega/lamina-01..07.png` e `entrega/visao-geral.jpg`: arte final.
- `projeto/carrossel.html` + `estilo.css` + `direcoes.js`: a peça em código. `direcoes.js` concentra o conteúdo de cada direção: fotos, marca, paleta e letra.
- `projeto/render.mjs`: `node render.mjs` exporta para `entrega/`; `node render.mjs --previa` exporta para `previa/` (fora do git).
- `projeto/img/`: só as fotos usadas, os dois recortes de gato (`*-gato.png`, mesmo tamanho da foto, para a camada da frente) e o selo original.
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
