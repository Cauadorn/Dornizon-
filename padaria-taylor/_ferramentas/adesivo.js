// Gera o adesivo da Doughgirl (borda branca de adesivo recortado) em PNG transparente, para colar na foto do saco.
// Uso: node padaria-taylor/_ferramentas/adesivo.js
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const raiz = path.resolve(__dirname, '..');
const svg = fs.readFileSync(path.join(raiz, '01-marca', 'ilustracao', 'doughgirl.svg'), 'utf8');
const saida = path.join(raiz, '03-mockups', '_camadas');

(async () => {
  fs.mkdirSync(saida, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 760, height: 880 } });
  await p.setContent(`<html><body style="margin:0;background:transparent">
    <div id="s" style="display:inline-block;padding:40px;filter:drop-shadow(9px 0 0 #fffdf8) drop-shadow(-9px 0 0 #fffdf8) drop-shadow(0 9px 0 #fffdf8) drop-shadow(0 -9px 0 #fffdf8)">${svg}</div></body></html>`);
  const el = await p.$('#s');
  await el.screenshot({ path: path.join(saida, 'adesivo-doughgirl.png'), omitBackground: true });
  await b.close();
  console.log('ok');
})();
