// Renderiza 07-apresentacao/pdf/apresentacao.html em PDF (1920x1080 por página) e gera prévias JPG de cada página.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const OUT = path.join(__dirname, '..', '07-apresentacao', 'pdf');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + path.join(OUT, 'apresentacao.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  await p.pdf({ path: path.join(OUT, 'bem-querer-apresentacao.pdf'), width: '1920px', height: '1080px', printBackground: true, preferCSSPageSize: true });
  const prev = path.join(OUT, 'previas');
  fs.mkdirSync(prev, { recursive: true });
  const pgs = await p.$$('.pg');
  for (let i = 0; i < pgs.length; i++) {
    await pgs[i].screenshot({ path: path.join(prev, `pagina-${String(i + 1).padStart(2, '0')}.jpg`), type: 'jpeg', quality: 80 });
  }
  console.log('ok', pgs.length, 'páginas', (fs.statSync(path.join(OUT, 'bem-querer-apresentacao.pdf')).size / 1048576).toFixed(1), 'MB');
  await b.close();
})();
