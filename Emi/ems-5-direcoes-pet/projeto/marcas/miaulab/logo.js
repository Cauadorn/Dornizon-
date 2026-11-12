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
// A v1 (gato grande atrás do A) está em logo-v1-grande.js.
function miauLogo(el, o = {}) {
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
    <g transform="translate(${cx} ${parede}) scale(${k})">${o.contorno ? patas(o.contorno, o.contorno) : ''}${patas(gato)}</g>
  </svg>
  ${o.lab === false ? '' : `<div style="position:absolute;right:0;top:610px;background:${o.labFundo || '#141418'};color:${o.labCor || '#fff'};font:700 64px/1 Mono;padding:10px 20px 16px;letter-spacing:.02em">.lab</div>`}`;
}
