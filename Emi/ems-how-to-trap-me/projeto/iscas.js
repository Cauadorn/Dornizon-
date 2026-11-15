// Uma lâmina por isca. Sem nome escrito: a isca é a colagem de recortes embaixo da caixa.
// estrelas: [cx, cy, raio] · icones: [tipo, x, y, tamanho, cor, giro, opacidade]
// iscas: { src (em recortes/), x, y, w, r (giro), z, flip } no quadro de 1080 × 1350
const LAMINAS = [
  { tema: 'gatos', iscas: [
      { src: 'gatos-1.png', x: 192, y: 748, w: 150 }, { src: 'gatos-6.png', x: 400, y: 744, w: 190 }, { src: 'gato-tricolor.png', x: 566, y: 770, w: 150 },
      { src: 'gato-filhote.png', x: 232, y: 896, w: 112, z: 2 }, { src: 'gato-olhao.png', x: 404, y: 846, w: 172, z: 2 }, { src: 'gato-fone.png', x: 562, y: 856, w: 160, z: 2 },
      { src: 'gato-laranja-branco.png', x: 690, y: 884, w: 128, z: 1 }, { src: 'gato-dancando.png', x: 476, y: 906, w: 136, z: 3 },
      { src: 'gatos-4.png', x: 372, y: 1004, w: 232, z: 4 },
      { src: 'gato-joinha.png', x: 566, y: 950, w: 150, z: 3 }, { src: 'gato-laranja-pe.png', x: 640, y: 1010, w: 124, z: 5 },
      { src: 'gato-pulando.png', x: 36, y: 846, w: 200, z: 5 },
    ], fundo: 'violeta', estrela: 'lavanda', estrelas: [[1010, 150, 380], [60, 520, 300], [1050, 1010, 300], [120, 1290, 340], [560, 420, 190]],
    icones: [['brilho', 860, 420, 78, 'manteiga'], ['brilho', 955, 520, 34, 'ivory'], ['espiral', 880, 1040, 104, 'lavanda', -12], ['brilho', 120, 400, 40, 'ivory']] },
  { tema: 'divas', iscas: [
      { src: 'divas-ts-reputation.jpg', x: 182, y: 742, w: 168, r: -5 }, { src: 'divas-ts-1989.jpg', x: 160, y: 912, w: 180, r: 4, z: 2 },
      { src: 'divas-od-artofloving.jpg', x: 404, y: 716, w: 178, r: 4 }, { src: 'divas-or-guts.jpg', x: 562, y: 742, w: 176, r: -5 },
      { src: 'divas-sc-sns.jpg', x: 398, y: 852, w: 186, r: -5, z: 2 }, { src: 'divas-or-sour.jpg', x: 560, y: 880, w: 180, r: 6, z: 2 }, { src: 'divas-ts-showgirl.jpg', x: 655, y: 925, w: 150, r: -4, z: 2 },
      { src: 'divas-od-messy.jpg', x: 410, y: 1000, w: 196, r: 5, z: 3 }, { src: 'divas-ts-lover.jpg', x: 590, y: 1030, w: 190, r: -6, z: 3 },
      { src: 'divas-a7x-nightmare.jpg', x: 190, y: 1076, w: 166, r: -6, z: 4 }, { src: 'divas-a7x-cityofevil.jpg', x: 756, y: 1050, w: 150, r: 7, z: 3 },
    ],
          fundo: 'plum', estrela: 'violeta-2', estrelas: [[60, 170, 360], [1040, 560, 320], [40, 1000, 300], [960, 1290, 360], [520, 430, 180]],
    icones: [['brilho', 110, 470, 70, 'manteiga'], ['brilho', 200, 570, 30, 'ivory'], ['estrela', 900, 430, 96, 'lavanda', 14], ['brilho', 950, 1040, 44, 'ivory']] },
  { tema: 'series', iscas: [
      { src: 'series-ahs-2.jpg', x: 186, y: 742, w: 150, r: -4 }, { src: 'series-gg-1.jpg', x: 158, y: 935, w: 172, r: 4, z: 2 },
      { src: 'series-gilmore-2.jpg', x: 404, y: 708, w: 160, r: 4 }, { src: 'series-ahs-3.jpg', x: 552, y: 740, w: 158, r: -4 }, { src: 'series-gg-2.jpg', x: 690, y: 880, w: 150, r: 5 },
      { src: 'series-gilmore-1.jpg', x: 402, y: 880, w: 190, r: -4, z: 2 }, { src: 'series-ahs-1.jpg', x: 580, y: 930, w: 180, r: 5, z: 2 },
    ],
         fundo: 'violeta-2', estrela: 'lavanda', estrelas: [[1010, 170, 370], [70, 560, 300], [1040, 1040, 300], [110, 1280, 350], [540, 420, 180]],
    icones: [['estrela', 96, 430, 100, 'manteiga', -14], ['brilho', 900, 440, 60, 'ivory'], ['espiral', 900, 1060, 100, 'ivory', 20, .9], ['brilho', 215, 560, 30, 'ivory']] },
  { tema: 'massas', iscas: [
      { src: 'massas-5.png', x: 180, y: 770, w: 170 }, { src: 'massas-1.png', x: 400, y: 742, w: 232 }, { src: 'massa-lasanha-1.png', x: 590, y: 772, w: 168 },
      { src: 'massa-espaguete-monte.png', x: 196, y: 876, w: 150, z: 2 }, { src: 'massas-2.png', x: 392, y: 850, w: 300, z: 2 }, { src: 'massa-lasanha-garfo.png', x: 668, y: 850, w: 110, z: 1 },
      { src: 'massas-6.png', x: 384, y: 1046, w: 204, z: 4 },
      { src: 'massas-3.png', x: 566, y: 986, w: 222, z: 3 }, { src: 'massa-lasanha-3.png', x: 724, y: 1052, w: 150, z: 4 },
      { src: 'massa-gato-lasanha.png', x: 596, y: 1100, w: 122, z: 5 },
    ], fundo: 'ameixa', estrela: 'violeta-2', estrelas: [[70, 160, 360], [1030, 540, 320], [50, 1010, 300], [970, 1290, 350], [540, 430, 180]],
    icones: [['brilho', 880, 430, 80, 'manteiga'], ['brilho', 800, 530, 32, 'ivory'], ['espiral', 90, 470, 104, 'lavanda', 10], ['brilho', 940, 1040, 40, 'ivory']] },
  { tema: 'cameras', iscas: [
      { src: 'cameras-3.png', x: 186, y: 752, w: 164 }, { src: 'cameras-6.png', x: 400, y: 744, w: 200 }, { src: 'camx-a-1.png', x: 580, y: 784, w: 172 },
      { src: 'cameras-4.png', x: 204, y: 880, w: 142, z: 2 }, { src: 'cameras-1.png', x: 392, y: 858, w: 252, z: 3 }, { src: 'cameras-5.png', x: 624, y: 904, w: 172, z: 2 },
      { src: 'camx-c-1.png', x: 396, y: 1056, w: 190, z: 4 }, { src: 'cameras-7.png', x: 588, y: 1040, w: 196, z: 4 }, { src: 'camx-b-1.png', x: 750, y: 1076, w: 156, z: 3 },
    ], fundo: 'violeta', estrela: 'lavanda', estrelas: [[1010, 160, 380], [60, 540, 300], [1050, 1020, 300], [110, 1290, 340], [550, 420, 180]],
    icones: [['brilho', 110, 440, 72, 'manteiga'], ['brilho', 200, 545, 30, 'ivory'], ['estrela', 890, 440, 92, 'lavanda', 16], ['brilho', 930, 1050, 42, 'ivory']] },
  { tema: 'doces', iscas: [
      { src: 'doce1-1.png', x: 190, y: 742, w: 152 }, { src: 'doce3-1.png', x: 420, y: 740, w: 112 }, { src: 'doce6-1.png', x: 540, y: 762, w: 152 },
      { src: 'doce2-1.png', x: 194, y: 900, w: 152, z: 2 }, { src: 'doce5-1.png', x: 398, y: 822, w: 172, z: 2 }, { src: 'doce8-1.png', x: 604, y: 852, w: 100, z: 2 },
      { src: 'doce7-1.png', x: 694, y: 906, w: 118, z: 1 },
      { src: 'doce4-1.png', x: 416, y: 1040, w: 154, z: 4 }, { src: 'doce9-1.png', x: 562, y: 1064, w: 200, z: 4 }, { src: 'docex-a-1.png', x: 740, y: 1060, w: 140, z: 3 },
    ], fundo: 'plum', estrela: 'violeta-2', estrelas: [[60, 170, 360], [1040, 560, 320], [40, 1000, 300], [960, 1290, 360], [520, 430, 180]],
    icones: [['espiral', 870, 420, 108, 'manteiga', 8], ['brilho', 110, 450, 60, 'ivory'], ['brilho', 195, 550, 28, 'ivory'], ['brilho', 950, 1040, 44, 'lavanda']] },
  { tema: 'livros',      fundo: 'violeta-2', estrela: 'lavanda', estrelas: [[1010, 170, 370], [70, 560, 300], [1040, 1040, 300], [110, 1280, 350], [540, 420, 180]],
    icones: [['brilho', 870, 430, 76, 'manteiga'], ['brilho', 955, 535, 32, 'ivory'], ['estrela', 92, 450, 96, 'ivory', -10, .9], ['brilho', 930, 1050, 40, 'ivory']] },
  { tema: 'ferramentas', fundo: 'ameixa', estrela: 'violeta-2', estrelas: [[70, 160, 360], [1030, 540, 320], [50, 1010, 300], [970, 1290, 350], [540, 430, 180]],
    icones: [['brilho', 110, 440, 72, 'manteiga'], ['brilho', 200, 545, 30, 'ivory'], ['espiral', 880, 430, 104, 'lavanda', -8], ['brilho', 940, 1040, 42, 'ivory']] },
  { tema: 'vazia', fim: true, fundo: 'violeta', estrela: 'lavanda', estrelas: [[1010, 150, 380], [60, 520, 300], [1050, 1010, 300], [120, 1290, 340], [560, 420, 190]],
    icones: [['brilho', 860, 420, 78, 'manteiga'], ['brilho', 955, 520, 34, 'ivory'], ['brilho', 120, 420, 44, 'ivory']] },
];
if (typeof module !== 'undefined') module.exports = { LAMINAS };
