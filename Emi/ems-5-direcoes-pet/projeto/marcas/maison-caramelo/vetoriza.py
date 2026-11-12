# Maison Caramelo · vetoriza o emblema gerado (gerados/3-relevo-simples.png: vira-lata caramelo de perfil no medalhão oval,
# a partir da referência 3 que a Emi escolheu, o galgo em relevo no vinho). Amplia 4x, alisa, limiar e potrace → emblema.svg.
import numpy as np, cv2, potrace
from PIL import Image
im = np.asarray(Image.open('gerados/3-relevo-simples.png').convert('L')).astype(np.float32) / 255
S = 4
big = cv2.GaussianBlur(cv2.resize(im, (im.shape[1] * S, im.shape[0] * S), interpolation=cv2.INTER_CUBIC), (0, 0), 1.4)
m = big < 0.5
n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8))
keep = np.zeros_like(m)
for i in range(1, n):
    if st[i, 4] > 60 * S * S: keep |= lab == i
ys, xs = np.where(keep); y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
keep = keep[y0:y1 + 1, x0:x1 + 1]
plist = potrace.Bitmap(~keep).trace(turdsize=20, alphamax=1.1, opticurve=True, opttolerance=0.2)
f = lambda q: f'{q.x / S:.2f} {q.y / S:.2f}'
partes = []
for c in plist:
    d = [f'M{f(c.start_point)}']
    for sg in c.segments:
        d.append(f'L{f(sg.c)} L{f(sg.end_point)}' if sg.is_corner else f'C{f(sg.c1)} {f(sg.c2)} {f(sg.end_point)}')
    partes.append(' '.join(d) + 'Z')
W, H = keep.shape[1] / S, keep.shape[0] / S
open('emblema.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} {H:.2f}" width="{W:.2f}" height="{H:.2f}"><path fill-rule="evenodd" fill="#000" d="{" ".join(partes)}"/></svg>')
print('ok', len(plist), 'curvas', round(W, 2), round(H, 2))
