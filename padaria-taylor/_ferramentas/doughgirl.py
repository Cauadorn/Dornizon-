"""Desenha a Doughgirl: um pão de fermentação natural vestido de showgirl (cocar de plumas, strass, cancã).

Uso: python3 padaria-taylor/_ferramentas/doughgirl.py
Saída: padaria-taylor/01-marca/ilustracao/doughgirl*.svg
"""
import math
from pathlib import Path

SAIDA = Path(__file__).resolve().parents[1] / "01-marca" / "ilustracao"

COR = {
    "portofino": "#F26B21",
    "menta": "#A8E0CF",
    "creme": "#FFF4E3",
    "chocolate": "#3B1F14",
    "casca": "#E9A85E",
    "casca2": "#C98140",
    "miolo": "#FBE3B5",
    "rosa": "#F27D84",
    "batom": "#B8322A",
}


def pluma(bx, by, ang, comp, larg, ondas=3.5):
    """Pluma de avestruz: contorno com borda fofa (ondinhas) ao longo de uma nervura levemente curva."""
    a = math.radians(ang)
    dx, dy = math.sin(a), -math.cos(a)  # direção da ponta
    lado = 1 if ang >= 0 else -1
    nx, ny = -dy * lado, dx * lado  # normal, para o lado de fora
    esq, dir_ = [], []
    n = 60
    for k in range(n + 1):
        t = k / n
        curva = (t ** 2.2) * comp * 0.22  # ponta que cai para fora, como pluma de verdade
        cx = bx + dx * comp * t + nx * curva
        cy = by + dy * comp * t + ny * curva
        w = larg * (math.sin(math.pi * min(1, 0.08 + t * 0.95)) ** 0.6)
        onda = 1 + 0.10 * abs(math.sin(t * ondas * 2 * math.pi)) * (t > 0.15)
        esq.append((cx + nx * w * onda, cy + ny * w * onda))
        onda2 = 1 + 0.10 * abs(math.sin(t * ondas * 2 * math.pi + 0.9)) * (t > 0.15)
        dir_.append((cx - nx * w * onda2, cy - ny * w * onda2))
    pts = esq + dir_[::-1]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"
    tip = (bx + dx * comp * 0.72 + nx * comp * 0.11, by + dy * comp * 0.72 + ny * comp * 0.11)
    nerv = f"M{bx:.1f} {by:.1f} Q{bx + dx * comp * 0.45 + nx * comp * 0.02:.1f} {by + dy * comp * 0.45 + ny * comp * 0.02:.1f} {tip[0]:.1f} {tip[1]:.1f}"
    return d, nerv


def pluma_fofa(bx, by, ang, comp, rmax, cor, choc):
    """Pluma de avestruz em bolinhas: um cordão de círculos sobrepostos que afina e enrola na ponta.
    Desenha em duas camadas (contorno grosso, depois o miolo) para o contorno sair só por fora, como nuvem."""
    a = math.radians(ang)
    lado = 1 if ang >= 0 else -1
    circ = []
    n = 14
    for k in range(n):
        t = k / (n - 1)
        x = bx + math.sin(a) * comp * t * 0.85 + lado * comp * 0.20 * (t ** 2.4)
        y = by - math.cos(a) * comp * t * 0.85 + comp * 0.16 * (t ** 3)
        r = rmax * (0.35 + 0.65 * math.sin(math.pi * min(1, 0.1 + t * 0.9)) ** 0.7) * (1 - 0.25 * t)
        circ.append((x, y, max(r, 8)))
        # penugem dos dois lados, alternando
        if 0.15 < t < 0.95:
            px, py = math.cos(a), math.sin(a)
            for sgn in (-1, 1):
                off = r * 0.72
                fase = 0.25 if (k + (sgn > 0)) % 2 else -0.1
                circ.append((x + sgn * px * off + fase * r * math.sin(a), y + sgn * py * off - fase * r * math.cos(a), r * 0.55))
    contorno = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + 3.5:.1f}" fill="{choc}"/>' for x, y, r in circ)
    miolo = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r - 0.5:.1f}" fill="{cor}"/>' for x, y, r in circ)
    return f'<g stroke="none">{contorno}{miolo}</g>'


def doughgirl(fundo=None, tremido=3.0, menta_vira="menta"):
    c = dict(COR)
    c["pluma2"] = COR[menta_vira]
    plumas = [(-66, 165, 36, "portofino"), (66, 165, 36, "portofino"), (-36, 190, 38, "pluma2"), (36, 190, 38, "pluma2"), (0.1, 215, 40, "portofino")]
    bx, by = 300, 312
    p_svg = [pluma_fofa(bx, by, ang, comp, larg, c[cor], c["chocolate"]) for ang, comp, larg, cor in plumas]
    # strass do cinto: pedrinhas seguindo a curva de baixo do pão
    strass = []
    for i in range(11):
        t = i / 10
        x = 196 + t * 208
        y = 488 + 16 * math.sin(t * math.pi)
        strass.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7.5" fill="{c["creme"]}"/>')
    fundo_svg = f'<rect width="600" height="720" fill="{fundo}"/>' if fundo else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 720" width="600" height="720">
