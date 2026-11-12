# Monta uma folha de conferência com várias imagens lado a lado (fundo cinza, transparência visível).
# uso: python3 -I folha.py <saida.jpg> <altura> <img1> <img2> ...
import sys
from PIL import Image
saida, alt = sys.argv[1], int(sys.argv[2])
ims = []
for f in sys.argv[3:]:
    im = Image.open(f).convert('RGBA')
    ims.append(im.resize((round(im.width * alt / im.height), alt)))
W = sum(i.width for i in ims) + 20 * (len(ims) + 1)
S = Image.new('RGBA', (W, alt + 40), (150, 150, 150, 255))
x = 20
for i in ims:
    S.alpha_composite(i, (x, 20)); x += i.width + 20
S.convert('RGB').save(saida, quality=85)
print('ok', S.size)
