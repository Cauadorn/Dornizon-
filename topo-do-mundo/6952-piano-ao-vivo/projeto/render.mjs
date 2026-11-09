// Exporta feed e story com o Chromium do Playwright.
// uso: node render.mjs                      -> entrega/feed.png e entrega/story.png (textos.json)
//      node render.mjs calibracao.json      -> idem, com outro arquivo de textos, em entrega/teste-*.png
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import http from 'node:http';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const dir = path.dirname(fileURLToPath(import.meta.url));
const textos = process.argv[2] || 'textos.json';
const prefixo = process.argv[2] ? 'teste-' : '';
const saida = path.join(dir, '..', 'entrega');
fs.mkdirSync(saida, { recursive: true });

const tipos = { '.html': 'text/html', '.json': 'application/json', '.ttf': 'font/ttf', '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml' };
const server = http.createServer((req, res) => {
  const p = path.join(dir, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!p.startsWith(dir) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': tipos[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const base = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch();

for (const [f, h] of [['feed', 1350], ['story', 1920]]) {
  const page = await browser.newPage({ viewport: { width: 1080, height: h }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => console.error('erro na página:', e.message));
  await page.goto(`${base}/arte.html?f=${f}&t=${encodeURIComponent(textos)}`);
  await page.waitForFunction(() => window.READY === true, null, { timeout: 60000 });
  const arquivo = path.join(saida, `${prefixo}${f}.png`);
  await page.locator('#arte').screenshot({ path: arquivo });
  console.log(arquivo);
}
await browser.close();
server.close();
