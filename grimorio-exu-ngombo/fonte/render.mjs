import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import path from 'node:path';
import fs from 'node:fs';
const dir = path.dirname(new URL(import.meta.url).pathname);
const modo = process.argv[2] || 'leitura';           // leitura | construcao
const out = path.join(dir, 'out', modo);
fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 2.5, viewport: { width: 700, height: 900 } });
await page.goto('file://' + path.join(dir, 'grimorio.html') + (modo === 'construcao' ? '?modo=construcao' : ''), { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(500);
const info = await page.evaluate(() => [...document.querySelectorAll('.page')].map((p, i) => {
  const inner = p.querySelector('.inner'); const pr = p.getBoundingClientRect(); const ir = inner.getBoundingClientRect();
  let maxB = 0; inner.querySelectorAll('*').forEach(el => { const r = el.getBoundingClientRect(); if (r.height > 0) maxB = Math.max(maxB, r.bottom); });
  return { n: i + 1, id: p.id, over: Math.round(maxB - ir.bottom) };
}));
const bad = info.filter(x => x.over > 1);
console.log('paginas', info.length, bad.length ? 'ESTOURO: ' + JSON.stringify(bad) : 'sem estouro');
const pages = await page.$$('.page'); let i = 0;
for (const el of pages) { i++; await el.screenshot({ path: path.join(out, `pagina-${String(i).padStart(2, '0')}.png`) }); }
await browser.close();
