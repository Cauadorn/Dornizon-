# EMS · "figurinhas raras" (carrossel de 7, 1080 × 1350)

Post da @itsemsdesign no pilar **bastidor e processo**: dez sites que entram no processo da Emi, dois por etapa (pesquisa, letra, cor, textura, entrega). Fecha com "qual figurinha tá *faltando* no meu álbum?", que puxa as indicações nos comentários.

**Status:** v4 aprovada em 12/11/2026. Lâminas finais em `entrega/` (7 × 1080 × 1350 + visão geral + legenda) e no Drive: [EMS · @itsemsdesign / 2026-11 · figurinhas raras](https://drive.google.com/drive/folders/1mXRfDny9CFU0yEo95pAPOt0JccynZHJV). As versões reprovadas (v1 a v3 e a página 4 com post-its) estão em `v1-descartada/`; as prévias de trabalho em `previa-v4/`.

## v4: uma referência de diagramação por página

O que destravou a v4: **cada página segue de perto a diagramação de uma referência que a Emi mandou** (sem as fotos de pessoas), numa família de cor só (violeta + marfim, rosa e manteiga de acento), com textura visível e as estrelas em retícula da marca em opacidades diferentes.

| Página | Referência (diagramação) | O que tem |
| --- | --- | --- |
| 1 · capa | Pinterest ref 6 (cartão de Notas sobre fundo rico) | Notas com "FIGURINHAS / RARAS" em Anton, *do meu pacotinho*, pacotinho de papel impresso passando de leve sobre as palavras, @ fora do cartão, mouse clicando dentro das notas |
| 2 · pesquisa | Pinterest ref 8 (agenda) | folha de agenda, "pra achar referência sem depender do *algoritmo*", lupa de acrílico ampliando a palavra de verdade (na cor da folha), cosmos.so e logosystem.co em blocos |
| 3 · letra | Pinterest ref 7 (papel com clipe sobre fundo escuro) | folha com "ACHAR A FONTE *sem chorar*", fontsinuse.com e fontshare.com, letras gigantes no fundo, ✨ 🥲 ⭐ |
| 4 · cor | Pinterest refs 4 e 5 | "nem toda *paleta bonita* funciona" gigante, conta-gotas pingando na palavra, barrinha de interface com os hex, bilhetes com clipe de realtimecolors.com e whocanuse.com |
| 5 · textura | Nicole Holz, ref 3 lâmina 5 | violeta-2 com linho, "pra marca não ficar *lisa.*" (só a "lisa" com textura de carimbo gasto), pincel de acrílico pintando a pincelada de verdade, fffuel.co e haikei.app, bloco miúdo de nomes de textura |
| 6 · entrega | LilyConts, ref 2 lâmina 9 | "ANTES / DE MANDAR / pro *cliente:*", cartão com shots.so e squoosh.app e o desenho do que cada um faz (celular com a capa deste carrossel; capa.png 2,8 MB → capa.webp 164 KB, números reais) |
| 7 · chamada | página de álbum "PROCURA-SE" (Pinterest) | cartaz de procurado colado no violeta da capa: "PROCURA-SE a figurinha *nº 11*", espaço vazio no lugar da foto, ficha (visto por último, características, recompensa: eu testo e conto aqui), "viu ela? me indica nos comentários ↓" |

**Ligações entre as páginas (metade de cada lado do corte):** estrela em retícula rosa 1|2; "&" em contorno 2|3; "g" cheio na 3 e em contorno na 4, mais estrela rosa 3|4; estrela em retícula que troca de cor no corte 4|5 (violeta no marfim, marfim no violeta); seta desenhada 5|6; "?" gigante 6|7. Por cima de tudo, uma camada contínua de relevo de papel e grão de impressão.

**Variantes guardadas da página 7:** `?p7=atual` (álbum escuro com seleção do Figma, reprovada) e `?p7=b` (álbum quase completo, as 10 figurinhas). Renderizar com `node projeto/render.mjs --q p7=b`.

### O que a Emi reprovou no caminho (e virou regra)

- Fundo de cada página numa cor diferente ("eu tô parecendo uma palhaça"): uma família de cor só.
- Foto gerada de cena ou de pessoa: foto real, só dela.
- Mesma textura e mesma receita em todas: cada página com a sua matéria e a sua referência.
- Título em bloco e diagramação básica: seguir a referência de perto.
- Emoji em todas as páginas: só onde agrega.
- Muito objeto 3D: lupa, conta-gotas e pincel bastam; entrega e chamada são flat.
- Pacotinho quadrado de laminado rosa ("parece camisinha"): envelope de papel impresso, vertical.
- Pincelada atravessando para a página vizinha: a ponte 4|5 virou estrela.
- Página que não se entende (checklist com itens genéricos): só os dois sites, cada um com o desenho do que faz.
- Conteúdo fora do centro: conferir a centralização do conteúdo dentro do cartão e do conjunto na página.

## Sites (conferidos em 12/11/2026)

| Etapa | Site | O que faz | Preço |
| --- | --- | --- | --- |
| pesquisa | cosmos.so | moodboard sem anúncio; busca por cor e por semelhança | grátis, Premium US$ 8/mês |
| pesquisa | logosystem.co | biblioteca de logos reais, filtrada por estilo, forma e cor | grátis |
| letra | fontsinuse.com | fontes aplicadas no mundo real, com crédito e contexto | grátis |
| letra | fontshare.com | fontes da Indian Type Foundry liberadas para uso comercial | grátis (EULA da ITF) |
| cor | realtimecolors.com | testa paleta e fontes num site de exemplo e exporta o CSS | grátis |
| cor | whocanuse.com | mostra como o contraste aparece para daltonismo e baixa visão | grátis, open source |
| textura | fffuel.co | geradores de SVG (grão, ruído, textura), uso comercial liberado | grátis |
| textura | haikei.app | fundos em SVG (ondas, blobs, camadas) | grátis |
| entrega | shots.so | põe print de site ou post em mockup de celular e notebook | freemium |
| entrega | squoosh.app | comprime e converte imagem no navegador | grátis, open source |

Ficaram de fora: Vectorizer.ai (só baixa pagando), Huemint (termos de uso comercial pouco claros), Savee (limites do plano grátis não confirmados) e Godly (agora se chama Recent).

## Referências e o que saiu de cada uma (`referencias/`)

- `post-enviado/`: @bybelladesignn, "designers legais não guardam segredos". Dela veio **só o intuito**: indicar ferramentas e pedir as favoritas de quem lê. Nenhuma ferramenta, frase ou diagramação dela entrou.
- `enviadas-emi/ref1` e `ref3` (Nicole Holz, psicóloga):
  - cada lâmina com composição e matéria diferentes (jeans, linho, renda, pincelada, água, listrado, papel com clipe);
  - serifa condensada misturada com itálico;
  - objeto com motivo (lírio, andorinha, barquinho).
- `enviadas-emi/ref2` (LilyConts):
  - fundo alternando claro, magenta e preto;
  - palavra gigante com objeto fotografado na cor da marca (calculadora rosa, cofrinho);
  - cabeçalho e rodapé de revista;
  - pílula com rabinho de balão.
- `escolacanvadesigner-texturas.jpg`: o catálogo de matérias (grão, revista, papel, linho, meio-tom, renda, pautado).
- `pinterest/`: buscas com `pinterest.mjs` (editorial + objeto, adesivos Y2K rosa e lilás, colagem @danibloom.design) e as primeiras buscas de álbum, figurinha e pacotinho.

## Produção

- `projeto/carrossel.html` + `estilo.css` + `textos.js`: a faixa inteira (7560 × 1350).
  - `node projeto/render.mjs` exporta as 7 lâminas e a visão geral em `entrega/`; `--n 4 --saida previa-v4` exporta só as primeiras.
  - `--guia` desenha a margem de 90px.
- **Imagens geradas no gerador do Figma** (`gpt-image-2.5-sunburst`), com as cores do objeto em hex no prompt e fundo #E9E9E9. Ficam em `projeto/geradas/`; os recortes (`projeto/recortar.py`, rembg BiRefNet, uma imagem por vez) em `projeto/recortes/`.
  - **Usados na v4:** `pacotinho` (envelope de papel impresso, vertical), `lupa` (acrílico rosa e lilás), `conta-gotas` (acrílico violeta), `pincel-pintando` (pincel de acrílico lilás já no fim da pincelada de tinta #3A1A8F; recorte = rembg no pincel + chave de cor contra o #E9E9E9 na tinta, sombra cinza convertida em sombra escura transparente, tinta escurecida para casar com as outras pinceladas).
  - **Matérias:** linho violeta (`texturas/linho-violeta.png`, página 5), pinceladas separadas de `texturas/pinceladas.png` em `pincelada-1..3.png`, tingidas com o mesmo filtro (`PINC`).
  - **Feitas no código:** estrela em retícula (`estrelaReticula`), relevo e fibra de papel (feTurbulence + feDiffuseLighting), carimbo gasto da "lisa" (máscara de ruído), relevo seco dos espaços de álbum (variante `atual` da 7), celular e etiqueta de arquivo (página 6), cartaz (página 7).
  - `recortes/capa-mini.jpg` é a página 1 reduzida, usada dentro do celular da página 6: refazer se a capa mudar.
  - Fora da v4: `presente`, `renda`, `leque`, `figurinha-lupa`, `pincel` (sem pintar), `pacotinho-3d`, `lupa-3d` e as versões antigas do pacotinho.
- **Duas armadilhas do SVG no HTML:** textura em `url("data:…")` não pode ir direto no atributo `style` (as aspas fecham o atributo; passar por variável CSS), e filtro de luz/ruído precisa de `color-interpolation-filters='sRGB'`, senão o cinza médio vira claro e a textura lava a cor.
- No Figma da EMS ficaram os quadros das gerações (38:x, 39:x, 48:2 pincel, 49:2 e 49:3 pincel pintando).

## Legenda (final, também em `entrega/legenda.txt` e no Drive)

```
o pacotinho das figurinhas raras chegou, e é tudo site que salva o meu processo.

todo designer tem um álbum de favoritos. esses são os dez que aparecem em quase todo projeto meu, separados por etapa, do jeito que eu uso de verdade:

pesquisa: cosmos.so e logosystem.co
letra: fontsinuse.com e fontshare.com
cor: realtimecolors.com e whocanuse.com
textura: fffuel.co e haikei.app
entrega: shots.so e squoosh.app

nenhum deles faz a marca por você. mas cada um tira um pedaço do trabalho chato do caminho, e sobra tempo pra parte que importa: pensar.

procura-se a figurinha nº 11: qual site você usa e acha que quase ninguém conhece?

↳ identidade visual, social media e site: dm aberta

#designgrafico #identidadevisual #branding #brandingdesign #ferramentasdedesign
```
