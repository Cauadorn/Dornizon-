"""Carimba a marca na foto do saco de papel: perspectiva, tinta que falha e que pega a textura do papel.

Uso: python3 padaria-taylor/_ferramentas/mockup.py
Precisa do carimbo em PNG (gerado por png.js) e das fotos em fotos-geradas/.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

RAIZ = Path(__file__).resolve().parents[1]
rng = np.random.default_rng(13)


def ruido(h, w, escalas=((4, 1.0), (16, 0.5), (60, 0.25))):
    """Ruído suave em várias escalas (0..1)."""
    total = np.zeros((h, w), np.float32)
    peso = 0
    for passo, amp in escalas:
        gh, gw = max(2, h // passo), max(2, w // passo)
        g = Image.fromarray((rng.random((gh, gw)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        total += np.asarray(g, np.float32) / 255 * amp
        peso += amp
    return total / peso


def gasta(alpha, forca=0.55):
    """Tinta de carimbo: falhas grandes e pequenas, borda mais cheia que o meio."""
    h, w = alpha.shape
    a = alpha.astype(np.float32) / 255
    n = ruido(h, w)
    falha_grande = np.clip((n - 0.38) * 3.2, 0, 1)  # manchas mais claras
    pontos = (rng.random((h, w)) > 0.06).astype(np.float32)  # poeira
    pontos = np.asarray(Image.fromarray((pontos * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)), np.float32) / 255
    a = a * (1 - forca * (1 - falha_grande)) * (0.55 + 0.45 * pontos)
    return np.clip(a, 0, 1)


def coeficientes(origem, destino):
    """Coeficientes de PERSPECTIVE do PIL (mapeia destino -> origem)."""
    m = []
    for (x, y), (u, v) in zip(destino, origem):
        m.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        m.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    A = np.array(m, np.float64)
    b = np.array(origem, np.float64).reshape(8)
    return np.linalg.solve(A, b)


def carimbar(foto, carimbo_png, quad, cor=(38, 60, 135), opacidade=0.9, rot=-4, forca=0.45, desfoque=0.6, saida=None):
    base = foto if isinstance(foto, Image.Image) else Image.open(foto).convert("RGB")
    W, H = base.size
    st = Image.open(carimbo_png).convert("RGBA").rotate(rot, resample=Image.BICUBIC, expand=True)
    sw, sh = st.size
    alpha = gasta(np.asarray(st)[:, :, 3], forca) if forca else np.asarray(st)[:, :, 3].astype(np.float32) / 255
    st_a = Image.fromarray((alpha * 255).astype(np.uint8))
    c = coeficientes([(0, 0), (sw, 0), (sw, sh), (0, sh)], quad)
    a_warp = st_a.transform((W, H), Image.PERSPECTIVE, tuple(c), Image.BICUBIC)
    a = np.asarray(a_warp.filter(ImageFilter.GaussianBlur(desfoque)), np.float32) / 255

    # a tinta pega menos onde a fibra do papel está alta
    cinza = np.asarray(base.convert("L"), np.float32)
    alto = cinza - np.asarray(base.convert("L").filter(ImageFilter.GaussianBlur(3)), np.float32)
    a = a * np.clip(1 - alto / 40, 0.55, 1.0) * opacidade

    px = np.asarray(base, np.float32)
    tinta = np.array(cor, np.float32) / 255
    multiplicado = px * tinta  # multiply: a luz da cena continua valendo
    out = px * (1 - a[..., None]) + multiplicado * a[..., None]
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    if saida:
        img.save(saida)
    return img


def recorte_4x5(img, cx, larg, saida, alvo=(1080, 1350)):
    W, H = img.size
    alt = H
    larg = int(alt * 4 / 5)
    x0 = int(min(max(cx - larg / 2, 0), W - larg))
    r = img.crop((x0, 0, x0 + larg, alt)).resize(alvo, Image.LANCZOS)
    r = r.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    # grão de filme por cima, para esconder a ampliação
    g = rng.normal(0, 7, (alvo[1], alvo[0], 1)).astype(np.float32)
    arr = np.clip(np.asarray(r, np.float32) + g, 0, 255).astype(np.uint8)
    Image.fromarray(arr).save(saida, quality=95)


def colar(foto, png, quad, rot=0, sombra=0.35):
    """Cola um adesivo colorido na foto: perspectiva, luz da cena por cima e uma sombrinha embaixo."""
    base = foto if isinstance(foto, Image.Image) else Image.open(foto).convert("RGB")
    W, H = base.size
    st = Image.open(png).convert("RGBA")
    st = st.crop(st.getchannel("A").getbbox()).rotate(rot, resample=Image.BICUBIC, expand=True)
    sw, sh = st.size
    c = coeficientes([(0, 0), (sw, 0), (sw, sh), (0, sh)], quad)
    w = st.transform((W, H), Image.PERSPECTIVE, tuple(c), Image.BICUBIC)
    arr = np.asarray(w, np.float32)
    a = arr[..., 3:4] / 255
    # luz da cena: o quanto o papel do saco está iluminado em cada ponto
    luz = np.asarray(base.convert("L").filter(ImageFilter.GaussianBlur(25)), np.float32)[..., None]
    ref = np.percentile(luz[a[..., 0] > 0.5], 90) if (a > 0.5).any() else 200
    fator = np.clip(luz / ref, 0.35, 1.05) * 0.9
    px = np.asarray(base, np.float32)
    # sombra: o adesivo descola um tiquinho do papel
    sa = np.asarray(Image.fromarray((a[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4)), np.float32)[..., None] / 255
    sa = np.roll(sa, (3, 2), axis=(0, 1))
    px = px * (1 - sa * sombra)
    cor = arr[..., :3] * fator
    out = px * (1 - a) + cor * a
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    pasta = RAIZ / "03-mockups"
    pasta.mkdir(exist_ok=True)
    fotos = RAIZ / "fotos-geradas"
    cam = pasta / "_camadas"
    img = colar(fotos / "saco3.png", cam / "adesivo-doughgirl.png", [(408, 196), (704, 198), (706, 500), (410, 504)], rot=-5)
    img = carimbar(img, cam / "recado-original.png", [(440, 516), (690, 511), (691, 572), (441, 578)],
                   cor=(30, 48, 120), opacidade=0.9, rot=2, forca=0, desfoque=0.7)
    img.save(pasta / "saco-doughgirl.png")
    recorte_4x5(img, 560, 0, pasta / "saco-doughgirl-4x5.jpg")
    print("ok")
