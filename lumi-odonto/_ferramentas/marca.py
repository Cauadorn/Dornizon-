"""Lettering da Lumi Odonto (v2), desenhado do zero, sem fonte pronta.

A palavra "lumi" é uma arcada:
- o m é um molar: coroa com duas cúspides em cima, três raízes embaixo (as de fora abrem um pouco);
- o l e o i são dentes de uma raiz só: toda perna termina afinando, como raiz;
- o u não tem raiz: o u é o sorriso;
- o pingo do i é cor de gengiva.

Uso: python3 lumi-odonto/_ferramentas/marca.py   (precisa de: pip install shapely fonttools)
Saída: lumi-odonto/01-marca/svg/*.svg
"""
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from shapely.geometry import Point, Polygon, box
from shapely.ops import unary_union

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "01-marca" / "svg"

COR = {
    "esmalte": "#F6F1E6",
    "hortela": "#2E8C68",
    "menta": "#CFE8D8",
    "gengiva": "#EE7F73",
    "cafe": "#3B2A22",
}
# versão: (cor das letras, cor do pingo, fundo para o arquivo de prova)
VERSOES = {
    "hortela": (COR["hortela"], COR["gengiva"]),
    "esmalte": (COR["esmalte"], COR["gengiva"]),
    "cafe": (COR["cafe"], COR["gengiva"]),
    "branco": ("#FFFFFF", "#FFFFFF"),
}

RES = 96
W = 30  # espessura do traço
XH = 100  # altura do x (coroa)
ASC = 150  # altura do l
GAP = 24  # espaço entre letras
TIP = 13  # ponta da raiz
INICIO_RAIZ = -55  # onde a perna começa a afinar
ABRE = 7  # quanto as raízes de fora do molar abrem


def circ(x, y, r):
    return Point(x, y).buffer(r, resolution=RES)


def ret(x0, x1, y0, y1):
    return box(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))


def acima(y):
    return box(-1e4, -1e4, 1e4, y)


def abaixo(y):
    return box(-1e4, y, 1e4, 1e4)


def raiz(x0, cx, n=90):
    """Perna de largura W que afina até a linha de base e termina arredondada."""
    yfim = -TIP / 2
    esq, dir_ = [], []
    for k in range(n + 1):
        s = k / n
        e = (3 * s * s - 2 * s ** 3) ** 0.85
        y = INICIO_RAIZ + (yfim - INICIO_RAIZ) * s
        esq.append((x0 + (cx - TIP / 2 - x0) * e, y))
        dir_.append((x0 + W + (cx + TIP / 2 - x0 - W) * e, y))
    return unary_union([Polygon(esq + dir_[::-1]), circ(cx, yfim, TIP / 2)])


def haste(x, topo):
    """Haste com topo redondo que desce até virar raiz."""
    return unary_union([ret(x, x + W, topo + W / 2, INICIO_RAIZ), circ(x + W / 2, topo + W / 2, W / 2), raiz(x, x + W / 2)])


def letras():
    x = 0
    l = haste(x, -ASC)
    x += W + GAP

    # u: sorriso
    uw = 100
    fora = unary_union([ret(x, x + uw, -XH + W / 2, -uw / 2), circ(x + uw / 2, -uw / 2, uw / 2).intersection(abaixo(-uw / 2))])
    dentro = unary_union([ret(x + W, x + uw - W, -500, -uw / 2), circ(x + uw / 2, -uw / 2, uw / 2 - W).intersection(abaixo(-uw / 2))])
    u = unary_union([fora.difference(dentro), circ(x + W / 2, -XH + W / 2, W / 2), circ(x + uw - W / 2, -XH + W / 2, W / 2)])
    x += uw + GAP

    # m: molar
    vao = W
    R = (vao + 2 * W) / 2
    cy = -XH + R
    c1, c2 = x + R, x + R + vao + W
    coroa = unary_union([circ(c1, cy, R).intersection(acima(cy)), circ(c2, cy, R).intersection(acima(cy)), ret(x, x + 3 * W + 2 * vao, cy, INICIO_RAIZ)])
    vaos = unary_union([
        circ(c1, cy, vao / 2).intersection(acima(cy)), ret(x + W, x + W + vao, cy, 10),
        circ(c2, cy, vao / 2).intersection(acima(cy)), ret(x + 2 * W + vao, x + 2 * W + 2 * vao, cy, 10),
    ])
    raizes = [
        raiz(x, x + W / 2 - ABRE),
        raiz(x + W + vao, x + W + vao + W / 2),
        raiz(x + 2 * (W + vao), x + 2 * (W + vao) + W / 2 + ABRE),
    ]
    m = unary_union([coroa.difference(vaos)] + raizes)
    xm = x
    x += 3 * W + 2 * vao + GAP

    i = haste(x, -XH)
    pingo = (x + W / 2, -XH - 30, 16.5)
    largura = x + W
    return {"l": l, "u": u, "m": m, "i": i, "pingo": pingo, "largura": largura, "xm": xm, "lm": 3 * W + 2 * vao}


