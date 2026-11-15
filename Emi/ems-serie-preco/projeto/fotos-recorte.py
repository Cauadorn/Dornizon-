# Recorta as fotos de fruta (fundo #E9E9E9) para entrarem por cima do papel e da letra nas lâminas.
import sys, numpy as np, cv2
from PIL import Image
from rembg import remove, new_session
d = sys.argv[1]; s = new_session('isnet-general-use')
def rec(nome):
    a = np.array(remove(Image.open(f'{d}/{nome}.png').convert('RGB'), session=s)); al = a[..., 3].astype(float)
    a[..., 3] = (np.clip((al - 60) / 150, 0, 1) * 255).astype('uint8'); return a
p = rec('prato'); ys, xs = np.where(p[..., 3] > 20); Image.fromarray(p[ys.min():ys.max() + 1, xs.min():xs.max() + 1]).save(f'{d}/prato-rec.png')
f = rec('frutas'); n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate((f[..., 3] > 60).astype(np.uint8), np.ones((25, 25), np.uint8)))
ids = sorted([i for i in range(1, n) if st[i, 4] > 20000], key=lambda i: st[i, 0])
for nome, i in zip(['ameixas', 'uvas', 'pitaya'], ids):
    x, y, w, h = st[i, :4]; c = f[y:y + h, x:x + w].copy(); c[..., 3] = np.where(lab[y:y + h, x:x + w] == i, c[..., 3], 0)
    ys, xs = np.where(c[..., 3] > 20); Image.fromarray(c[ys.min():ys.max() + 1, xs.min():xs.max() + 1]).save(f'{d}/{nome}-rec.png'); print(nome, c.shape)

# prato vazio, garfo e faca (foto de cima, fundo roxo escuro)
m = rec('mesa'); n, lab, st, _ = cv2.connectedComponentsWithStats((m[..., 3] > 60).astype(np.uint8))
ids = sorted([i for i in range(1, n) if st[i, 4] > 6000], key=lambda i: st[i, 0])
for nome, i in zip(['garfo', 'prato-vazio', 'faca'], ids):
    x, y, w, h = st[i, :4]; c = m[y:y + h, x:x + w].copy(); c[..., 3] = np.where(lab[y:y + h, x:x + w] == i, c[..., 3], 0)
    Image.fromarray(c).save(f'{d}/{nome}-rec.png'); print(nome, c.shape)
