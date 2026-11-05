"""Gera as duas versoes de cada arte: SEM logo (limpa) e COM logo (assinatura V2).

Uso: python compor.py arte.png UF saida_dir [--pos base|topo|canto] [--largura 0.30]
A cor da assinatura (clara/escura) e escolhida pela luminancia da area onde ela cai.
"""
import argparse
import os
import shutil
import subprocess
import tempfile

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
LOGOS = '/home/user/Dornizon-/farm-bem-querer/03-marca/assinatura-v2'


def rasterizar(svg_path, largura_px, out_png):
    subprocess.run(['node', os.path.join(HERE, 'svg_raster.js'), svg_path, str(largura_px), out_png], check=True)
    return Image.open(out_png).convert('RGBA')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('arte')
    ap.add_argument('uf')
    ap.add_argument('saida')
    ap.add_argument('--pos', default='base', choices=['base', 'topo', 'canto', 'faixa'])
    ap.add_argument('--forma', default='empilhado', choices=['empilhado', 'horizontal'])
    ap.add_argument('--faixa', type=float, default=0.13, help='altura da faixa de base (fração da altura)')
    ap.add_argument('--largura', type=float, default=0.30)
    ap.add_argument('--tom', default='auto', choices=['auto', 'claro', 'escuro'])
    ap.add_argument('--ink', default=None, help='cor da assinatura (#hex); padrão: off-white ou quase preto pelo tom')
    a = ap.parse_args()
    uf = a.uf.lower()
    os.makedirs(a.saida, exist_ok=True)
    arte = Image.open(a.arte).convert('RGBA')
    W, H = arte.size
    base = os.path.splitext(os.path.basename(a.arte))[0]

    lw = int(W * a.largura)
    margem = int(W * 0.06)
    # area provavel onde a assinatura cai (estimativa p/ escolher o tom)
    est_h = int(lw * 0.47)
    if a.pos == 'faixa':
        fh = int(H * a.faixa)
        x, y = (W - lw) // 2, H - fh + (fh - est_h) // 2
    elif a.pos == 'base':
        x, y = (W - lw) // 2, H - margem - est_h
    elif a.pos == 'topo':
        x, y = (W - lw) // 2, margem
    else:
        x, y = W - margem - lw, H - margem - est_h
    regiao = np.asarray(arte.convert('L').crop((x, y, x + lw, y + est_h)), dtype=np.float32)
    tom = a.tom if a.tom != 'auto' else ('claro' if regiao.mean() < 140 else 'escuro')

    # assinatura oficial da collab (FARM RIO / coração / havaianas), a mesma do chinelo
    import importlib.util
    spec = importlib.util.spec_from_file_location('ac', os.path.join(HERE, 'assinatura_collab.py'))
    ac = importlib.util.module_from_spec(spec); spec.loader.exec_module(ac)
    ink = a.ink or ('#FFFDF7' if tom == 'claro' else '#1E1A17')
    with tempfile.TemporaryDirectory() as td:
        svg = os.path.join(td, 'l.svg')
        ww, hh_, body = ac.collab(ink)
        open(svg, 'w').write(ac.K.svg(ww, hh_, body))
        logo = rasterizar(svg, lw, os.path.join(td, 'l.png'))
    if a.pos == 'faixa':
        y = H - fh + (fh - logo.height) // 2
    elif a.pos == 'base':
        y = H - margem - logo.height
    elif a.pos == 'canto':
        y = H - margem - logo.height
    com = arte.copy()
    # sombra suave so quando o fundo e muito movimentado (desvio alto)
    if regiao.std() > 55:
        sombra = Image.new('RGBA', logo.size, (0, 0, 0, 0))
        alpha = logo.split()[3].point(lambda v: int(v * 0.35))
        sombra.putalpha(alpha)
        from PIL import ImageFilter
        sombra = sombra.filter(ImageFilter.GaussianBlur(6))
        com.alpha_composite(sombra, (x + 2, y + 3))
    com.alpha_composite(logo, (x, y))

    sem_p = os.path.join(a.saida, f'{base}__sem-logo.png')
    com_p = os.path.join(a.saida, f'{base}__com-logo.png')
    if os.path.abspath(a.arte) != os.path.abspath(sem_p):
        shutil.copyfile(a.arte, sem_p)
    com.convert('RGB').save(com_p, optimize=True)
    print('ok', tom, sem_p, com_p)


if __name__ == '__main__':
    main()