def caminho(geom, dx=0.0, dy=0.0):
    partes = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
    out = []
    for p in partes:
        for anel in [p.exterior] + list(p.interiors):
            pts = list(anel.coords)
            out.append("M" + " L".join(f"{a + dx:.2f} {b + dy:.2f}" for a, b in pts) + "Z")
    return "".join(out)


def odonto(alvo_largura):
    """'ODONTO' em Archivo Expanded SemiBold, em curvas, com a largura pedida."""
    f = TTFont(RAIZ / "_fontes" / "Archivo-Expanded-600.ttf")
    gs, cm = f.getGlyphSet(), f.getBestCmap()
    nomes = [cm[ord(c)] for c in "ODONTO"]

    def lim(n):
        b = BoundsPen(gs)
        gs[n].draw(b)
        return b.bounds

    cap = f["OS/2"].sCapHeight
    letras_w = sum(gs[n].width for n in nomes[:-1]) + lim(nomes[-1])[2] - lim(nomes[0])[0]
    esp = 0.32 * cap  # espaçamento entre letras
    total = letras_w + esp * 5
    s = alvo_largura / total
    x = -lim(nomes[0])[0]
    paths = []
    for n in nomes:
        p = SVGPathPen(gs)
        gs[n].draw(p)
        paths.append((x, p.getCommands()))
        x += gs[n].width + esp
    return paths, s, cap * s


def svg(w, h, corpo, x0=0, y0=0):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.1f} {y0:.1f} {w:.1f} {h:.1f}" width="{w:.0f}" height="{h:.0f}">{corpo}</svg>\n'


def montar():
    SAIDA.mkdir(parents=True, exist_ok=True)
    for velho in SAIDA.glob("*.svg"):
        velho.unlink()
    L = letras()
    larg = L["largura"]
    px, py, pr = L["pingo"]
    m = 12  # margem

    for nome, (cor, cor_pingo) in VERSOES.items():
        letras_d = "".join(caminho(L[k]) for k in "lumi")
        pingo = f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{pr}" fill="{cor_pingo}"/>'
        corpo = f'<path fill="{cor}" d="{letras_d}"/>{pingo}'
        topo = -ASC - m
        (SAIDA / f"lumi-{nome}.svg").write_text(svg(larg + 2 * m, ASC + 2 * m, corpo, -m, topo))

        # com ODONTO embaixo, centrado, com 58% da largura do lettering
        paths, s, cap_h = odonto(larg * 0.58)
        gap = 28
        ox = (larg - larg * 0.58) / 2
        g = f'<g fill="{cor}" transform="translate({ox:.2f} {gap + cap_h:.2f}) scale({s:.5f} {-s:.5f})">'
        g += "".join(f'<path transform="translate({x:.1f} 0)" d="{d}"/>' for x, d in paths) + "</g>"
        (SAIDA / f"lumi-odonto-{nome}.svg").write_text(svg(larg + 2 * m, ASC + gap + cap_h + 2 * m, corpo + g, -m, topo))

        # só o molar (o m sozinho vira símbolo)
        d_m = caminho(L["m"], dx=-L["xm"])
        lm = L["lm"]
        (SAIDA / f"lumi-molar-{nome}.svg").write_text(svg(lm + 2 * m, XH + 2 * m, f'<path fill="{cor}" d="{d_m}"/>', -m, -XH - m))

    # foto de perfil: molar esmalte sobre hortelã
    lm = L["lm"]
    esc = 4.6
    d_m = caminho(L["m"], dx=-L["xm"])
    tx = (1080 - lm * esc) / 2
    ty = (1080 - XH * esc) / 2 + XH * esc + 8
    corpo = f'<rect width="1080" height="1080" fill="{COR["hortela"]}"/><g transform="translate({tx:.1f} {ty:.1f}) scale({esc})"><path fill="{COR["esmalte"]}" d="{d_m}"/></g>'
    (SAIDA / "lumi-avatar.svg").write_text(svg(1080, 1080, corpo))
    print("ok:", len(list(SAIDA.glob("*.svg"))), "arquivos em", SAIDA.relative_to(RAIZ.parent))


if __name__ == "__main__":
    montar()
