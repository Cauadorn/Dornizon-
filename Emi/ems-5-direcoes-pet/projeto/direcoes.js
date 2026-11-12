// Conteúdo do carrossel "5 direções criativas pra marcas pet" (@itsemsdesign).
// Cada direção = 8 quadros em volta do cartão central (grade 3 x 3, como a referência).
// Fotos: Nano Banana Pro em fundo #E9E9E9, recortadas e pousadas na cor da direção (regra "Geração de imagem" do DS EMS).
// Posição da foto: o ponto (ax, ay) da imagem (0 a 1) cai no ponto (x, y) do quadro; h = altura da imagem em px.

const dots = (cor, passo = 18, tam = 30) => `radial-gradient(circle, ${cor} ${tam}%, transparent ${tam + 3}%) 0 0 / ${passo}px ${passo}px`;
const grade = (cor, passo = 26) => `linear-gradient(${cor} 1px, transparent 1px) 0 0 / ${passo}px ${passo}px, linear-gradient(90deg, ${cor} 1px, transparent 1px) 0 0 / ${passo}px ${passo}px`;
const pista = (cor) => `repeating-linear-gradient(-58deg, transparent 0 46px, ${cor} 46px 60px)`;

const paleta = (cores) => `<div class="paleta" style="inset:0">${cores.map(([nome, hex, tx]) =>
  `<div style="background:${hex};color:${tx}"><b>${nome}</b><small>${hex.toUpperCase()}</small></div>`).join('')}</div>`;

const tipo = ({ fonte, aa, aaCor, sombra = 'none', amostra, amostraCss, cor, nome }) =>
  `<div class="tipo" style="inset:0;color:${cor}">
     <div class="aa" style="font:${aa};line-height:.86;color:${aaCor};text-shadow:${sombra}">Aa</div>
     <div class="amostra" style="font:${amostraCss};line-height:1.1">${amostra}</div>
     <div class="nome">${nome}</div></div>`;

