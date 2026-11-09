"""Mockup de chinelo (vista de cima) com a arte da estampa: versão 'par monta a imagem' e 'imagem em cada pé'.
Uso: python chinelo.py arte.png assinatura.svg saida.png  (cores via argumentos opcionais)"""
import base64
import re
import subprocess
import sys
import os

arte, assin, saida = sys.argv[1], sys.argv[2], sys.argv[3]
TIRA = sys.argv[4] if len(sys.argv) > 4 else '#2D5686'
LAT1 = sys.argv[5] if len(sys.argv) > 5 else '#D6A13D'
LAT2 = sys.argv[6] if len(sys.argv) > 6 else '#7C2420'
HERE = os.path.dirname(os.path.abspath(__file__))

img64 = base64.b64encode(open(arte, 'rb').read()).decode()
ext = 'png' if arte.endswith('png') else 'jpeg'
svg_assin = open(assin, encoding='utf8').read()
vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_assin)
aw, ah = float(vb.group(1)), float(vb.group(2))
inner = re.sub(r'^.*?<svg[^>]*>', '', svg_assin, flags=re.S).replace('</svg>', '')

# palmilha do pé direito (dedão à esquerda), caixa 320 x 860
SOLA = ('M165,860 C110,860 86,832 88,760 C91,690 118,612 112,540 C106,468 70,402 62,322 '
        'C52,212 72,44 142,22 C204,4 270,62 293,132 C313,194 307,282 290,362 C271,458 250,522 '
        '248,620 C246,720 251,782 238,822 C226,852 202,860 165,860 Z')
# tira em V: pino entre o dedão e o segundo dedo, presa nas laterais
TIRA_D = 'M88,488 C110,360 140,250 158,196 M158,196 C196,262 248,372 284,470'


def pe(x, y, espelho, clip_id, img_x, img_y, img_w, img_h, assinatura=False):
    t = f'translate({x + (320 if espelho else 0)} {y}) scale({-1 if espelho else 1} 1)'
    # a imagem não pode espelhar: ela é posicionada em coordenadas da página, fora do grupo transformado
    return f'''
    <g transform="{t}">
      <path d="{SOLA}" transform="translate(6 14)" fill="{LAT2}"/>
      <path d="{SOLA}" transform="translate(3 7)" fill="{LAT1}"/>
    </g>
    <clipPath id="{clip_id}"><path d="{SOLA}" transform="{t}"/></clipPath>
    <g clip-path="url(#{clip_id})">
      <image href="data:image/{ext};base64,{img64}" x="{img_x}" y="{img_y}" width="{img_w}" height="{img_h}" preserveAspectRatio="xMidYMid slice"/>
      {assin_svg(x, y, espelho) if assinatura else ''}
    </g>
    <g transform="{t}">
      <path d="{SOLA}" fill="none" stroke="rgba(0,0,0,.18)" stroke-width="2"/>
      <path d="{TIRA_D}" fill="none" stroke="rgba(0,0,0,.25)" stroke-width="30" stroke-linecap="round" transform="translate(4 8)"/>
      <path d="{TIRA_D}" fill="none" stroke="{TIRA}" stroke-width="28" stroke-linecap="round"/>
      <path d="{TIRA_D}" fill="none" stroke="rgba(255,255,255,.18)" stroke-width="6" stroke-linecap="round" transform="translate(-3 -3)"/>
      <circle cx="158" cy="196" r="17" fill="{TIRA}"/><circle cx="158" cy="196" r="7" fill="rgba(0,0,0,.25)"/>
    </g>'''


def assin_svg(x, y, espelho):
    w = 150
    h = w * ah / aw
    cx = x + 165 if not espelho else x + 155
    return f'<svg x="{cx - w / 2}" y="{y + 860 - h - 34}" width="{w}" height="{h}" viewBox="0 0 {aw} {ah}">{inner}</svg>'


W, H = 1700, 1150
# A: o par monta a imagem (imagem cobre os dois pés juntos)
ax, ay = 90, 170
par_w, par_h = 320 * 2 + 40, 860
A = pe(ax, ay, True, 'ca1', ax - 20, ay - 30, par_w + 40, par_h + 60) + \
    pe(ax + 360, ay, False, 'ca2', ax - 20, ay - 30, par_w + 40, par_h + 60, assinatura=True)
# B: a imagem em cada pé
bx = 930
B = pe(bx, ay, True, 'cb1', bx - 60, ay - 40, 440, 940, assinatura=True) + \
    pe(bx + 360, ay, False, 'cb2', bx + 300, ay - 40, 440, 940, assinatura=True)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<rect width="{W}" height="{H}" fill="#F3EEE5"/>
<g font-family="Jost, sans-serif" fill="#1E1A17">
  <text x="90" y="80" font-size="15" letter-spacing="4" fill="#6E655C">A · POSICIONADA — O PAR MONTA A JANELA</text>
  <text x="90" y="112" font-size="22">a janela só se completa com os dois pés juntos</text>
  <text x="930" y="80" font-size="15" letter-spacing="4" fill="#6E655C">B · POSICIONADA — A JANELA EM CADA PÉ</text>
  <text x="930" y="112" font-size="22">a imagem inteira recortada em cada palmilha</text>
</g>
{A}{B}
<g font-family="Jost, sans-serif" font-size="14" fill="#6E655C">
  <text x="90" y="1110">tira azul-colonial · lateral ocre e sangue-de-boi · assinatura no calcanhar (como na V1)</text>
</g></svg>'''
tmp = saida + '.svg'
open(tmp, 'w', encoding='utf8').write(svg)
subprocess.run(['node', os.path.join(HERE, 'svg_raster.js'), tmp, str(W * 2), saida], check=True)
print('ok', saida)
