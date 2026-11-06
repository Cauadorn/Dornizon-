// Renderiza 07-apresentacao/behance/behance.html: cada módulo em JPG de 2800 px (1400 a 2x) e a capa (1616x1264).
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const OUT = path.join(__dirname, '..', '07-apresentacao', 'behance');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 1400 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(OUT, 'behance.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  const dir = path.join(OUT, 'modulos');
  fs.mkdirSync(dir, { recursive: true });
  for (const f of fs.readdirSync(dir)) fs.unlinkSync(path.join(dir, f));
  const mods = await p.$$('.mod');
  for (let i = 0; i < mods.length; i++) {
    const id = await mods[i].getAttribute('id');
    await mods[i].screenshot({ path: path.join(dir, `${String(i + 1).padStart(2, '0')}-${id}.jpg`), type: 'jpeg', quality: 88 });
  }
  await (await p.$('#capa-behance')).screenshot({ path: path.join(OUT, 'capa-behance-1616x1264.jpg'), type: 'jpeg', quality: 92 });
  console.log('ok', mods.length, 'módulos + capa');
  await b.close();
})();
