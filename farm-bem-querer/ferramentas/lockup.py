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


def empilhado(estado, ink, heart_c):
    W = 1000
    hav, hh = _hav(60, 30, 880, ink)
    y = 30 + hh + 34
    hrt = L.heart(W / 2, y + 48, 104, -6)
    y += 104 + 30
    farm, fh = _farm_img(W / 2 - 370, y, 740, ink, 'fi' + ink.strip('#'))
    y += fh + 52
    # fio + linha da capsula
    rule = f'<rect x="{W / 2 - 60}" y="{y}" width="120" height="4" fill="{ink}"/>'
    y += 30
    cap = 'bem-querer'
    s1 = 84
    w1 = L.MED.width(cap, s1)
    st = estado.upper()
    s2 = 38
    w2 = L.SEMI.width(st, s2, 0.2)
    y1 = y + s1 * 0.8
    d = L.MED.line(cap, s1, W / 2 - w1 / 2, y1) + ' ' + L.SEMI.line(st, s2, W / 2 - w2 / 2, y1 + 70, 0.2)
    H = y1 + 70 + 24
    body = (f'{hav}<g fill="{heart_c}">{hrt}</g>{farm}{rule}<path fill="{ink}" d="{d}"/>')
    return W, round(H), body


def horizontal(estado, ink, heart_c):
    H = 200
    hav, hh = _hav(20, (H - 32 * 4.2) / 2, 149 * 4.2, ink)
    x = 20 + 149 * 4.2 + 40
    hrt = L.heart(x + 42, H / 2 + 2, 84, -6)
    x += 84 + 40
    farm, fh = _farm_img(x, (H - 600 * FARM_H / FARM_W) / 2, 600, ink, 'fh' + ink.strip('#'))
    x += 600 + 50
    bar = f'<rect x="{x}" y="40" width="4" height="{H - 80}" fill="{ink}"/>'
    x += 50
    cap = 'bem-querer'
    s1 = 68
    d = L.MED.line(cap, s1, x, H / 2 + 4)
    st = estado.upper()
    d += ' ' + L.SEMI.line(st, 30, x + 4, H / 2 + 52, 0.2)
    W = x + max(L.MED.width(cap, s1), L.SEMI.width(st, 30, 0.2)) + 30
    body = f'{hav}<g fill="{heart_c}">{hrt}</g>{farm}{bar}<path fill="{ink}" d="{d}"/>'
    return round(W), H, body


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
