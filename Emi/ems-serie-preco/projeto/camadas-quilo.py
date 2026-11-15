# Separa a cena da balança para o prato começar VAZIO e cada peça cair de uma vez:
# fundo sem prato, fundo do prato, cada peça (A, a, 4 amostras, estrela, cursor, 2 peças do ar),
# frente do prato (fica por cima das peças), ponteiro e máscara da palavra.
import sys, json, numpy as np, cv2
src, out = sys.argv[1], sys.argv[2]
im = cv2.imread(src); H, W = im.shape[:2]
fg = cv2.imread(out + '/fg.png', 0)
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV); hh, ss, vv = hsv[..., 0].astype(int), hsv[..., 1].astype(int), hsv[..., 2].astype(int)
yy, xx = np.mgrid[0:H, 0:W]
meta = {'w': W, 'h': H}
C = lambda x, y: (190 + x / 2, 90 + y / 2)                       # coordenada do recorte ampliado -> imagem
def poly(pts):
    m = np.zeros((H, W), np.uint8); cv2.fillPoly(m, [np.array([C(*p) for p in pts], np.int32)], 255); return m > 0
def caixa(x0, y0, x1, y1): return poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
K = np.ones((7, 7), np.uint8)
fecha = lambda m: cv2.morphologyEx(m.astype(np.uint8) * 255, cv2.MORPH_CLOSE, K) > 0

def salva(nome, alpha, img=None, pad=6):
    img = im if img is None else img
    a = cv2.GaussianBlur(alpha.astype(np.uint8), (0, 0), 1.0)
    ys, xs = np.where(a > 8); x0, x1, y0, y1 = max(xs.min() - pad, 0), min(xs.max() + pad, W), max(ys.min() - pad, 0), min(ys.max() + pad, H)
    cv2.imwrite(f'{out}/{nome}.png', np.dstack([img[y0:y1, x0:x1], a[y0:y1, x0:x1]]))
    meta[nome] = {'x': int(x0), 'y': int(y0), 'w': int(x1 - x0), 'h': int(y1 - y0)}

corte = 491; meta['corte'] = corte
topo = (fg > 110); topo[corte:, :] = False
# arco da frente do prato: metade de baixo de uma elipse
ecx, ecy = C(600, 545); erx, ery = 530 / 2, 50 / 2
dentro_el = ((xx - ecx) / erx) ** 2 + ((yy - ecy) / ery) ** 2 <= 1
arco = ecy + ery * np.sqrt(np.clip(1 - ((xx - ecx) / erx) ** 2, 0, 1))
acima = (yy < arco) & (np.abs(xx - ecx) <= erx) | (yy < ecy) & (np.abs(xx - ecx) > erx)

amar = (hh >= 8) & (hh <= 36) & (ss > 70) & (vv > 90)
rosa = ((hh >= 148) & (hh <= 178)) & (ss > 90) & (vv > 70)
marf = (hh >= 10) & (hh <= 40) & (ss <= 70) & (vv > 150)
viol = (hh >= 118) & (hh <= 146) & (ss > 110) & (vv > 120)
lila = (hh >= 126) & (hh <= 160) & (ss >= 25) & (ss <= 125) & (vv > 135)

pil = topo & acima
pe = topo & (yy < arco + 24)          # as peças da frente têm o pé um pouco abaixo do arco
P_amarela = poly([(712, 272), (786, 88), (958, 138), (960, 205), (828, 342)])
m = {}
m['cursor'] = fecha(topo & rosa & (xx > C(965, 0)[0]))   # a ponta do cursor passa na frente da borda
m['estrela'] = fecha(pe & (marf | amar) & caixa(808, 392, 1028, 640)) & ~m['cursor']
m['amostra3'] = fecha(pil & amar & P_amarela)
resto_amar = pe & amar & ~m['amostra3'] & ~m['estrela']
divisa = np.where(yy >= C(0, 380)[1], C(548, 0)[0], C(566, 0)[0])
m['a'] = fecha(resto_amar & (xx >= divisa)); m['A'] = fecha(resto_amar & (xx < divisa))
m['amostra1'] = fecha(pil & rosa & (xx < C(655, 0)[0])) & ~m['A'] & ~m['a']
m['amostra2'] = fecha(pil & viol & caixa(600, 50, 815, 305)) & ~m['a'] & ~m['amostra1'] & ~m['amostra3']
m['amostra4'] = fecha(pil & lila & poly([(800, 345), (935, 165), (1085, 245), (975, 470), (822, 480)])) & ~m['estrela'] & ~m['cursor'] & ~m['a'] & ~m['amostra3']
def maior(mk):   # só o corpo da peça: tira reflexo solto da mesma cor
    n, lab, st, _ = cv2.connectedComponentsWithStats(mk.astype(np.uint8)); return lab == 1 + int(np.argmax(st[1:, 4]))
