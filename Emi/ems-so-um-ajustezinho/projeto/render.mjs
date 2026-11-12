// Exporta as lâminas com o Chromium do Playwright.
// uso: node render.mjs   -> ../entrega/lamina-01..06.png + ../entrega/visao-geral.jpg
import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const dir = path.dirname(fileURLToPath(import.meta.url));
const saida = path.join(dir, '..', 'entrega');
fs.mkdirSync(saida, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080 * 6, height: 1350 }, deviceScaleFactor: 1 });
page.on('pageerror', (e) => console.error('erro na página:', e.message));
await page.goto(pathToFileURL(path.join(dir, 'carrossel.html')).href);
await page.waitForFunction(() => window.READY === true, null, { timeout: 60000 });

const laminas = page.locator('.lamina');
const n = await laminas.count();
for (let k = 0; k < n; k++) {
  await laminas.nth(k).screenshot({ path: path.join(saida, `lamina-${String(k + 1).padStart(2, '0')}.png`) });
}
const faixa = path.join(dir, 'faixa.png');
await page.screenshot({ path: faixa, fullPage: true });
await browser.close();

await new Promise((ok, falha) => {
  const p = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-i', faixa, '-vf', 'scale=3240:-1:flags=lanczos', '-q:v', '3', '-update', '1', path.join(saida, 'visao-geral.jpg')], { stdio: 'inherit' });
  p.on('close', (c) => (c === 0 ? ok() : falha(new Error('ffmpeg ' + c))));
});
fs.rmSync(faixa);
console.log('ok', n, 'lâminas');
