"""Reel do Bem-Querer (1080 x 1920, 9:16, 41,5 s, com a trilha de samba) no ritmo de um vídeo de lançamento de marca:
frase digitada -> logo montado sobre guias -> palavras em cor chapada -> paleta -> variações do logo ->
motion da onça -> frase -> campanha -> pares + site -> site no celular -> cartão final.
Todos os cortes caem na batida do samba (120 bpm, 0,5 s); a trilha entra no MP4 com reel_trilha.py.
Uso: cd /tmp && python3 -I .../gerar_reel.py ; node filme_render.js reel"""
import glob
import html
import json
import os
import subprocess

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(AQUI, '..')
B = os.path.join(P, '07-apresentacao', 'behance')
FIL = os.path.join(B, 'filmes')
IMG = os.path.join(B, '_img')
QD = os.path.join(B, '_quadros')
SITE = os.path.join(P, '07-apresentacao', 'site')
os.makedirs(FIL, exist_ok=True)
FPS = 24
e = lambda s: html.escape(s or '', quote=True)
PASTA = {os.path.basename(d)[3:]: d for d in glob.glob(os.path.join(P, '05-estampas', '[0-9][0-9]-*'))}


def pasta(uf):
    nomes = {'mg': 'minas-gerais', 'pa': 'para', 'ba': 'bahia', 'rs': 'rio-grande-do-sul', 'ce': 'ceara', 'ms': 'mato-grosso-do-sul'}
    return PASTA[nomes[uf]]


def jpg(origem, lado, nome):
    dst = os.path.join(IMG, nome + '.jpg')
    if not os.path.exists(dst):
        im = Image.open(origem).convert('RGB')
        im.thumbnail((lado, lado), Image.LANCZOS)
        im.save(dst, quality=90, optimize=True)
    return '../_img/' + nome + '.jpg'


# quadros do motion da onça em 720 px (o arco do reel é grande)
QMS = os.path.join(QD, 'ms720')
if not os.path.isdir(QMS) or not os.listdir(QMS):
    os.makedirs(QMS, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(SITE, 'video', 'ms.mp4'), '-vf', f'fps={FPS}', '-q:v', '2',
                    os.path.join(QMS, '%04d.jpg')], check=True)
NQ = {'ms720': len(os.listdir(QMS))}

camp = jpg(os.path.join(pasta('ce'), 'campanha', 'campanha-ce-renda.jpg'), 1920, 'reel-campanha-ce')
estudios = [jpg(os.path.join(pasta(u), 'chinelo', f'estudio-{u}.jpg'), 900, f'reel-estudio-{u}') for u in ('mg', 'pa', 'ba', 'rs')]

_s = open(os.path.join(P, '03-marca', 'identidade-bem-querer', 'simbolo-cor.svg'), encoding='utf8').read()
caminhos = [c + '/>' for c in _s[_s.index('<path'):_s.rindex('</g>')].split('/>') if c.strip()]
SIMB = f'<svg viewBox="-6 6 212 196"><g stroke-linecap="round">{"".join(caminhos)}</g></svg>'


def simb_mono(cor, veio):
    m = SIMB.replace('#C8321F', cor).replace('#E8892B', cor).replace('#FCFAF6', veio)
    return m.replace('fill-opacity=".95"', '')


def letras(t, cls='ch'):
    return ''.join(f'<span class="{cls}">{"&nbsp;" if c == " " else e(c)}</span>' for c in t)


def nome(cor_bem='var(--tinta)', cor_q='var(--vinho)'):
    return f'<span style="color:{cor_bem}">Bem-</span><span class="q" style="color:{cor_q}">Querer</span>'


ESTRIPES = [('AREIA', '#F4EDE3', '#2A1A17'), ('RENDA', '#EBE2D5', '#2A1A17'), ('CAJU', '#E07A2E', '#FFF3E6'), ('URUCUM', '#C8321F', '#FFF3E6'),
            ('AÇAÍ', '#6A1B29', '#FFF3E6'), ('BARRO', '#857568', '#FFF3E6'), ('CAFÉ', '#2A1A17', '#F4EDE3')]
