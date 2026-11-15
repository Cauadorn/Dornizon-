// Logo MIAU.LAB, desenhado em qualquer caixa: miauLogo(el, { cor, gato, olho, olho2, contorno, pelo, lab, id }).
// A caixa tem 899 x 700 (unidades do logo): o nome começa em x=0, o topo das letras fica em y=260 e a base em y=587.
// Referências: ONCE, wllab e CURAME (nome gigante e condensado, etiqueta preta de laboratório) + o quadro gato-espiando.
// v2 (a Emi: "tá muito grande… tem algo que incomoda… vetorizado… no negativo fica tudo preto"):
//   - o gato encolheu para quase metade do tamanho: espia de dentro do U, com uma patinha em cada haste.
//     O nome manda; o gato é o detalhe (como no "meow gigante + gatinho", nº 1 do quadro);
//   - mais gráfico e menos adesivo: só a silhueta, olhos de gato (íris rosa, pupila em fenda) e patas com dedinhos,
//     com a cabeça levemente inclinada e uma orelha diferente da outra;
//   - contorno: respiro na cor do fundo entre o gato e as letras (versão negativa, tudo preto);
//   - pelo: borda irregular de tinta, para quem quiser menos "vetor".
// Topo das letras (Archivo 900, largura 62%, 470px): M 0-118 e 178-293 · I 331-416 · A 500-620 · U 697-782 e 814-899.
// Unhas brancas e arranhões finos descendo nas hastes do U (o.fundo = cor do fundo, para o recorte; o.unhas=false tira).
// A v1 (gato grande atrás do A) está em logo-v1-grande.js.
function miauLogo(el, o = {}) {
  const fundo = o.fundo || '#2F55F2';
  const cor = o.cor || '#FF9FD2', gato = o.gato || '#141418', olho = o.olho || '#FF9FD2', olho2 = o.olho2 || '#FFFFFF';
  const id = o.id || 'l', k = o.k || 0.56, cx = o.cx || 798, parede = 260, folga = o.contorno ? 6 : 0;
  // cabeça desenhada para 280 de largura; k escala; leve inclinação e orelha direita um pouco mais baixa e aberta
  const cabeca = 'M-140 60 L-140 -50 C-140 -96 -134 -150 -123 -194 Q-119 -212 -103 -203 C-82 -188 -60 -168 -45 -150 '
    + 'Q0 -161 45 -150 C62 -164 86 -180 110 -190 Q127 -197 128 -180 C135 -140 140 -96 140 -50 L140 60 Z';
  // olhos: íris redonda (rosa) com pupila de gato em fenda (a Emi não entendeu a cápsula)
  const olhoGato = (x, r) => `<g transform="translate(${x} -80) rotate(${r})"><circle r="30" fill="${olho}"/>`
    + `<path d="M0 -24 Q11 0 0 24 Q-11 0 0 -24 Z" fill="${gato}"/><circle cx="9" cy="-11" r="5" fill="${olho2}"/></g>`;
  const filtro = o.pelo ? `<filter id="pelo-${id}" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".07" numOctaves="2" seed="7"/>`
    + `<feDisplacementMap in="SourceGraphic" scale="${5 / k}" xChannelSelector="R" yChannelSelector="G"/></filter>` : '';
  const comPelo = o.pelo ? `filter="url(#pelo-${id})"` : '';
  // patas de gato: um desenho só, com curvas contínuas (sem bolinhas emendadas): o dorso da pata vem de trás,
  // três dedos dobram por cima da borda da letra (o do meio maior), vales suaves entre os dedos e um risquinho afinado em cada vale.
  // As duas patas giram um pouco para dentro, como quem segura a borda.
  const PATA = 'M-50 -2 C-50 -22 -30 -33 0 -33 C30 -33 50 -22 50 -2 C50 14 45 30 32 31 C25 32 20 29 17 24 '
    + 'C14 33 7 38 0 38 C-7 38 -14 33 -17 24 C-20 29 -25 32 -32 31 C-45 30 -50 14 -50 -2 Z';
  const RISCO = 'M17 25 Q15.4 19 15.6 12 Q17.6 18 18.8 24 Z';
  const pata = (x, lado, f, s) => `<g transform="translate(${x} 3) rotate(${lado * 7})">`
    + `<path d="${PATA}" fill="${f}" ${s ? `stroke="${s}" stroke-width="${9 / k}" stroke-linejoin="round"` : ''}/>`
    + (s ? '' : `<path d="${RISCO}" fill="${o.contorno || cor}"/><path d="${RISCO}" transform="scale(-1 1)" fill="${o.contorno || cor}"/>`) + '</g>';
  const patas = (f, s) => pata(-106, 1, f, s) + pata(106, -1, f, s);
  // unhas (a Emi: "rola de fazer as unhas do gatinho e um rastrinho delicado"): ganchinho branco na ponta de cada dedo
  // e, descendo da unha, um arranhão fino e afinado recortado na letra (na cor do fundo), cada um de um tamanho.
  const DEDOS = [[-27, 31], [0, 38], [27, 31]], UNHA = 'M-2.8 -3 C-3 5 -1 11 2.6 14.5 C0.8 9 1.6 3 2.6 -3 Z';
  const unhas = (x, lado) => `<g transform="translate(${x} 3) rotate(${lado * 7})">`
    + DEDOS.map(([dx, dy]) => `<path d="${UNHA}" transform="translate(${dx} ${dy - 3})" fill="${o.unha || '#FFFFFF'}"/>`).join('') + '</g>';
  const pontas = (x, lado) => DEDOS.map(([dx, dy]) => { const t = lado * 7 * Math.PI / 180, py = dy + 13;
    return [cx + k * (x + dx * Math.cos(t) - py * Math.sin(t)), parede + k * (3 + dx * Math.sin(t) + py * Math.cos(t))]; });
  const TAM = [[44, 60, 34], [38, 54, 28]];
  const rastros = [[-106, 1], [106, -1]].map(([x, lado], i) => pontas(x, lado).map(([sx, sy], j) => {
    const L = TAM[i][j], w = 1.25, d = (j - 1) * 1.6 + lado * -1.2;
    return `<path d="M${sx - w} ${sy} Q${sx - w * .6 + d * .4} ${sy + L * .55} ${sx + d} ${sy + L} Q${sx + w * .6 + d * .4} ${sy + L * .55} ${sx + w} ${sy} Z" fill="${fundo}"/>`; }).join('')).join('');

  el.style.position = el.style.position || 'absolute';
  el.innerHTML = `
  <svg width="899" height="700" viewBox="0 0 899 700" style="position:absolute;left:0;top:0;overflow:visible">
    <defs><clipPath id="acima-${id}"><rect x="-300" y="-400" width="1500" height="${660 - folga}"/></clipPath>${filtro}</defs>
    <g clip-path="url(#acima-${id})"><g transform="translate(${cx} ${parede}) scale(${k}) rotate(-5 0 -60)">
      <path fill="${gato}" d="${cabeca}" ${comPelo}/>
      ${olhoGato(-54, 4)}${olhoGato(54, -4)}
    </g></g>
  </svg>
  <div style="position:absolute;left:-19px;top:191px;font:900 470px/1 Archivo;font-stretch:62%;color:${cor};white-space:nowrap">MIAU</div>
  <svg width="899" height="700" viewBox="0 0 899 700" style="position:absolute;left:0;top:0;overflow:visible">
    ${o.unhas === false ? '' : rastros}
    <g transform="translate(${cx} ${parede}) scale(${k})">${o.contorno ? patas(o.contorno, o.contorno) : ''}${patas(gato)}${o.unhas === false ? '' : unhas(-106, 1) + unhas(106, -1)}</g>
  </svg>
  ${o.lab === false ? '' : `<div style="position:absolute;right:0;top:610px;background:${o.labFundo || '#141418'};color:${o.labCor || '#fff'};font:700 64px/1 Mono;padding:10px 20px 16px;letter-spacing:.02em">.lab</div>`}`;
}

