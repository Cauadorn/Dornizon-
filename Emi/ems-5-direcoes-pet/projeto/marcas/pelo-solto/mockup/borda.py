# pelo solto · mockup do bordado na manga (referência Digs): a manga lisa foi gerada (base-manga.png) e o "ps" de verdade
# entra como bordado: preenchimento de pontos na diagonal (linha), relevo pelo campo de distância (luz de cima à esquerda,
# como o sol da foto), sombra curta no tecido, brilho de linha, e a luz e o grão da própria manga por cima.
# uso: borda.py ps-mascara.png mockup-manga-pelo-solto.jpg 555 700 178 -4 '#4E2511'   (a versão enviada)
import sys, numpy as np, cv2
from PIL import Image
mask_p, saida = sys.argv[1], sys.argv[2]
cx, cy, alt, giro = [float(v) for v in (sys.argv[3:7] if len(sys.argv) > 6 else (548, 668, 215, -4))]
cor = sys.argv[7] if len(sys.argv) > 7 else '#5A2E17'
foto = np.asarray(Image.open(sys.argv[8] if len(sys.argv) > 8 else 'base-manga-clara.png').convert('RGB')).astype(np.float32) / 255
H, W = foto.shape[:2]
# máscara do ps (preto no branco), recortada e escalada para 'alt' px × K (supersampling)
K = 4
m = np.asarray(Image.open(mask_p).convert('L')).astype(np.float32) / 255
m = 1 - m; ys, xs = np.where(m > .5); m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
h = int(alt * K); w = int(m.shape[1] * h / m.shape[0])
m = cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA)
pad = 30 * K; mm = np.zeros((h + 2 * pad, w + 2 * pad), np.float32); mm[pad:pad + h, pad:pad + w] = m
Rm = cv2.getRotationMatrix2D((mm.shape[1] / 2, mm.shape[0] / 2), -giro, 1)
mm = cv2.warpAffine(mm, Rm, (mm.shape[1], mm.shape[0]), flags=cv2.INTER_LINEAR)
bin_ = (mm > .5).astype(np.uint8)
# relevo: distância até a borda → altura arredondada (fio estufado)
dt = cv2.distanceTransform(bin_, cv2.DIST_L2, 5)
hgt = np.clip(dt / (3.2 * K), 0, 1); hgt = np.sin(hgt * np.pi / 2) ** .7
hgt = cv2.GaussianBlur(hgt, (0, 0), .6 * K)   # pouco desfoque: o filete entre o p e o s continua aberto
gy, gx = np.gradient(hgt)
luz = np.clip(.5 + (-gx * .9 - gy * 1.1) * 6 * K, 0, 1.4)          # sol de cima à esquerda
# pontos: fios na diagonal (45° + giro), cada fio um pouco diferente; um vinco escuro entre fios
yy, xx = np.mgrid[0:mm.shape[0], 0:mm.shape[1]].astype(np.float32)
ang = np.deg2rad(52 + giro); u = xx * np.cos(ang) + yy * np.sin(ang); v = -xx * np.sin(ang) + yy * np.cos(ang)
per = 1.7 * K   # fios finos e densos, como no bordado da Digs
fio = np.mod(u, per) / per
seg = np.floor(u / per)
rnd = np.random.default_rng(4); jit = rnd.random(int(seg.max()) + 3).astype(np.float32)
quebra = np.mod(v + jit[seg.astype(int) + 1] * 40 * K, 26 * K) / (26 * K)       # fios de comprimento finito (tatami)
perfil = np.sin(fio * np.pi) ** .6                                         # cada fio é cilíndrico
vinco = np.clip(1 - np.abs(quebra - .5) * 0 , 0, 1)
brilho = (perfil ** 8) * .12 * (.5 + .5 * jit[seg.astype(int) + 1])
irreg = cv2.GaussianBlur(rnd.normal(0, 1, perfil.shape).astype(np.float32), (0, 0), .8 * K) * .06   # fio irregular
c = np.array([int(cor[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255
fioCor = c[None, None, :] * (.74 + .26 * perfil[..., None] + irreg[..., None]) * (.78 + .32 * luz[..., None]) + brilho[..., None]
fioCor = np.clip(fioCor, 0, 1)
borda = np.clip(mm, 0, 1)
# sombra curta no tecido (embaixo à direita) e leve franzido em volta
sh = cv2.GaussianBlur(np.roll(np.roll(mm, int(1.6 * K), 0), int(1.2 * K), 1), (0, 0), 1.6 * K) * .5
franz = cv2.GaussianBlur(mm, (0, 0), 6 * K) * .08
# volta para a escala da foto
def red(a): return cv2.resize(a, (a.shape[1] // K, a.shape[0] // K), interpolation=cv2.INTER_AREA)
fioS, bordaS, shS, frS = red(fioCor), red(borda), red(sh), red(franz)
hh, ww = bordaS.shape
x0, y0 = int(cx - ww / 2), int(cy - hh / 2)
reg = foto[y0:y0 + hh, x0:x0 + ww]
lum = reg.mean(2, keepdims=True); ref = np.percentile(lum, 70)
luzFoto = np.clip(lum / ref, .7, 1.2)                                       # a luz da manga (dobras) passa por cima
tecido = reg * (1 - shS[..., None] - frS[..., None])
grao = (lum - cv2.GaussianBlur(lum, (0, 0), 1.0)[..., None]) * .6
fioFinal = np.clip(fioS * luzFoto + grao, 0, 1)
out = foto.copy(); out[y0:y0 + hh, x0:x0 + ww] = tecido * (1 - bordaS[..., None]) + fioFinal * bordaS[..., None]
Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(saida, quality=94)
print('ok', saida, (x0, y0, ww, hh))
