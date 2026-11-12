# Capa do case: foto da Emi grande (zoom 0,8, rosto à esquerda do centro), sombras puxadas para roxo/magenta.
# uso: python3 -I fotos/capa.py
import numpy as np
from PIL import Image
W, H, S, OX, OY = 1080, 1350, .8, -150, -40
im = Image.open('fotos/emi-capa.png').convert('RGB')
im = im.resize((round(im.width * S), round(im.height * S)), Image.LANCZOS)
can = Image.new('RGB', (W, H)); can.paste(im, (OX, OY))
a = np.asarray(can).astype(np.float32)
lum = (a * [.299, .587, .114]).sum(-1, keepdims=True) / 255
a += ((1 - lum) ** 2.2) * np.array([12, -6, 18])
Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save('fotos/capa-v2.jpg', quality=95)
print('ok')
