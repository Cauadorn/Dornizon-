# pelo solto · vetoriza a letra aprovada (gerados/1-poodle-bolhas.png, só o nome, sem poodle e sem bolhas).
# 1) recorta o "pelo solto" (sem o BANHO & TOSA, que é recomposto em fonte de verdade no logo.html);
# 2) amplia 4x (cúbico) e alisa de leve antes do limiar, para as curvas saírem contínuas;
# 3) potrace (potracer) → caminhos em curvas de Bézier → nome.svg (viewBox na escala da imagem original).
import numpy as np, cv2, potrace
from PIL import Image
im = np.asarray(Image.open('gerados/1-poodle-bolhas.png').convert('RGB')).astype(np.float32)
x0, y0, x1, y1 = 700, 240, 1345, 800                      # só o nome (o BANHO & TOSA começa em y ~ 825)
c = im[y0:y1, x0:x1]
fundo = np.array([253, 246, 229], np.float32)
tinta = np.array([96, 54, 30], np.float32)
# quanto da tinta marrom tem em cada pixel (0 = fundo, 1 = tinta); as bolhas amarelas viram fundo
d_f = np.linalg.norm(c - fundo, axis=2); d_t = np.linalg.norm(c - tinta, axis=2)
amarelo = (c[..., 0] > 180) & (c[..., 2] < 140) & (c[..., 0] - c[..., 2] > 80)
k = np.clip(d_f / (d_f + d_t + 1e-6), 0, 1); k[amarelo] = 0
S = 4
big = cv2.resize(k, (k.shape[1] * S, k.shape[0] * S), interpolation=cv2.INTER_CUBIC)
big = cv2.GaussianBlur(big, (0, 0), 1.6)
bm = big > 0.5
# tira o que não é letra: componentes pequenos e o resto do poodle que entra pela borda esquerda
n, lab, st, _ = cv2.connectedComponentsWithStats(bm.astype(np.uint8))
keep = np.zeros_like(bm)
for i in range(1, n):
    x, y, w, h, a = st[i]
    if a > 3000 * S and not (x < 60 * S and w < 80 * S): keep |= lab == i
bmp = potrace.Bitmap(~keep)   # o potracer trata True como fundo
plist = bmp.trace(turdsize=40, alphamax=1.15, opticurve=True, opttolerance=0.25)
def fmt(p): return f'{p.x / S:.2f} {p.y / S:.2f}'
partes = []
for curve in plist:
    d = [f'M{fmt(curve.start_point)}']
    for seg in curve.segments:
        if seg.is_corner: d.append(f'L{fmt(seg.c)} L{fmt(seg.end_point)}')
        else: d.append(f'C{fmt(seg.c1)} {fmt(seg.c2)} {fmt(seg.end_point)}')
    partes.append(' '.join(d) + 'Z')
W, H = x1 - x0, y1 - y0
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><path fill-rule="evenodd" fill="#5A2E17" d="{" ".join(partes)}"/></svg>'
open('nome.svg', 'w').write(svg)
ys, xs = np.where(keep); print('ok', len(plist), 'curvas; tinta x', xs.min() / S, xs.max() / S, 'y', ys.min() / S, ys.max() / S)
