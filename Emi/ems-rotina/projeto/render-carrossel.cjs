// Exporta as 6 lâminas (1080 × 1350) e a visão geral do carrossel.
const { chromium } = require('playwright');
const path = require('node:path');
const fs = require('node:fs');
(async () => {
  const out = path.join(__dirname, '..', 'entrega', 'carrossel'); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 6480, height: 1350 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(__dirname, 'carrossel.html'));
  await p.waitForFunction(() => window.READY === true);
  await p.waitForTimeout(400);
  for (let i = 0; i < 6; i++) await p.screenshot({ path: path.join(out, `lamina-0${i + 1}.png`), clip: { x: i * 1080, y: 0, width: 1080, height: 1350 } });
  await p.screenshot({ path: path.join(out, 'visao-geral.jpg'), type: 'jpeg', quality: 88 });
  // confere a margem de 90px: texto e etiquetas não podem passar dela
  const fora = await p.evaluate(() => [...document.querySelectorAll('.l')].flatMap((l, i) => [...l.querySelectorAll('.lead,.serif,.body,.cab,.tag,.pill')].map((e) => { const r = e.getBoundingClientRect(); const x0 = r.left - i * 1080, x1 = r.right - i * 1080;
    return (x0 < 88 || x1 > 992 || r.top < 88 || r.bottom > 1262) && !e.closest('.janela') ? `lâmina ${i + 1}: "${e.textContent.slice(0, 24)}" x ${Math.round(x0)}–${Math.round(x1)} y ${Math.round(r.top)}–${Math.round(r.bottom)}` : null; }).filter(Boolean)));
  console.log(fora.length ? fora.join('\n') : 'margens ok');
  await b.close();
})();
