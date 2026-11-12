# EMS · "figurinhas raras" (carrossel de 7, 1080 × 1350)

Post da @itsemsdesign no pilar **bastidor e processo**: dez sites que entram no processo da Emi, dois por etapa (pesquisa, letra, cor, textura, entrega). Fecha com "qual figurinha tá *faltando* no meu álbum?", que puxa as indicações nos comentários.

**Status:** v2 em prévia (`previa/`), esperando o retorno da Emi. A v1 foi reprovada ("tá horrível… coisa marrom, fora da minha paleta"; "mesma textura, mesma diagramação, mesma receita de bolo"). Ela está em `v1-descartada/` só como registro do que não fazer.

## O que mudou da v1 para a v2

| v1 (reprovada) | v2 |
| --- | --- |
| Uma receita só em todas as lâminas: título no alto à esquerda, cartões, bilhete e @ | **Cada lâmina tem composição própria** (refs da Nicole Holz e da LilyConts), amarradas pelo cabeçalho e rodapé de álbum, pela paleta e pela dupla Instrument Serif + itálico |
| Uma textura só (grão e papel) e objetos gerados sem cor (lupa de madeira, tachinha vermelha) | **Uma matéria por lâmina** (ref. "mil texturas" da @escolacanvadesigner): linho, caderno pautado, meio-tom, papel, retalhos, pincelada, renda. **Objetos fotografados já na paleta** (hex no prompt) |
| Figurinhas com cara de interface (número, preço, URL, chips miúdos) | Os sites viram tipografia grande (o nome em serifa) e o "pra quê" vai em balão ou cartão |
| Técnica: cartão chapado + objeto 3D | **Técnica: colagem editorial com foto recortada.** O post anterior (ajustezinho v8) foi 3D sobre papel amassado; este não repete nem o 3D nem o papel amassado |

## Lâminas (v2)

1. **Capa** (linho violeta): "o pacotinho das / figurinhas / *raras*". O pacotinho fotografado fica entre as duas palavras, na frente de "figurinhas" e atrás de "raras". Pílula "10 sites que salvam meu processo e quase ninguém tem no álbum", sem spoiler.
2. **Pesquisa** (caderno pautado com margem rosa): "referência / sem *algoritmo*". A lupa de acrílico rosa **amplia de verdade** a palavra embaixo da lente. Os sites são cosmos.so e logosystem.co, em verbete zigue-zague.
3. **Letra** (ameixa com meio-tom): "achar a fonte / sem *chorar*", com o "Aa" gigante como folha de amostra e o alfabeto no pé. Os sites são fontsinuse.com e fontshare.com.
4. **Cor** (lavanda-2): "paleta que sai / do *papel*", com leque de cartelas usando a própria paleta da EMS (ameixa, violeta, rosa, manteiga). Os sites são realtimecolors.com e whocanuse.com.
5. **Textura** (marfim): à esquerda, uma tira de retalhos (linho, pincel, meio-tom, renda); à direita, "pra marca / não ficar / *lisa*". Os sites são fffuel.co e haikei.app.
6. **Entrega** (plum com pincelada tom sobre tom): "a hora de / *mostrar*", com a caixa de presente lilás e laço rosa. Os sites são shots.so e squoosh.app, em balões de fala.
7. **Chamada** (vinho com renda marfim no topo): "qual figurinha / tá *faltando* no / meu álbum?", o espaço nº 11 vazio, "me indica nos comentários o site que você não vive sem. eu testo e conto." e o selo.

**Conectividade (objetos que atravessam o corte):** coração 1|2, brilho 2|3, brilho 3|4, cartela lavanda 4|5, coração 5|6, brilho 6|7. Nenhum fio.

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
  - `node projeto/render.mjs --saida previa` exporta as lâminas e a visão geral.
  - `--guia` desenha a margem de 90px.
- **Imagens geradas no gerador do Figma** (`gpt-image-2.5-sunburst`), com as cores do objeto em hex no prompt e fundo #E9E9E9. Ficam em `projeto/geradas/`; os recortes (`projeto/recortar.py`, rembg BiRefNet) ficam em `projeto/recortes/`.
  - **Fotos de objeto:** pacotinho de laminado rosa com figurinhas lilás, violeta e marfim; lupa de acrílico rosa e lilás; caixa de presente lilás com laço rosa.
  - **Matérias:** linho violeta (`texturas/linho-violeta.png`), renda marfim (recorte) e pinceladas violeta (`texturas/pinceladas.png`, com o alfa tirado da cor).
  - `pacotinho-3d` e `lupa-3d` são as versões em render 3D. Ficaram de fora para não repetir a técnica do ajustezinho v8.
- No Figma da EMS ficaram os quadros das gerações 38:2 e 38:3 (pacotinho e lupa em foto) e 39:2 a 39:5 (linho, renda, presente, pinceladas).

## Legenda (rascunho, fechar depois da aprovação)

```
abri o pacotinho e saiu figurinha rara.

todo designer tem um álbum de sites salvos nos favoritos. esses são os dez que aparecem em quase todo projeto meu, separados por etapa, do jeito que eu uso de verdade: pesquisa, letra, cor, textura e a hora de mostrar pro cliente.

nenhum deles faz a marca por você. mas cada um tira um pedaço do trabalho chato do caminho, e sobra tempo pra parte que importa: pensar.

agora me ajuda a completar o álbum: qual site você usa e acha que pouca gente conhece?

↳ identidade visual, social media e site: dm aberta

#designgrafico #identidadevisual #branding #brandingdesign #ferramentasdedesign
```
