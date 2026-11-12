// Exporta o carrossel (carrossel.html) como "cena" de camadas para montar no Figma com use_figma.
// Saída em figma/saida/: cena-<lamina>.json (árvore de quadros, textos, imagens e SVGs, coordenadas locais)
// e rasters/*.png (padrões, estrelas em retícula, grão, código de barras: o que não vira vetor simples).
// uso: node figma/exporta.mjs
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';

const dir = path.dirname(fileURLToPath(import.meta.url));
const projeto = path.join(dir, '..');
const saida = path.join(dir, 'saida');
fs.mkdirSync(path.join(saida, 'rasters'), { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(projeto, 'carrossel.html')).href);
await page.waitForFunction(() => window.pronto && window.pronto(), null, { timeout: 30000 });
await page.evaluate(() => document.fonts.ready);

const { cenas, rasters } = await page.evaluate(() => {
  const R = (v) => Math.round(v * 10) / 10;
  const cor = (s) => {            // "rgb(1, 2, 3)" / "rgba(1, 2, 3, .5)" -> [r,g,b,a] 0-1
    const m = s && s.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(',').map((x) => parseFloat(x));
    const a = p.length > 3 ? p[3] : 1; if (a === 0) return null;
    return [R(p[0] / 255 * 1000) / 1000, R(p[1] / 255 * 1000) / 1000, R(p[2] / 255 * 1000) / 1000, a];
  };
  const sombras = (s, tipo) => {   // box-shadow / text-shadow / drop-shadow -> [{x,y,b,c}]
    if (!s || s === 'none') return null;
    const out = [];
    for (const parte of s.split(/,(?![^(]*\))/)) {
      const c = cor(parte); const nums = (parte.replace(/rgba?\([^)]*\)/, '').match(/-?[\d.]+px/g) || []).map(parseFloat);
      if (c && nums.length >= 2) out.push({ x: nums[0], y: nums[1], b: nums[2] || 0, c });
    }
    return out.length ? out : null;
  };

  // 1) tira as rotações para medir o layout sem transformação (coordenadas locais)
  const todos = [...document.querySelectorAll('.slide, .slide *')];
  const trans = new Map();
  for (const e of todos) {
    const t = getComputedStyle(e).transform;
    if (t && t !== 'none') { trans.set(e, t); e.style.setProperty('transform', 'none', 'important'); }
  }
  const rect = new Map(todos.map((e) => [e, e.getBoundingClientRect()]));
  const matriz = (e) => {
    const t = trans.get(e); if (!t) return null;
    const m = t.match(/matrix\(([^)]+)\)/); if (!m) return null;
    const [a, b, c, d] = m[1].split(',').map(parseFloat);
    const sx = Math.hypot(a, b);
    return { a: a / sx, b: b / sx, c: c / sx, d: d / sx, flip: a < 0 && Math.abs(b) < 1e-6 };
  };

  const rasters = []; let nr = 0;
  const novoRaster = (w, h, html) => { const id = `r${String(++nr).padStart(3, '0')}`; rasters.push({ id, w: Math.round(w), h: Math.round(h), html }); return id; };

  const inline = (e, cs) => ['EM', 'B', 'STRONG', 'SMALL', 'SPAN', 'BR', 'I'].includes(e.tagName) && cs.position !== 'absolute' && cs.display.startsWith('inline') && cs.display !== 'inline-block';
  const temTextoDireto = (e) => [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());

  function runsDe(e, runs) {
    for (const n of e.childNodes) {
      if (n.nodeType === 3) {
        const t = n.textContent.replace(/\s+/g, ' ');
        if (!t) continue;
        const cs = getComputedStyle(e);
        runs.push({ s: t, ff: cs.fontFamily.split(',')[0].replace(/["']/g, '').trim(), fw: +cs.fontWeight, it: cs.fontStyle === 'italic' ? 1 : 0,
          fs: R(parseFloat(cs.fontSize)), c: cor(cs.color), ls: cs.letterSpacing === 'normal' ? 0 : R(parseFloat(cs.letterSpacing)) });
      } else if (n.nodeType === 1) {
        const cs = getComputedStyle(n);
        if (n.tagName === 'BR') runs.push({ s: '\n' });
        else if (inline(n, cs)) runsDe(n, runs);
      }
    }
    return runs;
  }

  function textoDe(e, cs, base) {
    const runs = runsDe(e, []);
    // apara espaços nas pontas e em volta de quebras
    let txt = runs.map((r) => r.s).join('');
    if (!txt.trim()) return null;
    if (runs.length) { runs[0].s = runs[0].s.replace(/^\s+/, ''); runs[runs.length - 1].s = runs[runs.length - 1].s.replace(/\s+$/, ''); }
    for (let i = 0; i < runs.length; i++) if (runs[i].s === '\n') { if (runs[i - 1]) runs[i - 1].s = runs[i - 1].s.replace(/\s+$/, ''); if (runs[i + 1]) runs[i + 1].s = runs[i + 1].s.replace(/^\s+/, ''); }
    const r = rect.get(e);
    const pl = parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth), pt = parseFloat(cs.paddingTop) + parseFloat(cs.borderTopWidth);
    const pr = parseFloat(cs.paddingRight) + parseFloat(cs.borderRightWidth), pb = parseFloat(cs.paddingBottom) + parseFloat(cs.borderBottomWidth);
    // linhas reais (para decidir largura automática ou fixa)
    const tops = new Set();
    const walker = document.createTreeWalker(e, NodeFilter.SHOW_TEXT);
    let nd; while ((nd = walker.nextNode())) { const rg = document.createRange(); rg.selectNodeContents(nd); for (const q of rg.getClientRects()) if (q.width > 0) tops.add(Math.round(q.top)); }
    const lh = cs.lineHeight === 'normal' ? null : R(parseFloat(cs.lineHeight));
    const t = { k: 't', x: R(r.left - base.left + pl), y: R(r.top - base.top + pt), w: R(r.width - pl - pr), h: R(r.height - pt - pb),
      al: cs.textAlign === 'center' ? 'C' : cs.textAlign === 'right' || cs.textAlign === 'end' ? 'R' : 'L', lh, linhas: tops.size, runs: runs.filter((x) => x.s) };
    const sh = sombras(cs.textShadow); if (sh) t.sh = sh;
    const sw = parseFloat(cs.webkitTextStrokeWidth); if (sw > 0) t.st = { w: sw / 2, c: cor(cs.webkitTextStrokeColor) };
    return t;
  }

  function svgDe(e, base) {
    const r = rect.get(e);
    const formas = e.querySelectorAll('*');
    if (formas.length > 150) {   // retícula: vira imagem
      // cor por variável CSS (fill="var(--x)") não existe na página do raster: troca pela cor calculada
      const html = e.outerHTML.replace(/var\(--[\w-]+\)/g, getComputedStyle(e).fill);
      const id = novoRaster(r.width, r.height, html);
      return { k: 'i', src: 'raster:' + id, x: R(r.left - base.left), y: R(r.top - base.top), w: R(r.width), h: R(r.height), n: 'retícula' };
    }
    const cl = e.cloneNode(true);
    const orig = [e, ...formas], cop = [cl, ...cl.querySelectorAll('*')];
    orig.forEach((o, i) => { const cs = getComputedStyle(o); const c = cop[i];
      for (const p of ['fill', 'stroke', 'stroke-width', 'stroke-linejoin', 'stroke-linecap']) { const v = cs.getPropertyValue(p); if (v && v !== 'none' || p === 'fill') c.setAttribute(p, v); }
      c.removeAttribute('class'); c.removeAttribute('style'); });
    cl.setAttribute('xmlns', 'http://www.w3.org/2000/svg'); cl.setAttribute('width', r.width); cl.setAttribute('height', r.height);
    if (!cl.getAttribute('viewBox')) cl.setAttribute('viewBox', `0 0 ${r.width} ${r.height}`);
    return { k: 's', svg: cl.outerHTML.replace(/\s+/g, ' '), x: R(r.left - base.left), y: R(r.top - base.top), w: R(r.width), h: R(r.height) };
  }

  function nome(e) {
    if (e.dataset.nome) return e.dataset.nome;
    const c = [...e.classList].join(' ');
    return c || e.tagName.toLowerCase();
  }

  // 2) percorre a árvore: caixas viram quadros; o resto é achatado no quadro mais próximo
  function andar(e, base, kids) {
    const cs = getComputedStyle(e);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    const r = rect.get(e); if (!r || (r.width === 0 && r.height === 0)) return;
    if (e.tagName === 'IMG') {
      const m = matriz(e);
      const n = { k: 'i', src: decodeURIComponent(e.getAttribute('src')).replace(/^img\//, ''), x: R(r.left - base.left), y: R(r.top - base.top), w: R(r.width), h: R(r.height), n: e.alt || e.getAttribute('src').replace(/^img\//, '') };
      if (m && m.flip) n.flip = 1;
      const sh = sombras(cs.filter.startsWith('drop-shadow') ? cs.filter.replace(/^drop-shadow\(/, '').replace(/\)$/, '') : null); if (sh) n.sh = sh;
      kids.push(n); return;
    }
    if (e.tagName.toLowerCase() === 'svg') { kids.push(svgDe(e, base)); return; }
    if (e.classList.contains('padrao') || e.classList.contains('grain')) {
      const id = novoRaster(r.width, r.height, `<div style="width:${r.width}px;height:${r.height}px;background:${cs.background}"></div>`);
      const n = { k: 'i', src: 'raster:' + id, x: R(r.left - base.left), y: R(r.top - base.top), w: R(r.width), h: R(r.height), n: e.classList.contains('grain') ? 'grão' : 'padrão' };
      if (+cs.opacity < 1) n.op = +cs.opacity;
      if (cs.mixBlendMode !== 'normal') n.bl = cs.mixBlendMode;
      kids.push(n); return;
    }
    const m = matriz(e);
    const fundo = cor(cs.backgroundColor);
    const bimg = cs.backgroundImage !== 'none' ? cs.backgroundImage : null;
    const borda = parseFloat(cs.borderTopWidth) > 0 && cs.borderTopStyle !== 'none' ? { w: parseFloat(cs.borderTopWidth), c: cor(cs.borderTopColor) } : null;
    const sombra = sombras(cs.boxShadow);
    const caixa = e.classList.contains('slide') || fundo || bimg || borda || sombra || cs.overflow === 'hidden' || m || +cs.opacity < 1 || cs.mixBlendMode !== 'normal';
    let alvo = kids, b = base;
    if (caixa) {
      const f = { k: 'f', n: nome(e), x: R(r.left - base.left), y: R(r.top - base.top), w: R(r.width), h: R(r.height), kids: [] };
      if (fundo) f.fill = fundo;
      const lim = (v) => { const n = parseFloat(v) || 0; const px = String(v).trim().endsWith('%') ? n / 100 * Math.min(r.width, r.height) : n; return Math.min(px, r.height / 2, r.width / 2); };
      const cantos = [cs.borderTopLeftRadius, cs.borderTopRightRadius, cs.borderBottomRightRadius, cs.borderBottomLeftRadius].map(lim);
      if (cantos.every((c) => c === cantos[0])) { if (cantos[0]) f.r = R(cantos[0]); }
      else f.rr = cantos.map(R);          // arco: topo redondo, base 22
      if (cs.overflow === 'hidden') f.clip = 1;
      if (borda && borda.c) f.st = borda;
      if (sombra) f.sh = sombra;
      if (+cs.opacity < 1) f.op = +cs.opacity;
      if (cs.mixBlendMode !== 'normal') f.bl = cs.mixBlendMode;
      if (m) f.m = [m.a, m.b, m.c, m.d];
      if (bimg) {
        const id = novoRaster(r.width, r.height, `<div style="width:${r.width}px;height:${r.height}px;background:${cs.background}"></div>`);
        f.kids.push({ k: 'i', src: 'raster:' + id, x: 0, y: 0, w: R(r.width), h: R(r.height), n: 'fundo' });
      }
      kids.push(f); alvo = f.kids; b = r;
    }
    if (temTextoDireto(e)) { const t = textoDe(e, cs, b); if (t) alvo.push(t); }
    // filhos, na ordem de empilhamento (z-index), mantendo a ordem do DOM entre iguais
    const filhos = [...e.children].map((c, i) => ({ c, i, z: parseInt(getComputedStyle(c).zIndex) || 0 })).sort((p, q) => p.z - q.z || p.i - q.i);
    for (const { c } of filhos) {
      const ccs = getComputedStyle(c);
      if (temTextoDireto(e) && inline(c, ccs)) continue;      // já entrou no texto
      andar(c, b, alvo);
    }
  }
  const cenas = [...document.querySelectorAll('section.slide')].map((s) => { const kids = []; andar(s, rect.get(s), kids); return kids[0]; });
  return { cenas, rasters };
});

for (const c of cenas) fs.writeFileSync(path.join(saida, `cena-${c.n}.json`), JSON.stringify(c));
const rp = await browser.newPage({ deviceScaleFactor: 1 });
for (const r of rasters) {
  await rp.setViewportSize({ width: Math.max(1, r.w), height: Math.max(1, r.h) });
  await rp.setContent(`<html><body style="margin:0;background:transparent">${r.html}</body></html>`);
  await rp.screenshot({ path: path.join(saida, 'rasters', r.id + '.png'), omitBackground: true, clip: { x: 0, y: 0, width: Math.max(1, r.w), height: Math.max(1, r.h) } });
}
console.log(cenas.map((c) => `${c.n}: ${JSON.stringify(c).length} bytes`).join('\n'));
console.log('rasters', rasters.length);
await browser.close();
