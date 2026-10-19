/* Kit Almah: desenha os elementos gráficos da marca (sol raiado, estrelas de quatro pontas,
   estampa) e injeta os vetores oficiais de svgs.js. Depende de window.ALMAH_SVG. */
(function () {
  var S = window.ALMAH_SVG || {};
  var ESTRELA = 'M0-1C.07-.24.24-.07 1 0 .24.07.07.24 0 1-.07.24-.24.07-1 0-.24-.07-.07-.24 0-1Z';

  function sorteio(semente) {
    var s = (semente >>> 0) || 1;
    return function () { s ^= s << 13; s ^= s >>> 17; s ^= s << 5; return ((s >>> 0) % 100000) / 100000; };
  }
  function f(n) { return Math.round(n * 100) / 100; }

  function svg(nome, attrs) {
    var s = S[nome] || '';
    return attrs ? s.replace('<svg ', '<svg ' + attrs + ' ') : s;
  }

  // sol raiado: raios longos e curtos alternados, alguns tracejados, como no rótulo
  function raios(o) {
    o = o || {};
    var n = o.n || 64, r0 = o.r0 == null ? 16 : o.r0, r1 = o.r1 || 98, de = o.de == null ? -180 : o.de, ate = o.ate == null ? 0 : o.ate;
    var peso = o.peso || .32, R = sorteio(o.semente || 11), d = '', pts = '';
    var cheio = Math.abs(ate - de) >= 360;
    for (var i = 0; i < (cheio ? n : n + 1); i++) {
      var a = (de + (ate - de) * i / n) * Math.PI / 180, c = Math.cos(a), s = Math.sin(a);
      var longo = i % 2 === 0;
      var ri = r0 + (longo ? 0 : 5 + R() * 6);
      var re = longo ? r1 * (.78 + R() * .22) : r1 * (.48 + R() * .3);
      if (R() < .24) {
        var m = ri + (re - ri) * (.42 + R() * .2), g = 2.2 + R() * 2;
        d += 'M' + f(c * ri) + ' ' + f(s * ri) + 'L' + f(c * m) + ' ' + f(s * m);
        d += 'M' + f(c * (m + g)) + ' ' + f(s * (m + g)) + 'L' + f(c * re) + ' ' + f(s * re);
      } else {
        d += 'M' + f(c * ri) + ' ' + f(s * ri) + 'L' + f(c * re) + ' ' + f(s * re);
      }
      if (o.pontos !== false && R() < .16) pts += '<circle cx="' + f(c * (re + 3)) + '" cy="' + f(s * (re + 3)) + '" r=".55"/>';
    }
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-100 -100 200 200" class="cheio" fill="currentColor" aria-hidden="true">' +
      '<path d="' + d + '" stroke="currentColor" stroke-width="' + peso + '" stroke-linecap="round" fill="none" vector-effect="' + (o.fixo ? 'non-scaling-stroke' : 'none') + '"/>' + pts + '</svg>';
  }

  function estrela(x, y, r, attrs) {
    return '<path d="' + ESTRELA + '" transform="translate(' + f(x) + ' ' + f(y) + ') scale(' + f(r) + ')"' + (attrs || '') + '/>';
  }

  // céu: estrelas de quatro pontas e pontinhos espalhados numa área w × h
  function estrelas(w, h, o) {
    o = o || {};
    var R = sorteio(o.semente || 5), n = o.n || 24, out = '';
    var m = o.miolo || 0;
    for (var i = 0; i < n; i++) {
      var x = R() * w, y = R() * h, grande = R() < (o.grandes || .18);
      // deixa o miolo livre para o texto
      if (m && x > w * m && x < w * (1 - m) && y > h * m && y < h * (1 - m)) { x = x < w / 2 ? x * m * 1.4 % (w * m) : w - (x % (w * m)); }
      var r = grande ? (o.rMax || 9) * (.6 + R() * .4) : (o.rMin || 2.4) * (.6 + R() * .6);
      out += estrela(x, y, r, ' class="est' + (grande ? ' g' : '') + '" style="--d:' + f(R() * 4) + 's"');
      var px = R() * w, py = R() * h;
      if (m && px > w * m && px < w * (1 - m) && py > h * m && py < h * (1 - m)) continue;
      if (R() < .6) out += '<circle cx="' + f(px) + '" cy="' + f(py) + '" r="' + f(.6 + R() * .9) + '" class="pt" style="--d:' + f(R() * 4) + 's"/>';
    }
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + w + ' ' + h + '" class="cheio" fill="currentColor" aria-hidden="true">' + out + '</svg>';
  }

  // estampa da marca: símbolo, estrelas e nuvem em meia-queda, numa cor só
  function estampa(cor, fundo, tam) {
    tam = tam || 240;
    var sim = function (x, y, w) { return svg('simbolo', 'x="' + x + '" y="' + y + '" width="' + w + '" height="' + w + '"'); };
    var nuv = function (x, y, w) { return svg('nuvem-linha-1', 'x="' + x + '" y="' + y + '" width="' + w + '" height="' + (w * .52) + '"'); };
    var est = function (x, y, r) { return estrela(x, y, r); };
    var corpo =
      sim(36, 30, 52) + sim(156, 150, 52) +
      nuv(140, 44, 70) + nuv(20, 166, 70) +
      est(112, 112, 7) + est(222, 222, 3) + est(200, 18, 3.5) + est(18, 116, 3) + est(98, 206, 3.2) + est(232, 104, 5) +
      '<circle cx="62" cy="126" r="1.2"/><circle cx="182" cy="110" r="1.2"/><circle cx="122" cy="20" r="1"/><circle cx="6" cy="226" r="1"/>';
    var s = '<svg xmlns="http://www.w3.org/2000/svg" width="' + tam + '" height="' + tam + '" viewBox="0 0 240 240" style="color:' + cor + '" fill="' + cor + '">' +
      (fundo ? '<rect width="240" height="240" fill="' + fundo + '"/>' : '') + corpo + '</svg>';
    return 'url("data:image/svg+xml;charset=utf-8,' + encodeURIComponent(s) + '")';
  }

  function cmyk(hex) {
    var r = parseInt(hex.slice(1, 3), 16) / 255, g = parseInt(hex.slice(3, 5), 16) / 255, b = parseInt(hex.slice(5, 7), 16) / 255;
    var k = 1 - Math.max(r, g, b);
    if (k >= 1) return '0 · 0 · 0 · 100';
    return [(1 - r - k) / (1 - k), (1 - g - k) / (1 - k), (1 - b - k) / (1 - k), k].map(function (v) { return Math.round(v * 100); }).join(' · ');
  }
  function rgb(hex) { return [1, 3, 5].map(function (i) { return parseInt(hex.slice(i, i + 2), 16); }).join(' · '); }

  function decorar(raiz) {
    raiz = raiz || document;
    raiz.querySelectorAll('[data-svg]').forEach(function (el) { el.innerHTML = svg(el.dataset.svg); el.classList.add('svg'); });
    raiz.querySelectorAll('[data-raios]').forEach(function (el) {
      var o = {}; (el.dataset.raios || '').split(';').forEach(function (p) { var kv = p.split(':'); if (kv[0]) o[kv[0].trim()] = parseFloat(kv[1]); });
      el.innerHTML = raios(o); el.classList.add('svg');
    });
    raiz.querySelectorAll('[data-estrelas]').forEach(function (el) {
      var o = {}; (el.dataset.estrelas || '').split(';').forEach(function (p) { var kv = p.split(':'); if (kv[0]) o[kv[0].trim()] = parseFloat(kv[1]); });
      var w = el.clientWidth || 400, h = el.clientHeight || 300;
      el.innerHTML = estrelas(w, h, o); el.classList.add('svg');
    });
    raiz.querySelectorAll('[data-estampa]').forEach(function (el) {
      var p = el.dataset.estampa.split(','); el.style.backgroundImage = estampa(p[0], p[1] || '', +(p[2] || 240));
    });
    raiz.querySelectorAll('[data-cmyk]').forEach(function (el) { el.textContent = cmyk(el.dataset.cmyk); });
    raiz.querySelectorAll('[data-rgb]').forEach(function (el) { el.textContent = rgb(el.dataset.rgb); });
  }

  window.Almah = { svg: svg, raios: raios, estrelas: estrelas, estrela: estrela, estampa: estampa, cmyk: cmyk, rgb: rgb, decorar: decorar, ESTRELA: ESTRELA };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { decorar(); });
  else decorar();
})();
