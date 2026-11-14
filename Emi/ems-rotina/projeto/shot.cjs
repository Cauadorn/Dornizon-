const { chromium } = require('playwright'); const path = require('node:path');
(async () => { const [html, out, w, h] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +w, height: +h } });
  await p.goto('file://' + path.resolve(html)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  await p.screenshot({ path: out, clip: { x: 0, y: 0, width: +w, height: +h } }); await b.close(); })();
