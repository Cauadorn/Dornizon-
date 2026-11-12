# Enrola um rótulo (arte = meia volta do pote, de borda a borda) num pote cilíndrico da foto.
# uso: aplica_cilindro.py <foto> <saida> <arte> "x0,x1,y0,y1" [<arte2> "x0,x1,y0,y1"] ...
#      x0,x1 = bordas do corpo do pote (silhueta); y0,y1 = topo e base do rótulo.
# A arte é amostrada por theta = asin((x - centro) / raio): comprime nas laterais como um rótulo de verdade,
# e herda a luz (sombra lateral, brilho) e o grão da foto.
import sys
import numpy as np, cv2
from PIL import Image

foto_p, saida = sys.argv[1], sys.argv[2]
foto = np.asarray(Image.open(foto_p).convert('RGB')).astype(np.float32) / 255
H, W = foto.shape[:2]
gray = cv2.cvtColor((foto * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
out = foto.copy()
args = sys.argv[3:]
for i in range(0, len(args), 2):
    arte = np.asarray(Image.open(args[i]).convert('RGB')).astype(np.float32) / 255
    x0, x1, y0, y1 = [float(v) for v in args[i + 1].split(',')]
    ah, aw = arte.shape[:2]
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    t = np.clip((xs - cx) / r, -0.999, 0.999)
    u = (np.arcsin(t) / np.pi + 0.5) * (aw - 1)
    v = (ys - y0) / (y1 - y0) * (ah - 1)
    amostra = cv2.remap(arte, u, v, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # máscara: faixa do rótulo, com borda suave de 1px em cima/embaixo e nas laterais
    m = np.clip(np.minimum(ys - y0, y1 - ys) + .5, 0, 1) * np.clip(np.minimum(xs - x0, x1 - xs) + .5, 0, 1)
    m = m[..., None]
    sel = gray[(m[..., 0] > .5)]
    ref = np.percentile(sel, 96)
    sombra = np.clip(gray / ref, 0, 1.04)[..., None]
    grao = (gray - cv2.GaussianBlur(gray, (0, 0), 1.4))[..., None] * 0.6
    # papel do rótulo: leve brilho especular da foto passa por cima (mantém o "plástico" do pote)
    brilho = np.clip((gray - ref * 0.98) * 3, 0, 0.18)[..., None]
    pintado = np.clip(amostra * sombra + grao + brilho, 0, 1)
    out = out * (1 - m) + pintado * m
Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(saida, quality=92)
print('ok', saida)
