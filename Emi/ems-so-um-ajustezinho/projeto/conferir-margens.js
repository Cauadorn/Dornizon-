// Confere a margem de 90px da EMS: mede a tinta de cada texto e assinatura até as bordas de cada lâmina.
// uso: node conferir-margens.js carrossel-v8.html
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 6480, height: 1350 } });
  await p.goto('file://' + path.resolve(process.argv[2])); await p.waitForFunction(() => window.READY === true);
  const res = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('.lamina').forEach(lam => {
      const L = lam.getBoundingClientRect();
      const check = (r, nome) => {
        if (!r || r.width < 1) return;
        const d = { esq: r.left - L.left, dir: L.right - r.right, cima: r.top - L.top, baixo: L.bottom - r.bottom };
        const ruim = Object.entries(d).filter(([k, v]) => v < 89.5).map(([k, v]) => `${k}=${v.toFixed(0)}`);
        if (ruim.length) out.push(`${lam.id} ${nome}: ${ruim.join(' ')}`);
      };
      const w = document.createTreeWalker(lam, NodeFilter.SHOW_TEXT);
      while (w.nextNode()) {
        const t = w.currentNode; if (!t.textContent.trim()) continue;
        const rg = document.createRange(); rg.selectNodeContents(t);
        for (const r of rg.getClientRects()) check(r, JSON.stringify(t.textContent.trim().slice(0, 28)));
      }
      lam.querySelectorAll('.handle, .selo, .emi svg, .aviso, .cta, .bilhete, .etapa, .etiqueta').forEach(e => check(e.getBoundingClientRect(), e.className.baseVal !== undefined ? 'cursor' : e.className));
    });
    return out;
  });
  console.log(res.length ? res.join('\n') : 'tudo dentro dos 90px');
  await b.close();
})();