listras = ''.join(f'<div class="lis" style="background:{c};color:{t}"><span>{n}</span></div>' for n, c, t in ESTRIPES)
cards = ''.join(f'<div class="card c{k}"><img src="{src}" alt=""></div>' for k, src in enumerate(estudios))


FL = ['pa', 'ba', 'sc', 'ma', 'mg', 'pe', 'rs', 'am']
EST = {'pa': 'Revoada de Miriti', 'ba': 'Cacau e Fita', 'sc': 'Baleia e Ostra', 'ma': 'Couro de Boi', 'mg': 'Barroco de Minas',
       'pe': 'Passo de Frevo', 'rs': 'Roda de Chimarrão', 'am': 'Encontro das Águas'}
_dados = {d['uf']: d for d in json.load(open(os.path.join(SITE, 'data.json'), encoding='utf8'))}
_ordem = [d['uf'] for d in json.load(open(os.path.join(SITE, 'data.json'), encoding='utf8'))]
_reg = {'mg': 'SUDESTE', 'rj': 'SUDESTE', 'ba': 'NORDESTE', 'pe': 'NORDESTE', 'ce': 'NORDESTE', 'ma': 'NORDESTE', 'am': 'NORTE', 'pa': 'NORTE',
        'to': 'NORTE', 'ms': 'CENTRO-OESTE', 'go': 'CENTRO-OESTE', 'pr': 'SUL', 'sc': 'SUL', 'rs': 'SUL'}
flashes = ''.join(f'<img class="fl" src="../../site/img/{u}-ilustracao.jpg" alt="">' for u in FL)
flash_legs = ''.join(f'<div class="f-leg l{k + 1}"><b>{_ordem.index(u) + 1:02d} / 14 · {_reg[u]}</b><strong>{e(_dados[u]["nome"])}</strong><em>{e(EST[u])}</em></div>'
                     for k, u in enumerate(FL))

