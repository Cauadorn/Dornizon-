// Captura as telas do programa "minha semana" em cada etapa, para o reel e o carrossel.
const { chromium } = require('playwright');
const path = require('node:path');
const fs = require('node:fs');
const DUMP = [
  'pet shop: aprovar paleta na terça',
  'cafeteria: responder orçamento',
  'carrossel da clínica pra sexta',
  'pet shop: mandar manual da marca quinta',
  'editar fotos do ensaio',
  'reunião de briefing da confeitaria segunda',
  'site da cafeteria: revisar a página inicial',
  'emitir nota do mês',
].join('\n');
(async () => {
  const out = path.join(__dirname, 'telas'); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 760, height: 1180 }, deviceScaleFactor: 2 });
  await p.addInitScript(() => { const D = Date; const fixo = new D(2026, 10, 16, 9, 0).getTime(); // segunda, 16 de novembro
    window.Date = class extends D { constructor(...a) { super(...(a.length ? a : [fixo])); } static now() { return fixo + Math.random() * 1000; } }; });
  await p.goto('file://' + path.join(__dirname, 'semana.html'));
  await p.evaluate(() => { localStorage.clear(); }); await p.reload();
  await p.evaluate(() => document.fonts.ready);
  const shot = (n) => p.screenshot({ path: path.join(out, n + '.png') });
  await shot('1-vazio');
  await p.fill('#dump', DUMP); await shot('2-despejo');
  await p.click('#organizar'); await p.waitForTimeout(1500);
  await p.evaluate(() => window.scrollTo(0, document.querySelector('#dias').offsetTop - 150)); await p.waitForTimeout(200);
  await shot('3-semana');
  const boxes = p.locator('.card input');
  await boxes.nth(0).check(); await p.locator('.card input').nth(2).check(); await p.locator('.card input').nth(4).check();
  await p.waitForTimeout(600); await shot('4-feitos');
  await p.screenshot({ path: path.join(out, '5-inteira.png'), fullPage: true });
  await b.close();
})();
