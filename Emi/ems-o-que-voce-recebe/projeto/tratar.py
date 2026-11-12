# Trata os objetos recortados (obj/c*.png: rembg birefnet-general sobre as fotos isoladas de iso/) na paleta da EMS:
# mapa de gradiente pela luminância, alfa preservado, recorte na caixa do objeto e redução para o tamanho de uso.
from PIL import Image, ImageFilter
import numpy as np
H = lambda h: np.array([int(h[i:i+2], 16) for i in (1, 3, 5)], float)
NOITE = [(0, '#2a1433'), (.16, '#3d1c46'), (.40, '#5b216c'), (.60, '#7b4df2'), (.80, '#c0a5c4'), (1, '#fffbde')]
MANT  = [(0, '#2a1433'), (.20, '#3d1c46'), (.44, '#5b216c'), (.62, '#7b4df2'), (.82, '#f2cf7a'), (1, '#fffbde')]
def mapa(g, stops):
    out = np.zeros(g.shape + (3,))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        m = (g >= a) & (g <= b); t = ((g - a) / (b - a))[m][:, None]
        out[m] = H(ca) * (1 - t) + H(cb) * t
    return out.astype('uint8')
# objeto, largura final em px, tema, ganho e gama da luminância
for i, larg, tema, ganho, gama in [(1, 712, NOITE, 1.3, .62), (3, 934, NOITE, 1.06, .9), (4, 1080, NOITE, 1.06, .9), (5, 501, NOITE, 1.06, .9), (6, 854, MANT, .9, .9)]:
    im = Image.open(f'obj/c{i}.png'); box = im.getbbox(); im = im.crop(box)
    a = np.asarray(im.getchannel('A'), float) / 255
    a = np.clip((a - .5) / .35, 0, 1)                       # borda firme, sem auréola do fundo cinza
    g = np.asarray(im.convert('L'), float) / 255
    g = np.clip((g - .05) * ganho, 0, 1) ** gama
    out = Image.fromarray(mapa(g, tema)).convert('RGBA')
    out.putalpha(Image.fromarray((a * 255).astype('uint8')))
    out = out.resize((larg, round(out.height * larg / out.width)), Image.LANCZOS)
    out.save(f'obj/o{i}.png'); print(i, box, out.size)
