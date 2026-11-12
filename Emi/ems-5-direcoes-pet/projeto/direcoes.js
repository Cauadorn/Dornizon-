// Conteúdo do carrossel "5 direções criativas pra marcas pet" (@itsemsdesign).
//
// v4 (12/11): UMA estrutura própria da EMS, igual nas 5 lâminas de direção (a Emi não quer layout
// diferente em cada uma), e que não é a da referência (grade 3 x 3 com cartão no meio):
//   foto do pet em destaque (alto, à esquerda) · marca fictícia e foto quadrada na coluna da direita ·
//   embaixo o cartão da direção, uma foto alta e a coluna paleta + letra.
// Fotos: cada imagem aparece UMA vez no carrossel (variações da mesma cena contam como repetição).
// cheia: { src, px, py, zoom } = foto inteira tipo object-fit: cover.

const dots = (cor, passo = 18, tam = 30) => `radial-gradient(circle, ${cor} ${tam}%, transparent ${tam + 3}%) 0 0 / ${passo}px ${passo}px`;

const paleta = (cores) => `<div class="paleta mini">${cores.map(([nome, hex, tx]) =>
  `<div style="background:${hex};color:${tx}"><b>${nome}</b><small>${hex.toUpperCase()}</small></div>`).join('')}</div>`;

// img (opcional): no lugar do "Aa", uma imagem (para marcas de letra desenhada, como o monograma do pelo solto).
// so: true → o quadro mostra só a imagem, centralizada (a Emi, no pelo solto: "aqui deixa só o ps")
const tipo = ({ aa, aaCor, sombra = 'none', amostra, amostraCss, cor, nome, img, imgAlt = 118, so = false }) =>
  so && img ? `<img src="img/${img}" alt="" style="position:absolute;left:50%;top:50%;height:${imgAlt}px;transform:translate(-50%,-50%)">` :
  `<div class="tipo" style="color:${cor}">
     ${img ? `<img src="img/${img}" alt="" style="display:block;height:${imgAlt}px;margin:0 auto 6px">` : `<div class="aa" style="font:${aa};line-height:.86;color:${aaCor};text-shadow:${sombra}">Aa</div>`}
     <div class="amostra" style="font:${amostraCss};line-height:1.1">${amostra}</div>
     <div class="nome">${nome}</div></div>`;

// conteúdo de tamanho fixo centralizado no quadro
const centro = (w, h, html) => `<div class="centro" style="width:${w}px;height:${h}px;margin:${-h / 2}px 0 0 ${-w / 2}px">${html}</div>`;

// Marcas fictícias (uma por direção). Regras de acabamento:
// - texto centralizado no corpo da forma, não na caixa (o balão tem cauda: o centro dele não é o centro da caixa);
// - texto com espaçamento entre letras ganha o mesmo valor de recuo à esquerda (o espaçamento sobra depois da última letra);
// - forma e texto feitos em camadas simples (SVG para a forma, texto de verdade por cima) para virar camada editável no Figma.
// Explosão de gibi (estrela de pontas irregulares), gerada uma vez
const EXPLOSAO = (() => { const n = 18, cx = 190, cy = 150, pts = [];
  for (let i = 0; i < n * 2; i++) { const a = (i / (n * 2)) * Math.PI * 2 - Math.PI / 2;
    const r = i % 2 ? 112 + (i % 4 === 1 ? 6 : -4) : 156 + ((i * 37) % 3) * 9;
    pts.push(`${(cx + Math.cos(a) * r * 1.12).toFixed(1)},${(cy + Math.sin(a) * r * .86).toFixed(1)}`); }
  return pts.join(' '); })();
// Faixa com pontas recortadas
const FAIXA = 'M14 8 L286 0 L274 30 L290 60 L10 66 L24 36 Z';
// Alfinete de fralda (número de peito)
const ALFINETE = (x, y, r) => `<svg viewBox="0 0 34 12" width="34" height="12" style="position:absolute;left:${x}px;top:${y}px;transform:rotate(${r}deg)">
  <path d="M5 6 H30" stroke="#9AA3AD" stroke-width="2.4" stroke-linecap="round"/><path d="M8 3.2 H28" stroke="#C9D0D6" stroke-width="1.6" stroke-linecap="round"/>
  <circle cx="5" cy="6" r="4.2" fill="#C9D0D6" stroke="#7B848D" stroke-width="1.2"/></svg>`;
const BRILHO4 = (x, y, w, cor) => `<svg viewBox="0 0 40 40" width="${w}" height="${w}" style="position:absolute;left:${x}px;top:${y}px"><path d="M20 0 C21.5 13 27 18.5 40 20 C27 21.5 21.5 27 20 40 C18.5 27 13 21.5 0 20 C13 18.5 18.5 13 20 0 Z" fill="${cor}"/></svg>`;

