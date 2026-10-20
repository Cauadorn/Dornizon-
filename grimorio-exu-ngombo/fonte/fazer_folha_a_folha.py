# Caderninho "folha a folha": cada A4 deitado, dobrado ao meio, guarda 4 páginas SEGUIDAS.
# Folha k: frente = [4k | 4k-3], verso = [4k-2 | 4k-1]. Empilhar as folhas dobradas em ordem e furar na dobra.
# Uso: python3 -I fazer_folha_a_folha.py <pasta_paginas> <saida_pdf> <pasta_faces>
import sys, glob, os, io
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
src, out_pdf, out_dir = sys.argv[1:4]
files = sorted(glob.glob(os.path.join(src,'pagina-*.png'))); n=len(files); assert n%4==0
pages = [Image.open(f).convert('RGB') for f in files]
os.makedirs(out_dir, exist_ok=True)
W,H = 2808,1984; pw,ph = 1404,1984
faces=[]
for k in range(1, n//4+1):
    for lado,(l,r) in (('frente',(4*k,4*k-3)),('verso',(4*k-2,4*k-1))):
        sheet = Image.new('RGB',(W,H),(234,223,196))
        sheet.paste(pages[l-1].resize((pw,ph), Image.LANCZOS),(0,0))
        sheet.paste(pages[r-1].resize((pw,ph), Image.LANCZOS),(pw,0))
        name=f'folha-{k}-{lado}.jpg'
        sheet.save(os.path.join(out_dir,name),'JPEG',quality=88,optimize=True,dpi=(240,240))
        faces.append((name,l,r))
SW,SH = landscape(A4)
c = canvas.Canvas(out_pdf, pagesize=(SW,SH))
for name,l,r in faces:
    im = Image.open(os.path.join(out_dir,name)).resize((1900, round(1900*H/W)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b,'JPEG',quality=76,optimize=True); b.seek(0)
    c.drawImage(ImageReader(b),0,0,SW,SH)
    c.setLineWidth(0.3); c.setStrokeGray(0.45); c.line(SW/2,0,SW/2,8); c.line(SW/2,SH-8,SW/2,SH)
    c.showPage()
c.save()
print([f'{a}: {l}|{r}' for a,l,r in faces])
