// Cena do carrossel "Estrela das águas": um lago amazônico à noite, visto de cima,
// em papel recortado. As 7 lâminas são janelas de uma única faixa contínua (7 × 1080 px),
// então folhas e ondas atravessam de uma lâmina para a outra quando se arrasta o carrossel.
// buildScene(t) devolve o SVG da faixa inteira no instante t (segundos); a capa animada
// usa o mesmo desenho, só que recortado na primeira lâmina e redesenhado quadro a quadro.

export const W = 1080;
export const H = 1350;
export const N = 7;
export const LOOP = 10; // duração do loop da capa, em segundos

export const COR = {
  noite0: '#06171E',
  noite1: '#0B2830',
  noite2: '#113843',
  creme: '#FFF6E0',
  lua: '#F7ECCB',
  folha: '#5C8E2E',
  folhaClara: '#86B443',
  folhaEscura: '#3F6A1F',
  veia: '#3B621C',
  bordaVerde: '#A8CC60',
  vermelho: '#A03B2C',
  vermelhoClaro: '#C9593F',
  vermelhoEscuro: '#5E1A17',
  branco: '#F8F2E2',
  rosa: '#F28DA8',
  rosaFundo: '#C9406E',
  miolo: '#F2C35A',
  mata0: '#0C3326',
  mata1: '#174A30',
  mata2: '#25603A',
  mata3: '#3A7A3F',
  tinta: '#2A1A10',
  papel: '#F1E6CC',
};

const f = (n) => (Math.round(n * 10) / 10).toString();
const rad = (a) => (a * Math.PI) / 180;
const P = (r, a) => [r * Math.cos(rad(a)), r * Math.sin(rad(a))];
const TAU = Math.PI * 2;

function rng(seed) {
  let s = seed >>> 0;
  return () => {
    s = (s + 0x6d2b79f5) >>> 0;
    let x = s;
    x = Math.imul(x ^ (x >>> 15), x | 1);
    x ^= x + Math.imul(x ^ (x >>> 7), x | 61);
    return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
  };
}

function mix(a, b, k) {
  const pa = [1, 3, 5].map((i) => parseInt(a.slice(i, i + 2), 16));
  const pb = [1, 3, 5].map((i) => parseInt(b.slice(i, i + 2), 16));
  return '#' + pa.map((v, i) => Math.round(v + (pb[i] - v) * k).toString(16).padStart(2, '0')).join('');
}

let uid = 0;
const id = (p) => `${p}${++uid}`;

// ---------------------------------------------------------------- defs
function defs() {
  return `<defs>
  <linearGradient id="gAgua" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="${COR.noite0}"/><stop offset=".55" stop-color="${COR.noite1}"/><stop offset="1" stop-color="${COR.noite2}"/>
  </linearGradient>
  <radialGradient id="gFolha" cx=".42" cy=".38" r=".7">
    <stop offset="0" stop-color="${COR.folhaClara}"/><stop offset=".7" stop-color="${COR.folha}"/><stop offset="1" stop-color="${COR.folhaEscura}"/>
  </radialGradient>
  <radialGradient id="gBorda" r=".5">
    <stop offset=".9" stop-color="${COR.vermelhoClaro}"/><stop offset="1" stop-color="${COR.vermelho}"/>
  </radialGradient>
  <radialGradient id="gAvesso" cx=".45" cy=".42" r=".65">
    <stop offset="0" stop-color="#7E2620"/><stop offset="1" stop-color="${COR.vermelhoEscuro}"/>
  </radialGradient>
  <radialGradient id="gHalo" r=".5">
    <stop offset="0" stop-color="${COR.lua}" stop-opacity=".34"/><stop offset=".45" stop-color="${COR.lua}" stop-opacity=".12"/><stop offset="1" stop-color="${COR.lua}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="gVaga" r=".5">
    <stop offset="0" stop-color="#FFF3B0" stop-opacity="1"/><stop offset=".25" stop-color="#F7E27A" stop-opacity=".7"/><stop offset="1" stop-color="#F7E27A" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="gPapel" cx=".4" cy=".35" r=".85">
    <stop offset="0" stop-color="#F7EED8"/><stop offset="1" stop-color="#E4D3AE"/>
  </radialGradient>
  <filter id="sombra" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="0" dy="12" stdDeviation="14" flood-color="#010A0E" flood-opacity=".6"/>
  </filter>
  <filter id="sombraP" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#06140c" flood-opacity=".45"/>
  </filter>
  <filter id="desfoque" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7"/></filter>
  <filter id="brilho" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3"/></filter>
  <filter id="grao" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="7" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 .5  0 0 0 0 .45  0 0 0 0 .38  0 0 0 1.1 -.35"/>
  </filter>
  <filter id="fibra" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".012 .06" numOctaves="3" seed="3"/>
    <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 .9  0 0 0 .5 -.18"/>
  </filter>
  <pattern id="hachura" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
    <line x1="0" y1="0" x2="0" y2="7" stroke="${COR.tinta}" stroke-width="1.3"/>
  </pattern>
  <pattern id="hachuraX" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)">
    <line x1="0" y1="0" x2="0" y2="7" stroke="${COR.tinta}" stroke-width="1.1"/>
  </pattern>
</defs>`;
}

