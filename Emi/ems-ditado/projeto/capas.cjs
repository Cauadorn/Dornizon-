const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 2160, height: 1350 } });
  await p.goto('file://' + path.join(__dirname, 'capas.html')); await p.waitForFunction(() => window.READY === true);
  await p.screenshot({ path: path.join(__dirname, '../previa/capa-A-coracao.png'), clip: { x: 0, y: 0, width: 1080, height: 1350 } });
  await p.screenshot({ path: path.join(__dirname, '../previa/capa-B-lembrado.png'), clip: { x: 1080, y: 0, width: 1080, height: 1350 } });
  await p.screenshot({ path: path.join(__dirname, '../previa/lado-a-lado.jpg'), type: 'jpeg', quality: 88 }); await b.close(); })();
