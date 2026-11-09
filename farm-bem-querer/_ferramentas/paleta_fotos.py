"""Extrai a paleta de um estado a partir das fotos reais escolhidas.
Para cada foto: cores dominantes (median cut). Depois junta tudo e escolhe N cores distintas,
priorizando as que tem presenca e personalidade (saturacao), sem perder um claro e um escuro."""
import colorsys
import json
import sys

import numpy as np
from PIL import Image


def dominantes(path, k=6):
    im = Image.open(path).convert('RGB')
    im.thumbnail((240, 240))
    q = im.quantize(colors=k, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:k * 3]
    counts = sorted(q.getcolors(), reverse=True)
    out = []
    total = sum(c for c, _ in counts)
    for c, idx in counts:
        rgb = tuple(pal[idx * 3: idx * 3 + 3])
        out.append((c / total, rgb))
    return out


def dist(a, b):
    return np.linalg.norm(np.array(a, float) - np.array(b, float))


def escolher(fotos, n=6):
    cand = []
    for f in fotos:
        for peso, rgb in dominantes(f):
            h, l, s = colorsys.rgb_to_hls(*(v / 255 for v in rgb))
            cand.append({'rgb': rgb, 'peso': peso, 's': s, 'l': l, 'foto': f})
    # nota: presenca + saturacao (cor com personalidade)
    for c in cand:
        c['nota'] = c['peso'] * 0.6 + c['s'] * 0.5 * (1 - abs(c['l'] - 0.5))
    cand.sort(key=lambda c: -c['nota'])
    escolhidas = []
    for c in cand:
        if all(dist(c['rgb'], e['rgb']) > 70 for e in escolhidas):
            escolhidas.append(c)
        if len(escolhidas) >= n - 2:
            break
    # garante um claro (papel/cal) e um escuro (sombra/terra)
    claros = sorted(cand, key=lambda c: -c['l'] + (0.3 if c['s'] > 0.5 else 0))
    escuros = sorted(cand, key=lambda c: c['l'])
    for pool in (claros, escuros):
        for c in pool:
            if all(dist(c['rgb'], e['rgb']) > 60 for e in escolhidas):
                escolhidas.append(c)
                break
    return ['#%02X%02X%02X' % c['rgb'] for c in escolhidas], [c['foto'] for c in escolhidas]


if __name__ == '__main__':
    fotos = sys.argv[1:]
    cores, origem = escolher(fotos)
    print(json.dumps({'cores': cores, 'origem': origem}, ensure_ascii=False))
