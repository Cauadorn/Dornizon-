// Uma lâmina por isca. Sem nome escrito: a isca é a colagem de recortes embaixo da caixa.
// estrelas: [cx, cy, raio] · icones: [tipo, x, y, tamanho, cor, giro, opacidade]
// iscas: { src (em recortes/), x, y, w, r (giro), z, flip } no quadro de 1080 × 1350
const LAMINAS = [
  { tema: 'gatos', iscas: [
      { src: 'gatos-1.png', x: 176, y: 770, w: 168, z: 2 },
      { src: 'gatos-6.png', x: 408, y: 748, w: 200 }, { src: 'gatos-2.png', x: 500, y: 800, w: 200, z: 1 },
      { src: 'gatos-5.png', x: 600, y: 880, w: 176, z: 2, flip: 1 }, { src: 'gatos-4.png', x: 396, y: 930, w: 250, z: 3 },
    ], estrelas: [[1000, 170, 330], [60, 1260, 300]],  icones: [['brilho', 840, 430, 64, 'manteiga'], ['brilho', 930, 520, 30, 'ivory', 0, .8], ['espiral', 96, 560, 92, 'lavanda', -12, .9]] },
  { tema: 'divas', iscas: [
      { src: 'divas-ts-reputation.jpg', x: 182, y: 742, w: 168, r: -5 }, { src: 'divas-ts-1989.jpg', x: 160, y: 912, w: 180, r: 4, z: 2 },
      { src: 'divas-od-artofloving.jpg', x: 404, y: 716, w: 178, r: 4 }, { src: 'divas-or-guts.jpg', x: 562, y: 742, w: 176, r: -5 },
      { src: 'divas-sc-sns.jpg', x: 398, y: 852, w: 186, r: -5, z: 2 }, { src: 'divas-or-sour.jpg', x: 560, y: 880, w: 180, r: 6, z: 2 }, { src: 'divas-ts-showgirl.jpg', x: 655, y: 925, w: 150, r: -4, z: 2 },
      { src: 'divas-od-messy.jpg', x: 410, y: 1000, w: 196, r: 5, z: 3 }, { src: 'divas-ts-lover.jpg', x: 590, y: 1030, w: 190, r: -6, z: 3 },
    ],
          estrelas: [[80, 560, 300], [1010, 1230, 320]],  icones: [['xoxo', 800, 440, 150, 'pink', -8], ['brilho', 110, 470, 54, 'manteiga'], ['brilho', 960, 1010, 34, 'ivory', 0, .8]] },
  { tema: 'series', iscas: [
      { src: 'series-ahs-2.jpg', x: 186, y: 742, w: 150, r: -4 }, { src: 'series-gg-1.jpg', x: 158, y: 935, w: 172, r: 4, z: 2 },
      { src: 'series-gilmore-2.jpg', x: 404, y: 708, w: 160, r: 4 }, { src: 'series-ahs-3.jpg', x: 552, y: 740, w: 158, r: -4 }, { src: 'series-gg-2.jpg', x: 690, y: 880, w: 150, r: 5 },
      { src: 'series-gilmore-1.jpg', x: 402, y: 880, w: 190, r: -4, z: 2 }, { src: 'series-ahs-1.jpg', x: 580, y: 930, w: 180, r: 5, z: 2 },
    ],
         estrelas: [[1010, 520, 300], [90, 1240, 280]],  icones: [['estrela', 100, 500, 84, 'manteiga', -14], ['brilho', 900, 470, 44, 'ivory', 0, .85], ['espiral', 880, 1040, 86, 'lavanda', 20, .9]] },
  { tema: 'massas',      estrelas: [[70, 480, 280], [1000, 1180, 330]],  icones: [['brilho', 860, 440, 70, 'manteiga'], ['brilho', 790, 530, 30, 'ivory', 0, .8], ['xoxo', 80, 520, 130, 'lavanda', 10, .9]] },
  { tema: 'cameras',     estrelas: [[1000, 190, 320], [70, 1210, 310]],  icones: [['brilho', 120, 480, 60, 'manteiga'], ['brilho', 190, 560, 28, 'ivory', 0, .8], ['estrela', 880, 470, 80, 'lavanda', 16, .9]] },
  { tema: 'doces',       estrelas: [[90, 540, 300], [1010, 1250, 300]],  icones: [['espiral', 850, 440, 96, 'pink', 8], ['brilho', 120, 480, 46, 'manteiga'], ['brilho', 950, 1000, 32, 'ivory', 0, .8]] },
  { tema: 'livros',      estrelas: [[1000, 500, 300], [80, 1230, 300]],  icones: [['brilho', 850, 450, 66, 'manteiga'], ['brilho', 940, 540, 30, 'ivory', 0, .8], ['estrela', 96, 500, 80, 'lavanda', -10, .9]] },
  { tema: 'ferramentas', estrelas: [[80, 500, 290], [1010, 1200, 320]],  icones: [['xoxo', 810, 440, 140, 'lavanda', -6, .9], ['brilho', 110, 480, 56, 'manteiga'], ['brilho', 180, 560, 28, 'ivory', 0, .8]] },
  { tema: 'vazia', fim: true, estrelas: [[1010, 180, 320], [70, 1250, 300]], icones: [['brilho', 110, 500, 60, 'manteiga'], ['brilho', 185, 585, 28, 'ivory', 0, .8]] },
];
if (typeof module !== 'undefined') module.exports = { LAMINAS };
