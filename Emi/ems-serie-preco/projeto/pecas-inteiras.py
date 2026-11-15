# Recorta as peças geradas sozinhas (o "A" e as quatro amostras) para caírem inteiras.
import sys, numpy as np, cv2
from PIL import Image
from rembg import remove, new_session
d = sys.argv[1]; s = new_session('isnet-general-use')
def rec(nome):
    a = np.array(remove(Image.open(f'{d}/{nome}.png').convert('RGB'), session=s)); al = a[..., 3].astype(float)
    a[..., 3] = (np.clip((al - 40) / 175, 0, 1) * 255).astype('uint8'); return a
for nome in ['A', 'a-min', 'balanca', 'estrela']:
    A = rec(nome); ys, xs = np.where(A[..., 3] > 20); Image.fromarray(A[ys.min():ys.max() + 1, xs.min():xs.max() + 1]).save(f'{d}/{nome}-rec.png')
am = rec('amostras'); n, lab, st, cen = cv2.connectedComponentsWithStats((am[..., 3] > 60).astype(np.uint8))
ids = sorted([i for i in range(1, n) if st[i, 4] > 5000], key=lambda i: st[i, 0])
for k, i in enumerate(ids[:4]):
    x, y, w, h = st[i, :4]; c = am[y:y + h, x:x + w].copy(); c[..., 3] = np.where(lab[y:y + h, x:x + w] == i, c[..., 3], 0)
    Image.fromarray(c).save(f'{d}/amostra{k + 1}-rec.png'); print('amostra', k + 1, w, h)
print('A', A.shape, len(ids))