const MARCA = {
  // 01 · pacote de petisco (stand-up pouch) chapado: quadrinho impresso com "AU!" fora de registro, textos de embalagem
  gibi: centro(300, 360, `
    <div style="position:absolute;left:24px;top:10px;width:252px;height:338px;transform:rotate(-3deg)">
      <svg viewBox="0 0 252 338" width="252" height="338" style="position:absolute;inset:0">
        <path d="M10 0 H242 Q252 0 252 10 V322 Q252 334 238 335 Q126 342 14 335 Q0 334 0 322 V10 Q0 0 10 0 Z" transform="translate(8 9)" fill="rgba(27,27,27,.9)"/>
        <path d="M10 0 H242 Q252 0 252 10 V322 Q252 334 238 335 Q126 342 14 335 Q0 334 0 322 V10 Q0 0 10 0 Z" fill="#F2542D"/>
        <path d="M10 0 H242 Q252 0 252 10 V30 H0 V10 Q0 0 10 0 Z" fill="#D9441F"/>
        <path d="M0 30 H252" stroke="#B8361A" stroke-width="2"/><path d="M8 40 H244" stroke="#1B1B1B" stroke-width="1.6" stroke-dasharray="3 4" opacity=".45"/>
        <rect x="108" y="10" width="36" height="10" rx="5" fill="#FFD23F"/>
        <path d="M0 14 L7 18 L0 22 Z" fill="#FFD23F"/><path d="M252 14 L245 18 L252 22 Z" fill="#FFD23F"/></svg>
      <div style="position:absolute;left:22px;top:56px;width:208px;height:146px;background:#FFD23F;border:4px solid #1B1B1B;transform:rotate(-2deg);overflow:hidden">
        <div class="padrao" style="position:absolute;left:96px;top:60px;width:130px;height:100px;background:radial-gradient(circle,#F2542D 32%,transparent 35%) 0 0 / 11px 11px;opacity:.9"></div>
        <div style="position:absolute;left:0;right:0;top:20px;text-align:center;font:400 104px/1 'Bagel Fat One';color:#2B59C3;margin-left:5px;margin-top:4px">AU!</div>
        <div style="position:absolute;left:0;right:0;top:20px;text-align:center;font:400 104px/1 'Bagel Fat One';color:#1B1B1B">AU!</div></div>
      <div style="position:absolute;left:186px;top:40px;width:62px;height:62px;border-radius:50%;background:#2B59C3;border:3px solid #1B1B1B;transform:rotate(12deg);
        display:grid;place-items:center;text-align:center;font:400 12px/1.05 'Bagel Fat One';color:#fff">nº1 do<br>bairro</div>
      <div style="position:absolute;left:0;right:0;top:218px;text-align:center;font:400 40px/1 'Bagel Fat One';color:#FFD23F;letter-spacing:.01em">petiscaria</div>
      <div style="position:absolute;left:0;right:0;top:266px;text-align:center;font:600 11px/1 var(--sans);color:#fff;letter-spacing:.2em;padding-left:.2em">PETISCO CROCANTE P/ CÃES</div>
      <div style="position:absolute;left:22px;right:22px;top:290px;display:flex;justify-content:space-between;font:500 11px/1 var(--sans);color:#fff;opacity:.9">
        <span>sabor frango</span><span>80 g</span></div></div>`),
  // 03 · letra groovy com sombras empilhadas e faixa arco-íris que dobra a curva
};

