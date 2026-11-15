# MIAU.LAB · gato v3 (a Emi: "você refinou o logo? … tá refinadinho ou tá vetorizado?").
# O gato da v2 era desenhado na mão em SVG (cabeça quase retangular, laterais retas). A v3 parte de uma silhueta
# gerada (gerado.png: cabeça orgânica, patas sob as bochechas com um fio separando da cara, unhas em gancho) e a Emi
# pediu "menos pelinhos no rosto… mais parecido com o original": os tufos das bochechas são alisados por abertura
# morfológica de raio R (só entre y 300 e 745, para não arredondar a ponta das orelhas nem comer as unhas).
# Uso: vetoriza.py R  → gato-rR.svg (viewBox na escala da imagem gerada, 1024 px)
import sys, numpy as np, cv2, potrace
from PIL import Image
R = int(sys.argv[1]) if len(sys.argv) > 1 else 0
S = 4
g = np.asarray(Image.open('gato-v3/gerado.png').convert('L')).astype(np.float32) / 255
big = cv2.resize(1 - g, (g.shape[1] * S, g.shape[0] * S), interpolation=cv2.INTER_CUBIC)
big = cv2.GaussianBlur(big, (0, 0), 1.6)
m = (big > .5).astype(np.uint8)
if R:
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * R * S + 1, 2 * R * S + 1))
    ab = cv2.morphologyEx(m, cv2.MORPH_OPEN, k)
    # faixa de transição suave entre o original e o alisado
    y = np.arange(m.shape[0])[:, None] / S
    w = np.clip((y - 300) / 30, 0, 1) * np.clip((745 - y) / 10, 0, 1)
    m = ((ab * w + m * (1 - w)) > .5).astype(np.uint8)
    # o alisado não cria tinta nova, mas pode soltar fiapos: fica só o maior pedaço + as unhas
n, lab, st, _ = cv2.connectedComponentsWithStats(m)
keep = np.zeros_like(m, bool)
for i in range(1, n):
    if st[i][4] > 200 * S * S: keep |= lab == i
plist = potrace.Bitmap(~keep).trace(turdsize=30, alphamax=1.0, opticurve=True, opttolerance=0.2)
f = lambda p: f'{p.x / S:.2f} {p.y / S:.2f}'
partes = []
for c in plist:
    d = [f'M{f(c.start_point)}']
    for s in c.segments:
        d.append(f'L{f(s.c)} L{f(s.end_point)}' if s.is_corner else f'C{f(s.c1)} {f(s.c2)} {f(s.end_point)}')
    partes.append(' '.join(d) + 'Z')
open(f'gato-v3/gato-r{R}.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill-rule="evenodd" d="{" ".join(partes)}"/></svg>')
print('R', R, 'curvas', len(plist))
