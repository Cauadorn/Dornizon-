# Peças da colagem: retratos de domínio público recortados e passados para o duotone da EMS,
# papéis rasgados e estrelas de papel. uso: python3 colagem.py  (lê obras/ e recortes/*-bruto.png, escreve pecas/)
import os, numpy as np
from PIL import Image, ImageFilter, ImageChops
AQUI = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(AQUI, 'pecas'); os.makedirs(P, exist_ok=True)
hexrgb = lambda h: np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32)
COR = {k: hexrgb(v) for k, v in dict(ivory='#fffbde', tinta='#2a1433', ameixa='#3d1c46', plum='#5b216c', violeta='#6225d8', violeta2='#7b4df2',
                                      lavanda='#c0a5c4', lavanda2='#e4d6e6', pink='#dd34a8', manteiga='#f2cf7a').items()}

def duotone(im, paradas=('tinta', 'plum', 'lavanda', 'ivory'), contraste=1.25, grao=9, semente=1):
    """Luminância da pintura vira um degrau de cores da marca; grão de impressão por cima."""
    a = np.asarray(im.convert('L')).astype(np.float32) / 255
    lo, hi = np.percentile(a, 2), np.percentile(a, 98)
    a = np.clip((a - lo) / (hi - lo + 1e-6), 0, 1)
    a = np.clip((a - .5) * contraste + .5, 0, 1)
    xs = np.linspace(0, 1, len(paradas))
    out = np.stack([np.interp(a, xs, [COR[p][c] for p in paradas]) for c in range(3)], -1)
    out += np.random.default_rng(semente).normal(0, grao, out.shape[:2])[..., None]
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))

def recorte(nome, caixa=None, largura=1000, **kw):
    """Recorte do rembg: borda dura (sem pelo vazando), duotone, tamanho final."""
    im = Image.open(os.path.join(AQUI, 'recortes', nome + '-bruto.png'))
    if caixa: im = im.crop(tuple(int(v * s) for v, s in zip(caixa, (im.width, im.height, im.width, im.height))))
    al = np.asarray(im.split()[3]).astype(np.float32)
    al = np.clip((al - 90) / 80, 0, 1) * 255
    al = Image.fromarray(al.astype(np.uint8)).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(.8))
    bb = al.point(lambda v: 255 if v > 40 else 0).getbbox()
    cor = duotone(im.convert('RGB'), **kw); cor.putalpha(al); cor = cor.crop(bb)
    e = largura / cor.width
    return cor.resize((largura, round(cor.height * e)), Image.LANCZOS)

def rasgado(w, h, semente=1, forca=14):
    """Máscara de papel rasgado nos quatro lados."""
    r = np.random.default_rng(semente)
    def perfil(n):
        x = np.arange(n); p = np.zeros(n)
        for passo, amp in ((120, .5), (34, .3), (7, .2)):
            pts = r.random(n // passo + 3); p += amp * np.interp(x / passo, np.arange(len(pts)), pts)
        return (p - p.min()) / (p.max() - p.min() + 1e-6) * forca
    yy, xx = np.mgrid[0:h, 0:w]
    m = (yy >= perfil(w)[None, :]) & (yy <= h - 1 - perfil(w)[None, :]) & (xx >= perfil(h)[:, None]) & (xx <= w - 1 - perfil(h)[:, None])
    return m

def papel(w, h, cor='ivory', semente=1, forca=14, fibra=7):
    """Pedaço de papel rasgado, com fibra e a beirada mais clara (o miolo do papel aparecendo)."""
    r = np.random.default_rng(semente + 100)
    m = rasgado(w, h, semente, forca)
    dentro = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(9))) > 0
    base = np.ones((h, w, 3), np.float32) * COR[cor]
    ruido = np.asarray(Image.fromarray((r.random((h // 3 + 1, w // 3 + 1)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) / 255 - .5
    fino = r.normal(0, 1, (h, w))
    base += (ruido * fibra * 2 + fino * fibra * .6)[..., None]
    base[m & ~dentro] = base[m & ~dentro] * .35 + np.array([255, 253, 240]) * .65
    return Image.fromarray(np.dstack([base.clip(0, 255), m * 255]).astype(np.uint8))

def foto_rasgada(nome, caixa, w, h, semente=1, **kw):
    """Pedaço da pintura como papel rasgado (para quando o recorte da figura não fecha)."""
    im = Image.open(os.path.join(AQUI, 'obras', nome + '.jpg')).convert('RGB')
    im = im.crop(tuple(int(v * s) for v, s in zip(caixa, (im.width, im.height, im.width, im.height)))).resize((w, h), Image.LANCZOS)
    cor = np.asarray(duotone(im, **kw)).astype(np.float32)
    m = rasgado(w, h, semente, 18)
    dentro = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(13))) > 0
    cor[m & ~dentro] = (255, 251, 222)
    return Image.fromarray(np.dstack([cor, m * 255]).astype(np.uint8))

def estrela(tam, cor='manteiga', semente=1):
    """Brilho da marca recortado em papel."""
    m = Image.open(os.path.join(AQUI, 'assets', 'i-brilho.png')).convert('RGBA').split()[3].resize((tam, tam), Image.LANCZOS)
    p = papel(tam, tam, cor, semente, forca=0, fibra=9).convert('RGB'); p.putalpha(m)
    return p

sal = lambda im, n: (im.save(os.path.join(P, n)), print(n, im.size))

# retratos recortados
sal(recorte('mona-lisa', largura=980), 'mona.png')
sal(recorte('rembrandt', largura=900, semente=3), 'rembrandt.png')
sal(recorte('vigee', largura=980, semente=4), 'vigee.png')
sal(foto_rasgada('grito', (.22, .40, .82, .98), 560, 680, semente=5, contraste=1.3), 'grito.png')
sal(recorte('venus', caixa=(0, 0, 1, .27), largura=860, semente=6), 'venus.png')
sal(recorte('arnolfini', largura=900, semente=7, contraste=1.4), 'arnolfini.png')
# retratos em pedaço de papel rasgado
sal(foto_rasgada('moca-brinco', (.08, .04, .92, .86), 760, 890, semente=8), 'moca.png')
sal(foto_rasgada('van-gogh', (.10, .06, .90, .82), 760, 860, semente=9, contraste=1.35), 'vangogh.png')
# papéis
for nome, w, h, cor, s in [('tira-a', 560, 96, 'ivory', 1), ('tira-b', 700, 100, 'ivory', 2), ('tira-c', 820, 104, 'ivory', 3), ('tira-plum', 760, 100, 'plum', 4),
                           ('tira-manteiga', 520, 96, 'manteiga', 5), ('cartao-ivory', 760, 430, 'ivory', 6), ('cartao-plum', 780, 380, 'plum', 7),
                           ('venda', 620, 150, 'ivory', 8), ('tira-pink', 480, 110, 'pink', 9), ('faixa-lavanda', 1200, 420, 'lavanda', 10), ('faixa-violeta', 1200, 520, 'violeta', 11)]:
    sal(papel(w, h, cor, s), nome + '.png')
for i, (t, c) in enumerate([(150, 'manteiga'), (110, 'manteiga'), (90, 'ivory'), (130, 'pink'), (100, 'lavanda')]):
    sal(estrela(t, c, i), f'estrela-{i + 1}.png')
