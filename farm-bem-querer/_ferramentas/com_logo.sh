#!/bin/bash
# uso: com_logo.sh arte.png UF ink saida_dir  -> mede a faixa da base, compõe e confere o centro
set -e
ART=$1; UF=$2; INK=$3; OUT=$4
read FX LG <<< $(python3 -I - "$ART" <<'PY'
import sys
from PIL import Image
import numpy as np
im=np.asarray(Image.open(sys.argv[1]).convert('RGB'),np.float32)
H=im.shape[0]
base=im[-6:, 100:-100].reshape(-1,3).mean(0)
row=im[:, 100:-100].mean(1)
d=np.abs(row-base).sum(1)
y=H-1
while y>0 and d[y]<40: y-=1
fh=(H-1-y)/H
lw=(fh*H*0.60)/0.4625/im.shape[1]
print(round(fh,4), round(lw,4))
PY
)
echo "faixa=$FX largura=$LG"
./venv/bin/python -I compor.py "$ART" "$UF" "$OUT" --pos faixa --faixa $FX --largura $LG --ink "$INK"
B=$(basename "$ART" .png)
python3 -I - "$OUT/${B}__com-logo.png" "$OUT/${B}__sem-logo.png" <<'PY'
import sys
from PIL import Image
import numpy as np
a=np.asarray(Image.open(sys.argv[1]).convert('RGB'),np.float32); b=np.asarray(Image.open(sys.argv[2]).convert('RGB'),np.float32)
ys,xs=np.where(np.abs(a-b).sum(2)>30)
print('logo centro x',(xs.min()+xs.max())/2,'de',a.shape[1]/2,'| margem baixo',a.shape[0]-1-ys.max())
PY
