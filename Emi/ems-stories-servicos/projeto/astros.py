# Trata fotos de astros (NASA, domínio público) na paleta da EMS para as capas de destaque:
# recorta em quadrado em volta do astro, mapa de gradiente ameixa -> plum -> rosa queimado -> manteiga -> marfim.
from PIL import Image, ImageOps
import numpy as np
H = lambda h: np.array([int(h[i:i+2], 16) for i in (1, 3, 5)], float)
STOPS = [(0, '#3d1c46'), (.28, '#5b216c'), (.55, '#b0569a'), (.80, '#f2cf7a'), (1, '#fffbde')]
def mapa(g):
    out = np.zeros(g.shape + (3,))
    for (a, ca), (b, cb) in zip(STOPS, STOPS[1:]):
        m = (g >= a) & (g <= b); t = ((g - a) / (b - a))[m][:, None]
        out[m] = H(ca) * (1 - t) + H(cb) * t
    return out.astype('uint8')
# nome: (limiar do fundo, ocupação do astro no quadrado, gama)
for nome, (lim, ocup, gama) in {'terra': (22, .86, .8), 'sol': (60, .8, 1.25), 'saturno': (14, .9, .75), 'jupiter': (22, .86, .9)}.items():
    im = Image.open(f'astro/{nome}-orig.jpg').convert('L'); im.thumbnail((3000, 3000))
    a = np.asarray(im)
    ys, xs = np.where(a > lim)
    x0, x1, y0, y1 = np.percentile(xs, .2), np.percentile(xs, 99.8), np.percentile(ys, .2), np.percentile(ys, 99.8)
    cx, cy, lado = (x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, y1 - y0) / ocup
    q = Image.new('L', (int(lado), int(lado)), 0)
    q.paste(im, (int(lado / 2 - cx), int(lado / 2 - cy)))
    q = ImageOps.autocontrast(q.resize((1400, 1400), Image.LANCZOS), cutoff=(0, .5))
    g = (np.asarray(q, float) / 255) ** gama
    if nome != 'sol': g[g < lim / 255 * .6] = 0   # limpa o ruído do céu; no sol a coroa fica
    Image.fromarray(mapa(g)).save(f'astro/{nome}.jpg', quality=92); print(nome, int(lado))
