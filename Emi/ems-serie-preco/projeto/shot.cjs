const { chromium } = require('playwright'); const path = require('node:path');
(async () => { const [html, out, w, h] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +w, height: +h } });
  const [arq, q] = html.split('?'); await p.goto('file://' + path.resolve(arq) + (q ? '?' + q : '')); await p.waitForLoadState('networkidle'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  await p.screenshot({ path: out, clip: { x: 0, y: 0, width: +w, height: +h } }); await b.close(); })();