// ---------------------------------------------------------------- água
function agua(width) {
  const r = rng(11);
  let correntes = '';
  for (let i = 0; i < 46; i++) {
    const x = r() * width;
    const y = r() * H;
    const L = 120 + r() * 360;
    const a = 6 * (r() - 0.5);
    correntes += `<path d="M${f(x)} ${f(y)} q ${f(L / 4)} ${f(-8 - r() * 8)} ${f(L / 2)} 0 t ${f(L / 2)} 0" transform="rotate(${f(a)} ${f(x)} ${f(y)})" fill="none" stroke="#5FA3A6" stroke-opacity="${f(0.05 + r() * 0.06)}" stroke-width="${f(1.5 + r() * 2)}" stroke-linecap="round"/>`;
  }
  return `<rect width="${width}" height="${H}" fill="url(#gAgua)"/>${correntes}`;
}

// ---------------------------------------------------------------- vitória-régia (de cima)
// Borda virada para cima (avesso vermelho aparecendo por fora), faixa verde-clara da parede
// da borda, superfície com nervuras radiais e células "acolchoadas" e a fenda de escoamento.
export function folha({ x, y, r, rot = 0, fenda = 40, nerv = 20, seed = 1, sombra = true }) {
  const rr = rng(seed);
  const clip = id('cf');
  const angs = Array.from({ length: nerv }, (_, i) => (i * 360) / nerv + (rr() - 0.5) * 6);
  let veias = '';
  for (const a of angs) {
    const [x1, y1] = P(r * 0.07, a);
    const [x2, y2] = P(r * 0.9, a);
    veias += `<line x1="${f(x1)}" y1="${f(y1)}" x2="${f(x2)}" y2="${f(y2)}"/>`;
  }
  const aneis = [0.24, 0.39, 0.52, 0.64, 0.75, 0.85];
  for (const k of aneis) {
    let d = '';
    for (let i = 0; i < nerv; i++) {
      const a1 = angs[i];
      const a2 = angs[(i + 1) % nerv] + (i + 1 === nerv ? 360 : 0);
      const [x1, y1] = P(r * k, a1);
      const [x2, y2] = P(r * k, a2);
      const [cx, cy] = P(r * k * 0.9, (a1 + a2) / 2);
      d += `M${f(x1)} ${f(y1)}Q${f(cx)} ${f(cy)} ${f(x2)} ${f(y2)}`;
    }
    veias += `<path d="${d}"/>`;
  }
  const [n1x, n1y] = P(r * 1.02, fenda - 3.2);
  const [n2x, n2y] = P(r * 1.02, fenda + 3.2);
  const [n3x, n3y] = P(r * 0.88, fenda);
  return `<g transform="translate(${f(x)} ${f(y)}) rotate(${f(rot)})"${sombra ? ' filter="url(#sombra)"' : ''}>
    <circle r="${f(r)}" fill="url(#gBorda)"/>
    <circle r="${f(r * 0.955)}" fill="${COR.bordaVerde}"/>
    <clipPath id="${clip}"><circle r="${f(r * 0.915)}"/></clipPath>
    <g clip-path="url(#${clip})">
      <circle r="${f(r * 0.915)}" fill="url(#gFolha)"/>
      <g stroke="${COR.veia}" stroke-opacity=".55" stroke-width="${f(Math.max(1.2, r * 0.009))}" fill="none" stroke-linecap="round">${veias}</g>
      <circle r="${f(r * 0.93)}" fill="none" stroke="#17300a" stroke-opacity=".5" stroke-width="${f(r * 0.07)}" filter="url(#desfoque)"/>
    </g>
    <circle r="${f(r * 0.045)}" fill="${COR.folhaEscura}" opacity=".7"/>
    <path d="M${f(n3x)} ${f(n3y)}L${f(n1x)} ${f(n1y)}L${f(n2x)} ${f(n2y)}Z" fill="${COR.noite1}"/>
  </g>`;
}

