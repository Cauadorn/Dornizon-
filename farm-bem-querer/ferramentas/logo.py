"""Sistema de logo 'bem-querer' — texto convertido em contorno (SVG portatil)."""
import json
import math
import os
import sys

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'logo-out')
os.makedirs(OUT, exist_ok=True)


class Font:
    def __init__(self, path, axes):
        tt = instantiateVariableFont(TTFont(path), axes)
        self.gs = tt.getGlyphSet()
        self.cmap = tt.getBestCmap()
        self.upm = tt['head'].unitsPerEm
        self.hmtx = tt['hmtx']
        os2 = tt['OS/2']
        self.cap = getattr(os2, 'sCapHeight', 0.7 * self.upm) / self.upm
        self.xh = getattr(os2, 'sxHeight', 0.5 * self.upm) / self.upm

    def adv(self, ch, size, track=0.0):
        g = self.cmap.get(ord(ch))
        base = self.hmtx[g][0] if g else self.upm * 0.3
        return base * size / self.upm + track * size

    def width(self, text, size, track=0.0):
        return sum(self.adv(c, size, track) for c in text) - track * size

    def glyph(self, ch, size, x, y, rot=0.0):
        g = self.cmap.get(ord(ch))
        if not g or ch == ' ':
            return ''
        s = size / self.upm
        c, sn = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        pen = SVGPathPen(self.gs)
        self.gs[g].draw(TransformPen(pen, Transform(s * c, s * sn, s * sn, -s * c, x, y)))
        return pen.getCommands()

    def line(self, text, size, x, y, track=0.0):
        d = []
        for ch in text:
            d.append(self.glyph(ch, size, x, y))
            x += self.adv(ch, size, track)
        return ' '.join(p for p in d if p)

    def arc(self, text, size, cx, cy, r, center_deg, track=0.0, bottom=False):
        """Texto em arco. Topo: le no sentido horario, letras para fora.
        Base: le da esquerda p/ direita, letras para dentro."""
        total = self.width(text, size, track) / r  # rad
        d = []
        if not bottom:
            a = math.radians(center_deg) - total / 2
            for ch in text:
                w = self.adv(ch, size, track) / r
                x, y = cx + r * math.cos(a), cy + r * math.sin(a)
                d.append(self.glyph(ch, size, x, y, math.degrees(a) + 90))
                a += w
        else:
            a = math.radians(center_deg) + total / 2
            for ch in text:
                w = self.adv(ch, size, track) / r
                x, y = cx + r * math.cos(a), cy + r * math.sin(a)
                d.append(self.glyph(ch, size, x, y, math.degrees(a) - 90))
                a -= w
        return ' '.join(p for p in d if p)


F = os.path.join(HERE, 'fonts', 'Fraunces.ttf')
FI = os.path.join(HERE, 'fonts', 'Fraunces-Italic.ttf')
BLACK = Font(F, {'wght': 900, 'opsz': 144, 'SOFT': 100, 'WONK': 1})
SEMI = Font(F, {'wght': 650, 'opsz': 18, 'SOFT': 60, 'WONK': 0})
MED = Font(F, {'wght': 560, 'opsz': 72, 'SOFT': 100, 'WONK': 0})
ITAL = Font(FI, {'wght': 420, 'opsz': 48, 'SOFT': 100, 'WONK': 1})

# coracao desenhado a mao (levemente assimetrico), caixa ~100x92, ponta em (50,90)
HEART = ('M50.5 90 C 42 82.5, 26 71, 15.5 58 C 6 46.5, 2.5 34, 6.5 23.5 '
         'C 10.5 12.5, 21 6.5, 31.5 8 C 39.5 9.2, 45.5 14.5, 49.5 22.5 '
         'C 53.5 13.5, 60.5 6.8, 70 5.6 C 82.5 4.2, 93.5 12.5, 95.5 25.5 '
         'C 97.5 38.5, 90 50.5, 80.5 60.5 C 71 70.5, 58.5 81, 50.5 90 Z')


