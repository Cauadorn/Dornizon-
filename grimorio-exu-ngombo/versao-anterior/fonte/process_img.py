# Uso: python3 -I process_img.py nome1.png nome2.png ...  (lê img_raw/, grava img/ com papel transparente)
import sys
from PIL import Image
import numpy as np
for name in sys.argv[1:]:
    im=Image.open('img_raw/'+name).convert('RGB')
    a=np.asarray(im).astype(np.float32)/255
    lum=a.mean(-1); bright=a[lum>=np.percentile(lum,60)]
    paper=np.percentile(bright,70,axis=0); a=np.clip(a/paper,0,1)
    alpha=1-a.min(-1)
    hist,edges=np.histogram(alpha,bins=200,range=(0,1)); pk=hist.max(); j=np.argmax(hist)
    while j<len(hist)-1 and hist[j]>pk*0.015: j+=1
    floor=min(edges[j]+0.01,0.14)
    alpha=np.clip((alpha-floor)/(1-floor),0,1); al=alpha[...,None]
    rgb=np.clip(np.where(al>1e-4,(a-(1-al))/np.maximum(al,1e-4),0),0,1)
    Image.fromarray((np.dstack([rgb,alpha])*255).astype(np.uint8),'RGBA').save('img/'+name)
    print(name,'floor',round(float(floor),3))
