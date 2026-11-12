# Limpa a silhueta gerada (cao-salto-gerado-2.png): tira os espinhos de pelo solto e suaviza a borda,
# como um traço vetorial redondo. Saída: cao-salto.png (alfa, 2x a resolução original).
import numpy as np, cv2
from PIL import Image
im = np.asarray(Image.open('cao-salto-gerado-2.png').convert('L')).astype(np.float32) / 255
S = 4
big = cv2.resize(im, (im.shape[1] * S, im.shape[0] * S), interpolation=cv2.INTER_CUBIC)
m = (big < 0.5).astype(np.uint8)
m = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (27, 27)))
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
n, lab, st, _ = cv2.connectedComponentsWithStats(m)
keep = np.zeros_like(m)
for i in range(1, n):
    if st[i, 4] > 20000: keep[lab == i] = 1
f = cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 9)
alpha = np.clip((f - 0.5) * 3 + 0.5, 0, 1)
small = cv2.resize(alpha, (im.shape[1] * 2, im.shape[0] * 2), interpolation=cv2.INTER_AREA)
ys, xs = np.where(small > 0.02); y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
small = small[y0 - 8:y1 + 9, x0 - 8:x1 + 9]
rgba = np.zeros(small.shape + (4,), np.uint8); rgba[..., 3] = (small * 255).astype(np.uint8)
Image.fromarray(rgba).save('cao-salto.png'); print(rgba.shape)
