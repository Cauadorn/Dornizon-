"""Mapa dos corações: cada ilustração com o coração circulado + zoom do detalhe + legenda.
Uso: python mapa_coracoes.py config.json saida.jpg
config: [{"estado": "Minas Gerais", "arte": "caminho.png", "caixa": [x0,y0,x1,y1], "texto": "a sombra da veneziana"}]"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FUNDO = (243, 238, 229)
TINTA = (30, 26, 23)
CINZA = (110, 101, 92)
MARCA = (192, 54, 44)


def fonte(nome, tam):
    return ImageFont.truetype(os.path.join(HERE, 'fonts', nome), tam)


def cartao(item, H=760):
    arte = Image.open(item['arte']).convert('RGB')
    x0, y0, x1, y1 = item['caixa']
    # miniatura com o coração circulado
    esc = H / arte.height
    mini = arte.resize((int(arte.width * esc), H), Image.LANCZOS)
    d = ImageDraw.Draw(mini)
    cx, cy = (x0 + x1) / 2 * esc, (y0 + y1) / 2 * esc
    r = max(x1 - x0, y1 - y0) / 2 * esc * 1.15 + 6
    for k in range(3):
        d.ellipse((cx - r - k, cy - r - k, cx + r + k, cy + r + k), outline=MARCA)
    # zoom do detalhe (quadrado)
    lado = max(x1 - x0, y1 - y0)
    mx, my = (x0 + x1) // 2, (y0 + y1) // 2
    z = arte.crop((mx - lado // 2, my - lado // 2, mx + lado // 2, my + lado // 2)).resize((H - 150, H - 150), Image.LANCZOS)
    W = mini.width + 30 + z.width
    c = Image.new('RGB', (W, H + 110), FUNDO)
    c.paste(mini, (0, 0))
    c.paste(z, (mini.width + 30, 0))
    d = ImageDraw.Draw(c)
    d.text((0, H + 18), item['estado'].upper(), font=fonte('Jost.ttf', 26), fill=CINZA)
    d.text((0, H + 54), item['texto'], font=fonte('Fraunces-Italic.ttf', 34), fill=TINTA)
    # traço ligando o círculo ao zoom
    d.line((cx + r, cy, mini.width + 30, (H - 150) / 2), fill=MARCA, width=2)
    return c


def main():
    itens = json.load(open(sys.argv[1], encoding='utf8'))
    cards = [cartao(i) for i in itens]
    col = 2
    cw = max(c.width for c in cards)
    ch = max(c.height for c in cards)
    linhas = (len(cards) + col - 1) // col
    M = 70
    out = Image.new('RGB', (col * cw + (col + 1) * M, linhas * ch + (linhas + 1) * M + 120), FUNDO)
    d = ImageDraw.Draw(out)
    d.text((M, 50), 'ONDE O CORAÇÃO MORA', font=fonte('Jost.ttf', 30), fill=CINZA)
    d.text((M, 92), 'em cada estado, o coração é formado pelos próprios elementos', font=fonte('Fraunces-Italic.ttf', 40), fill=TINTA)
    for i, c in enumerate(cards):
        x = M + (i % col) * (cw + M)
        y = 120 + M + (i // col) * (ch + M)
        out.paste(c, (x, y))
    out.save(sys.argv[2], quality=90)
    print('ok', sys.argv[2], out.size)


if __name__ == '__main__':
    main()
