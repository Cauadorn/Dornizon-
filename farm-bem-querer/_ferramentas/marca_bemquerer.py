"""Identidade Bem-Querer: símbolo (coração de duas folhas) + prancha com três caminhos de emblema.
Uso: python3 -I marca_bemquerer.py  → grava SVGs e prancha.html em 03-marca/identidade-bem-querer/
A assinatura havaianas ♥ FARM RIO segue no calcanhar; aqui é o emblema da cápsula."""
import json
import math
import os

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(P, '03-marca', 'identidade-bem-querer')
IMG = os.path.join(P, '07-apresentacao', 'site', 'img')
os.makedirs(OUT, exist_ok=True)

PAPEL, TINTA, CORACAO = '#FCFAF6', '#1D1915', '#D7262E'
FOLHA_A, FOLHA_B = '#C8321F', '#E8892B'   # amendoeira no outono carioca: vermelho e laranja


def folha(rot, cx=100, cy=178, L=150, k=1.0):
    """Folha obovada (base estreita, ponta larga e redonda), girada em torno da base."""
    pts = [(0, 0), (14 * k, -18), (44 * k, -60), (46 * k, -98), (48 * k, -128), (30 * k, -L + 2), (0, -L - 5),
           (-30 * k, -L + 2), (-48 * k, -128), (-46 * k, -98), (-44 * k, -60), (-14 * k, -18), (0, 0)]
    a = math.radians(rot)
    T = lambda p: (cx + p[0] * math.cos(a) - p[1] * math.sin(a), cy + p[0] * math.sin(a) + p[1] * math.cos(a))
    q = [T(p) for p in pts]
    d = f'M{q[0][0]:.1f},{q[0][1]:.1f}' + ''.join(
        f'C{q[i][0]:.1f},{q[i][1]:.1f} {q[i + 1][0]:.1f},{q[i + 1][1]:.1f} {q[i + 2][0]:.1f},{q[i + 2][1]:.1f}' for i in range(1, 13, 3)) + 'Z'
    n0, n1, n2 = T((0, 6)), T((2, -62)), T((0, -L + 24))
    veia = f'M{n0[0]:.1f},{n0[1]:.1f} Q{n1[0]:.1f},{n1[1]:.1f} {n2[0]:.1f},{n2[1]:.1f}'
    p0, p1 = T((0, 0)), T((0, 17))
    talo = f'M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}'
    return d, veia, talo


def simbolo(c1=FOLHA_A, c2=FOLHA_B, veia=PAPEL, fundo=PAPEL, mono=None, ang=27, k=1.18):
    """Duas folhas que caem juntas e formam um coração. mono = uma cor só (a folha da frente ganha um fio do fundo)."""
    e, ve, te = folha(-ang, k=k)
    d, vd, td = folha(ang, k=k * .96)
    if mono:
        c1 = c2 = mono
    fio = f' stroke="{fundo}" stroke-width="4.5" paint-order="stroke"' if mono else ''
    return (f'<g stroke-linecap="round"><path d="{te}" stroke="{c1}" stroke-width="5.5"/><path d="{td}" stroke="{c2}" stroke-width="5.5"/>'
            f'<path d="{e}" fill="{c1}"/><path d="{d}" fill="{c2}"{fio}{"" if mono else " fill-opacity=\".95\""}/>'
            f'<path d="{ve}" fill="none" stroke="{veia}" stroke-width="3.4"/><path d="{vd}" fill="none" stroke="{veia}" stroke-width="3.4"/></g>')


def svg_simbolo(**kw):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 6 212 196">{simbolo(**kw)}</svg>'


for nome, kw in {'simbolo-cor': {}, 'simbolo-tinta': {'mono': TINTA, 'veia': PAPEL},
                 'simbolo-branco': {'mono': '#FFFFFF', 'veia': '#000000', 'fundo': '#000000'}}.items():
    open(os.path.join(OUT, nome + '.svg'), 'w', encoding='utf8').write(svg_simbolo(**kw))

