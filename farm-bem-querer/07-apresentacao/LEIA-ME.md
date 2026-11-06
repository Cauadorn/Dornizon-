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

## Texto sem viúvas
`_ferramentas/tipografia.py` cola as duas últimas palavras de cada bloco (e não deixa quebrar no hífen nem em "Bem-Querer"). O site, o PDF, o carrossel e o Behance passam por ela ao gerar.

## Carrossel do Instagram (com motions)
```
cd /tmp && python3 -I /home/user/Dornizon-/farm-bem-querer/_ferramentas/gerar_insta.py
cd /home/user/Dornizon-/farm-bem-querer/_ferramentas && node insta_render.js
node motion_camadas.js ../07-apresentacao/instagram/carrossel.html .sl ../07-apresentacao/instagram/_camadas 1 5 6 7 8
python3 -I motion_compor.py ../07-apresentacao/instagram/_camadas ../07-apresentacao/instagram/videos bem-querer 3
python3 -I insta_pacote.py        # instagram/carrossel-final/ + ZIP na ordem de postagem
```

## Post do Behance
```
cd /home/user/Dornizon-/farm-bem-querer/_ferramentas && node behance_telas.js
cd /tmp && python3 -I /home/user/Dornizon-/farm-bem-querer/_ferramentas/gerar_behance.py
cd /home/user/Dornizon-/farm-bem-querer/_ferramentas && node behance_render.js
node motion_camadas.js ../07-apresentacao/behance/behance.html .mod ../07-apresentacao/behance/_camadas 1 6 7 8 9 10
python3 -I motion_compor.py ../07-apresentacao/behance/_camadas ../07-apresentacao/behance/videos modulo 3 1280
python3 -I behance_pacote.py      # behance/pacote/ (capa, módulos em ordem, textos) + ZIP
```
Os vídeos juntam o módulo parado, o motion de `site/video/<uf>.mp4` recortado no arco e os chinelos por cima.
