"""Folha de contato com marcação: verde = local confirmado; vermelho = sem local; NC = não comercial."""
import json
import os
import sys

from PIL import Image, ImageDraw

d, out = sys.argv[1], sys.argv[2]
cred = json.load(open(os.path.join(d, 'creditos.json'), encoding='utf8'))
itens = [c for lista in cred.values() for c in lista if os.path.exists(os.path.join(d, c['arquivo']))]
cols, tw, th = 7, 250, 180
rows = (len(itens) + cols - 1) // cols
sheet = Image.new('RGB', (cols * tw, rows * (th + 30)), 'white')
dr = ImageDraw.Draw(sheet)
for i, c in enumerate(itens):
    try:
        im = Image.open(os.path.join(d, c['arquivo'])).convert('RGB')
    except Exception:
        continue
    im.thumbnail((tw - 6, th - 6))
    x, y = (i % cols) * tw, (i // cols) * (th + 30)
    sheet.paste(im, (x + 3, y + 3))
    cor = (20, 150, 60) if c.get('local_ok') else (210, 30, 30)
    dr.rectangle([x + 2, y + 2, x + 3 + im.width, y + 3 + im.height], outline=cor, width=3)
    tag = ('NC ' if c.get('nc') else '') + ','.join(c.get('onde', []))[:26]
    dr.text((x + 4, y + th + 2), c['arquivo'][:34], fill='black')
    dr.text((x + 4, y + th + 14), tag, fill=cor)
sheet.save(out, quality=80)
print(len(itens), 'fotos')
