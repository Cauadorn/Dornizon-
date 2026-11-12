# Corta as fotos do Pinterest em 1080x1350 (4:5) com o enquadramento de cada lâmina.
# (cx, cy) = centro do recorte em fração da foto; w = largura do recorte em fração da largura da foto.
import os
from PIL import Image
AQUI = os.path.dirname(os.path.abspath(__file__))
CORTES = {
    'cadeira-morro':       (0.52, 0.715, 0.74),
    'mulher-morro-ceu':    (0.478, 0.4835, 0.46),
    'mesinha-caderno':     (0.50, 0.62, 1.00),
    'trem-janela-escura':  (0.50, 0.40, 1.00),
    'janela-cama-azul':    (0.42, 0.50, 0.80),
    'mar-ondas':           (0.50, 0.50, 1.00),
    'mar-mulher-agua':     (0.50, 0.42, 1.00),
    'poltrona-azul-trigo': (0.50, 0.50, 1.00),
    'janela-lua':          (0.50, 0.50, 1.00),
    'mulher-campo-azul':   (0.50, 0.50, 1.00),
    'mesinha-cha':         (0.50, 0.64, 1.00),
    'janela-cortina-azul': (0.50, 0.50, 1.00),
    'mulher-campo-ceu':    (0.50, 0.55, 1.00),
    'cadeira-campo-vasto': (0.50, 0.56, 1.00),
}
for nome, (cx, cy, wf) in CORTES.items():
    im = Image.open(os.path.join(AQUI, nome + '.jpg')).convert('RGB')
    W, H = im.size
    w = W * wf; h = w * 1.25
    if h > H: h = H; w = h * 0.8
    x0 = min(max(cx * W - w / 2, 0), W - w); y0 = min(max(cy * H - h / 2, 0), H - h)
    im.crop((round(x0), round(y0), round(x0 + w), round(y0 + h))).resize((1080, 1350), Image.LANCZOS).save(os.path.join(AQUI, 'base', nome + '.jpg'), quality=94)
    print(nome, 'escala', round(1080 / w, 2))