def heart(x, y, w, rot=0):
    s = w / 100
    return f'<path d="{HEART}" transform="translate({x:.2f} {y:.2f}) rotate({rot}) scale({s:.4f}) translate(-50 -48)"/>'


INK_FILTER = '''<filter id="tinta" x="-5%" y="-5%" width="110%" height="110%">
  <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="3.2" xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="1" seed="9" result="g"/>
  <feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -4.5 3.9" result="ga"/>
  <feComposite in="d" in2="ga" operator="in"/>
</filter>'''


def svg(w, h, body, textured=False, bg=None):
    defs = f'<defs>{INK_FILTER}</defs>' if textured else ''
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    g_open = '<g filter="url(#tinta)">' if textured else '<g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'{defs}{rect}{g_open}{body}</g></svg>')


# ---------- 1. WORDMARK ----------
def wordmark(ink, accent, size=220):
    track = -0.01
    w_bem = BLACK.width('bem', size, track)
    w_q = BLACK.width('querer', size, track)
    gap = size * 0.06
    hw = size * 0.40  # largura do coracao no lugar do hifen
    x0 = 20
    base = 20 + size * 0.98
    bem = BLACK.line('bem', size, x0, base, track)
    hx = x0 + w_bem + gap + hw / 2
    hy = base - BLACK.xh * size * 0.52
    q = BLACK.line('querer', size, hx + hw / 2 + gap, base, track)
    W = hx + hw / 2 + gap + w_q + 20
    # tagline em italico
    tag = 'um coração em cada canto do Brasil'
    ts = size * 0.20
    tw = ITAL.width(tag, ts)
    tag_d = ITAL.line(tag, ts, (W - tw) / 2, base + size * 0.42)
    H = base + size * 0.52
    body = (f'<path fill="{ink}" d="{bem} {q}"/>'
            f'<g fill="{accent}">{heart(hx, hy, hw, -8)}</g>'
            f'<path fill="{ink}" d="{tag_d}"/>')
    return W, H, body


# ---------- 2. SELO por estado ----------
def selo(state, ink, accent, paper=None):
    D = 1000
    c = D / 2
    R_out = 488
    R_in = 330
    band_size = 56
    track = 0.16
    top = SEMI.arc('FARM RIO × HAVAIANAS', band_size, c, c, R_in + 46, -90, track)
    bot_text = state.upper()
    # reduz o corpo se o nome do estado for longo
    bsize = band_size
    while SEMI.width(bot_text, bsize, track) / (R_in + 46 + SEMI.cap * bsize) > math.radians(120):
        bsize -= 2
    bot = SEMI.arc(bot_text, bsize, c, c, R_in + 46 + SEMI.cap * bsize, 90, track, bottom=True)
    # centro: bem / querer empilhado + coracao
    s1 = 168
    l1 = BLACK.width('bem', s1, -0.01)
    l2 = BLACK.width('querer', s1, -0.01)
    y1 = c - 14
    y2 = c + 138
    bem = BLACK.line('bem', s1, c - l1 / 2 - 52, y1, -0.01)
    quer = BLACK.line('querer', s1, c - l2 / 2, y2, -0.01)
    hx = c + l1 / 2 + 24
    hy = y1 - BLACK.xh * s1 * 0.55
    body = ''
    if paper:
        body += f'<circle cx="{c}" cy="{c}" r="{R_out}" fill="{paper}"/>'
    body += (f'<circle cx="{c}" cy="{c}" r="{R_out - 6}" fill="none" stroke="{ink}" stroke-width="12"/>'
             f'<circle cx="{c}" cy="{c}" r="{R_out - 30}" fill="none" stroke="{ink}" stroke-width="4"/>'
             f'<circle cx="{c}" cy="{c}" r="{R_in}" fill="none" stroke="{ink}" stroke-width="5"/>'
             f'<path fill="{ink}" d="{top} {bot} {bem} {quer}"/>'
             f'<g fill="{accent}">{heart(hx, hy, 118, -10)}'
             f'{heart(c - (R_in + 70), c + 4, 34, -90)}{heart(c + (R_in + 70), c + 4, 34, 90)}</g>')
    return D, D, body


