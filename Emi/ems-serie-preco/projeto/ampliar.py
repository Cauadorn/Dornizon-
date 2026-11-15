# Amplia 2x as camadas da capa com Real-ESRGAN (x2plus), no próprio lugar, para o vídeo sair nítido.
# As imagens geradas têm 1024 px; ampliadas na arte, ficam macias. O tamanho na tela não muda: o HTML fixa a largura de cada camada.
# uso: python ampliar.py <modelo.pth> <pasta> <arquivo1.png> [arquivo2.png ...]
import sys, os, numpy as np, cv2, torch, torch.nn as nn, torch.nn.functional as F
class RDB(nn.Module):
    def __init__(s, nf=64, gc=32):
        super().__init__(); s.conv1 = nn.Conv2d(nf, gc, 3, 1, 1); s.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1); s.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1)
        s.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1); s.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1); s.l = nn.LeakyReLU(0.2, True)
    def forward(s, x):
        x1 = s.l(s.conv1(x)); x2 = s.l(s.conv2(torch.cat((x, x1), 1))); x3 = s.l(s.conv3(torch.cat((x, x1, x2), 1)))
        x4 = s.l(s.conv4(torch.cat((x, x1, x2, x3), 1))); return s.conv5(torch.cat((x, x1, x2, x3, x4), 1)) * 0.2 + x
class RRDB(nn.Module):
    def __init__(s): super().__init__(); s.rdb1, s.rdb2, s.rdb3 = RDB(), RDB(), RDB()
    def forward(s, x): return s.rdb3(s.rdb2(s.rdb1(x))) * 0.2 + x
class Net(nn.Module):   # RRDBNet, escala 2 (entrada com pixel-unshuffle)
    def __init__(s):
        super().__init__(); s.conv_first = nn.Conv2d(12, 64, 3, 1, 1); s.body = nn.Sequential(*[RRDB() for _ in range(23)]); s.conv_body = nn.Conv2d(64, 64, 3, 1, 1)
        s.conv_up1 = nn.Conv2d(64, 64, 3, 1, 1); s.conv_up2 = nn.Conv2d(64, 64, 3, 1, 1); s.conv_hr = nn.Conv2d(64, 64, 3, 1, 1); s.conv_last = nn.Conv2d(64, 3, 3, 1, 1); s.l = nn.LeakyReLU(0.2, True)
    def forward(s, x):
        f = s.conv_first(F.pixel_unshuffle(x, 2)); f = f + s.conv_body(s.body(f))
        f = s.l(s.conv_up1(F.interpolate(f, scale_factor=2, mode='nearest'))); f = s.l(s.conv_up2(F.interpolate(f, scale_factor=2, mode='nearest')))
        return s.conv_last(s.l(s.conv_hr(f)))
net = Net(); sd = torch.load(sys.argv[1], map_location='cpu'); net.load_state_dict(sd.get('params_ema', sd.get('params', sd)), strict=True); net.eval()
@torch.no_grad()
def x2(rgb):   # rgb uint8 HxWx3 -> 2H x 2W, em blocos com sobra pra não marcar emenda
    h, w = rgb.shape[:2]; ph, pw = (-h) % 2, (-w) % 2; im = np.pad(rgb, ((0, ph), (0, pw), (0, 0)), mode='edge')
    t = torch.from_numpy(im.astype(np.float32) / 255).permute(2, 0, 1)[None]; H, W = t.shape[2:]; out = torch.zeros(1, 3, H * 2, W * 2); T, B = 256, 16
    for y in range(0, H, T):
        for x in range(0, W, T):
            y0, x0, y1, x1 = max(y - B, 0), max(x - B, 0), min(y + T + B, H), min(x + T + B, W)
            y0 -= (y - y0) % 2; x0 -= (x - x0) % 2; y1 += (y1 - y0) % 2 and (1 if y1 < H else -1); x1 += (x1 - x0) % 2 and (1 if x1 < W else -1)
            o = net(t[:, :, y0:y1, x0:x1]); ye, xe = min(y + T, H), min(x + T, W)
            out[:, :, y * 2:ye * 2, x * 2:xe * 2] = o[:, :, (y - y0) * 2:(ye - y0) * 2, (x - x0) * 2:(xe - x0) * 2]
    return (out[0].clamp(0, 1).permute(1, 2, 0).numpy() * 255 + .5).astype(np.uint8)[:h * 2, :w * 2]
d = sys.argv[2]
for nome in sys.argv[3:]:
    p = os.path.join(d, nome); im = cv2.imread(p, cv2.IMREAD_UNCHANGED)
    if im.ndim == 3 and im.shape[2] == 4:
        a = im[..., 3]; cor = im[..., :3].copy()
        if (a < 255).any():   # espalha a cor da borda pra dentro do transparente: a ampliação não puxa halo escuro
            cor = cv2.inpaint(cor, (a < 8).astype(np.uint8) * 255, 4, cv2.INPAINT_TELEA) if (a < 8).mean() < .6 else cor
        r = x2(cv2.cvtColor(cor, cv2.COLOR_BGR2RGB)); al = x2(np.dstack([a, a, a]))[..., 0]
        cv2.imwrite(p, np.dstack([cv2.cvtColor(r, cv2.COLOR_RGB2BGR), al]))
    else:
        r = x2(cv2.cvtColor(im[..., :3], cv2.COLOR_BGR2RGB)); cv2.imwrite(p, cv2.cvtColor(r, cv2.COLOR_RGB2BGR))
    print(nome, im.shape[1], 'x', im.shape[0], '->', im.shape[1] * 2, 'x', im.shape[0] * 2, flush=True)
