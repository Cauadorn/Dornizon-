# Maison Caramelo · relevo seco tom sobre tom (como a referência 3): o logo prensado num papel/couro vinho.
# mascara = logo.html renderizado preto no branco em 2x; o relevo vem do campo de altura (máscara desfocada),
# luz de cima à esquerda (brilho na borda de cima, sombra embaixo à direita), papel com fibra e grão.
# uso: relevo.py <mascara_2x.png> <saida.jpg> [cor_base=#4A1D22] [forca=1] [textura=1]
import sys, numpy as np, cv2
from PIL import Image
mk, saida = sys.argv[1], sys.argv[2]
base = sys.argv[3] if len(sys.argv) > 3 else '#4A1D22'; forca = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
tex = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0   # intensidade da textura do papel (papel claro pede menos)
m = 1 - np.asarray(Image.open(mk).convert('L')).astype(np.float32) / 255     # 1 = tinta
H, W = m.shape
rng = np.random.default_rng(7)
# papel: ondulação larga + fibra média + grão fino
def ruido(sig, amp):
    n = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), sig); return n / (n.std() + 1e-6) * amp
papel = ruido(60, .014) + ruido(6, .02) + ruido(1.2, .03)   # papel de feltro: pouca mancha, fibra fina
fibra = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), sigmaX=9, sigmaY=1.2); fibra = fibra / fibra.std() * .015
# altura do relevo: linhas sobem, com borda arredondada
alt = cv2.GaussianBlur(m, (0, 0), 2.2) * 1.0 + cv2.GaussianBlur(m, (0, 0), 6) * .25
gy, gx = np.gradient(alt)
luz = (-gx * .75 - gy * 1.0) * 9 * forca                 # positivo nas bordas viradas para a luz
c = np.array([int(base[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255
# dentro da linha o papel fica um pouco mais escuro (pressão) e acetinado
dentro = cv2.GaussianBlur(m, (0, 0), 1.0)
tom = 1 + (papel + fibra) * tex + np.clip(luz, -.35, .45) - dentro * .06 * forca
out = c[None, None, :] * tom[..., None]
# vinheta suave de luz (de cima à esquerda)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
vin = 1.06 - .14 * ((xx / W) * .5 + (yy / H) * .8)
out = np.clip(out * vin[..., None], 0, 1)
im = Image.fromarray((out * 255).astype(np.uint8)).resize((W // 2, H // 2), Image.LANCZOS)
im.save(saida, quality=94); print('ok', saida, im.size)
