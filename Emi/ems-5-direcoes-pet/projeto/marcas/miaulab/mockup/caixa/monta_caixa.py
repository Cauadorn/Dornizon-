# Mockup MIAU.LAB · caixa de comprimidos (substitui os frascos de gotas, que a Emi achou feios).
# base-caixa.png: caixa branca gerada no Figma (gemini-3.1-flash-image), cantos medidos com zoom de 5x.
# 1) frente e lateral: a arte entra em perspectiva (homografia). Antes, a arte é reduzida com INTER_AREA para ~2x o
#    tamanho final (sem serrilhado) e a luz da foto é aplicada em linear (a lateral herda a referência da frente: fica na sombra);
# 2) topo (a aba): pintado de rosa com a luz da foto; máscara = o que não é fundo rosa acima das arestas de cima;
# 3) a cartela e os comprimidos (recorte BiRefNet, cartela-recorte.png em x=80,y=760) voltam por cima, porque ficam na frente da caixa.
import numpy as np, cv2
from PIL import Image

foto = np.asarray(Image.open('base-caixa.png').convert('RGB')).astype(np.float32) / 255
H, W = foto.shape[:2]
lum = foto.mean(2)
def lin(c): return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def srgb(l): return np.where(l <= 0.0031308, l * 12.92, 1.055 * np.clip(l, 0, None) ** (1 / 2.4) - 0.055)
def hexrgb(h): return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255
SS = 4
def mascara(poly):
    big = np.zeros((H * SS, W * SS), np.uint8)
    cv2.fillPoly(big, [np.round(np.array(poly, np.float32) * SS).astype(np.int32)], 255, lineType=cv2.LINE_AA)
    return cv2.resize(big, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255

FRENTE = [(305.5, 204), (660, 218), (658.5, 851), (310, 800)]
LADO = [(660, 218), (738, 207), (736, 820), (658.5, 851)]
mf = mascara(FRENTE)
ref = np.percentile(lum[mf > 0.95], 97)
grao = (lum - cv2.GaussianBlur(lum, (0, 0), 1.6)) * 0.7
out = foto.copy()

def aplica(arq, quad):
    global out
    arte = np.asarray(Image.open(arq).convert('RGB')).astype(np.float32) / 255
    q = np.array(quad, np.float32)
    lado_px = max(np.linalg.norm(q[1] - q[0]), np.linalg.norm(q[2] - q[3])); alto_px = max(np.linalg.norm(q[3] - q[0]), np.linalg.norm(q[2] - q[1]))
    alvo = (int(lado_px * 2), int(alto_px * 2))
    if alvo[0] < arte.shape[1]: arte = cv2.resize(arte, alvo, interpolation=cv2.INTER_AREA)
    ah, aw = arte.shape[:2]
    M = cv2.getPerspectiveTransform(np.array([[0, 0], [aw, 0], [aw, ah], [0, ah]], np.float32), q)
    w = cv2.warpPerspective(arte, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    m = mascara(quad)[..., None]
    luz = np.clip(lum / ref, 0, 1.03)[..., None] ** 2.2
    p = np.clip(srgb(lin(w) * luz) + grao[..., None], 0, 1)
    out = out * (1 - m) + p * m

aplica('caixa-frente.png', FRENTE)
aplica('caixa-lado.png', LADO)

# topo: a aba de cima, rosa
poly_topo = [(296, 170), (750, 170), (738, 207), (660, 218), (305.5, 204)]
area = mascara(poly_topo) > 0.5
nao_fundo = ((foto[..., 0] - foto[..., 1]) < 0.07) & (lum > 0.55)
mt = (area & nao_fundo).astype(np.uint8)
mt = cv2.morphologyEx(mt, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(mt)
mt = (lab == 1 + int(np.argmax(st[1:, 4]))).astype(np.float32)
mt = np.maximum(cv2.GaussianBlur(mt, (0, 0), 0.6), 0) * (1 - mascara(FRENTE)) * (1 - mascara(LADO))
rosa = hexrgb('#FF9FD2')
pt = np.clip(srgb(lin(rosa)[None, None, :] * (np.clip(lum / ref, 0, 1.03) ** 2.2)[..., None]) + grao[..., None], 0, 1)
out = out * (1 - mt[..., None]) + pt * mt[..., None]

# cartela e comprimidos por cima
c = np.asarray(Image.open('cartela-recorte.png').convert('RGBA')).astype(np.float32) / 255
x0, y0 = 80, 760; ch, cw = c.shape[:2]
a = c[..., 3:4]
out[y0:y0 + ch, x0:x0 + cw] = out[y0:y0 + ch, x0:x0 + cw] * (1 - a) + foto[y0:y0 + ch, x0:x0 + cw] * a
Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save('mockup-caixa-miaulab.jpg', quality=94)
print('ok')
