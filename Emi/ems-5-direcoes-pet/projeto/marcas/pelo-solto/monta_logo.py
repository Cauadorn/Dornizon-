# pelo solto · monta o logo final a partir da base (logo-base.html, cada camada numa cor pura):
# separa as camadas, recorta cada uma "com tesoura" (cortes retos, approxPolyDP), pinta nas cores da marca,
# põe a sombra escura deslocada (Moon Gazer) e o grão de papel/tinta (Barking Barber).
# uso: monta_logo.py <base.png> <saida.png> [fundo=#F3E2C3] [pelo=#C8472B] [solto=#E39B2D] [poodle=#4A3115] [sombra=#3A2410] [brilho=#E39B2D]
import sys, numpy as np, cv2
from PIL import Image
args = sys.argv[1:]
base, saida = args[0], args[1]
cores = dict(fundo='#F3E2C3', pelo='#C8472B', solto='#E39B2D', poodle='#4A3115', sombra='#3A2410', brilho='#E39B2D')
for k, v in zip(['fundo', 'pelo', 'solto', 'poodle', 'sombra', 'brilho'], args[2:]): cores[k] = v
hx = lambda h: np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255
im = np.asarray(Image.open(base).convert('RGB')).astype(np.int32)
R, G, B = im[..., 0], im[..., 1], im[..., 2]
cam = {'pelo': (R > 200) & (G < 80) & (B < 80), 'solto': (G > 200) & (R < 80) & (B < 80),
       'poodle': (B > 200) & (R < 80) & (G < 80), 'brilho': (R > 200) & (B > 200) & (G < 80), 'sub': (G > 200) & (B > 200) & (R < 80)}
H, W = R.shape
S = 2
def tesoura(m, tol):
    big = cv2.resize(m.astype(np.uint8), (W * S, H * S), interpolation=cv2.INTER_NEAREST)
    cont, hier = cv2.findContours(big, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    out = np.zeros_like(big)
    for i, c in enumerate(cont):
        if hier[0][i][3] < 0 and cv2.contourArea(c) > (8 * S) ** 2: cv2.fillPoly(out, [cv2.approxPolyDP(c, tol * S, True)], 1)
    for i, c in enumerate(cont):
        if hier[0][i][3] >= 0 and cv2.contourArea(c) > (4 * S) ** 2: cv2.fillPoly(out, [cv2.approxPolyDP(c, tol * S, True)], 0)
    return cv2.resize(out.astype(np.float32), (W, H), interpolation=cv2.INTER_AREA)
mask = {k: tesoura(v, {'poodle': 3.5, 'brilho': 1.5, 'sub': 1.2}.get(k, 4.5)) for k, v in cam.items()}
tudo = np.clip(mask['pelo'] + mask['solto'] + mask['poodle'], 0, 1)
# sombra: tudo deslocado para baixo e para a direita (papel escuro atrás)
M = np.float32([[1, 0, 9], [0, 1, 11]])
sombra = np.clip(cv2.warpAffine(tudo, M, (W, H)) - tudo, 0, 1)
out = np.ones((H, W, 3), np.float32) * hx(cores['fundo'])
def pinta(m, cor):
    global out
    out = out * (1 - m[..., None]) + hx(cor) * m[..., None]
pinta(sombra, cores['sombra']); pinta(mask['poodle'], cores['poodle']); pinta(mask['pelo'], cores['pelo'])
pinta(mask['solto'], cores['solto']); pinta(mask['brilho'], cores['brilho']); pinta(mask['sub'], cores['poodle'])
# grão: falhas de tinta (pontinhos do fundo dentro da tinta) + respingos leves no fundo
rng = np.random.default_rng(11)
n = rng.random((H, W)); falha = (n > .985).astype(np.float32); falha = cv2.GaussianBlur(falha, (0, 0), .6)
tinta = np.clip(tudo + sombra + mask['brilho'] + mask['sub'], 0, 1)
out = out * (1 - (falha * tinta)[..., None] * .55) + hx(cores['fundo']) * (falha * tinta)[..., None] * .55
grao = (rng.random((H, W)) - .5)[..., None] * .045
out = np.clip(out + grao, 0, 1)
Image.fromarray((out * 255).astype(np.uint8)).save(saida); print('ok', saida)
