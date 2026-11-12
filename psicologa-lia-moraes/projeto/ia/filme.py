# Tratamento "filme" para as fotos da Lia geradas no Canva (tirar a cara de IA):
# menos laranja, pretos levantados, fundo mais neutro que a pessoa, grão de filme.
# uso: python3 -I ia/filme.py <foto> <recorte-com-alpha> <saida> [sat_fundo] [sat_pessoa]
import sys, numpy as np
from PIL import Image, ImageFilter
src, rec, dst = sys.argv[1:4]
sf = float(sys.argv[4]) if len(sys.argv) > 4 else .55
sp = float(sys.argv[5]) if len(sys.argv) > 5 else .82
im = np.asarray(Image.open(src).convert('RGB')).astype(np.float32) / 255
a = np.asarray(Image.open(rec).getchannel('A').filter(ImageFilter.GaussianBlur(6))).astype(np.float32)[..., None] / 255
lum = (im * [.299, .587, .114]).sum(-1, keepdims=True)
sat = sf + (sp - sf) * a
im = lum + (im - lum) * sat
# puxa o laranja para um bege mais neutro (menos vermelho, um pouco de verde nas sombras)
im[..., 0] = im[..., 0] ** 1.05
im[..., 1] = im[..., 1] ** 0.99
im[..., 2] = im[..., 2] ** 0.93
sh = (1 - lum) ** 2
im += sh * np.array([-.012, .008, .02])
# curva suave em S + pretos levantados (filme)
im = np.clip(im, 0, 1)
im = im + .10 * np.sin((im - .5) * np.pi) * (im * (1 - im)) * 2
im = .045 + im * .93
# vinheta leve
h, w = im.shape[:2]
y, x = np.mgrid[0:h, 0:w]
d = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h * .45) / (h / 2)) ** 2)
im *= (1 - .10 * np.clip(d - .55, 0, 1) ** 1.5)[..., None]
# grão: ruído de luminância, levemente borrado, mais forte nos meios-tons
rng = np.random.default_rng(7)
n = rng.normal(0, 1, (h, w)).astype(np.float32)
n = np.asarray(Image.fromarray(((n * 40) + 128).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.7))).astype(np.float32) / 255 - .5
lm = (im * [.299, .587, .114]).sum(-1)
im += (n * .085 * (.45 + 1.6 * lm * (1 - lm)))[..., None]
Image.fromarray((np.clip(im, 0, 1) * 255).astype(np.uint8)).save(dst, quality=94)
print('ok', dst)
