// Renderiza as lâminas de 02-apresentacao/apresentacao.html em PNG 1080 x 1350.
// Uso: node padaria-taylor/_ferramentas/render.js
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const raiz = path.resolve(__dirname, '..');
const html = path.join(raiz, '02-apresentacao', 'apresentacao.html');
const saida = path.join(raiz, '02-apresentacao', 'png');
const nomes = ['01-logo', '02-doughgirl', '03-cores', '04-adesivos', '05-saco', '06-cartao-fidelidade'];

(async () => {
  fs.rmSync(saida, { recursive: true, force: true });
  fs.mkdirSync(saida, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await p.goto('file://' + html);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  const secoes = await p.$$('section.l');
  for (let i = 0; i < secoes.length; i++) {
    await secoes[i].screenshot({ path: path.join(saida, `${nomes[i] || i + 1}.png`) });
  }
  await b.close();
  console.log('ok', secoes.length, 'lâminas');
})();