// avesso da folha: nervuras grossas que funcionam como vigas (a "engenharia")
export function avesso({ x, y, r, rot = 0, nerv = 16, seed = 5 }) {
  const rr = rng(seed);
  let vigas = '';
  let cruz = '';
  let espinhos = '';
  const angs = Array.from({ length: nerv }, (_, i) => (i * 360) / nerv + (rr() - 0.5) * 4);
  for (const a of angs) {
    const w0 = r * 0.05;
    const [ax, ay] = P(r * 0.06, a - 90);
    const pts = [P(r * 0.08, a), P(r * 0.93, a)];
    const [p0, p1] = pts;
    const [nx, ny] = P(1, a + 90);
    vigas += `<path d="M${f(p0[0] + nx * w0)} ${f(p0[1] + ny * w0)}L${f(p1[0] + nx * 3)} ${f(p1[1] + ny * 3)}L${f(p1[0] - nx * 3)} ${f(p1[1] - ny * 3)}L${f(p0[0] - nx * w0)} ${f(p0[1] - ny * w0)}Z"/>`;
    for (let k = 0.18; k < 0.9; k += 0.085) {
      const [sx, sy] = P(r * k, a);
      espinhos += `<circle cx="${f(sx + nx * w0 * (1 - k) * 0.9)}" cy="${f(sy + ny * w0 * (1 - k) * 0.9)}" r="2.2"/><circle cx="${f(sx - nx * w0 * (1 - k) * 0.9)}" cy="${f(sy - ny * w0 * (1 - k) * 0.9)}" r="2.2"/>`;
    }
    void ax; void ay;
  }
  for (const k of [0.3, 0.45, 0.6, 0.74, 0.86]) {
    let d = '';
    for (let i = 0; i < nerv; i++) {
      const a1 = angs[i];
      const a2 = angs[(i + 1) % nerv] + (i + 1 === nerv ? 360 : 0);
      const [x1, y1] = P(r * k, a1);
      const [x2, y2] = P(r * k, a2);
      const [cx, cy] = P(r * k * 1.04, (a1 + a2) / 2);
      d += `M${f(x1)} ${f(y1)}Q${f(cx)} ${f(cy)} ${f(x2)} ${f(y2)}`;
    }
    cruz += `<path d="${d}"/>`;
  }
  return `<g transform="translate(${f(x)} ${f(y)}) rotate(${f(rot)})" filter="url(#sombra)">
    <circle r="${f(r)}" fill="${COR.vermelhoEscuro}"/>
    <circle r="${f(r * 0.97)}" fill="url(#gAvesso)"/>
    <g fill="none" stroke="#B4483A" stroke-opacity=".75" stroke-width="${f(r * 0.012)}">${cruz}</g>
    <g fill="${COR.vermelhoClaro}" filter="url(#sombraP)">${vigas}</g>
    <g fill="#F2B3A0" opacity=".8">${espinhos}</g>
    <circle r="${f(r * 0.1)}" fill="${COR.vermelhoClaro}" filter="url(#sombraP)"/>
    <circle r="${f(r * 0.05)}" fill="#7E2620"/>
  </g>`;
}

// ---------------------------------------------------------------- flor (de cima)
// abre = 0 (botão) .. 1 (aberta); rosa = 0 (branca, 1ª noite) .. 1 (rosa, 2ª noite)
function petala(L, w) {
  return `M0 0C${f(w)} ${f(-L * 0.28)} ${f(w * 0.72)} ${f(-L * 0.86)} 0 ${f(-L)}C${f(-w * 0.72)} ${f(-L * 0.86)} ${f(-w)} ${f(-L * 0.28)} 0 0Z`;
}

