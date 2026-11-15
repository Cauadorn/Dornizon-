// MIAU.LAB · exporta cada <section> de behance.html como uma prancha (2x: 2800 px de largura, JPG q92) + a capa do projeto.
// uso: node behance/exporta.mjs
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url';
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, '../../..'), out = path.join(aqui, 'pranchas');
fs.mkdirSync(out, { recursive: true });
const tipos = { '.html': 'text/html', '.png': 'image/png', '.woff2': 'font/woff2', '.js': 'text/javascript', '.jpg': 'image/jpeg' };
const srv = http.createServer((rq, rs) => { const f = path.join(raiz, decodeURIComponent(rq.url.split('?')[0]));
  fs.readFile(f, (e, d) => { if (e) { rs.writeHead(404); rs.end(); return; } rs.writeHead(200, { 'content-type': tipos[path.extname(f)] || 'application/octet-stream' }); rs.end(d); }); });
await new Promise(r => srv.listen(0, r));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: 2 });
await p.goto(`http://127.0.0.1:${srv.address().port}/marcas/miaulab/behance/behance.html`);
await p.waitForFunction(() => document.body.dataset.pronto === '1');
await p.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
await p.evaluate(async () => { const urls = [...document.querySelectorAll('.foto')].map(f => getComputedStyle(f).backgroundImage.slice(5, -2));
  await Promise.all(urls.map(u => { const i = new Image(); i.src = u; return i.decode().catch(() => {}); })); });
await p.waitForTimeout(500);
for (const s of await p.$$('section')) { const id = await s.getAttribute('id'); await s.screenshot({ path: path.join(out, `${id}.jpg`), type: 'jpeg', quality: 92 }); console.log(id); }
// capa do Behance (808x632 → 2x): recorte da prancha 01 centrado no gato
await p.setViewportSize({ width: 1400, height: 1750 });
await p.evaluate(() => window.scrollTo(0, 0));
const bb = await (await p.$('#b01')).boundingBox();
await p.screenshot({ path: path.join(out, 'capa-behance.jpg'), type: 'jpeg', quality: 92, clip: { x: bb.x + 296, y: bb.y + 520, width: 808, height: 632 } });
await b.close(); srv.close(); console.log('ok');
