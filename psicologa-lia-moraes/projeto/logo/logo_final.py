# Monta os arquivos finais do logo da Lia Moraes (texto convertido em contorno).
# Monograma "lm" (vetorizado de esbocos/monograma-vetor.svg) + "Lia Moraes" em Playfair Display
# + "PSICÓLOGA" em Jost fina e espaçada.
# uso: python3 -I logo_final.py   -> logo/final/*.svg
import io, os, re
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, 'fontes-base')
FINAL = os.path.join(AQUI, 'final')
os.makedirs(FINAL, exist_ok=True)

COBALTO, CREME, PESSEGO = '#2742C2', '#F5EEE3', '#F3C6A8'

class Fonte:
    def __init__(self, arquivo, eixos):
        f = instantiateVariableFont(TTFont(os.path.join(BASE, arquivo)), eixos)
        b = io.BytesIO(); f.flavor = None; f.save(b)
        self.tt = TTFont(io.BytesIO(b.getvalue()))
        self.hb = hb.Font(hb.Face(b.getvalue()))
        self.upm = self.tt['head'].unitsPerEm
        self.gs = self.tt.getGlyphSet()
        self.ordem = self.tt.getGlyphOrder()

    def texto(self, s, tam, x=0, y=0, track=0.0):
        """retorna (path d em y-para-baixo, largura) do texto com kerning da fonte e espaçamento extra (em em)."""
        buf = hb.Buffer(); buf.add_str(s); buf.guess_segment_properties()
        hb.shape(self.hb, buf, {'kern': True, 'liga': True})
        k = tam / self.upm
        pen = SVGPathPen(self.gs)
        cx = 0
        n = len(buf.glyph_infos)
        for i, (inf, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
            nome = self.ordem[inf.codepoint]
            gx = x + (cx + pos.x_offset) * k
            gy = y - pos.y_offset * k
            self.gs[nome].draw(TransformPen(pen, (k, 0, 0, -k, gx, gy)))
            cx += pos.x_advance + (track * self.upm if i < n - 1 else 0)
        return pen.getCommands(), cx * k

    def caixa_alta(self):
        return self.tt['OS/2'].sCapHeight / self.upm

PLAYFAIR = Fonte('PlayfairDisplay-normal.woff2', {'wght': 400})
JOST = Fonte('Jost-normal.woff2', {'wght': 300})

# monograma: path do potrace + caixa real da tinta
svg_m = open(os.path.join(AQUI, 'esbocos', 'monograma-vetor.svg')).read()
D_MONO = re.search(r' d="([^"]+)"', svg_m).group(1)
nums = [float(v) for v in re.findall(r'-?\d+\.?\d*', D_MONO)]
xs, ys = nums[0::2], nums[1::2]
MX0, MY0, MX1, MY1 = min(xs), min(ys), max(xs), max(ys)
# centro de massa da tinta (medido na vetorização) -> centralização ótica
CENT_X, CENT_Y = 1780.8, 2017.9
PESO = 0.7
OPT_X = (MX0 + MX1) / 2 + PESO * (CENT_X - (MX0 + MX1) / 2)
OPT_Y = (MY0 + MY1) / 2 + PESO * (CENT_Y - (MY0 + MY1) / 2)

def monograma(cx, topo, altura, cy=None):
    """<path> do monograma escalado para 'altura', com o centro ótico em cx (e em cy, se dado; senão topo em 'topo')."""
    k = altura / (MY1 - MY0)
    larg = (MX1 - MX0) * k
    tx = cx - OPT_X * k
    ty = (cy - OPT_Y * k) if cy is not None else (topo - MY0 * k)
    return f'<path transform="translate({tx:.2f} {ty:.2f}) scale({k:.5f})" d="{D_MONO}"/>', larg

def arquivo(nome, corpo, vb, cor, fundo=None, raio=None):
    x0, y0, w, h = vb
    bg = ''
    if fundo and raio:
        bg = f'<circle cx="{x0 + w/2}" cy="{y0 + h/2}" r="{raio}" fill="{fundo}"/>'
    elif fundo:
        bg = f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{fundo}"/>'
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.1f} {y0:.1f} {w:.1f} {h:.1f}">{bg}'
         f'<g fill="{cor}">{corpo}</g></svg>')
    open(os.path.join(FINAL, nome + '.svg'), 'w').write(s)