const DIRECOES = [
  // ---------------- 01 · pop de gibi ----------------
  {
    titulo: 'pop de <em>gibi</em>', card: 'var(--violeta)',
    texto: 'cores primárias chapadas, contorno grosso e retícula de gibi. pra petisco e brinquedo que querem ser a alegria da prateleira.',
    quadros: {
      TL: { bg: '#F2542D', padrao: dots('#E0401B'), foto: { src: 'd1pet-3', h: 1150, ax: .67, ay: .11, x: 160, y: 168 } },
      TC: { bg: '#2B59C3', padrao: dots('#3A68D2', 20), foto: { src: 'd1prod-2', h: 262, ax: .5, ay: .5, x: 214, y: 222 } },
      TR: { bg: '#FFD23F', padrao: dots('#F2542D', 16, 22), escolhido: [196, 326], html: `
        <svg viewBox="0 0 308 408" width="308" height="408" style="position:absolute;inset:0">
          <path d="M206.8 250.6 L246 330 L158.4 259.9 A125 100 0 1 1 206.8 250.6 Z" fill="#fff" stroke="#1B1B1B" stroke-width="7" stroke-linejoin="round"/></svg>
        <div style="position:absolute;left:0;right:0;top:104px;text-align:center;font:400 112px/1 'Bagel Fat One';color:#1B1B1B;transform:rotate(-6deg)">AU!</div>
        <div style="position:absolute;left:0;right:0;top:338px;text-align:center;font:400 30px/1 'Bagel Fat One';color:#F2542D;-webkit-text-stroke:6px #1B1B1B;paint-order:stroke fill">petiscaria</div>` },
      ML: { bg: '#FFD23F', padrao: dots('#F5BD12', 18), foto: { src: 'd1pet-1', h: 410, ax: .5, ay: .5, x: 150, y: 262 } },
      MR: { bg: '#fff', html: paleta([['amarelo gema', '#FFD23F', '#1B1B1B'], ['vermelho tomate', '#F2542D', '#1B1B1B'], ['azul gibi', '#2B59C3', '#FFFBDE'], ['preto nanquim', '#1B1B1B', '#FFFBDE']]) },
      BL: { bg: '#2B59C3', html: tipo({ aa: "400 182px 'Bagel Fat One'", aaCor: '#FFD23F', sombra: '7px 7px 0 #1B1B1B', amostra: 'au au!', amostraCss: "400 40px 'Bagel Fat One'", cor: '#FFFBDE', nome: 'bagel fat one' }) },
      BC: { bg: '#FFF4DE', padrao: dots('#F8C9B8', 18), foto: { src: 'd1pet-4', h: 330, ax: .5, ay: .5, x: 214, y: 212 } },
      BR: { bg: '#F2542D', padrao: dots('#E0401B'), foto: { src: 'd1prod-3', h: 540, ax: .44, ay: .62, x: 150, y: 200 } },
    },
  },
  // ---------------- 02 · clube de grife ----------------
  {
    titulo: 'clube de <em>grife</em>', card: 'var(--plum)',
    texto: 'creme, caramelo e café, serifa clássica, monograma, tricô e couro. pra marcas premium que querem ser grife, não petshop.',
    quadros: {
      TL: { bg: '#4A2E21', escolhido: [256, 360], html: `
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#D8BC7E;text-align:center;padding-top:20px">
          <div style="width:74px;height:74px;border:1.5px solid #D8BC7E;border-radius:50%;display:grid;place-items:center;font:italic 500 32px/1 'Bodoni Moda'">MC</div>
          <div style="font:500 50px/1 'Bodoni Moda';margin-top:26px;letter-spacing:.01em">Maison</div>
          <div style="font:italic 500 60px/1 'Bodoni Moda';margin-top:2px">Caramelo</div>
          <div style="width:120px;height:1px;background:#D8BC7E;margin:20px 0 14px;opacity:.7"></div>
          <div style="font:500 13px/1 'Bodoni Moda';letter-spacing:.34em">PET COUTURE</div></div>` },
      TC: { bg: '#F3E9D7', foto: { src: 'd2pet-1', h: 372, ax: .5, ay: .52, x: 214, y: 214 } },
      TR: { bg: '#23392E', foto: { src: 'd2prod-1', h: 600, ax: .8, ay: .8, x: 190, y: 286 } },
      ML: { bg: '#fff', html: paleta([['creme de leite', '#F3E9D7', '#4A2E21'], ['caramelo', '#C08A4F', '#2A1A12'], ['café coado', '#4A2E21', '#F3E9D7'], ['verde-garrafa', '#23392E', '#F3E9D7'], ['ouro velho', '#B8975A', '#2A1A12']]) },
      MR: { bg: '#C08A4F', foto: { src: 'd2pet-3', h: 640, ax: 0, ay: 0, x: -8, y: 34 } },
      BL: { bg: '#4A2E21', foto: { src: 'd2prod-2', h: 262, ax: .5, ay: .5, x: 154, y: 210 } },
      BC: { bg: '#EADBC2', html: tipo({ aa: "italic 500 200px 'Bodoni Moda'", aaCor: '#4A2E21', amostra: 'coleção inverno', amostraCss: "500 32px 'Bodoni Moda'", cor: '#4A2E21', nome: 'bodoni moda' }) },
      BR: { bg: '#F3E9D7', foto: { src: 'd2pet-4', h: 560, ax: .6, ay: .34, x: 108, y: 200 } },
    },
  },
  // ---------------- 03 · retrô setentinha ----------------
  {
    titulo: 'retrô <em>setentinha</em>', card: 'var(--wine)', tituloTam: 84,
    texto: 'laranja queimado, mostarda e marrom, letra groovy e grão de filme. pra banho e tosa e petshop de bairro com história pra contar.',
    quadros: {
      TL: { bg: '#E9B03B', foto: { src: 'd3pet-3', h: 800, ax: .5, ay: .36, x: 154, y: 214 } },
      TC: { bg: '#6B3A1F', foto: { src: 'd3prod-2', h: 212, ax: .5, ay: .5, x: 214, y: 222 } },
      TR: { bg: '#F4E3C3', escolhido: [196, 326], html: `
        <svg viewBox="0 0 308 408" width="308" height="408" style="position:absolute;inset:0">
          <g fill="none" stroke-width="30"><circle cx="154" cy="520" r="250" stroke="#7D7A3A"/><circle cx="154" cy="520" r="220" stroke="#6B3A1F"/>
          <circle cx="154" cy="520" r="190" stroke="#E2701E"/><circle cx="154" cy="520" r="160" stroke="#E9B03B"/></g></svg>
        <div style="position:absolute;left:0;right:0;top:48px;text-align:center;font:400 78px/.9 'Shrikhand';color:#6B3A1F;text-shadow:4px 4px 0 #E2701E;transform:rotate(-5deg)">pelo<br>solto</div>
        <div style="position:absolute;left:0;right:0;top:218px;text-align:center;font:400 26px/1 'Shrikhand';color:#7D7A3A">banho & tosa</div>` },
      ML: { bg: '#E2701E', foto: { src: 'd3pet-2', h: 400, ax: .42, ay: .5, x: 168, y: 270 } },
      MR: { bg: '#fff', html: paleta([['mostarda', '#E9B03B', '#3A1E0E'], ['laranja queimado', '#E2701E', '#3A1E0E'], ['marrom vinil', '#6B3A1F', '#F4E3C3'], ['verde oliva', '#7D7A3A', '#F4E3C3'], ['areia', '#F4E3C3', '#3A1E0E']]) },
      BL: { bg: '#7D7A3A', html: tipo({ aa: "400 168px 'Shrikhand'", aaCor: '#F4E3C3', sombra: '6px 6px 0 #E2701E', amostra: 'paz & ração', amostraCss: "400 34px 'Shrikhand'", cor: '#F4E3C3', nome: 'shrikhand' }) },
      BC: { bg: '#F4E3C3', foto: { src: 'd3pet-4', h: 420, ax: .36, ay: .46, x: 214, y: 208 } },
      BR: { bg: '#E2701E', foto: { src: 'd3prod-3', h: 600, ax: .8, ay: .68, x: 150, y: 204 } },
    },
  },
  // ---------------- 04 · modo atleta ----------------
  {
    titulo: 'modo <em>atleta</em>', card: 'var(--creative-purple)',
    texto: 'azul royal, verde-limão, cara de uniforme e foto em movimento. pra passeio, coleira e adestramento que vendem energia.',
    quadros: {
      TL: { bg: '#1F3FBF', escolhido: [256, 360], html: `
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding-top:30px">
          <div style="font:400 150px/1 'Graduate';color:#C7F23E;-webkit-text-stroke:8px #fff;paint-order:stroke fill">AU</div>
          <div style="font:400 25px/1 'Graduate';color:#fff;letter-spacing:.14em;margin-top:16px">RUNNING CLUB</div>
          <div style="font:400 14px/1 'Graduate';color:#C7F23E;letter-spacing:.3em;margin-top:12px">EST. 2026</div></div>` },
      TC: { bg: '#EEF1F4', padrao: pista('#E1E6EC'), foto: { src: 'd4pet-2', h: 360, ax: .5, ay: .5, x: 214, y: 214 } },
      TR: { bg: '#1E1E24', foto: { src: 'd4prod-1', h: 620, ax: .38, ay: .42, x: 154, y: 206 } },
      ML: { bg: '#fff', html: paleta([['azul royal', '#1F3FBF', '#FFFBDE'], ['verde-limão', '#C7F23E', '#1E1E24'], ['branco quadra', '#EEF1F4', '#1E1E24'], ['asfalto', '#1E1E24', '#FFFBDE']]) },
      MR: { bg: '#C7F23E', foto: { src: 'd4pet-4', h: 820, ax: .7, ay: .22, x: 168, y: 200 } },
      BL: { bg: '#EEF1F4', padrao: pista('#E1E6EC'), foto: { src: 'd4prod-2', h: 196, ax: .5, ay: .5, x: 154, y: 214 } },
      BC: { bg: '#1E1E24', html: tipo({ aa: "400 180px 'Graduate'", aaCor: '#C7F23E', amostra: 'bora correr?', amostraCss: "400 32px 'Graduate'", cor: '#FFFBDE', nome: 'graduate' }) },
      BR: { bg: '#EEF1F4', padrao: pista('#DDF5A0'), foto: { src: 'd4pet-1', h: 330, ax: .5, ay: .5, x: 154, y: 200, flip: true } },
    },
  },
  // ---------------- 05 · ciência fofa ----------------
  {
    titulo: 'ciência <em>fofa</em>', card: 'var(--ameixa)',
    texto: 'branco, azul clínico e menta, rótulo de laboratório e letra mono. pra nutrição e saúde pet: confiança sem cara de hospital.',
    quadros: {
      TL: { bg: '#BDEBD6', foto: { src: 'd5pet-1', h: 1080, ax: .5, ay: .2, x: 154, y: 206 } },
      TC: { bg: '#F5F7F6', padrao: grade('#E3E8EC'), foto: { src: 'd5prod-2', h: 232, ax: .5, ay: .5, x: 214, y: 220 } },
      TR: { bg: '#2F6BFF', escolhido: [196, 326], html: `
        <div style="position:absolute;left:36px;top:58px;width:236px;height:296px;background:#fff;border:2px solid #23262B;border-radius:10px;transform:rotate(-4deg);
             box-shadow:6px 8px 0 rgba(35,38,43,.35);padding:20px 18px;font-family:'Space Mono';color:#23262B">
          <div style="font:700 30px/1 'Space Mono'">MIAU.LAB</div>
          <div style="font:400 15px/1.3 'Space Mono';margin-top:8px">fórmula nº 07</div>
          <div style="height:2px;background:#23262B;margin:16px 0"></div>
          <div style="font:400 13px/1.45 'Space Mono'">suplemento p/ gatos<br>60 cápsulas<br>lote 26.11</div>
          <div style="position:absolute;left:18px;right:18px;bottom:20px;height:46px;background:repeating-linear-gradient(90deg,#23262B 0 2px,transparent 2px 5px,#23262B 5px 9px,transparent 9px 11px,#23262B 11px 12px,transparent 12px 16px)"></div>
          <div style="position:absolute;right:16px;top:18px;width:30px;height:30px;border-radius:50%;background:#BDEBD6;border:2px solid #23262B"></div></div>` },
      ML: { bg: '#2F6BFF', foto: { src: 'd5pet-3', h: 450, ax: .44, ay: .5, x: 150, y: 266 } },
      MR: { bg: '#fff', html: paleta([['azul clínico', '#2F6BFF', '#FFFBDE'], ['menta', '#BDEBD6', '#23262B'], ['branco jaleco', '#F5F7F6', '#23262B'], ['grafite', '#23262B', '#FFFBDE']]) },
      BL: { bg: '#23262B', html: tipo({ aa: "700 156px 'Space Mono'", aaCor: '#BDEBD6', amostra: 'fórmula_07', amostraCss: "400 30px 'Space Mono'", cor: '#FFFBDE', nome: 'space mono' }) },
      BC: { bg: '#BDEBD6', foto: { src: 'd5pet-4', h: 410, ax: .5, ay: .5, x: 214, y: 214 } },
      BR: { bg: '#F5F7F6', padrao: grade('#E3E8EC'), foto: { src: 'd5prod-1', h: 640, ax: .42, ay: .44, x: 150, y: 204 } },
    },
  },
];

// Capa: gato preto (diretoria criativa) recortado sobre o violeta.
const CAPA = {
  gato: { src: 'gato-3', h: 1150, ax: .5, ay: 1, x: 660, y: 1352, sombra: false },
  selecao: 'left:372px;top:196px;width:560px;height:520px',
  nota: { texto: 'diretoria<br>criativa', x: 150, y: 200, lx: 262, ly: 214, lw: 110, lh: 70, path: 'M4 14 C44 4 84 22 106 62' },
};

// Chamada: o mesmo gato acenando.
const CHAMADA = {
  gato: { src: 'gato-2', h: 760, ax: .5, ay: 1, x: 800, y: 1352, sombra: false },
};
