# Recorta os objetos 3D gerados (fundo #E9E9E9) e apara a sobra transparente.
import sys, os
from rembg import remove, new_session
from PIL import Image
import numpy as np
src, dst = sys.argv[1], sys.argv[2]
s = new_session(sys.argv[3] if len(sys.argv) > 3 else 'birefnet-general')
for f in sorted(os.listdir(src)):
    im = Image.open(os.path.join(src, f)).convert('RGB')
    out = remove(im, session=s)
    a = np.array(out); al = a[..., 3].astype(float)
    al = np.clip((al - 40) / (215 - 40), 0, 1) * 255  # borda firme, sem halo cinza
    a[..., 3] = al.astype('uint8'); out = Image.fromarray(a)
    out = out.crop(out.getbbox()); out.save(os.path.join(dst, f)); print(f, out.size)
