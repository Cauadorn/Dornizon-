# MIAU.LAB · post de apresentação: prepara as lâminas de foto (1440x1800).
# - cada foto entra em "cover" (corta o excesso, centralizado, com ajuste fino dx/dy em fração);
# - a panorâmica (L5|6) vira 2880x1800 e é cortada ao meio: a divisa cai exatamente no meio, para a conexão encaixar;
# - grão de filme leve e igual em todas (como as fotos da RUTH), com semente fixa para ser reproduzível.
# uso: monta-fotos.py entrada.png saida-prefixo [pano] [dx] [dy] [grao]
import sys, numpy as np
from PIL import Image
ent, pref = sys.argv[1], sys.argv[2]
pano = len(sys.argv) > 3 and sys.argv[3] == 'pano'
dx = float(sys.argv[4]) if len(sys.argv) > 4 else 0; dy = float(sys.argv[5]) if len(sys.argv) > 5 else 0
gr = float(sys.argv[6]) if len(sys.argv) > 6 else 7
W, H = (2880, 1800) if pano else (1440, 1800)
im = Image.open(ent).convert('RGB')
k = max(W / im.width, H / im.height)
im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
x0 = (im.width - W) / 2 * (1 + dx); y0 = (im.height - H) / 2 * (1 + dy)
im = im.crop((round(x0), round(y0), round(x0) + W, round(y0) + H))
a = np.asarray(im).astype(np.float32)
rng = np.random.default_rng(7)
g = rng.normal(0, 1, (H, W)).astype(np.float32)
# grão mais visível nos meios-tons, quase nada nos brancos e pretos
lum = a.mean(2) / 255; peso = 4 * lum * (1 - lum)
a = np.clip(a + (g * gr * peso)[..., None], 0, 255).astype(np.uint8)
out = Image.fromarray(a)
if pano:
    out.crop((0, 0, 1440, 1800)).save(pref + '-a.png'); out.crop((1440, 0, 2880, 1800)).save(pref + '-b.png')
else:
    out.save(pref + '.png')
print('ok', pref)