export function flor({ x, y, s, abre = 1, rosa = 0, rot = 0, sombra = true, espinho = true }) {
  const camadas = [
    { n: 4, L: 1.0, w: 0.2, cor: '#6E2A22', off: 45, sep: true },
    { n: 13, L: 0.62 + 0.38 * abre, w: 0.21, cor: mix(COR.branco, COR.rosa, rosa * 0.8), off: 0 },
    { n: 12, L: 0.5 + 0.3 * abre, w: 0.19, cor: mix('#FBF6EA', mix(COR.rosa, COR.rosaFundo, 0.4), rosa), off: 14 },
    { n: 10, L: 0.36 + 0.16 * abre, w: 0.16, cor: mix('#FFFAF0', COR.rosaFundo, rosa), off: 5 },
  ];
  let g = `<g transform="translate(${f(x)} ${f(y)}) rotate(${f(rot)})"${sombra ? ' filter="url(#sombra)"' : ''}>`;
  for (const c of camadas) {
    if (c.sep && abre < 0.35) continue;
    const L = s * c.L;
    const w = s * c.w;
    let pet = '';
    let veio = '';
    for (let i = 0; i < c.n; i++) {
      const a = (i * 360) / c.n + c.off;
      pet += `<path d="${petala(L, w)}" transform="rotate(${f(a)})"/>`;
      if (!c.sep) veio += `<line x1="0" y1="${f(-L * 0.25)}" x2="0" y2="${f(-L * 0.85)}" transform="rotate(${f(a)})"/>`;
      else if (espinho) {
        for (let k = 0.3; k < 0.95; k += 0.12) veio += `<circle cx="0" cy="${f(-L * k)}" r="1.6" transform="rotate(${f(a)})"/>`;
      }
    }
    g += `<g filter="url(#sombraP)"><g fill="${c.cor}">${pet}</g>`;
    g += c.sep
      ? `<g fill="#E9A48C" opacity=".8">${veio}</g></g>`
      : `<g stroke="#000" stroke-opacity=".07" stroke-width="${f(Math.max(1, s * 0.012))}">${veio}</g></g>`;
  }
  const rm = s * 0.17;
  let estames = '';
  for (let i = 0; i < 22; i++) {
    const [ex, ey] = P(rm * 0.78, i * (360 / 22));
    estames += `<circle cx="${f(ex)}" cy="${f(ey)}" r="${f(s * 0.022)}"/>`;
  }
  g += `<circle r="${f(rm)}" fill="${COR.miolo}" filter="url(#sombraP)"/>
    <circle r="${f(rm * 0.55)}" fill="#E0A23E"/>
    <g fill="#FCE3A0">${estames}</g></g>`;
  return g;
}

// ---------------------------------------------------------------- lua refletida
function lua({ x, y, r, t = 0, halo = true }) {
  const clip = id('cl');
  let cortes = '';
  const rr = rng(23);
  for (let i = 0; i < 9; i++) {
    const yy = -r + (i + 0.6) * ((2 * r) / 9) + (rr() - 0.5) * 6;
    const fase = rr() * TAU;
    const dx = Math.sin(t * (TAU / LOOP) * (i % 2 ? 1 : 2) + fase) * r * 0.12;
    const L = r * (0.5 + rr() * 0.9);
    const x0 = -r * 1.1 + rr() * r * 1.4 + dx;
    cortes += `<path d="M${f(x0)} ${f(yy)}q ${f(L / 4)} -4 ${f(L / 2)} 0 t ${f(L / 2)} 0" stroke-width="${f(3 + rr() * 5)}"/>`;
  }
  return `<g transform="translate(${f(x)} ${f(y)})">
    ${halo ? `<circle r="${f(r * 3)}" fill="url(#gHalo)"/>` : ''}
    <clipPath id="${clip}"><circle r="${f(r)}"/></clipPath>
    <circle r="${f(r)}" fill="${COR.lua}"/>
    <g clip-path="url(#${clip})" fill="none" stroke="${COR.noite1}" stroke-opacity=".75" stroke-linecap="round">${cortes}</g>
  </g>`;
}

// ondas concêntricas que nascem do centro e somem (fase cíclica: fecha o loop)
function ondas({ x, y, rMax, t = 0, n = 4, periodo = LOOP / 2, op = 0.3, larg = 2 }) {
  let g = '';
  for (let k = 0; k < n; k++) {
    const fase = (t / periodo + k / n) % 1;
    const r = 20 + rMax * fase;
    const o = op * Math.sin(Math.PI * fase);
    g += `<circle cx="${f(x)}" cy="${f(y)}" r="${f(r)}" fill="none" stroke="${COR.lua}" stroke-opacity="${f(o * 100) / 100}" stroke-width="${larg}"/>`;
  }
  return g;
}

