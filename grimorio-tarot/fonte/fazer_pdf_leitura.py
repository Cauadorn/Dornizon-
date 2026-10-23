# Junta as páginas A5 do modo de leitura num PDF leve (páginas como JPEG).
# Uso: python3 -I fazer_pdf_leitura.py <pasta_paginas> <saida_pdf>
import sys, glob, os, io
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
src, out_pdf = sys.argv[1:3]
W, H = 148 * mm, 210 * mm
c = canvas.Canvas(out_pdf, pagesize=(W, H))
for f in sorted(glob.glob(os.path.join(src, 'pagina-*.png'))):
    im = Image.open(f).convert('RGB').resize((1050, 1490), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=72, optimize=True); b.seek(0)
    c.drawImage(ImageReader(b), 0, 0, W, H); c.showPage()
c.save()
