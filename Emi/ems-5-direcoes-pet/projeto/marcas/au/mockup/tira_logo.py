# Tira o logo grande do canto do mockup (a Emi: "tira só esse logo daí"); o logo fica só na roupa.
# O logo preto está sobre o céu: máscara = pixels escuros na caixa do canto, alargada; preenchimento por inpaint
# (Telea) em escala reduzida, para o céu sair liso, e o grão da foto volta por cima.
import numpy as np, cv2
from PIL import Image
im = np.asarray(Image.open('mockup-corrida-matilha-final.jpg').convert('RGB'))
H, W = im.shape[:2]
x0, y0, x1, y1 = 1120, 20, 1720, 430
cx = im[y0:y1, x0:x1].astype(np.float32) / 255
lum = cx.mean(2)
m = (lum < 0.42).astype(np.uint8)
m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17)))
k = 2
peq = cv2.resize(im[y0:y1, x0:x1], ((x1 - x0) // k, (y1 - y0) // k), interpolation=cv2.INTER_AREA)
mp = cv2.resize(m, ((x1 - x0) // k, (y1 - y0) // k), interpolation=cv2.INTER_NEAREST)
cheio = cv2.inpaint(cv2.cvtColor(peq, cv2.COLOR_RGB2BGR), mp, 12, cv2.INPAINT_TELEA)
cheio = cv2.cvtColor(cheio, cv2.COLOR_BGR2RGB)
cheio = cv2.resize(cheio, (x1 - x0, y1 - y0), interpolation=cv2.INTER_CUBIC).astype(np.float32)
cheio = cv2.GaussianBlur(cheio, (0, 0), 2.5)
ruido = np.random.default_rng(5).normal(0, 2.2, cheio.shape[:2])[..., None]
cheio = cheio + ruido
mf = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 3)[..., None]
reg = im[y0:y1, x0:x1].astype(np.float32)
out = im.copy(); out[y0:y1, x0:x1] = np.clip(reg * (1 - mf) + cheio * mf, 0, 255).astype(np.uint8)
Image.fromarray(out).save('mockup-corrida-matilha-sem-logo.jpg', quality=93)
print('ok')
