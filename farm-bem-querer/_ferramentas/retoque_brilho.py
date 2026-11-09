"""Troca brilhos em forma de coração (desenhados nas frutas) por brilhos redondos pintados.
Uso: python retoque_brilho.py entrada.png saida.png y,x y,x ..."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import os
LIM = float(os.environ.get("LIM", 115))
ent, sai = sys.argv[1], sys.argv[2]
pts = [tuple(int(v) for v in p.split(',')) for p in sys.argv[3:]]
im = np.asarray(Image.open(ent).convert('RGB'), np.float32)
out = im.copy()
rng = np.random.default_rng(7)
for (y, x) in pts:
    R = 34
    win = out[y - R:y + R, x - R:x + R].copy()
    L = win.mean(2)
    hl = (L > LIM) & (win[..., 0] > win[..., 2])
    # mantém só o componente ligado ao centro
    lab = np.zeros(hl.shape, bool); st = []
    cy, cx = np.unravel_index(np.argmax(hl * (1 / (1 + (np.indices(hl.shape)[0] - R) ** 2 + (np.indices(hl.shape)[1] - R) ** 2))), hl.shape)
    st.append((cy, cx)); lab[cy, cx] = True
    while st:
        a, b = st.pop()
        for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            aa, bb = a + da, b + db
            if 0 <= aa < 2 * R and 0 <= bb < 2 * R and hl[aa, bb] and not lab[aa, bb]:
                lab[aa, bb] = True; st.append((aa, bb))
    ys, xs = np.where(lab)
    if len(ys) < 20:
        continue
    hc = win[lab].mean(0)
    my, mx = ys.mean(), xs.mean()
    h, w = ys.max() - ys.min() + 1, xs.max() - xs.min() + 1
    m = np.asarray(Image.fromarray((lab * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.2)), np.float32)[..., None] / 255
    # textura da própria fruta logo abaixo do brilho (clone)
    dy = int(h * 0.9) + 4
    fonte = out[y - R + dy:y + R + dy, x - R:x + R]
    base = win * (1 - m) + fonte * m
    # brilho novo: mancha oval irregular, como pincelada de guache
    S = 4
    N = 2 * R * S
    yy_, xx_ = np.mgrid[0:N, 0:N] / S
    ang = np.deg2rad(rng.uniform(-28, -12))
    rx, ry = xx_ - mx, yy_ - (my - h * 0.06)
    u = rx * np.cos(ang) + ry * np.sin(ang)
    v = -rx * np.sin(ang) + ry * np.cos(ang)
    rw, rh = w * 0.36, h * 0.24
    dist = (u / rw) ** 2 + (v / rh) ** 2
    ruido = np.asarray(Image.fromarray((rng.random((N // 6 + 1, N // 6 + 1)) * 255).astype(np.uint8)).resize((N, N), Image.BICUBIC), np.float32) / 255 - 0.5
    forma = np.clip((1.0 - (dist + 0.55 * ruido)) * 6, 0, 1)
    nm = np.asarray(Image.fromarray((forma * 255).astype(np.uint8)).resize((2 * R, 2 * R), Image.LANCZOS), np.float32)[..., None] / 255 * 0.93
    tex = 1 + rng.normal(0, 0.03, (2 * R, 2 * R, 1))
    novo = base * (1 - nm) + (hc * tex) * nm
    out[y - R:y + R, x - R:x + R] = novo
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(sai)
print('ok', len(pts))
