// Camadas de impressão (preto no branco) para aplicar nas fotos: a betty a uma cor e a assinatura.
// Uso: node padaria-taylor/_ferramentas/camadas.js
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const raiz = path.resolve(__dirname, '..');
const saida = path.join(raiz, '03-mockups', '_camadas');
const f = n => fs.readFileSync(path.join(raiz, '_fontes', n)).toString('base64');

const camadas = {
  'impressao-betty': fs.readFileSync(path.join(raiz, '01-marca', 'ilustracao', 'betty-impressao.svg'), 'utf8'),
  'impressao-assinatura': `<div style="text-align:center;padding:10px 30px">
     <div style="font:900 190px/1 Fr;letter-spacing:-.03em">loaf story</div>
     <div style="font:italic 60px/1.2 Fell;margin-top:6px">a small, free business</div></div>`,
};

(async () => {
  fs.mkdirSync(saida, { recursive: true });
  const b = await chromium.launch();
  for (const [nome, html] of Object.entries(camadas)) {
    const p = await b.newPage({ viewport: { width: 1400, height: 800 } });
    await p.setContent(`<html><head><style>
      @font-face{font-family:Fr;src:url(data:font/ttf;base64,${f('Fraunces-900.ttf')});font-weight:900}
      @font-face{font-family:Fell;src:url(data:font/ttf;base64,${f('IMFellDWPica-400-italic.ttf')});font-style:italic}
      body{margin:0;background:#fff;color:#000}#t{display:inline-block}</style></head><body><div id="t">${html}</div></body></html>`);
    await p.evaluate(() => document.fonts.ready);
    await (await p.$('#t')).screenshot({ path: path.join(saida, `${nome}.png`) });
    await p.close();
  }
  await b.close();
  console.log('ok');
})();
