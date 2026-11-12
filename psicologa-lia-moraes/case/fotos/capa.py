# Capa do case (v3): foto da Emi com pouco zoom (largura da lâmina), descida T px com a parede estendida
# para o título; cores naturais (sem tinta roxa). Gera também o recorte para a cabeça passar na frente do título.
# uso: python3 -I fotos/capa.py
import numpy as np, cv2
from PIL import Image
W, H, T = 1080, 1350, 250
im = Image.open('fotos/emi-capa.png').convert('RGB')
s = W / im.width
a = np.asarray(im.resize((W, round(im.height * s)), Image.LANCZOS)).astype(np.float32)
topo = cv2.GaussianBlur(a[:30].mean(axis=0, keepdims=True), (0, 0), sigmaX=40, sigmaY=.1)
ext = np.repeat(topo, T, axis=0) * np.linspace(.975, 1, T)[:, None, None]
ext += np.random.default_rng(3).normal(0, 2, ext.shape[:2])[..., None]
full = np.concatenate([ext, a])[:H].copy()
for k in range(40):
    t = (k / 40) ** 1.5; full[T + k] = full[T + k] * t + ext[-1] * (1 - t)
Image.fromarray(np.clip(full, 0, 255).astype(np.uint8)).save('fotos/capa-v3.jpg', quality=95)
print('ok')
