// Emoji do iPhone (Apple) em arte feita por código.
// O Chromium deste ambiente só tem a fonte Noto Color Emoji (desenho do Android/Google).
// Este script troca cada emoji do texto da página por <img> do desenho da Apple,
// do pacote emoji-datasource-apple@16.0.0 (64px, servido pelo jsDelivr).
//
// Uso no HTML da arte, antes do script que marca window.READY:
//   <script src="caminho/para/emoji-iphone.js"></script>
//   ... await window.emojiIphone;  window.READY = true;
// Tamanho: o emoji ocupa 1em da letra em volta. Ajuste com CSS em img.emoji-iphone.
// A imagem tem 64px: acima de ~64px na arte final, amplie antes (Topaz) e use arquivo local.
(function () {
  const CDN = 'https://cdn.jsdelivr.net/npm/emoji-datasource-apple@16.0.0/img/apple/64/';
  const RE = /(?:[\u{1F1E6}-\u{1F1FF}]{2}|[0-9#*]️?⃣|(?![©®™](?!️))\p{Extended_Pictographic}(?:️|[\u{1F3FB}-\u{1F3FF}])*(?:‍\p{Extended_Pictographic}(?:️|[\u{1F3FB}-\u{1F3FF}])*)*)/gu;
  const cps = (s) => [...s].map((c) => c.codePointAt(0).toString(16).padStart(4, '0'));
  // o nome do arquivo às vezes leva o fe0f e às vezes não: tenta as variações
  const nomes = (e) => {
    const a = cps(e), sem = a.filter((c) => c !== 'fe0f');
    return [...new Set([a.join('-'), sem.join('-'), [sem[0], 'fe0f', ...sem.slice(1)].join('-')])];
  };
  const carrega = (img, lista) => new Promise((ok) => {
    let i = 0;
    img.onload = () => ok(true);
    img.onerror = () => (++i < lista.length ? (img.src = CDN + lista[i] + '.png') : (console.warn('emoji sem desenho Apple:', img.alt), img.replaceWith(img.alt), ok(false)));
    img.src = CDN + lista[0] + '.png';
  });
  window.emojiIphone = (async () => {
    if (document.readyState === 'loading') await new Promise((r) => document.addEventListener('DOMContentLoaded', r));
    const st = document.createElement('style');
    st.textContent = 'img.emoji-iphone{height:1em;width:1em;vertical-align:-0.12em;display:inline-block;object-fit:contain}';
    document.head.appendChild(st);
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: (n) => (n.parentElement.closest('script,style,textarea') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT),
    });
    const alvos = [];
    for (let n; (n = w.nextNode());) if (RE.test(n.data)) alvos.push(n);
    const espera = [];
    for (const n of alvos) {
      const f = document.createDocumentFragment();
      let k = 0;
      n.data.replace(RE, (e, pos) => {
        if (pos > k) f.appendChild(document.createTextNode(n.data.slice(k, pos)));
        const img = document.createElement('img');
        img.className = 'emoji-iphone'; img.alt = e; img.draggable = false;
        espera.push(carrega(img, nomes(e)));
        f.appendChild(img);
        k = pos + e.length;
      });
      if (k < n.data.length) f.appendChild(document.createTextNode(n.data.slice(k)));
      n.replaceWith(f);
    }
    return Promise.all(espera);
  })();
})();
