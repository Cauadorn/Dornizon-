// Renderiza 07-apresentacao/instagram/carrossel.html em JPGs 1080x1440, um por slide.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const OUT = path.join(__dirname, '..', '07-apresentacao', 'instagram');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1440 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(OUT, 'carrossel.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  const dir = path.join(OUT, 'slides');
  fs.mkdirSync(dir, { recursive: true });
  const sls = await p.$$('.sl');
  for (let i = 0; i < sls.length; i++) {
    await sls[i].screenshot({ path: path.join(dir, `bem-querer-${String(i + 1).padStart(2, '0')}.jpg`), type: 'jpeg', quality: 92 });
  }
  console.log('ok', sls.length, 'slides');
  await b.close();
})();
