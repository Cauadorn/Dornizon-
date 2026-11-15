# Separa a cena da balança em camadas que se mexem de verdade:
# fundo limpo, prato+pilha (afunda), ponteiro (gira), duas peças no ar (caem) e a máscara da palavra (brilho).
import sys, json, numpy as np, cv2
src, out = sys.argv[1], sys.argv[2]
im = cv2.imread(src); H, W = im.shape[:2]
fg = cv2.imread(out + '/fg.png', 0)
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
meta = {'w': W, 'h': H}

def sprite(mask, nome, pad=6):
    m = cv2.GaussianBlur(mask, (0, 0), 1.2)
    ys, xs = np.where(m > 8); x0, x1, y0, y1 = max(xs.min() - pad, 0), min(xs.max() + pad, W), max(ys.min() - pad, 0), min(ys.max() + pad, H)
    rgba = np.dstack([im[y0:y1, x0:x1], m[y0:y1, x0:x1]]); cv2.imwrite(f'{out}/{nome}.png', rgba)
    meta[nome] = {'x': int(x0), 'y': int(y0), 'w': int(x1 - x0), 'h': int(y1 - y0)}

apagar = np.zeros((H, W), np.uint8)

# 1) peças no ar: claras sobre o fundo escuro, fora da máscara de objeto, no alto à direita
claro = ((hsv[..., 2] > 140) & (fg < 40)).astype(np.uint8) * 255
claro[260:, :] = 0; claro[:, :560] = 0
claro = cv2.morphologyEx(claro, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
n, lab, st, cen = cv2.connectedComponentsWithStats(claro)
pecas = sorted([i for i in range(1, n) if st[i, 4] > 600], key=lambda i: -st[i, 4])[:2]
for k, i in enumerate(pecas):
    m = cv2.dilate((lab == i).astype(np.uint8) * 255, np.ones((7, 7), np.uint8))
    sprite(m, f'peca{k + 1}'); apagar |= cv2.dilate(m, np.ones((25, 25), np.uint8))
    print('peça', k + 1, st[i].tolist())

# 2) ponteiro: rosa dentro do mostrador
pink = ((hsv[..., 0] > 150) & (hsv[..., 0] < 174) & (hsv[..., 1] > 90) & (hsv[..., 2] > 110)).astype(np.uint8) * 255
reg = np.zeros_like(pink); reg[560:710, 460:630] = 255
pont = cv2.morphologyEx(pink & reg, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
n, lab, st, cen = cv2.connectedComponentsWithStats(pont); i = 1 + int(np.argmax(st[1:, 4]))
pont = (lab == i).astype(np.uint8) * 255
dist = cv2.distanceTransform(pont, cv2.DIST_L2, 5); py, px = np.unravel_index(np.argmax(dist), dist.shape)  # eixo = parte mais gorda
pm = cv2.dilate(pont, np.ones((7, 7), np.uint8)); sprite(pm, 'ponteiro', 10)
meta['ponteiro']['px'] = int(px); meta['ponteiro']['py'] = int(py)
apagar_p = cv2.dilate(pont, np.ones((19, 19), np.uint8))
print('ponteiro', st[i].tolist(), 'eixo', px, py)

# 3) prato + pilha: a parte de cima do objeto, até o pescoço da balança
linha = np.array([(fg[y, 300:760] > 128).sum() for y in range(380, 560)]); corte = 380 + int(np.argmin(linha))
topo = fg.copy(); topo[corte:, :] = 0; topo[:, :] = np.where(topo > 0, topo, 0)
rgba = np.dstack([im, topo]); cv2.imwrite(out + '/topo.png', rgba); meta['corte'] = corte
print('corte no pescoço em y =', corte)
# faixa que aparece quando o topo desce: apaga do fundo
tb = (topo > 60).astype(np.uint8) * 255
desc = np.zeros_like(tb); desc[22:, :] = tb[:-22, :]
faixa = cv2.dilate(tb, np.ones((7, 7), np.uint8)) & ~desc; faixa[corte - 4:, :] = 0

# 4) fundo limpo
bg = cv2.inpaint(im, apagar, 9, cv2.INPAINT_TELEA)
bg = cv2.inpaint(bg, apagar_p, 7, cv2.INPAINT_TELEA)
bg = cv2.inpaint(bg, faixa, 9, cv2.INPAINT_TELEA)
cv2.imwrite(out + '/fundo.png', bg)

# 5) palavra: objeto abaixo do mostrador, rosa
pal = ((fg > 128) & (pink > 0)).astype(np.uint8) * 255; pal[:705, :] = 0
pal = cv2.morphologyEx(pal, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)); pal = cv2.GaussianBlur(pal, (0, 0), 1.5)
cv2.imwrite(out + '/palavra-mask.png', np.dstack([np.full((H, W, 3), 255, np.uint8), pal]))
json.dump(meta, open(out + '/meta.json', 'w'), indent=1); print(json.dumps(meta))