CSS = '''
*{box-sizing:border-box}
:root{--creme:#F4EDE3;--creme2:#EBE2D5;--tinta:#2A1A17;--vinho:#6A1B29;--laranja:#E07A2E;--urucum:#C8321F;--suave:#857568;--claro:#F2B98A;--serif:"Instrument Serif",Georgia,serif;--sans:"Jost",system-ui,sans-serif}
html,body{margin:0;background:#000}
#palco{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--creme);color:var(--tinta);font-family:var(--sans);-webkit-font-smoothing:antialiased}
.cena{position:absolute;inset:0;visibility:hidden;overflow:hidden}
.centro{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.ch{display:inline-block;white-space:pre}
.q{font-style:italic}
/* A */
#A{background:var(--creme)}
.a1{font:400 66px/1.2 var(--sans);letter-spacing:.01em;color:var(--tinta)}
.a2{font:italic 400 190px/.95 var(--serif);color:var(--vinho);letter-spacing:-.03em;margin-top:18px}
#a-simb{width:120px;margin-top:40px}
/* B */
#B{background:var(--creme)}
.b-zoom{position:absolute;inset:0;transform-origin:68% 50%}
.guia{position:absolute;background:none;border-color:rgba(200,50,31,.55);border-style:dashed;border-width:0}
.gh{left:0;right:0;border-top-width:2px;transform-origin:left}
.gv{top:0;bottom:0;border-left-width:2px;transform-origin:top}
.b-tit{position:absolute;left:0;right:0;top:860px;margin:0;text-align:center;font:400 214px/1 var(--serif);letter-spacing:-.035em;white-space:nowrap}
.b-tit .q{color:var(--vinho)}
#swoosh{position:absolute;inset:0;width:100%;height:100%}
/* C */
.palavra-c{font:500 112px/1 var(--sans);letter-spacing:.12em;text-transform:uppercase}
#C1{background:var(--creme)}
.c-barra{position:relative;display:inline-block;padding:22px 34px;background:var(--laranja);color:#FFF3E6;transform-origin:left}
#C2{background:var(--vinho);color:#FFF3E6}
#C3{background:#0CA5AE;color:#FFF3E6}
#C4{background:var(--urucum);color:#FFF3E6}
#C5{background:var(--tinta)}
/* D */
#D{background:var(--tinta)}
.listras{position:absolute;inset:0;display:flex;flex-direction:column}
.lis{flex:1;display:flex;align-items:center;justify-content:center;font:500 30px/1 var(--sans);letter-spacing:.3em}
.lis span{opacity:0}
#bola{position:absolute;left:540px;top:960px;width:2400px;height:2400px;margin:-1200px 0 0 -1200px;border-radius:50%;background:var(--laranja);transform:scale(0)}
/* E */
.logo-g{font:400 236px/.9 var(--serif);letter-spacing:-.035em;margin:0}
.logo-g .q{display:block}
#E1{background:var(--laranja);color:#FFF3E6}
#E2{background:var(--creme)}
#E3{background:var(--vinho);color:var(--claro)}
#E4{background:var(--urucum)}
#E5{background:var(--tinta);color:#FFF3E6}
.e-simb{width:190px;margin-bottom:64px}
.e-simb-g{width:520px}
.assin-claro{width:640px;filter:brightness(0) invert(1)}
.lockup{display:flex;flex-direction:column;align-items:center;gap:34px}
.lockup .col{font:italic 400 110px/1 var(--serif);color:var(--claro)}
.lockup small{display:block;font:500 24px/1 var(--sans);font-style:normal;letter-spacing:.3em;text-transform:uppercase;color:rgba(255,243,230,.7);margin-bottom:18px}
/* F */
#F{background:var(--creme)}
.f-arte{position:absolute;left:150px;top:300px;width:780px;height:1045px}
.arco{position:absolute;inset:0;overflow:hidden;border-radius:999px 999px 0 0;background:var(--creme2);box-shadow:0 60px 110px -60px rgba(40,10,10,.5)}
.arco img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 100%}
.f-par{position:absolute;left:28px;top:220px;width:250px;transform:rotate(-12deg);filter:drop-shadow(0 4px 4px rgba(40,10,10,.25)) drop-shadow(0 26px 30px rgba(40,10,10,.28))}
.f-leg{position:absolute;left:0;right:0;top:1440px;text-align:center}
.f-leg b{display:block;font:500 26px/1 var(--sans);letter-spacing:.3em;color:var(--vinho)}
.f-leg strong{display:block;font:400 92px/1 var(--serif);margin-top:20px}
.f-leg em{display:block;font:italic 400 44px/1.2 var(--serif);color:var(--suave);margin-top:10px}
.f-leg{visibility:hidden}
.f-leg.l0{visibility:visible}
.arco img.fl{visibility:hidden}
/* G */
#G{background:var(--vinho);color:#FFF3E6}
.g1{font:400 62px/1.2 var(--sans);letter-spacing:.02em;color:rgba(255,243,230,.85)}
.g2{font:italic 400 172px/.95 var(--serif);color:var(--claro);letter-spacing:-.025em;margin-top:26px}
/* H */
#H{background:#222}
.h-foto{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.h-veu{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,10,8,0) 38%,rgba(20,10,8,.72) 88%)}
.h-nome{position:absolute;left:0;right:0;bottom:250px;text-align:center;font:400 170px/.9 var(--serif);letter-spacing:-.035em;color:#FFF3E6;text-shadow:0 10px 40px rgba(0,0,0,.35)}
.h-nome .q{color:var(--claro)}
.h-leg{position:absolute;left:0;right:0;bottom:170px;text-align:center;font:500 24px/1 var(--sans);letter-spacing:.3em;text-transform:uppercase;color:rgba(255,243,230,.85)}
/* I */
#I{background:#F1DCC6}
.card{position:absolute;width:390px;height:488px;border-radius:22px;overflow:hidden;box-shadow:0 40px 70px -40px rgba(60,20,10,.55);background:#fff}
.card img{width:100%;height:100%;object-fit:cover}
.c0{left:120px;top:330px;transform:rotate(-4deg)}
.c1{left:560px;top:300px;transform:rotate(3deg)}
.c2{left:110px;top:870px;transform:rotate(2deg)}
.c3{left:550px;top:850px;transform:rotate(-3deg)}
.fone{position:absolute;width:390px;height:844px;border-radius:58px;border:14px solid #1B1210;background:#1B1210;overflow:hidden;box-shadow:0 60px 90px -40px rgba(30,10,5,.6)}
.fone img{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:44px}
.fone::after{content:"";position:absolute;left:50%;top:14px;width:110px;height:30px;margin-left:-55px;border-radius:20px;background:#1B1210}
.i-fone{left:590px;top:1010px;transform:rotate(8deg)}
/* J */
#J{background:var(--laranja)}
.j1{left:120px;top:420px;transform:rotate(-6deg)}
.j2{left:570px;top:560px;transform:rotate(5deg)}
.j-leg{position:absolute;left:0;right:0;top:250px;text-align:center;font:500 26px/1 var(--sans);letter-spacing:.3em;text-transform:uppercase;color:#FFF3E6}
.j-leg em{display:block;font:italic 400 76px/1 var(--serif);letter-spacing:-.01em;text-transform:none;margin-top:16px}
/* K */
#K{background:var(--tinta);color:#FFF3E6}
.k-folha{position:absolute;width:760px}
.k1{left:-220px;top:-300px;transform:rotate(160deg)}
.k2{right:-240px;bottom:-280px;transform:rotate(-20deg)}
.k-nome{font:400 210px/.9 var(--serif);letter-spacing:-.035em;margin:0}
.k-nome .q{display:block;color:var(--claro)}
.k-sub{font:italic 400 44px/1.2 var(--serif);color:rgba(255,243,230,.8);margin:34px 0 46px}
.k-assin{width:520px;filter:brightness(0) invert(1);opacity:.92}
.k-legal{position:absolute;left:80px;right:80px;bottom:120px;text-align:center;font:500 20px/1.6 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:rgba(255,243,230,.55)}
'''

