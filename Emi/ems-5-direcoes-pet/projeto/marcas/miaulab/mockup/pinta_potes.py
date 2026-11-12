# Mockup MIAU.LAB: pinta os dois potes brancos da foto (base-potes.png) inteiros na cor da marca (tampa e corpo)
# e enrola a arte do rótulo no corpo, seguindo a curva do pote.
# A versão anterior ficou "torta" porque o rótulo tinha borda reta e a boca do pote é curva. Aqui cada pixel do pote
# vira (ângulo, altura) no cilindro: a altura desconta a curva da elipse, b(h) = K * (h - H0), que cresce para baixo
# porque a câmera está na altura da tampa de cima (medido nas frestas: 455 reta, 699 com ~8 px de curva, 748 com ~9).
# uso: pinta_potes.py <saida.jpg> <arte-pote-de-cima.png> <cor-de-cima> <arte-pote-de-baixo.png> <cor-de-baixo>
import sys
import numpy as np, cv2
from PIL import Image

saida, arte1, cor1, arte2, cor2 = sys.argv[1:6]
foto = np.asarray(Image.open('base-potes.png').convert('RGB')).astype(np.float32) / 255
H, W = foto.shape[:2]
lum = foto.mean(2)
K, H0 = 0.028, 455.0

# silhueta: borda direita medida linha a linha (a esquerda tem o focinho do gato e a sombra da base), espelhada no eixo CX.
# As linhas de cima (408-420) e de baixo (975-986) estreitam: são os cantos arredondados da tampa e da base.
CX = 659.5
borda_dir = {408: 716, 409: 736, 410: 752, 411: 759, 412: 763, 413: 765, 414: 767, 416: 769, 419: 770, 450: 771, 480: 772,
             660: 772, 675: 771, 682: 768, 690: 761, 696: 762, 700: 769, 705: 770, 760: 771, 960: 770, 968: 765, 975: 753,
             977: 747, 979: 743, 980: 740, 981: 734, 983: 718, 985: 694, 986: 672}
ys = sorted(borda_dir)
meia = np.interp(np.arange(H), ys, [borda_dir[y] + 0.5 - CX for y in ys], left=-1, right=-1)

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
cob = np.clip(meia[yy.astype(int)] - np.abs(xx - CX) + 0.5, 0, 1)
# o focinho do gato só encosta na borda esquerda (termina em x=546): nada a proteger dentro do pote

# coordenadas no cilindro
r = 112.5
t = np.clip((xx - CX) / r, -0.999, 0.999)
c = np.sqrt(1 - t * t)
h = (yy + H0 * K * c) / (1 + K * c)          # altura na borda (sem a curva da elipse)
u = np.arcsin(t) / np.pi + 0.5               # 0..1 na meia volta da frente

def lin(rgb): return np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
def srgb(l): return np.where(l <= 0.0031308, l * 12.92, 1.055 * np.clip(l, 0, None) ** (1 / 2.4) - 0.055)
def hexrgb(hx): return np.array([int(hx[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255

sel = cob > 0.9
ref = np.percentile(lum[sel], 97)
sombra = np.clip(lum / ref, 0, 1.0) ** 2.2                   # luz da foto em linear
brilho = np.clip((lum - ref * 0.985) * 4, 0, 0.12)[..., None]  # o pouco de brilho do plástico
grao = (lum - cv2.GaussianBlur(lum, (0, 0), 1.3))[..., None] * 0.5

def arte_em(arq, h0, h1):
    a = np.asarray(Image.open(arq).convert('RGB')).astype(np.float32) / 255
    ah, aw = a.shape[:2]
    mu = (u * (aw - 1)).astype(np.float32); mv = ((h - h0) / (h1 - h0) * (ah - 1)).astype(np.float32)
    return cv2.remap(a, mu, mv, cv2.INTER_AREA if False else cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

base_cor = np.zeros_like(foto)
# pote de cima: tampa h<455, corpo 455..691.5 · pote de baixo: tampa 691.5..740, corpo 740..
c1, c2 = hexrgb(cor1), hexrgb(cor2)
tampa1 = h < 455; corpo1 = (h >= 455) & (h < 691.5); tampa2 = (h >= 691.5) & (h < 740); corpo2 = h >= 740
base_cor[tampa1] = c1; base_cor[tampa2] = c2
a1 = arte_em(arte1, 455, 691.5); a2 = arte_em(arte2, 740, 972)
base_cor[corpo1] = a1[corpo1]; base_cor[corpo2] = a2[corpo2]

pintado = srgb(lin(base_cor) * sombra[..., None]) + brilho + grao
pintado = np.clip(pintado, 0, 1)
m = cob[..., None]
out = foto * (1 - m) + pintado * m
Image.fromarray((out * 255).astype(np.uint8)).save(saida, quality=93)
print('ok', saida, 'ref', round(float(ref), 3))