const DIRECOES = [
  // ---------------- 01 · pop de gibi ----------------
  {
    titulo: 'pop de <em>gibi</em>', pra: 'petisco e brinquedo', card: 'var(--violeta)',
    texto: 'cores primárias chapadas, contorno grosso e retícula de gibi. pra petisco e brinquedo que querem ser a alegria da prateleira.',
    heroi: { bg: '#FFD23F', cheia: { src: 'd1pet-2', px: .5, py: .3 } },
    // TOTÓ (aprovado em 12/11, a partir da referência NOSY): logo creme sobre massa vermelha com patinhas.
    // Arte em marcas/toto/logo.html (?pata=anel); a imagem do quadro é gerada por ela (img/toto-marca.jpg).
    marca: { bg: '#F2542D', cheia: { src: 'toto-marca', px: .5, py: .5 }, cursor: [326, 338] },
    quadrado: { bg: '#F2542D', cheia: { src: 'd1extra', px: .04, py: .5 } },
    alto: { bg: '#F4E9D6', cheia: { src: 'toto-pacote', px: .5, py: .45 } },   // aplicação aprovada: pacote TOTÓ (marcas/toto/mockup)
    paleta: [['amarelo gema', '#FFD23F', '#1B1B1B'], ['vermelho tomate', '#F2542D', '#1B1B1B'], ['azul gibi', '#2B59C3', '#FFFBDE'], ['preto nanquim', '#1B1B1B', '#FFFBDE']],
    tipo: { bg: '#2B59C3', aa: "400 112px 'Cherry Bomb One'", aaCor: '#FFD23F', sombra: '5px 5px 0 #1B1B1B', amostra: 'au au!', amostraCss: "400 28px 'Cherry Bomb One'", cor: '#FFFBDE', nome: 'cherry bomb one' },
  },
  // ---------------- 02 · clube de grife ----------------
  {
    titulo: 'clube de <em>grife</em>', pra: 'marca premium', card: 'var(--plum)',
    texto: 'vinho, caramelo e creme, serifa clássica, relevo seco e tricô. pra marca premium que quer ser grife, não petshop.',
    // Maison Caramelo (aprovada em 12/11): o caramelo empinado com a flor (silhueta de vaso grego) sobre o nome em Cormorant,
    // a partir das refs 14 Eros & Co. e 15 oval em relevo (referencias/maison-caramelo/brasao). Marca em marcas/maison-caramelo.
    heroi: { bg: '#4A1D22', cheia: { src: 'maison-outdoor', px: .5, py: .5 } },   // mockup aprovado: outdoor na parede de tijolo (PATTU)
    marca: { bg: '#EDE8DD', cheia: { src: 'maison-marca', px: .5, py: .5 }, cursor: [326, 338] },   // logo.html?w=452&h=430&escala=.54&dx=-21.5&dy=23
    quadrado: { bg: '#23392E', cheia: { src: 'd2pet-2', px: .5, py: .45 } },   // o whippet de suéter no sofá verde (a Emi pediu de volta)
    alto: { bg: '#EEE8D8', cheia: { src: 'maison-selo', px: .5, py: .5 } },   // o selo oval prensado no papel creme (selo.html?w=2080&h=3776&rx=.34 + relevo.py, subido 64 px para centrar no quadro visível)
    paleta: [['vinho', '#4A1D22', '#EDE8DD'], ['caramelo', '#B9793F', '#2B1416'], ['creme', '#EDE8DD', '#4A1D22'], ['nanquim', '#2B1416', '#EDE8DD']],
    tipo: { bg: '#4A1D22', aa: "500 118px 'Cormorant'", aaCor: '#EDE3CC', amostra: 'tricô · couro · alfaiataria', amostraCss: "500 17px 'Cormorant';letter-spacing:.06em", cor: '#EDE3CC', nome: 'cormorant garamond' },
  },
  // ---------------- 03 · retrô setentinha ----------------
  {
    titulo: 'retrô <em>setentinha</em>', pra: 'banho e tosa de bairro', card: 'var(--wine)',
    texto: 'café, mostarda e azul piscina, letra groovy desenhada e monograma bordado. pra banho e tosa de bairro com história.',
    // pelo solto (aprovado em 12/11): o nome veio do conceito gerado que a Emi escolheu, vetorizado (marcas/pelo-solto/logo.html);
    // o monograma ps sobreposto (ps-sobreposto.svg) é o que vai bordado e estampado. Pesquisa em referencias/pelo-solto.
    heroi: { bg: '#5FA7AE', cheia: { src: 'pelo-manga', px: .5, py: .5 } },   // mockup aprovado: ps bordado na manga (Digs)
    marca: { bg: '#FDF6E5', cheia: { src: 'pelo-marca', px: .5, py: .5 }, cursor: [326, 338] },   // logo.html?w=452&h=430&escala=.46&dx=-20.5&dy=21.5 (centro da tinta no centro da moldura)
    quadrado: { bg: '#6B3A1F', cheia: { src: 'd3prod-2', px: .5, py: .8 } },
    alto: { bg: '#E9B03B', cheia: { src: 'd3extra', px: .55, py: .5 } },
    paleta: [['creme', '#FDF6E5', '#5A2E17'], ['café', '#5A2E17', '#FDF6E5'], ['mostarda', '#E9A92B', '#5A2E17'], ['azul piscina', '#5FA7AE', '#FDF6E5']],
    tipo: { bg: '#5A2E17', img: 'pelo-ps-creme.svg', imgAlt: 150, so: true },   // só o ps (pedido da Emi)
  },
  // ---------------- 04 · modo atleta ----------------
  {
    titulo: 'modo <em>atleta</em>', pra: 'passeio e adestramento', card: 'var(--creative-purple)',
    texto: 'verde-limão, preto e azul elétrico, letra pesada inclinada e a matilha correndo junto. pra passeio, coleira e adestramento que vendem energia.',
    // MATILHA running club (aprovada em 12/11): o nome "AU" virou MATILHA. Pesquisa em referencias/au-running-club,
    // logo em marcas/au/logo.html e estampa em marcas/au/estampa. O destaque é o mockup aprovado: Grandorf + Juicy Kibbles,
    // gerado no Canva com o logo e a estampa de referência, na rua e só com a guia (marcas/au/mockup).
    heroi: { bg: '#8EC9F2', cheia: { src: 'matilha-corrida', px: .5, py: .2 } },   // sem o logo grande do canto (a Emi pediu; marcas/au/mockup/tira_logo.py), com 110 px de céu espelhado em cima
    marca: { bg: '#CCFF3E', cheia: { src: 'matilha-marca', px: .5, py: .5 }, cursor: [326, 338] },
    quadrado: { bg: '#B8502E', cheia: { src: 'd4prod-2', px: .5, py: .5 } },
    alto: { bg: '#8EC9F2', cheia: { src: 'd4pet-2', px: .5, py: .4 } },
    paleta: [['verde-limão', '#CCFF3E', '#121212'], ['azul elétrico', '#4342FF', '#FFFBDE'], ['branco faixa', '#F1F1EC', '#121212'], ['preto pista', '#121212', '#CCFF3E']],
    tipo: { bg: '#121212', aa: "italic 900 112px 'Rubik'", aaCor: '#CCFF3E', amostra: 'corre com ele', amostraCss: "italic 600 22px 'Rubik'", cor: '#FFFBDE', nome: 'rubik black italic' },
  },
  // ---------------- 05 · ciência fofa ----------------
  {
    titulo: 'ciência <em>fofa</em>', pra: 'nutrição e saúde', card: 'var(--ameixa)',
    texto: 'azul de laboratório, rosa cápsula, etiqueta preta e nome gigante. pra nutrição e saúde pet: ciência sem cara de hospital.',
    // MIAU.LAB (aprovada em 12/11): a pesquisa está em referencias/miaulab e o logo em marcas/miaulab/logo.js.
    // Nome condensado, gato preto espiando de dentro do U, com unhas e arranhões, e ".lab" embaixo.
    // O destaque é a aplicação aprovada: os potes pintados com o rótulo enrolado (marcas/miaulab/mockup/pinta_potes.py).
    heroi: { bg: '#BDEBD6', cheia: { src: 'miau-potes', px: .5, py: .5 } },
    marca: { bg: '#2F55F2', cheia: { src: 'miau-marca', px: .5, py: .5 }, cursor: [326, 338] },
    // caixa de comprimidos MIAU.LAB (marcas/miaulab/mockup/caixa). Substituiu os frascos de gotas, que a Emi achou feios.
    quadrado: { bg: '#F2C4C4', cheia: { src: 'miau-caixa', px: .5, py: .5 } },
    alto: { bg: '#BDEBD6', cheia: { src: 'd5extra', px: .45, py: .5 } },
    paleta: [['azul laboratório', '#2F55F2', '#FFFBDE'], ['rosa cápsula', '#FF9FD2', '#141418'], ['jaleco', '#F5F7F6', '#141418'], ['nanquim', '#141418', '#FFFBDE']],
    tipo: { bg: '#141418', aa: "900 extra-condensed 132px 'Archivo'", aaCor: '#FF9FD2', amostra: '.lab nº07', amostraCss: "700 22px 'Space Mono'", cor: '#FFFBDE', nome: 'archivo + space mono' },
  },
];

// Capa: capa de revista com o gato preto de modelo (fundo violeta com estrelas em retícula, aprovado).
const CAPA = { foto: { src: 'capa-2', px: .5, py: .5 }, recorte: 'capa-2-gato' };

// Chamada: enquete; o gato (fundo ameixa) levanta a pata até a opção marcada.
const CHAMADA = {
  foto: { src: 'cham-2', px: .85, py: .95, zoom: 1.25 }, recorte: 'cham-2-gato', marcada: 1,
  // estrelas em retícula na parede (textura), mesmo grafismo das estrelas da parede da capa
  estrelas: [
    { cx: 960, cy: 720, R: 270, passo: 12, rmax: 3.6, uniforme: true, opacidade: .55, rot: -14 },
    { cx: 120, cy: 160, R: 190, passo: 12, rmax: 3.6, uniforme: true, opacidade: .5, rot: 10 },
    { cx: 150, cy: 1010, R: 210, passo: 12, rmax: 3.6, uniforme: true, opacidade: .45, rot: -24 },
  ],
};
