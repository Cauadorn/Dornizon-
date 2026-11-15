// Confere se alguma palavra curta (1 ou 2 letras: e, o, a, é, da, de, do, em, um...) ficou sobrando
// no fim de uma linha. Regra: ela sempre desce junto com a palavra seguinte.
// Pega tanto a quebra automática quanto o <br> escrito à mão.
// Uso: node conferir-palavra-curta.js <arquivo.html> [largura altura]
//      (espera window.READY === true se a página definir; padrão 6480x1350, a faixa do carrossel)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [arq, w = '6480', h = '1350'] = process.argv.slice(2);
  if (!arq) { console.log('uso: node conferir-palavra-curta.js <arquivo.html> [largura altura]'); process.exit(2); }
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +h } });
  await p.goto('file://' + path.resolve(arq));
  await p.waitForFunction(() => window.READY === true || !('READY' in window), null, { timeout: 60000 }).catch(() => {});
  await p.waitForTimeout(300);
  const achados = await p.evaluate(() => {
    const curta = /^[\p{L}]{1,2}$/u;
    const blocoDe = (el) => {
      for (let e = el; e; e = e.parentElement) {
        const d = getComputedStyle(e).display;
        if (!d.startsWith('inline') && d !== 'contents') return e;
      }
      return document.body;
    };
    const palavras = [];
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: (n) => (n.parentElement.closest('script,style') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT),
    });
    for (let n; (n = w.nextNode());) {
      const re = /[^\s ]+/g;
      for (let m; (m = re.exec(n.data));) {
        const r = document.createRange(); r.setStart(n, m.index); r.setEnd(n, m.index + m[0].length);
        const rs = [...r.getClientRects()].filter((x) => x.width > 0);
        if (!rs.length) continue;
        palavras.push({ t: m[0], r: rs[rs.length - 1], bloco: blocoDe(n.parentElement), el: n.parentElement });
      }
    }
    const out = [];
    for (let i = 0; i < palavras.length - 1; i++) {
      const a = palavras[i], z = palavras[i + 1];
      if (a.bloco !== z.bloco || !curta.test(a.t)) continue;
      if (z.r.top > a.r.top + a.r.height * 0.5) {
        const lam = a.el.closest('.lamina');
        out.push(`${lam ? lam.id || 'lâmina' : ''} "${palavras.slice(Math.max(0, i - 3), i + 1).map((x) => x.t).join(' ')} ⏎ ${z.t}"`);
      }
    }
    return out;
  });
  await b.close();
  if (!achados.length) console.log('nenhuma palavra curta sobrando no fim da linha');
  else { console.log('palavra curta sobrando no fim da linha:'); achados.forEach((x) => console.log(' -', x)); process.exitCode = 1; }
})();
