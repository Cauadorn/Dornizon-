# Recorta os objetos gerados (fundo #E9E9E9) com rembg e endurece a borda.
import sys, numpy as np
from PIL import Image
from rembg import remove, new_session
modelo = sys.argv[1] if len(sys.argv) > 1 else 'birefnet-general'
sess = new_session(modelo)
for nome in sys.argv[2:]:
    im = Image.open(f'geradas/{nome}.png').convert('RGB')
    out = remove(im, session=sess)
    a = np.array(out)
    al = a[:, :, 3].astype(float)
    al[al < 60] = 0; al[al > 200] = 255
    a[:, :, 3] = al.astype('uint8')
    o = Image.fromarray(a); bb = o.getbbox(); o = o.crop(bb)
    o.save(f'recortes/{nome}.png'); print(nome, o.size)
