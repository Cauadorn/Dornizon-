# Aplica uma arte (PNG) numa superfície de uma foto em perspectiva, mantendo luz e textura da foto.
# uso: aplica.py <foto> <saida> <arte1> "x1,y1 x2,y2 x3,y3 x4,y4" [<arte2> "quad2"] ...
#      cantos em ordem: topo-esq, topo-dir, base-dir, base-esq (em pixels da foto)
# arte "cor:#RRGGBB" pinta a superfície com uma cor chapada.
import sys
import numpy as np, cv2
from PIL import Image, ImageFilter

foto_path, saida = sys.argv[1], sys.argv[2]
pares = sys.argv[3:]
foto = np.asarray(Image.open(foto_path).convert('RGB')).astype(np.float32) / 255
H, W = foto.shape[:2]
gray = cv2.cvtColor((foto * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
out = foto.copy()
SS = 3   # supersampling da máscara para borda limpa
for i in range(0, len(pares), 2):
    arte_src, quad = pares[i], pares[i + 1]
    dst = np.array([[float(v) for v in p.split(',')] for p in quad.split()], np.float32)
    if arte_src.startswith('cor:'):
        h = arte_src[4:].lstrip('#'); cor = np.array([int(h[j:j + 2], 16) for j in (0, 2, 4)], np.float32) / 255
        arte = np.ones((64, 64, 3), np.float32) * cor
    else:
        arte = np.asarray(Image.open(arte_src).convert('RGB')).astype(np.float32) / 255
    ah, aw = arte.shape[:2]
    src = np.array([[0, 0], [aw, 0], [aw, ah], [0, ah]], np.float32)
    Mx = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(arte, Mx, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT)
    # máscara com antialias
    mask_big = np.zeros((H * SS, W * SS), np.uint8)
    cv2.fillPoly(mask_big, [np.round(dst * SS).astype(np.int32)], 255, lineType=cv2.LINE_AA)
    mask = cv2.resize(mask_big, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    mask = cv2.erode(mask, np.ones((2, 2), np.uint8))[..., None]
    # sombreado: luminância da superfície branca normalizada pelo ponto mais claro dela
    # referência de luz: a da PRIMEIRA superfície (a frente); as outras herdam, para a lateral ficar na sombra
    if i == 0:
        sel = gray[mask[..., 0] > .5]
        ref = np.percentile(sel, 97) if sel.size else 1
    sombra = np.clip(gray / ref, 0, 1.05)[..., None]
    # textura fina do papel (alta frequência) volta por cima
    blur = cv2.GaussianBlur(gray, (0, 0), 2.0)
    grao = (gray - blur)[..., None] * 0.8
    pintado = np.clip(warped * sombra + grao, 0, 1)
    out = out * (1 - mask) + pintado * mask
Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(saida, quality=92)
print('ok', saida)
