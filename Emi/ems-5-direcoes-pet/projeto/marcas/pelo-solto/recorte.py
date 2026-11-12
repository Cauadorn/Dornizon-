# Efeito "papel recortado com tesoura" (a referência que a Emi mais gostou: 20, The Barking Barber):
# pega uma forma (PNG preto no branco ou com alfa), acha os contornos e troca cada curva por cortes retos
# (approxPolyDP), com os buracos preservados. Sai um PNG com alfa na mesma escala.
# uso: recorte.py <entrada> <saida> <tolerancia_px> [escala_trabalho]
import sys, numpy as np, cv2
from PIL import Image
ent, sai, tol = sys.argv[1], sys.argv[2], float(sys.argv[3])
S = int(sys.argv[4]) if len(sys.argv) > 4 else 2
im = Image.open(ent)
if im.mode == 'RGBA': a = np.asarray(im)[..., 3] > 127
else: a = np.asarray(im.convert('L')) < 128
a = a.astype(np.uint8)
H, W = a.shape
big = cv2.resize(a, (W * S, H * S), interpolation=cv2.INTER_NEAREST)
cont, hier = cv2.findContours(big, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
out = np.zeros_like(big)
if hier is not None:
    for i, c in enumerate(cont):
        if cv2.contourArea(c) < (12 * S) ** 2: continue          # migalhas
        p = cv2.approxPolyDP(c, tol * S, True)
        cor = 0 if hier[0][i][3] >= 0 else 1                       # buraco ou forma
        cv2.fillPoly(out, [p], cor, lineType=cv2.LINE_8)
    # buracos depois das formas
    for i, c in enumerate(cont):
        if hier[0][i][3] >= 0 and cv2.contourArea(c) >= (6 * S) ** 2:
            cv2.fillPoly(out, [cv2.approxPolyDP(c, tol * S, True)], 0)
alpha = cv2.resize(out.astype(np.float32), (W, H), interpolation=cv2.INTER_AREA)
rgba = np.zeros((H, W, 4), np.uint8); rgba[..., 3] = (alpha * 255).astype(np.uint8)
Image.fromarray(rgba).save(sai); print('ok', sai)
