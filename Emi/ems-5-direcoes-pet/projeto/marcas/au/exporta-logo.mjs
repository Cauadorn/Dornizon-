// Exporta o logo MATILHA em PNG transparente, aparado pelo alfa (fotografa o palco inteiro, como no TOTÓ).
// uso: node exporta-logo.mjs <saida.png> [tinta=#121212]
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import path from 'node:path'; import { fileURLToPath } from 'node:url';
const aqui = path.dirname(fileURLToPath(import.meta.url));
const [saida, tinta = '#121212'] = process.argv.slice(2);
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: 3 });
await p.goto(`file://${aqui}/logo.html?bordas=0&fundo=transparent&tinta=${encodeURIComponent(tinta)}`);
await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
await p.addStyleTag({ content: 'html,body,.palco{background:transparent!important}' });
const png = await p.screenshot({ omitBackground: true });
await b.close();
const sharpless = await import('node:fs'); sharpless.writeFileSync(saida, png); console.log('ok', saida);
