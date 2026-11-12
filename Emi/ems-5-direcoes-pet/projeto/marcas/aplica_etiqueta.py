# Aplica uma arte numa etiqueta de papel em branco enrolada num frasco cilíndrico da foto.
# uso: aplica_etiqueta.py <foto> <saida> <arte> "cx,r,xmin,xmax" "e,b,s(topo)" "e,b,s(base)" [<arte2> ...]
#   cx, r = eixo e raio do frasco na foto; xmin..xmax = trecho visível da etiqueta (corta onde outro frasco passa na frente).
#   topo/base: a borda da etiqueta medida na foto e ajustada como arco de elipse com inclinação:
#   y(x) = e + b*sqrt(1 - t^2) + s*t, com t = (x - cx) / r. Assim o rótulo acompanha a curva de verdade, sem ficar torto.
# A arte é a meia volta da frente (de borda a borda): u = asin(t)/pi + 0.5, v = (y - topo) / (base - topo).
# Herda a luz do papel (em linear) e o grão da foto.
import sys
import numpy as np, cv2
from PIL import Image

foto_p, saida = sys.argv[1], sys.argv[2]
foto = np.asarray(Image.open(foto_p).convert('RGB')).astype(np.float32) / 255
H, W = foto.shape[:2]
lum = foto.mean(2)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
def lin(c): return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def srgb(l): return np.where(l <= 0.0031308, l * 12.92, 1.055 * np.clip(l, 0, None) ** (1 / 2.4) - 0.055)
out = foto.copy()
args = sys.argv[3:]
for i in range(0, len(args), 4):
    arte = np.asarray(Image.open(args[i]).convert('RGB')).astype(np.float32) / 255
    cx, r, xmin, xmax = [float(v) for v in args[i + 1].split(',')]
    pt = [float(v) for v in args[i + 2].split(',')]; pb = [float(v) for v in args[i + 3].split(',')]
    t = np.clip((xx - cx) / r, -0.9995, 0.9995); c = np.sqrt(1 - t * t)
    topo = pt[0] + pt[1] * c + pt[2] * t; base = pb[0] + pb[1] * c + pb[2] * t
    m = np.clip(np.minimum(yy - topo, base - yy) + 0.5, 0, 1) * np.clip(np.minimum(xx - xmin, xmax - xx) + 0.5, 0, 1)
    ah, aw = arte.shape[:2]
    u = ((np.arcsin(t) / np.pi + 0.5) * (aw - 1)).astype(np.float32)
    v = ((yy - topo) / (base - topo) * (ah - 1)).astype(np.float32)
    a = cv2.remap(arte, u, v, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    sel = m > 0.9
    ref = np.percentile(lum[sel], 98)
    luz = np.clip(lum / ref, 0, 1.0)[..., None] ** 2.2
    grao = (lum - cv2.GaussianBlur(lum, (0, 0), 1.2))[..., None] * 0.6
    pintado = np.clip(srgb(lin(a) * luz) + grao, 0, 1)
    out = out * (1 - m[..., None]) + pintado * m[..., None]
Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(saida, quality=93)
print('ok', saida)
