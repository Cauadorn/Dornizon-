# Aplica as artes planas (artes/*.png) nas cenas em branco (../ia/mockups/base-*.png),
# com perspectiva, curvatura (canecas) e a luz/sombra da própria foto.
# uso: python3 -I compor.py  -> final/mockup-*.png
import os
import numpy as np
import cv2

AQUI = os.path.dirname(os.path.abspath(__file__))
BASES = os.path.join(AQUI, '..', 'ia', 'mockups')
ARTES = os.path.join(AQUI, 'artes')
FINAL = os.path.join(AQUI, 'final')
os.makedirs(FINAL, exist_ok=True)
DEP = os.path.join(AQUI, 'depuracao')
os.makedirs(DEP, exist_ok=True)

def ler(p, alfa=False):
    im = cv2.imread(p, cv2.IMREAD_UNCHANGED)
    if alfa and im.shape[2] == 3:
        im = np.dstack([im, np.full(im.shape[:2], 255, np.uint8)])
    return im

def maior_componente(mask, n=1):
    num, lab, st, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    ordem = np.argsort(-st[1:, cv2.CC_STAT_AREA])[:n] + 1
    return [(lab == i) for i in ordem]

def quadrilatero(mask):
    cs, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)
    h = cv2.convexHull(c)
    per = cv2.arcLength(h, True)
    for eps in np.linspace(0.005, 0.08, 60):
        ap = cv2.approxPolyDP(h, eps * per, True)
        if len(ap) == 4:
            return ap.reshape(4, 2).astype(np.float32)
    r = cv2.minAreaRect(c)
    return cv2.boxPoints(r).astype(np.float32)

def ordenar(q, retrato=False):
    """ordena os cantos (sentido horário) começando de forma que o 1º lado seja o lado longo (ou curto,
    se retrato) e aponte para a direita."""
    c = q.mean(0)
    ang = np.arctan2(q[:, 1] - c[1], q[:, 0] - c[0])
    q = q[np.argsort(ang)]                       # horário na imagem (y para baixo)
    melhor = None
    for s in range(4):
        r = np.roll(q, -s, axis=0)
        e0 = r[1] - r[0]; e1 = r[2] - r[1]
        longo = np.linalg.norm(e0) >= np.linalg.norm(e1)
        if longo == (not retrato) and e0[0] > 0:
            ang0 = abs(np.degrees(np.arctan2(e0[1], e0[0])))
            if melhor is None or ang0 < melhor[0]:
                melhor = (ang0, r)
    return melhor[1] if melhor else q

def luz(base, mask, pct=97):
    L = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY).astype(np.float32)
    ref = np.percentile(L[mask], pct)
    return np.clip(L / ref, 0, 1.08)

def expandir(q, f):
    c = q.mean(0)
    return (c + (q - c) * (1 + f)).astype(np.float32)

def crescer_no_papel(base, mask, n=4):
    hsv = cv2.cvtColor(base, cv2.COLOR_BGR2HSV).astype(np.int32)
    papel = (hsv[..., 1] < 16) & (hsv[..., 2] > 150)
    m = mask.astype(np.uint8)
    for _ in range(n):
        m = (cv2.dilate(m, np.ones((3, 3), np.uint8)).astype(bool) & (papel | m.astype(bool))).astype(np.uint8)
    return m.astype(bool)

def aplicar_plano(base, mask, quad, arte, borda_bgr):
    mask = crescer_no_papel(base, mask)
    H, W = base.shape[:2]
    h, w = arte.shape[:2]
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    M = cv2.getPerspectiveTransform(src, quad)
    warp = cv2.warpPerspective(arte, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    a = warp[..., 3:4].astype(np.float32) / 255
    cor = warp[..., :3].astype(np.float32) * a + np.array(borda_bgr, np.float32) * (1 - a)  # lateral do papel na cor da arte
    sh = luz(base, mask)[..., None]
    m = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 0.8)[..., None]
    out = base.astype(np.float32) * (1 - m) + np.clip(cor * sh, 0, 255) * m
    return out

def depurar(nome, base, quads):
    d = base.copy()
    for q in quads:
        cv2.polylines(d, [q.astype(np.int32)], True, (0, 0, 255), 2)
        cv2.circle(d, tuple(q[0].astype(int)), 8, (0, 255, 0), -1)
    cv2.imwrite(os.path.join(DEP, nome + '.jpg'), d)

def mascara_branca(base, lim_l=200, lim_s=40):
    hsv = cv2.cvtColor(base, cv2.COLOR_BGR2HSV)
    m = (hsv[..., 2] > lim_l) & (hsv[..., 1] < lim_s)
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    return m.astype(bool)

# ------------------------------------------------------------------ cartões
def cartoes():
    base = ler(os.path.join(BASES, 'base-cartoes.png'))
    m = mascara_branca(base, 205, 9)
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8)).astype(bool)
    comps = maior_componente(m, 2)
    comps.sort(key=lambda c: np.nonzero(c)[0].mean())         # de cima para baixo
    quads = [ordenar(quadrilatero(c)) for c in comps]
    depurar('cartoes', base, quads)
    out = base.astype(np.float32)
    for c, q, nome, borda in zip(comps, quads, ['cartao-frente', 'cartao-verso'], [(194, 66, 39), (168, 198, 243)]):
        out = aplicar_plano(out.astype(np.uint8), c, expandir(q, .014), ler(os.path.join(ARTES, nome + '.png'), True), borda)
    cv2.imwrite(os.path.join(DEP, 'mockup-cartoes-obj.png'), ((comps[0] | comps[1]) * 255).astype(np.uint8))
    cv2.imwrite(os.path.join(FINAL, 'mockup-cartoes.png'), out.astype(np.uint8))

