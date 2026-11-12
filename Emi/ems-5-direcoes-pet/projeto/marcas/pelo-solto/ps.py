# pelo solto · monograma "ps" para estampar (pedido da Emi: "uma versão PS pra estampar algumas coisas").
# Usa o "p" de "pelo" e o "s" de "solto" do próprio logo, na posição em que já estão (o pé do "p" desce ao lado do "s"):
# o monograma nasce do desenho aprovado, sem redesenhar. Precisa da máscara salva pelo vetoriza.py (nome-mask.npy).
import sys, numpy as np, cv2, potrace
m = np.load(sys.argv[1])
S = 4
n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8))
# "p" = o componente mais à esquerda em cima; "s" = o mais à esquerda embaixo
comps = [(i, st[i]) for i in range(1, n) if st[i][4] > 5000 * S]
p = min((c for c in comps if c[1][1] < 200 * S), key=lambda c: c[1][0])[0]
s = min((c for c in comps if c[1][1] > 300 * S), key=lambda c: c[1][0])[0]
mm = (lab == p) | (lab == s)
ys, xs = np.where(mm); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
mm = mm[y0:y1 + 1, x0:x1 + 1]
plist = potrace.Bitmap(~mm).trace(turdsize=40, alphamax=1.15, opticurve=True, opttolerance=0.25)
f = lambda q: f'{q.x / S:.2f} {q.y / S:.2f}'
partes = []
for c in plist:
    d = [f'M{f(c.start_point)}']
    for sg in c.segments:
        d.append(f'L{f(sg.c)} L{f(sg.end_point)}' if sg.is_corner else f'C{f(sg.c1)} {f(sg.c2)} {f(sg.end_point)}')
    partes.append(' '.join(d) + 'Z')
W, H = (x1 - x0 + 1) / S, (y1 - y0 + 1) / S
open('ps.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} {H:.2f}" width="{W:.2f}" height="{H:.2f}"><path fill-rule="evenodd" fill="#5A2E17" d="{" ".join(partes)}"/></svg>')
print('ok ps.svg', round(W, 2), round(H, 2))
