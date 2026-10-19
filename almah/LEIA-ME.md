# Almah · peças da Coleção Gênesis

Tudo saiu do drive "coleçao genisi" (logo, fontes, rótulos, papelaria, fotos, vídeos e o brand book antigo).

| Pasta | O que tem |
|---|---|
| `brandbook/` | `Almah Brand Book 2026.pdf` (22 páginas, 1920 × 1080) e o `brandbook.html` que gera o PDF |
| `pinterest/` | `almah-pinterest-1080x1920@2x.jpg` e o HTML de origem |
| `behance/` | `subir-nesta-ordem/` (16 módulos; os 3 do logo em GIF animado), `capa/` (JPG e GIF), `motion-mp4/` (os 3 motions em MP4 1280 e 1920), `texto-behance.md` (título, descrição PT/EN, tags, ordem), `previa/` (página de prévia) e `projeto.html` + `projeto.js`, que geram tudo |
| `site/` | Site animado (a abertura é o logo acendendo: primeiro a lua, depois o fogo): `index.html` para hospedar (Vercel, Netlify, GitHub Pages), `artifact.html` é a mesma página no formato do Claude |
| `kit/` | Cores, sol raiado, estrelas, estampa e os vetores oficiais em JS, usados por todas as peças |
| `assets/` | Fotos, rótulos, papelaria, vetores e vídeos já otimizados |

## O que é novo em relação ao brand book antigo

- Tom de apoio **Noite** `#1C1726`, para fundos escuros onde a chama brilha.
- **Estampa** com símbolo, nuvem e estrelas em meia-queda.
- Área de proteção, tamanhos mínimos, usos incorretos, voz e tom, e modelos de post.
- Textos de personalidade de cada vela (Aura, Terra, Selene, Serena, Vênus). Revise se combinam com a Emi.

## Site

Para publicar fora do Claude, suba a pasta `site/` inteira (Vercel: arrastar a pasta no painel ou `vercel deploy site`).
Os vídeos vão em MP4 (H.264) e WebM; o filme está sem áudio porque a trilha original é uma música comercial.

Para regerar PDF e imagens: abrir o HTML no Chrome e imprimir em PDF (o brandbook já tem o tamanho de página configurado).