// v3 · APROVADA ("sim perfeito"): gato-v3/gerado-e.png, olhos nivelados, patas .39, unhas e arranhões reais.
// v3 (a Emi: "você refinou o logo? … tá refinadinho ou tá vetorizado?" e "mais parecido com o original… os olhos do gatinho"):
// mesmo logo e mesma montagem da v2 (gato espiando de dentro do U, uma pata em cada haste, olhos de gato rosa com
// pupila em fenda, arranhões descendo nas hastes), mas o desenho da cabeça e das patas sai de uma silhueta gerada e
// vetorizada (gato-v3/gerado-b.png → gato-v3/extrai.py → gato-v3/gato.js): bochecha redonda com UM tufinho de cada lado,
// orelhas com curva, patas com dedos e unhas em gancho, e um fio na cor do fundo separando a pata da cara.
// Unhas e arranhões: os mesmos da v2 (unha off-white #F1ECE2 em gancho + arranhão fino), na ponta dos dedos novos. Precisa de gato-v3/gato.js carregado antes (const GATO3).
function miauLogoV3(el, o = {}) {
  const G = GATO3, fundo = o.fundo || '#2F55F2', cor = o.cor || '#FF9FD2', gato = o.gato || '#141418';
  const olho = o.olho || '#FF9FD2', olho2 = o.olho2 || '#FFFFFF', id = o.id || 'l3';
  const s = o.s3 || .3, sp = o.sp3 || .39, cx = o.cx || 798, parede = 260, dx = o.patasDx || 59.4;   // aprovado: gato E, patas .39
  const ko = .56, olhoGato = (x, r) => `<g transform="translate(${x} -80) rotate(${r})"><circle r="30" fill="${olho}"/>`
    + `<path d="M0 -24 Q11 0 0 24 Q-11 0 0 -24 Z" fill="${gato}"/><circle cx="9" cy="-11" r="5" fill="${olho2}"/></g>`;
  const cab = `<g transform="translate(${cx} ${parede}) scale(${s}) translate(${-G.cabeca.cx} ${-G.borda})"><path d="${G.cabeca.d}" fill="${gato}"/></g>`;
  // olhos acompanham a inclinação da cabeça nova (a direita mais baixa); a v2 girava -5°, ao contrário: "o olho tá tudo torto"
  const olhos = `<g transform="translate(${cx + (o.olhoDx || 0)} ${parede + (o.olhoDy || 0)}) scale(${ko * (o.olhoK || 1)}) rotate(${o.olhoGiro ?? 0} 0 -80)">${olhoGato(-54, 0)}${olhoGato(54, 0)}</g>`;
  const pata = (P, x, lado) => {
    const pc = (P.x0 + P.x1) / 2, t = `translate(${x} ${parede}) rotate(${lado * (o.giro3 ?? 4)}) scale(${sp}) translate(${-pc} ${-G.borda})`;
    return { t, pc, svg: `<g transform="${t}">`
      // fio na cor do fundo só contra a cara (acima da borda), como no desenho gerado
      + `<path d="${P.d}" fill="none" stroke="${fundo}" stroke-width="${o.fio3 || 11}" stroke-linejoin="round" clip-path="url(#acimaB-${id})"/>`
      + `<path d="${P.d}" fill="${gato}"/>`
      + '</g>' };
  };
  const pE = pata(G.pataE, cx - dx, 1), pD = pata(G.pataD, cx + dx, -1);
  // unhas e arranhões IGUAIS aos da v2 (mesmo desenho UNHA, mesma escala .56, mesmos tamanhos e desvios), só que
  // na ponta de cada dedo da pata nova: unha off-white em gancho e, logo abaixo, o arranhão fino recortado na letra
  const UNHA = 'M-2.8 -3 C-3 5 -1 11 2.6 14.5 C0.8 9 1.6 3 2.6 -3 Z', ku = .56, TAM = [[44, 60, 34], [38, 54, 28]];
  const giro = o.giro3 ?? 4;
  const dedo = (P, x, lado, [ux, uy]) => { const t = lado * giro * Math.PI / 180, px = (ux - (P.x0 + P.x1) / 2) * sp, py = (uy - G.borda) * sp;
    return [x + px * Math.cos(t) - py * Math.sin(t), parede + px * Math.sin(t) + py * Math.cos(t)]; };
  let unhasSvg = '', rastros = '';
  // arranhão de verdade (a Emi: "os arranhões continuam retilíneos" e depois "não era pra ficar curvo, era pra ficar
  // mais real"): reto como na v2 (mesma direção e desvio), mas com cara de risco de unha: borda rasgada e irregular
  // (ruído fino diferente em cada lado), largura que crava logo abaixo da unha e some de forma desigual, um tremor leve
  // no traço e, no do meio de cada pata, uma falha curta onde a unha "pulou".
  const hash = (i, sd) => { const x = Math.sin(i * 127.1 + sd * 311.7) * 43758.5453; return (x - Math.floor(x)) * 2 - 1; };
  const ruido = (x, sd) => { const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f); return hash(i, sd) * (1 - u) + hash(i + 1, sd) * u; };
  const fbm = (x, sd) => ruido(x, sd) * .6 + ruido(x * 2.3, sd + 7) * .28 + ruido(x * 5.1, sd + 13) * .12;
  function risco(sx, sy, L, lado, sd) {
    const j = sd % 3, d = (j - 1) * 1.6 + lado * -1.2, w0 = o.rastroW || 1.4, N = 160, R = o.rasgo ?? .45;
    const falha = j === 1 ? [.5 + .06 * hash(sd, 3), .57 + .06 * hash(sd, 3)] : null;
    const pecas = []; let esq = [], dir = [];
    const fecha = () => { if (esq.length > 2) pecas.push(esq.concat(dir.reverse())); esq = []; dir = []; };
    for (let n = 0; n <= N; n++) {
      const t = n / N, x = sx + d * t + .45 * fbm(t * 3 + sd, sd + 1), y = sy + L * t;
      // perfil: crava (sobe rápido), mantém um pouco e afina irregular até um fio
      let w = w0 * Math.min(1, .45 + t / .05) * Math.pow(1 - t, .75) * (1 + .3 * fbm(t * 6, sd + 5));
      if (falha && t > falha[0] && t < falha[1]) { fecha(); continue; }
      if (falha && t >= falha[1]) w *= .7;
      const rg = (k) => .55 * fbm(t * 13, sd + k) + .45 * fbm(t * 47, sd + k + 3);   // lascas grandes + farpas finas
      const wl = Math.max(0, w * (1 + R * 1.15 * rg(11))), wr = Math.max(0, w * (1 + R * 1.15 * rg(23)));
      esq.push([x - wl, y]); dir.push([x + wr, y]);
    }
    fecha();
    return pecas.map(p => `<path d="M${p.map(q => q[0].toFixed(2) + ' ' + q[1].toFixed(2)).join(' L')} Z" fill="${fundo}"/>`).join('');
  }
  [[G.pataE, cx - dx, 1], [G.pataD, cx + dx, -1]].forEach(([P, x, lado], i) => P.dedos.forEach((u, j) => {
    const [tx, ty] = dedo(P, x, lado, u), r = lado * 7;
    unhasSvg += `<g transform="translate(${tx} ${ty}) rotate(${r}) scale(${ku})"><path d="${UNHA}" transform="translate(0 ${-(o.encaixeUnha ?? 4)})" fill="${o.unha || '#F1ECE2'}"/></g>`;
    const tr = r * Math.PI / 180, py = 13 - (o.encaixeUnha ?? 4) + 3;
    const sx = tx - py * ku * Math.sin(tr), sy = ty + py * ku * Math.cos(tr), L = TAM[i][j] * (o.rastroK || 1);
    rastros += risco(sx, sy, L, lado, i * 3 + j);
  }));
  el.style.position = el.style.position || 'absolute';
  el.innerHTML = `
  <svg width="899" height="700" viewBox="0 0 899 700" style="position:absolute;left:0;top:0;overflow:visible">${cab}${olhos}</svg>
  <div style="position:absolute;left:-19px;top:191px;font:900 470px/1 Archivo;font-stretch:62%;color:${cor};white-space:nowrap">MIAU</div>
  <svg width="899" height="700" viewBox="0 0 899 700" style="position:absolute;left:0;top:0;overflow:visible">
    <defs><clipPath id="acimaB-${id}" clipPathUnits="userSpaceOnUse"><rect x="-2000" y="-2000" width="5000" height="${2000 + G.borda}"/></clipPath>
</defs>
    ${o.unhas === false ? '' : rastros}${pE.svg}${pD.svg}${o.unhas === false ? '' : unhasSvg}
  </svg>
  ${o.lab === false ? '' : `<div style="position:absolute;right:0;top:610px;background:${o.labFundo || '#141418'};color:${o.labCor || '#fff'};font:700 64px/1 Mono;padding:10px 20px 16px;letter-spacing:.02em">.lab</div>`}`;
}
