"""A mascote da era folklore/evermore: uma gata em posição de pão ("cat loaf"), de orelha dobrada
(Scottish Fold, como as gatas da Taylor), vestindo o cardigã de tricô com estrela bordada.

Uso: python3 padaria-taylor/_ferramentas/betty.py
Saída: padaria-taylor/01-marca/ilustracao/betty.svg
"""
from pathlib import Path

SAIDA = Path(__file__).resolve().parents[1] / "01-marca" / "ilustracao"

COR = {
    "cardiga": "#F2EADB",
    "trico": "#D9CBB0",
    "pelo": "#EAE4DA",
    "pelo2": "#B8AFA2",
    "lenha": "#3A2A20",
    "ferrugem": "#B5582D",
    "musgo": "#6E7A55",
    "rosa": "#E9A3A0",
}

TREMIDO = """<filter id="mao" x="-5%" y="-5%" width="110%" height="110%">
<feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="7" result="r"/>
<feDisplacementMap in="SourceGraphic" in2="r" scale="2.6" xChannelSelector="R" yChannelSelector="G"/></filter>"""


def trança(x, y0, y1, w=14, passo=22):
    """Uma trança de tricô (cable knit) vertical: dois fios que se cruzam."""
    d = []
    y = y0
    lado = 1
    while y < y1:
        d.append(f"M{x - w * lado:.1f} {y:.1f} C{x - w * lado:.1f} {y + passo * 0.5:.1f} {x + w * lado:.1f} {y + passo * 0.5:.1f} {x + w * lado:.1f} {y + passo:.1f}")
        lado *= -1
        y += passo
    return "".join(d)


def betty(fundo=None, mono=False):
    c = dict(COR)
    if mono:  # versão de impressão a uma cor: traço preto, preenchimento branco (some na multiplicação)
        c = {k: "#FFFFFF" for k in COR}
        c["lenha"] = "#000000"
    fundo_svg = f'<rect width="600" height="520" fill="{fundo}"/>' if fundo else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 520" width="600" height="520">
<defs>{TREMIDO}
<clipPath id="corpo"><path d="M104 440 C92 336 148 254 300 248 C452 254 508 336 496 440 C462 462 138 462 104 440 Z"/></clipPath></defs>
{fundo_svg}
<g filter="url(#mao)" stroke="{c["lenha"]}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
  <!-- rabo dando a volta -->
  <path d="M470 440 C520 430 548 392 528 356 C518 340 500 344 504 362 C516 392 486 420 446 430" fill="{c["pelo"]}"/>
  <!-- o corpo-pão, de cardigã -->
  <path d="M104 440 C92 336 148 254 300 248 C452 254 508 336 496 440 C462 462 138 462 104 440 Z" fill="{c["cardiga"]}"/>
  <!-- tranças do tricô -->
  <g clip-path="url(#corpo)" fill="none" stroke="{c["trico"]}" stroke-width="4">
    <path d="{trança(160, 300, 450)}"/><path d="{trança(160, 311, 450)}"/><path d="{trança(208, 290, 450)}"/><path d="{trança(208, 301, 450)}"/>
    <path d="{trança(392, 290, 450)}"/><path d="{trança(392, 301, 450)}"/><path d="{trança(440, 300, 450)}"/><path d="{trança(440, 311, 450)}"/>
  </g>
  <!-- abertura do cardigã com o peito da gata -->
  <path d="M262 300 C270 360 286 410 300 452 C314 410 330 360 338 300 Z" fill="{c["pelo"]}"/>
  <path d="M262 300 C270 360 286 410 300 452" fill="none"/>
  <path d="M338 300 C330 360 314 410 300 452" fill="none"/>
  <!-- botões -->
  <circle cx="330" cy="342" r="8" fill="{c["ferrugem"]}" stroke-width="4"/>
  <circle cx="320" cy="384" r="8" fill="{c["ferrugem"]}" stroke-width="4"/>
  <circle cx="310" cy="424" r="8" fill="{c["ferrugem"]}" stroke-width="4"/>
  <!-- estrela bordada -->
  <path d="M150 352 L157 368 L174 369 L161 380 L165 397 L150 388 L135 397 L139 380 L126 369 L143 368 Z" fill="{c["ferrugem"]}" stroke-width="4"/>
  <!-- patinhas aparecendo -->
  <path d="M232 452 C230 432 266 430 268 452" fill="{c["pelo"]}"/>
  <path d="M332 452 C334 430 370 432 368 452" fill="{c["pelo"]}"/>
  <path d="M244 446 L244 452 M256 445 L256 452 M344 445 L344 452 M356 446 L356 452" fill="none" stroke-width="3.5"/>
  <!-- cabeça -->
  <path d="M188 236 C182 170 236 134 300 134 C364 134 418 170 412 236 C406 290 360 316 300 316 C240 316 194 290 188 236 Z" fill="{c["pelo"]}"/>
  <!-- orelhas dobradas (Scottish Fold) -->
  <path d="M214 170 C216 142 244 128 262 142 C250 150 236 162 230 178 Z" fill="{c["pelo2"]}"/>
  <path d="M386 170 C384 142 356 128 338 142 C350 150 364 162 370 178 Z" fill="{c["pelo2"]}"/>
  <!-- listras na testa -->
  <path d="M284 146 L288 166 M300 142 L300 166 M316 146 L312 166" fill="none" stroke="{c["pelo2"]}" stroke-width="6"/>
</g>
<g stroke="{c["lenha"]}" stroke-linecap="round" stroke-linejoin="round" fill="none">
  <!-- olhos fechados, satisfeita -->
  <path d="M244 230 C252 242 268 242 276 230" stroke-width="6"/>
  <path d="M324 230 C332 242 348 242 356 230" stroke-width="6"/>
  <!-- nariz e boca -->
  <path d="M292 254 L308 254 L300 264 Z" fill="{c["rosa"]}" stroke-width="4"/>
  <path d="M300 264 C298 274 288 276 282 268 M300 264 C302 274 312 276 318 268" stroke-width="4"/>
  <!-- bigodes -->
  <path d="M232 262 L190 256 M234 274 L192 280 M368 262 L410 256 M366 274 L408 280" stroke-width="3.5"/>
</g>
{"" if mono else f'<ellipse cx="238" cy="262" rx="15" ry="9" fill="{c["rosa"]}" opacity=".7"/><ellipse cx="362" cy="262" rx="15" ry="9" fill="{c["rosa"]}" opacity=".7"/>'}
</svg>
'''


if __name__ == "__main__":
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "betty.svg").write_text(betty())
    (SAIDA / "betty-impressao.svg").write_text(betty(mono=True))
    print("ok")