H = f'''<div id="palco">
<section class="cena centro" id="A"><p class="a1">{letras("Uma collab feita com")}</p><p class="a2">{letras("bem-querer")}</p><div id="a-simb">{SIMB}</div></section>
<section class="cena" id="B"><div class="b-zoom">
  <i class="guia gh" style="top:880px"></i><i class="guia gh" style="top:1052px"></i><i class="guia gh" style="top:968px;border-color:rgba(200,50,31,.3)"></i>
  <i class="guia gv" style="left:96px"></i><i class="guia gv" style="left:540px;border-color:rgba(200,50,31,.3)"></i><i class="guia gv" style="left:984px"></i>
  <p class="b-tit">{letras("Bem-")}<span class="q">{letras("Querer")}</span></p></div>
  <svg id="swoosh" viewBox="0 0 1080 1920"><path id="sw" d="M-120,1500 C 260,1160 520,1700 760,1260 S 1060,700 1240,860" fill="none" stroke="#E07A2E" stroke-width="150" stroke-linecap="round"/></svg></section>
<section class="cena centro" id="C1"><div class="c-barra palavra-c">{letras("solar")}</div></section>
<section class="cena centro" id="C2"><p class="palavra-c">{letras("afetiva")}</p></section>
<section class="cena centro" id="C3"><p class="palavra-c">{letras("de rua")}</p></section>
<section class="cena centro" id="C4"><p class="palavra-c">{letras("brasileira")}</p></section>
<section class="cena" id="D"><div class="listras">{listras}</div><div id="bola"></div></section>
<section class="cena centro" id="E1"><div class="e-simb">{simb_mono("#FFF3E6", "#E07A2E")}</div><p class="logo-g">{nome("#FFF3E6", "#FFF3E6")}</p></section>
<section class="cena centro" id="E2"><div class="e-simb">{SIMB}</div><p class="logo-g">{nome()}</p></section>
<section class="cena centro" id="E3"><div class="lockup"><img class="assin-claro" src="../_img/assinatura-topo.svg" alt=""><div class="col"><small>coleção</small>Bem-Querer</div></div></section>
<section class="cena centro" id="E4"><div class="e-simb-g">{simb_mono("#FFF3E6", "#C8321F")}</div></section>
<section class="cena centro" id="E5"><p class="logo-g">{nome("#FFF3E6", "#F2B98A")}</p></section>
<section class="cena" id="F"><div class="f-arte"><div class="arco"><img data-uf="ms720" data-t0="21.0" alt="">{flashes}</div></div>
  <img class="f-par" src="../../site/img/ms-par.webp" alt="">
  <div class="f-leg l0"><b>10 / 14 · CENTRO-OESTE</b><strong>Mato Grosso do Sul</strong><em>Onça de Bonito</em></div>{flash_legs}</section>
<section class="cena centro" id="G"><p class="g1">{letras("em cada estampa,")}</p><p class="g2">{letras("um coração")}<br>{letras("escondido")}</p></section>
<section class="cena" id="H"><img class="h-foto" src="{camp}" alt=""><div class="h-veu"></div>
  <p class="h-nome">{letras("Bem-")}<span class="q">{letras("Querer")}</span></p><p class="h-leg">Ceará · Renda ao Vento</p></section>
<section class="cena" id="I">{cards}<div class="fone i-fone"><img src="../_img/reel-tela-estado.png" alt=""></div></section>
<section class="cena" id="J"><p class="j-leg">o site<em>14 estados, um por página</em></p>
  <div class="fone j1"><img src="../_img/reel-tela-home.png" alt=""></div><div class="fone j2"><img src="../_img/reel-tela-roda.png" alt=""></div></section>
<section class="cena centro" id="K"><div class="k-folha k1">{simb_mono("#E07A2E", "#2A1A17")}</div><div class="k-folha k2">{simb_mono("#C8321F", "#2A1A17")}</div>
  <p class="k-nome">Bem-<span class="q">Querer</span></p><p class="k-sub">uma V2 conceitual da collab</p><img class="k-assin" src="../_img/assinatura-topo.svg" alt="">
  <p class="k-legal">projeto conceitual de portfólio de Emilly Silva<br>sem vínculo com FARM&nbsp;Rio e havaianas</p></section>
</div>'''

