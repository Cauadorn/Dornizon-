/* Bem-Querer · comportamento comum a todas as páginas. Cada parte só roda se o elemento existir. */
document.addEventListener('DOMContentLoaded', function () {
  var reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fino = matchMedia('(hover: hover) and (pointer: fine)').matches;
  var celular = matchMedia('(max-width: 900px)').matches;
  var G = window.gsap && !reduz ? window.gsap : null, lenis = null;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  if (G) {
    G.registerPlugin(ScrollTrigger);
    if (window.Lenis) {
      lenis = new Lenis({ lerp: .09 });
      lenis.on('scroll', ScrollTrigger.update);
      G.ticker.add(function (t) { lenis.raf(t * 1000); });
      G.ticker.lagSmoothing(0);
    }
  }

  /* ---- topo, menu e transição entre páginas ---- */
  var topo = $('.topo'), hero = $('.hero');
  function fundoTopo() { topo.classList.toggle('solido', scrollY > (hero ? innerHeight * 1.6 : 40)); }
  addEventListener('scroll', fundoTopo, { passive: true }); fundoTopo();
  var bt = $('.topo .pilula'), menu = $('#menu');
  function abre(sim) { menu.classList.toggle('aberto', sim); bt.setAttribute('aria-expanded', sim); if (lenis) { sim ? lenis.stop() : lenis.start(); } }
  bt.addEventListener('click', function () { abre(!menu.classList.contains('aberto')); });
  addEventListener('keydown', function (e) { if (e.key === 'Escape') abre(false); });

  var cortina = $('.cortina');
  function vaiPara(alvo) {
    var sp = alvo.closest('.pin-spacer'), y = (sp || alvo).getBoundingClientRect().top + scrollY;
    if (lenis) lenis.scrollTo(y, { duration: 1.4 }); else scrollTo({ top: y, behavior: reduz ? 'auto' : 'smooth' });
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href]');
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank') return;
    var href = a.getAttribute('href');
    if (href.charAt(0) === '#') {
      var alvo = href.length > 1 && document.getElementById(href.slice(1));
      if (alvo) { e.preventDefault(); abre(false); vaiPara(alvo); }
      return;
    }
    if (/^(https?:|mailto:)/.test(href) || !cortina || reduz) return;
    e.preventDefault();
    try { sessionStorage.setItem('bq-cortina', '1'); } catch (er) {}
    cortina.classList.add('cobre');
    setTimeout(function () { location.href = a.href; }, 560);
  });
  addEventListener('pageshow', function (e) { if (e.persisted && cortina) cortina.classList.remove('cobre'); });

  /* ---- foto que acompanha o mouse nas listas ---- */
  var fm = $('.foto-mouse');
  if (fm && fino) {
    var fx = G ? G.quickTo(fm, 'left', { duration: .5, ease: 'power3' }) : function (v) { fm.style.left = v + 'px'; };
    var fy = G ? G.quickTo(fm, 'top', { duration: .5, ease: 'power3' }) : function (v) { fm.style.top = v + 'px'; };
    $$('[data-img]').forEach(function (li) {
      li.addEventListener('pointerenter', function () { fm.src = li.dataset.img; fm.classList.add('on'); });
      li.addEventListener('pointerleave', function () { fm.classList.remove('on'); });
    });
    addEventListener('pointermove', function (e) { fx(e.clientX + 150); fy(e.clientY); });
  }

  /* ---- encontre o coração ---- */
  var busca = $('.busca');
  if (busca) {
    var btc = $('.bt-claro', busca);
    var achou = function (sim) { busca.classList.toggle('achou', sim); btc.textContent = sim ? 'esconder de novo' : 'mostrar o coração'; };
    btc.addEventListener('click', function () { achou(!busca.classList.contains('achou')); });
    $('.alvo', busca).addEventListener('click', function () { achou(true); });
  }

  /* ---- início: carregador e a janela com as ilustrações inteiras (vídeo quando houver) ---- */
  if (hero) {
    var ims = $$('.janela > *'), k = 0, leg = $('.janela-leg'), troca = null;
    var legenda = function (m) { if (leg) leg.innerHTML = '<b>' + m.dataset.n + '</b> · ' + m.dataset.nome + ' · ' + m.dataset.est; };
    var mostraMidia = function (i) {
      var velho = ims[k]; velho.classList.remove('on'); if (velho.pause) velho.pause();
      k = (i + ims.length) % ims.length;
      var m = ims[k];
      m.classList.add('on'); legenda(m);
      clearTimeout(troca);
      if (reduz) return;
      if (m.tagName === 'VIDEO') {
        m.currentTime = 0;
        m.onended = function () { mostraMidia(k + 1); };
        var pr = m.play(); if (pr && pr.catch) pr.catch(function () { troca = setTimeout(function () { mostraMidia(k + 1); }, 3200); });
      } else troca = setTimeout(function () { mostraMidia(k + 1); }, 3200);
    };
    legenda(ims[0]);
    var entrada = function () {
      mostraMidia(0);
      if (!G) return;
      G.from('.p-bem', { xPercent: -14, opacity: 0, duration: 1.4, ease: 'expo.out' });
      G.from('.p-querer', { xPercent: 14, opacity: 0, duration: 1.4, ease: 'expo.out' });
      G.fromTo('.janela', { clipPath: 'inset(100% 0% 0% 0% round 999px 999px 0px 0px)' }, { clipPath: 'inset(0% 0% 0% 0% round 999px 999px 0px 0px)', duration: 1.6, ease: 'expo.out', clearProps: 'clipPath' });
      G.from('.hero .rodape-h', { opacity: 0, y: 20, duration: 1, delay: .5 });
      G.from('.janela-leg', { opacity: 0, duration: 1, delay: .7 });
    };
    var cl = $('.carrega'), visto = false;
    try { visto = sessionStorage.getItem('bq-visto') === '1'; sessionStorage.setItem('bq-visto', '1'); } catch (e) {}
    if (cl && !visto) {
      var pct = $('.pct', cl), clS = $('.cl', cl), feitas = 0, mostrado = 0, acabou = false;
      var mostra = function (v) { pct.textContent = v; clS.style.setProperty('--p', v + '%'); };
      var fim = function () { if (acabou) return; acabou = true; mostra(100); setTimeout(function () { cl.classList.add('foi'); entrada(); }, reduz ? 0 : 500); };
      var conta = function () {
        feitas++;
        var alvo = Math.round(feitas / ims.length * 100);
        if (G) G.to({ v: mostrado }, { v: alvo, duration: .6, ease: 'power2.out', onUpdate: function () { mostrado = Math.round(this.targets()[0].v); mostra(mostrado); } });
        else mostra(alvo);
        if (feitas >= ims.length) setTimeout(fim, G ? 650 : 0);
      };
      ims.forEach(function (m) {
        if (m.tagName === 'VIDEO') { if (m.readyState >= 1) conta(); else { m.addEventListener('loadedmetadata', conta, { once: true }); m.addEventListener('error', conta, { once: true }); } }
        else if (m.complete) conta(); else { m.addEventListener('load', conta); m.addEventListener('error', conta); }
      });
      setTimeout(fim, 4500);
    } else {
      if (cl) cl.classList.add('foi');
      entrada();
    }
    if (G) {
      var tl = G.timeline({ scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: .8 } });
      tl.to('.p-bem', { xPercent: -40, opacity: 0, ease: 'none' }, 0)
        .to('.p-querer', { xPercent: 40, opacity: 0, ease: 'none' }, 0)
        .to('.janela > *', { scale: 1.1, ease: 'none' }, 0)
        .to('.hero .rodape-h, .janela-leg', { opacity: 0, ease: 'none', duration: .3 }, 0);
    }
  } else {
    var cl2 = $('.carrega'); if (cl2) cl2.remove();
  }

  /* ---- vídeos fora da abertura: tocam só quando aparecem ---- */
  var vids = $$('video[data-auto]');
  if (vids.length && !reduz && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) { if (x.isIntersecting) { var pr = x.target.play(); if (pr && pr.catch) pr.catch(function () {}); } else x.target.pause(); });
    }, { threshold: .25 });
    vids.forEach(function (v) { io.observe(v); });
  }

  /* ---- a roda dos pares ---- */
  var roda = $('.roda');
  if (roda) {
    var itens = $$('.item', roda), N = itens.length, passo = 360 / N, irPara;
    var aro = $('.aro', roda), anel = $('.anel', roda), info = $('.roda-info', roda);
    var nEl = $('.n', info), nmEl = $('strong', info), esEl = $('em', info), ver = $('.r-ver', info), atual = -1;
    var gira = function (phi) {
      aro.style.transform = 'rotate(' + (-phi) + 'deg)';
      anel.style.transform = 'rotate(' + (phi * .5) + 'deg)';
      itens.forEach(function (it, i) {
        var d = ((i * passo - phi) % 360 + 540) % 360 - 180;
        it.style.setProperty('--s', (1 + .24 * Math.max(0, 1 - Math.abs(d) / (passo * 1.1))).toFixed(3));
      });
      var kk = ((Math.round(phi / passo) % N) + N) % N;
      if (kk !== atual) { atual = kk; var it = itens[kk]; nEl.textContent = it.dataset.n; nmEl.textContent = it.dataset.nome; esEl.textContent = it.dataset.est; ver.href = it.getAttribute('href'); }
    };
    gira(0);
    /* a roda gira arrastando para o lado, tocando num par vizinho ou nas setas; a página não prende a rolagem */
    var arena = $('.roda-arena', roda), phi = 0, alvo = 0, raf = null;
    var anima = function () {
      phi += (alvo - phi) * (reduz ? 1 : .16);
      if (Math.abs(alvo - phi) < .03) phi = alvo;
      gira(phi);
      raf = phi === alvo ? null : requestAnimationFrame(anima);
    };
    var animaPara = function (p) { alvo = p; if (!raf) raf = requestAnimationFrame(anima); };
    irPara = function (n) {
      var base = Math.round(alvo / passo), d = (((n - base) % N) + N) % N;
      if (d > N / 2) d -= N;
      animaPara((base + d) * passo);
    };
    var ativo = false, arrastou = false, x0 = 0, p0 = 0, grausPorPx = .2, ux = 0, ut = 0, vel = 0;
    arena.addEventListener('pointerdown', function (e) {
      if (e.button) return;
      var a = aro.getBoundingClientRect(), r = itens[0].getBoundingClientRect();
      var R = Math.hypot(r.left + r.width / 2 - a.left, r.top + r.height / 2 - a.top) || 300;
      grausPorPx = 180 / (Math.PI * R);
      ativo = true; arrastou = false; x0 = ux = e.clientX; ut = performance.now(); vel = 0; p0 = phi;
      if (raf) { cancelAnimationFrame(raf); raf = null; }
      alvo = phi;
    });
    addEventListener('pointermove', function (e) {
      if (!ativo) return;
      var dx = e.clientX - x0;
      if (!arrastou && Math.abs(dx) > 6) { arrastou = true; arena.classList.add('arrastando'); }
      if (!arrastou) return;
      var t = performance.now();
      vel = (e.clientX - ux) / Math.max(1, t - ut); ux = e.clientX; ut = t;
      phi = alvo = p0 - dx * grausPorPx;
      gira(phi);
    });
    addEventListener('pointerup', function () {
      if (!ativo) return;
      ativo = false; arena.classList.remove('arrastando');
      if (arrastou) { var proj = phi - vel * 160 * grausPorPx; animaPara(Math.round(proj / passo) * passo); }
    });
    addEventListener('pointercancel', function () { if (ativo) { ativo = false; arena.classList.remove('arrastando'); animaPara(Math.round(phi / passo) * passo); } });
    itens.forEach(function (it, i) {
      it.addEventListener('click', function (e) {
        if (arrastou) { e.preventDefault(); e.stopPropagation(); arrastou = false; return; }
        if (i !== atual) { e.preventDefault(); e.stopPropagation(); irPara(i); }
      }, true);
      $('img', it).setAttribute('draggable', 'false');
      it.setAttribute('draggable', 'false');   /* link arrastável cancelaria o gesto no computador */
    });
    arena.addEventListener('dragstart', function (e) { e.preventDefault(); });
    arena.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); irPara(atual + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); irPara(atual - 1); }
    });
    $('.r-prox', roda).addEventListener('click', function () { irPara(atual + 1); });
    $('.r-ant', roda).addEventListener('click', function () { irPara(atual - 1); });
  }

  if (!G) return;

  /* ---- manifesto: as palavras acendem ---- */
  var mt = $('.m-txt');
  if (mt) {
    var partes = [];
    [].slice.call(mt.childNodes).forEach(function (n) {
      if (n.nodeType === 3) {
        n.textContent.split(/(\s+)/).forEach(function (w) {
          if (!w) return;
          if (/^\s+$/.test(w)) { partes.push(document.createTextNode(w)); return; }
          var s = document.createElement('span'); s.className = 'w'; s.textContent = w; partes.push(s);
        });
      } else { if (n.classList) n.classList.add('w'); partes.push(n); }
    });
    mt.textContent = ''; partes.forEach(function (p) { mt.appendChild(p); });
    G.fromTo($$('.w', mt), { opacity: .14 }, { opacity: 1, stagger: .05, ease: 'none', scrollTrigger: { trigger: mt, start: 'top 80%', end: 'bottom 45%', scrub: true } });
  }

  /* ---- abertura das páginas internas ---- */
  var ph = $$('.pg-hero > *, .e-hero .cena-txt > *');
  if (ph.length) G.from(ph, { y: 46, opacity: 0, duration: 1.2, stagger: .08, ease: 'power3.out', delay: .25 });
  var eh = $('.e-hero');
  if (eh) {
    G.fromTo('.e-hero .arco-ilu', { clipPath: 'inset(100% 0% 0% 0% round 999px 999px 0px 0px)' }, { clipPath: 'inset(0% 0% 0% 0% round 999px 999px 0px 0px)', duration: 1.6, ease: 'expo.out', delay: .2, clearProps: 'clipPath' });
    G.from('.e-hero .par-flutua', { y: 160, rotation: 24, opacity: 0, duration: 1.6, ease: 'expo.out', delay: .5 });
    G.to('.e-hero .par-flutua', { y: -90, ease: 'none', scrollTrigger: { trigger: eh, start: 'top top', end: 'bottom top', scrub: true } });
  }
  $$('.cinema img').forEach(function (img) {
    G.fromTo(img, { yPercent: -5 }, { yPercent: 5, ease: 'none', scrollTrigger: { trigger: img.parentNode, start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  $$('.arco-ilu img, .arco-ilu video').forEach(function (img) {
    G.fromTo(img, { yPercent: -5 }, { yPercent: 5, ease: 'none', scrollTrigger: { trigger: img.closest('section'), start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  /* ---- entradas genéricas ---- */
  $$('.moldura, .foto-est, .quadro-cor, .carta-e .arco, .trilho .arco').forEach(function (m) {
    G.fromTo(m, { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.3, ease: 'expo.out', clearProps: 'clipPath', scrollTrigger: { trigger: m, start: 'top 90%', once: true } });
  });
  $$('[data-rev], .linhas li, .evita li, .tres > div, .numeros > div, .coracoes a, .paletas a, .bloco, .caderno > *, .secao-t > *, .busca-in > div > :not(.resp), .prosa > *').forEach(function (el) {
    G.from(el, { y: 34, opacity: 0, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 92%', once: true } });
  });
  addEventListener('load', function () { ScrollTrigger.refresh(); });
});
