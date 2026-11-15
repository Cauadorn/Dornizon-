# MIAU.LAB · site v2: recortes das fotos por chave de cor (fundos lisos), sem IA de remoção de fundo.
#   gato.png      gato preto da panorâmica (fundo amarelo: pixel escuro)
#   mao-pouch.png mão + pouch Pelo & Pele (fundo amarelo: distância de cor em Lab, sombras amarelas fora)
#   petisco-N.png peixinhos que caem na foto do pouch (componentes pequenos)
#   caixa.png     caixa Mobilidade + cartela (fundo rosa: matiz rosa fora)
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
F = '../post/fotos/'
def lab(a):
    c = np.where(a > 0.04045, ((a + 0.055) / 1.055) ** 2.4, a / 12.92)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    x = c @ M.T; x /= np.array([0.95047, 1, 1.08883]); f = np.where(x > 0.008856, np.cbrt(x), 7.787 * x + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)
def salva(im, m, nome, borda=1.2, larg=None):
    alfa = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(borda)); o = im.copy(); o.putalpha(alfa)
    ys, xs = np.where(m); o = o.crop((max(0, xs.min() - 6), max(0, ys.min() - 6), xs.max() + 6, ys.max() + 6))
    if larg and o.width > larg: o = o.resize((larg, int(o.height * larg / o.width)), Image.LANCZOS)
    o.save('img/' + nome, optimize=True); print(nome, o.size)
def maior(m, minimo=0):
    l, n = ndimage.label(m); t = ndimage.sum(m, l, range(1, n + 1)); return l, t
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
# gato preto
im = Image.open(F + 'v2-l56-panoramica.png').convert('RGB'); a = np.asarray(im).astype(float)
m = a.mean(2) < 95; m = ndimage.binary_closing(m, iterations=3); m = ndimage.binary_fill_holes(m); m = ndimage.binary_opening(m, iterations=2)
l, t = maior(m); m = l == 1 + int(np.argmax(t)); salva(im, m, 'gato.png', 1.4, 1400)
# mão + pouch e petiscos (fundo amarelo)
im = Image.open(F + 'v2-l3-edicao-b.png').convert('RGB'); L = lab(np.asarray(im).astype(float) / 255)
bg = np.median(np.concatenate([L[:20].reshape(-1, 3), L[:, :20].reshape(-1, 3), L[-20:].reshape(-1, 3)]), 0)
hb = np.degrees(np.arctan2(bg[2], bg[1])); h = np.degrees(np.arctan2(L[..., 2], L[..., 1])); C = np.hypot(L[..., 1], L[..., 2])
d = np.hypot(L[..., 1] - bg[1], L[..., 2] - bg[2]); amarelo = (np.abs(h - hb) < 9) & (C > 22) & (L[..., 0] > 45)
m = ((d > 14) | (L[..., 0] < 45)) & ~amarelo; m = ndimage.binary_opening(m, iterations=2); m = ndimage.binary_fill_holes(m)
l, t = maior(m); principal = l == 1 + int(np.argmax(t)); salva(im, principal, 'mao-pouch.png', 1.2, 1100)
k = 0
for i, tam in enumerate(t):
    if 2500 < tam < 60000 and i + 1 != 1 + int(np.argmax(t)):
        mm = ndimage.binary_dilation(l == i + 1, iterations=1); k += 1; salva(im, mm, f'petisco-{k}.png', 1.0, 260)
# caixa (fundo rosa)
im = Image.open(F + 'v2-l7-caixa.png').convert('RGB'); L = lab(np.asarray(im).astype(float) / 255)
bg = np.median(np.concatenate([L[:20].reshape(-1, 3), L[:, :20].reshape(-1, 3)]), 0); print('rosa', bg.round(1))
d = np.hypot(L[..., 1] - bg[1], L[..., 2] - bg[2]); h = np.degrees(np.arctan2(L[..., 2], L[..., 1])); hb = np.degrees(np.arctan2(bg[2], bg[1]))
C = np.hypot(L[..., 1], L[..., 2]); rosa = (np.abs(h - hb) < 14) & (C > 10) & (L[..., 0] > 50)
m = ((d > 12) | (L[..., 0] < 40)) & ~rosa; m = ndimage.binary_opening(m, iterations=2); m = ndimage.binary_fill_holes(m)
l, t = maior(m); m = np.isin(l, 1 + np.where(t > 6000)[0]); salva(im, m, 'caixa.png', 1.2, 1000)
