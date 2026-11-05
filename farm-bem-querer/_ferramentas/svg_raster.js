const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [,, inp, w, out] = process.argv;
  let svg = fs.readFileSync(inp, 'utf8');
  const vb = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/); const W = +w, H = Math.round(W * vb[2] / vb[1]);
  svg = svg.replace(/width="[\d.]+" height="[\d.]+"/, `width="${W}" height="${H}"`);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await p.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
  await p.screenshot({ path: out, omitBackground: true, clip: { x: 0, y: 0, width: W, height: H } }); await b.close();
})();
