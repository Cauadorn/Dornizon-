/* Injetado em behance.html para gravar o módulo de abertura em movimento:
   a chama de verdade dentro do arco, estrelas piscando e nuvens flutuando.
   O vídeo vai e volta (4 s para frente, 4 s para trás) para o loop não ter emenda. */
(function () {
  var mod = document.querySelector('.m1');
  var est = [].slice.call(mod.querySelectorAll('.ceu .est, .ceu .pt'));
  var nuvens = [].slice.call(mod.querySelectorAll('.nuv'));
  var video;
  window.DURACAO = 8;
  window.prepararMotion = function () {
    return new Promise(function (ok) {
      var img = mod.querySelector('.janela img');
      video = document.createElement('video');
      video.muted = true; video.playsInline = true; video.preload = 'auto';
      video.style.cssText = 'width:100%;height:100%;object-fit:cover;border-radius:999px 999px 6px 6px;display:block';
      video.src = '../site/video/chama.webm';
      video.addEventListener('loadeddata', function () { ok(); }, { once: true });
      img.replaceWith(video);
    });
  };
  function buscar(s) {
    return new Promise(function (ok) {
      if (Math.abs(video.currentTime - s) < 0.001) return ok();
      video.addEventListener('seeked', function () { requestAnimationFrame(function () { ok(); }); }, { once: true });
      video.currentTime = s;
    });
  }
  window.renderFrame = function (t) {
    var TAU = Math.PI * 2;
    est.forEach(function (e, i) { e.style.opacity = 0.5 + 0.4 * Math.sin(TAU * (t / 8 * (1 + i % 3) + i * 0.618)); });
    nuvens.forEach(function (n, i) { n.style.transform = 'translate(' + (Math.sin(TAU * (t / 8 + i * .25)) * 7).toFixed(2) + 'px,' + (Math.cos(TAU * (t / 8 + i * .25)) * 3).toFixed(2) + 'px)'; });
    var ida = t < 4 ? t : 8 - t;
    return buscar(0.6 + ida);
  };
})();
