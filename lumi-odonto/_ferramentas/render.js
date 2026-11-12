// Renderiza cada prancha de 02-identidade/identidade.html em PNG 1080 x 1350.
// Uso: node lumi-odonto/_ferramentas/render.js
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const raiz = path.resolve(__dirname, '..');
const html = path.join(raiz, '02-identidade', 'identidade.html');
const saida = path.join(raiz, '02-identidade', 'png');
const nomes = ['01-capa', '02-lettering', '03-versoes', '04-cores', '05-tipografia', '06-aplicacoes', '07-fotos', '08-voz'];

(async () => {
  fs.rmSync(saida, { recursive: true, force: true });
  fs.mkdirSync(saida, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await p.goto('file://' + html);
  await p.waitForSelector('body[data-pronto="1"]');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  const secoes = await p.$$('section.b');
  for (let i = 0; i < secoes.length; i++) {
    const arq = path.join(saida, `${nomes[i] || String(i + 1).padStart(2, '0')}.png`);
    await secoes[i].screenshot({ path: arq });
    console.log('ok', path.relative(raiz, arq));
  }
  await b.close();
})();
