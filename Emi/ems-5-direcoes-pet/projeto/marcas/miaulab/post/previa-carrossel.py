# MIAU.LAB · prévia do carrossel: tira com as 8 lâminas e vídeo simulando o arrasto no feed.
# uso: previa-carrossel.py  (lê carrossel/ e quadros/, grava carrossel/previa-tira.jpg e carrossel/previa-arrasto.mp4)
import subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
C = 'carrossel/'
def ab(p): return Image.open(p).convert('RGB')
anim = {1: [ab('quadros/t1-%d.png' % i) for i in range(3)], 4: [ab('quadros/t4-%d.png' % i) for i in range(2)]}
fixa = {2: ab(C+'02.png'), 3: ab(C+'03.png'), 5: ab(C+'05-06-a.png'), 6: ab(C+'05-06-b.png'), 7: ab(C+'07.png'), 8: ab(C+'08.png')}
def quadro(n, t):  # lâmina n no tempo t (s); animadas trocam a cada 0,5 s
    if n in anim: return anim[n][int(t / .5) % len(anim[n])]
    return fixa[n]
# 1) tira
w, h, g = 360, 450, 12
tira = Image.new('RGB', (8 * w + 7 * g + 2 * 40, h + 2 * 40 + 36), (246, 241, 232))
d = ImageDraw.Draw(tira)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 18)
except: f = None
for i in range(8):
    n = i + 1; x = 40 + i * (w + g)
    tira.paste(quadro(n, 0).resize((w, h), Image.LANCZOS), (x, 40))
    rot = '%02d' % n + (' · animada' if n in anim else '') + (' · conecta' if n in (5, 6) else '')
    d.text((x, 40 + h + 10), rot, fill=(30, 30, 30), font=f)
tira.save(C + 'previa-tira.jpg', quality=90)
# 2) vídeo do arrasto: 1,6 s parada em cada lâmina + 0,4 s de arrasto com easing
W, H, fps = 720, 900, 30
para, arr = 1.6, .4
def ease(u): return u * u * (3 - 2 * u)
cache = {}
def img(n, t):
    k = (n, int(t / .5) % 3 if n in anim else 0)
    if k not in cache: cache[k] = np.asarray(quadro(n, t).resize((W, H), Image.LANCZOS))
    return cache[k]
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(fps), '-i', '-',
                      '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', C + 'previa-arrasto.mp4'], stdin=subprocess.PIPE)
T = 8 * para + 7 * arr + .6; t = 0
while t < T:
    seg = para + arr; i = min(int(t // seg), 7); r = t - i * seg
    if i < 7 and r > para:
        u = ease((r - para) / arr); dx = int(u * W)
        fr = np.concatenate([img(i + 1, t), img(i + 2, t)], 1)[:, dx:dx + W]
    else:
        fr = img(i + 1, t)
    p.stdin.write(np.ascontiguousarray(fr).tobytes()); t += 1 / fps
p.stdin.close(); p.wait()
print('ok')
