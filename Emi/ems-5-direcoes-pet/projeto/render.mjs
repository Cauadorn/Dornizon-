// Exporta o carrossel com o Chromium do Playwright.
// uso: node render.mjs            -> ../entrega/lamina-01..07.png + ../entrega/visao-geral.jpg
//      node render.mjs --previa   -> ../previa/ (só a visão geral, para conferir)
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';

const dir = path.dirname(fileURLToPath(import.meta.url));
const previa = process.argv.includes('--previa');
const saida = path.join(dir, '..', previa ? 'previa' : 'entrega');
fs.mkdirSync(saida, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(dir, 'carrossel.html')).href);
await page.waitForFunction(() => window.pronto && window.pronto(), null, { timeout: 30000 });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(300);

const nomes = await page.$$eval('section.slide', (ss) => ss.map((s) => s.dataset.nome));
const arquivos = [];
for (const nome of nomes) {
  const f = path.join(saida, `${nome}.png`);
  await page.locator(`section[data-nome="${nome}"]`).screenshot({ path: f });
  arquivos.push(f);
  console.log(f);
}

// visão geral: as 7 lâminas lado a lado
const vg = await browser.newPage({ viewport: { width: 7 * 540 + 8 * 24, height: 675 + 48 } });
const imgs = arquivos.map((f) => `<img src="data:image/png;base64,${fs.readFileSync(f).toString('base64')}" style="width:540px;height:675px;display:block">`).join('');
await vg.setContent(`<body style="margin:0;background:#1b1020;display:flex;gap:24px;padding:24px">${imgs}</body>`);
await vg.waitForLoadState('load');
await vg.screenshot({ path: path.join(saida, 'visao-geral.jpg'), quality: 88, type: 'jpeg' });
console.log(path.join(saida, 'visao-geral.jpg'));
await browser.close();
