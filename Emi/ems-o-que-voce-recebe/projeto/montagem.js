// Montagem comum: estrelas em retícula, acabamento de papel e grão, matéria por lâmina, texto na pauta.
// window.ESTRELAS = [[x global, y, raio, cor, opacidade, giro], ...] definido antes deste script.
const COR = { ivory: '#fffbde', manteiga: '#f2cf7a', lavanda: '#c0a5c4', violeta2: '#7b4df2', violeta: '#6225d8', plum: '#5b216c' };
// estrela em retícula (HalftoneStar) atravessando cada corte: x global, y, raio, cor, opacidade, giro
const ESTRELAS = window.ESTRELAS || [];
function estrela(cx, cy, R, cor, op, rot) {
  const pts = [];
  for (let i = 0; i < 10; i++) { const a = (Math.PI / 5) * i - Math.PI / 2 + (rot * Math.PI) / 180, r = i % 2 ? R * 0.46 : R; pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
  const dentro = (x, y) => { let d = false; for (let i = 0, j = 9; i < 10; j = i++) { const [xi, yi] = pts[i], [xj, yj] = pts[j]; if (yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) d = !d; } return d; };
  const passo = Math.max(9, R / 26); let s = '';
  for (let y = cy - R, l = 0; y <= cy + R; y += passo, l++) for (let x = cx - R + (l % 2 ? passo / 2 : 0); x <= cx + R; x += passo) {
    if (!dentro(x, y)) continue;
    const d = Math.hypot(x - cx, y - cy) / R, r = passo * 0.5 * (1 - d * 0.82);
    if (r > 0.9) s += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r.toFixed(1)}"/>`;
  }
  return `<svg class="ht"><g fill="${COR[cor]}" opacity="${op}">${s}</g></svg>`;
}
const laminas = [...document.querySelectorAll('.l')];
for (const [gx, y, R, cor, op, rot] of ESTRELAS)
  for (const k of [Math.floor((gx - 1) / 1080), Math.floor(gx / 1080)]) if (laminas[k]) laminas[k].insertAdjacentHTML('afterbegin', estrela(gx - k * 1080, y, R, cor, op, rot));
// acabamento contínuo: relevo de papel (soft-light) + grão de impressão (overlay); e uma matéria por lâmina
{
  const uri = (svg) => `url("data:image/svg+xml;utf8,${svg}")`;
  const grao = uri(`<svg xmlns='http://www.w3.org/2000/svg' width='360' height='360'><filter id='g' color-interpolation-filters='sRGB'><feTurbulence type='fractalNoise' baseFrequency='.82' numOctaves='2' seed='21' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/><feComponentTransfer><feFuncR type='linear' slope='2.6' intercept='-.8'/><feFuncG type='linear' slope='2.6' intercept='-.8'/><feFuncB type='linear' slope='2.6' intercept='-.8'/></feComponentTransfer></filter><rect width='100%' height='100%' filter='url(%23g)'/></svg>`);
  const papel = uri(`<svg xmlns='http://www.w3.org/2000/svg' width='800' height='800'><filter id='p' color-interpolation-filters='sRGB'><feTurbulence type='fractalNoise' baseFrequency='.028' numOctaves='5' seed='31' stitchTiles='stitch'/><feDiffuseLighting lighting-color='white' surfaceScale='3.2'><feDistantLight azimuth='225' elevation='30'/></feDiffuseLighting></filter><rect width='100%' height='100%' filter='url(%23p)'/></svg>`);
  const fibras = uri(`<svg xmlns='http://www.w3.org/2000/svg' width='500' height='500'><filter id='f' color-interpolation-filters='sRGB'><feTurbulence type='fractalNoise' baseFrequency='0.6 0.05' numOctaves='2' seed='8' stitchTiles='stitch'/><feDiffuseLighting lighting-color='white' surfaceScale='1.6'><feDistantLight azimuth='225' elevation='30'/></feDiffuseLighting></filter><rect width='100%' height='100%' filter='url(%23f)'/></svg>`);
  const r = document.documentElement.style;
  r.setProperty('--tx-grao', grao); r.setProperty('--tx-papel', papel); r.setProperty('--tx-fibras', fibras);
  laminas.forEach((l) => l.insertAdjacentHTML('beforeend', '<i class="materia"></i>'));
}
if (new URLSearchParams(location.search).has('guia')) document.body.classList.add('guia');
Promise.all([document.fonts.ready, ...[...document.images].map((i) => i.decode().catch(() => 0))]).then(() => {
  // texto sentado na pauta: a linha de base de cada [data-base] cai no y pedido
  for (const el of document.querySelectorAll('[data-base]')) {
    const m = document.createElement('i'); m.style.cssText = 'display:inline-block;width:0;height:0';
    el.prepend(m); el.style.top = '0px';
    const base = m.getBoundingClientRect().top - el.closest('.l').getBoundingClientRect().top;
    el.style.top = (+el.dataset.base - base) + 'px'; m.remove();
  }
  window.READY = true;
});
