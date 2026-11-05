# Site Bem-Querer

No ar: https://cauadorn.github.io/Dornizon-/

## Páginas
- `index.html` início: abertura em arco, manifesto, roda dos 14 pares e índice do site
- `projeto.html`, `pesquisa.html`, `colecao.html`, `processo.html`, `campanha.html`, `identidade.html`, `creditos.html`
- `estados/<nome-do-estado>.html` uma página por estado, dentro da Coleção (encontre o coração, o par, caderno de campo, rua, lugar, o que a gente evitou)

## Como gerar e publicar
```
cd /tmp && python3 -I /home/user/Dornizon-/farm-bem-querer/_ferramentas/gerar_site_v5.py
bash /home/user/Dornizon-/farm-bem-querer/_ferramentas/publicar_pages.sh "mensagem"
```
- Estilo e comportamento comuns: `_ferramentas/v5/bq.css` e `_ferramentas/v5/bq.js` (copiados para `site/css` e `site/js`).
- GSAP, ScrollTrigger e Lenis ficam em `site/js` (o site não depende de CDN além do Google Fonts).
- Os textos vêm de `gerar_site.py` (dados), `textos_v2.py` e dos cadernos; as caixas do coração de `mapa_coracoes_caixas.json`.
- `gerar_site.py`, `gerar_v4.py` e os modelos antigos ficam só como histórico: não rodar, eles sobrescrevem o `index.html`.