for k in m: m[k] = (maior(m[k] & topo)).astype(np.uint8) * 255

# amostras: completa a parte escondida atrás das letras, esticando a amostra na direção do prato
def completa(mask, comp=120):
    ys, xs = np.where(mask > 0); c = np.array([xs.mean(), ys.mean()])
    alvo = np.array([ecx, ecy + 10.0]); d = (alvo - c) / np.linalg.norm(alvo - c)
    base = cv2.erode(mask, np.ones((5, 5), np.uint8)); cor = np.median(im[base > 0], axis=0)
    img = im.copy().astype(np.float32); acc = mask.copy(); src_m = base.copy()
    for i in range(2, comp, 2):
        Mx = np.float32([[1, 0, d[0] * i], [0, 1, d[1] * i]])
        sm = cv2.warpAffine(src_m, Mx, (W, H)); si = cv2.warpAffine(im, Mx, (W, H)).astype(np.float32)
        novo = (sm > 0) & (acc == 0)
        img[novo] = .35 * si[novo] + .65 * cor * (1 - .10 * i / comp); acc[novo] = 255
    return img.astype(np.uint8), acc
# PEÇAS INTEIRAS: o "A" e as amostras vêm de imagens geradas sozinhas (cenas/pecas), encaixadas no lugar da arte,
# para caírem completas, sem o pedaço que na arte fica escondido atrás de outra peça.
PEC = src.rsplit('/', 1)[0] + '/pecas'
def casa_cor(rgba, alvo):      # aproxima a cor da peça nova da cor da peça na arte
    a = rgba[..., 3] > 200; g = alvo / (np.median(rgba[..., :3][a], axis=0) + 1e-3)
    rgba[..., :3] = np.clip(rgba[..., :3].astype(np.float32) * (0.5 + 0.5 * g), 0, 255).astype(np.uint8); return rgba
for k in ['amostra1', 'amostra2', 'amostra3', 'amostra4']:
    ys, xs = np.where(m[k] > 0); pts = np.stack([xs, ys], 1).astype(np.float32); c = pts.mean(0)
    w_, v_ = np.linalg.eigh(np.cov((pts - c).T)); u = v_[:, 1]
    if np.dot(u, np.array([ecx, ecy]) - c) < 0: u = -u
    v = np.array([u[1], -u[0]]); pu = (pts - c) @ u; pv = (pts - c) @ v
    larg = np.percentile(pv, 99.5) - np.percentile(pv, .5); meio = (np.percentile(pv, 99.5) + np.percentile(pv, .5)) / 2
    topo_pt = c + u * np.percentile(pu, .3) + v * meio
    card = cv2.imread(f'{PEC}/{k}-rec.png', cv2.IMREAD_UNCHANGED); hc, wc = card.shape[:2]; esc = larg / wc
    card = casa_cor(card, np.median(im[cv2.erode(m[k], np.ones((9, 9), np.uint8)) > 0], axis=0))
    A_ = cv2.getAffineTransform(np.float32([[wc / 2, 0], [wc, 0], [wc / 2, hc]]), np.float32([topo_pt, topo_pt + v * larg / 2, topo_pt + u * hc * esc * .86]))
    wp = cv2.warpAffine(card, A_, (W, H), flags=cv2.INTER_AREA); salva(k, wp[..., 3], wp[..., :3])
