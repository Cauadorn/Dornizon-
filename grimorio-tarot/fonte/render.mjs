import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import path from 'node:path';
import fs from 'node:fs';
const dir = path.dirname(new URL(import.meta.url).pathname);
const modo = process.argv[2] || 'leitura';           // leitura | construcao
const so = process.argv[3] ? process.argv[3].split(',').map(Number) : null;   // ex.: 6,7 (só estas páginas)
const out = path.join(dir, 'out', modo);
if (!so) fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 2.5, viewport: { width: 700, height: 900 } });
await page.goto('file://' + path.join(dir, 'grimorio.html') + (modo === 'construcao' ? '?modo=construcao' : ''), { waitUntil: 'load' });
await page.waitForFunction(() => document.body.dataset.pronto === '1');
await page.waitForTimeout(300);
const info = await page.evaluate(() => [...document.querySelectorAll('.page')].map((p, i) => {
  const inner = p.querySelector('.inner'); const ir = inner.getBoundingClientRect();
  let maxB = 0; inner.querySelectorAll('*').forEach(el => { const r = el.getBoundingClientRect(); if (r.height > 0) maxB = Math.max(maxB, r.bottom); });
  return { n: i + 1, fs: inner.dataset.fs ? +inner.dataset.fs : null, over: Math.round(maxB - ir.bottom) };
}));
const bad = info.filter(x => x.over > 1);
console.log('paginas', info.length, bad.length ? 'ESTOURO: ' + JSON.stringify(bad) : 'sem estouro');
console.log('letra (pt):', info.filter(x => x.fs).map(x => `${x.n}:${x.fs}`).join(' '));
const pages = await page.$$('.page'); let i = 0;
for (const el of pages) { i++; if (so && !so.includes(i)) continue; await el.screenshot({ path: path.join(out, `pagina-${String(i).padStart(3, '0')}.png`) }); }
await browser.close();
