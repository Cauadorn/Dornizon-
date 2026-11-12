# Mockup MATILHA running club: cena gerada (base-corrida.png) no esquema da Grandorf (grande-angular de baixo, a pessoa
# correndo com o cachorro, o rosto fora do quadro) com a roupa combinando do Juicy Kibbles (jaqueta verde-limão de listras
# pretas na pessoa e no vizsla; o short já veio com a estampa de cachorrinhos correndo).
# Aqui entra a marca de verdade:
#   1) garrafinha: rótulo branco enrolado no cilindro (homografia + u = asin), a mão fica na frente (máscara pelo branco do rótulo);
#   2) peito: logo bordado em preto, pequeno, com sombra de relevo e a luz das dobras do tecido;
#   3) jaqueta do cachorro: só o cachorro do logo, bordado.
import numpy as np, cv2
from PIL import Image

foto = np.asarray(Image.open('base-corrida.png').convert('RGB')).astype(np.float32) / 255
H, W = foto.shape[:2]
lum = foto.mean(2)
out = foto.copy()
def lin(c): return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def srgb(l): return np.where(l <= 0.0031308, l * 12.92, 1.055 * np.clip(l, 0, None) ** (1 / 2.4) - 0.055)
logo = np.asarray(Image.open('../logo-matilha-preto.png').convert('RGBA')).astype(np.float32) / 255
cao = np.asarray(Image.open('../cao-salto.png').convert('RGBA')).astype(np.float32) / 255

# ---------- 1) garrafinha ----------
Q = np.array([(403.5, 273), (470.5, 283.5), (447.5, 378), (384.5, 362)], np.float32)   # cantos do rótulo branco
AW, AH = 1100, 1000                                          # arte = meia volta do rótulo (pi*r x altura)
arte = np.ones((AH, AW, 3), np.float32)
lg = cv2.resize(logo, (int(AW * .62), int(AW * .62 * logo.shape[0] / logo.shape[1])), interpolation=cv2.INTER_AREA)
y0, x0 = (AH - lg.shape[0]) // 2 + 20, (AW - lg.shape[1]) // 2
a = lg[..., 3:4]; arte[y0:y0 + lg.shape[0], x0:x0 + lg.shape[1]] = arte[y0:y0 + lg.shape[0], x0:x0 + lg.shape[1]] * (1 - a) + lg[..., :3] * a
cv2.rectangle(arte, (0, 60), (AW, 84), (0.263, 0.259, 1.0), -1)            # filete azul elétrico em cima
cv2.rectangle(arte, (0, AH - 84), (AW, AH - 60), (0.263, 0.259, 1.0), -1)  # e embaixo
M = cv2.getPerspectiveTransform(np.float32([[0, 0], [1, 0], [1, 1], [0, 1]]), Q)
Mi = np.linalg.inv(M)
S = 4
bx0, by0, bx1, by1 = 378, 268, 476, 384
ys, xs = np.mgrid[0:(by1 - by0) * S, 0:(bx1 - bx0) * S].astype(np.float32)
px = bx0 + (xs + .5) / S - .5; py = by0 + (ys + .5) / S - .5
den = Mi[2, 0] * px + Mi[2, 1] * py + Mi[2, 2]
s = (Mi[0, 0] * px + Mi[0, 1] * py + Mi[0, 2]) / den; t = (Mi[1, 0] * px + Mi[1, 1] * py + Mi[1, 2]) / den
dentro = ((s >= 0) & (s <= 1) & (t >= 0) & (t <= 1)).astype(np.float32)
u = (np.arcsin(np.clip(2 * s - 1, -.999, .999)) / np.pi + .5) * (AW - 1)
v = np.clip(t, 0, 1) * (AH - 1)
amostra = cv2.remap(arte, u.astype(np.float32), v.astype(np.float32), cv2.INTER_LINEAR)
sub = foto[by0:by1, bx0:bx1]; sl = sub.mean(2); sat = sub.max(2) - sub.min(2)
branco = ((sl > 0.45) & (sat < 0.13)).astype(np.float32)
branco = cv2.morphologyEx(branco, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
ref = np.percentile(sl[branco > 0], 97)
luz = np.clip(cv2.resize(np.clip(sl / ref, 0, 1.02), ((bx1 - bx0) * S, (by1 - by0) * S), interpolation=cv2.INTER_CUBIC), 0, 1.02)[..., None] ** 2.2
pint = srgb(lin(amostra) * luz) * dentro[..., None]
pm = cv2.resize(pint, (bx1 - bx0, by1 - by0), interpolation=cv2.INTER_AREA)
mq = cv2.resize(dentro, (bx1 - bx0, by1 - by0), interpolation=cv2.INTER_AREA)
m = (cv2.GaussianBlur(branco, (0, 0), .6) * mq)[..., None]
cor = pm / np.maximum(mq[..., None], 1e-3)
out[by0:by1, bx0:bx1] = out[by0:by1, bx0:bx1] * (1 - m) + cor * m

# ---------- 2) e 3) bordados ----------
def borda(img, cx, cy, largura, giro):
    global out
    h = int(largura * img.shape[0] / img.shape[1])
    a = cv2.resize(img[..., 3], (largura * 4, h * 4), interpolation=cv2.INTER_AREA)
    R = cv2.getRotationMatrix2D((largura * 2, h * 2), giro, 1)
    a = cv2.warpAffine(a, R, (largura * 4, h * 4))
    a = cv2.resize(a, (largura, h), interpolation=cv2.INTER_AREA)
    X0, Y0 = int(cx - largura / 2), int(cy - h / 2)
    reg = out[Y0:Y0 + h, X0:X0 + largura]; L = lum[Y0:Y0 + h, X0:X0 + largura]
    dobra = np.clip(L / cv2.GaussianBlur(L, (0, 0), 6), .75, 1.2)[..., None]  # luz das dobras do tecido
    sombra = np.roll(a, 1, axis=0)[..., None] * .35                           # relevo do bordado
    reg = reg * (1 - sombra * (1 - a[..., None]) * .6)
    fio = np.full_like(reg, .07) * dobra + np.clip((dobra - 1) * .25, 0, None)
    grao = (np.random.default_rng(3).random(a.shape)[..., None] - .5) * .05
    out[Y0:Y0 + h, X0:X0 + largura] = reg * (1 - a[..., None]) + np.clip(fio + grao, 0, 1) * a[..., None]

borda(logo, 607, 172, 66, 3)       # peito esquerdo da pessoa (lado direito da foto)
borda(cao, 238, 742, 40, 4)        # jaqueta do vizsla, entre as listras

Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save('mockup-corrida-matilha.jpg', quality=94)
print('ok')
