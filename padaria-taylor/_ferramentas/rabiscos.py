"""Rabiscos de traço único (estilo caderno), para padronagens, cardápio e embalagens.

Cada rabisco é desenhado numa caixa de 200 x 200. Uso: python3 padaria-taylor/_ferramentas/rabiscos.py
Saída: padaria-taylor/01-marca/ilustracao/rabiscos/*.svg e uma folha com todos.
"""
from pathlib import Path

SAIDA = Path(__file__).resolve().parents[1] / "01-marca" / "ilustracao" / "rabiscos"
LENHA = "#3A2A20"
FERRUGEM = "#B5582D"
MUSGO = "#6E7A55"

TREMIDO = """<filter id="mao" x="-10%" y="-10%" width="120%" height="120%">
<feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="2" seed="3" result="r"/>
<feDisplacementMap in="SourceGraphic" in2="r" scale="2.4" xChannelSelector="R" yChannelSelector="G"/></filter>"""

R = {}

# pão de fermentação natural, de lado, com a orelha do corte
R["pao"] = f'''
<path d="M30 140 C24 96 58 64 100 62 C142 64 176 96 170 140 C150 152 50 152 30 140 Z"/>
<path d="M58 92 C80 74 120 70 146 84"/>
<path d="M62 96 C86 86 118 84 142 90"/>
<path d="M48 120 L54 116 M150 118 L144 114 M98 128 L102 124"/>
'''
# pote de fermento (levain) com bolhas, elástico marcando quanto cresceu
R["fermento"] = f'''
<path d="M62 52 L138 52 L138 64 L62 64 Z"/>
<path d="M66 64 C56 76 56 88 56 100 L56 160 C56 172 66 176 76 176 L124 176 C134 176 144 172 144 160 L144 100 C144 88 144 76 134 64"/>
<path d="M56 108 C80 116 120 100 144 110"/>
<path d="M56 96 L144 96" stroke="{FERRUGEM}" stroke-width="6"/>
<circle cx="82" cy="132" r="5"/><circle cx="110" cy="146" r="7"/><circle cx="122" cy="124" r="4"/><circle cx="92" cy="158" r="4"/>
<path d="M78 40 C82 32 90 30 96 34 M104 34 C110 26 120 28 122 36"/>
'''
# cabana com fumaça na chaminé
R["cabana"] = f'''
<path d="M36 100 L100 48 L164 100"/>
<path d="M48 92 L48 170 L152 170 L152 92"/>
<path d="M88 170 L88 128 L112 128 L112 170"/>
<path d="M62 114 L80 114 L80 132 L62 132 Z M71 114 L71 132"/>
<path d="M124 114 L142 114 L142 132 L124 132 Z M133 114 L133 132"/>
<path d="M130 74 L130 50 L144 50 L144 86"/>
<path d="M136 40 C126 32 136 22 128 12 M146 36 C140 28 150 22 144 14"/>
<path d="M48 150 L152 150" stroke-dasharray="2 14"/>
'''
# pinheiro
R["pinheiro"] = f'''
<path d="M100 22 L66 72 L84 72 L56 114 L78 114 L44 160 L156 160 L122 114 L144 114 L116 72 L134 72 Z"/>
<path d="M92 160 L92 182 L108 182 L108 160"/>
'''
# caneca com vapor
R["caneca"] = f'''
<path d="M50 84 L140 84 L134 166 C132 176 124 180 114 180 L76 180 C66 180 58 176 56 166 Z"/>
<path d="M138 102 C166 100 168 140 134 142"/>
<path d="M76 70 C66 58 84 50 74 34 M100 70 C90 56 108 48 98 30 M124 70 C114 58 132 50 122 34"/>
<path d="M72 120 L120 120" stroke="{FERRUGEM}" stroke-width="6"/>
'''
# cesta com pães e paninho xadrez
R["cesta"] = f'''
<path d="M30 104 L170 104 L156 172 L44 172 Z"/>
<path d="M50 104 C52 74 92 60 100 104"/>
<path d="M96 104 C100 66 146 66 150 104"/>
<path d="M66 82 C72 76 82 76 86 82 M112 80 C120 74 130 74 136 80"/>
<path d="M42 126 L158 126 M40 148 L160 148"/>
<path d="M70 104 L66 172 M100 104 L100 172 M130 104 L134 172"/>
<path d="M30 104 C20 96 30 86 40 92" stroke="{FERRUGEM}"/>
'''
# rolo de massa e colher de pau cruzados
R["rolo"] = f'''
<path d="M40 150 L150 52"/>
<path d="M58 140 L140 66 L152 80 L70 154 Z" />
<path d="M40 150 L30 160 M150 52 L162 42" stroke-width="9"/>
<path d="M56 56 L146 150"/>
<path d="M146 150 C150 168 170 172 176 160 C182 146 164 136 152 142"/>
'''
# biscoito de chai com glacê
R["biscoito"] = f'''
<circle cx="100" cy="104" r="62"/>
<path d="M54 92 C70 80 80 104 96 90 C112 76 122 104 140 90 C150 82 156 92 156 98"/>
<path d="M50 112 C66 102 78 124 96 110 C114 96 126 124 146 110"/>
<circle cx="78" cy="134" r="3.5" fill="{LENHA}"/><circle cx="112" cy="140" r="3.5" fill="{LENHA}"/><circle cx="128" cy="72" r="3.5" fill="{LENHA}"/>
'''
# estrela (a do cardigã) e brilhinho
R["estrela"] = f'''
<path d="M100 30 L118 76 L168 78 L128 108 L142 158 L100 128 L58 158 L72 108 L32 78 L82 76 Z" fill="{FERRUGEM}"/>
'''
# raminho
R["raminho"] = f'''
<path d="M100 180 C100 130 96 80 104 24"/>
<path d="M100 150 L70 128 M100 150 L130 128 M100 118 L74 98 M100 118 L126 98 M102 86 L80 68 M102 86 L124 68 M104 56 L90 42 M104 56 L118 42"/>
'''


def svg(nome, cor=LENHA, esp=5.5):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200"><defs>{TREMIDO}</defs>'
            f'<g filter="url(#mao)" fill="none" stroke="{cor}" stroke-width="{esp}" stroke-linecap="round" stroke-linejoin="round">{R[nome]}</g></svg>\n')


def grupo(nome, x, y, s=1.0, rot=0, cor=LENHA, esp=5.5):
    """O rabisco pronto para entrar dentro de outro SVG (precisa do filtro #mao no documento)."""
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s}) translate(-100 -100)" filter="url(#mao)" fill="none" '
            f'stroke="{cor}" stroke-width="{esp / s:.2f}" stroke-linecap="round" stroke-linejoin="round">{R[nome]}</g>')


if __name__ == "__main__":
    SAIDA.mkdir(parents=True, exist_ok=True)
    for n in R:
        (SAIDA / f"{n}.svg").write_text(svg(n))
    nomes = list(R)
    folha = "".join(grupo(n, 120 + (i % 5) * 220, 120 + (i // 5) * 220) for i, n in enumerate(nomes))
    (SAIDA.parent / "rabiscos-folha.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 460" width="1120" height="460"><defs>{TREMIDO}</defs>{folha}</svg>\n')
    print("ok", nomes)