data = json.load(open(os.path.join(P, '07-apresentacao', 'site', 'data.json'), encoding='utf8'))
coracoes = ''.join(f'<figure><img src="file://{IMG}/{s["coracao"]}" alt=""><figcaption>{s["uf"].upper()}</figcaption></figure>' for s in data)

SIMB = lambda w, **kw: f'<svg viewBox="-6 6 212 196" width="{w}" aria-hidden="true">{simbolo(**kw)}</svg>'

CARIMBO = lambda cor, txt_cima, txt_baixo, centro, w=300, rot=-8: f'''
<svg viewBox="0 0 300 300" width="{w}" style="transform:rotate({rot}deg)">
  <defs>
    <filter id="tinta{abs(hash(txt_cima)) % 999}"><feTurbulence type="fractalNoise" baseFrequency=".75" numOctaves="2" seed="4"/>
      <feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.25 1.42"/><feComposite in="SourceGraphic" operator="in"/></filter>
    <path id="arcoC" d="M45,150 A105,105 0 0 1 255,150"/><path id="arcoB" d="M38,150 A112,112 0 0 0 262,150"/>
  </defs>
  <g filter="url(#tinta{abs(hash(txt_cima)) % 999})" fill="{cor}" stroke="{cor}">
    <circle cx="150" cy="150" r="140" fill="none" stroke-width="5"/><circle cx="150" cy="150" r="128" fill="none" stroke-width="1.6"/>
    <circle cx="150" cy="150" r="78" fill="none" stroke-width="1.6"/>
    <text font-family="Jost" font-weight="600" font-size="{25 if len(txt_cima) <= 12 else 19}" letter-spacing="{5.5 if len(txt_cima) <= 12 else 3}" stroke="none"><textPath href="#arcoC" startOffset="50%" text-anchor="middle">{txt_cima}</textPath></text>
    <text font-family="Jost" font-weight="500" font-size="17" letter-spacing="4.5" stroke="none"><textPath href="#arcoB" startOffset="50%" text-anchor="middle" dominant-baseline="hanging">{txt_baixo}</textPath></text>
    <text x="40" y="156" font-size="16" stroke="none">★</text><text x="246" y="156" font-size="16" stroke="none">★</text>
    <g transform="translate(97 92) scale(.53)" stroke="none">{centro}</g>
  </g>
</svg>'''

html = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,300..900,0..100,0..1;1,9..144,300..900,0..100,0..1&family=Jost:wght@400;500;600&display=block">
<style>
*{{box-sizing:border-box}}
body{{margin:0;width:1400px;background:{PAPEL};color:{TINTA};font:400 15px/1.5 Jost,sans-serif;padding:56px 56px 64px}}
.eb{{font:600 12px/1 Jost;letter-spacing:.18em;text-transform:uppercase;color:#6E655C}}
h1{{font:400 46px/1.05 Fraunces;font-variation-settings:"SOFT" 100,"WONK" 1,"opsz" 144;margin:12px 0 10px;letter-spacing:-.01em}}
.sub{{max-width:78ch;margin:0 0 36px;color:#3B342E;font-size:16px}}
.cols{{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}}
.cam{{background:#fff;box-shadow:0 20px 40px -28px rgba(0,0,0,.45);display:flex;flex-direction:column}}
.palco{{height:360px;display:grid;place-items:center;background:#F6F1E8;border-bottom:1px solid #EEE6DA;position:relative;overflow:hidden}}
.mini{{display:grid;grid-template-columns:1fr 1fr;height:150px}}
.mini > div{{display:grid;place-items:center;overflow:hidden}}
.txt{{padding:22px 24px 26px}}
.txt h2{{font:500 28px/1.1 Fraunces;font-variation-settings:"SOFT" 100,"WONK" 1;margin:6px 0 8px}}
.txt p{{margin:0 0 8px;color:#3B342E}}
.txt .f{{font-size:13px;color:#6E655C}}
.rec{{display:inline-block;background:{CORACAO};color:#fff;font:600 10px/1 Jost;letter-spacing:.14em;text-transform:uppercase;padding:5px 8px;margin-left:8px;vertical-align:4px}}
/* caminho 1 */
.wm{{font-family:Fraunces;font-style:italic;font-weight:480;font-variation-settings:"SOFT" 100,"WONK" 1,"opsz" 144;letter-spacing:-.02em;line-height:.9;white-space:nowrap}}
.lock1{{display:grid;justify-items:center;gap:6px}}
.lock1 .wm{{font-size:76px}}
.lock1 .tag{{font:600 11px/1 Jost;letter-spacing:.32em;text-transform:uppercase;color:#6E655C;margin-top:8px}}
.h-hif{{display:inline-flex;align-items:center}}
.h-hif svg{{margin:0 .02em;transform:translateY(.06em)}}
/* caminho 2 */
.letreiro{{white-space:nowrap;font-family:Fraunces;font-weight:900;font-variation-settings:"SOFT" 0,"WONK" 1,"opsz" 144;font-size:66px;line-height:.9;color:#F4C531;letter-spacing:.005em;
  -webkit-text-stroke:2.5px #1F3E8C;paint-order:stroke fill;text-shadow:3px 3px 0 #1F3E8C,6px 6px 0 #C8321F,7px 7px 0 #C8321F,9px 9px 0 #C8321F}}
.faixa{{display:inline-block;background:#C8321F;color:#FFF7E8;font:italic 600 24px/1 Fraunces;font-variation-settings:"SOFT" 100,"WONK" 1;padding:9px 22px 11px;transform:rotate(-3deg);
  clip-path:polygon(0 0,100% 0,96% 50%,100% 100%,0 100%,4% 50%);margin-top:16px}}
/* sistema */
.sis{{display:grid;grid-template-columns:1.1fr 1fr 1.1fr;gap:24px;margin-top:28px}}
.box{{background:#fff;padding:22px 24px;box-shadow:0 20px 40px -28px rgba(0,0,0,.45)}}
.box h3{{font:600 12px/1 Jost;letter-spacing:.18em;text-transform:uppercase;color:#6E655C;margin:0 0 14px}}
.ty div{{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid #EEE6DA;padding:8px 0}}
.ty small{{font:500 12px Jost;color:#6E655C}}
.cores{{display:flex;flex-wrap:wrap;gap:8px}}
.cores span{{width:36px;height:36px;border-radius:50%;box-shadow:inset 0 0 0 1px rgba(0,0,0,.12)}}
.coracoes{{display:grid;grid-template-columns:repeat(7,1fr);gap:8px}}
.coracoes figure{{margin:0;text-align:center;font:600 10px/1 Jost;letter-spacing:.12em;color:#6E655C}}
.coracoes img{{width:100%;aspect-ratio:1;object-fit:cover;border-radius:50%;margin-bottom:4px}}
</style></head><body>
<p class="eb">identidade · bem-querer · três caminhos</p>
<h1>O emblema da cápsula</h1>
<p class="sub">A assinatura havaianas ♥ FARM RIO continua no calcanhar, igual. O que nasce aqui é o emblema da cápsula, como a FARM fez com a flor exclusiva da adidas FW23: vai na campanha, na embalagem, na etiqueta e na apresentação.</p>
<div class="cols">

  <article class="cam">
    <div class="palco"><div class="lock1">{SIMB(118)}<div class="wm">bem-querer</div><div class="tag">do Rio para o Brasil</div></div></div>
    <div class="mini">
      <div style="background:#59173B"><div class="wm h-hif" style="font-size:40px;color:#FCE9D2">bem{SIMB(30, mono='#FCE9D2', veia='#59173B', fundo='#59173B')}querer</div></div>
      <div style="background:#F3ECE1;gap:14px;grid-auto-flow:column">{SIMB(44)}{SIMB(26, mono=TINTA)}{SIMB(16, mono=TINTA)}</div>
    </div>
    <div class="txt"><p class="eb">caminho 1 <span class="rec">recomendado</span></p><h2>Coração de dois</h2>
      <p>Duas folhas de amendoeira caem juntas e viram um coração. É a regra da coleção (o coração nunca é desenhado, ele é formado pelos elementos) virando símbolo. A folha é do Rio porque a viagem sai do Rio.</p>
      <p>Na campanha, o símbolo muda de estado: em cada um, o coração é feito com os elementos de lá.</p>
      <p class="f">Fraunces Italic (Soft, Wonky) · Jost · OFL, Google Fonts</p></div>
  </article>

  <article class="cam">
    <div class="palco" style="background:#FFF3D6"><div style="text-align:center"><div class="letreiro">Bem-Querer</div><div class="faixa">do Rio para o Brasil</div></div></div>
    <div class="mini">
      <div style="background:#1F3E8C"><div class="letreiro" style="font-size:30px;-webkit-text-stroke-color:#0E1E4A;text-shadow:2px 2px 0 #0E1E4A,4px 4px 0 #C8321F">Bem-Querer</div></div>
      <div style="background:#F3ECE1"><div class="letreiro" style="font-size:24px;text-shadow:1px 1px 0 #1F3E8C,3px 3px 0 #C8321F">Bem-Querer</div></div>
    </div>
    <div class="txt"><p class="eb">caminho 2</p><h2>Letreiro</h2>
      <p>Vem dos abridores de letras: placa de feira, nome de barco no Pará, para-choque de caminhão, fachada de boteco. É a letra pintada à mão que existe nos quatorze estados.</p>
      <p>Funciona muito bem em campanha e embalagem. Em tamanho pequeno perde força e briga com o logo da havaianas.</p>
      <p class="f">Fraunces Black (Wonky) com sombra de letreiro · Jost</p></div>
  </article>

  <article class="cam">
    <div class="palco">{CARIMBO('#B5302A', 'BEM-QUERER', 'DO RIO PARA O BRASIL', simbolo(mono='#B5302A', veia=PAPEL), 290)}</div>
    <div class="mini">
      <div style="background:#0CA5AE">{CARIMBO('#FFFBF4', 'MATO GROSSO DO SUL', 'BEM-QUERER · 10/14', simbolo(mono='#FFFBF4', veia='#0CA5AE', fundo='#0CA5AE'), 136, 6)}</div>
      <div style="background:#F3ECE1">{CARIMBO('#1F3E8C', 'PARÁ', 'BEM-QUERER · 08/14', simbolo(mono='#1F3E8C', veia='#F3ECE1', fundo='#F3ECE1'), 136, -4)}</div>
    </div>
    <div class="txt"><p class="eb">caminho 3</p><h2>Carimbo de viagem</h2>
      <p>O emblema como o carimbo do passaporte ou do correio: cada estado ganha o seu, com número de 01 a 14. Conversa com o caderno de viagem do site e da embalagem.</p>
      <p>Pode ser o selo secundário do caminho 1 em vez de concorrer com ele.</p>
      <p class="f">Jost em arco · tinta irregular de carimbo · símbolo ao centro</p></div>
  </article>
</div>

<div class="sis">
  <div class="box ty"><h3>tipografia (para qualquer caminho)</h3>
    <div><span style="font:italic 480 34px/1 Fraunces;font-variation-settings:'SOFT' 100,'WONK' 1">Fraunces</span><small>títulos · emblema</small></div>
    <div><span style="font:500 24px/1 Jost">Jost</span><small>texto · etiqueta · linha da cápsula</small></div>
    <div><span style="font:italic 400 24px/1 Fraunces;font-variation-settings:'SOFT' 100,'WONK' 1">Fraunces Itálico</span><small>anotação · legenda</small></div>
  </div>
  <div class="box"><h3>cores-base + uma paleta por estado</h3>
    <div class="cores"><span style="background:{PAPEL}"></span><span style="background:{TINTA}"></span><span style="background:{CORACAO}"></span><span style="background:{FOLHA_A}"></span><span style="background:{FOLHA_B}"></span>
      {''.join(f'<span style="background:{s["paleta"][0]}" title="{s["uf"]}"></span>' for s in data)}</div>
  </div>
  <div class="box"><h3>o símbolo muda de estado</h3><div class="coracoes">{coracoes}</div></div>
</div>
</body></html>'''

open(os.path.join(OUT, 'prancha-caminhos.html'), 'w', encoding='utf8').write(html)
print('ok', OUT)
