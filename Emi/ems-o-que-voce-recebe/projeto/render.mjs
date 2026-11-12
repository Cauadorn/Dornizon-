// Exporta o carrossel com o Chromium do Playwright.
// uso: node render.mjs                  -> ../entrega/lamina-01..06.png + visao-geral.jpg
//      node render.mjs --saida previa   -> em ../previa/
//      node render.mjs --guia           -> desenha a margem de 90px
import { createRequire } from 'node:module';
import http from 'node:http';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const dir = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const N = 6, W = 1080, H = 1350;
const saida = path.join(dir, '..', opt('--saida', 'entrega'));
fs.mkdirSync(saida, { recursive: true });

const tipos = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.ttf': 'font/ttf', '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml' };
const server = http.createServer((req, res) => {
  const p = path.join(dir, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!p.startsWith(dir) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': tipos[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: N * W, height: H }, deviceScaleFactor: 1 });
page.on('pageerror', (e) => console.error('erro na página:', e.message));
page.on('requestfailed', (r) => console.error('falhou:', r.url()));
await page.goto(`http://127.0.0.1:${server.address().port}/carrossel.html${args.includes('--guia') ? '?guia' : ''}`);
await page.waitForFunction(() => window.READY === true, null, { timeout: 60000 });
for (let k = 0; k < N; k++) {
  await page.screenshot({ path: path.join(saida, `lamina-${String(k + 1).padStart(2, '0')}.png`), clip: { x: k * W, y: 0, width: W, height: H } });
}
await page.screenshot({ path: path.join(saida, 'visao-geral.jpg'), type: 'jpeg', quality: 86, clip: { x: 0, y: 0, width: N * W, height: H } });
await browser.close();
server.close();
console.log('ok', saida);
