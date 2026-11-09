"""Cores vivas de uma foto: só pixels com saturação e luz médias, agrupados (bom para fachadas e tecidos)."""
import colorsys, sys
import numpy as np
from PIL import Image
def vivas(path, k=8, smin=0.35, lmin=0.22, lmax=0.85):
    im = Image.open(path).convert('RGB'); im.thumbnail((320, 320))
    a = np.asarray(im, dtype=np.float32).reshape(-1, 3) / 255
    mx, mn = a.max(1), a.min(1); l = (mx + mn) / 2
    s = np.where(l < 0.5, (mx - mn) / (mx + mn + 1e-6), (mx - mn) / (2 - mx - mn + 1e-6))
    sel = a[(s > smin) & (l > lmin) & (l < lmax)]
    if len(sel) < 50: return []
    side = int(np.sqrt(len(sel))); sel = sel[: side * side].reshape(side, side, 3)
    q = Image.fromarray((sel * 255).astype(np.uint8)).quantize(colors=k, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[: k * 3]; tot = side * side
    return [('#%02X%02X%02X' % tuple(pal[i*3:i*3+3]), c / tot) for c, i in sorted(q.getcolors(), reverse=True)]
for f in sys.argv[2:]:
    print(f + ': ' + '  '.join(f'{h}({p:.0%})' for h, p in vivas(sys.argv[1] + '/' + f)))
