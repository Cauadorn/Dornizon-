# Recorta a pessoa das fotos (fundo transparente) para o efeito "pessoa na frente do título".
# uso: python3 -I recortar.py ia/lia-sofa-v1.png ia/lia-online-v1.png ...
import sys, os
from rembg import new_session, remove
from PIL import Image
s = new_session('isnet-general-use')
for f in sys.argv[1:]:
    im = Image.open(f).convert('RGB')
    out = remove(im, session=s, alpha_matting=True, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=12, alpha_matting_erode_size=8)
    dst = os.path.splitext(f)[0] + '-recorte.png'
    out.save(dst); print('ok', dst, out.size)
