// Exporta as capas de destaque: ../entrega/destaque-servicos-a.png e -b.png (1080 × 1920, arte no círculo central de 720px)
// e destaque-previa.jpg (como fica no círculo do perfil).
import { createRequire } from 'node:module';
import http from 'node:http'; import path from 'node:path'; import fs from 'node:fs';
import { fileURLToPath } from 'node:url';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const dir = path.dirname(fileURLToPath(import.meta.url));
const saida = path.join(dir, '..', 'entrega');
const tipos = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.ttf': 'font/ttf', '.jpg': 'image/jpeg', '.png': 'image/png' };
const server = http.createServer((req, res) => {
  const p = path.join(dir, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!p.startsWith(dir) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': tipos[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(res);
}).listen(0);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 2160, height: 1920 }, deviceScaleFactor: 1 });
page.on('pageerror', (e) => console.error('erro na página:', e.message));
await page.goto(`http://127.0.0.1:${server.address().port}/destaque.html`);
await page.waitForFunction(() => window.READY === true, null, { timeout: 60000 });
for (const [k, n] of [[0, 'a'], [1, 'b']]) await page.screenshot({ path: path.join(saida, `destaque-servicos-${n}.png`), clip: { x: k * 1080, y: 0, width: 1080, height: 1920 } });
await browser.close(); server.close(); console.log('ok');
