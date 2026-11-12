# Trata os objetos recortados (obj/c*.png, rembg birefnet-general) na paleta da EMS:
# mapa de gradiente pela luminância, alfa preservado, recorte na caixa do objeto e ampliação.
from PIL import Image, ImageFilter
import numpy as np
H = lambda h: np.array([int(h[i:i+2], 16) for i in (1, 3, 5)], float)
NOITE = [(0, '#2a1433'), (.16, '#3d1c46'), (.40, '#5b216c'), (.60, '#7b4df2'), (.80, '#c0a5c4'), (1, '#fffbde')]
MANT  = [(0, '#2a1433'), (.20, '#3d1c46'), (.44, '#5b216c'), (.62, '#7b4df2'), (.80, '#f2cf7a'), (1, '#fffbde')]
def mapa(g, stops):
    out = np.zeros(g.shape + (3,))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        m = (g >= a) & (g <= b); t = ((g - a) / (b - a))[m][:, None]
        out[m] = H(ca) * (1 - t) + H(cb) * t
    return out.astype('uint8')
for i, escala, tema, ganho in [(1, 1.5, NOITE, 1.75), (3, 1.0, NOITE, 1.12), (4, 1.0, NOITE, 1.3), (5, 1.22, NOITE, 1.12), (6, 1.3, MANT, 1.12)]:
    im = Image.open(f'obj/c{i}.png'); box = im.getbbox(); im = im.crop(box)
    if i == 6:                                               # envelope: tira os ramos da frente e fecha o retângulo
        import cv2
        rgb = np.asarray(im.convert('RGB')).copy(); al = np.asarray(im.getchannel('A'))
        h, w = al.shape
        xs = np.where(al[int(h * .08)] > 128)[0]; ys = np.where(al[:, w // 2] > 128)[0]
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        lum = np.asarray(im.convert('L')).astype(float)
        escuro = (lum < 150).astype('uint8')
        yy, xx = np.mgrid[:h, :w]
        selo = (xx - w * .51) ** 2 + (yy - h * .497) ** 2 < (w * .085) ** 2
        escuro[selo] = 0; escuro[: int(h * .45)] = 0             # só a metade de baixo, fora do lacre
        escuro[al < 128] = 1
        escuro = cv2.dilate(escuro, np.ones((9, 9), 'uint8'))
        escuro[selo] = 0
        rgb = cv2.inpaint(rgb, escuro, 9, cv2.INPAINT_TELEA)
        rgb = cv2.GaussianBlur(rgb, (0, 0), 1.2) * escuro[..., None] + rgb * (1 - escuro[..., None])
        lum2 = rgb.mean(axis=2); baixo = (yy > h * .45) & ~selo
        med = np.median(rgb[baixo & (lum2 > 190)], axis=0)        # cor do papel
        t = np.clip((med.mean() - lum2) / 40, 0, 1)[..., None] * baixo[..., None]
        rgb = rgb * (1 - t) + med * t                              # apaga manchas e sombra de baixo
        novo = np.zeros((h, w), 'uint8'); novo[y0:y1 + 1, x0:x1 + 1] = 255
        im = Image.fromarray(rgb.astype('uint8')).convert('RGBA'); im.putalpha(Image.fromarray(novo))
    a = np.asarray(im.getchannel('A'), float) / 255
    a = np.clip((a - .35) / .45, 0, 1)                      # borda firme, sem auréola
    g = np.asarray(im.convert('L'), float) / 255
    g = np.clip((g - .06) * ganho, 0, 1) ** .9
    out = Image.fromarray(mapa(g, tema)).convert('RGBA')
    out.putalpha(Image.fromarray((a * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(.6)))
    if escala != 1:
        out = out.resize((round(out.width * escala), round(out.height * escala)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
    out.save(f'obj/o{i}.png'); print(i, box, out.size)
