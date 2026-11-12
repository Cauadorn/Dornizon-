// Palavra curta nunca sobra no fim da linha (regra da Emi, 12/11/2026).
// Palavra de 1 ou 2 letras (e, o, a, é, da, de, do, em, um, só...) desce junto com a seguinte:
//  - cola cada uma na palavra seguinte com espaço inquebrável (vale para a quebra automática);
//  - se tiver <br> logo depois dela, passa a palavra para a linha de baixo ("cansa é<br>ajuste" -> "cansa<br>é ajuste").
// Uso: <script src="caminho/para/palavra-curta.js"></script> no fim do <body>,
//      antes do script que ajusta o layout e marca window.READY.
// Depois de renderizar, conferir com: node conferir-palavra-curta.js <arquivo.html>
(function () {
  const CURTA_FIM = /(^|[\s ])([\p{L}]{1,2})[ \t\n\r]*$/u;
  const COLA = /(?<=^|[\s (“"‘'])([\p{L}]{1,2})[ \t\n\r]+/gu;
  const fora = (n) => n.parentElement && n.parentElement.closest('script,style,textarea');
  // 1) <br> logo depois de palavra curta: a palavra desce
  document.querySelectorAll('br').forEach((br) => {
    let antes = br.previousSibling;
    if (!antes || antes.nodeType !== 3) return;
    let desce = '';
    for (let m; (m = antes.data.match(CURTA_FIM));) {
      desce = m[2] + ' ' + desce;
      antes.data = antes.data.slice(0, m.index + m[1].length).replace(/[\s ]+$/, '');
    }
    if (!desce) return;
    const depois = br.nextSibling;
    if (depois && depois.nodeType === 3) depois.data = desce + depois.data.replace(/^[ \t\n\r]+/, '');
    else br.after(document.createTextNode(desce));
  });
  // 2) cola toda palavra curta na seguinte
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n; (n = w.nextNode());) if (!fora(n)) n.data = n.data.replace(COLA, '$1 ');
})();
