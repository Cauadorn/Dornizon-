# Gera (1) um PDF pequeno do caderninho e (2) as 16 faces A4 em JPEG, a partir de pagina-*.png
# Uso: python3 -I fazer_faces.py <pasta_paginas> <saida_pdf_pequeno> <pasta_faces>
import sys, glob, os, io
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
src, out_pdf, out_dir = sys.argv[1:4]
files = sorted(glob.glob(os.path.join(src,'pagina-*.png'))); n=len(files)
pages = [Image.open(f).convert('RGB') for f in files]
order=[]
for k in range(n//4):
    order.append((n-2*k, 2*k+1)); order.append((2*k+2, n-2*k-1))
os.makedirs(out_dir, exist_ok=True)
# faces em JPEG, A4 paisagem a 240 dpi (2808 x 1984)
W,H = 2808,1984; pw,ph = 1404,1984
for i,(l,r) in enumerate(order, start=1):
    sheet = Image.new('RGB',(W,H),(234,223,196))
    sheet.paste(pages[l-1].resize((pw,ph), Image.LANCZOS),(0,0))
    sheet.paste(pages[r-1].resize((pw,ph), Image.LANCZOS),(pw,0))
    lado = 'frente' if i%2==1 else 'verso'
    sheet.save(os.path.join(out_dir, f'folha-{(i+1)//2}-{lado}.jpg'), 'JPEG', quality=85, optimize=True, dpi=(240,240))
# PDF pequeno (para ver/enviar): faces reduzidas a 1700px de largura, JPEG q72
SW,SH = landscape(A4)
c = canvas.Canvas(out_pdf, pagesize=(SW,SH))
for f in sorted(glob.glob(os.path.join(out_dir,'folha-*.jpg')), key=lambda p:(int(os.path.basename(p).split('-')[1]), 0 if 'frente' in p else 1)):
    im = Image.open(f); im = im.resize((1700, round(1700*H/W)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b,'JPEG',quality=72,optimize=True); b.seek(0)
    c.drawImage(ImageReader(b), 0, 0, SW, SH); c.showPage()
c.save()
print('ok', len(order), 'faces')