def vertical():
    H = 300                       # altura do monograma
    m, lm = monograma(0, 0, H)
    t_nome, t_psi = 56, 16
    base_nome = H + 34 + t_nome * PLAYFAIR.caixa_alta() + 4
    d_nome, w_nome = PLAYFAIR.texto('Lia Moraes', t_nome)
    d_nome, w_nome = PLAYFAIR.texto('Lia Moraes', t_nome, x=-w_nome / 2, y=base_nome)
    base_psi = base_nome + 22 + t_psi * JOST.caixa_alta() + 6
    _, w_psi = JOST.texto('PSICÓLOGA', t_psi, track=.7)
    d_psi, _ = JOST.texto('PSICÓLOGA', t_psi, x=-w_psi / 2, y=base_psi, track=.7)
    corpo = m + f'<path d="{d_nome}"/><path d="{d_psi}"/>'
    k = H / (MY1 - MY0)
    mx0, mx1 = (MX0 - OPT_X) * k, (MX1 - OPT_X) * k
    meia = max(-mx0, mx1, w_nome / 2, w_psi / 2)
    pad = 60
    vb = (-meia - pad, -pad, 2 * meia + 2 * pad, base_psi + 2 * pad)
    arquivo('lia-moraes-vertical', corpo, vb, COBALTO)
    arquivo('lia-moraes-vertical-negativo', corpo, vb, CREME, COBALTO)
    arquivo('lia-moraes-vertical-pessego', corpo, vb, COBALTO, PESSEGO)

def horizontal():
    H = 200
    m, lm = monograma(lm_meio := 0, 0, H)
    t_nome, t_psi = 74, 18
    x_txt = (MX1 - OPT_X) * (H / (MY1 - MY0)) + 52
    ch = PLAYFAIR.caixa_alta() * t_nome
    bloco = ch + 30 + JOST.caixa_alta() * t_psi
    k = H / (MY1 - MY0)
    topo_txt = (OPT_Y - MY0) * k - bloco / 2
    base_nome = topo_txt + ch
    d_nome, w_nome = PLAYFAIR.texto('Lia Moraes', t_nome, x=x_txt, y=base_nome)
    base_psi = base_nome + 30 + JOST.caixa_alta() * t_psi
    d_psi, w_psi = JOST.texto('PSICÓLOGA', t_psi, x=x_txt + 3, y=base_psi, track=.7)
    corpo = m + f'<path d="{d_nome}"/><path d="{d_psi}"/>'
    pad = 50
    x0 = (MX0 - OPT_X) * k - pad
    x_txt_fim = x_txt + max(w_nome, w_psi)
    vb = (x0, -pad, x_txt_fim + pad - x0, H + 2 * pad)
    arquivo('lia-moraes-horizontal', corpo, vb, COBALTO)
    arquivo('lia-moraes-horizontal-negativo', corpo, vb, CREME, COBALTO)

def monograma_sozinho():
    H = 300
    m, lm = monograma(0, 0, H)
    pad = 40
    vb = (-lm / 2 - pad, -pad, lm + 2 * pad, H + 2 * pad)
    arquivo('lia-moraes-monograma', m, vb, COBALTO)
    # perfil: círculo cobalto com o monograma creme (opticamente um pouco acima do centro)
    R = 260
    H = 262
    m2, _ = monograma(0, 0, H, cy=0)
    arquivo('lia-moraes-perfil', m2, (-R, -R, 2 * R, 2 * R), CREME, COBALTO, raio=R)
    arquivo('lia-moraes-perfil-pessego', m2, (-R, -R, 2 * R, 2 * R), COBALTO, PESSEGO, raio=R)

vertical(); horizontal(); monograma_sozinho()
print('ok', sorted(os.listdir(FINAL)))
