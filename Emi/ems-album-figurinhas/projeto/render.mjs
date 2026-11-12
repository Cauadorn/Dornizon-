// Exporta o carrossel com o Chromium do Playwright.
// uso: node render.mjs                 -> ../entrega/lamina-01..07.png + visao-geral.jpg
//      node render.mjs --n 2 --saida previa   -> só as 2 primeiras lâminas em ../previa/
//      node render.mjs --guia          -> desenha a margem de 90px (conferência)
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
const N = +opt('--n', 7);
const saida = path.join(dir, '..', opt('--saida', 'entrega'));
fs.mkdirSync(saida, { recursive: true });

const tipos = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.ttf': 'font/ttf', '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml' };
const server = http.createServer((req, res) => {
  const p = path.join(dir, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!p.startsWith(dir) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': tipos[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const base = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: N * 1080, height: 1350 }, deviceScaleFactor: 1 });
page.on('pageerror', (e) => console.error('erro na página:', e.message));
page.on('requestfailed', (r) => console.error('falhou:', r.url()));
await page.goto(`${base}/carrossel.html?n=${N}${args.includes('--guia') ? '&guia' : ''}`);
await page.waitForFunction(() => window.READY === true, null, { timeout: 60000 });

for (let k = 0; k < N; k++) {
  await page.screenshot({ path: path.join(saida, `lamina-${String(k + 1).padStart(2, '0')}.png`), clip: { x: k * 1080, y: 0, width: 1080, height: 1350 } });
}
await page.screenshot({ path: path.join(saida, 'visao-geral.jpg'), type: 'jpeg', quality: 88, clip: { x: 0, y: 0, width: N * 1080, height: 1350 } });
await browser.close();
server.close();
console.log('ok', saida);
