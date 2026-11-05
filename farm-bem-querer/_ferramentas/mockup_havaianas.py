"""Mockup no formato das fotos da collab havaianas ♥ FARM Rio (par visto de cima, fundo claro).
Usa a foto real de produto como molde: troca a estampa da palmilha pela arte do estado, recolore a tira
e aplica a assinatura V2 no calcanhar. Uso:
python mockup_havaianas.py arte.png UF cor_tira cor_borda saida.png [--tom claro|escuro]"""
import argparse
import os
import subprocess
import tempfile

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
MOLDE = os.path.join(HERE, 'molde')
LOGOS = '/home/user/Dornizon-/farm-bem-querer/03-marca/assinatura-v2'


def hex2rgb(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255


def blur(m, r):
    return np.asarray(Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)), np.float32) / 255


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('arte'); ap.add_argument('uf'); ap.add_argument('tira'); ap.add_argument('borda'); ap.add_argument('saida')
    ap.add_argument('--tom', default='auto')
    ap.add_argument('--molde', default='banana-0.jpg')
    ap.add_argument('--modo', default='posicionada', choices=['posicionada', 'rapport', 'diptico'])
    ap.add_argument('--escala', type=float, default=0.75, help='rapport: largura do módulo em relação à largura da sola')
    a = ap.parse_args()

    foto = Image.open(os.path.join(MOLDE, a.molde)).convert('RGB')
    F = np.asarray(foto, np.float32) / 255
    H, W = F.shape[:2]
    sola = np.asarray(Image.open(os.path.join(MOLDE, 'mascara-sola-bruta.png')).convert('L'), np.float32) / 255
    tira = np.asarray(Image.open(os.path.join(MOLDE, 'mascara-tira-bruta.png')).convert('L'), np.float32) / 255
    tira = blur(np.asarray(Image.fromarray((tira * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)), np.float32) / 255, 0.8)
    sola = blur(sola, 0.8)
    # palmilha impressa = sola encolhida (sobra a borda de borracha)
    palm = np.asarray(Image.fromarray((sola * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(9)), np.float32) / 255
    palm = blur(palm, 1.0)

    arte = Image.open(a.arte).convert('RGB')
    out = F.copy()
    # luz da foto: luminância muito borrada dentro da sola (tira a estampa original, fica o volume)
    lum = F.mean(2)
    luz = blur(lum * (sola > 0.5), 28) / (blur((sola > 0.5).astype(np.float32), 28) + 1e-4)
    luz = luz / (np.median(luz[sola > 0.5]) + 1e-4)
    luz = np.clip(0.88 + 0.12 * luz, 0.8, 1.08)

    borda_cor = hex2rgb(a.borda)
    cores_tira = [hex2rgb(c) for c in a.tira.split(',')]
    if len(cores_tira) == 1:
        cores_tira = cores_tira * 2
    for metade in (slice(0, W // 2), slice(W // 2, W)):
        m = np.zeros_like(sola)
        m[:, metade] = sola[:, metade]
        ys, xs = np.where(m > 0.5)
        y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
        bh, bw = y1 - y0 + 1, x1 - x0 + 1
        cam = np.zeros_like(F)
        if a.modo == 'rapport':
            tw = max(8, int(bw * a.escala))
            tile = np.asarray(arte.resize((tw, int(arte.height * tw / arte.width)), Image.LANCZOS), np.float32) / 255
            th = tile.shape[0]
            reps_y, reps_x = bh // th + 2, bw // tw + 2
            grande = np.tile(tile, (reps_y, reps_x, 1))
            # o mesmo desenho continua de um pé para o outro (como na collab)
            off = (x0 * 7) % tw
            cam[y0:y1 + 1, x0:x1 + 1] = grande[0:bh, off:off + bw]
        else:
            fonte = arte
            if a.modo == 'diptico':
                meio = arte.width // 2
                fonte = arte.crop((0, 0, meio, arte.height)) if metade.start == 0 else arte.crop((meio, 0, arte.width, arte.height))
            esc = max(bh / fonte.height, bw / fonte.width)
            rw, rh = int(fonte.width * esc) + 2, int(fonte.height * esc) + 2
            art = np.asarray(fonte.resize((rw, rh), Image.LANCZOS), np.float32) / 255
            ox = (rw - bw) // 2
            cam[y0:y1 + 1, x0:x1 + 1] = art[0:bh, ox:ox + bw]
        if False:
            esc = max(bh / arte.height, bw / arte.width)
            rw, rh = int(arte.width * esc) + 2, int(arte.height * esc) + 2
            art = np.asarray(arte.resize((rw, rh), Image.LANCZOS), np.float32) / 255
            ox = (rw - bw) // 2
            cam[y0:y1 + 1, x0:x1 + 1] = art[0:bh, ox:ox + bw]
        pm = np.zeros_like(palm)
        pm[:, metade] = palm[:, metade]
        bm = np.zeros_like(sola)
        bm[:, metade] = sola[:, metade]
        # borda de borracha
        sombra_borda = 0.82 + 0.18 * blur(pm, 3)
        out = out * (1 - bm[..., None]) + (borda_cor * sombra_borda[..., None]) * bm[..., None]
        # estampa com a luz da foto e leve escurecimento nas beiradas
        bord = 0.9 + 0.1 * blur(pm, 10)
        imp = cam * luz[..., None] * bord[..., None]
        out = out * (1 - pm[..., None]) + imp * pm[..., None]

    # assinatura no calcanhar
    tom = a.tom
    for metade in (slice(0, W // 2), slice(W // 2, W)):
        ys, xs = np.where(sola[:, metade] > 0.5)
        y1 = ys.max(); xs = xs + metade.start
        cx = (xs.min() + xs.max()) // 2
        lw = int((xs.max() - xs.min()) * 0.46)
        reg = out[y1 - int(lw * 0.9): y1 - int(lw * 0.2), cx - lw // 2: cx + lw // 2]
        t = tom if tom != 'auto' else ('claro' if reg.mean() < 0.5 else 'escuro')
        with tempfile.TemporaryDirectory() as td:
            png = os.path.join(td, 'l.png')
            subprocess.run(['node', os.path.join(HERE, 'svg_raster.js'), os.path.join(LOGOS, f'assinatura-{a.uf.lower()}-empilhado-{t}.svg'), str(lw * 2), png], check=True)
            lg = Image.open(png).convert('RGBA').resize((lw, None) if False else (lw, int(lw * Image.open(png).height / Image.open(png).width)), Image.LANCZOS)
        L = np.asarray(lg, np.float32) / 255
        lh = L.shape[0]
        yy = y1 - int(lh * 1.25)
        if a.modo == 'rapport':
            # respiro: mancha suave na cor do fundo do padrão atrás da assinatura
            fundo = np.median(np.asarray(arte.convert('RGB').resize((256, 256)), np.float32).reshape(-1, 3), axis=0) / 255
            rm = np.zeros(out.shape[:2], np.float32)
            rm[yy - int(lh * 0.25): yy + int(lh * 1.25), cx - int(lw * 0.62): cx + int(lw * 0.62)] = 1
            rm = np.clip(blur(rm, 9) * 2.2, 0, 1) * (palm > 0.4)
            out = out * (1 - rm[..., None]) + (fundo * luz[..., None]) * rm[..., None]
        al = L[..., 3:4] * 0.92
        out[yy:yy + lh, cx - lw // 2: cx - lw // 2 + lw] = out[yy:yy + lh, cx - lw // 2: cx - lw // 2 + lw] * (1 - al) + L[..., :3] * al

    # sombra da tira na palmilha + tira recolorida com o relevo original
    sh = blur(np.roll(np.roll(tira, 7, 0), 4, 1), 5) * (1 - tira) * (palm > 0.3)
    out = out * (1 - 0.32 * sh[..., None])
    lt = F.mean(2)
    ref = np.median(lt[tira > 0.6]) + 1e-4
    rel = np.clip(lt / ref, 0.55, 1.35)
    cor_map = np.zeros_like(F)
    cor_map[:, :W // 2] = cores_tira[0]
    cor_map[:, W // 2:] = cores_tira[1]
    tcol = np.clip(cor_map * rel[..., None] * 1.02, 0, 1)
    out = out * (1 - tira[..., None]) + tcol * tira[..., None]

    Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(a.saida, quality=92)
    print('ok', a.saida)


if __name__ == '__main__':
    main()
