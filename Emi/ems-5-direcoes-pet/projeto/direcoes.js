// Conteúdo do carrossel "5 direções criativas pra marcas pet" (@itsemsdesign).
//
// v3 (12/11): cada lâmina tem um layout próprio, que conversa com o universo da direção
// (tirinha de gibi, página de revista, arcos anos 70, foto de ação com patch, ficha de laboratório).
// Nada de grade 3 x 3 repetida com cartão no meio: essa era a estrutura da referência.
// Fotos: cada imagem aparece UMA vez no carrossel (variações da mesma cena contam como repetição).
//
// bloco: r = [x, y, w, h] no canvas 1080 x 1350 (quem encosta na borda ganha sangria de 30px).
//   cheia: { src, px, py, zoom } = foto inteira tipo object-fit: cover.
//   forma: 'arco' (topo em arco), 'capsula' (pílula). escolhido: [kx, ky] = seleção do Figma + cursor "emi".
// cartao: r, modo 'v' (vertical) ou 'h' (faixa), tam = corpo do título.

const dots = (cor, passo = 18, tam = 30) => `radial-gradient(circle, ${cor} ${tam}%, transparent ${tam + 3}%) 0 0 / ${passo}px ${passo}px`;

const paleta = (cores) => `<div class="paleta">${cores.map(([nome, hex, tx]) =>
  `<div style="background:${hex};color:${tx}"><b>${nome}</b><small>${hex.toUpperCase()}</small></div>`).join('')}</div>`;

const tipo = ({ aa, aaCor, sombra = 'none', amostra, amostraCss, cor, nome }) =>
  `<div class="tipo" style="color:${cor}">
     <div class="aa" style="font:${aa};line-height:.86;color:${aaCor};text-shadow:${sombra}">Aa</div>
     <div class="amostra" style="font:${amostraCss};line-height:1.1">${amostra}</div>
     <div class="nome">${nome}</div></div>`;

// conteúdo de tamanho fixo centralizado no quadro
const centro = (w, h, html) => `<div class="centro" style="width:${w}px;height:${h}px;margin:${-h / 2}px 0 0 ${-w / 2}px">${html}</div>`;

const MARCA = {
  gibi: centro(308, 408, `
    <svg viewBox="0 0 308 408" width="308" height="408" style="position:absolute;inset:0">
      <path d="M206.8 250.6 L246 330 L158.4 259.9 A125 100 0 1 1 206.8 250.6 Z" fill="#fff" stroke="#1B1B1B" stroke-width="7" stroke-linejoin="round"/></svg>
    <div style="position:absolute;left:0;right:0;top:104px;text-align:center;font:400 112px/1 'Bagel Fat One';color:#1B1B1B;transform:rotate(-6deg)">AU!</div>
    <div style="position:absolute;left:0;right:0;top:338px;text-align:center;font:400 30px/1 'Bagel Fat One';color:#F2542D;-webkit-text-stroke:6px #1B1B1B;paint-order:stroke fill">petiscaria</div>`),
  grife: `
    <div class="pilha" style="color:#D8BC7E">
      <div style="width:84px;height:84px;border:1.5px solid #D8BC7E;border-radius:50%;display:grid;place-items:center;font:italic 500 36px/1 'Bodoni Moda'">MC</div>
      <div style="font:500 58px/1 'Bodoni Moda';margin-top:30px;letter-spacing:.01em">Maison</div>
      <div style="font:italic 500 70px/1 'Bodoni Moda';margin-top:2px">Caramelo</div>
      <div style="width:140px;height:1px;background:#D8BC7E;margin:24px 0 16px;opacity:.7"></div>
      <div style="font:500 14px/1 'Bodoni Moda';letter-spacing:.34em">PET COUTURE</div></div>`,
  setentinha: (w, h) => `
    <svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" style="position:absolute;inset:0">
      <g fill="none" stroke-width="30"><circle cx="${w / 2}" cy="${h + 210}" r="322" stroke="#7D7A3A"/><circle cx="${w / 2}" cy="${h + 210}" r="292" stroke="#6B3A1F"/>
      <circle cx="${w / 2}" cy="${h + 210}" r="262" stroke="#E2701E"/><circle cx="${w / 2}" cy="${h + 210}" r="232" stroke="#E9B03B"/></g></svg>
    <div style="position:absolute;left:0;right:0;top:44px;text-align:center;font:400 104px/.9 'Shrikhand';color:#6B3A1F;text-shadow:5px 5px 0 #E2701E;transform:rotate(-5deg)">pelo<br>solto</div>
    <div style="position:absolute;left:0;right:0;top:262px;text-align:center;font:400 30px/1 'Shrikhand';color:#7D7A3A">banho & tosa</div>`,
  atleta: `
    <div class="pilha">
      <div style="font:400 132px/1 'Graduate';color:#C7F23E;-webkit-text-stroke:8px #fff;paint-order:stroke fill">AU</div>
      <div style="font:400 22px/1 'Graduate';color:#fff;letter-spacing:.14em;margin-top:12px">RUNNING CLUB</div>
      <div style="font:400 13px/1 'Graduate';color:#C7F23E;letter-spacing:.3em;margin-top:10px">EST. 2026</div></div>`,
  ciencia: centro(236, 296, `
    <div style="position:absolute;inset:0;background:#fff;border:2px solid #23262B;border-radius:10px;transform:rotate(-4deg);
         box-shadow:6px 8px 0 rgba(35,38,43,.35);padding:20px 18px;font-family:'Space Mono';color:#23262B">
      <div style="font:700 30px/1 'Space Mono'">MIAU.LAB</div>
      <div style="font:400 15px/1.3 'Space Mono';margin-top:8px">fórmula nº 07</div>
      <div style="height:2px;background:#23262B;margin:16px 0"></div>
      <div style="font:400 13px/1.45 'Space Mono'">suplemento p/ gatos<br>60 cápsulas<br>lote 26.11</div>
      <div style="position:absolute;left:18px;right:18px;bottom:20px;height:46px;background:repeating-linear-gradient(90deg,#23262B 0 2px,transparent 2px 5px,#23262B 5px 9px,transparent 9px 11px,#23262B 11px 12px,transparent 12px 16px)"></div>
      <div style="position:absolute;right:16px;top:18px;width:30px;height:30px;border-radius:50%;background:#BDEBD6;border:2px solid #23262B"></div></div>`),
};

