// Gera PNGs transparentes com texto "de caneta" para colar nos mockups.
// Uso: node padaria-taylor/_ferramentas/escrita.js
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const raiz = path.resolve(__dirname, '..');
const fonte = fs.readFileSync(path.join(raiz, '_fontes', 'NanumPenScript-400.ttf')).toString('base64');
const saida = path.join(raiz, '03-mockups', '_camadas');

const textos = {
  'recado-original': `<div style="font-size:150px;line-height:.9;transform:rotate(-3deg)">Original Sourdough!</div>
    <div style="font-size:110px;line-height:1;margin:26px 0 0 120px;transform:rotate(-1.5deg)">baked at 4am, for you
    <svg width="78" height="70" viewBox="0 0 78 70" style="vertical-align:-6px"><path d="M39 64 C10 44 2 30 6 18 C11 4 30 4 39 20 C47 4 68 4 72 18 C76 32 66 46 39 64Z" fill="none" stroke="#000" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/></svg></div>`,
};

(async () => {
  fs.mkdirSync(saida, { recursive: true });
  const b = await chromium.launch();
  for (const [nome, html] of Object.entries(textos)) {
    const p = await b.newPage({ viewport: { width: 1600, height: 500 } });
    await p.setContent(`<html><head><style>@font-face{font-family:P;src:url(data:font/ttf;base64,${fonte})}
      body{margin:0;background:transparent}#t{display:inline-block;padding:30px;font-family:P;color:#000}</style></head>
      <body><div id="t">${html}</div></body></html>`);
    await p.evaluate(() => document.fonts.ready);
    const el = await p.$('#t');
    await el.screenshot({ path: path.join(saida, `${nome}.png`), omitBackground: true });
    await p.close();
  }
  await b.close();
  console.log('ok');
})();
