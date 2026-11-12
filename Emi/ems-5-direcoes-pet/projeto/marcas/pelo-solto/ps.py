# pelo solto · monograma "ps" para estampar (a Emi vai usar os dois: o logo completo e o ps).
# O "p" de "pelo" e o "s" de "solto" saem do próprio logo (máscara do vetoriza.py). 1ª versão: na posição do logo,
# "mais junto" (a Emi não gostou do vão): o "s" sobe até ficar a FOLGA px do "p" (distância medida entre as máscaras).
# Com FOLGA negativa, o "s" entra no "p" e um filete na cor do fundo separa os dois (encostar e passar um pouco fica estilizado).
# uso: ps.py <nome-mask.npy> <saida.svg> <folga_px> [dx_px]
import sys, numpy as np, cv2, potrace
m = np.load(sys.argv[1]); saida = sys.argv[2]; FOLGA = float(sys.argv[3]); DX = float(sys.argv[4]) if len(sys.argv) > 4 else 0
S = 4
n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8))
comps = [(i, st[i]) for i in range(1, n) if st[i][4] > 5000 * S]
ip = min((c for c in comps if c[1][1] < 200 * S), key=lambda c: c[1][0])[0]
is_ = min((c for c in comps if c[1][1] > 300 * S), key=lambda c: c[1][0])[0]
P = (lab == ip).astype(np.uint8); Sm = (lab == is_).astype(np.uint8)
dt = cv2.distanceTransform(1 - P, cv2.DIST_L2, 5)            # distância de cada pixel até o "p"
def desloca(img, dx, dy): return cv2.warpAffine(img, np.float32([[1, 0, dx], [0, 1, dy]]), (img.shape[1], img.shape[0]), flags=cv2.INTER_NEAREST)
alvo = FOLGA * S; dy = 0
for dy in range(0, -200 * S, -2):                             # sobe o "s" até a menor distância chegar na folga
    s2 = desloca(Sm, DX * S, dy)
    d = dt[s2 > 0].min() if (s2 > 0).any() else 1e9
    if alvo >= 0 and d <= alvo: break
    if alvo < 0 and (P & s2).sum() > 0 and (cv2.distanceTransform(1 - s2, cv2.DIST_L2, 5)[P > 0].min() <= 0) and dy <= -int(-alvo) * 0: pass
    if alvo < 0 and (P & s2).sum() >= (-alvo) * S * 40: break
s2 = desloca(Sm, DX * S, dy)
if alvo < 0:
    # o "s" fica por cima do "p", com um filete na cor do fundo em volta do "s"
    filete = cv2.dilate(s2, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5 * S, 5 * S)))
    mm = ((P > 0) & (filete == 0)) | (s2 > 0)
else:
    mm = (P > 0) | (s2 > 0)
ys, xs = np.where(mm); mm = mm[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
plist = potrace.Bitmap(~mm).trace(turdsize=40, alphamax=1.15, opticurve=True, opttolerance=0.25)
f = lambda q: f'{q.x / S:.2f} {q.y / S:.2f}'
partes = []
for c in plist:
    dd = [f'M{f(c.start_point)}']
    for sg in c.segments:
        dd.append(f'L{f(sg.c)} L{f(sg.end_point)}' if sg.is_corner else f'C{f(sg.c1)} {f(sg.c2)} {f(sg.end_point)}')
    partes.append(' '.join(dd) + 'Z')
W, H = mm.shape[1] / S, mm.shape[0] / S
open(saida, 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} {H:.2f}" width="{W:.2f}" height="{H:.2f}"><path fill-rule="evenodd" fill="#5A2E17" d="{" ".join(partes)}"/></svg>')
print('ok', saida, 'subiu', -dy / S, 'px; tamanho', round(W, 1), round(H, 1))