JS = '''
const FPS = __FPS__, NQ = __NQ__, QD = '../_quadros/';
const quadro = (uf, t) => QD + uf + '/' + String((Math.floor(Math.max(0, t) * FPS) % NQ[uf]) + 1).padStart(4, '0') + '.jpg';
async function trocaQuadros(t) {
  const espera = [];
  document.querySelectorAll('img[data-uf][data-t0]').forEach(im => {
    const src = quadro(im.dataset.uf, t - +im.dataset.t0);
    if (im.getAttribute('src') !== src) { im.setAttribute('src', src); espera.push(im.decode().catch(() => {})); }
  });
  await Promise.all(espera);
}
const DUR = 41.5;
const tl = gsap.timeline({ paused: true, defaults: { ease: 'power3.out' } });
// cada cena entra e sai em cortes secos, sempre na batida do samba (0,5 s)
const corte = (id, de, ate) => { tl.set('#' + id, { visibility: 'visible' }, de); if (ate) tl.set('#' + id, { visibility: 'hidden' }, ate); };
function monta() {
  gsap.set('.ch', { opacity: 0 });
  // A. frase digitada (0 a 4)
  corte('A', 0, 4.0);
  tl.to('.a1 .ch', { opacity: 1, duration: .01, stagger: .055 }, .25)
    .fromTo('.a2 .ch', { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: .5, stagger: .07 }, 1.5)
    .from('#a-simb', { scale: 0, opacity: 0, duration: .6, ease: 'back.out(2.4)' }, 2.5)
    .to('#A > *', { opacity: 0, filter: 'blur(14px)', y: -20, duration: .5, ease: 'power2.in' }, 3.5);
  // B. o nome montado sobre as guias, zoom, e o traço laranja varre (4 a 8,5)
  corte('B', 4.0, 8.5);
  tl.from('.gh', { scaleX: 0, duration: .6, stagger: .08, ease: 'power2.out' }, 4.0)
    .from('.gv', { scaleY: 0, duration: .6, stagger: .08, ease: 'power2.out' }, 4.1)
    .fromTo('.b-tit .ch', { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .35, stagger: .1 }, 4.25)
    .to('.b-zoom', { scale: 2.4, x: -240, duration: 1.5, ease: 'power2.inOut' }, 6.0);
  const sw = document.getElementById('sw'), L = sw.getTotalLength();
  gsap.set(sw, { strokeDasharray: L, strokeDashoffset: L });
  tl.to(sw, { strokeDashoffset: 0, duration: .65, ease: 'power2.in' }, 7.5)
    .to(sw, { attr: { 'stroke-width': 1900 }, duration: .35, ease: 'power2.in' }, 8.15);
  // C. palavras em cor chapada, uma por compasso (8,5 a 13)
  corte('C1', 8.5, 9.5);
  tl.from('.c-barra', { scaleX: 0, duration: .45, ease: 'power3.out' }, 8.5)
    .to('#C1 .ch', { opacity: 1, duration: .01, stagger: .05 }, 8.75);
  corte('C2', 9.5, 10.5); tl.fromTo('#C2 .ch', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, stagger: .035 }, 9.5);
  corte('C3', 10.5, 11.5); tl.fromTo('#C3 .ch', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, stagger: .035 }, 10.5);
  corte('C4', 11.5, 13.0); tl.fromTo('#C4 .ch', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .3, stagger: .03 }, 11.5);
  corte('C5', 12.5, 13.0); tl.fromTo('#C5', { yPercent: 100 }, { yPercent: 0, duration: .5, ease: 'power3.inOut' }, 12.5);
  // D. a paleta e a bola laranja que leva para o logo (13 a 17)
  corte('D', 13.0, 17.0);
  tl.from('.lis', { xPercent: -100, duration: .5, stagger: { each: .1, from: 'end' }, ease: 'power3.out' }, 13.0)
    .to('.lis span', { opacity: 1, duration: .3, stagger: .07 }, 14.0)
    .to('#bola', { scale: 1, duration: .75, ease: 'power2.in' }, 16.25);
  // E. variações do logo (17 a 21): as que pedem leitura ficam 1 s, as outras meio
  [['E1', 17.0], ['E2', 18.0], ['E3', 18.5], ['E4', 19.5], ['E5', 20.0]].forEach(([id, t], k, a) => {
    corte(id, t, k < a.length - 1 ? a[k + 1][1] : 21.0);
    tl.from('#' + id + ' > *', { opacity: 0, y: 24, scale: .96, duration: .35, stagger: .06 }, t);
  });
  // F. o motion da onça no arco, o par cai, e oito estados passam a cada colcheia (21 a 25)
  corte('F', 21.0, 25.0);
  tl.fromTo('.f-arte', { clipPath: 'inset(100% 0% 0% 0% round 999px 999px 0px 0px)' }, { clipPath: 'inset(0% 0% 0% 0% round 999px 999px 0px 0px)', duration: .8, ease: 'power3.inOut' }, 21.0)
    .from('.f-par', { opacity: 0, y: -120, rotation: -40, duration: .7, ease: 'back.out(1.6)' }, 21.5)
    .from('.f-leg.l0 > *', { opacity: 0, y: 26, duration: .5, stagger: .08 }, 21.75)
    .to('.f-par', { opacity: 0, duration: .15 }, 22.85);
  document.querySelectorAll('.arco img.fl').forEach(function (im, k) {
    const t = 23.0 + k * .25;
    tl.set(im, { visibility: 'visible' }, t).set('.f-leg', { visibility: 'hidden' }, t).set('.f-leg.l' + (k + 1), { visibility: 'visible' }, t);
    if (k > 0) tl.set(document.querySelectorAll('.arco img.fl')[k - 1], { visibility: 'hidden' }, t);
  });
  // G. a frase (25 a 27,5)
  corte('G', 25.0, 27.5);
  tl.to('#G .g1 .ch', { opacity: 1, duration: .01, stagger: .045 }, 25.1)
    .fromTo('#G .g2 .ch', { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .45, stagger: .045 }, 26.0);
  // H. campanha em tela cheia, o nome entra (27,5 a 31)
  corte('H', 27.5, 31.0);
  tl.fromTo('.h-foto', { scale: 1.14 }, { scale: 1, duration: 3.5, ease: 'none' }, 27.5)
    .fromTo('.h-nome .ch', { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .45, stagger: .07 }, 28.0)
    .from('.h-leg', { opacity: 0, duration: .5 }, 29.0);
  // I. quatro pares e o site no celular (31 a 34)
  corte('I', 31.0, 34.0);
  tl.from('.card', { opacity: 0, y: 220, rotation: 0, duration: .7, stagger: .1, ease: 'power3.out' }, 31.0)
    .from('.i-fone', { x: 600, rotation: 20, duration: .8, ease: 'power3.out' }, 31.5)
    .to('.i-fone', { y: -26, duration: 1.7, ease: 'sine.inOut' }, 32.3);
  // J. o site no celular (34 a 37)
  corte('J', 34.0, 37.0);
  tl.from('.j-leg', { opacity: 0, y: 20, duration: .5 }, 34.0)
    .from('.j1', { y: 1300, rotation: -16, duration: .8, ease: 'power3.out' }, 34.0)
    .from('.j2', { y: 1300, rotation: 14, duration: .8, ease: 'power3.out' }, 34.15)
    .to('.j1', { y: -30, duration: 2.1, ease: 'sine.inOut' }, 34.85)
    .to('.j2', { y: 24, duration: 2.1, ease: 'sine.inOut' }, 34.9);
  // K. cartão final (37 a 41,5); o nome pulsa no golpe final da música, em 40
  corte('K', 37.0, null);
  tl.from('.k1', { x: -300, y: -300, rotation: 120, opacity: 0, duration: 1.1, ease: 'power3.out' }, 37.0)
    .from('.k2', { x: 300, y: 300, rotation: -70, opacity: 0, duration: 1.1, ease: 'power3.out' }, 37.1)
    .from('.k-nome, .k-sub, .k-assin, .k-legal', { opacity: 0, y: 26, duration: .7, stagger: .12 }, 37.5)
    .to('.k-nome', { scale: 1.045, duration: .1, ease: 'power2.out' }, 40.0)
    .to('.k-nome', { scale: 1, duration: .55, ease: 'back.out(3)' }, 40.1);
}
window.FILME = { dur: DUR, seek: async t => { tl.seek(t, false); await trocaQuadros(t); } };
window.PRONTO = document.fonts.ready.then(() => new Promise(r => setTimeout(r, 300))).then(monta);
'''.replace('__FPS__', str(FPS)).replace('__NQ__', json.dumps(NQ))

doc = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>reel</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Jost:wght@400;500&display=block">
<style>{CSS}</style></head><body>{H}
<script src="../../site/js/gsap.min.js"></script><script>{JS}</script></body></html>'''
open(os.path.join(FIL, 'reel.html'), 'w', encoding='utf8').write(doc)
print('ok: filmes/reel.html;', NQ['ms720'], 'quadros da onça')
