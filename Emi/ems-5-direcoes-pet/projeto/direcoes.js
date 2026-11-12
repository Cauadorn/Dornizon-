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

const tipo = ({ aa, aaCor, sombra = 'none', amostra, amostraCss, cor, nome }) =>
  `<div class="tipo" style="color:${cor}">
     <div class="aa" style="font:${aa};line-height:.86;color:${aaCor};text-shadow:${sombra}">Aa</div>
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
  // 02 · etiqueta de couro pendurada, dourado em relevo
  grife: centro(300, 380, `
    <svg viewBox="0 0 300 380" width="300" height="380" style="position:absolute;inset:0">
      <path d="M150 -40 C150 10 120 30 150 78" fill="none" stroke="#C08A4F" stroke-width="3"/></svg>
    <div style="position:absolute;left:44px;top:58px;width:212px;height:300px;transform:rotate(-5deg)">
      <svg viewBox="0 0 212 300" width="212" height="300" style="position:absolute;inset:0">
        <path d="M40 0 H172 L212 40 V288 Q212 300 200 300 H12 Q0 300 0 288 V40 Z" transform="translate(6 8)" fill="rgba(42,26,18,.45)"/>
        <path d="M40 0 H172 L212 40 V288 Q212 300 200 300 H12 Q0 300 0 288 V40 Z" fill="#4A2E21"/>
        <path d="M44 9 H168 L203 44 V284 Q203 291 196 291 H16 Q9 291 9 284 V44 Z" fill="none" stroke="#C08A4F" stroke-width="1.4" stroke-dasharray="5 4" opacity=".8"/>
        <circle cx="106" cy="30" r="11" fill="#F3E9D7"/><circle cx="106" cy="30" r="11" fill="none" stroke="#B8975A" stroke-width="4"/></svg>
      <div style="position:absolute;left:0;right:0;top:78px;text-align:center;color:#D8BC7E;text-shadow:0 1px 0 rgba(0,0,0,.45)">
        <div style="font:500 13px/1 'Bodoni Moda';letter-spacing:.42em;padding-left:.42em">MAISON</div>
        <div style="font:italic 500 43px/1 'Bodoni Moda';margin-top:12px;letter-spacing:-.01em">Caramelo</div>
        <div style="width:58px;height:1px;background:#B8975A;margin:16px auto 12px"></div>
        <div style="font:500 10px/1 'Bodoni Moda';letter-spacing:.38em;padding-left:.38em">PET COUTURE</div>
        <div style="font:italic 500 13px/1 'Bodoni Moda';margin-top:58px;opacity:.85">nº 001 · coleção inverno</div></div></div>`),
  // 03 · letra groovy com sombras empilhadas e faixa arco-íris que dobra a curva
  setentinha: `
    <svg viewBox="0 0 422 400" width="422" height="400" style="position:absolute;inset:0">
      <g fill="none" stroke-width="16" stroke-linecap="butt">
        <path d="M-10 52 H318 A58 58 0 0 1 376 110 V410" stroke="#7D7A3A"/>
        <path d="M-10 68 H318 A42 42 0 0 1 360 110 V410" stroke="#6B3A1F"/>
        <path d="M-10 84 H318 A26 26 0 0 1 344 110 V410" stroke="#E2701E"/>
        <path d="M-10 100 H318 A10 10 0 0 1 328 110 V410" stroke="#E9B03B"/></g></svg>
    <div style="position:absolute;left:30px;top:118px;width:300px;font:400 92px/.84 'Shrikhand';color:#FFF6E5;-webkit-text-stroke:5px #6B3A1F;paint-order:stroke fill;
      text-shadow:4px 4px 0 #6B3A1F,8px 8px 0 #E2701E,12px 12px 0 #E9B03B,16px 16px 0 #7D7A3A;transform:rotate(-5deg)">pelo<br>solto</div>
    ${BRILHO4(250, 128, 26, '#E2701E')}${BRILHO4(36, 330, 18, '#7D7A3A')}
    <div style="position:absolute;left:44px;top:322px;font:400 24px/1 'Shrikhand';color:#6B3A1F">banho &amp; tosa</div>
    <div style="position:absolute;left:46px;top:354px;font:500 12px/1 var(--sans);letter-spacing:.3em;color:#6B3A1F">DESDE 1974</div>`,
  // 04 · número de peito preso com alfinetes
  atleta: centro(300, 272, `
    <div style="position:absolute;left:10px;top:14px;width:280px;height:236px;transform:rotate(-4deg);background:#F7F8FA;border-radius:6px;
      box-shadow:7px 9px 0 rgba(10,20,70,.35);overflow:hidden;color:#1E1E24">
      <div style="position:absolute;left:0;right:0;top:0;height:46px;background:#1E1E24"></div>
      <div style="position:absolute;left:0;right:0;top:15px;text-align:center;font:400 17px/1 'Graduate';color:#C7F23E;letter-spacing:.16em;padding-left:.16em">AU RUNNING CLUB</div>
      <div style="position:absolute;left:0;right:0;top:56px;text-align:center;font:400 128px/1 'Graduate';color:#1F3FBF;letter-spacing:-.02em">026</div>
      <div style="position:absolute;left:0;right:0;bottom:0;height:34px;background:#C7F23E"></div>
      <div style="position:absolute;left:0;right:0;bottom:11px;text-align:center;font:400 13px/1 'Graduate';letter-spacing:.24em;padding-left:.24em">5K · CORRE COM ELE</div>
      ${ALFINETE(10, 54, -30)}${ALFINETE(236, 52, 28)}${ALFINETE(10, 170, 20)}${ALFINETE(236, 172, -24)}</div>`),
  ciencia: centro(262, 318, `
    <div style="position:absolute;left:6px;top:4px;width:250px;height:306px;background:#fff;border:2px solid #23262B;border-radius:12px;overflow:hidden;
         transform:rotate(-4deg);box-shadow:6px 8px 0 rgba(35,38,43,.35);color:#23262B">
      <div style="position:absolute;left:0;right:0;top:0;height:56px;background:#BDEBD6;border-bottom:2px solid #23262B"></div>
      <div style="position:absolute;left:16px;top:15px;font:700 25px/1 'Space Mono'">MIAU.LAB</div>
      <div style="position:absolute;right:14px;top:14px;width:26px;height:26px;border-radius:50%;border:2px solid #23262B;background:#fff"></div>
      <div style="position:absolute;left:16px;top:72px;font:400 13px/1 'Space Mono';opacity:.75">fórmula</div>
      <div style="position:absolute;left:14px;top:88px;font:700 52px/1 'Space Mono'">nº07</div>
      <div style="position:absolute;left:16px;right:16px;top:152px;height:2px;background:#23262B"></div>
      <div style="position:absolute;left:16px;top:164px;font:400 12.5px/1.5 'Space Mono'">suplemento p/ gatos<br>60 cápsulas · lote 26.11</div>
      <div style="position:absolute;left:16px;right:16px;top:218px;height:46px;background:repeating-linear-gradient(90deg,#23262B 0 2px,transparent 2px 5px,#23262B 5px 9px,transparent 9px 11px,#23262B 11px 12px,transparent 12px 16px)"></div>
      <div style="position:absolute;left:0;right:0;top:270px;text-align:center;font:400 11px/1 'Space Mono';letter-spacing:.2em;padding-left:.2em">7 891234 260711</div></div>`),
};

const DIRECOES = [
  // ---------------- 01 · pop de gibi ----------------
  {
    titulo: 'pop de <em>gibi</em>', pra: 'petisco e brinquedo', card: 'var(--violeta)',
    texto: 'cores primárias chapadas, contorno grosso e retícula de gibi. pra petisco e brinquedo que querem ser a alegria da prateleira.',
    heroi: { bg: '#FFD23F', cheia: { src: 'd1pet-2', px: .5, py: .3 } },
    marca: { bg: '#2B59C3', html: MARCA.gibi, cursor: [318, 338] },
    quadrado: { bg: '#F2542D', cheia: { src: 'd1extra', px: .04, py: .5 } },
    alto: { bg: '#2B59C3', cheia: { src: 'd1prod-1', px: .5, py: .45 } },
    paleta: [['amarelo gema', '#FFD23F', '#1B1B1B'], ['vermelho tomate', '#F2542D', '#1B1B1B'], ['azul gibi', '#2B59C3', '#FFFBDE'], ['preto nanquim', '#1B1B1B', '#FFFBDE']],
    tipo: { bg: '#2B59C3', aa: "400 104px 'Bagel Fat One'", aaCor: '#FFD23F', sombra: '5px 5px 0 #1B1B1B', amostra: 'au au!', amostraCss: "400 26px 'Bagel Fat One'", cor: '#FFFBDE', nome: 'bagel fat one' },
  },
  // ---------------- 02 · clube de grife ----------------
  {
    titulo: 'clube de <em>grife</em>', pra: 'marca premium', card: 'var(--plum)',
    texto: 'creme, caramelo e café, serifa clássica, monograma, tricô e couro. pra marca premium que quer ser grife, não petshop.',
    heroi: { bg: '#23392E', cheia: { src: 'd2pet-2', px: .55, py: .5 } },
    marca: { bg: '#F3E9D7', html: MARCA.grife, cursor: [300, 340] },
    quadrado: { bg: '#F3E9D7', cheia: { src: 'd2prod-2', px: .62, py: .6 } },
    alto: { bg: '#23392E', cheia: { src: 'd2extra', px: .6, py: .55 } },
    paleta: [['creme', '#F3E9D7', '#4A2E21'], ['caramelo', '#C08A4F', '#2A1A12'], ['café', '#4A2E21', '#F3E9D7'], ['verde-garrafa', '#23392E', '#F3E9D7']],
    tipo: { bg: '#EADBC2', aa: "italic 500 120px 'Bodoni Moda'", aaCor: '#4A2E21', amostra: 'coleção inverno', amostraCss: "500 22px 'Bodoni Moda'", cor: '#4A2E21', nome: 'bodoni moda' },
  },
  // ---------------- 03 · retrô setentinha ----------------
  {
    titulo: 'retrô <em>setentinha</em>', pra: 'banho e tosa de bairro', card: 'var(--wine)',
    texto: 'laranja queimado, mostarda e marrom, letra groovy e grão de filme. pra banho e tosa e petshop de bairro com história.',
    heroi: { bg: '#E2701E', cheia: { src: 'd3pet-2', px: .62, py: .6 } },
    marca: { bg: '#F4E3C3', html: MARCA.setentinha, cursor: [330, 300] },
    quadrado: { bg: '#6B3A1F', cheia: { src: 'd3prod-2', px: .5, py: .8 } },
    alto: { bg: '#E9B03B', cheia: { src: 'd3extra', px: .55, py: .5 } },
    paleta: [['mostarda', '#E9B03B', '#3A1E0E'], ['laranja queimado', '#E2701E', '#3A1E0E'], ['marrom vinil', '#6B3A1F', '#F4E3C3'], ['verde oliva', '#7D7A3A', '#F4E3C3']],
    tipo: { bg: '#7D7A3A', aa: "400 100px 'Shrikhand'", aaCor: '#F4E3C3', sombra: '5px 5px 0 #E2701E', amostra: 'paz & ração', amostraCss: "400 24px 'Shrikhand'", cor: '#F4E3C3', nome: 'shrikhand' },
  },
  // ---------------- 04 · modo atleta ----------------
  {
    titulo: 'modo <em>atleta</em>', pra: 'passeio e adestramento', card: 'var(--creative-purple)',
    texto: 'azul royal, verde-limão, cara de uniforme e foto em movimento. pra passeio, coleira e adestramento que vendem energia.',
    heroi: { bg: '#8EC9F2', cheia: { src: 'd4pet-2', px: .5, py: .4 } },
    marca: { bg: '#1F3FBF', html: MARCA.atleta, cursor: [326, 316] },
    quadrado: { bg: '#B8502E', cheia: { src: 'd4prod-2', px: .5, py: .5 } },
    alto: { bg: '#1E1E24', cheia: { src: 'd4extra', px: .42, py: .6 } },
    paleta: [['azul royal', '#1F3FBF', '#FFFBDE'], ['verde-limão', '#C7F23E', '#1E1E24'], ['branco quadra', '#EEF1F4', '#1E1E24'], ['asfalto', '#1E1E24', '#FFFBDE']],
    tipo: { bg: '#1E1E24', aa: "400 108px 'Graduate'", aaCor: '#C7F23E', amostra: 'bora correr?', amostraCss: "400 22px 'Graduate'", cor: '#FFFBDE', nome: 'graduate' },
  },
  // ---------------- 05 · ciência fofa ----------------
  {
    titulo: 'ciência <em>fofa</em>', pra: 'nutrição e saúde', card: 'var(--ameixa)',
    texto: 'branco, azul clínico e menta, rótulo de laboratório e letra mono. pra nutrição e saúde pet: confiança sem cara de hospital.',
    heroi: { bg: '#BDEBD6', cheia: { src: 'd5pet-1', px: .5, py: .6 } },
    marca: { bg: '#2F6BFF', html: MARCA.ciencia, cursor: [326, 338] },
    quadrado: { bg: '#F5F7F6', cheia: { src: 'd5prod-2', px: .5, py: .72 } },
    alto: { bg: '#BDEBD6', cheia: { src: 'd5extra', px: .45, py: .5 } },
    paleta: [['azul clínico', '#2F6BFF', '#FFFBDE'], ['menta', '#BDEBD6', '#23262B'], ['branco jaleco', '#F5F7F6', '#23262B'], ['grafite', '#23262B', '#FFFBDE']],
    tipo: { bg: '#23262B', aa: "700 96px 'Space Mono'", aaCor: '#BDEBD6', amostra: 'fórmula_07', amostraCss: "400 22px 'Space Mono'", cor: '#FFFBDE', nome: 'space mono' },
  },
];

// Capa: capa de revista com o gato preto de modelo (fundo violeta com estrelas em retícula, aprovado).
const CAPA = { foto: { src: 'capa-2', px: .5, py: .5 }, recorte: 'capa-2-gato', cedilha: [452, 330, 80, 96] };

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
