// Prints do site (celular) para os mockups do reel: abertura, roda e página de estado.
const { chromium, devices } = require('playwright');
const path = require('path');
const fs = require('fs');
const SITE = 'file://' + path.join(__dirname, '..', '07-apresentacao', 'site') + '/';
const OUT = path.join(__dirname, '..', '07-apresentacao', 'behance', '_img');
fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch();
  for (const [nome, pg, alvo, espera] of [['reel-tela-home', 'index.html', null, 3200], ['reel-tela-roda', 'index.html', '.roda', 1500],
    ['reel-tela-estado', 'estados/mato-grosso-do-sul.html', null, 2800]]) {
    const ctx = await b.newContext(devices['iPhone 13']);
    await ctx.addInitScript(() => { try { sessionStorage.setItem('bq-visto', '1'); } catch (e) {} });
    const p = await ctx.newPage();
    await p.goto(SITE + pg, { waitUntil: 'load' });
    await p.waitForTimeout(espera);
    if (alvo) {
      const h = await p.evaluate(() => document.body.scrollHeight);
      for (let y = 0; y < h; y += 600) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(30); }
      const y = await p.evaluate(s => document.querySelector(s).getBoundingClientRect().top + scrollY, alvo);
      await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(1600);
    }
    await p.screenshot({ path: path.join(OUT, nome + '.png') });
    await ctx.close();
  }
  console.log('telas do reel ok');
  await b.close();
})();
