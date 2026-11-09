// Prepara slides/módulos para virar vídeo: exporta o bloco inteiro (base), só os chinelos
// com fundo transparente (topo) e a posição de cada arco com ilustração (mapa.json).
// O motion_compor.py junta isso com os motions de site/video/<uf>.mp4.
// uso: node motion_camadas.js <arquivo.html> <seletor-dos-blocos> <pasta-saida> <n> [<n> ...]
//   ex.: node motion_camadas.js ../07-apresentacao/instagram/carrossel.html .sl ../07-apresentacao/instagram/_camadas 1 5 6 7 8
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const [arq, sel, saida, ...ns] = process.argv.slice(2);
const alvos = ns.map(Number);
(async () => {
  fs.mkdirSync(saida, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 1440 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(arq), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  const blocos = await p.$$(sel);
  const mapa = {};
  for (const n of alvos) {
    const el = blocos[n - 1];
    const nn = String(n).padStart(2, '0');
    await el.screenshot({ path: path.join(saida, `base-${nn}.png`) });
    mapa[nn] = await el.evaluate(bl => {
      const r0 = bl.getBoundingClientRect();
      return [...bl.querySelectorAll('.arco img, .quadro img')].map(img => {
        const r = img.getBoundingClientRect();
        const arco = img.closest('.arco, .quadro');
        return {
          uf: img.dataset.uf || decodeURIComponent(img.getAttribute('src')).split('/').pop().split('-')[0],
          x: r.left - r0.left, y: r.top - r0.top, w: r.width, h: r.height,
          pos: getComputedStyle(img).objectPosition, raio: parseFloat(getComputedStyle(arco).borderTopLeftRadius),
        };
      }).filter(a => a.w > 0);
    });
  }
  await p.addStyleTag({ content: `html,body,${sel}{background:transparent !important} ${sel} *{visibility:hidden !important} ${sel} .flutua{visibility:visible !important}` });
  for (const n of alvos) {
    const nn = String(n).padStart(2, '0');
    await blocos[n - 1].screenshot({ path: path.join(saida, `topo-${nn}.png`), omitBackground: true });
  }
  fs.writeFileSync(path.join(saida, 'mapa.json'), JSON.stringify(mapa, null, 1));
  console.log('camadas:', Object.keys(mapa).map(k => `${k}(${mapa[k].length} arcos)`).join(' '));
  await b.close();
})();