// ---------------------------------------------------------------- mata (moldura em papel)
function lanca({ x, y, L, w, rot, cor, veia = true }) {
  return `<g transform="translate(${f(x)} ${f(y)}) rotate(${f(rot)})" filter="url(#sombra)">
    <path d="M0 0C${f(w)} ${f(-L * 0.2)} ${f(w * 0.9)} ${f(-L * 0.75)} 0 ${f(-L)}C${f(-w * 0.9)} ${f(-L * 0.75)} ${f(-w)} ${f(-L * 0.2)} 0 0Z" fill="${cor}"/>
    ${veia ? `<path d="M0 -4L0 ${f(-L * 0.92)}" stroke="#000" stroke-opacity=".18" stroke-width="3"/>` : ''}
  </g>`;
}

function fronde({ x, y, L, rot, cor, n = 16, curva = 0.18, lado = 1 }) {
  // palmeira (açaí): ráquis curva com folíolos finos dos dois lados
  let fol = '';
  const pts = [];
  for (let i = 0; i <= n; i++) {
    const k = i / n;
    pts.push([lado * Math.sin(k * 1.4) * L * curva, -k * L]);
  }
  for (let i = 1; i < n; i++) {
    const [px, py] = pts[i];
    const k = i / n;
    const fl = L * (0.34 - 0.22 * k);
    for (const s of [-1, 1]) {
      const a = s * (58 - 18 * k);
      fol += `<path d="M0 0C${f(fl * 0.05)} ${f(-fl * 0.3)} ${f(fl * 0.04)} ${f(-fl * 0.8)} 0 ${f(-fl)}C${f(-fl * 0.04)} ${f(-fl * 0.8)} ${f(-fl * 0.06)} ${f(-fl * 0.3)} 0 0Z" transform="translate(${f(px)} ${f(py)}) rotate(${f(a + lado * 6)}) scale(${f(1 + 0.6 * (1 - k))} 1)"/>`;
    }
  }
  const d = 'M' + pts.map((p) => `${f(p[0])} ${f(p[1])}`).join('L');
  return `<g transform="translate(${f(x)} ${f(y)}) rotate(${f(rot)})" filter="url(#sombra)">
    <g fill="${cor}">${fol}</g><path d="${d}" stroke="${cor}" stroke-width="5" fill="none" stroke-linecap="round"/>
  </g>`;
}

// ---------------------------------------------------------------- vida
function vagalumes({ x0, x1, y0, y1, n, t = 0, seed = 3 }) {
  const r = rng(seed);
  let g = '';
  for (let i = 0; i < n; i++) {
    const bx = x0 + r() * (x1 - x0);
    const by = y0 + r() * (y1 - y0);
    const fa = r() * TAU;
    const w = TAU / LOOP;
    const x = bx + Math.sin(t * w + fa) * 18;
    const y = by + Math.cos(t * w * 2 + fa) * 12;
    const pisca = 0.35 + 0.65 * Math.max(0, Math.sin(t * w * 3 + fa * 2));
    const tam = 2 + r() * 2.5;
    g += `<circle cx="${f(x)}" cy="${f(y)}" r="${f(tam * 6)}" fill="url(#gVaga)" opacity="${f(pisca * 0.55 * 100) / 100}"/><circle cx="${f(x)}" cy="${f(y)}" r="${f(tam)}" fill="#FFF7C2" opacity="${f(pisca * 100) / 100}"/>`;
  }
  return g;
}

// besouro polinizador (Cyclocephala), que passa a noite dentro da flor
function besouro({ x, y, rot = 0, s = 1, t = 0 }) {
  const p = Math.sin(t * 14) * 10;
  let pernas = '';
  for (const [yy, a] of [[-4, 35], [3, 0], [10, -30]]) {
    pernas += `<path d="M0 ${yy}l12 ${f(-a / 6 + p / 8)}l6 ${f(4 - p / 10)}"/><path d="M0 ${yy}l-12 ${f(-a / 6 - p / 8)}l-6 ${f(4 + p / 10)}"/>`;
  }
  return `<g transform="translate(${f(x)} ${f(y)}) rotate(${f(rot)}) scale(${s})" filter="url(#sombraP)">
    <g stroke="#2B1608" stroke-width="2.2" fill="none" stroke-linecap="round">${pernas}</g>
    <ellipse cx="0" cy="-15" rx="6.5" ry="5" fill="#3A2210"/>
    <ellipse cx="0" cy="3" rx="11" ry="15" fill="#B9822F"/>
    <path d="M0 -11V18" stroke="#6A4317" stroke-width="1.6"/>
    <ellipse cx="-4" cy="-3" rx="3" ry="6" fill="#E4B565" opacity=".6"/>
  </g>`;
}

