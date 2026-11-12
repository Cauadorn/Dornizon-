// Logo MIAU.LAB, desenhado em qualquer caixa: miauLogo(el, { cor, gato, olho, lab: true|false }).
// A caixa tem 899 x 700 (unidades do logo): o nome começa em x=0, o topo das letras fica em y=260, a base em y=587.
// Referências: ONCE, wllab e CURAME (nome gigante e condensado, etiqueta preta de laboratório) + o quadro gato-espiando
// (3 hidden cat, 5 e 10 espiando com patas). O gato preto espia por trás do A, com as patinhas no I e no U.
// As pupilas são cápsulas (meio preta, meio na cor do nome). O ".lab" vai embaixo do nome.
// Topo das letras (Archivo 900, largura 62%, 470px): M 0-118 e 178-293 · I 331-416 · A 500-620 · U 697-782 e 814-899.
function miauLogo(el, o = {}) {
  const cor = o.cor || '#FF9FD2', gato = o.gato || '#141418', olho = o.olho || cor;
  const pupila = (x, r) => `<g transform="translate(${x} -64) rotate(${r})"><rect x="-13" y="-29" width="26" height="58" rx="13" fill="#141418"/>`
    + `<path d="M-13 0 V16 A13 13 0 0 0 13 16 V0 Z" fill="${olho}"/><circle cx="5" cy="-15" r="5" fill="#fff"/></g>`;
  el.style.position = el.style.position || 'absolute';
  el.innerHTML = `
  <svg width="899" height="700" viewBox="0 0 899 700" style="position:absolute;left:0;top:0;overflow:visible">
    <defs><clipPath id="acima-${o.id || 'l'}"><rect x="-200" y="-300" width="1300" height="560"/></clipPath></defs>
    <g clip-path="url(#acima-${o.id || 'l'})"><g transform="translate(560 260)">
      <path fill="${gato}" d="M-140 40 L-140 -50 C-140 -96 -134 -150 -123 -194 Q-119 -212 -103 -203 C-82 -188 -60 -168 -45 -150 Q0 -161 45 -150 C60 -168 82 -188 103 -203 Q119 -212 123 -194 C134 -150 140 -96 140 -50 L140 40 Z"/>
      <circle cx="-56" cy="-66" r="37" fill="#fff"/><circle cx="56" cy="-66" r="37" fill="#fff"/>
      ${pupila(-50, 6)}${pupila(50, -6)}
      <path d="M-12 -26 Q0 -30 12 -26 Q4 -14 0 -12 Q-4 -14 -12 -26 Z" fill="${olho}" stroke="${olho}" stroke-width="4" stroke-linejoin="round"/>
    </g></g>
  </svg>
  <div style="position:absolute;left:-19px;top:191px;font:900 470px/1 Archivo;font-stretch:62%;color:${cor};white-space:nowrap">MIAU</div>
  <svg width="899" height="700" viewBox="0 0 899 700" style="position:absolute;left:0;top:0;overflow:visible">
    <g fill="${gato}"><ellipse cx="373" cy="262" rx="50" ry="31"/><ellipse cx="740" cy="262" rx="50" ry="31"/></g>
    <g stroke="${cor}" stroke-width="7" stroke-linecap="round">
      <line x1="357" y1="278" x2="357" y2="290"/><line x1="389" y1="278" x2="389" y2="290"/>
      <line x1="724" y1="278" x2="724" y2="290"/><line x1="756" y1="278" x2="756" y2="290"/></g>
  </svg>
  ${o.lab === false ? '' : `<div style="position:absolute;right:0;top:610px;background:#141418;color:#fff;font:700 64px/1 Mono;padding:10px 20px 16px;letter-spacing:.02em">.lab</div>`}`;
}
