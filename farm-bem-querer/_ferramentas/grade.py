import sys
from PIL import Image, ImageDraw
d, out, fs = sys.argv[1], sys.argv[2], sys.argv[3:]
W = 900; out_im = Image.new('RGB', (W * 2, 660 * ((len(fs) + 1) // 2)), 'white')
for i, f in enumerate(fs):
    im = Image.open(d + '/' + f).convert('RGB'); im.thumbnail((890, 640))
    x, y = (i % 2) * W, (i // 2) * 660
    out_im.paste(im, (x, y)); g = ImageDraw.Draw(out_im)
    for gx in range(0, im.width, 100):
        g.line([(x + gx, y), (x + gx, y + im.height)], fill=(255, 0, 255)); g.text((x + gx + 2, y + 2), str(gx), fill=(255, 0, 255))
    for gy in range(0, im.height, 100):
        g.line([(x, y + gy), (x + im.width, y + gy)], fill=(255, 0, 255)); g.text((x + 2, y + gy + 2), str(gy), fill=(255, 0, 255))
    g.text((x + 5, y + im.height - 14), f + ' %dx%d' % im.size, fill=(255, 255, 0))
out_im.save(out, quality=82)
