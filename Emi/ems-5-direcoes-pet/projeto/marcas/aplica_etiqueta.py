# Aplica uma arte numa etiqueta de papel em branco enrolada num frasco cilíndrico da foto.
# uso: aplica_etiqueta.py <foto> <saida> <arte> "cx,r,xmin,xmax" "e,b,s(topo)" "e,b,s(base)" [<arte2> ...]
#   cx, r = eixo e raio do frasco na foto; xmin..xmax = trecho visível da etiqueta (corta onde outro frasco passa na frente);
#   um 5º número opcional gira o rótulo no frasco (fração de meia volta; positivo leva a arte para a esquerda),
#   para o logo não ficar escondido atrás do frasco da frente.
#   topo/base: a borda da etiqueta medida na foto e ajustada como arco de elipse com inclinação:
#   y(x) = e + b*sqrt(1 - t^2) + s*t, com t = (x - cx) / r. Assim o rótulo acompanha a curva de verdade, sem ficar torto.
# A arte é a meia volta da frente (de borda a borda): u = asin(t)/pi + 0.5, v = (y - topo) / (base - topo).
# Lições da 1ª tentativa (a Emi: "extremamente mal aplicado"):
#   - supersampling (S x S por pixel, só na caixa da etiqueta): sem isso a arte reduzida fica serrilhada;
#   - a máscara passa ~1 px da borda medida: senão sobra um filete branco do papel original (cara de adesivo).
# Herda a luz do papel (em linear) e o grão da foto.
import sys
import numpy as np, cv2
from PIL import Image

S, FOLGA_Y, FOLGA_X = 4, 1.3, 0.9
foto_p, saida = sys.argv[1], sys.argv[2]
foto = np.asarray(Image.open(foto_p).convert('RGB')).astype(np.float32) / 255
H, W = foto.shape[:2]
lum1 = foto.mean(2)
def lin(c): return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def srgb(l): return np.where(l <= 0.0031308, l * 12.92, 1.055 * np.clip(l, 0, None) ** (1 / 2.4) - 0.055)
out = foto.copy()
args = sys.argv[3:]
for i in range(0, len(args), 4):
    arte = np.asarray(Image.open(args[i]).convert('RGB')).astype(np.float32) / 255
    g = [float(v) for v in args[i + 1].split(',')]
    cx, r, xmin, xmax = g[:4]; giro = g[4] if len(g) > 4 else 0.0
    pt = [float(v) for v in args[i + 2].split(',')]; pb = [float(v) for v in args[i + 3].split(',')]
    # caixa da etiqueta (em pixels da foto), com margem
    X0, X1 = int(xmin) - 3, int(xmax) + 4
    Y0 = int(pt[0] + min(0, pt[2]) - abs(pt[2]) - 4); Y1 = int(pb[0] + pb[1] + abs(pb[2]) + 5)
    bw, bh = X1 - X0, Y1 - Y0
    # grade fina: centro de cada sub-pixel em coordenadas da foto
    ys, xs = np.mgrid[0:bh * S, 0:bw * S].astype(np.float32)
    xx = X0 + (xs + 0.5) / S - 0.5; yy = Y0 + (ys + 0.5) / S - 0.5
    t = np.clip((xx - cx) / r, -0.9995, 0.9995); c = np.sqrt(1 - t * t)
    topo = pt[0] + pt[1] * c + pt[2] * t - FOLGA_Y; base = pb[0] + pb[1] * c + pb[2] * t + FOLGA_Y
    m = ((yy >= topo) & (yy <= base) & (xx >= xmin - FOLGA_X) & (xx <= xmax + FOLGA_X)).astype(np.float32)
    ah, aw = arte.shape[:2]
    u = (np.clip(np.arcsin(t) / np.pi + 0.5 + giro, 0, 1) * (aw - 1)).astype(np.float32)
    v = (np.clip((yy - topo) / (base - topo), 0, 1) * (ah - 1)).astype(np.float32)
    a = cv2.remap(arte, u, v, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    # luz do papel: a luminância da foto ampliada (suave), relativa ao branco do papel
    caixa = foto[Y0:Y1, X0:X1]
    lumc = cv2.resize(caixa.mean(2), (bw * S, bh * S), interpolation=cv2.INTER_CUBIC)
    sel = lum1[Y0:Y1, X0:X1][cv2.resize(m, (bw, bh), interpolation=cv2.INTER_AREA) > 0.95]
    ref = np.percentile(sel, 98)
    luz = np.clip(lumc / ref, 0, 1.0)[..., None] ** 2.2
    pintado = srgb(lin(a) * luz)
    # volta para a resolução da foto (média dos sub-pixels = antisserrilhado) e compõe
    pm = cv2.resize(pintado * m[..., None], (bw, bh), interpolation=cv2.INTER_AREA)
    mm = cv2.resize(m, (bw, bh), interpolation=cv2.INTER_AREA)[..., None]
    lumb = lum1[Y0:Y1, X0:X1]
    grao = (lumb - cv2.GaussianBlur(lumb, (0, 0), 1.2))[..., None] * 0.6 * mm
    out[Y0:Y1, X0:X1] = out[Y0:Y1, X0:X1] * (1 - mm) + pm + grao
Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(saida, quality=94)
print('ok', saida)
