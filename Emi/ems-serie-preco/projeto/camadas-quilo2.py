# Segunda etapa: troca a balança da arte pela balança vazia gerada inteira (cenas/pecas/balanca-rec.png),
# refaz o fundo sem balança, separa a palavra (fica na frente) e troca as estrelas pela estrela inteira.
import sys, json, numpy as np, cv2
src, out = sys.argv[1], sys.argv[2]; PEC = src.rsplit('/', 1)[0] + '/pecas'
im = cv2.imread(src); H, W = im.shape[:2]; fg = cv2.imread(out + '/fg.png', 0)
meta = json.load(open(out + '/meta.json'))
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV); hh, ss, vv = hsv[..., 0].astype(int), hsv[..., 1].astype(int), hsv[..., 2].astype(int)
yy, xx = np.mgrid[0:H, 0:W]
def salva(nome, rgba, x, y): cv2.imwrite(f'{out}/{nome}.png', rgba); meta[nome] = {'x': int(x), 'y': int(y), 'w': int(rgba.shape[1]), 'h': int(rgba.shape[0])}

# palavra: rosa do objeto, do mostrador pra baixo
rosa = ((hh >= 148) & (hh <= 178)) & (ss > 90) & (vv > 70)
# recorte da palavra por GrabCut: rosa cheio é letra com certeza; violeta/marfim da balança antiga e o fundo são fundo com certeza;
# o que fica na dúvida (sombra e brilho na borda das letras) o algoritmo decide pela vizinhança, e a borda sai inteira
forte = rosa & (ss > 120) & (vv > 100)
viol = (hh >= 112) & (hh <= 146) & (ss > 70)
marf = (hh >= 8) & (hh <= 45) & (ss < 90) & (vv > 150)
gc = np.full((H, W), cv2.GC_PR_BGD, np.uint8)
gc[rosa & (fg > 100)] = cv2.GC_PR_FGD
gc[cv2.erode(forte.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0] = cv2.GC_FGD
gc[cv2.erode(((viol | marf) & ~rosa).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0] = cv2.GC_BGD
gc[fg < 20] = cv2.GC_BGD; gc[:700, :] = cv2.GC_BGD
y0, y1 = 690, 1120; sub = gc[y0:y1].copy()
cv2.grabCut(im[y0:y1], sub, None, np.zeros((1, 65)), np.zeros((1, 65)), 6, cv2.GC_INIT_WITH_MASK)
pal = np.zeros((H, W), np.uint8); pal[y0:y1] = np.where((sub == cv2.GC_FGD) | (sub == cv2.GC_PR_FGD), 255, 0)
n, lab, st, _ = cv2.connectedComponentsWithStats(pal); pal = np.isin(lab, [i for i in range(1, n) if st[i, 4] > 2500]).astype(np.uint8) * 255
cs, hi = cv2.findContours(pal, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
for i, c in enumerate(cs):
    if hi[0][i][3] >= 0 and cv2.contourArea(c) < 900: cv2.drawContours(pal, [c], -1, 255, -1)
pal = cv2.morphologyEx(pal, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
pal = cv2.GaussianBlur(pal, (0, 0), 1.0)
cv2.imwrite(out + '/palavra.png', np.dstack([im, pal])); cv2.imwrite(out + '/palavra-mask.png', np.dstack([np.full((H, W, 3), 255, np.uint8), pal]))

# fundo sem balança, sem peças e sem palavra (a palavra volta por cima, como camada)
tudo = cv2.dilate(((fg > 40) | (pal > 40)).astype(np.uint8) * 255, np.ones((35, 35), np.uint8))
claro = ((vv > 140) & (fg < 40)).astype(np.uint8) * 255; claro[260:, :] = 0; claro[:, :560] = 0
tudo |= cv2.dilate(cv2.morphologyEx(claro, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)), np.ones((31, 31), np.uint8))
tudo[1085:, :] = 0                                          # o reflexo da palavra no chão fica
peq = cv2.resize(im, (W // 4, H // 4), interpolation=cv2.INTER_AREA); mq = cv2.resize(tudo, (W // 4, H // 4), interpolation=cv2.INTER_NEAREST)
liso = cv2.resize(cv2.GaussianBlur(cv2.inpaint(peq, mq, 12, cv2.INPAINT_TELEA), (0, 0), 9), (W, H), interpolation=cv2.INTER_CUBIC)
w = cv2.GaussianBlur(tudo.astype(np.float32) / 255, (0, 0), 10)[..., None]
cv2.imwrite(out + '/fundo.png', (im * (1 - w) + liso * w).astype(np.uint8))

# balança nova: mesma largura de prato da pilha (com folga), centrada onde a antiga estava
bal = cv2.imread(f'{PEC}/balanca-rec.png', cv2.IMREAD_UNCHANGED); E = .70
bal = cv2.resize(bal, (int(bal.shape[1] * E), int(bal.shape[0] * E)), interpolation=cv2.INTER_AREA); hb, wb = bal.shape[:2]
bx, by = int(490 - 362 * E), int(362.5 - 78 * E)
ys, xs = np.mgrid[0:hb, 0:wb]; cx, cy, rx, ry = 362 * E, 78 * E, 356 * E, 62 * E
arco = cy + ry * np.sqrt(np.clip(1 - ((xs - cx) / rx) ** 2, 0, 1)); pesc = int(308 * E)
corpo = bal.copy(); corpo[:pesc - 12, :, 3] = 0; salva('bal-corpo', corpo, bx, by)
prato = bal.copy(); prato[pesc + 8:, :, 3] = 0; salva('bal-prato', prato[:pesc + 8], bx, by)
frente = bal.copy(); frente[..., 3] = np.where((ys > arco) & (ys < pesc - 6), frente[..., 3], 0); salva('bal-prato-frente', frente[:pesc], bx, by)
meta['balanca'] = {'eixo': [bx + 360 * E, by + 588 * E], 'pescoco': by + pesc, 'arco': [bx + cx, by + cy, rx, ry]}

# estrelas inteiras, no tamanho e no lugar das da arte
est = cv2.imread(f'{PEC}/estrela-rec.png', cv2.IMREAD_UNCHANGED)
for nome in ['estrela', 'ar2']:
    q = meta[nome]; t = max(q['w'], q['h']) - 12
    e = cv2.resize(est, (t, int(t * est.shape[0] / est.shape[1])), interpolation=cv2.INTER_AREA)
    salva(nome, e, q['x'] + (q['w'] - e.shape[1]) // 2, q['y'] + (q['h'] - e.shape[0]) // 2)
json.dump(meta, open(out + '/meta.json', 'w'), indent=1); print(meta['balanca'], meta['bal-corpo'], meta['estrela'], meta['ar2'])
