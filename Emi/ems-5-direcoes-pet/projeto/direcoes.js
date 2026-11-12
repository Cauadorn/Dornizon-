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

const MARCA = {
  gibi: centro(308, 408, `
    <svg viewBox="0 0 308 408" width="308" height="408" style="position:absolute;inset:0">
      <path d="M206.8 250.6 L246 330 L158.4 259.9 A125 100 0 1 1 206.8 250.6 Z" fill="#fff" stroke="#1B1B1B" stroke-width="7" stroke-linejoin="round"/></svg>
    <div style="position:absolute;left:0;right:0;top:104px;text-align:center;font:400 112px/1 'Bagel Fat One';color:#1B1B1B;transform:rotate(-6deg)">AU!</div>
    <div style="position:absolute;left:0;right:0;top:338px;text-align:center;font:400 30px/1 'Bagel Fat One';color:#F2542D;-webkit-text-stroke:6px #1B1B1B;paint-order:stroke fill">petiscaria</div>`),
  grife: `
    <div class="pilha" style="color:#D8BC7E">
      <div style="width:80px;height:80px;border:1.5px solid #D8BC7E;border-radius:50%;display:grid;place-items:center;font:italic 500 34px/1 'Bodoni Moda'">MC</div>
      <div style="font:500 56px/1 'Bodoni Moda';margin-top:26px;letter-spacing:.01em">Maison</div>
      <div style="font:italic 500 68px/1 'Bodoni Moda';margin-top:2px">Caramelo</div>
      <div style="width:140px;height:1px;background:#D8BC7E;margin:22px 0 14px;opacity:.7"></div>
      <div style="font:500 14px/1 'Bodoni Moda';letter-spacing:.34em">PET COUTURE</div></div>`,
  setentinha: (w, h) => `
    <svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" style="position:absolute;inset:0">
      <g fill="none" stroke-width="30"><circle cx="${w / 2}" cy="${h + 250}" r="322" stroke="#7D7A3A"/><circle cx="${w / 2}" cy="${h + 250}" r="292" stroke="#6B3A1F"/>
      <circle cx="${w / 2}" cy="${h + 250}" r="262" stroke="#E2701E"/><circle cx="${w / 2}" cy="${h + 250}" r="232" stroke="#E9B03B"/></g></svg>
    <div style="position:absolute;left:0;right:0;top:34px;text-align:center;font:400 100px/.9 'Shrikhand';color:#6B3A1F;text-shadow:5px 5px 0 #E2701E;transform:rotate(-5deg)">pelo<br>solto</div>
    <div style="position:absolute;left:0;right:0;top:238px;text-align:center;font:400 28px/1 'Shrikhand';color:#7D7A3A">banho & tosa</div>`,
  atleta: `
    <div class="pilha">
      <div style="font:400 150px/1 'Graduate';color:#C7F23E;-webkit-text-stroke:8px #fff;paint-order:stroke fill">AU</div>
      <div style="font:400 25px/1 'Graduate';color:#fff;letter-spacing:.14em;margin-top:16px">RUNNING CLUB</div>
      <div style="font:400 14px/1 'Graduate';color:#C7F23E;letter-spacing:.3em;margin-top:12px">EST. 2026</div></div>`,
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
  // ---------------- 01 · pop de gibi ----------------
  {
    titulo: 'pop de <em>gibi</em>', pra: 'petisco e brinquedo', card: 'var(--violeta)',
    texto: 'cores primárias chapadas, contorno grosso e retícula de gibi. pra petisco e brinquedo que querem ser a alegria da prateleira.',
    heroi: { bg: '#FFD23F', cheia: { src: 'd1pet-2', px: .5, py: .3 } },
    marca: { bg: '#FFD23F', padrao: dots('#F2542D', 16, 22), html: MARCA.gibi, cursor: [326, 290] },
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
    marca: { bg: '#4A2E21', html: MARCA.grife, cursor: [330, 330] },
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
    marca: { bg: '#F4E3C3', html: MARCA.setentinha(422, 400), cursor: [330, 300] },
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
    marca: { bg: '#1F3FBF', html: MARCA.atleta, cursor: [330, 310] },
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
    marca: { bg: '#2F6BFF', html: MARCA.ciencia, cursor: [300, 320] },
    quadrado: { bg: '#F5F7F6', cheia: { src: 'd5prod-2', px: .5, py: .72 } },
    alto: { bg: '#BDEBD6', cheia: { src: 'd5extra', px: .45, py: .5 } },
    paleta: [['azul clínico', '#2F6BFF', '#FFFBDE'], ['menta', '#BDEBD6', '#23262B'], ['branco jaleco', '#F5F7F6', '#23262B'], ['grafite', '#23262B', '#FFFBDE']],
    tipo: { bg: '#23262B', aa: "700 96px 'Space Mono'", aaCor: '#BDEBD6', amostra: 'fórmula_07', amostraCss: "400 22px 'Space Mono'", cor: '#FFFBDE', nome: 'space mono' },
  },
];

// Capa: capa de revista com o gato preto de modelo (fundo violeta com estrelas em retícula, aprovado).
const CAPA = { foto: { src: 'capa-2', px: .5, py: .5 }, recorte: 'capa-2-gato' };

// Chamada: enquete; o gato (fundo ameixa) levanta a pata até a opção marcada.
const CHAMADA = { foto: { src: 'cham-2', px: .85, py: .95, zoom: 1.25 }, recorte: 'cham-2-gato', marcada: 1 };
