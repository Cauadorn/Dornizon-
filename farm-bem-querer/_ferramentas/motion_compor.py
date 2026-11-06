"""Junta o bloco parado + os motions recortados no arco + os chinelos por cima, em MP4.
Antes: node motion_camadas.js ...  (gera base-NN.png, topo-NN.png e mapa.json)
Uso:   python3 -I motion_compor.py <pasta-camadas> <pasta-videos> <prefixo> [voltas] [largura-final]
  ex.: python3 -I motion_compor.py ../07-apresentacao/instagram/_camadas ../07-apresentacao/instagram/videos bem-querer 3"""
import json
import math
import os
import subprocess
import sys

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
VID = os.path.join(AQUI, '..', '07-apresentacao', 'site', 'video')
TMP, OUT, PREF = sys.argv[1], sys.argv[2], sys.argv[3]
VOLTAS = int(sys.argv[4]) if len(sys.argv) > 4 else 3
LARG = int(sys.argv[5]) if len(sys.argv) > 5 else 0
SW, SH = 720, 964  # tamanho dos motions
os.makedirs(OUT, exist_ok=True)


def duracao(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).decode())


def mascara(w, h, raio, nome):
    k = 4
    r = min(raio, w / 2) * k
    im = Image.new('L', (w * k, h * k), 0)
    d = ImageDraw.Draw(im)
    d.rectangle([0, r, w * k, h * k], fill=255)
    d.rounded_rectangle([0, 0, w * k - 1, 2 * r], radius=r, fill=255)
    im.resize((w, h), Image.LANCZOS).save(nome)


mapa = json.load(open(os.path.join(TMP, 'mapa.json')))
for nn, arcos in mapa.items():
    ent = ['-loop', '1', '-framerate', '24', '-i', os.path.join(TMP, f'base-{nn}.png')]
    filtros, ult = [], '0:v'
    dur = min(duracao(os.path.join(VID, a['uf'] + '.mp4')) for a in arcos) * VOLTAS
    for i, a in enumerate(arcos):
        x, y = round(a['x']), round(a['y'])
        w, h = round(a['w']), round(a['h'])
        f = max(w / SW, h / SH)
        sw, sh = math.ceil(SW * f / 2) * 2, math.ceil(SH * f / 2) * 2
        px, py = [float(v.strip('%')) / 100 for v in a['pos'].split()[:2]]
        cx, cy = round((sw - w) * px), round((sh - h) * py)
        m = os.path.join(TMP, f'mask-{nn}-{i}.png')
        mascara(w, h, a['raio'], m)
        iv = 1 + 2 * i
        ent += ['-stream_loop', str(VOLTAS), '-i', os.path.join(VID, a['uf'] + '.mp4'), '-loop', '1', '-framerate', '24', '-i', m]
        filtros.append(f'[{iv}:v]fps=24,scale={sw}:{sh}:flags=lanczos,crop={w}:{h}:{cx}:{cy},format=rgba[v{i}]')
        filtros.append(f'[{iv + 1}:v]format=gray[m{i}]')
        filtros.append(f'[v{i}][m{i}]alphamerge[a{i}]')
        filtros.append(f'[{ult}][a{i}]overlay={x}:{y}[o{i}]')
        ult = f'o{i}'
    it = 1 + 2 * len(arcos)
    ent += ['-loop', '1', '-framerate', '24', '-i', os.path.join(TMP, f'topo-{nn}.png')]
    fim = f'scale={LARG}:-2:flags=lanczos,' if LARG else 'crop=trunc(iw/2)*2:trunc(ih/2)*2,'
    filtros.append(f'[{ult}][{it}:v]overlay=0:0,{fim}format=yuv420p[fim]')
    saida = os.path.join(OUT, f'{PREF}-{nn}.mp4')
    cmd = ['ffmpeg', '-y', '-v', 'error'] + ent + ['-filter_complex', ';'.join(filtros), '-map', '[fim]', '-t', f'{dur:.3f}',
                                                   '-c:v', 'libx264', '-profile:v', 'high', '-crf', '17', '-preset', 'slow', '-r', '24',
                                                   '-movflags', '+faststart', saida]
    subprocess.run(cmd, check=True)
    print(os.path.basename(saida), f'{dur:.1f}s', round(os.path.getsize(saida) / 1e6, 1), 'MB')
