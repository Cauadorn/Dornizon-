// Rasteriza um SVG em PNG transparente.  uso: node svg2png.cjs <entrada.svg> <saida.png> <largura> [cor]
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [ent, sai, larg, cor] = process.argv.slice(2);
  let svg = fs.readFileSync(ent, 'utf8');
  if (cor) svg = svg.replace(/fill="#[0-9A-Fa-f]{6}"><path/, `fill="${cor}"><path`).replace(/<g fill="#[0-9A-Fa-f]{6}">/, `<g fill="${cor}">`);
  const vb = svg.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
  const W = +larg, H = Math.round(W * vb[3] / vb[2]);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: W, height: H } });
  await p.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg ', `<svg width="${W}" height="${H}" `)}</body></html>`);
  await p.screenshot({ path: sai, omitBackground: true });
  await b.close(); console.log('ok', sai, W, H);
})();
