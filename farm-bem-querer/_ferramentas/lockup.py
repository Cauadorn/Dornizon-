"""Assinatura da collab V2 no sistema da FARM: havaianas ♥ FARM RIO + linha da capsula.
Gera SVG (empilhado e horizontal) por estado. Logos oficiais apenas para mockup de portfolio."""
import base64
import io
import json
import os
import re
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import logo as L  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
HAV_D = re.search(r'<path[^>]*d="([^"]+)"', open(os.path.join(HERE, 'brand', 'havaianas.svg')).read()).group(1)
HAV_W, HAV_H = 149, 32

_farm = Image.open(os.path.join(HERE, 'brand', 'farmrio.png')).convert('RGBA')
_farm = _farm.crop(_farm.getbbox())
FARM_W, FARM_H = _farm.size
_buf = io.BytesIO()
_farm.save(_buf, 'PNG')
FARM_B64 = base64.b64encode(_buf.getvalue()).decode()


def _farm_img(x, y, w, ink, fid):
    h = w * FARM_H / FARM_W
    return (f'<filter id="{fid}"><feFlood flood-color="{ink}"/><feComposite in2="SourceAlpha" operator="in"/></filter>'
            f'<image href="data:image/png;base64,{FARM_B64}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" filter="url(#{fid})"/>'), h


def _hav(x, y, w, ink):
    s = w / HAV_W
    return f'<path fill="{ink}" transform="translate({x:.1f} {y:.1f}) scale({s:.4f})" d="{HAV_D}"/>', HAV_H * s


def _linha_capsula(estado, ink, cx, y, largura_max, size=46, track=0.24):
    a, b = 'BEM-QUERER', estado.upper()
    gap = size * 0.9
    while True:
        wa = L.JOST_M.width(a, size, track)
        wb = L.JOST_L.width(b, size, track)
        if wa + gap + wb <= largura_max or size < 20:
            break
        size -= 1
        gap = size * 0.9
    x = cx - (wa + gap + wb) / 2
    d = L.JOST_M.line(a, size, x, y, track) + ' ' + L.JOST_L.line(b, size, x + wa + gap, y, track)
    return f'<path fill="{ink}" d="{d}"/>', size


def empilhado(estado, ink, heart_c):
    W = 1000
    hav, hh = _hav(60, 30, 880, ink)
    y = 30 + hh + 34
    hrt = L.heart(W / 2, y + 48, 104, -6)
    y += 104 + 30
    farm, fh = _farm_img(W / 2 - 370, y, 740, ink, 'fi' + ink.strip('#'))
    y += fh + 56
    rule = f'<rect x="{W / 2 - 370}" y="{y}" width="740" height="2.5" fill="{ink}" opacity=".55"/>'
    y += 30 + 40
    cap, size = _linha_capsula(estado, ink, W / 2, y, 740)
    H = y + 22
    return W, round(H), f'{hav}<g fill="{heart_c}">{hrt}</g>{farm}{rule}{cap}'


def horizontal(estado, ink, heart_c):
    H = 200
    hav, hh = _hav(20, (H - 32 * 4.2) / 2, 149 * 4.2, ink)
    x = 20 + 149 * 4.2 + 40
    hrt = L.heart(x + 42, H / 2 + 2, 84, -6)
    x += 84 + 40
    farm, fh = _farm_img(x, (H - 600 * FARM_H / FARM_W) / 2, 600, ink, 'fh' + ink.strip('#'))
    x += 600 + 54
    bar = f'<rect x="{x}" y="52" width="2.5" height="{H - 104}" fill="{ink}" opacity=".55"/>'
    x += 54
    s1 = 34
    t = 0.24
    d = L.JOST_M.line('BEM-QUERER', s1, x, H / 2 - 6, t) + ' ' + L.JOST_L.line(estado.upper(), s1, x, H / 2 + 42, t)
    W = x + max(L.JOST_M.width('BEM-QUERER', s1, t), L.JOST_L.width(estado.upper(), s1, t)) + 24
    return round(W), H, f'{hav}<g fill="{heart_c}">{hrt}</g>{farm}{bar}<path fill="{ink}" d="{d}"/>'


def svg(w, h, body, textured=False):  # logos oficiais nunca recebem textura
    return L.svg(w, h, body, textured=textured)


if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    estados = json.load(open(os.path.join(HERE, 'estados.json')))
    for e in estados:
        uf = e['uf'].lower()
        for nome, fn in (('empilhado', empilhado), ('horizontal', horizontal)):
            for tom, ink, hc in (('claro', '#FFFDF7', '#FFFDF7'), ('escuro', e['logo_ink'], e['logo_heart'])):
                w, h, b = fn(e['nome'], ink, hc)
                open(f'{out}/assinatura-{uf}-{nome}-{tom}.svg', 'w').write(svg(w, h, b))
    print('ok')
