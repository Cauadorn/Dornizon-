"""Cena ilustrada (a mesa da cabana) e padronagem de rabiscos.

Uso: python3 padaria-taylor/_ferramentas/cena.py
Saída: padaria-taylor/01-marca/ilustracao/cena.svg e padrao-*.svg
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from rabiscos import TREMIDO, grupo  # noqa: E402
from betty import betty  # noqa: E402

SAIDA = Path(__file__).resolve().parents[1] / "01-marca" / "ilustracao"


def cena(cor="#F2EADB", esp=5.5):
    """Janela da cabana com pinheiros lá fora, mesa com pão, fermento, caneca, cesta, e a betty em cima."""
    t = f'fill="none" stroke="{cor}" stroke-width="{esp}" stroke-linecap="round" stroke-linejoin="round" filter="url(#mao)"'
    partes = [
        # janela com topo arredondado
        f'<path {t} d="M300 560 L300 250 C300 150 380 96 540 96 C700 96 780 150 780 250 L780 560 Z"/>',
        f'<path {t} d="M540 100 L540 560 M300 330 L780 330"/>',
        f'<path {t} d="M280 560 L800 560"/>',
        # pinheiros lá fora
        grupo("pinheiro", 400, 440, 0.95, cor=cor, esp=esp),
        grupo("pinheiro", 650, 420, 1.1, cor=cor, esp=esp),
        grupo("pinheiro", 470, 230, 0.6, cor=cor, esp=esp),
        grupo("pinheiro", 720, 220, 0.55, cor=cor, esp=esp),
        # lua
        f'<path {t} d="M610 170 C590 176 584 204 602 216 C580 216 570 190 584 174 C592 166 602 166 610 170 Z"/>',
        # mesa
        f'<path {t} d="M100 760 L980 760 M140 760 L160 960 M940 760 L920 960 M100 784 L980 784"/>',
        # coisas na mesa (a base de cada rabisco encosta no tampo)
        grupo("pao", 215, 695, 1.3, cor=cor, esp=esp),
        grupo("biscoito", 345, 733, 0.42, cor=cor, esp=esp),
        grupo("biscoito", 382, 738, 0.36, rot=20, cor=cor, esp=esp),
        grupo("fermento", 488, 673, 1.15, cor=cor, esp=esp),
        grupo("caneca", 900, 680, 1.0, cor=cor, esp=esp),
        grupo("estrela", 210, 220, 0.3, cor=cor, esp=esp),
        grupo("estrela", 880, 300, 0.22, cor=cor, esp=esp),
    ]
    gata = betty().split(">", 1)[1].rsplit("</svg>", 1)[0]
    partes.append(f'<g transform="translate(538 505) scale(0.55)">{gata}</g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 40 1080 960" width="1080" height="960">'
            f'<defs>{TREMIDO}</defs>{"".join(partes)}</svg>\n')


def padrao(cor, w=1080, h=1350, semente=13, esp=5.5):
    rnd = random.Random(semente)
    nomes = ["pao", "fermento", "cabana", "pinheiro", "caneca", "cesta", "rolo", "biscoito", "estrela", "raminho"]
    partes = []
    passo = 230
    for j, y in enumerate(range(40, h + 120, passo)):
        for i, x in enumerate(range(40 + (passo // 2 if j % 2 else 0), w + 120, passo)):
            n = nomes[(i * 3 + j * 7) % len(nomes)]
            s = 0.5 if n == "estrela" else 0.78
            partes.append(grupo(n, x, y, s, rot=rnd.randint(-16, 16), cor=cor, esp=esp))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<defs>{TREMIDO}</defs>{"".join(partes)}</svg>\n')


if __name__ == "__main__":
    (SAIDA / "cena.svg").write_text(cena())
    (SAIDA / "padrao-creme.svg").write_text(padrao("#F2EADB"))
    (SAIDA / "padrao-lenha.svg").write_text(padrao("#3A2A20"))
    print("ok")
