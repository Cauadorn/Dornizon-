# Logo "au! petiscaria" (direção pop de gibi), vetorial, a partir da Bagel Fat One:
# - o "u" é a boca do cachorro: a língua sai por baixo da curva;
# - o pingo do "!" vira um biscoito de osso, inclinado;
# - três traços de "latido" de gibi saem do "!";
# - "PETISCARIA" em Bungee, espaçada, embaixo.
# Saída: marcas/logo-au.svg (cores da marca) e marcas/logo-au-<cor>.svg (versões de uma cor).
# uso: <python com fonttools> marcas/gera_logo_au.py
import pathlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen

AQUI = pathlib.Path(__file__).resolve().parent
BAGEL = TTFont(AQUI.parent / 'fonts' / 'BagelFatOne-Regular.ttf')
BUNGEE = TTFont(AQUI.parent / 'fonts' / 'Bungee-Regular.ttf')

def glifo(fonte, ch):
    gs = fonte.getGlyphSet(); nome = fonte.getBestCmap()[ord(ch)]
    return gs, nome, fonte['hmtx'][nome][0], fonte['head'].unitsPerEm

def contornos(fonte, ch):
    """Lista de contornos (cada um uma lista de operações RecordingPen) e a caixa de cada um."""
    gs, nome, adv, upm = glifo(fonte, ch)
    rec = RecordingPen(); gs[nome].draw(rec)
    cs, atual = [], []
    for op, args in rec.value:
        atual.append((op, args))
        if op in ('closePath', 'endPath'): cs.append(atual); atual = []
    caixas = []
    for c in cs:
        bp = BoundsPen(gs)
        for op, args in c: getattr(bp, op)(*args)
        caixas.append(bp.bounds)
    return cs, caixas, adv, upm

def svg_de(cs, s, dx, dy):
    pen = SVGPathPen(None); t = TransformPen(pen, (s, 0, 0, -s, dx, dy))
    for c in cs:
        for op, args in c: getattr(t, op)(*args)
    return pen.getCommands()

def texto(fonte, txt, tam, x, base, track=0.0):
    gs = fonte.getGlyphSet(); cmap = fonte.getBestCmap(); upm = fonte['head'].unitsPerEm; s = tam / upm
    partes = []
    for ch in txt:
        nome = cmap[ord(ch)]; pen = SVGPathPen(gs); gs[nome].draw(TransformPen(pen, (s, 0, 0, -s, x, base)))
        partes.append(pen.getCommands()); x += fonte['hmtx'][nome][0] * s + track * tam
    return ' '.join(partes), x

def largura(fonte, txt, tam, track=0.0):
    cmap = fonte.getBestCmap(); upm = fonte['head'].unitsPerEm
    return sum(fonte['hmtx'][cmap[ord(c)]][0] * tam / upm + track * tam for c in txt) - track * tam

TAM, BASE, X0 = 230, 236, 30
s = TAM / BAGEL['head'].unitsPerEm
# a, u, ! com kerning manual (Bagel é larga: aperta)
ca, ba, adv_a, _ = contornos(BAGEL, 'a')
cu, bu, adv_u, _ = contornos(BAGEL, 'u')
ce, be, adv_e, _ = contornos(BAGEL, '!')
xa = X0
xu = xa + adv_a * s - 14
xe = xu + adv_u * s - 18
d_a = svg_de(ca, s, xa, BASE)
d_u = svg_de(cu, s, xu, BASE)
# "!": tira o pingo (o contorno mais baixo) e guarda a posição dele
i_pingo = min(range(len(ce)), key=lambda i: be[i][1])
haste = [c for i, c in enumerate(ce) if i != i_pingo]
d_e = svg_de(haste, s, xe, BASE)
px0, py0, px1, py1 = be[i_pingo]
pingo_cx, pingo_cy = xe + (px0 + px1) / 2 * s, BASE - (py0 + py1) / 2 * s
# caixa do "u" para posicionar a língua (centro da curva de baixo)
ux0, uy0, ux1, uy1 = (min(b[0] for b in bu), min(b[1] for b in bu), max(b[2] for b in bu), max(b[3] for b in bu))
u_cx, u_base = xu + (ux0 + ux1) / 2 * s, BASE - uy0 * s
# topo da haste do "!" (para os traços de latido)
hx0, hy0, hx1, hy1 = be[1 - i_pingo] if len(be) == 2 else be[0]
topo_x, topo_y = xe + hx1 * s, BASE - hy1 * s

