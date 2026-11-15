# Separa os objetos de uma folha de recortes gerada sobre fundo liso #E9E9E9 (só Pillow + numpy).
# uso: python3 recortar.py folhas/gatos.png gatos [tolerancia=11] -> recortes/gatos-1.png ... (ordem de leitura)
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageOps

folha, nome = sys.argv[1], sys.argv[2]
tol = float(sys.argv[3]) if len(sys.argv) > 3 else 11
src = Image.open(folha)
tem_alfa = src.mode == 'RGBA' and np.asarray(src)[..., 3].min() < 250   # folha que já veio sem fundo do Magnific
im = src.convert('RGB')
a = np.asarray(im).astype(np.int16)
H, W = a.shape[:2]
fundo = np.median(np.concatenate([a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3), a[:, :8].reshape(-1, 3), a[:, -8:].reshape(-1, 3)]), axis=0)
parece = (np.abs(a - fundo).max(axis=2) <= tol)
# só é fundo o que está ligado à borda da folha (o claro de dentro do objeto fica)
m = ImageOps.expand(Image.fromarray((parece * 255).astype('uint8')), 1, 255)
ImageDraw.floodfill(m, (0, 0), 128)
obj = Image.fromarray(((np.asarray(m)[1:-1, 1:-1] != 128) * 255).astype('uint8'))
if tem_alfa:
    alfa = np.asarray(src)[..., 3]
    obj = Image.fromarray(((alfa > 40) * 255).astype('uint8')).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5))
else:
    obj = obj.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5))          # tira poeira
    alfa = np.asarray(obj.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2)))  # come 1px da borda: sem halo cinza
resto = obj.copy(); pecas = []
while True:
    r = np.asarray(resto); ys, xs = np.nonzero(r == 255)
    if not len(ys): break
    ImageDraw.floodfill(resto, (int(xs[0]), int(ys[0])), 100)
    peca = np.asarray(resto) == 100
    if not peca.any(): resto.putpixel((int(xs[0]), int(ys[0])), 0); continue
    yy, xx = np.nonzero(peca); y0, y1, x0, x1 = yy.min(), yy.max() + 1, xx.min(), xx.max() + 1
    if (y1 - y0) * (x1 - x0) >= 0.004 * H * W: pecas.append((y0, y1, x0, x1, peca[y0:y1, x0:x1].copy()))
    resto = Image.fromarray(np.where(peca | (np.asarray(resto) == 100), 0, np.asarray(resto)).astype('uint8')).copy()
alt = np.median([p[1] - p[0] for p in pecas])
pecas.sort(key=lambda p: (round(p[0] / (alt * .7)), p[2]))
for k, (y0, y1, x0, x1, peca) in enumerate(pecas, 1):
    rec = im.crop((x0, y0, x1, y1)).convert('RGBA')
    perto = np.asarray(Image.fromarray((peca * 255).astype('uint8')).filter(ImageFilter.MaxFilter(9))) > 0
    rec.putalpha(Image.fromarray(np.where(perto, alfa[y0:y1, x0:x1], 0).astype('uint8')))
    rec.save(f'recortes/{nome}-{k}.png'); print(f'{nome}-{k}.png', rec.size)
