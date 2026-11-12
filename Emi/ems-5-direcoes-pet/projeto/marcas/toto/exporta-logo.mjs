// Exporta o logo TOTÓ em PNG transparente, sem cortar as letras giradas: fotografa o palco inteiro
// (fundo transparente) e o recorte é feito depois, pelo alfa. uso: node exporta-logo.mjs <saida.png> [cor]
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import path from 'node:path'; import { fileURLToPath, pathToFileURL } from 'node:url';
const aqui = path.dirname(fileURLToPath(import.meta.url));
const [out, cor = '#FFF1D6'] = process.argv.slice(2);
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: 2 });
await p.goto(pathToFileURL(path.join(aqui, 'logo.html')).href + `?fundo=transparent&pata=anel&cor=${encodeURIComponent(cor)}`);
await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
await p.locator('.palco').screenshot({ path: out, omitBackground: true }); await b.close();
