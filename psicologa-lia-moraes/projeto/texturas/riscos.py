# Riscos e poeira de filme (PNG transparente 1080x1350) para sobrepor nas fotos.
# uso: python3 -I texturas/riscos.py <semente> <saida>
import sys, math, random
from PIL import Image, ImageDraw, ImageFilter
seed, dst = int(sys.argv[1]), sys.argv[2]
r = random.Random(seed)
W, H, K = 1080, 1350, 2
im = Image.new('RGBA', (W * K, H * K), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
def curva(x, y, comp, ang, curv, larg, alfa):
    pts = []
    for i in range(24):
        t = i / 23
        a = ang + curv * (t - .5)
        pts.append((x + math.cos(a) * comp * t * K, y + math.sin(a) * comp * t * K + math.sin(t * math.pi) * curv * 30 * K))
    d.line(pts, fill=(255, 250, 242, alfa), width=max(1, int(larg * K)), joint='curve')
# riscos curtos (tipo fio/poeira grande)
for _ in range(26):
    curva(r.uniform(0, W * K), r.uniform(0, H * K), r.uniform(25, 120), r.uniform(-.6, .6) + (r.random() < .5) * math.pi / 2,
          r.uniform(-.9, .9), r.uniform(.8, 1.6), r.randint(90, 190))
# fios de cabelo/fibra mais longos
for _ in range(4):
    curva(r.uniform(0, W * K), r.uniform(0, H * K), r.uniform(140, 260), r.uniform(0, math.pi), r.uniform(-2, 2), 1, r.randint(70, 130))
# riscos verticais finos de película
for _ in range(3):
    x = r.uniform(.05, .95) * W * K; y0 = r.uniform(0, .5) * H * K
    d.line([(x, y0), (x + r.uniform(-6, 6) * K, y0 + r.uniform(.3, .7) * H * K)], fill=(255, 250, 242, r.randint(40, 80)), width=1)
# pontinhos de poeira
for _ in range(220):
    x, y = r.uniform(0, W * K), r.uniform(0, H * K); s = r.choice([1, 1, 1, 1.5, 2, 3]) * K / 2
    c = (255, 250, 242, r.randint(80, 200)) if r.random() < .8 else (20, 18, 30, r.randint(60, 140))
    d.ellipse([x - s, y - s, x + s, y + s], fill=c)
im = im.filter(ImageFilter.GaussianBlur(.6)).resize((W, H), Image.LANCZOS)
im.save(dst); print('ok', dst)