# "A" inteiro, na altura e na posição do "A" da arte
ys, xs = np.where(m['A'] > 0); x0, y0, hA = xs.min(), ys.min(), ys.max() - ys.min() + 1
la = casa_cor(cv2.imread(f'{PEC}/A-rec.png', cv2.IMREAD_UNCHANGED), np.median(im[cv2.erode(m['A'], np.ones((9, 9), np.uint8)) > 0], axis=0))
la = cv2.resize(la, (int(la.shape[1] * hA / la.shape[0]), hA), interpolation=cv2.INTER_AREA); tela = np.zeros((H, W, 4), np.uint8)
tela[y0:y0 + la.shape[0], x0:x0 + la.shape[1]] = la; salva('A', tela[..., 3], tela[..., :3])
# "a" e estrela: completa a mordida onde a peça da frente passa por cima
def completa_mordida(k, da_frente, lado):
    limpa = cv2.inpaint(im, cv2.dilate(m[da_frente], np.ones((9, 9), np.uint8)), 9, cv2.INPAINT_TELEA)
    ys, xs = np.where(m[da_frente] > 0); xc = xs.mean()
    perto = cv2.dilate(m[k], np.ones((lado, lado), np.uint8)) > 0
    cheia = (m[k] > 0) | ((m[da_frente] > 0) & perto & (xx < xc)); salva(k, cv2.morphologyEx(cheia.astype(np.uint8) * 255, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)), limpa)
