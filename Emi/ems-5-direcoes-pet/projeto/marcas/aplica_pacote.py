# Aplica a arte num pacote (stand-up pouch) branco da foto, seguindo o contorno real do pacote:
# a máscara sai da própria foto (branco pouco saturado contra o fundo), a arte é deformada pelo quadrilátero
# aproximado do pacote e herda a luz, as dobras e o grão da foto.
# uso: aplica_pacote.py <foto> <arte> <saida> "x1,y1 x2,y2 x3,y3 x4,y4" [y_min y_max [recorte.png]]
import sys
import numpy as np, cv2
from PIL import Image

foto_p, arte_p, saida, quad = sys.argv[1:5]
y_min, y_max = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (0, 10**6)
recorte_p = sys.argv[7] if len(sys.argv) > 7 else None   # PNG RGBA do recorte do pacote (rembg/BiRefNet), mais preciso que a cor
foto = np.asarray(Image.open(foto_p).convert('RGB')).astype(np.float32) / 255
H, W = foto.shape[:2]
hsv = cv2.cvtColor((foto * 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
sat, val = hsv[..., 1] / 255, hsv[..., 2] / 255
if recorte_p:
    alfa = np.asarray(Image.open(recorte_p).convert('RGBA'))[..., 3]
    cand = (alfa > 128).astype(np.uint8)
else:
    cand = ((sat < 0.075) & (val > 0.55)).astype(np.uint8)
cand[:y_min] = 0; cand[y_max:] = 0
cand = cv2.morphologyEx(cand, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(cand)
k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
m = (lab == k).astype(np.uint8) * 255
cont, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
m = np.zeros_like(m); cv2.drawContours(m, cont, -1, 255, -1)          # preenche buracos
m = cv2.erode(m, np.ones((3, 3), np.uint8))
mask = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 0.9)[..., None]

arte = np.asarray(Image.open(arte_p).convert('RGB')).astype(np.float32) / 255
ah, aw = arte.shape[:2]
dst = np.array([[float(v) for v in p.split(',')] for p in quad.split()], np.float32)
Mx = cv2.getPerspectiveTransform(np.array([[0, 0], [aw, 0], [aw, ah], [0, ah]], np.float32), dst)
warped = cv2.warpPerspective(arte, Mx, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
gray = cv2.cvtColor((foto * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
ref = np.percentile(gray[mask[..., 0] > .5], 96)
sombra = np.clip(gray / ref, 0, 1.06)[..., None]
grao = (gray - cv2.GaussianBlur(gray, (0, 0), 1.6))[..., None] * 0.7
pintado = np.clip(warped * sombra + grao, 0, 1)
out = foto * (1 - mask) + pintado * mask
Image.fromarray((out * 255).astype(np.uint8)).save(saida, quality=92)
Image.fromarray((mask[..., 0] * 255).astype(np.uint8)).save(saida.rsplit('.', 1)[0] + '-mascara.png')
print('ok', saida)
