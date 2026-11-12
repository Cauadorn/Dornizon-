# Prepara as texturas do case como "mapas" em cinza neutro (média 128) para usar em overlay/soft-light:
# assim elas marcam a matéria (dobra, trama, grão, retícula) sem lavar a cor do fundo.
# uso: python3 -I texturas/preparar.py   (rodar dentro de case/)
import numpy as np, cv2
from PIL import Image
W, H = 1080, 1350
def mapa(src, dst, desvio, crop=None, gira=False):
    im = Image.open(src).convert('L')
    if gira: im = im.rotate(90, expand=True)
    s = max(W / im.width, H / im.height) * (crop or 1)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    a = np.asarray(im.crop((x, y, x + W, y + H))).astype(np.float32)
    a = (a - a.mean()) / (a.std() + 1e-6) * desvio + 128
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(dst); print('ok', dst)
mapa('texturas/papel-amassado.jpg', 'texturas/m-papel-amassado.png', 34)
mapa('texturas/linho-canvas.jpg', 'texturas/m-linho.png', 30, crop=1.0, gira=True)
mapa('texturas/grao.jpg', 'texturas/m-grao.png', 38)
# meio-tom orgânico: pontos que crescem e somem seguindo um campo suave
rng = np.random.default_rng(4)
campo = cv2.GaussianBlur(rng.random((H // 4, W // 4)).astype(np.float32), (0, 0), 18)
campo = (campo - campo.min()) / (campo.max() - campo.min())
campo = cv2.resize(campo, (W, H))
img = Image.new('L', (W * 2, H * 2), 255); from PIL import ImageDraw; d = ImageDraw.Draw(img)
passo = 12
for y in range(0, H, passo):
    for x in range(0, W, passo):
        r = passo * .55 * campo[y, x] ** 1.6
        if r > .5: d.ellipse([(x - r) * 2, (y - r) * 2, (x + r) * 2, (y + r) * 2], fill=0)
img.resize((W, H), Image.LANCZOS).save('texturas/m-meiotom.png'); print('ok meio-tom')
