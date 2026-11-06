"""PDF do post do Behance: um módulo por página, na ordem do post (vídeos entram com a imagem parada).
Depende de behance_pacote.py ter montado behance/pacote/. Uso: python3 -I behance_pdf.py [saida.pdf]"""
import glob
import os
import sys

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
PK = os.path.join(AQUI, '..', '07-apresentacao', 'behance', 'pacote')
SAIDA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, '..', '07-apresentacao', 'behance', 'behance-bem-querer.pdf')
LARG = 2000
paginas = []
for f in sorted(glob.glob(os.path.join(PK, '2-modulos-em-ordem', '*'))):
    nome = os.path.splitext(os.path.basename(f))[0]
    if f.endswith('.mp4'):
        f = os.path.join(PK, '3-alternativas-paradas', nome + '.jpg')
    im = Image.open(f).convert('RGB')
    if im.width != LARG:
        im = im.resize((LARG, round(im.height * LARG / im.width)), Image.LANCZOS)
    paginas.append(im)
paginas[0].save(SAIDA, save_all=True, append_images=paginas[1:], resolution=200, quality=86)
print('ok', len(paginas), 'páginas', round(os.path.getsize(SAIDA) / 1e6, 1), 'MB')
