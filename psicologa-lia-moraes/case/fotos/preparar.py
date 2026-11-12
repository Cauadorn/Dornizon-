# Capa do case: foto da Emi em 1080x1350, descida 330 px, com a parede estendida para cima (espaço do título),
# sombras puxadas para roxo/magenta (regra de fotografia da EMS) e recorte para a cabeça passar na frente do título.
# uso: python3 -I fotos/preparar.py
import numpy as np, cv2
from PIL import Image
D, W, H = 330, 1080, 1350
im = Image.open('fotos/emi-capa.png').convert('RGB')
s = W / im.width
im = im.resize((W, round(im.height * s)), Image.LANCZOS)
a = np.asarray(im).astype(np.float32)
# parede para cima: média das 30 primeiras linhas por coluna, bem suavizada, com leve escurecimento no alto
topo = cv2.GaussianBlur(a[:30].mean(axis=0, keepdims=True), (0, 0), sigmaX=40, sigmaY=0.1)
ext = np.repeat(topo, D, axis=0)
gr = np.linspace(0.965, 1.0, D)[:, None, None]
ext = ext * gr
rng = np.random.default_rng(3)
ext += rng.normal(0, 2.2, ext.shape[:2])[..., None]
# emenda suave de 24 px
full = np.concatenate([ext, a])[:H]
for k in range(40):
    t = (k / 40) ** 1.5
    full[D + k] = full[D + k] * t + ext[-1] * (1 - t)
full = np.clip(full, 0, 255)
# sombras para roxo/magenta
lum = (full * [.299, .587, .114]).sum(-1, keepdims=True) / 255
sh = (1 - lum) ** 2.2
full = full + sh * np.array([10, -6, 16])
Image.fromarray(np.clip(full, 0, 255).astype(np.uint8)).save('fotos/capa-1080.jpg', quality=95)
print('ok')