// ---------------------------------------------------------------- herbário (século XIX)
// prancha botânica em papel creme, desenhada a traço, com o lacre real da Rainha Vitória
function prancha({ x, y, w, h, rot }) {
  const cx = w / 2;
  const fy = h * 0.4;
  // flor em vista lateral, a traço
  let flor = '';
  const pet = (ang, L, larg) => `<path d="M0 0C${f(larg)} ${f(-L * 0.3)} ${f(larg * 0.7)} ${f(-L * 0.85)} 0 ${f(-L)}C${f(-larg * 0.7)} ${f(-L * 0.85)} ${f(-larg)} ${f(-L * 0.3)} 0 0Z" transform="rotate(${f(ang)})"/>`;
  for (const a of [-78, -62, -46, -30, 30, 46, 62, 78]) flor += pet(a, 150, 30);
  let miolo = '';
  for (const a of [-16, -6, 4, 14]) miolo += pet(a, 120, 24);
  // folha em perfil, mostrando a borda virada
  const fol = `<path d="M${f(cx - 240)} ${f(h * 0.74)}Q${f(cx - 250)} ${f(h * 0.66)} ${f(cx - 232)} ${f(h * 0.66)}L${f(cx + 232)} ${f(h * 0.66)}Q${f(cx + 250)} ${f(h * 0.66)} ${f(cx + 240)} ${f(h * 0.74)}Q${f(cx)} ${f(h * 0.8)} ${f(cx - 240)} ${f(h * 0.74)}Z"/>`;
  let costelas = '';
  for (let i = -6; i <= 6; i++) costelas += `<path d="M${f(cx)} ${f(h * 0.79)}Q${f(cx + i * 22)} ${f(h * 0.78)} ${f(cx + i * 36)} ${f(h * 0.745)}"/>`;
  let haste = `<path d="M${f(cx)} ${f(fy + 8)}C${f(cx + 6)} ${f(h * 0.55)} ${f(cx - 8)} ${f(h * 0.62)} ${f(cx)} ${f(h * 0.67)}" />`;
  return `<g transform="translate(${f(x)} ${f(y)}) rotate(${f(rot)})" filter="url(#sombra)">
    <rect width="${w}" height="${h}" fill="url(#gPapel)"/>
    <rect width="${w}" height="${h}" filter="url(#fibra)" opacity=".5"/>
    <rect x="22" y="22" width="${w - 44}" height="${h - 44}" fill="none" stroke="${COR.tinta}" stroke-opacity=".55" stroke-width="1.4"/>
    <rect x="30" y="30" width="${w - 60}" height="${h - 60}" fill="none" stroke="${COR.tinta}" stroke-opacity=".35" stroke-width=".8"/>
    <g fill="none" stroke="${COR.tinta}" stroke-width="2" stroke-linecap="round">${haste}</g>
    <g transform="translate(${f(cx)} ${f(fy)})">
      <g fill="url(#hachura)" stroke="${COR.tinta}" stroke-width="2" opacity=".85">${flor}</g>
      <g fill="#F4EBD3" stroke="${COR.tinta}" stroke-width="2">${miolo}</g>
      <g fill="url(#hachuraX)" opacity=".35">${miolo}</g>
      <ellipse cx="0" cy="4" rx="40" ry="12" fill="#F4EBD3" stroke="${COR.tinta}" stroke-width="2"/>
    </g>
    <g stroke="${COR.tinta}" stroke-width="2" fill="url(#hachura)">${fol}</g>
    <g stroke="${COR.tinta}" stroke-width="1.2" fill="none" opacity=".8">${costelas}</g>
    <path d="M${f(cx - 150)} ${f(h * 0.885)}H${f(cx + 150)}M${f(cx - 110)} ${f(h * 0.905)}H${f(cx + 110)}" stroke="${COR.tinta}" stroke-opacity=".4" stroke-width="2"/>
    <g transform="translate(${f(w - 70)} ${f(h - 78)}) rotate(-12)">
      <circle r="44" fill="#9B2420"/><circle r="44" fill="none" stroke="#6A1414" stroke-width="5" stroke-dasharray="6 5"/>
      <circle r="33" fill="none" stroke="#C9473F" stroke-width="2"/>
      <path d="M-20 10L-23 -12L-10 -2L0 -18L10 -2L23 -12L20 10Z" fill="#E8B04A"/><rect x="-20" y="12" width="40" height="6" fill="#E8B04A"/>
    </g>
    <rect x="${f(w * 0.32)}" y="-14" width="110" height="34" fill="#E9DDBB" opacity=".75" transform="rotate(-4 ${f(w * 0.32)} -14)"/>
  </g>`;
}

