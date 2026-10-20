# Imposição do PDF A5 (20 páginas) em folhas A4 paisagem para dobrar ao meio.
# Uso: python3 impor-caderninho.py grimorio-exu-ngombo.pdf grimorio-caderninho-A4.pdf
import sys, io
from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
src=PdfReader(sys.argv[1]); n=len(src.pages); assert n%4==0, "precisa de múltiplo de 4 páginas"
SW,SH=landscape(A4)
buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=(SW,SH)); c.setLineWidth(0.3); c.setStrokeGray(0.45)
c.line(SW/2,0,SW/2,8); c.line(SW/2,SH-8,SW/2,SH); c.save(); buf.seek(0); ticks=PdfReader(buf).pages[0]
order=[]
for k in range(n//4):
    order.append((n-2*k, 2*k+1)); order.append((2*k+2, n-2*k-1))
w=PdfWriter()
for left,right in order:
    page=w.add_blank_page(width=SW,height=SH)
    for pg,x in ((left,0),(right,SW/2)):
        page.merge_transformed_page(src.pages[pg-1], Transformation().translate(x,0))
    page.merge_page(ticks)
w.write(sys.argv[2]); print(order)
