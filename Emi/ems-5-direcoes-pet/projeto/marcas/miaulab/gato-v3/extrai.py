# MIAU.LAB · gato v3: separa a silhueta gerada (gerado-b.png) em cabeça + pata esquerda + pata direita, vetoriza cada
# uma (potrace) e grava gato-v3/gato.js para o logo.js montar como no original: uma pata em cada haste do U,
# com o fio na cor do fundo entre a pata e a cara, e os arranhões saindo da ponta das unhas.
# Coordenadas no espaço da imagem gerada (1024 px); a "borda" (topo do U) fica em y = BORDA.
import sys, json, numpy as np, cv2, potrace
from PIL import Image
# uso: extrai.py [F orelha] [saída .js] [desenho .png]; a borda (topo do U) = base reta da cabeça, achada sozinha
S = 4
ORIGEM = sys.argv[3] if len(sys.argv) > 3 else 'gato-v3/gerado-e.png'
g = np.asarray(Image.open(ORIGEM).convert('L')).astype(np.float32) / 255
m = (g < .5).astype(np.uint8)
n, lab, st, cen = cv2.connectedComponentsWithStats(m, connectivity=4)
grandes = sorted([i for i in range(1, n) if st[i][4] > 50], key=lambda i: -st[i][4])
cab = grandes[0]
BORDA = int(np.where(lab[:, 512] == cab)[0].max()) + 1
patas = sorted(grandes[1:3], key=lambda i: cen[i][0])          # esquerda, direita
pecas = {'cabeca': None, 'pataE': lab == patas[0], 'pataD': lab == patas[1]}
for i in grandes[3:]:                                          # unha solta volta para a pata mais perto
    lado = 'pataE' if cen[i][0] < 512 else 'pataD'; pecas[lado] |= lab == i
# cabeça inteira: tudo junto, fios fechados, buracos preenchidos, cortada na borda
tudo = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
cnts, _ = cv2.findContours(tudo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cheia = np.zeros_like(m); cv2.drawContours(cheia, [max(cnts, key=cv2.contourArea)], -1, 1, -1)
cheia[BORDA:] = 0
# orelhas (a Emi: "a orelha não tá parecendo de gato… parece de raposa"): achata só o que fica acima do topo da cabeça
# (Y0), com transição suave de B px para a lateral da orelha não quebrar. F = altura nova da orelha / altura gerada.
F = float(sys.argv[1]) if len(sys.argv) > 1 else 1
Y0, B = 425, 70
yo = np.arange(m.shape[0], dtype=np.float32); t = np.clip(Y0 - yo, 0, None)
delta = np.where(t < B, (1 / F - 1) * t ** 2 / (2 * B), (1 / F - 1) * (t - B / 2))
mapy = np.repeat((yo - delta)[:, None], m.shape[1], 1).astype(np.float32)
mapx = np.repeat(np.arange(m.shape[1], dtype=np.float32)[None, :], m.shape[0], 0)
cheia = cv2.remap(cheia.astype(np.float32), mapx, mapy, cv2.INTER_LINEAR, borderValue=0) > .5
pecas['cabeca'] = cheia.astype(bool)
def caminho(mask):
    big = cv2.resize(mask.astype(np.float32), (mask.shape[1] * S, mask.shape[0] * S), interpolation=cv2.INTER_CUBIC)
    big = cv2.GaussianBlur(big, (0, 0), 1.6) > .5
    pl = potrace.Bitmap(~big).trace(turdsize=30, alphamax=1.0, opticurve=True, opttolerance=0.2)
    f = lambda p: f'{p.x / S:.1f} {p.y / S:.1f}'
    out = []
    for c in pl:
        d = [f'M{f(c.start_point)}']
        for s in c.segments:
            d.append(f'L{f(s.c)} L{f(s.end_point)}' if s.is_corner else f'C{f(s.c1)} {f(s.c2)} {f(s.end_point)}')
        out.append(' '.join(d) + 'Z')
    return ' '.join(out)
dados = {'borda': BORDA}
for nome, mk in pecas.items():
    ys, xs = np.where(mk)
    dados[nome] = {'d': caminho(mk), 'x0': int(xs.min()), 'x1': int(xs.max()), 'y0': int(ys.min()), 'y1': int(ys.max())}
    if nome != 'cabeca':
        # unhas: as geradas saíam com lascas brancas em volta ("uma sombra branca embaixo das unhas, não ficou legal").
        # A pata fica sem as unhas geradas (abertura morfológica come os ganchos finos) e o logo.js desenha as unhas e os
        # arranhões da v2 ("os arranhados eu queria mais parecidos com o primeiro") na ponta de cada dedo.
        corpo = cv2.morphologyEx(mk.astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))).astype(bool)
        corpo |= mk & (np.arange(mk.shape[0])[:, None] < BORDA + 19)
        dados[nome]['d'] = caminho(corpo)
        # ponta de cada dedo: os 3 pontos mais baixos do contorno de baixo, afastados entre si
        cols = np.where(corpo.any(0))[0]
        fundoY = np.array([np.where(corpo[:, x])[0].max() for x in cols], float)
        fundoY = np.convolve(fundoY, np.ones(7) / 7, 'same')
        ordem = np.argsort(-fundoY); dedos = []
        for i in ordem:
            if all(abs(cols[i] - d[0]) > 32 for d in dedos): dedos.append([int(cols[i]), float(fundoY[i])])
            if len(dedos) == 3: break
        dados[nome]['dedos'] = sorted(dedos)
        # pontas das unhas: o pixel mais baixo de cada pedaço abaixo de y=750
        sub = mk.copy(); sub[:750] = 0
        k, lb, s2, _ = cv2.connectedComponentsWithStats(sub.astype(np.uint8))
        pts = []
        for j in range(1, k):
            yy, xx = np.where(lb == j); b = yy.argmax(); pts.append([int(xx[b]), int(yy[b])])
        dados[nome]['unhas'] = sorted(pts)
# centro da cabeça na altura das bochechas
ys, xs = np.where(pecas['cabeca'][560:620]); dados['cabeca']['cx'] = float((xs.min() + xs.max()) / 2)
open(sys.argv[2] if len(sys.argv) > 2 else 'gato-v3/gato.js', 'w').write('// gerado por gato-v3/extrai.py\nconst GATO3 = ' + json.dumps(dados) + ';\n')
for k_, v in dados.items():
    if k_ != 'borda': print(k_, {a: b for a, b in v.items() if a != 'd'})