# ------------------------------------------------------------------ calendário
def calendario():
    base = ler(os.path.join(BASES, 'base-calendario.png'))
    m = mascara_branca(base, 215, 7)
    c = maior_componente(m, 1)[0]
    q = ordenar(quadrilatero(c), retrato=True)
    depurar('calendario', base, [q])
    out = aplicar_plano(base, c, expandir(q, .045), ler(os.path.join(ARTES, 'calendario.png'), True), (194, 66, 39))
    V = cv2.cvtColor(base, cv2.COLOR_BGR2HSV)[..., 2]
    preto = maior_componente(cv2.morphologyEx((V < 90).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)).astype(bool), 1)[0]
    cv2.imwrite(os.path.join(DEP, 'mockup-calendario-obj.png'), ((c | preto) * 255).astype(np.uint8))
    cv2.imwrite(os.path.join(FINAL, 'mockup-calendario.png'), out.astype(np.uint8))

# ------------------------------------------------------------------ canecas (estampa enrolada no cilindro)
def caneca(out, base, mask, arte, alt_frac=0.5, cy_frac=0.52, op=0.96):
    ys, xs = np.nonzero(mask)
    # corpo = colunas onde a máscara é alta (a alça cobre poucas linhas)
    cols = np.array([mask[:, x].sum() for x in range(base.shape[1])])
    corpo = cols > cols.max() * 0.72
    xi = np.nonzero(corpo)[0]
    x0, x1 = xi.min(), xi.max()
    cx, R = (x0 + x1) / 2, (x1 - x0) / 2
    linhas = np.nonzero(mask[:, int(cx)])[0]
    y0, y1 = linhas.min(), linhas.max()
    hc = y1 - y0
    h, w = arte.shape[:2]
    alt = hc * alt_frac
    k = alt / h                                  # pixels de arco por pixel da arte
    yc = y0 + hc * cy_frac
    Y, X = np.mgrid[0:base.shape[0], 0:base.shape[1]].astype(np.float32)
    s = np.clip((X - cx) / R, -0.999, 0.999)
    u = np.arcsin(s) * R                          # comprimento de arco a partir do centro
    mapx = (u / k + w / 2).astype(np.float32)
    mapy = ((Y - yc) / k + h / 2).astype(np.float32)
    est = cv2.remap(arte, mapx, mapy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    dentro = mask & (np.abs(X - cx) < R * 0.97)
    a = est[..., 3].astype(np.float32) / 255 * dentro * op
    a *= np.clip((1 - np.abs(s)) * 6, 0, 1)       # some suavemente na curva
    L = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY).astype(np.float32)
    ref = np.median(L[dentro])
    sh = np.clip(L / ref, 0.55, 1.6)[..., None]
    cor = np.clip(est[..., :3].astype(np.float32) * np.minimum(sh, 1) + 255 * np.maximum(sh - 1, 0) * 0.6, 0, 255)
    return out * (1 - a[..., None]) + cor * a[..., None]

def canecas():
    base = ler(os.path.join(BASES, 'base-canecas.png'))
    hsv = cv2.cvtColor(base, cv2.COLOR_BGR2HSV).astype(np.int32)
    H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    azul = (H > 100) & (H < 130) & (S > 90)
    pes = (H > 5) & (H < 22) & (S > 45) & (V > 150)
    azul = maior_componente(cv2.morphologyEx(azul.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8)).astype(bool), 1)[0]
    pes = maior_componente(cv2.morphologyEx(pes.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8)).astype(bool), 1)[0]
    cv2.imwrite(os.path.join(DEP, 'canecas-mask.png'), (azul * 255 + pes * 128).astype(np.uint8))
    out = base.astype(np.float32)
    out = caneca(out, base, azul, ler(os.path.join(ARTES, 'caneca-cobalto.png'), True), alt_frac=0.62, cy_frac=0.53)
    out = caneca(out, base, pes, ler(os.path.join(ARTES, 'caneca-pessego.png'), True), alt_frac=0.66, cy_frac=0.53)
    cv2.imwrite(os.path.join(DEP, 'mockup-canecas-obj.png'), ((azul | pes) * 255).astype(np.uint8))
    cv2.imwrite(os.path.join(FINAL, 'mockup-canecas.png'), np.clip(out, 0, 255).astype(np.uint8))

if __name__ == '__main__':
    cartoes(); calendario(); canecas()
    print('ok', sorted(os.listdir(FINAL)))

# ------------------------------------------------------------------ enquadramento centralizado (4:5, 1080x1350)
def enquadrar(nome, margem=0.2):
    im = cv2.imread(os.path.join(FINAL, nome))
    obj = cv2.imread(os.path.join(DEP, nome.replace('.png', '-obj.png')), 0) > 127
    H, W = im.shape[:2]
    ys, xs = np.nonzero(obj)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w = max((x1 - x0) * (1 + 2 * margem), (y1 - y0) * (1 + 2 * margem) * 0.8)
    w = min(w, W, H * 0.8)
    h = w / 0.8
    xa = min(max(cx - w / 2, 0), W - w)      # desloca para dentro da imagem, sem cortar o objeto
    ya = min(max(cy - h / 2, 0), H - h)
    xa, ya = int(round(xa)), int(round(ya))
    rec = im[ya:ya + int(round(h)), xa:xa + int(round(w))]
    out = cv2.resize(rec, (1080, 1350), interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite(os.path.join(FINAL, nome), out)
    print('enquadrado', nome, 'objeto', (x0, y0, x1, y1), 'janela', (xa, ya, int(w), int(h)))

if __name__ == '__main__':
    for n in ['mockup-cartoes.png', 'mockup-canecas.png', 'mockup-calendario.png']:
        enquadrar(n)
