/* Almah · site da Coleção Gênesis
   Acender a vela na abertura, juntar lua e chama, virar as cartas, queimar a vela no ritual,
   montar um rótulo. Funciona sem GSAP (tudo visível, sem animação de rolagem). */
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduz = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var temGsap = !!(window.gsap && window.ScrollTrigger) && !reduz;
  var html = document.documentElement, body = document.body;
  html.classList.toggle('com-gsap', temGsap);
  if (temGsap) { gsap.registerPlugin(ScrollTrigger); gsap.ticker.lagSmoothing(1000, 33); }

  /* ---------- vídeos: carregam perto da tela, tocam só quando visíveis ---------- */
  // H.264 primeiro; navegador sem H.264 recebe a versão WebM (VP9)
  var podeMp4 = !!document.createElement('video').canPlayType('video/mp4; codecs="avc1.42E01E"');
  function carregar(v) { if (v.dataset.src && !v.getAttribute('src')) { v.src = podeMp4 ? v.dataset.src : v.dataset.src.replace(/\.mp4$/, '.webm'); } }
  function tocar(v) { carregar(v); var p = v.play(); if (p && p.catch) p.catch(function () {}); }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var v = e.target;
        if (e.isIntersecting) {
          if (v.id === 'chamaVideo') { if (aceso) tocar(v); }
          else if (v.hasAttribute('autoplay') || v.id === 'filmeVideo') { if (!(v.id === 'filmeVideo' && filmePausado)) tocar(v); }
          else carregar(v);
        }
        else if (!v.paused) v.pause();
      });
    }, { rootMargin: '200px 0px' });
    $$('video[data-src]').forEach(function (v) { if (!v.closest('.carta')) io.observe(v); });
  } else { $$('video[data-src]').forEach(carregar); }

  /* ---------- 1 · acender ---------- */
  var chama = $('#chamaVideo');
  carregar(chama);
  var aceso = false, timerAcender;
  function acender() {
    if (aceso) return;
    aceso = true; clearTimeout(timerAcender);
    body.classList.add('aceso');
    var p = chama.play(); if (p && p.catch) p.catch(function () {});
    $('#pavio').setAttribute('aria-label', 'Vela acesa');
  }
  function apagar() {
    aceso = false; body.classList.remove('aceso'); chama.pause();
    $('#pavio').setAttribute('aria-label', 'Acender a vela');
  }
  $('#pavio').addEventListener('click', function () { aceso ? apagar() : acender(); });
  timerAcender = setTimeout(acender, reduz ? 0 : 2600);

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

  /* ---------- 7 · crie seu rótulo ---------- */
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

  /* ---------- 8 · paleta: copiar o código ---------- */
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

  /* ---------- 9 · filme ---------- */
  var filme = $('#filmeVideo'), filmePausado = false;
  $('#filmePlay').addEventListener('click', function () {
    if (filme.paused) { filmePausado = false; tocar(filme); this.textContent = 'Pausar'; }
    else { filmePausado = true; filme.pause(); this.textContent = 'Assistir'; }
  });

  /* ---------- 4 · coleção: virar as cartas ---------- */
  var colecao = $('#colecao');
  $$('.carta').forEach(function (c) {
    c.addEventListener('click', function () {
      var virar = !c.classList.contains('virada');
      $$('.carta.virada').forEach(function (o) {
        o.classList.remove('virada'); o.setAttribute('aria-pressed', 'false');
        var vv = $('video', o); if (vv) vv.pause();
      });
      if (virar) {
        c.classList.add('virada'); c.setAttribute('aria-pressed', 'true');
        colecao.style.setProperty('--fundo', c.dataset.cor); colecao.classList.add('virada');
        var v = $('video', c); if (v) tocar(v);
      } else {
        colecao.style.removeProperty('--fundo'); colecao.classList.remove('virada');
      }
    });
  });

  /* ---------- rodapé: acender de novo ---------- */
  $('#deNovo').addEventListener('click', function () {
    apagar();
    window.scrollTo({ top: 0, behavior: reduz ? 'auto' : 'smooth' });
    setTimeout(acender, reduz ? 0 : 1600);
  });

  /* ---------- 5 · ritual: estados da vela ---------- */
  var vela = $('#vela'), relogio = $('#relogio');
  var ESTADO = {
    1: { nivel: 196, pavio: 170, piscina: 104 },
    2: { nivel: 196, pavio: 182, piscina: 104 },
    3: { nivel: 242, pavio: 228, piscina: 104 },
    4: { nivel: 242, pavio: 228, piscina: 104 },
    5: { nivel: 242, pavio: 228, piscina: 104 }
  };
  var passoAtual = 0;
  function irPasso(n) {
    if (n === passoAtual) return;
    passoAtual = n; vela.dataset.passo = n;
    $$('.passo').forEach(function (p) { p.classList.toggle('ativo', +p.dataset.passo === n); });
    var e = ESTADO[n], d = temGsap ? 1.4 : 0;
    var set = function (sel, attrs) { if (temGsap) gsap.to(sel, { attr: attrs, duration: d, ease: 'power2.inOut' }); else { var el = $(sel); for (var k in attrs) el.setAttribute(k, attrs[k]); } };
    set('#cera', { y: e.nivel });
    set('#topoCera', { cy: e.nivel });
    set('#piscina', { cy: e.nivel, rx: e.piscina, ry: 13 });
    set('#pavioR', { y1: e.nivel, y2: e.pavio });
    if (temGsap) {
      gsap.to('#chamaR', { y: e.pavio - 170, duration: d, ease: 'power2.inOut' });
      gsap.to('#chamaBrilho', { attr: { cy: e.pavio - 52 }, duration: d, ease: 'power2.inOut' });
      gsap.to('#fumaca', { y: e.pavio - 170, duration: .1 });
    }
    if (n === 3) contarHoras();
  }
  function contarHoras() {
    if (!temGsap) { relogio.firstChild.nodeValue = '3:00'; return; }
    var o = { m: 0 };
    gsap.to(o, { m: 180, duration: 2.2, ease: 'power1.inOut', onUpdate: function () {
      var m = Math.round(o.m); relogio.firstChild.nodeValue = Math.floor(m / 60) + ':' + String(m % 60).padStart(2, '0');
    } });
  }

  if (!temGsap) { irPasso(1); return; }

  /* ================= daqui para baixo, só com GSAP ================= */

  /* abertura: nuvens e sol se afastam na rolagem; o ponteiro mexe o céu */
  $$('.hero [data-par]').forEach(function (el) {
    gsap.to(el, { y: +el.dataset.par * 2.2, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
  });
  gsap.to('.palco', { y: -80, opacity: .25, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
  gsap.from('.palco > *', { y: 30, opacity: 0, duration: 1.3, stagger: .12, ease: 'power3.out', delay: .2 });
  if (window.matchMedia('(pointer: fine)').matches) {
    var solX = gsap.quickTo('#sol', 'x', { duration: 1.6, ease: 'power3' }), solY = gsap.quickTo('#sol', 'y', { duration: 1.6, ease: 'power3' });
    $('.hero').addEventListener('pointermove', function (e) {
      solX((e.clientX / innerWidth - .5) * -40); solY((e.clientY / innerHeight - .5) * -30);
    });
  }

  /* manifesto: a luz passa pelas palavras */
  var tx = $('#manifestoTexto');
  tx.innerHTML = tx.textContent.split(' ').map(function (w) { return '<span class="p">' + w + '</span>'; }).join(' ');
  gsap.fromTo('#manifestoTexto .p', { opacity: .2 }, { opacity: 1, stagger: .1, ease: 'none', scrollTrigger: { trigger: tx, start: 'top 80%', end: 'bottom 45%', scrub: true } });

  /* símbolo: lua e chama se encontram */
  var leg = $$('#legendas p');
  var tl = gsap.timeline({ scrollTrigger: { trigger: '#simbolo', start: 'top top', end: '+=160%', pin: true, scrub: 1, anticipatePin: 1 } });
  tl.fromTo('#pLua', { xPercent: -46, rotate: -35, opacity: .8 }, { xPercent: 0, rotate: 0, opacity: 1, duration: 1, ease: 'none' }, 0)
    .fromTo('#pChama', { xPercent: 52, yPercent: -14, scale: .8, opacity: .8 }, { xPercent: 0, yPercent: 0, scale: 1, opacity: 1, duration: 1, ease: 'none' }, 0)
    .to(leg[0], { opacity: 0, y: -12, duration: .14 }, .3)
    .fromTo(leg[1], { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .14 }, .36)
    .to(leg[1], { opacity: 0, y: -12, duration: .14 }, .72)
    .fromTo(leg[2], { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .14 }, .8)
    .fromTo('#halo', { opacity: 0, scale: .6 }, { opacity: 1, scale: 1.1, duration: .2 }, .82);

  /* coleção: as cartas são dadas do baralho */
  $$('.carta').forEach(function (c) {
    var r = parseFloat(getComputedStyle(c).getPropertyValue('--rot')) || 0;
    gsap.fromTo(c, { '--dy': '220px', '--dr': (-r) + 'deg', opacity: 0 }, {
      '--dy': '0px', '--dr': '0deg', opacity: 1, duration: 1.1, ease: 'power3.out', delay: $$('.carta').indexOf(c) * .09,
      scrollTrigger: { trigger: '#baralho', start: 'top 82%' }
    });
  });

  /* ritual: cada passo acende um estado da vela */
  $$('.passo').forEach(function (p) {
    ScrollTrigger.create({ trigger: p, start: 'top 62%', end: 'bottom 62%', onToggle: function (s) { if (s.isActive) irPasso(+p.dataset.passo); } });
  });


  /* galeria: o trilho anda de lado (tela larga) */
  var mm = gsap.matchMedia();
  mm.add('(min-width: 900px)', function () {
    html.classList.add('largo');
    var trilho = $('#trilho');
    var dist = function () { return Math.max(0, trilho.scrollWidth - innerWidth); };
    gsap.to(trilho, { x: function () { return -dist(); }, ease: 'none',
      scrollTrigger: { trigger: '#galeria', start: 'top top', end: function () { return '+=' + dist(); }, pin: true, scrub: 1, invalidateOnRefresh: true } });
    return function () { html.classList.remove('largo'); };
  });

  /* entradas suaves */
  $$('.colecao .topo, .ritual .cab, .galeria .cab, .oficina .grade > div, .marca-sec h2, .marca-sec .grade > *, .papelaria img, .filme .grade > *').forEach(function (el) {
    gsap.from(el, { y: 40, opacity: 0, duration: 1.1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 88%' } });
  });

  /* imagens que chegam depois mudam a altura: recalcula */
  var t0; function rec() { clearTimeout(t0); t0 = setTimeout(function () { ScrollTrigger.refresh(); }, 200); }
  $$('img').forEach(function (im) { if (!im.complete) im.addEventListener('load', rec); });
  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
})();
