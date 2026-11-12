// Renderiza a faixa do case (10800 x 1350) e corta em lâminas 1080 x 1350.
// uso: node cortar.cjs [pasta-saida]
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const out = process.argv[2] || 'laminas'; fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 5400, height: 1350 } });
  await p.goto('file://' + path.resolve('case.html')); await p.waitForFunction(() => window.READY === true); await p.waitForTimeout(400);
  const el = await p.$('#faixa'); await el.screenshot({ path: path.join(out, 'faixa.png') });
  await b.close(); console.log('ok faixa');
})();
