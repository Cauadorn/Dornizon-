# Vetoriza uma área de uma imagem chapada (tinta cobalto sobre creme) em SVG com curvas.
# uso: python3 -I vetorizar.py <imagem> <x0,y0,x1,y1> <saida.svg> [escala]
import sys
import numpy as np
from PIL import Image, ImageFilter
import potrace

img, caixa, saida = sys.argv[1], sys.argv[2], sys.argv[3]
esc = int(sys.argv[4]) if len(sys.argv) > 4 else 6
x0, y0, x1, y1 = map(int, caixa.split(','))
FUNDO = [244., 236., 219.]
TINTA = [20., 45., 181.]
im = Image.open(img).convert('RGB').crop((x0, y0, x1, y1)).filter(ImageFilter.MedianFilter(3))
im = im.resize((im.width * esc, im.height * esc), Image.LANCZOS)
a = np.asarray(im).astype(float)
# distância até o creme do fundo -> tinta
fundo = np.array(FUNDO)
tinta = np.array(TINTA)
t = ((a - fundo) @ (tinta - fundo)) / ((tinta - fundo) @ (tinta - fundo))
m = Image.fromarray((np.clip(t, 0, 1) * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(esc * 1.1))
bits = np.asarray(m) <= 128  # potracer traça o lado False como forma
bmp = potrace.Bitmap(bits)
path = bmp.trace(turdsize=int(4 * esc * esc), alphamax=1.3, opticurve=True, opttolerance=1.6)
parts = []
for curve in path:
    s = curve.start_point
    d = [f'M{s.x:.1f} {s.y:.1f}']
    for seg in curve.segments:
        if seg.is_corner:
            d.append(f'L{seg.c.x:.1f} {seg.c.y:.1f}L{seg.end_point.x:.1f} {seg.end_point.y:.1f}')
        else:
            d.append(f'C{seg.c1.x:.1f} {seg.c1.y:.1f} {seg.c2.x:.1f} {seg.c2.y:.1f} {seg.end_point.x:.1f} {seg.end_point.y:.1f}')
    parts.append(''.join(d) + 'Z')
W, H = bits.shape[1], bits.shape[0]
open(saida, 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><path fill="#2742C2" fill-rule="evenodd" d="{"".join(parts)}"/></svg>')
print('ok', saida, W, H, len(parts), 'contornos')