# "a" inteiro: mesma altura do "a" da arte, alinhado pela direita (a esquerda dele fica atrás do pé do "A")
ys, xs = np.where(m['a'] > 0); x1, y0, ha = xs.max(), ys.min(), ys.max() - ys.min() + 1
lm = casa_cor(cv2.imread(f'{PEC}/a-min-rec.png', cv2.IMREAD_UNCHANGED), np.median(im[cv2.erode(m['a'], np.ones((9, 9), np.uint8)) > 0], axis=0))
lm = cv2.resize(lm, (int(lm.shape[1] * ha / lm.shape[0]), ha), interpolation=cv2.INTER_AREA); tela = np.zeros((H, W, 4), np.uint8)
tela[y0:y0 + lm.shape[0], x1 + 1 - lm.shape[1]:x1 + 1] = lm; salva('a', tela[..., 3], tela[..., :3])
# estrela: só o marfim dela, completando a ponta que o cursor cobre
m['estrela'] = maior(cv2.morphologyEx(((m['estrela'] > 0) & (ss < 112)).astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))).astype(np.uint8) * 255; m['estrela'] = cv2.morphologyEx(m['estrela'], cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
completa_mordida('estrela', 'cursor', 25); salva('cursor', m['cursor'])

# frente do prato: tudo do topo que não é peça (inclui a tigela até o pescoço)
todas = np.zeros((H, W), np.uint8)
for k in m: todas |= cv2.dilate(m[k], np.ones((3, 3), np.uint8))
frente = topo & ~acima
resto = cv2.dilate(((amar | rosa | (marf & (ss > 28))) & frente).astype(np.uint8) * 255, np.ones((17, 17), np.uint8))
val = (frente & (cv2.dilate(resto, np.ones((9, 9), np.uint8)) == 0)).astype(np.float32)     # só plástico do prato, sem resto de peça
num = cv2.GaussianBlur(im.astype(np.float32) * val[..., None], (0, 0), 16); den = cv2.GaussianBlur(val, (0, 0), 16)[..., None] + 1e-4
med = np.median(im[val > 0], axis=0); mist = np.where(den > .08, num / den, med)
forro = np.zeros_like(im); forro[:] = med; forro[val > 0] = im[val > 0]; forro[val == 0] = mist[val == 0].astype(np.uint8)
fora = (cv2.dilate(m['cursor'], np.ones((9, 9), np.uint8)) > 0) & (xx > ecx + erx - 14)   # rabo do cursor que passa da ponta do prato
salva('prato-forro', (frente & ~fora).astype(np.uint8) * 255, forro)   # atrás das peças: tapa os buracos dos pés
salva('prato-frente', (frente & (cv2.dilate(todas, np.ones((5, 5), np.uint8)) == 0)).astype(np.uint8) * 255)   # nítido, por cima
# borda de trás e pontas do prato que já aparecem na arte (lilás, fora das peças)
tras = topo & acima & (todas == 0) & lila & (yy > C(0, 470)[1]); salva('prato-tras', fecha(tras).astype(np.uint8) * 255)

# peças que estão no ar
apagar = np.zeros((H, W), np.uint8)
claro = ((vv > 140) & (fg < 40)).astype(np.uint8) * 255; claro[260:, :] = 0; claro[:, :560] = 0
claro = cv2.morphologyEx(claro, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
n, lab, st, cen = cv2.connectedComponentsWithStats(claro)
for k, i in enumerate(sorted([i for i in range(1, n) if st[i, 4] > 600], key=lambda i: -st[i, 4])[:2]):
    mm = cv2.dilate((lab == i).astype(np.uint8) * 255, K); salva(f'ar{k + 1}', mm); apagar |= cv2.dilate(mm, np.ones((25, 25), np.uint8))

# ponteiro
reg = np.zeros((H, W), bool); reg[560:710, 460:630] = True
pont = cv2.morphologyEx((rosa & reg).astype(np.uint8) * 255, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
n, lab, st, cen = cv2.connectedComponentsWithStats(pont); pont = (lab == 1 + int(np.argmax(st[1:, 4]))).astype(np.uint8) * 255
dist = cv2.distanceTransform(pont, cv2.DIST_L2, 5); py, px = np.unravel_index(np.argmax(dist), dist.shape)
salva('ponteiro', cv2.dilate(pont, K), pad=10); meta['ponteiro'].update(px=int(px), py=int(py))

# fundo: sem peças do ar, sem ponteiro (e sem a sombra dele) e sem prato nenhum
bg = cv2.inpaint(im, apagar, 9, cv2.INPAINT_TELEA)
bg = cv2.inpaint(bg, cv2.dilate(pont, np.ones((33, 33), np.uint8)), 9, cv2.INPAINT_TELEA)
buraco = cv2.dilate(topo.astype(np.uint8) * 255, np.ones((31, 31), np.uint8)); buraco[corte + 6:, :] = 0
liso = cv2.inpaint(bg, buraco, 21, cv2.INPAINT_TELEA); borr = cv2.GaussianBlur(liso, (0, 0), 22)
w = cv2.GaussianBlur((cv2.erode(buraco, np.ones((41, 41), np.uint8))).astype(np.float32) / 255, (0, 0), 14)[..., None]
bg = (liso * (1 - w) + borr * w).astype(np.uint8); cv2.imwrite(out + '/fundo.png', bg)

# fundo do prato vazio: elipse lilás com a borda de trás mais clara
cor_in = np.median(im[tras], axis=0) if tras.sum() > 50 else np.array([225, 175, 205])
el = np.zeros((H, W, 3), np.float32); d2 = ((xx - ecx) / erx) ** 2 + ((yy - ecy) / ery) ** 2
sombra = np.clip((yy - (ecy - ery)) / (2 * ery), 0, 1)[..., None]
el[:] = cor_in * (.60 + .26 * sombra) * (1.04 - .10 * np.clip((xx - (ecx - erx)) / (2 * erx), 0, 1))[..., None]   # fundo da tigela: mais escuro atrás, clareia perto da borda da frente
aro = np.clip(1 - np.abs(np.sqrt(d2) - .93) / .09, 0, 1)[..., None] * (yy < ecy)[..., None]
el = np.clip(el + aro * 46, 0, 255)
salva('prato-fundo', (np.clip((1.02 - np.sqrt(d2)) / .04, 0, 1) * 255), el.astype(np.uint8))

pal = ((fg > 128) & rosa).astype(np.uint8) * 255; pal[:705, :] = 0
pal = cv2.GaussianBlur(cv2.morphologyEx(pal, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)), (0, 0), 1.5)
cv2.imwrite(out + '/palavra-mask.png', np.dstack([np.full((H, W, 3), 255, np.uint8), pal]))
json.dump(meta, open(out + '/meta.json', 'w'), indent=1)

# conferência: remonta a cena final com as camadas
def cola(dst, nome):
    s = cv2.imread(f'{out}/{nome}.png', cv2.IMREAD_UNCHANGED); q = meta[nome]; a = s[..., 3:4].astype(np.float32) / 255
    r = dst[q['y']:q['y'] + q['h'], q['x']:q['x'] + q['w']]; r[:] = (s[..., :3] * a + r * (1 - a)).astype(np.uint8)
vazio = bg.copy()
for nme in ['prato-fundo', 'prato-tras', 'prato-forro', 'prato-frente']: cola(vazio, nme)
cheio = bg.copy()
for nme in ['prato-fundo', 'prato-tras', 'prato-forro', 'amostra1', 'amostra2', 'amostra3', 'amostra4', 'A', 'a', 'estrela', 'cursor', 'prato-frente', 'ponteiro']: cola(cheio, nme)
cv2.imwrite(sys.argv[3], np.hstack([vazio[60:560, 150:870], cheio[60:560, 150:870], im[60:560, 150:870]]))
print({k: meta[k] for k in meta if isinstance(meta[k], dict)})