const DIRECOES = [
  // ---------------- 01 · pop de gibi: página de gibi, três tiras com quadros de larguras diferentes ----------------
  {
    layout: 'tirinha', card: 'var(--violeta)',
    titulo: 'pop de <em>gibi</em>', letra: 'bagel fat one',
    texto: 'cores primárias chapadas, contorno grosso e retícula de gibi. pra petisco e brinquedo que querem ser a alegria da prateleira.',
    cartao: { r: [0, 418, 520, 580], tam: 150 },
    cores: ['#FFD23F', '#F2542D', '#2B59C3', '#1B1B1B'],
    blocos: [
      { r: [0, 0, 380, 400], bg: '#FFD23F', padrao: dots('#F2542D', 16, 22), html: MARCA.gibi, escolhido: [318, 214] },
      { r: [398, 0, 300, 400], bg: '#2B59C3', cheia: { src: 'd1prod-1', px: .5, py: .45 } },
      { r: [716, 0, 364, 400], bg: '#fff', html: paleta([['amarelo gema', '#FFD23F', '#1B1B1B'], ['vermelho tomate', '#F2542D', '#1B1B1B'], ['azul gibi', '#2B59C3', '#FFFBDE'], ['preto nanquim', '#1B1B1B', '#FFFBDE']]) },
      { r: [538, 418, 542, 580], bg: '#FFD23F', cheia: { src: 'd1pet-2', px: .5, py: .3 } },
      { r: [0, 1016, 640, 334], bg: '#F2542D', cheia: { src: 'd1extra', px: .4, py: .5 } },
      { r: [658, 1016, 422, 334], bg: '#2B59C3', html: tipo({ aa: "400 150px 'Bagel Fat One'", aaCor: '#FFD23F', sombra: '6px 6px 0 #1B1B1B', amostra: 'au au!', amostraCss: "400 36px 'Bagel Fat One'", cor: '#FFFBDE', nome: 'bagel fat one' }) },
    ],
  },
  // ---------------- 02 · clube de grife: página de revista, uma foto gigante e coluna lateral ----------------
  {
    layout: 'revista', card: 'var(--plum)',
    titulo: 'clube de <em>grife</em>', letra: 'bodoni moda',
    texto: 'creme, caramelo e café, serifa clássica, monograma, tricô e couro. pra marca premium que quer ser grife, não petshop.',
    cartao: { r: [0, 918, 560, 432], tam: 96 },
    cores: ['#F3E9D7', '#C08A4F', '#4A2E21', '#23392E', '#B8975A'],
    blocos: [
      { r: [0, 0, 680, 900], bg: '#23392E', cheia: { src: 'd2pet-2', px: .55, py: .5 } },
      { r: [698, 0, 382, 440], bg: '#4A2E21', html: MARCA.grife, escolhido: [300, 360] },
      { r: [698, 458, 382, 442], bg: '#F3E9D7', cheia: { src: 'd2prod-2', px: .6, py: .55 } },
      { r: [578, 918, 242, 432], bg: '#fff', html: paleta([['creme', '#F3E9D7', '#4A2E21'], ['caramelo', '#C08A4F', '#2A1A12'], ['café', '#4A2E21', '#F3E9D7'], ['verde-garrafa', '#23392E', '#F3E9D7'], ['ouro velho', '#B8975A', '#2A1A12']]) },
      { r: [838, 918, 242, 432], bg: '#23392E', cheia: { src: 'd2extra', px: .62, py: .55 } },
    ],
  },
  // ---------------- 03 · retrô setentinha: arcos e cantos redondos de anos 70 ----------------
  {
    layout: 'arcos', card: 'var(--wine)',
    titulo: 'retrô <em>setentinha</em>', letra: 'shrikhand',
    texto: 'laranja queimado, mostarda e marrom, letra groovy e grão de filme. pra banho e tosa e petshop de bairro com história pra contar.',
    cartao: { r: [0, 0, 560, 480], tam: 100 },
    cores: ['#E9B03B', '#E2701E', '#6B3A1F', '#7D7A3A', '#F4E3C3'],
    blocos: [
      { r: [578, 0, 502, 480], bg: '#F4E3C3', html: MARCA.setentinha(502, 480) },
      { r: [0, 498, 530, 852], bg: '#E2701E', forma: 'arco', cheia: { src: 'd3pet-2', px: .62, py: .6 } },
      { r: [548, 498, 532, 470], bg: '#6B3A1F', forma: 'arco', cheia: { src: 'd3prod-2', px: .5, py: .78 } },
      { r: [548, 986, 257, 364], bg: '#fff', html: paleta([['mostarda', '#E9B03B', '#3A1E0E'], ['laranja', '#E2701E', '#3A1E0E'], ['marrom vinil', '#6B3A1F', '#F4E3C3'], ['oliva', '#7D7A3A', '#F4E3C3'], ['areia', '#F4E3C3', '#3A1E0E']]), escolhido: [180, 250] },
      { r: [823, 986, 257, 364], bg: '#E9B03B', cheia: { src: 'd3extra', px: .45, py: .45 } },
    ],
  },
  // ---------------- 04 · modo atleta: foto de ação de ponta a ponta, patch do clube por cima ----------------
  {
    layout: 'acao', card: 'var(--creative-purple)',
    titulo: 'modo <em>atleta</em>', letra: 'graduate',
    texto: 'azul royal, verde-limão, cara de uniforme e foto em movimento. pra passeio, coleira e adestramento que vendem energia.',
    cartao: { r: [0, 858, 500, 492], tam: 92, txt: 22, chips: [['azul royal', '#1F3FBF'], ['verde-limão', '#C7F23E'], ['branco quadra', '#EEF1F4'], ['asfalto', '#1E1E24']] },
    cores: ['#1F3FBF', '#C7F23E', '#EEF1F4', '#1E1E24'],
    blocos: [
      { r: [0, 0, 1080, 840], bg: '#8EC9F2', cheia: { src: 'd4pet-2', px: .5, py: .42 } },
      { r: [518, 858, 270, 492], bg: '#B8502E', cheia: { src: 'd4prod-2', px: .5, py: .5 } },
      { r: [806, 858, 274, 492], bg: '#1E1E24', cheia: { src: 'd4extra', px: .4, py: .6 } },
      { r: [748, 520, 286, 286], bg: '#1F3FBF', flutua: -6, html: MARCA.atleta, escolhido: [214, 236] },
    ],
  },
  // ---------------- 05 · ciência fofa: ficha de laboratório, cápsula e quadros de prontuário ----------------
  {
    layout: 'ficha', card: 'var(--ameixa)',
    titulo: 'ciência <em>fofa</em>', letra: 'space mono',
    texto: 'branco, azul clínico e menta, rótulo de laboratório e letra mono. pra nutrição e saúde pet: confiança sem cara de hospital.',
    cartao: { r: [0, 0, 1080, 380], modo: 'h', tam: 132 },
    cores: ['#2F6BFF', '#BDEBD6', '#F5F7F6', '#23262B'],
    blocos: [
      { r: [36, 416, 412, 898], bg: '#BDEBD6', forma: 'capsula', cheia: { src: 'd5pet-1', px: .5, py: .62 } },
      { r: [484, 398, 280, 467], bg: '#F5F7F6', cheia: { src: 'd5prod-2', px: .5, py: .62 } },
      { r: [782, 398, 298, 467], bg: '#BDEBD6', cheia: { src: 'd5extra', px: .45, py: .5 }, escolhido: [200, 390] },
      { r: [484, 883, 280, 467], bg: '#2F6BFF', html: MARCA.ciencia },
      { r: [782, 883, 298, 467], bg: '#fff', html: paleta([['azul clínico', '#2F6BFF', '#FFFBDE'], ['menta', '#BDEBD6', '#23262B'], ['branco jaleco', '#F5F7F6', '#23262B'], ['grafite', '#23262B', '#FFFBDE']]) },
    ],
  },
];

// Capa: fundo marfim, título em serifa no topo, foto inteira do gato preto em quadro à direita,
// índice das 5 direções à esquerda. (A capa da referência tinha "5" gigante + pílula: não usar.)
const CAPA = { cheia: { src: 'capa-2', px: .45, py: .45 } };
