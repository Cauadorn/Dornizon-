# Almah · peças da Coleção Gênesis

Tudo saiu do drive "coleçao genisi" (logo, fontes, rótulos, papelaria, fotos, vídeos e o brand book antigo).

| Pasta | O que tem |
|---|---|
| `brandbook/` | `Almah Brand Book 2026.pdf` (22 páginas, 1920 × 1080) e o `brandbook.html` que gera o PDF |
| `pinterest/` | `almah-pinterest-1080x1920@2x.jpg` (o board), `pins/` com cinco pins 2:3 em 2000 × 3000 (cinco velas, seu pedido chegou, abrir uma Almah, a lua guarda a chama, cuidados) e os HTML de origem (`pinterest.html`, `pins.html`) |
| `instagram/` | Os mockups prontos para postar: 4:5 (1080 × 1350), o kit em 1:1 e a coleção em paisagem; as velas 05 a 09 funcionam como carrossel |
| `behance/` | `subir-nesta-ordem/` (23 módulos guiados pela fotografia; 2 motions em GIF: a chama desenhada sobre a foto da lua e o logo acendendo), `capa/` (JPG e GIF), `motion-mp4/` (os 2 motions em MP4 1280), `texto-behance.md` (título, descrição PT/EN, tags, ordem, nota sobre as imagens de IA), `previa/` (página de prévia), `projeto.html` (gera os módulos desenhados) e `motion/` (as duas animações) |
| `site/` | Site animado. Abre com a foto da lua e a chama desenhada à mão acendendo sobre o pavio (toque para acender de novo); depois o manifesto, o símbolo do traço à luz (esboço, construção, projeção), a coleção na prateleira e nas cartas, a caixa se abrindo em cinco tempos, o gerador de rótulo, a marca e o filme. `index.html` para hospedar (Vercel, Netlify, GitHub Pages), `artifact.html` é a mesma página no formato do Claude |
| `kit/` | Cores, sol raiado, estrelas, estampa e os vetores oficiais em JS, usados por todas as peças |
| `assets/` | Fotos, rótulos, papelaria, vetores e vídeos já otimizados; `img/mock-*` são os mockups fotográficos (caixa, envelope, cuidados, coleção, esboço, entrega, kit e `mock-vela-*`, as cinco velas com o rótulo) |

## O que é novo em relação ao brand book antigo

- Tom de apoio **Noite** `#1C1726`, para fundos escuros onde a chama brilha.
- **Estampa** com símbolo, nuvem e estrelas em meia-queda.
- Área de proteção, tamanhos mínimos, usos incorretos, voz e tom, e modelos de post.
- Textos de personalidade de cada vela (Aura, Terra, Selene, Serena, Vênus). Revise se combinam com a Emi.

## Site

Para publicar fora do Claude, suba a pasta `site/` inteira (Vercel: arrastar a pasta no painel ou `vercel deploy site`).
Os vídeos vão em MP4 (H.264) e WebM; o filme está sem áudio porque a trilha original é uma música comercial.

Para regerar PDF e imagens: abrir o HTML no Chrome e imprimir em PDF (o brandbook já tem o tamanho de página configurado).
