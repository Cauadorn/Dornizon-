# Primeira passada: máscara de tudo que é objeto e onde ficam as peças (ponteiro, peças no ar, palavra).
import sys, numpy as np, cv2
from PIL import Image
from rembg import remove, new_session
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB'); a = np.array(im)
fg = np.array(remove(im, session=new_session('isnet-general-use'), only_mask=True))
cv2.imwrite(out + '/fg.png', fg)
hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)
pink = ((hsv[..., 0] > 150) & (hsv[..., 0] < 172) & (hsv[..., 1] > 110) & (hsv[..., 2] > 120)).astype(np.uint8) * 255
cv2.imwrite(out + '/pink.png', pink)
n, lab, st, cen = cv2.connectedComponentsWithStats((fg > 128).astype(np.uint8))
for i in range(1, n):
    if st[i, 4] > 300: print('fg comp', i, st[i].tolist())
n, lab, st, cen = cv2.connectedComponentsWithStats(pink)
for i in range(1, n):
    if st[i, 4] > 400: print('pink comp', i, st[i].tolist())
