"""Assinatura igual à da collab já existente (como impressa nas solas): FARM RIO / ♥ / havaianas.
Sem linha de cápsula e sem coração redesenhado: a V2 é uma participação dentro da collab."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lockup as K

CORACAO = 'M50 90 C21 67 5 49 8 30 C11 13 33 6 50 25 C67 6 89 13 92 30 C95 49 79 67 50 90 Z'


def collab(ink):
    W = 1000
    farm, fh = K._farm_img(120, 20, 760, ink, 'fc' + ink.strip('#'))
    y = 20 + fh + 26
    hs = 1.3
    heart = f'<path fill="{ink}" transform="translate({W / 2 - 50 * hs} {y}) scale({hs})" d="{CORACAO}"/>'
    y += 90 * hs + 22
    hav, hh = K._hav(160, y, 680, ink)
    H = y + hh + 20
    return W, round(H), farm + heart + hav


if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    cores = {'branco': '#FFFDF7', 'preto': '#1E1A17', 'azul-colonial': '#2D5686', 'sangue-de-boi': '#7C2420',
             'ocre-escuro': '#8A5A12', 'caramelo': '#9A5B2E'}
    for nome, c in cores.items():
        w, h, b = collab(c)
        open(f'{out}/assinatura-collab-{nome}.svg', 'w').write(K.svg(w, h, b))
    print('ok', list(cores))