# ---------- 3. MOLDURA da colecao (3:4) ----------
def moldura(state, ink, accent, W=1500, H=2000):
    m = 56
    r = 46
    sw = 7
    # lockup inferior: bem<3querer · ESTADO
    s = 84
    lock_t1 = 'bem'
    lock_t2 = 'querer'
    st = state.upper()
    ss = 36
    w1 = BLACK.width(lock_t1, s, -0.01)
    w2 = BLACK.width(lock_t2, s, -0.01)
    hw = s * 0.42
    w_st = SEMI.width(st, ss, 0.18)
    dot = 26
    total = w1 + 8 + hw + 8 + w2 + dot * 2 + w_st
    x = (W - total) / 2
    base = H - m + s * 0.30
    d = BLACK.line(lock_t1, s, x, base, -0.01)
    hx = x + w1 + 8 + hw / 2
    x2 = x + w1 + 8 + hw + 8
    d += ' ' + BLACK.line(lock_t2, s, x2, base, -0.01)
    x3 = x2 + w2 + dot * 2
    d += ' ' + SEMI.line(st, ss, x3, base - 2, 0.18)
    gap0, gap1 = x - 26, x + total + 26
    # linha com abertura embaixo, cantos arredondados
    path = (f'M {gap1:.1f} {H - m} L {W - m - r} {H - m} Q {W - m} {H - m} {W - m} {H - m - r} '
            f'L {W - m} {m + r} Q {W - m} {m} {W - m - r} {m} L {m + r} {m} Q {m} {m} {m} {m + r} '
            f'L {m} {H - m - r} Q {m} {H - m} {m + r} {H - m} L {gap0:.1f} {H - m}')
    corners = ''.join(heart(px, py, 40, rot) for px, py, rot in [
        (m + 52, m + 52, -12), (W - m - 52, m + 52, 12), (m + 52, H - m - 52, 8), (W - m - 52, H - m - 52, -8)])
    body = (f'<path d="{path}" fill="none" stroke="{ink}" stroke-width="{sw}" stroke-linecap="round"/>'
            f'<path fill="{ink}" d="{d}"/>'
            f'<circle cx="{x2 + w2 + dot}" cy="{base - s * 0.2}" r="4.5" fill="{ink}"/>'
            f'<g fill="{accent}">{heart(hx, base - BLACK.xh * s * 0.5, hw, -8)}{corners}</g>')
    return W, H, body


if __name__ == '__main__':
    states = json.load(open(os.path.join(HERE, 'estados.json')))
    W, H, b = wordmark('#2B1D16', '#D7262E')
    open(f'{OUT}/bem-querer-wordmark.svg', 'w').write(svg(round(W), round(H), b))
    open(f'{OUT}/bem-querer-wordmark-tinta.svg', 'w').write(svg(round(W), round(H), b, textured=True))
    W, H, b = wordmark('#F6F0E4', '#E8453C')
    open(f'{OUT}/capa-wordmark.svg', 'w').write(svg(round(W), round(H), b, textured=True))
    for st in states:
        uf = st['uf'].lower()
        D, _, b = selo(st['nome'], st['logo_ink'], st['logo_heart'], paper=st['logo_paper'])
        open(f'{OUT}/selo-{uf}.svg', 'w').write(svg(D, D, b))
        open(f'{OUT}/selo-{uf}-tinta.svg', 'w').write(svg(D, D, b, textured=True))
        W2, H2, b2 = moldura(st['nome'], st['logo_ink'], st['logo_heart'])
        open(f'{OUT}/moldura-{uf}.svg', 'w').write(svg(W2, H2, b2))
    print('ok', OUT)
