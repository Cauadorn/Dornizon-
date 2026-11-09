import numpy as np, sys
from PIL import Image, ImageFilter
W='/tmp/claude-0/-home-user-dornizon-/50e34bb1-6fc8-52cf-89f6-3543fe6b8ad6/scratchpad/work/'
S=float(sys.argv[1]) if len(sys.argv)>1 else 1.35
X=int(sys.argv[2]) if len(sys.argv)>2 else 760
raw=np.asarray(Image.open(W+'raw2.jpg').convert('RGB')).astype(np.float32)
H,Wd=raw.shape[:2]  # 2700,2160
# --- background wall
from scipy.ndimage import gaussian_filter
reg=raw[0:1300,24:904]
row=np.concatenate([reg,reg[:,::-1],reg,reg[:,::-1]],axis=1)[:, :Wd]
wall=np.concatenate([row,row[::-1],row],axis=0)[:H]
low=np.stack([gaussian_filter(wall[...,c],90) for c in range(3)],-1)
hi=raw[0:1300,24:904]-np.stack([gaussian_filter(raw[0:1300,24:904,c],4) for c in range(3)],-1)
hr=np.concatenate([hi,hi[:,::-1],hi,hi[:,::-1]],axis=1); hit=np.concatenate([hr,hr[::-1],hr],axis=0)[:H,:Wd]
wall=low+hit*0.9
# keep original left strip (continuity with slide 4)
xs=np.arange(Wd)[None,:,None]
m=np.clip((210-xs)/150,0,1)  # 1 = original
bg=raw*m+wall*(1-m)
# floor darkening / vignette
ys=np.arange(H)[:,None,None]/H
dark=np.clip((ys-0.62)/0.38,0,1)**1.3
shade=np.array([40,8,14],np.float32)
bg=bg*(1-0.75*dark)+shade*0.75*dark
# --- subject
cut=Image.open(W+'pedro_cut.png').convert('RGBA')
from scipy.ndimage import label
A0=np.asarray(cut)[...,3]; lab,n=label(A0>40); sizes=[(lab==i).sum() for i in range(1,n+1)]
keep=lab==(1+int(np.argmax(sizes)))
from scipy.ndimage import binary_dilation
keep=binary_dilation(keep,iterations=6)
arr=np.asarray(cut).copy(); arr[...,3]=(arr[...,3]*keep).astype(np.uint8); cut=Image.fromarray(arr)
cw,ch=cut.size
cut=cut.resize((int(cw*S),int(ch*S)),Image.LANCZOS)
p=np.asarray(cut).astype(np.float32)
rgb=p[...,:3]; a=p[...,3:]/255
lum=(rgb@np.array([.299,.587,.114]))[...,None]/255
# grade: warm, red bounce in shadows, a bit more contrast
g=rgb.copy()
g=g*np.array([1.07,0.98,0.90])+np.array([6,0,-4])
red=g*np.array([1.0,0.62,0.64])
g=g*(1-(1-lum)*0.42)+red*((1-lum)*0.42)
g=(g-128)*1.06+128
# directional light: from left (window) warm, right side darker
xx=np.linspace(0,1,g.shape[1])[None,:,None]
g=g*(1.10-0.24*xx)
g=np.clip(g,0,255)
# place
ph,pw=g.shape[:2]
oy=H-ph+int(0.15*ph)  # push down a bit so legs crop out
ox=X
canvas=bg.copy()
# shadow on wall (right/up offset)
al=Image.fromarray((a[...,0]*255).astype(np.uint8))
sh=np.zeros((H,Wd),np.float32)
def paste(dst,src,ox,oy):
    y0,x0=max(oy,0),max(ox,0); y1,x1=min(oy+src.shape[0],H),min(ox+src.shape[1],Wd)
    return (slice(y0,y1),slice(x0,x1)),(slice(y0-oy,y1-oy),slice(x0-ox,x1-ox))
shb=np.asarray(al.filter(ImageFilter.GaussianBlur(40))).astype(np.float32)/255
d,s=paste(sh,shb,ox+170,oy-40); sh[d]=shb[s]
canvas=canvas*(1-0.45*sh[...,None])
d,s=paste(canvas,g,ox,oy)
A=a[s]; canvas[d]=canvas[d]*(1-A)+g[s]*A
# grain to match other slides
rng=np.random.default_rng(1)
canvas+=rng.normal(0,4.5,canvas.shape[:2])[...,None]
out=Image.fromarray(np.clip(canvas,0,255).astype(np.uint8))
out.save(W+'fundo_novo.jpg',quality=93)
out.resize((540,675)).save(W+'fundo_small.jpg')
