import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import path from 'node:path';
import fs from 'node:fs';

const dir = path.dirname(new URL(import.meta.url).pathname);
const out = path.join(dir, 'out');
fs.mkdirSync(out, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 2.5, viewport: { width: 700, height: 900 } });
await page.goto('file://' + path.join(dir, 'grimorio.html'), { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(300);

// report overflow per page
const overflow = await page.evaluate(() => {
  return [...document.querySelectorAll('.page')].map(p => {
    const inner = p.querySelector('.inner');
    const pr = p.getBoundingClientRect();
    let maxBottom = 0;
    inner.querySelectorAll('*').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.height > 0) maxBottom = Math.max(maxBottom, r.bottom - pr.top);
    });
    return { id: p.id, pageH: Math.round(pr.height), contentBottom: Math.round(maxBottom), over: maxBottom > pr.height - 38 };
  });
});
console.table(overflow);

const pages = await page.$$('.page');
let i = 0;
for (const el of pages) {
  i++;
  await el.screenshot({ path: path.join(out, `pagina-${String(i).padStart(2, '0')}.png`) });
}
await page.pdf({ path: path.join(out, 'grimorio-exu-ngombo.pdf'), preferCSSPageSize: true, printBackground: true });
await browser.close();
console.log('done', i, 'pages');