<defs><filter id="mao" x="-5%" y="-5%" width="110%" height="110%">
<feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="4" result="r"/>
<feDisplacementMap in="SourceGraphic" in2="r" scale="{tremido}" xChannelSelector="R" yChannelSelector="G"/></filter></defs>
{fundo_svg}
<g filter="url(#mao)" stroke="{c["chocolate"]}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
  {"".join(p_svg)}
  <!-- perna de apoio, meia creme e salto portofino -->
  <path d="M262 532 C260 580 258 615 256 648" fill="none" stroke-width="22"/><path d="M262 532 C260 580 258 615 256 648" fill="none" stroke="{c["creme"]}" stroke-width="9"/>
  <path d="M232 664 C232 648 248 640 262 646 C270 652 272 662 270 670 L236 672 Z" fill="{c["portofino"]}"/>
  <path d="M266 670 L270 694" fill="none" stroke-width="5"/>
  <!-- perna de cancã, chute lá em cima -->
  <path d="M366 530 C420 548 470 540 506 506" fill="none" stroke-width="22"/><path d="M366 530 C420 548 470 540 506 506" fill="none" stroke="{c["creme"]}" stroke-width="9"/>
  <path d="M498 492 C506 476 526 474 534 488 C534 500 524 508 512 512 L500 510 Z" fill="{c["portofino"]}"/>
  <path d="M528 478 L548 462" fill="none" stroke-width="5"/>
  <!-- braços de borracha -->
  <path d="M184 446 C146 440 118 414 104 372" fill="none"/>
  <path d="M416 446 C454 440 482 414 496 372" fill="none"/>
  <!-- luvas -->
  <path d="M88 372 C82 350 96 336 110 344 C116 330 136 336 132 354 C138 368 124 382 108 380 Z" fill="{c["creme"]}"/>
  <path d="M512 372 C518 350 504 336 490 344 C484 330 464 336 468 354 C462 368 476 382 492 380 Z" fill="{c["creme"]}"/>
  <!-- o pão -->
  <path d="M168 526 C138 432 164 318 300 302 C436 318 462 432 432 526 C402 556 198 556 168 526 Z" fill="{c["casca"]}"/>
  <!-- casca mais escura embaixo -->
  <path d="M176 512 C230 534 370 534 424 512 C420 524 426 522 432 526 C402 556 198 556 168 526 C172 522 176 520 176 512 Z" fill="{c["casca2"]}" stroke="none"/>
  <!-- o corte: orelha levantada com o miolo aparecendo -->
  <path d="M214 360 C254 326 340 316 392 334 C372 350 300 356 232 372 Z" fill="{c["miolo"]}"/>
  <path d="M214 360 C254 326 340 316 392 334" fill="none" stroke-width="8"/>
  <path d="M196 410 C204 398 214 392 226 390" fill="none" stroke-width="4"/>
  <path d="M404 404 C398 394 390 388 380 386" fill="none" stroke-width="4"/>
  <!-- joia do cocar -->
  <path d="M300 290 L316 306 L300 324 L284 306 Z" fill="{c["menta"]}"/>
</g>
<g stroke="{c["chocolate"]}" stroke-linecap="round" stroke-linejoin="round" fill="none">
  <path d="M250 424 C258 412 274 412 282 424" stroke-width="6"/>
  <path d="M318 424 C326 412 342 412 350 424" stroke-width="6"/>
  <path d="M252 417 L242 408 M258 412 L252 401 M266 410 L264 398" stroke-width="4"/>
  <path d="M348 417 L358 408 M342 412 L348 401 M334 410 L336 398" stroke-width="4"/>
  <path d="M282 450 C288 476 312 476 318 450 Z" fill="{c["batom"]}" stroke-width="5"/>
  <path d="M292 465 C298 460 304 460 309 465" stroke="#F49C8E" stroke-width="5"/>
</g>
<ellipse cx="240" cy="452" rx="17" ry="10" fill="{c["rosa"]}" opacity=".8"/>
<ellipse cx="360" cy="452" rx="17" ry="10" fill="{c["rosa"]}" opacity=".8"/>
<g fill="{c["creme"]}"><circle cx="200" cy="392" r="4.5"/><circle cx="214" cy="380" r="2.8"/><circle cx="398" cy="380" r="4.5"/><circle cx="386" cy="368" r="2.8"/><circle cx="414" cy="408" r="2.6"/></g>
<g stroke="{c["chocolate"]}" stroke-width="4" stroke-linejoin="round">
  <path d="M96 236 L104 258 L126 266 L104 274 L96 296 L88 274 L66 266 L88 258 Z" fill="{c["portofino"]}"/>
  <path d="M522 214 L527 228 L541 233 L527 238 L522 252 L517 238 L503 233 L517 228 Z" fill="{c["creme"]}"/>
  <path d="M150 140 L154 151 L165 155 L154 159 L150 170 L146 159 L135 155 L146 151 Z" fill="{c["creme"]}"/>
</g>
</svg>
'''


if __name__ == "__main__":
    SAIDA.mkdir(parents=True, exist_ok=True)
    (SAIDA / "doughgirl.svg").write_text(doughgirl())
    (SAIDA / "doughgirl-para-fundo-menta.svg").write_text(doughgirl(menta_vira="creme"))
    print("ok")
