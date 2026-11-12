// Exporta cada .art de um HTML como PNG (transparente onde a arte não tem fundo).
// uso: node artes.cjs <arquivo.html> <pasta-saida>
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const [f, out] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 2000, height: 1400 } });
  await p.goto('file://' + path.resolve(f));
  await p.waitForFunction(() => window.READY === true);
  await p.waitForTimeout(300);
  await p.addStyleTag({ content: 'body{background:transparent!important}' });
  for (const el of await p.$$('.art')) {
    const id = await el.getAttribute('id');
    await el.screenshot({ path: path.join(out, id + '.png'), omitBackground: true });
    console.log('ok', id);
  }
  await b.close();
})();
