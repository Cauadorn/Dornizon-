/* Almah · site da Coleção Gênesis
   O foguinho desenhado à mão acende sobre a foto da lua; o símbolo vai do traço à luz;
   a prateleira e as cartas mostram a coleção; a caixa se abre em cinco tempos; dá para montar um rótulo.
   Funciona sem GSAP (tudo visível, sem animação de rolagem). */
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduz = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var temGsap = !!(window.gsap && window.ScrollTrigger) && !reduz;
  var html = document.documentElement, body = document.body;
  var NS = 'http://www.w3.org/2000/svg';
  html.classList.toggle('com-gsap', temGsap);
  if (temGsap) { gsap.registerPlugin(ScrollTrigger); gsap.ticker.lagSmoothing(1000, 33); }
  function el(nome, at, pai) { var e = document.createElementNS(NS, nome); for (var k in at) e.setAttribute(k, at[k]); if (pai) pai.appendChild(e); return e; }
  function clamp(x) { return Math.max(0, Math.min(1, x)); }
  function prog(t, a, b) { return clamp((t - a) / (b - a)); }
  function suave(x) { return x * x * (3 - 2 * x); }
  var TAU = Math.PI * 2;

  /* fase da lua (0 nova, 1 cheia), crescente iluminado à direita */
  function fase(svg, p, cor) {
    svg.setAttribute('viewBox', '-50 -50 100 100');
    var r = 44, k = Math.cos(Math.PI * p), rx = Math.abs(k) * r;
    el('circle', { cx: 0, cy: 0, r: r, fill: 'none', stroke: cor, 'stroke-width': 3, opacity: .7 }, svg);
    if (p >= .999) el('circle', { cx: 0, cy: 0, r: r, fill: cor }, svg);
    else el('path', { d: 'M0 ' + (-r) + ' A' + r + ' ' + r + ' 0 0 1 0 ' + r + ' A' + rx + ' ' + r + ' 0 0 ' + (k > 0 ? 0 : 1) + ' 0 ' + (-r) + 'Z', fill: cor }, svg);
  }
  $$('svg[data-fase]').forEach(function (s) { fase(s, +s.dataset.fase, '#E9D29A'); });

  /* ---------- vídeos: carregam perto da tela, tocam só quando visíveis ---------- */
  // H.264 primeiro; navegador sem H.264 recebe a versão WebM (VP9)
  var podeMp4 = !!document.createElement('video').canPlayType('video/mp4; codecs="avc1.42E01E"');
  function carregar(v) { if (v.dataset.src && !v.getAttribute('src')) { v.src = podeMp4 ? v.dataset.src : v.dataset.src.replace(/\.mp4$/, '.webm'); } }
  function tocar(v) { carregar(v); var p = v.play(); if (p && p.catch) p.catch(function () {}); }
  var filmePausado = false;
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var v = e.target;
        if (e.isIntersecting) {
          if (v.hasAttribute('autoplay') || v.id === 'filmeVideo') { if (!(v.id === 'filmeVideo' && filmePausado)) tocar(v); }
          else carregar(v);
        }
        else if (!v.paused) v.pause();
      });
    }, { rootMargin: '200px 0px' });
    $$('video[data-src]').forEach(function (v) { if (!v.closest('.carta')) io.observe(v); });
  } else { $$('video[data-src]').forEach(carregar); }

  /* ---------- 1 · acender: o traço desenha a chama sobre o pavio, ela se enche e tremula ---------- */
  var hero = $('.hero'), quadro = $('#quadro');
  var dChama = (window.ALMAH_SVG.chama.match(/ d="([^"]+)"/) || [])[1];
  var mexe = $('#mexe'), fCheia = $('#fCheia'), fTraco = $('#fTracoP'), fBrilho = $('#fBrilhoP');
  var luzCena = $('#luzCena'), veu = $('#veu'), turb = $('#turb'), lados = $$('.hero .lado');
  [fCheia, fTraco, fBrilho].forEach(function (p) { p.setAttribute('d', dChama); });
  var L = fTraco.getTotalLength();
  fTraco.style.strokeDasharray = L + ' ' + L;
  var BX = 95, BY = 395;            // fundo da gota, que fica no pavio
  var inclina = 0, inclinaAlvo = 0;  // a chama se curva de leve para o lado do ponteiro
  function chamaEm(t) {
    var acende = suave(prog(t, .5, 2.3)), enche = suave(prog(t, 2.0, 3.0)), luz = suave(prog(t, 1.8, 3.4));
    var a = 3.2 * Math.sin(TAU * .5 * t) + 1.6 * Math.sin(TAU * 1.25 * t + 1.1) + .7 * Math.sin(TAU * 2.75 * t + .4);
    var sy = 1 + .035 * Math.sin(TAU * .75 * t + .6) + .018 * Math.sin(TAU * 2.25 * t + 2.0);
    var lz = .9 + .06 * Math.sin(TAU * 1.75 * t + .3) + .04 * Math.sin(TAU * 3.25 * t + 1.7);
    var k = .25 + .75 * enche;
    inclina += (inclinaAlvo - inclina) * .06;
    mexe.setAttribute('transform', 'translate(' + BX + ' ' + BY + ') skewX(' + (a * k + inclina * enche).toFixed(3) + ') scale(' +
      (1 + (1 / Math.sqrt(sy) - 1) * k).toFixed(4) + ' ' + (1 + (sy - 1) * k).toFixed(4) + ') translate(' + (-BX) + ' ' + (-BY) + ')');
    turb.setAttribute('seed', 1 + (Math.floor(t * 12.5) % 50));   // contorno "fervendo", como animação à mão
    fTraco.style.strokeDashoffset = (L * (1 - acende)).toFixed(1);
    fTraco.style.opacity = (1 - .85 * enche).toFixed(3);
    fCheia.style.opacity = enche.toFixed(3);
    fBrilho.style.opacity = (.55 * enche * lz).toFixed(3);
    luzCena.style.opacity = (luz * lz).toFixed(3);
    veu.style.opacity = (.18 * (1 - luz)).toFixed(3);
  }
  function textoEm(t) { // o nome e as frases entram depois da chama; só durante a abertura
    lados.forEach(function (e, i) { var d = suave(prog(t, 2.6 + i * .3, 3.8 + i * .3)); e.style.opacity = d; e.style.transform = 'translateY(' + ((1 - d) * 14).toFixed(1) + 'px)'; });
  }
  var inicio = 0, heroNaTela = true, rodando = false;
  function quadroHero(agora) {
    if (!inicio) inicio = agora;
    var t = (agora - inicio) / 1000;
    chamaEm(t > 3.6 ? 3.6 + ((t - 3.6) % 4) : t);   // o tremular fecha o laço a cada 4 s
    if (t < 4.6) textoEm(t);
    if (heroNaTela) requestAnimationFrame(quadroHero); else rodando = false;
  }
  function acender() {
    if (reduz) { chamaEm(3.6); textoEm(9); return; }
    inicio = 0;
    if (!rodando) { rodando = true; requestAnimationFrame(quadroHero); }
  }
  quadro.addEventListener('click', acender);
  if (window.matchMedia('(pointer: fine)').matches && !reduz) {
    hero.addEventListener('pointermove', function (e) {
      var r = quadro.getBoundingClientRect();
      var cx = r.left + r.width * (716 / 1600);
      inclinaAlvo = Math.max(-1, Math.min(1, (e.clientX - cx) / (innerWidth * .5))) * 7;
    });
    hero.addEventListener('pointerleave', function () { inclinaAlvo = 0; });
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      heroNaTela = es[0].isIntersecting;
      if (heroNaTela && !rodando && !reduz) { rodando = true; requestAnimationFrame(quadroHero); }
    }).observe(hero);
  }
  if (document.readyState !== 'loading') acender(); else document.addEventListener('DOMContentLoaded', acender);

  /* âncoras: rolagem suave feita aqui, não no CSS */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (!a) return;
    var alvo = document.querySelector(a.getAttribute('href'));
    if (!alvo) return;
    e.preventDefault();
    alvo.scrollIntoView({ behavior: reduz ? 'auto' : 'smooth' });
  });

  /* luz que acompanha o cursor */
  var luz = $('#luz');
  if (window.matchMedia('(pointer: fine)').matches && !reduz) {
    window.addEventListener('pointermove', function (e) {
      luz.style.transform = 'translate(' + e.clientX + 'px,' + e.clientY + 'px)';
      body.classList.add('com-luz');
    }, { passive: true });
    document.addEventListener('pointerleave', function () { body.classList.remove('com-luz'); });
  }

  /* ---------- navegação: aparece depois da abertura, troca de cor com o fundo ---------- */
  var secoes = $$('[data-tema]');
  var nav = $('.nav');
  var pendente = false;
  function aoRolar() {
    pendente = false;
    var y = window.scrollY, alto = document.documentElement.scrollHeight - innerHeight;
    body.classList.toggle('nav-on', y > innerHeight * .55);
    nav.style.setProperty('--p', alto > 0 ? Math.min(1, y / alto).toFixed(4) : 0);
    var claro = false;
    for (var i = 0; i < secoes.length; i++) {
      var r = secoes[i].getBoundingClientRect();
      if (r.top <= 40 && r.bottom > 40) { claro = secoes[i].dataset.tema === 'claro'; break; }
    }
    body.classList.toggle('nav-claro', claro);
  }
  window.addEventListener('scroll', function () { if (!pendente) { pendente = true; requestAnimationFrame(aoRolar); } }, { passive: true });
  aoRolar();

  /* ---------- 3 · construção do símbolo: R, r, eixo e o círculo da gota ---------- */
  var guias = (function () {
    var S = window.ALMAH_SVG;
    var dLua = S.lua.match(/ d="([^"]+)"/)[1], dCh = S['chama-simbolo'].match(/ d="([^"]+)"/)[1];
    var cx0 = 360, cy0 = -40, W = 580, H = 600;
    var svg = el('svg', { viewBox: cx0 + ' ' + cy0 + ' ' + W + ' ' + H, 'aria-hidden': 'true' }, $('#tracoDesenho'));
    var tmp = el('path', { d: dLua, fill: 'none' }, svg), Lt = tmp.getTotalLength(), pts = [];
    for (var i = 0; i < 720; i++) { var p = tmp.getPointAtLength(Lt * i / 720); pts.push([p.x, p.y]); }
    svg.removeChild(tmp);
    function ajusta(ps) { // círculo por mínimos quadrados
      var sx = 0, sy = 0, sxx = 0, syy = 0, sxy = 0, sz = 0, sxz = 0, syz = 0, n = ps.length;
      ps.forEach(function (q) { var x = q[0], y = q[1], z = x * x + y * y; sx += x; sy += y; sxx += x * x; syy += y * y; sxy += x * y; sz += z; sxz += x * z; syz += y * z; });
      var A = [[sxx, sxy, sx], [sxy, syy, sy], [sx, sy, n]], b = [-sxz, -syz, -sz];
      function det(m) { return m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]); }
      function troca(m, c, v) { return m.map(function (l, r) { return l.map(function (x, j) { return j === c ? v[r] : x; }); }); }
      var D = det(A), Dd = det(troca(A, 0, b)) / D, Ee = det(troca(A, 1, b)) / D, Ff = det(troca(A, 2, b)) / D;
      var cx = -Dd / 2, cy = -Ee / 2; return [cx, cy, Math.sqrt(cx * cx + cy * cy - Ff)];
    }
    var g0 = [644.5, 279.5, 224.5];
    var O = ajusta(pts.filter(function (q) { return Math.abs(Math.hypot(q[0] - g0[0], q[1] - g0[1]) - g0[2]) < 7; }));
    var I = ajusta(pts.filter(function (q) { return Math.hypot(q[0] - O[0], q[1] - O[1]) < O[2] - 8; }));
    var tmp2 = el('path', { d: dCh, fill: 'none' }, svg), L2 = tmp2.getTotalLength(), pc = [];
    for (i = 0; i < 400; i++) { var q = tmp2.getPointAtLength(L2 * i / 400); if (q.y > 300) pc.push([q.x, q.y]); }
    svg.removeChild(tmp2);
    var G = ajusta(pc), eixo = 652.5, guia = '#1D7053', tinta = '#503B69';
    var grade = el('g', { stroke: tinta, 'stroke-width': .5, 'stroke-opacity': .08 }, svg);
    for (var x = cx0; x <= cx0 + W; x += 20) el('line', { x1: x, y1: cy0, x2: x, y2: cy0 + H }, grade);
    for (var y = cy0; y <= cy0 + H; y += 20) el('line', { x1: cx0, y1: y, x2: cx0 + W, y2: y }, grade);
    var linhas = [
      el('line', { x1: cx0, y1: O[1], x2: cx0 + W, y2: O[1], stroke: guia, 'stroke-width': .8, 'stroke-dasharray': '4 5', opacity: .55 }, svg),
      el('line', { x1: eixo, y1: cy0, x2: eixo, y2: cy0 + H, stroke: guia, 'stroke-width': .8, 'stroke-dasharray': '4 5', opacity: .55 }, svg)
    ];
    var circ = [O, I].map(function (c) { return el('circle', { cx: c[0], cy: c[1], r: c[2], fill: 'none', stroke: guia, 'stroke-width': 1.1 }, svg); });
    circ.push(el('circle', { cx: G[0], cy: G[1], r: G[2], fill: 'none', stroke: guia, 'stroke-width': .9 }, svg));
    var formas = [el('path', { d: dLua, fill: tinta }, svg), el('path', { d: dCh, fill: tinta }, svg)];
    var m = el('g', { fill: guia, 'font-family': 'Poppins', 'font-size': 12, 'letter-spacing': '1' }, svg);
    el('circle', { cx: O[0], cy: O[1], r: 3 }, m); el('circle', { cx: I[0], cy: I[1], r: 3 }, m);
    var aO = 205 * Math.PI / 180, aI = 25 * Math.PI / 180;
    el('line', { x1: O[0], y1: O[1], x2: O[0] + O[2] * Math.cos(aO), y2: O[1] + O[2] * Math.sin(aO), stroke: guia, 'stroke-width': .8 }, m);
    el('line', { x1: I[0], y1: I[1], x2: I[0] + I[2] * Math.cos(aI), y2: I[1] + I[2] * Math.sin(aI), stroke: guia, 'stroke-width': .8 }, m);
    el('text', { x: O[0] + O[2] * .5 * Math.cos(aO) - 4, y: O[1] + O[2] * .5 * Math.sin(aO) - 8 }, m).textContent = 'R';
    el('text', { x: I[0] + I[2] * .5 * Math.cos(aI) + 2, y: I[1] + I[2] * .5 * Math.sin(aI) - 8 }, m).textContent = 'r';
    el('text', { x: eixo + 8, y: cy0 + 24 }, m).textContent = 'eixo';
    circ.forEach(function (c) { var l = TAU * +c.getAttribute('r'); c.style.strokeDasharray = l + ' ' + l; c.dataset.l = l; });
    return { circ: circ, linhas: linhas, formas: formas, marcas: m };
  })();

  /* ---------- 6 · crie seu rótulo ---------- */
  var rot = $('#rotuloVivo'), rNome = $('#rNome'), rAroma = $('#rAroma'), rPeso = $('#rPeso');
  var cNome = $('#campoNome'), cAroma = $('#campoAroma');
  function atualizarRotulo() {
    var nome = (cNome.value.trim() || 'Almah').toUpperCase();
    rNome.textContent = nome;
    var n = nome.length;
    rNome.style.setProperty('--tam', (n <= 6 ? 15 : Math.max(7.6, 15 * 6.4 / n)).toFixed(2) + 'cqi');
    rAroma.textContent = cAroma.value.trim() || 'aroma';
    var cor = ($('input[name=cor]:checked') || {}).value || '#503B6A';
    rot.style.setProperty('--c', cor);
    rPeso.textContent = ($('input[name=peso]:checked') || {}).value || '150g';
  }
  $('#formRotulo').addEventListener('input', atualizarRotulo);
  $('#formRotulo').addEventListener('change', atualizarRotulo);
  $('#formRotulo').addEventListener('submit', function (e) { e.preventDefault(); });
  var CEU = [['Lyra', 'flor de laranjeira'], ['Aurora', 'bergamota'], ['Íris', 'violeta'], ['Estela', 'jasmim'], ['Luna', 'algodão'], ['Nyx', 'âmbar e baunilha'],
    ['Ceres', 'trigo e mel'], ['Gaia', 'alecrim'], ['Órion', 'cedro'], ['Vega', 'chá branco'], ['Maia', 'figo'], ['Sírius', 'pimenta rosa'], ['Andrômeda', 'flor de cerejeira'], ['Atena', 'oliveira']];
  $('#sortear').addEventListener('click', function () {
    var atual = cNome.value.trim().toLowerCase(), par;
    do { par = CEU[Math.floor(Math.random() * CEU.length)]; } while (par[0].toLowerCase() === atual);
    cNome.value = par[0]; cAroma.value = par[1];
    var cores = $$('input[name=cor]'); cores[Math.floor(Math.random() * cores.length)].checked = true;
    atualizarRotulo();
    if (temGsap) gsap.fromTo(rot, { rotate: -2, scale: .97 }, { rotate: 0, scale: 1, duration: .7, ease: 'back.out(2)' });
  });
  atualizarRotulo();

  /* ---------- 7 · paleta: copiar o código ---------- */
  var toast = $('#toast'), tToast;
  function avisar(t) { toast.textContent = t; toast.classList.add('on'); clearTimeout(tToast); tToast = setTimeout(function () { toast.classList.remove('on'); }, 1800); }
  $$('#paleta .chip').forEach(function (c) {
    c.addEventListener('click', function () {
      var hex = c.dataset.hex;
      try {
        navigator.clipboard.writeText(hex).then(function () { avisar('Copiado: ' + hex); }, function () { avisar('Código: ' + hex); });
      } catch (e) { avisar('Código: ' + hex); }
    });
  });

  /* ---------- 8 · filme ---------- */
  var filme = $('#filmeVideo');
  $('#filmePlay').addEventListener('click', function () {
    if (filme.paused) { filmePausado = false; tocar(filme); this.textContent = 'Pausar'; }
    else { filmePausado = true; filme.pause(); this.textContent = 'Assistir'; }
  });

  /* ---------- 4 · coleção: virar as cartas; a prateleira aponta para a carta ---------- */
  var colecao = $('#colecao'), cartas = $$('.carta');
  function virar(c, forcar) {
    var vira = forcar || !c.classList.contains('virada');
    $$('.carta.virada').forEach(function (o) {
      if (o === c && forcar) return;
      o.classList.remove('virada'); o.setAttribute('aria-pressed', 'false');
      var vv = $('video', o); if (vv) vv.pause();
    });
    if (vira) {
      c.classList.add('virada'); c.setAttribute('aria-pressed', 'true');
      colecao.style.setProperty('--fundo', c.dataset.cor); colecao.classList.add('virada');
      var v = $('video', c); if (v) tocar(v);
    } else {
      colecao.style.removeProperty('--fundo'); colecao.classList.remove('virada');
    }
  }
  cartas.forEach(function (c) { c.addEventListener('click', function () { virar(c); }); });
  $$('.ponto').forEach(function (p) {
    p.addEventListener('click', function () {
      var c = cartas[+p.dataset.carta];
      $('#baralho').scrollIntoView({ behavior: reduz ? 'auto' : 'smooth', block: 'center' });
      setTimeout(function () { virar(c, true); if (c.scrollIntoView) c.scrollIntoView({ behavior: reduz ? 'auto' : 'smooth', block: 'nearest', inline: 'center' }); }, reduz ? 0 : 650);
    });
  });

  /* ---------- 5 · a caixa: cada etapa troca a foto ---------- */
  var fotosC = $$('#fotosCaixa img'), etapas = $$('.etapa');
  function irEtapa(i) {
    etapas.forEach(function (e) { e.classList.toggle('ativa', +e.dataset.i === i); });
    fotosC.forEach(function (f) { f.classList.toggle('ativa', +f.dataset.i === i); });
  }
  if ('IntersectionObserver' in window) {
    var ioE = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) irEtapa(+e.target.dataset.i); });
    }, { rootMargin: '-45% 0px -45% 0px' });
    etapas.forEach(function (e) { ioE.observe(e); });
  }

  /* ---------- rodapé: acender de novo ---------- */
  $('#deNovo').addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: reduz ? 'auto' : 'smooth' });
    setTimeout(acender, reduz ? 0 : 900);
  });

  if (!temGsap) return;

  /* ================= daqui para baixo, só com GSAP ================= */

  /* abertura: a foto se aproxima e o texto sai na rolagem */
  gsap.to('.hero .quadro svg', { scale: 1.08, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
  gsap.fromTo('.hero .lado, .rolar', { y: 0, autoAlpha: 1 }, { y: -60, autoAlpha: 0, ease: 'none', immediateRender: false, scrollTrigger: { trigger: '.hero', start: '30% top', end: '85% top', scrub: true } });

  /* manifesto: a luz passa pelas palavras */
  var tx = $('#manifestoTexto');
  tx.innerHTML = tx.textContent.split(' ').map(function (w) { return '<span class="p">' + w + '</span>'; }).join(' ');
  gsap.fromTo('#manifestoTexto .p', { opacity: .2 }, { opacity: 1, stagger: .1, ease: 'none', scrollTrigger: { trigger: tx, start: 'top 80%', end: 'bottom 45%', scrub: true } });

  /* do traço à luz: esboço, construção desenhada, projeção */
  var cam = $$('.traco .camada'), fal = $$('.traco .fala');
  gsap.set(guias.circ, { strokeDashoffset: function (i, c) { return +c.dataset.l; } });
  gsap.set(guias.formas.concat(guias.linhas, [guias.marcas]), { opacity: 0 });
  var tt = gsap.timeline({ scrollTrigger: { trigger: '#traco', start: 'top top', end: '+=260%', pin: '.traco .fixo', scrub: 1, anticipatePin: 1 } });
  tt.to(cam[0].querySelector('img'), { scale: 1.06, duration: 1, ease: 'none' }, 0)
    .to(cam[1], { opacity: 1, duration: .25 }, .8).to(fal[0], { opacity: 0, y: -14, duration: .2 }, .8).fromTo(fal[1], { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .2 }, .95)
    .to(guias.linhas, { opacity: .55, duration: .2 }, 1.05)
    .to(guias.circ, { strokeDashoffset: 0, duration: .6, stagger: .12, ease: 'none' }, 1.1)
    .to(guias.marcas, { opacity: 1, duration: .2 }, 1.5)
    .to(guias.formas, { opacity: .94, duration: .35, stagger: .15 }, 1.6)
    .to(cam[2], { opacity: 1, duration: .3 }, 2.3).to(fal[1], { opacity: 0, y: -14, duration: .2 }, 2.3).fromTo(fal[2], { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .2 }, 2.45)
    .fromTo(cam[2].querySelector('img'), { scale: 1.08 }, { scale: 1, duration: .9, ease: 'none' }, 2.3);

  /* coleção: as cartas são dadas do baralho */
  cartas.forEach(function (c, i) {
    var r = parseFloat(getComputedStyle(c).getPropertyValue('--rot')) || 0;
    gsap.fromTo(c, { '--dy': '220px', '--dr': (-r) + 'deg', opacity: 0 }, {
      '--dy': '0px', '--dr': '0deg', opacity: 1, duration: 1.1, ease: 'power3.out', delay: i * .09,
      scrollTrigger: { trigger: '#baralho', start: 'top 82%' }
    });
  });
  gsap.from('.linha img', { scale: 1.08, ease: 'none', scrollTrigger: { trigger: '.linha', start: 'top bottom', end: 'bottom top', scrub: true } });

  /* entradas suaves */
  $$('.colecao .topo, .caixa .cab, .oficina .grade > div, .marca-sec h2, .marca-sec .grade > *, .papelaria img, .filme .grade > *').forEach(function (e) {
    gsap.from(e, { y: 40, opacity: 0, duration: 1.1, ease: 'power3.out', scrollTrigger: { trigger: e, start: 'top 88%' } });
  });

  /* imagens que chegam depois mudam a altura: recalcula */
  var t0; function rec() { clearTimeout(t0); t0 = setTimeout(function () { ScrollTrigger.refresh(); }, 200); }
  $$('img').forEach(function (im) { if (!im.complete) im.addEventListener('load', rec); });
  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
})();
