// Fotografa o site para o módulo "o site" do Behance (salva em 07-apresentacao/behance/_img/).
const { chromium, devices } = require('playwright');
const path = require('path');
const fs = require('fs');
const SITE = 'file://' + path.join(__dirname, '..', '07-apresentacao', 'site') + '/';
const OUT = path.join(__dirname, '..', '07-apresentacao', 'behance', '_img');
fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch();
  const telas = [
    ['tela-desk-home', { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 }, 'index.html', null],
    ['tela-mob-estado', devices['iPhone 13'], 'estados/mato-grosso-do-sul.html', null],
    ['tela-mob-roda', devices['iPhone 13'], 'index.html', '.roda-palco'],
    ['tela-mob-colecao', devices['iPhone 13'], 'colecao.html', '#reg-5'],
  ];
  for (const [nome, opt, pg, alvo] of telas) {
    const ctx = await b.newContext(opt);
    await ctx.addInitScript(() => { try { sessionStorage.setItem('bq-visto', '1'); } catch (e) {} });
    const p = await ctx.newPage();
    await p.goto(SITE + pg, { waitUntil: 'load' });
    await p.waitForTimeout(2600);
    if (alvo) {
      const h = await p.evaluate(() => document.body.scrollHeight);
      for (let y = 0; y < h; y += 600) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(30); }
      const y = await p.evaluate(s => document.querySelector(s).getBoundingClientRect().top + scrollY, alvo);
      await p.evaluate(y => scrollTo(0, y), Math.max(0, y - (alvo.startsWith('#') ? 120 : 0)));
      await p.waitForTimeout(1500);
    }
    await p.screenshot({ path: path.join(OUT, nome + '.png') });
    await ctx.close();
  }
  console.log('telas ok');
  await b.close();
})();
