/* Motions do projeto do Behance. Cada módulo animado registra render(t) em MOTION.
   Na página, os módulos tocam sozinhos; na gravação, selecionar('#id') entrega
   DURACAO e renderFrame(t) para capturar quadro a quadro. */
document.addEventListener('DOMContentLoaded', function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var TAU = Math.PI * 2;
  function clamp(x) { return Math.max(0, Math.min(1, x)); }
  function prog(t, a, b) { return clamp((t - a) / (b - a)); }
  function suave(x) { return x * x * (3 - 2 * x); }
  function sai(x) { return 1 - Math.pow(1 - x, 3); }
  function mix(a, b, k) { return a + (b - a) * k; }
  function px(n) { return n.toFixed(2) + 'px'; }
  function revelaLua(el, k) { // a lua se desenha da ponta de cima, no sentido anti-horário
    var a = k * 300;
    var m = 'conic-gradient(from 312deg at 48.8% 54.4%, transparent 0deg, transparent ' + Math.max(0, 360 - a) + 'deg, #000 ' + Math.min(360, 360 - a + 6) + 'deg, #000 360deg)';
    el.style.webkitMaskImage = m; el.style.maskImage = m;
  }
  function tracar(el, k) { var L = el.__L || (el.__L = el.getTotalLength()); el.style.strokeDasharray = L + ' ' + L; el.style.strokeDashoffset = L * (1 - k); }
  function cor(k) { return 'rgb(255,' + Math.round(mix(168, 235, k)) + ',' + Math.round(mix(84, 180, k)) + ')'; }
  function ceu(alvo, w, h, semente, periodo, evitar) {
    alvo.innerHTML = Almah.estrelas(w, h, { n: 46, semente: semente, rMax: 9, miolo: .18 });
    // tira as estrelas que caem em cima de texto ou de rótulo
    var base = alvo.getBoundingClientRect(), caixas = $$(evitar || '.cab', alvo.parentNode).map(function (e) { return e.getBoundingClientRect(); });
    $$('.est, .pt', alvo).forEach(function (e) {
      var r = e.getBoundingClientRect(), x = (r.left + r.right) / 2, y = (r.top + r.bottom) / 2;
      if (caixas.some(function (c) { return x > c.left - 24 && x < c.right + 24 && y > c.top - 24 && y < c.bottom + 24; })) e.remove();
    });
    var est = $$('.est, .pt', alvo);
    return function (t) { est.forEach(function (e, i) { e.style.opacity = 0.5 + 0.4 * Math.sin(TAU * (t / periodo * (1 + i % 3) + i * .618)); }); };
  }
  var MOTION = {};

  /* ---------- 01 · como nasceu o símbolo ---------- */
  MOTION['#m-nasceu'] = { dur: 9, render: function (t) {
    var fim = 1 - suave(prog(t, 8.2, 9));
    var k = suave(prog(t, 3.8, 5.4));
    var lua = $('#n-lua'), ch = $('#n-chama'), chP = $('#n-chama path');
    revelaLua($('#n-lua-svg'), suave(prog(t, .3, 2.0)));
    lua.style.opacity = suave(prog(t, .2, .8)) * fim;
    lua.style.left = px(mix(400, 700, k));
    ch.style.left = px(mix(1000, 700, k));
    ch.style.opacity = suave(prog(t, 1.9, 2.4)) * fim;
    var g = sai(prog(t, 1.9, 3.2));
    chP.style.transformBox = 'fill-box'; chP.style.transformOrigin = '50% 100%';
    chP.style.transform = 'scale(' + mix(.5, 1, g).toFixed(4) + ',' + mix(.05, 1, g).toFixed(4) + ')';
    $('#n-mais').style.opacity = suave(prog(t, 2.3, 2.8)) * (1 - suave(prog(t, 3.5, 3.9)));
    $('#n-l1').style.opacity = suave(prog(t, .9, 1.6)) * (1 - suave(prog(t, 3.4, 4.0)));
    $('#n-l2').style.opacity = suave(prog(t, 2.4, 3.1)) * (1 - suave(prog(t, 3.4, 4.0)));
    $('#n-l3').style.opacity = suave(prog(t, 5.6, 6.4)) * fim;
    $('#n-l3').style.transform = 'translateY(' + px(mix(10, 0, sai(prog(t, 5.6, 6.6)))) + ')';
    var h = $('#n-halo');
    h.style.opacity = (suave(prog(t, 5.0, 5.8)) * (1 - .45 * suave(prog(t, 5.8, 7.0)))) * fim;
    h.style.transform = 'translate(-50%,-50%) scale(' + mix(.5, 1.05, sai(prog(t, 5.0, 6.4))).toFixed(4) + ')';
  } };

  /* ---------- 02 · construção do símbolo ---------- */
  (function () {
    var S = window.ALMAH_SVG, NS = 'http://www.w3.org/2000/svg';
    var dLua = S.lua.match(/ d="([^"]+)"/)[1], dChama = S['chama-simbolo'].match(/ d="([^"]+)"/)[1];
    var cx0 = 360, cy0 = -40, W = 580, H = 600;
    var box = $('#c-desenho');
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', cx0 + ' ' + cy0 + ' ' + W + ' ' + H);
    box.appendChild(svg);
    function el(nome, at, pai) { var e = document.createElementNS(NS, nome); for (var k in at) e.setAttribute(k, at[k]); (pai || svg).appendChild(e); return e; }
    // círculos ajustados aos pontos do contorno (mínimos quadrados)
    var tmp = el('path', { d: dLua, fill: 'none' });
    var L = tmp.getTotalLength(), pts = [];
    for (var i = 0; i < 720; i++) { var p = tmp.getPointAtLength(L * i / 720); pts.push([p.x, p.y]); }
    svg.removeChild(tmp);
    function ajusta(ps) {
      var sx = 0, sy = 0, sxx = 0, syy = 0, sxy = 0, sz = 0, sxz = 0, syz = 0, n = ps.length;
      ps.forEach(function (q) { var x = q[0], y = q[1], z = x * x + y * y; sx += x; sy += y; sxx += x * x; syy += y * y; sxy += x * y; sz += z; sxz += x * z; syz += y * z; });
      var A = [[sxx, sxy, sx], [sxy, syy, sy], [sx, sy, n]], b = [-sxz, -syz, -sz];
      function det(m) { return m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]); }
      function troca(m, c, v) { return m.map(function (l, r) { return l.map(function (x, j) { return j === c ? v[r] : x; }); }); }
      var D = det(A), Dd = det(troca(A, 0, b)) / D, Ee = det(troca(A, 1, b)) / D, Ff = det(troca(A, 2, b)) / D;
      var cx = -Dd / 2, cy = -Ee / 2; return [cx, cy, Math.sqrt(cx * cx + cy * cy - Ff)];
    }
    var g0 = [644.5, 279.5, 224.5];
    var fora = pts.filter(function (q) { return Math.abs(Math.hypot(q[0] - g0[0], q[1] - g0[1]) - g0[2]) < 7; });
    var O = ajusta(fora);
    var dentro = pts.filter(function (q) { return Math.hypot(q[0] - O[0], q[1] - O[1]) < O[2] - 8; });
    var I = ajusta(dentro);
    var tmp2 = el('path', { d: dChama, fill: 'none' }), L2 = tmp2.getTotalLength(), pc = [];
    for (i = 0; i < 400; i++) { var q = tmp2.getPointAtLength(L2 * i / 400); if (q.y > 300) pc.push([q.x, q.y]); }
    svg.removeChild(tmp2);
    var G = ajusta(pc);
    var eixo = 652.5;
    var ouro = '#E9D29A', creme = '#FFEBB4';
    var grade = el('g', { stroke: creme, 'stroke-width': .5, opacity: 0 });
    for (var x = cx0; x <= cx0 + W; x += 20) el('line', { x1: x, y1: cy0, x2: x, y2: cy0 + H, 'stroke-opacity': .07 }, grade);
    for (var y = cy0; y <= cy0 + H; y += 20) el('line', { x1: cx0, y1: y, x2: cx0 + W, y2: y, 'stroke-opacity': .07 }, grade);
    var eH = el('line', { x1: cx0, y1: O[1], x2: cx0, y2: O[1], stroke: ouro, 'stroke-width': .8, 'stroke-dasharray': '4 5', opacity: .6 });
    var eV = el('line', { x1: eixo, y1: cy0, x2: eixo, y2: cy0, stroke: ouro, 'stroke-width': .8, 'stroke-dasharray': '4 5', opacity: .6 });
    var cO = el('circle', { cx: O[0], cy: O[1], r: O[2], fill: 'none', stroke: ouro, 'stroke-width': 1 });
    var cI = el('circle', { cx: I[0], cy: I[1], r: I[2], fill: 'none', stroke: ouro, 'stroke-width': 1 });
    var cG = el('circle', { cx: G[0], cy: G[1], r: G[2], fill: 'none', stroke: ouro, 'stroke-width': .9 });
    var marcas = el('g', { fill: ouro, opacity: 0, 'font-family': 'Poppins', 'font-size': 11, 'letter-spacing': '1' });
    el('circle', { cx: O[0], cy: O[1], r: 3 }, marcas); el('circle', { cx: I[0], cy: I[1], r: 3 }, marcas);
    var aO = 205 * Math.PI / 180, aI = 25 * Math.PI / 180;
    el('line', { x1: O[0], y1: O[1], x2: O[0] + O[2] * Math.cos(aO), y2: O[1] + O[2] * Math.sin(aO), stroke: ouro, 'stroke-width': .8 }, marcas);
    el('line', { x1: I[0], y1: I[1], x2: I[0] + I[2] * Math.cos(aI), y2: I[1] + I[2] * Math.sin(aI), stroke: ouro, 'stroke-width': .8 }, marcas);
    el('text', { x: O[0] + O[2] * .5 * Math.cos(aO) - 4, y: O[1] + O[2] * .5 * Math.sin(aO) - 8 }, marcas).textContent = 'R';
    el('text', { x: I[0] + I[2] * .5 * Math.cos(aI) + 2, y: I[1] + I[2] * .5 * Math.sin(aI) - 8 }, marcas).textContent = 'r';
    el('text', { x: eixo + 8, y: cy0 + 24 }, marcas).textContent = 'eixo';
    var luaF = el('path', { d: dLua, fill: creme, opacity: 0 });
    var luaT = el('path', { d: dLua, fill: 'none', stroke: creme, 'stroke-width': 1.4 });
    var chF = el('path', { d: dChama, fill: creme, opacity: 0 });
    var chT = el('path', { d: dChama, fill: 'none', stroke: creme, 'stroke-width': 1.4 });
    var itens = [$('#c-i1'), $('#c-i2'), $('#c-i3')];
    MOTION['#m-constr'] = { dur: 11, render: function (t) {
      var fim = 1 - suave(prog(t, 10.2, 11));
      var guia = mix(1, .32, suave(prog(t, 7.0, 8.2)));
      grade.setAttribute('opacity', suave(prog(t, 0, 1.0)) * fim);
      eH.setAttribute('x2', mix(cx0, cx0 + W, sai(prog(t, .5, 1.7)))); eH.setAttribute('opacity', .6 * guia * fim);
      eV.setAttribute('y2', mix(cy0, cy0 + H, sai(prog(t, .7, 1.9)))); eV.setAttribute('opacity', .6 * guia * fim);
      tracar(cO, suave(prog(t, 1.2, 2.8))); cO.setAttribute('opacity', (prog(t, 1.2, 1.25)) * guia * fim);
      tracar(cI, suave(prog(t, 2.0, 3.4))); cI.setAttribute('opacity', (prog(t, 2.0, 2.05)) * guia * fim);
      marcas.setAttribute('opacity', suave(prog(t, 2.8, 3.4)) * guia * fim);
      tracar(luaT, suave(prog(t, 3.4, 5.2))); luaT.setAttribute('opacity', prog(t, 3.4, 3.45) * (1 - suave(prog(t, 7.0, 7.8))) * fim);
      tracar(cG, suave(prog(t, 4.6, 5.6))); cG.setAttribute('opacity', prog(t, 4.6, 4.65) * guia * fim);
      tracar(chT, suave(prog(t, 5.0, 6.8))); chT.setAttribute('opacity', prog(t, 5.0, 5.05) * (1 - suave(prog(t, 7.0, 7.8))) * fim);
      luaF.setAttribute('opacity', suave(prog(t, 6.8, 7.8)) * fim);
      chF.setAttribute('opacity', suave(prog(t, 7.0, 8.0)) * fim);
      var ativo = [[1.2, 4.4], [4.4, 7.0], [7.0, 10.2]];
      itens.forEach(function (it, j) { var a = ativo[j]; it.style.opacity = .3 + .7 * suave(prog(t, a[0], a[0] + .4)) * (1 - suave(prog(t, a[1], a[1] + .4))); });
    } };
  })();

  /* ---------- 03 · a chama acende ---------- */
  (function () {
    var piscar = ceu($('#a-ceu'), 1400, 876, 17, 10.4, '.cab, .simbolo, .nome, .credito');
    MOTION['#m-acende'] = { dur: 10.4, render: function (t) {
      piscar(t);
      $('#a-ceu').style.opacity = suave(prog(t, 0, 1.2));
      var lua = $('#a-lua'), chP = $('#a-chama path');
      revelaLua(lua, suave(prog(t, .4, 2.9)));
      lua.style.opacity = suave(prog(t, .4, 1.2));
      var br = prog(t, 2.2, 2.8) * (1 - prog(t, 3.4, 4.0));
      $('#a-brasa').style.opacity = br * (0.75 + 0.25 * Math.sin(TAU * t * 2.2));
      var g = sai(prog(t, 2.7, 4.6)), fl = suave(prog(t, 3.6, 5.2));
      var sy = mix(0.04, 1, g) * (1 + fl * (0.022 * Math.sin(TAU * 1.3 * t) + 0.014 * Math.sin(TAU * 2.9 * t + 1)));
      var sx = mix(0.45, 1, g) * (1 + fl * 0.012 * Math.sin(TAU * 1.7 * t + 2));
      var sk = (1 - g) * 4 * Math.sin(TAU * 1.1 * t) + fl * 1.1 * Math.sin(TAU * 0.8 * t);
      chP.style.transformBox = 'fill-box'; chP.style.transformOrigin = '50% 100%';
      chP.style.transform = 'scale(' + sx.toFixed(4) + ',' + sy.toFixed(4) + ') skewX(' + sk.toFixed(3) + 'deg)';
      chP.style.opacity = suave(prog(t, 2.7, 3.3));
      chP.style.fill = cor(suave(prog(t, 2.9, 5.0)));
      var v = 1 - suave(prog(t, 9.5, 10.4));
      var bri = suave(prog(t, 2.8, 5.0)), b = $('#a-brilho');
      b.style.opacity = bri * v; b.style.transform = 'translate(-50%,-50%) scale(' + mix(.3, 1, bri).toFixed(4) + ')';
      $('#a-sol').style.opacity = 0.3 * suave(prog(t, 3.6, 5.8)) * v;
      ['#a-n1', '#a-n2'].forEach(function (id, i) { var e = $(id); e.style.opacity = (i ? .38 : .48) * suave(prog(t, 4.2, 6.0)) * v; e.style.transform = 'translateY(' + px(mix(16, 0, sai(prog(t, 4.2, 6.4)))) + ')'; });
      var n = sai(prog(t, 4.7, 6.4)), nome = $('#a-nome');
      nome.style.opacity = n * v; nome.style.filter = 'blur(' + mix(7, 0, n).toFixed(2) + 'px)';
      nome.style.transform = 'translateX(-50%) translateY(' + px(mix(14, 0, n)) + ')';
      var c = suave(prog(t, 6.4, 7.4)), cr = $('#a-credito');
      cr.style.opacity = c * .85 * v; cr.style.letterSpacing = mix(.42, .3, c).toFixed(3) + 'em';
      $('#m-acende .simbolo').style.opacity = v;
    } };
  })();

  /* ---------- 07 · cinco céus ---------- */
  (function () {
    var piscar = ceu($('#ceus-ceu'), 1400, 876, 23, 10, '.cab, .r');
    var rs = $$('#m-ceus .r');
    var arco = $('#ceus-arco');
    MOTION['#m-ceus'] = { dur: 10, render: function (t) {
      piscar(t);
      arco.style.opacity = suave(prog(t, .2, 1.4)) * (1 - suave(prog(t, 9.0, 10)));
      var La = arco.__L || (arco.__L = arco.getTotalLength()); arco.style.strokeDashoffset = 0; arco.setAttribute('stroke-dasharray', '3 6');
      arco.style.clipPath = 'inset(0 ' + (100 - 100 * sai(prog(t, .2, 4.4))).toFixed(2) + '% 0 0)';
      var fim = 1 - suave(prog(t, 9.0, 10));
      rs.forEach(function (r, i) {
        var a = .5 + i * .8, e = sai(prog(t, a, a + 1.0));
        var boia = 5 * Math.sin(TAU * (t / 5 + i * .2)) * suave(prog(t, a + .8, a + 1.8));
        r.style.opacity = suave(prog(t, a, a + .8)) * fim;
        r.style.transform = 'translateY(' + px(mix(30, 0, e) + boia) + ') rotate(' + r.style.getPropertyValue('--rot') + ')';
        r.style.filter = 'blur(' + mix(6, 0, e).toFixed(2) + 'px)';
        r.style.setProperty('--g', (suave(prog(t, a + .2, a + .8)) * (1 - suave(prog(t, a + 1.0, a + 2.4)))).toFixed(3));
      });
    } };
  })();

  /* ---------- 08 · o aroma em cena (vídeos) ---------- */
  (function () {
    var vs = $$('#m-aroma video');
    vs.forEach(function (v) { v.src = v.dataset.webm; });
    function buscar(v, s) { return new Promise(function (ok) { if (Math.abs(v.currentTime - s) < .001) return ok(); v.addEventListener('seeked', function () { ok(); }, { once: true }); v.currentTime = s; }); }
    MOTION['#m-aroma'] = { dur: 5,
      preparar: function () { return Promise.all(vs.map(function (v) { v.pause(); return v.readyState >= 2 ? 0 : new Promise(function (ok) { v.addEventListener('loadeddata', ok, { once: true }); }); })); },
      ao_vivo: function () { vs.forEach(function (v) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }); },
      render: function (t) { var s = .3 + (t < 2.5 ? t : 5 - t); return Promise.all(vs.map(function (v) { return buscar(v, s); })).then(function () { return new Promise(function (ok) { requestAnimationFrame(function () { ok(); }); }); }); }
    };
  })();

  /* ---------- 09 · o céu que se repete ---------- */
  MOTION['#m-estampa'] = { dur: 6, render: function (t) {
    $('#e-faixa').style.backgroundPosition = px(-(t / 6) * 150) + ' 0';
    $('#e-sol').style.transform = 'rotate(' + (3 * Math.sin(TAU * t / 6)).toFixed(3) + 'deg)';
    $('#e-nuv').style.transform = 'translateX(' + px(9 * Math.sin(TAU * t / 6)) + ')';
    $('#e-est').style.transform = 'scale(' + (1 + .07 * Math.sin(TAU * t / 3)).toFixed(4) + ') rotate(' + (6 * Math.sin(TAU * t / 6)).toFixed(3) + 'deg)';
    $('#e-est2').style.opacity = (.55 + .45 * Math.sin(TAU * (t / 3 + .3))).toFixed(3);
    $('#e-est3').style.opacity = (.55 + .45 * Math.sin(TAU * (t / 2 + .7))).toFixed(3);
  } };

  /* ---------- 10 · o ritual da queima ---------- */
  (function () {
    var passos = $$('#m-ritual .passo'), pontos = $$('#m-ritual .pontos i');
    var A = function (id, k, v) { $(id).setAttribute(k, v); };
    MOTION['#m-ritual'] = { dur: 12.5, render: function (t) {
      passos.forEach(function (p, j) {
        var a = j * 2.5, b = j === 4 ? 12.0 : a + 2.0;
        p.style.opacity = suave(prog(t, a, a + .5)) * (1 - suave(prog(t, b, b + .5)));
        p.style.transform = 'translateY(' + px(mix(12, 0, sai(prog(t, a, a + .8)))) + ')';
        pontos[j].style.opacity = (t >= a && t < a + 2.5) ? 1 : .25;
      });
      var piscina = suave(prog(t, .4, 2.2));
      var nivel = mix(196, 242, suave(prog(t, 5.2, 7.2)));
      var topoPavio = mix(170, 182, suave(prog(t, 2.8, 3.6))) + (nivel - 196);
      A('#r-cera', 'y', nivel.toFixed(2)); A('#r-topo', 'cy', nivel.toFixed(2));
      A('#r-piscina', 'cy', nivel.toFixed(2)); A('#r-piscina', 'rx', mix(34, 104, piscina).toFixed(2)); A('#r-piscina', 'ry', mix(6, 13, piscina).toFixed(2));
      A('#r-pavio', 'y1', nivel.toFixed(2)); A('#r-pavio', 'y2', topoPavio.toFixed(2));
      var apaga = 1 - suave(prog(t, 10.0, 10.5));
      var calma = 1 - .6 * suave(prog(t, 7.6, 8.4));
      var sy = 1 + calma * (.04 * Math.sin(TAU * 1.4 * t) + .02 * Math.sin(TAU * 3.1 * t + 1));
      var sk = calma * 2.2 * Math.sin(TAU * .9 * t);
      var ch = $('#r-chama');
      ch.style.transform = 'translateY(' + px(topoPavio - 170) + ') scale(1,' + sy.toFixed(4) + ') skewX(' + sk.toFixed(3) + 'deg)';
      ch.style.opacity = apaga;
      A('#r-brilho', 'cy', (topoPavio - 52).toFixed(2)); $('#r-brilho').style.opacity = apaga;
      var tes = suave(prog(t, 2.6, 3.0)) * (1 - suave(prog(t, 4.2, 4.8)));
      $('#r-tesoura').style.opacity = tes; $('#r-tesoura').style.transform = 'translate(' + px(mix(20, 0, suave(prog(t, 2.6, 3.2)))) + ',' + px(topoPavio - 170) + ')';
      $('#r-mesa').style.opacity = suave(prog(t, 7.6, 8.2));
      var fu = $('#r-fumaca'); fu.style.opacity = suave(prog(t, 10.3, 10.8)) * (1 - suave(prog(t, 11.8, 12.4)));
      fu.style.transform = 'translateY(' + px(topoPavio - 170 - 26 * prog(t, 10.3, 12.4)) + ')';
      $$('#r-fumaca path').forEach(function (p, i) { p.style.strokeDasharray = '160'; p.style.strokeDashoffset = (160 * (1 - prog(t, 10.3 + i * .3, 11.9))).toFixed(1); });
      var rel = $('#r-relogio'), m = Math.round(180 * suave(prog(t, 5.2, 7.2)));
      rel.firstChild.nodeValue = Math.floor(m / 60) + ':' + String(m % 60).padStart(2, '0');
      rel.style.opacity = suave(prog(t, 5.0, 5.4)) * (1 - suave(prog(t, 7.4, 7.9)));
      $('#r-tudo').style.opacity = suave(prog(t, 0, .5)) * (1 - suave(prog(t, 12.0, 12.5)));
    } };
  })();

  /* ---------- gravação ---------- */
  window.MOTION = MOTION;
  window.selecionar = function (sel) {
    window.CAPTURA = true;
    var m = MOTION[sel];
    window.DURACAO = m.dur;
    window.renderFrame = m.render;
    return m.preparar ? m.preparar() : Promise.resolve();
  };

  /* ---------- na página: tudo toca sozinho ---------- */
  Object.keys(MOTION).forEach(function (k) { MOTION[k].render(0); if (MOTION[k].ao_vivo) MOTION[k].ao_vivo(); });
  var t0 = performance.now();
  function quadro(agora) {
    if (window.CAPTURA) return;
    var s = (agora - t0) / 1000;
    Object.keys(MOTION).forEach(function (k) {
      var m = MOTION[k], el = $(k), r = el.getBoundingClientRect();
      if (m.ao_vivo || r.bottom < -50 || r.top > innerHeight + 50) return;
      m.render(s % m.dur);
    });
    requestAnimationFrame(quadro);
  }
  requestAnimationFrame(quadro);
});
