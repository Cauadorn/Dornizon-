// Exporta cada SVG de 01-marca/svg para PNG com fundo transparente (4x), para usar no Canva/Figma.
// Uso: node lumi-odonto/_ferramentas/logos_png.js
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const raiz = path.resolve(__dirname, '..');
const pasta = path.join(raiz, '01-marca', 'svg');
const saida = path.join(raiz, '01-marca', 'png');

(async () => {
  fs.rmSync(saida, { recursive: true, force: true });
  fs.mkdirSync(saida, { recursive: true });
  const b = await chromium.launch();
  for (const arq of fs.readdirSync(pasta).filter(f => f.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(pasta, arq), 'utf8');
    const [, w, h] = svg.match(/width="([\d.]+)" height="([\d.]+)"/);
    const avatar = arq.includes('avatar');
    const escala = avatar ? 1 : 4;
    const p = await b.newPage({ viewport: { width: Math.ceil(+w), height: Math.ceil(+h) }, deviceScaleFactor: escala });
    await p.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
    await p.screenshot({ path: path.join(saida, arq.replace('.svg', '.png')), omitBackground: !avatar, clip: { x: 0, y: 0, width: +w, height: +h } });
    await p.close();
  }
  await b.close();
  console.log('ok', fs.readdirSync(saida).length, 'PNGs em', path.relative(process.cwd(), saida));
})();
