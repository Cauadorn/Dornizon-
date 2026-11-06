"""Acabamento de um motion: recorta o 9:16 de volta para o 3:4 da ilustração, cola por cima a faixa da
assinatura (parada e nítida, tirada da versão com logo) e fecha o loop sem pulo.
Uso: python3 -I motion_finaliza.py bruto.mp4 <pasta-do-estado> <uf> [crossfade|pingpong]
Grava 07-apresentacao/site/video/<uf>.mp4 (720 x 964, H.264, sem áudio) e um quadro de conferência ao lado."""
import glob
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(AQUI)
bruto, pasta, uf = sys.argv[1], sys.argv[2], sys.argv[3]
modo = sys.argv[4] if len(sys.argv) > 4 else 'crossfade'
sem = glob.glob(os.path.join(P, '05-estampas', pasta, '*__sem-logo.png'))[0]
com = sem.replace('__sem-logo', '__com-logo')
SAIDA = os.path.join(P, '07-apresentacao', 'site', 'video')
os.makedirs(SAIDA, exist_ok=True)

ilu = np.asarray(Image.open(sem).convert('RGB'), np.float32)
H0, W0 = ilu.shape[:2]
y = H0 - 1
while y > 0 and ilu[y].std(axis=0).mean() < 6:
    y -= 1
faixa_y = y + 1                      # onde começa a faixa da assinatura (px da ilustração)

# geometria do vídeo bruto
info = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,duration',
                       '-of', 'csv=p=0', bruto], capture_output=True, text=True).stdout.strip().split(',')
vw, vh, dur = int(info[0]), int(info[1]), float(info[2])
H9 = round(W0 * 16 / 9)
pad = (H9 - H0) // 2
esc = vw / W0
cy, ch = round(pad * esc / 2) * 2, round(H0 * esc / 2) * 2   # recorte do 3:4 dentro do 9:16
OW, OH = vw, ch

with tempfile.TemporaryDirectory() as td:
    # faixa com o logo, na escala do vídeo
    faixa = Image.open(com).convert('RGB').crop((0, faixa_y, W0, H0))
    fh = round((H0 - faixa_y) * OW / W0)
    faixa = faixa.resize((OW, fh), Image.LANCZOS)
    fp = os.path.join(td, 'faixa.png')
    faixa.save(fp)
    base = f'[0:v]crop={vw}:{ch}:0:{cy},setsar=1[c];[c][1:v]overlay=0:{OH - fh}[o]'
    meio = os.path.join(td, 'meio.mp4')
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', bruto, '-i', fp, '-filter_complex', base, '-map', '[o]', '-an',
                    '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', meio], check=True)
    final = os.path.join(SAIDA, f'{uf}.mp4')
    if modo == 'pingpong':
        filtro = '[0:v]split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1[o]'
    else:
        # os últimos 0,8 s se fundem no primeiro quadro: o fim volta para o começo sem pulo
        xf = 0.8
        filtro = (f'[0:v]split[a][b];[b]trim=0:{xf},setpts=PTS-STARTPTS[ini];'
                  f'[a]trim={xf}:{dur:.3f},setpts=PTS-STARTPTS[resto];'
                  f'[resto][ini]xfade=transition=fade:duration={xf}:offset={dur - 2 * xf:.3f}[o]')
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', meio, '-filter_complex', filtro, '-map', '[o]', '-an',
                    '-c:v', 'libx264', '-crf', '22', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', final], check=True)
conf = os.path.join(SAIDA, '..', '..', 'motion-conferencia')
os.makedirs(conf, exist_ok=True)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', final, '-vf', 'select=eq(n\\,0)+eq(n\\,45)+eq(n\\,75)+eq(n\\,105),scale=360:-2,tile=4x1',
                '-frames:v', '1', os.path.join(conf, f'{uf}-quadros.jpg')], check=True)
print('ok', final, f'{OW}x{OH}', f'{os.path.getsize(final) / 1048576:.1f} MB', 'faixa', faixa_y, 'recorte y', cy)
