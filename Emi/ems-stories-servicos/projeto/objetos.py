# Objetos já aprovados no carrossel "figurinhas raras" (pacotinho, lupa, presente, pincel),
# tratados na mesma cor da capa da lua: mapa de gradiente plum -> rosa queimado -> manteiga -> marfim, mantendo o recorte.
from PIL import Image
import numpy as np
H = lambda h: np.array([int(h[i:i+2], 16) for i in (1, 3, 5)], float)
STOPS = [(0, '#4a1d58'), (.25, '#6d2c80'), (.5, '#b0569a'), (.78, '#f2cf7a'), (1, '#fffbde')]
for nome in ['pacotinho', 'lupa-3d', 'presente', 'pincel']:
    im = Image.open(f'objetos/{nome}.png').convert('RGBA')
    a = np.asarray(im, float); alfa = a[..., 3] / 255
    g = (a[..., 0] * .299 + a[..., 1] * .587 + a[..., 2] * .114) / 255
    lo, hi = np.percentile(g[alfa > .5], [1, 99]); g = np.clip((g - lo) / (hi - lo), 0, 1) ** .9
    out = np.zeros(g.shape + (4,))
    for (x0, c0), (x1, c1) in zip(STOPS, STOPS[1:]):
        m = (g >= x0) & (g <= x1); t = ((g - x0) / (x1 - x0))[m][:, None]
        out[m, :3] = H(c0) * (1 - t) + H(c1) * t
    out[..., 3] = a[..., 3]
    Image.fromarray(out.astype('uint8'), 'RGBA').save(f'objetos/{nome}-manteiga.png'); print(nome, im.size)
