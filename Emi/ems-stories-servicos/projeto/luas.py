# Trata as fotos da lua (NASA/GSFC Scientific Visualization Studio, domínio público) na paleta da EMS.
# Para cada fase gera: <fase>-<tema>.jpg (mapa de gradiente, céu = cor de fundo do story)
# e <fase>-<tema>-frente.png (só a parte acesa, com alfa, para a letra passar por trás da lua).
import sys
from PIL import Image, ImageFilter
import numpy as np
H = lambda h: np.array([int(h[i:i+2], 16) for i in (1, 3, 5)], float)
TEMAS = {
  'noite':    [(0, '#2a1433'), (.10, '#3d1c46'), (.38, '#5b216c'), (.62, '#7b4df2'), (.82, '#c0a5c4'), (1, '#fffbde')],
  'ameixa':   [(0, '#3d1c46'), (.30, '#5b216c'), (.58, '#7b4df2'), (.80, '#c0a5c4'), (1, '#fffbde')],
  'manteiga': [(0, '#3d1c46'), (.28, '#5b216c'), (.55, '#b0569a'), (.80, '#f2cf7a'), (1, '#fffbde')],
  'violeta':  [(0, '#6225d8'), (.35, '#7b4df2'), (.70, '#c0a5c4'), (1, '#fffbde')],
}
def mapa(g, stops):
    out = np.zeros(g.shape + (3,))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        m = (g >= a) & (g <= b); t = ((g - a) / (b - a))[m][:, None]
        out[m] = H(ca) * (1 - t) + H(cb) * t
    return out.astype('uint8')
for fase, tema in [a.split(':') for a in sys.argv[1:]]:
    g = np.asarray(Image.open(f'lua/{fase}.jpg').convert('L'), float) / 255
    g = np.clip(g * 1.25, 0, 1) ** .85            # abre os meios-tons
    rgb = mapa(g, TEMAS[tema])
    Image.fromarray(rgb).save(f'lua/{fase}-{tema}.jpg', quality=92)
    alfa = np.clip((g - .10) / .16, 0, 1)          # parte acesa
    a = Image.fromarray((alfa * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.2))
    im = Image.fromarray(rgb).convert('RGBA'); im.putalpha(a); im.save(f'lua/{fase}-{tema}-frente.png')
    print(fase, tema)
