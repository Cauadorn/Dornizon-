# MIAU.LAB · troca a estampa de uma embalagem numa foto gerada (Nano Banana) pela arte EXATA (a IA deforma o logo:
# esticou o U, alargou as letras). Mantém a foto: a luz, as dobras e o brilho da embalagem saem de um mapa de luz
# tirado da própria foto — cada pixel da estampa antiga é dividido pela média da sua cor (cobalto, rosa, preto, creme),
# então sobra só a iluminação, suavizada sem atravessar as bordas da estampa. Os dedos por cima ficam intactos.
# uso: troca-estampa.py foto.png arte.png "TL TR BR BL" mascara-embalagem.npy saida.png [mascara-dedos.npy]
import sys, numpy as np, cv2
from PIL import Image
foto = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(np.float32)
arte = np.asarray(Image.open(sys.argv[2]).convert('RGB')).astype(np.float32)
quad = np.float32([[float(v) for v in p.split(',')] for p in sys.argv[3].split()])
emb = np.load(sys.argv[4]).astype(np.float32)
dedos = np.load(sys.argv[6]).astype(np.float32) if len(sys.argv) > 6 else np.zeros_like(emb)
H, W = foto.shape[:2]
lum = foto.mean(2)
# 1) classes de cor da estampa antiga (k-means em Lab, só dentro da embalagem)
lab = cv2.cvtColor(foto.astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)
dentro = (emb > .5) & (dedos < .5)
amostra = lab[dentro][::7]
K = 4
_, rot, centros = cv2.kmeans(amostra, K, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 40, .5), 4, cv2.KMEANS_PP_CENTERS)
# a classe de cada pixel ignora o L (para a sombra não trocar a classe): distância só em a,b + um pouco de L
d = np.stack([((lab[..., 1] - c[1]) ** 2 + (lab[..., 2] - c[2]) ** 2 + .15 * (lab[..., 0] - c[0]) ** 2) for c in centros], -1)
cls = d.argmin(-1)
luz = np.zeros((H, W), np.float32); peso = np.zeros((H, W), np.float32)
# só a cor dominante (a de maior área, o fundo da embalagem) informa a luz: as outras deixavam fantasmas da estampa antiga
dom = int(np.argmax([((cls == k) & dentro).sum() for k in range(K)]))
for k in [dom]:
    mk = (cls == k) & dentro
    if mk.sum() < 500: continue
    med = np.median(lum[mk])
    if med < 25: continue                                   # preto: não informa a luz
    nucleo = cv2.erode(mk.astype(np.uint8), np.ones((7, 7), np.uint8)).astype(np.float32)  # longe das bordas da estampa
    luz += nucleo * lum / med; peso += nucleo
# a luz vira uma superfície polinomial suave (grau 4) ajustada nos pontos da cor dominante: cobre a embalagem toda,
# inclusive onde a estampa antiga tinha outra cor, sem herdar nenhuma forma dela
ys, xs = np.nonzero(peso > .5)
sel = np.random.default_rng(1).choice(len(ys), min(len(ys), 60000), replace=False); ys, xs = ys[sel], xs[sel]
def base(x, y, g=4):
    x = x / W * 2 - 1; y = y / H * 2 - 1
    return np.stack([x ** i * y ** j for i in range(g + 1) for j in range(g + 1 - i)], -1)
coef, *_ = np.linalg.lstsq(base(xs.astype(np.float32), ys.astype(np.float32)), (luz[ys, xs] / peso[ys, xs]), rcond=None)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
luz = np.clip((base(xx.ravel(), yy.ravel()) @ coef).reshape(H, W), .35, 1.45).astype(np.float32)
# 2) arte em perspectiva (reduzida antes, sem serrilhado; borda replicada)
lados = (int(np.linalg.norm(quad[1] - quad[0]) * 1.5), int(np.linalg.norm(quad[3] - quad[0]) * 1.5))
a = cv2.resize(arte, lados, interpolation=cv2.INTER_AREA)
M = cv2.getPerspectiveTransform(np.float32([[0, 0], [lados[0], 0], [lados[0], lados[1]], [0, lados[1]]]), quad)
aw = cv2.warpPerspective(a, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
# 3) cor da arte × luz (sombras escurecem; o que passa de 1 vira brilho por cima, como no plástico fosco da foto)
pint = aw * np.clip(luz, 0, 1)[..., None] ** 1.05 + np.clip(luz - 1, 0, None)[..., None] * 255 * .6
m = np.clip(emb * (1 - dedos), 0, 1)[..., None]
out = foto * (1 - m) + pint * m
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(sys.argv[5])
print('ok', W, H)
