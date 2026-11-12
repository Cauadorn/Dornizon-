"""Gera o logo da Lumi Odonto em SVG (texto já em curvas, não depende de fonte instalada).

Uso: python3 lumi-odonto/_ferramentas/marca.py
Saída: lumi-odonto/01-marca/svg/*.svg
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen

RAIZ = Path(__file__).resolve().parents[1]
FONTES = RAIZ / "_fontes"
SAIDA = RAIZ / "01-marca" / "svg"

COR = {
    "salvia": "#9BB5A0",
    "folha": "#4F6F5C",
    "areia": "#EDE6DA",
    "leite": "#F8F5EF",
    "grafite": "#2E2E2E",
    "pessego": "#F2B8A0",
}

# Versões: (nome, cor do arco, cor do texto, cor da luz)
VERSOES = {
    "cor": (COR["folha"], COR["grafite"], COR["pessego"]),
    "negativo": (COR["leite"], COR["leite"], COR["pessego"]),
    "grafite": (COR["grafite"], COR["grafite"], COR["grafite"]),
    "branco": ("#FFFFFF", "#FFFFFF", "#FFFFFF"),
}


def glifos(fonte):
    f = TTFont(FONTES / fonte)
    return f, f.getGlyphSet(), f.getBestCmap()


def caminho(gs, nome):
    p = SVGPathPen(gs)
    gs[nome].draw(p)
    return p.getCommands()


def limites(gs, nome):
    b = BoundsPen(gs)
    gs[nome].draw(b)
    return b.bounds


# ---------- "lumi" em Instrument Serif, com o pingo do i virando a luz (pêssego)
def palavra_lumi():
    f, gs, cm = glifos("InstrumentSerif-Regular.ttf")
    x, partes = 0, []
    aperto = -14  # aproxima um pouco as letras
    for ch in "lumı":
        g = cm[ord(ch)]
        partes.append((x, caminho(gs, g)))
        if ch == "ı":
            # centro do pingo original do i
            rp = RecordingPen()
            gs[cm[ord("i")]].draw(rp)
            pts, contornos, atual = [], [], []
            for op, args in rp.value:
                atual.extend(args)
                if op == "closePath":
                    contornos.append(atual)
                    atual = []
            pingo = max(contornos, key=lambda c: min(p[1] for p in c))
            xs = [p[0] for p in pingo]
            ys = [p[1] for p in pingo]
            cx, cy = (min(xs) + max(xs)) / 2 + x, (min(ys) + max(ys)) / 2
            r = (max(xs) - min(xs)) / 2 * 1.32
        x += gs[g].width + aperto
    largura = x - aperto
    l_min = limites(gs, cm[ord("l")])[0]
    m_max = partes[-1][0] + limites(gs, cm[ord("ı")])[2]
    return partes, (cx, cy + 22, r), l_min, m_max  # pingo sobe um tico


# ---------- "ODONTO" em Manrope SemiBold, espaçado para ocupar a largura pedida
def palavra_odonto(largura_alvo_unidades_lumi, escala_rel):
    f, gs, cm = glifos("Manrope-600.ttf")
    nomes = [cm[ord(c)] for c in "ODONTO"]
    larg_letras = sum(gs[n].width for n in nomes[:-1]) + limites(gs, nomes[-1])[2]
    x0 = limites(gs, nomes[0])[0]
    larg_letras -= x0
    alvo = largura_alvo_unidades_lumi / escala_rel
    espaco = (alvo - larg_letras) / (len(nomes) - 1)
    x, partes = -x0, []
    for n in nomes:
        partes.append((x, caminho(gs, n)))
        x += gs[n].width + espaco
    cap = f["OS/2"].sCapHeight
    return partes, cap


def grupo_letras(partes, tx, ty, s, cor):
    out = [f'<g fill="{cor}" transform="translate({tx:.2f} {ty:.2f}) scale({s} {-s})">']
    for x, d in partes:
        out.append(f'<path transform="translate({x:.1f} 0)" d="{d}"/>')
    out.append("</g>")
    return "\n".join(out)


# ---------- símbolo: arco (arcada / porta) com o sol nascendo dentro
# desenhado numa caixa 84 x 104 (origem no canto de cima à esquerda)
def simbolo(tx, ty, s, cor_arco, cor_luz):
    arco = "M0 104V42A42 42 0 0 1 84 42V104H64V42A22 22 0 0 0 20 42V104Z"
    sol = "M24 104A18 18 0 0 1 60 104Z"
    return (
        f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s})">'
        f'<path fill="{cor_arco}" d="{arco}"/><path fill="{cor_luz}" d="{sol}"/></g>'
    )


def svg(w, h, corpo, fundo=None):
    bg = f'<rect width="{w:.0f}" height="{h:.0f}" fill="{fundo}"/>' if fundo else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
        f'width="{w:.0f}" height="{h:.0f}">{bg}{corpo}</svg>\n'
    )


def montar():
    SAIDA.mkdir(parents=True, exist_ok=True)
    lumi, pingo, l_min, m_max = palavra_lumi()
    s_lumi = 0.2  # 1000 unidades -> 200 px
    larg_lumi = (m_max - l_min) * s_lumi
    alt_l = 740 * s_lumi  # topo do l até a linha de base
    s_od = 0.0215
    odonto, cap = palavra_odonto(m_max - l_min, s_od / s_lumi)
    alt_od = cap * s_od
    gap = 30  # linha de base do lumi até o topo do ODONTO

    def bloco_texto(x, y_topo, cor_txt, cor_luz):
        base = y_topo + alt_l
        cx, cy, r = pingo
        t = grupo_letras(lumi, x - l_min * s_lumi, base, s_lumi, cor_txt)
        t += f'<circle cx="{x + (cx - l_min) * s_lumi:.2f}" cy="{base - cy * s_lumi:.2f}" r="{r * s_lumi:.2f}" fill="{cor_luz}"/>'
        t += grupo_letras(odonto, x, base + gap + alt_od, s_od, cor_txt)
        return t, alt_l + gap + alt_od

    for nome, (c_arco, c_txt, c_luz) in VERSOES.items():
        # horizontal: símbolo com a altura do bloco de texto
        m = 24
        txt, alt_txt = bloco_texto(0, 0, c_txt, c_luz)
        s_sim = alt_txt / 104
        larg_sim = 84 * s_sim
        respiro = 0.42 * larg_sim
        corpo = simbolo(m, m, s_sim, c_arco, c_luz)
        txt, _ = bloco_texto(m + larg_sim + respiro, m, c_txt, c_luz)
        W = m * 2 + larg_sim + respiro + larg_lumi
        H = m * 2 + alt_txt
        (SAIDA / f"lumi-horizontal-{nome}.svg").write_text(svg(W, H, corpo + txt))

        # vertical: símbolo em cima, centrado
        s_sim_v = 1.85
        larg_v, alt_v = 84 * s_sim_v, 104 * s_sim_v
        W = m * 2 + max(larg_lumi, larg_v)
        corpo = simbolo((W - larg_v) / 2, m, s_sim_v, c_arco, c_luz)
        txt, alt_txt = bloco_texto((W - larg_lumi) / 2, m + alt_v + 40, c_txt, c_luz)
        H = m + alt_v + 40 + alt_txt + m
        (SAIDA / f"lumi-vertical-{nome}.svg").write_text(svg(W, H, corpo + txt))

        # só o nome
        txt, alt_txt = bloco_texto(m, m, c_txt, c_luz)
        (SAIDA / f"lumi-nome-{nome}.svg").write_text(svg(m * 2 + larg_lumi, m * 2 + alt_txt, txt))

        # só o símbolo
        (SAIDA / f"lumi-simbolo-{nome}.svg").write_text(svg(84 * 4 + 48, 104 * 4 + 48, simbolo(24, 24, 4, c_arco, c_luz)))

    # avatar (foto de perfil): quadrado areia; o Instagram recorta em círculo
    A = 1080
    s = 5.2
    corpo = f'<rect width="1080" height="1080" fill="{COR["areia"]}"/>' + simbolo(
        (A - 84 * s) / 2, (A - 104 * s) / 2 + 20, s, COR["folha"], COR["pessego"]
    )
    (SAIDA / "lumi-avatar.svg").write_text(svg(A, A, corpo))
    print("ok:", len(list(SAIDA.glob("*.svg"))), "arquivos em", SAIDA)


if __name__ == "__main__":
    montar()
