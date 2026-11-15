// Conferência de texto das lâminas (regras da Emi):
//  1) palavra de 1 ou 2 letras nunca sobra no fim da linha: desce com a palavra seguinte;
//  2) sem viúva: a última linha de um bloco não pode ter uma palavra só (a não ser que todas as linhas tenham uma);
//  3) centralização: bloco marcado com data-centro tem o texto no meio da lâmina (ou do cartão data-bloco em que está);
//  4) margem de 90px para texto.
// uso: node conferir-texto.cjs "pagina.html?n=2" ["pagina.html?n=3" ...]
const { chromium } = require('playwright'); const path = require('node:path');
(async () => {
  const b = await chromium.launch(); let total = 0;
  for (const alvo of process.argv.slice(2)) {
    const [arq, q] = alvo.split('?'); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
    await p.goto('file://' + path.resolve(arq) + (q ? '?' + q : '')); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(700);
    const achados = await p.evaluate(() => {
      document.querySelectorAll('#c *').forEach((e) => { if (getComputedStyle(e).transform !== 'none') e.style.transform = 'none'; });   // mede sem rotação
      const out = [], vis = (e) => { const s = getComputedStyle(e); return s.display !== 'none' && s.visibility !== 'hidden' && +s.opacity > 0.05; };
      const temBlocoFilho = (e) => [...e.querySelectorAll('*')].some((c) => ['block', 'flex', 'grid'].includes(getComputedStyle(c).display) && c.textContent.trim());
      const blocos = [...document.querySelectorAll('#c *')].filter((e) => vis(e) && e.textContent.trim() && !temBlocoFilho(e) && !['inline'].includes(getComputedStyle(e).display));
      for (const e of blocos) {
        const palavras = []; const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT);
        for (let n = w.nextNode(); n; n = w.nextNode()) { const re = /\S+/g; let m; while ((m = re.exec(n.data))) { const r = document.createRange(); r.setStart(n, m.index); r.setEnd(n, m.index + m[0].length); const q = r.getBoundingClientRect(); if (q.width) palavras.push({ t: m[0], x0: q.left, x1: q.right, y: (q.top + q.bottom) / 2, h: q.height }); } }
        if (!palavras.length) continue;
        const linhas = []; for (const pl of palavras) { const l = linhas.find((L) => Math.abs(L.y - pl.y) < pl.h * 0.45); if (l) l.p.push(pl); else linhas.push({ y: pl.y, p: [pl] }); }
        linhas.sort((a, c) => a.y - c.y); const txt = palavras.map((x) => x.t).join(' ').slice(0, 44);
        const limpa = (t) => t.replace(/[^\p{L}\p{N}]/gu, '');
        linhas.slice(0, -1).forEach((l) => { const u = l.p[l.p.length - 1].t; if (limpa(u).length > 0 && limpa(u).length <= 2) out.push(`palavra curta no fim da linha: "${u}" em «${txt}»`); });
        if (linhas.length > 1 && linhas[linhas.length - 1].p.length === 1 && linhas.some((l) => l.p.length > 1)) out.push(`viúva: "${linhas[linhas.length - 1].p[0].t}" sozinha na última linha de «${txt}»`);
        const x0 = Math.min(...palavras.map((x) => x.x0)), x1 = Math.max(...palavras.map((x) => x.x1)), ys = palavras.map((x) => x.y);
        const girado = e.closest('[data-bloco]');
        if (!girado && (x0 < 88 || x1 > 992 || Math.min(...ys) < 88 || Math.max(...ys) > 1262)) out.push(`fora da margem de 90px (x ${Math.round(x0)}–${Math.round(x1)}): «${txt}»`);
        if (e.closest('[data-centro]') || e.hasAttribute('data-centro')) { const base = girado ? girado.getBoundingClientRect() : { left: 0, right: 1080 }; const meio = (base.left + base.right) / 2;
          linhas.forEach((l) => { const c = (Math.min(...l.p.map((x) => x.x0)) + Math.max(...l.p.map((x) => x.x1))) / 2; if (Math.abs(c - meio) > 14) out.push(`fora do centro em ${Math.round(c - meio)}px: «${l.p.map((x) => x.t).join(' ').slice(0, 40)}»`); }); }
      }
      // 5) miolo de cartão: o conteúdo tem a mesma folga em cima e embaixo, e dos dois lados
      for (const m of document.querySelectorAll('[data-miolo]')) { const base = m.getBoundingClientRect(); let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9;
        const w = document.createTreeWalker(m, NodeFilter.SHOW_TEXT); for (let n = w.nextNode(); n; n = w.nextNode()) { if (!n.data.trim()) continue; const r = document.createRange(); r.selectNodeContents(n); for (const q of r.getClientRects()) { x0 = Math.min(x0, q.left); x1 = Math.max(x1, q.right); y0 = Math.min(y0, q.top); y1 = Math.max(y1, q.bottom); } }
        // conta também imagem, caixinha de marcar e linha pontilhada: tudo o que se vê dentro do cartão
        m.querySelectorAll('*').forEach((i) => { const s = getComputedStyle(i); if (i.tagName !== 'IMG' && !(parseFloat(s.borderTopWidth) > 0 || parseFloat(s.borderLeftWidth) > 0)) return; const q = i.getBoundingClientRect(); if (!q.width) return; x0 = Math.min(x0, q.left); x1 = Math.max(x1, q.right); y0 = Math.min(y0, q.top); y1 = Math.max(y1, q.bottom); });
        const cima = y0 - base.top, baixo = base.bottom - y1, esq = x0 - base.left, dir = base.right - x1;
        if (Math.abs(cima - baixo) > 22) out.push(`cartão com folga desigual: ${Math.round(cima)}px em cima, ${Math.round(baixo)}px embaixo`);
        if (Math.abs(esq - dir) > 22) out.push(`cartão com folga desigual: ${Math.round(esq)}px à esquerda, ${Math.round(dir)}px à direita`);
        if (Math.min(cima, baixo, esq, dir) < 28) out.push(`conteúdo encostando na borda do cartão (menor folga ${Math.round(Math.min(cima, baixo, esq, dir))}px)`); }
      return out;
    });
    console.log(`\n${alvo}: ${achados.length ? achados.length + ' problema(s)' : 'ok'}`); achados.forEach((a) => console.log('  - ' + a)); total += achados.length; await p.close();
  }
  await b.close(); process.exit(total ? 1 : 0);
})();