TINTA, AMARELO, VERMELHO, AZUL, ROSA = '#1B1B1B', '#FFD23F', '#F2542D', '#2B59C3', '#FF7A93'

def logo(cor_letra, cor_lingua, cor_osso, cor_tracos, cor_sub, fundo=None):
    W, H = 640, 360
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    if fundo: p.append(f'<rect width="{W}" height="{H}" fill="{fundo}"/>')
    # língua: gota arredondada saindo de baixo do "u", com o vinco no meio; desenhada ANTES do "u" para sair de trás
    lx, ly, lw, lh = u_cx + 6, u_base - 30, 64, 92
    p.append(f'<g transform="rotate(8 {lx:.1f} {ly:.1f})">'
             f'<path d="M{lx-lw/2:.1f} {ly:.1f} V{ly+lh-lw/2:.1f} A{lw/2:.1f} {lw/2:.1f} 0 0 0 {lx+lw/2:.1f} {ly+lh-lw/2:.1f} V{ly:.1f} Z" fill="{cor_lingua}"/>'
             f'<path d="M{lx:.1f} {ly+18:.1f} V{ly+lh-30:.1f}" stroke="{cor_letra}" stroke-width="7" stroke-linecap="round" opacity=".55"/></g>')
    p.append(f'<path d="{d_a} {d_u} {d_e}" fill="{cor_letra}"/>')
    # biscoito de osso no lugar do pingo
    bx, by = pingo_cx + 4, pingo_cy + 2
    osso = (f'<g transform="translate({bx:.1f} {by:.1f}) rotate(-28)">'
            f'<rect x="-30" y="-11" width="60" height="22" rx="4"/>'
            f'<circle cx="-30" cy="-11" r="13"/><circle cx="-30" cy="11" r="13"/><circle cx="30" cy="-11" r="13"/><circle cx="30" cy="11" r="13"/></g>')
    p.append(f'<g fill="{cor_osso}">{osso}</g>')
    # traços de latido (gibi): três traços curtos saindo do alto do "!"
    tx, ty = topo_x + 16, topo_y + 6
    for ang, comp, desl in [(-38, 34, 0), (-8, 40, 10), (22, 32, 4)]:
        p.append(f'<path transform="translate({tx:.1f} {ty:.1f}) rotate({ang})" d="M{14+desl} 0 H{14+desl+comp}" stroke="{cor_tracos}" stroke-width="11" stroke-linecap="round"/>')
    # PETISCARIA
    tam_s, tr = 34, 0.26
    ls = largura(BUNGEE, 'PETISCARIA', tam_s, tr)
    larg_au = xe + adv_e * s - xa
    sx = xa + (larg_au - ls) / 2 + 6
    d_s, _ = texto(BUNGEE, 'PETISCARIA', tam_s, sx, BASE + 84, tr)
    p.append(f'<path d="{d_s}" fill="{cor_sub}"/>')
    p.append('</svg>')
    return '\n'.join(p)

(AQUI / 'logo-au.svg').write_text(logo(TINTA, VERMELHO, AMARELO, VERMELHO, TINTA))
(AQUI / 'logo-au-azul.svg').write_text(logo(TINTA, VERMELHO, AMARELO, VERMELHO, TINTA, fundo=AZUL))
(AQUI / 'logo-au-claro.svg').write_text(logo('#FFFFFF', VERMELHO, AMARELO, AMARELO, '#FFFFFF'))
(AQUI / 'logo-au-1cor.svg').write_text(logo(TINTA, TINTA, TINTA, TINTA, TINTA))
print('ok', round(pingo_cx), round(pingo_cy), round(u_cx), round(u_base), round(topo_x), round(topo_y))
