# Peixinho dos petiscos MIAU.LAB (a Emi: "deixa as pílulas e os peixinhos, mas melhore esses peixes em alguma IA"):
# peixe gerado no Figma (gpt-image-2.5-sunburst, peixe-ia-1.png) separado em 3 cores (creme, rosa, preto) e vetorizado
# camada a camada (potrace) → peixe.js (const PEIXE = {creme, rosa, preto, w, h}); o rosa vira a cor de destaque de cada pouch.
import json, numpy as np, cv2, potrace
from PIL import Image
im = np.asarray(Image.open('peixe/peixe-ia-1.png').convert('RGB')).astype(np.float32)
alvos = {'creme': (246, 238, 220), 'rosa': (244, 185, 205), 'preto': (28, 26, 36), 'branco': (255, 255, 255)}
nomes = list(alvos); C = np.array([alvos[n] for n in nomes], np.float32)
d = ((im[..., None, :] - C[None, None]) ** 2).sum(-1); cls = d.argmin(-1)
ys, xs = np.nonzero(cls != nomes.index('branco')); x0, x1, y0, y1 = xs.min() - 4, xs.max() + 4, ys.min() - 4, ys.max() + 4
S = 3; out = {'w': int(x1 - x0), 'h': int(y1 - y0)}
for n in ('creme', 'rosa', 'preto'):
    m = (cls == nomes.index(n)).astype(np.float32)[y0:y1, x0:x1]
    if n == 'creme': m = np.maximum(m, (cls != nomes.index('branco')).astype(np.float32)[y0:y1, x0:x1])   # corpo cheio por baixo
    big = cv2.GaussianBlur(cv2.resize(m, (m.shape[1] * S, m.shape[0] * S), interpolation=cv2.INTER_CUBIC), (0, 0), 1.4) > .5
    pl = potrace.Bitmap(~big).trace(turdsize=20, alphamax=1.0, opticurve=True, opttolerance=.2)
    f = lambda p: f'{p.x / S:.1f} {p.y / S:.1f}'
    ds = []
    for c in pl:
        seg = [f'M{f(c.start_point)}'] + [f'L{f(s.c)} L{f(s.end_point)}' if s.is_corner else f'C{f(s.c1)} {f(s.c2)} {f(s.end_point)}' for s in c.segments]
        ds.append(' '.join(seg) + 'Z')
    out[n] = ' '.join(ds)
open('peixe/peixe.js', 'w').write('// gerado por peixe/vetoriza.py\nconst PEIXE = ' + json.dumps(out) + ';\n')
print('ok', out['w'], out['h'], {k: len(v) for k, v in out.items() if isinstance(v, str)})