// cota técnica (diâmetro) sem número: só o gesto de medir
function cota({ x1, y1, x2, y2 }) {
  const a = (Math.atan2(y2 - y1, x2 - x1) * 180) / Math.PI;
  return `<g stroke="${COR.creme}" stroke-width="2" fill="none" opacity=".85">
    <line x1="${f(x1)}" y1="${f(y1)}" x2="${f(x2)}" y2="${f(y2)}" stroke-dasharray="2 10" stroke-linecap="round"/>
    <g transform="translate(${f(x1)} ${f(y1)}) rotate(${f(a)})"><path d="M0 -18V18M0 0l16 -9M0 0l16 9"/></g>
    <g transform="translate(${f(x2)} ${f(y2)}) rotate(${f(a + 180)})"><path d="M0 -18V18M0 0l16 -9M0 0l16 9"/></g>
  </g>`;
}

// ---------------------------------------------------------------- composição
// rosa da flor da capa: vai do branco ao rosa e volta, num ciclo que fecha o loop
export const rosaCapa = (t) => (1 - Math.cos((TAU * t) / LOOP)) / 2;

export function buildScene(t = 0, { estatico = false } = {}) {
  uid = 0;
  const X = (k) => k * W;
  const w = TAU / LOOP;
  const bal = (amp, fase = 0, mult = 1) => Math.sin(t * w * mult + fase) * amp;
  const pinkCapa = estatico ? 0.08 : rosaCapa(t);
  const L = [];

  L.push(agua(W * N));

  // ---- lâmina 1: capa
  L.push(lua({ x: X(0) + 760, y: 930, r: 120, t }));
  L.push(ondas({ x: X(0) + 700, y: 950, rMax: 420, t, n: 4, op: 0.28 }));
  L.push(folha({ x: X(0) + 190 + bal(4), y: 1150 + bal(3, 1), r: 300, rot: 20 + bal(1.2, 2), fenda: 300, seed: 2 }));
  L.push(folha({ x: X(0) + 1130 + bal(3, 2), y: 1240, r: 250, rot: -30 + bal(1, 1), fenda: 200, seed: 3 }));
  L.push(folha({ x: X(0) + 950 + bal(3, 4), y: 640 + bal(3, 2), r: 120, rot: 60, fenda: 110, seed: 4 }));
  L.push(flor({ x: X(0) + 700, y: 950, s: 168 * (0.97 + 0.03 * Math.sin(t * w)), abre: 0.92 + 0.08 * Math.sin(t * w), rosa: pinkCapa, rot: bal(3) }));
  L.push(flor({ x: X(0) + 470 + bal(2, 1), y: 1250, s: 54, abre: 0.1, rot: 20 }));
  {
    // besouro dá a volta na borda da folha da capa
    const a = (t / LOOP) * 360 + 200;
    const [bx, by] = P(300 * 0.8, a);
    L.push(besouro({ x: X(0) + 190 + bx, y: 1150 + by, rot: a + 180, s: 1.1, t }));
  }
  L.push(fronde({ x: X(0) + 1150, y: -60, L: 520, rot: 210 + bal(2.5, 0), cor: COR.mata1, lado: -1 }));
  L.push(fronde({ x: X(0) + 1110, y: -80, L: 430, rot: 236 + bal(2, 1.3), cor: COR.mata2, lado: -1 }));
  L.push(lanca({ x: X(0) - 20, y: 1380, L: 330, w: 70, rot: 38 + bal(2, 0.5), cor: COR.mata2 }));
  L.push(lanca({ x: X(0) + 40, y: 1400, L: 260, w: 58, rot: 12 + bal(2, 2), cor: COR.mata3 }));

  // ---- lâmina 2: tamanho e nomes indígenas
  L.push(folha({ x: X(1) + 760, y: 930, r: 470, rot: 8, fenda: 160, seed: 6 }));
  L.push(flor({ x: X(1) + 330, y: 1290, s: 100, abre: 0.85, rosa: 0, rot: 12 }));
  L.push(ondas({ x: X(1) + 330, y: 1290, rMax: 260, t: 1.3, n: 3, op: 0.22 }));
  L.push(lanca({ x: X(1) + 1080, y: -40, L: 300, w: 64, rot: 200, cor: COR.mata1 }));

  // ---- lâmina 3: a lenda de Naiá e Jaci
  L.push(lua({ x: X(2) + 540, y: 690, r: 205, t: 2.1 }));
  L.push(ondas({ x: X(2) + 540, y: 690, rMax: 470, t: 0, n: 5, periodo: 1, op: 0.32, larg: 2.5 }));
  L.push(flor({ x: X(2) + 540, y: 690, s: 96, abre: 0.75, rosa: 0, rot: 8 }));
  L.push(vagalumes({ x0: X(2) + 80, x1: X(2) + 1000, y0: 420, y1: 1000, n: 16, t: 2.4, seed: 9 }));
  L.push(fronde({ x: X(2) - 40, y: 1420, L: 470, rot: 32, cor: COR.mata1 }));
  L.push(fronde({ x: X(2) + 1120, y: 1420, L: 440, rot: -36, cor: COR.mata2, lado: -1 }));

  // ---- lâmina 4: o século XIX
  L.push(folha({ x: X(3) - 60, y: 360, r: 230, rot: -12, fenda: 10, seed: 8 }));
  L.push(prancha({ x: X(3) + 250, y: 470, w: 600, h: 660, rot: -4 }));
  L.push(folha({ x: X(3) + 1010, y: 1240, r: 210, rot: 40, fenda: 220, seed: 10 }));

  // ---- lâmina 5: engenharia da natureza
  L.push(avesso({ x: X(4) + 690, y: 860, r: 340, rot: 8 }));
  L.push(cota({ x1: X(4) + 690 - 340, y1: 1235, x2: X(4) + 690 + 340, y2: 1235 }));
  L.push(flor({ x: X(4) + 150, y: 1070, s: 70, abre: 0.9, rosa: 0, rot: 4 }));
  L.push(flor({ x: X(4) + 150, y: 1240, s: 70, abre: 0.85, rosa: 1, rot: 14 }));
  L.push(besouro({ x: X(4) + 182, y: 1214, rot: -30, s: 0.8 }));

  // ---- lâmina 6: síntese
  L.push(folha({ x: X(5) + 100, y: 1260, r: 260, rot: 70, fenda: 300, seed: 12 }));
  L.push(folha({ x: X(5) + 1010, y: 1180, r: 230, rot: 150, fenda: 250, seed: 13 }));
  L.push(ondas({ x: X(5) + 540, y: 1140, rMax: 380, t: 3.2, n: 4, op: 0.24 }));
  L.push(flor({ x: X(5) + 540, y: 1140, s: 250, abre: 1, rosa: 0.72, rot: 6 }));
  L.push(vagalumes({ x0: X(5) + 80, x1: X(5) + 1000, y0: 760, y1: 960, n: 7, t: 4, seed: 15 }));

  // ---- lâmina 7: assinatura
  L.push(folha({ x: X(6) - 40, y: 160, r: 180, rot: 20, fenda: 30, seed: 16 }));
  L.push(lua({ x: X(6) + 860, y: 1150, r: 70, t: 5 }));
  L.push(folha({ x: X(6) + 520, y: 1520, r: 330, rot: 0, fenda: 270, seed: 17 }));
  L.push(flor({ x: X(6) + 860, y: 1150, s: 70, abre: 0.6, rosa: 0, rot: 30 }));

  // papel: grão por cima de tudo
  L.push(`<rect width="${W * N}" height="${H}" filter="url(#grao)" opacity=".22" style="mix-blend-mode:overlay"/>`);

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W * N}" height="${H}" viewBox="0 0 ${W * N} ${H}">${defs()}${L.join('\n')}</svg>`;
}
