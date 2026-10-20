# Gera PDFs leves (cada página = JPEG) a partir de out/pagina-*.png.
# Uso: python3 -I fazer_pdf_leve.py <pasta_com_pagina-XX.png> <saida_A5.pdf> <saida_A4_caderninho.pdf>
import sys, glob, io, os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader

src, out_a5, out_a4 = sys.argv[1:4]
files = sorted(glob.glob(os.path.join(src, 'pagina-*.png')))
n = len(files); assert n % 4 == 0, n
A5W, A5H = 420.0, 595.2756   # pt (148 x 210 mm)

def jpeg(f):
    im = Image.open(f).convert('RGB')
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=88, optimize=True, progressive=False)
    buf.seek(0); return ImageReader(buf)
imgs = [jpeg(f) for f in files]

# A5 solto
c = canvas.Canvas(out_a5, pagesize=(A5W, A5H))
for im in imgs:
    c.drawImage(im, 0, 0, A5W, A5H); c.showPage()
c.save()

# caderninho A4 paisagem (dobra ao meio, ordem de caderno)
SW, SH = landscape(A4)
order = []
for k in range(n // 4):
    order.append((n - 2*k, 2*k + 1))
    order.append((2*k + 2, n - 2*k - 1))
c = canvas.Canvas(out_a4, pagesize=(SW, SH))
for left, right in order:
    c.drawImage(imgs[left-1], 0, (SH-A5H)/2, A5W, A5H)
    c.drawImage(imgs[right-1], SW/2, (SH-A5H)/2, A5W, A5H)
    c.setLineWidth(0.3); c.setStrokeGray(0.45)
    c.line(SW/2, 0, SW/2, 8); c.line(SW/2, SH-8, SW/2, SH)
    c.showPage()
c.save()
print('paginas', n, '| ordem', order)
