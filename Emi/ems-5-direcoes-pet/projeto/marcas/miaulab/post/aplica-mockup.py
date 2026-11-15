# MIAU.LAB · aplica a arte plana (arte.html) num mockup de foto real (a Emi: nada com cara de IA, "usa mockups").
# A arte entra por homografia nos 4 cantos da face da embalagem e vira TINTA: multiplicação sobre o material da foto
# (a textura do kraft/papel e a luz continuam), o branco da arte some; o magenta (#FF00FF) vira tinta branca opaca que
# herda a luz da foto. Só imprime onde a máscara do material deixa (dedos e mãos por cima ficam intactos).
# uso: aplica-mockup.py base.png arte.png "x,y x,y x,y x,y" (TL TR BR BL) mascara.npy saida.png [tinta|pinta]
import sys, numpy as np, cv2
from PIL import Image
base = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(np.float32)
arte = np.asarray(Image.open(sys.argv[2]).convert('RGB')).astype(np.float32)
quad = np.float32([[float(v) for v in p.split(',')] for p in sys.argv[3].split()])
mat = np.load(sys.argv[4]).astype(np.float32)
H, W = base.shape[:2]
# magenta → máscara de tinta branca; na camada de multiplicação ele vira branco (não tinge)
mag = np.clip(1 - (np.abs(arte[..., 0] - 255) + arte[..., 1] + np.abs(arte[..., 2] - 255)) / 180, 0, 1)
tinta = arte.copy(); tinta[mag > 0] = tinta[mag > 0] * (1 - mag[mag > 0, None]) + 255 * mag[mag > 0, None]
# reduz a arte para ~1,5x o tamanho que ela vai ocupar (sem serrilhado) e deforma
lados = [np.linalg.norm(quad[1] - quad[0]), np.linalg.norm(quad[3] - quad[0])]
alvo = (int(lados[0] * 1.6), int(lados[1] * 1.6))
tinta = cv2.resize(tinta, alvo, interpolation=cv2.INTER_AREA); mag = cv2.resize(mag, alvo, interpolation=cv2.INTER_AREA)
src = np.float32([[0, 0], [alvo[0], 0], [alvo[0], alvo[1]], [0, alvo[1]]])
M = cv2.getPerspectiveTransform(src, quad)
tw = cv2.warpPerspective(tinta, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE if (len(sys.argv) > 6 and sys.argv[6] == "pinta") else cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
mw = cv2.warpPerspective(mag, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=0)
modo = sys.argv[6] if len(sys.argv) > 6 else 'tinta'
lum = base.mean(2)
if modo == 'pinta':
    # embalagem 100% na cor da arte (a Emi: "o saco vai ser bege?"): a arte é a cor; da foto só vêm a luz, as dobras e o grão
    ref = np.percentile(lum[mat > .5], 60)
    luz = (lum / ref)[..., None]
    sombra = np.clip(luz, 0, 1) ** 1.1                  # sombras e dobras escurecem a cor
    brilho = np.clip(luz - 1, 0, .18) * 255 * .5       # o que passa da referência vira brilho por cima (limitado)
    pint = tw * sombra + brilho
    out = base * (1 - mat[..., None]) + pint * mat[..., None]
else:
    # tinta impressa: multiplica (um pouco menos que 100%, tinta real não é perfeitamente opaca no kraft)
    forca = float(sys.argv[7]) if len(sys.argv) > 7 else .94
    mult = base * (tw / 255)
    out = base * (1 - mat[..., None] * forca) + mult * mat[..., None] * forca
# tinta branca opaca com a luz da foto
ref = np.percentile(lum[mat > .5], 70)
luz = np.clip(lum / ref, .55, 1.12)[..., None]
branco = np.array([241, 236, 226], np.float32) * luz
a = (mw * mat)[..., None] * .96
out = out * (1 - a) + branco * a
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(sys.argv[5], quality=95)
print('ok', W, H)
