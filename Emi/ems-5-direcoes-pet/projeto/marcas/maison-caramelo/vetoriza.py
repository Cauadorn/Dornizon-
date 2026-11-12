# Maison Caramelo · vetoriza a silhueta gerada (estilo vaso grego: preto chapado com linhas finas vazadas).
# Referências que a Emi escolheu no quadro de brasão: 14 Eros & Co. (bicho pequeno em silhueta + nome em serifa) e
# 15 oval floral em relevo (selo oval de borda recortada, prensado tom sobre tom).
# uso: vetoriza.py <png gerado> <saida.svg>
import sys, numpy as np, cv2, potrace
from PIL import Image
im = np.asarray(Image.open(sys.argv[1]).convert('L')).astype(np.float32) / 255
S = 4
big = cv2.GaussianBlur(cv2.resize(im, (im.shape[1] * S, im.shape[0] * S), interpolation=cv2.INTER_CUBIC), (0, 0), 1.2)
m = big < 0.5
n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8))
keep = np.zeros_like(m)
for i in range(1, n):
    if st[i, 4] > 40 * S * S: keep |= lab == i
ys, xs = np.where(keep); keep = keep[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
plist = potrace.Bitmap(~keep).trace(turdsize=12, alphamax=1.0, opticurve=True, opttolerance=0.2)
f = lambda q: f'{q.x / S:.2f} {q.y / S:.2f}'
partes = []
for c in plist:
    d = [f'M{f(c.start_point)}']
    for sg in c.segments:
        d.append(f'L{f(sg.c)} L{f(sg.end_point)}' if sg.is_corner else f'C{f(sg.c1)} {f(sg.c2)} {f(sg.end_point)}')
    partes.append(' '.join(d) + 'Z')
W, H = keep.shape[1] / S, keep.shape[0] / S
open(sys.argv[2], 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} {H:.2f}" width="{W:.2f}" height="{H:.2f}"><path fill-rule="evenodd" fill="#000" d="{" ".join(partes)}"/></svg>')
print('ok', sys.argv[2], len(plist), 'curvas', round(W, 1), round(H, 1))
