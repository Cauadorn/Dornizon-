"""Reel do Bem-Querer: "caça ao coração" (1080 x 1920, 9:16, sem som).
O vídeo é um jogo. Cada ilustração aparece, quem assiste procura o coração, e ele se revela: o resto escurece,
um anel se desenha em volta e a câmera entra. Três rodadas com calma (Pará, Santa Catarina, Rio), o par na areia
de Ipanema, uma rodada rápida com sete estados, quatro estados que ficam para quem assiste, os 14 pares e a assinatura.
O placar no topo conta os corações achados. A revelação acontece sempre na emenda do loop do motion (o quadro 1),
que é o desenho original, então o coração está exatamente onde a caixa de mapa_coracoes_caixas.json diz.
Cortes no tempo de 120 bpm (0,5 s), para casar com a música escolhida no Instagram.
Uso: cd /tmp && python3 -I .../gerar_reel.py ; node filme_render.js reel-coracao"""
import html
import json
import math
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


def nb(t):
    """Sem viúva: junta as duas últimas palavras."""
    t = e(t)
    i = t.rfind(' ')
    return t if i < 0 else t[:i] + '&nbsp;' + t[i + 1:]


data = json.load(open(os.path.join(SITE, 'data.json'), encoding='utf8'))
POR = {s['uf']: s for s in data}
CAIXA = {c['estado']: c['caixa'] for c in json.load(open(os.path.join(AQUI, 'mapa_coracoes_caixas.json'), encoding='utf8'))}

# quadros dos motions em 720 px
NQ = {}
for s in data:
    d = os.path.join(QD, s['uf'] + '720')
    if not os.path.isdir(d) or not os.listdir(d):
        os.makedirs(d, exist_ok=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(SITE, 'video', s['uf'] + '.mp4'), '-vf', f'fps={FPS}', '-q:v', '2',
                        os.path.join(d, '%04d.jpg')], check=True)
    NQ[s['uf'] + '720'] = len(os.listdir(d))


def jpg(origem, lado, nome):
    dst = os.path.join(IMG, nome + '.jpg')
    if not os.path.exists(dst):
        im = Image.open(origem).convert('RGB')
        im.thumbnail((lado, lado), Image.LANCZOS)
        im.save(dst, quality=90, optimize=True)
    return '../_img/' + nome + '.jpg'


ipanema = jpg(os.path.join(P, '05-estampas', '02-rio-de-janeiro', 'campanha', 'lugar-rj-areia-ipanema.jpg'), 2200, 'reel-ipanema')

# símbolo: 0 haste esq, 1 haste dir, 2 folha esq, 3 folha dir, 4 veio esq, 5 veio dir
_s = open(os.path.join(P, '03-marca', 'identidade-bem-querer', 'simbolo-cor.svg'), encoding='utf8').read()
caminhos = [c + '/>' for c in _s[_s.index('<path'):_s.rindex('</g>')].split('/>') if c.strip()]
SIMB = f'<svg viewBox="-6 6 212 196"><g stroke-linecap="round">{"".join(caminhos)}</g></svg>'
folha = lambda idx: f'<svg class="{"fe" if idx[0] == 0 else "fd"}" viewBox="-6 6 212 196"><g stroke-linecap="round">{"".join(caminhos[i] for i in idx)}</g></svg>'

# ------------------------------------------------------------------ o arco
AW = 790
AH = round(AW * 2336 / 1744)
AX, AY = (1080 - AW) // 2, 384


def coracao(uf):
    x0, y0, x1, y1 = CAIXA[POR[uf]['nome']]
    px, py = (x0 + x1) / 2 / 1744 * AW, (y0 + y1) / 2 / 2336 * AH
    r = max(max(x1 - x0, y1 - y0) * .62 / 1744 * AW, 52)
    return px, py, r


def arco(uf, ts, tr=None):
    """tr = momento da revelação: o motion para no quadro 1 (a emenda do loop) e o coração aparece."""
    q = uf + '720'
    if tr is None:
        return f'<div class="arco-w"><div class="arco"><div class="zoom"><img data-uf="{q}" data-t0="{ts:.4f}" alt=""></div></div></div>'
    px, py, r = coracao(uf)
    t0 = tr - NQ[q] / FPS
    m = f'radial-gradient(circle {r:.0f}px at {px:.1f}px {py:.1f}px,transparent 96%,#000 100%)'
    c = 2 * math.pi * r
    return (f'<div class="arco-w"><div class="arco"><div class="zoom" style="transform-origin:{px:.1f}px {py:.1f}px">'
            f'<img data-uf="{q}" data-t0="{t0:.4f}" data-t1="{tr:.4f}" alt="">'
            f'<div class="veu-c" style="-webkit-mask-image:{m};mask-image:{m}"></div>'
            f'<svg class="anel" viewBox="0 0 {AW} {AH}"><circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.0f}" transform="rotate(-90 {px:.1f} {py:.1f})" '
            f'stroke-dasharray="{c:.1f}" stroke-dashoffset="{c:.1f}"/></svg></div></div></div>')


def zoom_de(uf):
    px, py, r = coracao(uf)
    z = round(min(2.0, max(1.35, .5 * AW / (2 * r))), 3)
    dx = min(max(AW / 2 - px, -(AW - px) * (z - 1)), px * (z - 1))
    dy = min(max(AH * .46 - py, -(AH - py) * (z - 1)), py * (z - 1))
    return z, round(dx, 1), round(dy, 1)


# ------------------------------------------------------------------ roteiro
# rodadas com calma: (uf, entra, revela, sai, título)
LENTAS = [('pa', 0.0, 4.0, 6.0, ('tem um coração', 'escondido aqui.')),
          ('sc', 6.0, 8.0, 10.0, ('e', 'aqui?')),
          ('rj', 10.0, 11.5, 13.5, ('e no', 'Rio?'))]
PROD = (13.5, 16.0)
RAPIDAS = ['ba', 'ms', 'pr', 'go', 'rs', 'ce', 'ma']    # 1 s cada, a partir de 16.0
T_RAP = 16.0
RESTAM = ['mg', 'pe', 'am', 'to']                        # 0,5 s cada, sem revelar
T_RES = T_RAP + len(RAPIDAS)
T_GRADE = T_RES + .5 * len(RESTAM)                       # 25.0
T_ACHOU = T_GRADE + 2.0                                  # 27.0
T_FIM = T_ACHOU + 1.5                                    # 28.5
DUR = T_FIM + 5.0                                        # 33.5

rodadas, secoes = [], []
n = 0
for k, (uf, ts, tr, te, (t1, t2)) in enumerate(LENTAS):
    n += 1
    if k == 0:
        topo = f'<p class="t1">{e(t1)}</p><p class="t2">{e(t2)}</p>'
        rotulo = '<span class="pausa"></span>pausa e procura'
    else:
        topo = f'<p class="t1 so">{e(t1)} <em>{e(t2)}</em></p>'
        rotulo = 'procura'
    secoes.append(f'<section class="cena" id="L{k}">{arco(uf, ts, tr)}<div class="topo">{topo}</div>'
                  f'<div class="baixo"><div class="procura"><b>{rotulo}</b><i class="barra"><i></i></i></div>'
                  f'<div class="achou"><b>{e(POR[uf]["nome"])}</b><em>{nb(POR[uf]["coracao_texto"])}</em></div></div></section>')
    rodadas.append({'id': f'L{k}', 'tipo': 'lenta', 'ts': ts, 'tr': tr, 'te': te, 'z': zoom_de(uf)[0], 'dx': zoom_de(uf)[1], 'dy': zoom_de(uf)[2], 'n': n, 'bar': 1.5 if k == 0 else ts + .3})
secoes.append(f'<section class="cena" id="PROD"><img class="foto" src="{ipanema}" alt=""><div class="veu-topo"></div>'
              f'<div class="topo"><p class="t1">e cada estampa</p><p class="t2">vira um par.</p></div></section>')
for k, uf in enumerate(RAPIDAS):
    n += 1
    ts = T_RAP + k
    secoes.append(f'<section class="cena" id="R{k}">{arco(uf, ts, ts + .5)}'
                  f'<div class="baixo"><div class="achou"><em class="nome-r">{e(POR[uf]["nome"])}</em></div></div></section>')
    rodadas.append({'id': f'R{k}', 'tipo': 'rapida', 'ts': ts, 'tr': ts + .5, 'te': ts + 1, 'n': n})
for k, uf in enumerate(RESTAM):
    ts = T_RES + .5 * k
    secoes.append(f'<section class="cena" id="Q{k}">{arco(uf, ts - 1.3)}'
                  f'<div class="baixo"><div class="achou mostra"><b>onde está?</b><em class="nome-r">{e(POR[uf]["nome"])}</em></div></div></section>')
    rodadas.append({'id': f'Q{k}', 'tipo': 'resta', 'ts': ts, 'te': ts + .5})

# os 14 pares, 4-3-4-3
pares, i = '', 0
for lin, qtd in enumerate([4, 3, 4, 3]):
    for c in range(qtd):
        uf = data[i]['uf']
        x = 540 + (c - (qtd - 1) / 2) * 235 - 105
        y = 430 + lin * 262
        rot = (-6, 4, -3, 6, -5, 3, -4)[(i * 3) % 7]
        pares += f'<img class="gp" src="../../site/img/{uf}-par.webp" style="left:{x:.0f}px;top:{y}px;transform:rotate({rot}deg)" alt="">'
        i += 1
secoes.append(f'<section class="cena" id="GRADE">{pares}<div class="topo"><p class="t1 m">14 estados, 14 pares,</p><p class="t2 m">14 corações.</p></div></section>')
secoes.append('<section class="cena centro" id="ACHOU"><p class="ac1">achou</p><p class="ac2">todos?</p></section>')
secoes.append(f'<section class="cena centro" id="FIM"><div id="simb">{folha([0, 2, 4])}{folha([1, 3, 5])}</div>'
              '<p class="f-nome"><span class="ch">B</span><span class="ch">e</span><span class="ch">m</span><span class="ch">-</span>'
              + ''.join(f'<span class="ch q">{c}</span>' for c in 'Querer') + '</p>'
              '<p class="f-sub">uma V2 conceitual da collab</p><img class="f-assin" src="../_img/assinatura-topo.svg" alt="">'
              '<p class="f-cta">o projeto inteiro está no link da bio</p>'
              '<p class="f-legal">projeto conceitual de portfólio de Emilly Silva<br>sem vínculo com FARM&nbsp;Rio e havaianas</p></section>')
# por cima de tudo: títulos das rodadas rápidas e o placar
secoes.append('<section class="cena" id="TRAP"><div class="topo"><p class="t1">agora,</p><p class="t2">mais rápido.</p></div></section>')
secoes.append(f'<section class="cena" id="TRES"><div class="topo"><p class="t1">esses {len(RESTAM)}</p><p class="t2">ficam com você.</p></div></section>')
nums = ''.join(f'<span class="n{k}">{k}</span>' for k in range(n + 1))
secoes.append(f'<section class="cena" id="PLACAR"><div class="placar"><span class="mini">{SIMB}</span><b>corações achados</b>'
              f'<span class="num">{nums}</span><span class="de">/14</span></div></section>')

CSS = '''
*{box-sizing:border-box}
:root{--creme:#F4EDE3;--creme2:#EBE2D5;--tinta:#2A1A17;--vinho:#6A1B29;--laranja:#E07A2E;--urucum:#C8321F;--suave:#857568;--claro:#F2B98A;--serif:"Instrument Serif",Georgia,serif;--sans:"Jost",system-ui,sans-serif}
html,body{margin:0;background:#000}
#palco{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--creme);color:var(--tinta);font-family:var(--sans);-webkit-font-smoothing:antialiased}
.cena{position:absolute;inset:0;visibility:hidden;overflow:hidden}
.centro{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
#L0,#L1,#L2,[id^=R],[id^=Q],#GRADE{background:var(--creme)}
#TRAP,#TRES,#PLACAR{background:none}
/* títulos no topo */
.topo{position:absolute;left:60px;right:60px;top:166px;text-align:center}
.topo p{margin:0;font:400 104px/.98 var(--serif);letter-spacing:-.025em;white-space:nowrap}
.topo .t2,.topo em{font-style:italic;color:var(--vinho)}
.topo .so{font-size:128px;padding-top:44px}
.topo .m{font-size:92px}
/* o arco */
.arco-w{position:absolute;left:__AX__px;top:__AY__px;width:__AW__px;height:__AH__px}
.arco{position:absolute;inset:0;overflow:hidden;border-radius:999px 999px 0 0;background:var(--creme2);box-shadow:0 50px 90px -50px rgba(40,10,10,.45)}
.zoom{position:absolute;inset:0}
.zoom img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.veu-c{position:absolute;inset:0;background:rgba(30,16,13,.8);opacity:0}
.anel{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.anel circle{fill:none;stroke:#FFF3E6;stroke-width:5;filter:drop-shadow(0 0 10px rgba(255,220,180,.55))}
/* embaixo do arco */
.baixo{position:absolute;left:70px;right:70px;top:1470px;height:150px;text-align:center}
.procura,.achou{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center}
.procura{opacity:0}
.procura b{display:flex;align-items:center;gap:14px;font:500 24px/1 var(--sans);letter-spacing:.3em;text-transform:uppercase;color:var(--suave)}
.pausa{display:inline-block;width:18px;height:22px;border-left:6px solid var(--vinho);border-right:6px solid var(--vinho)}
.barra{display:block;position:relative;width:420px;height:4px;margin-top:22px;background:rgba(42,26,23,.14);border-radius:4px;overflow:hidden}
.barra i{position:absolute;inset:0;background:var(--vinho);transform-origin:left;transform:scaleX(0)}
.achou{opacity:0}
.achou.mostra{opacity:1}
.achou b{font:500 24px/1 var(--sans);letter-spacing:.3em;text-transform:uppercase;color:var(--vinho)}
.achou em{margin-top:14px;font:italic 400 50px/1.12 var(--serif);color:var(--tinta);max-width:900px;text-wrap:balance}
.achou em.nome-r{margin-top:0;font:400 72px/1 var(--serif);font-style:normal}
.achou.mostra em.nome-r{margin-top:16px}
/* produto */
#PROD{background:#d9c6ad}
.foto{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 60%}
.veu-topo{position:absolute;left:0;right:0;top:0;height:640px;background:linear-gradient(180deg,rgba(244,237,227,.92) 0%,rgba(244,237,227,.6) 45%,rgba(244,237,227,0) 100%)}
/* grade */
.gp{position:absolute;width:210px;filter:drop-shadow(0 3px 3px rgba(40,10,10,.22)) drop-shadow(0 18px 22px rgba(40,10,10,.22))}
/* achou todos? */
#ACHOU{background:var(--vinho);color:#FFF3E6}
.ac1,.ac2{margin:0;font:400 250px/.9 var(--serif);letter-spacing:-.035em}
.ac2{font-style:italic;color:var(--claro)}
/* fim */
#FIM{background:var(--tinta);color:#FFF3E6;justify-content:flex-start;padding-top:420px}
#simb{position:relative;width:240px;height:222px}
#simb svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.f-nome{margin:44px 0 0;font:400 196px/.9 var(--serif);letter-spacing:-.035em;white-space:nowrap}
.f-nome .ch{display:inline-block}
.f-nome .q{font-style:italic;color:var(--claro)}
.f-sub{margin:26px 0 44px;font:italic 400 46px/1.2 var(--serif);color:rgba(255,243,230,.82)}
.f-assin{width:470px;filter:brightness(0) invert(1);opacity:.92}
.f-cta{margin:58px 0 0;font:500 24px/1 var(--sans);letter-spacing:.28em;text-transform:uppercase;color:var(--claro)}
.f-legal{position:absolute;left:80px;right:80px;top:1470px;margin:0;text-align:center;font:500 19px/1.7 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:rgba(255,243,230,.5)}
/* placar */
.placar{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:76px;display:flex;align-items:center;gap:16px;padding:14px 30px 14px 22px;border-radius:50px;background:rgba(244,237,227,.94);border:1.5px solid rgba(42,26,23,.16);white-space:nowrap}
.placar .mini{width:42px;height:39px;display:block}
.placar .mini svg{width:100%;height:100%;display:block}
.placar b{font:500 23px/1 var(--sans);letter-spacing:.22em;text-transform:uppercase;color:var(--suave);margin-right:6px}
.num{position:relative;display:inline-block;width:52px;height:42px;text-align:right}
.num span{position:absolute;right:0;top:0;font:500 42px/1 var(--sans);font-variant-numeric:tabular-nums;color:var(--vinho);opacity:0}
.num .n0{opacity:1}
.de{font:500 42px/1 var(--sans);color:var(--tinta)}
'''.replace('__AX__', str(AX)).replace('__AY__', str(AY)).replace('__AW__', str(AW)).replace('__AH__', str(AH))

JS = '''
const FPS = __FPS__, NQ = __NQ__, QD = '../_quadros/', RODADAS = __RODADAS__, DUR = __DUR__;
const quadro = (uf, t) => QD + uf + '/' + String((Math.floor(Math.max(0, t) * FPS + 1e-6) % NQ[uf]) + 1).padStart(4, '0') + '.jpg';
// só troca os quadros das cenas que estão na tela
async function trocaQuadros(t) {
  const espera = [];
  document.querySelectorAll('img[data-uf]').forEach(im => {
    if (getComputedStyle(im.closest('.cena')).visibility !== 'visible') return;
    const tt = im.dataset.t1 ? Math.min(t, +im.dataset.t1) : t;
    const src = quadro(im.dataset.uf, tt - +im.dataset.t0);
    if (im.getAttribute('src') !== src) { im.setAttribute('src', src); espera.push(im.decode().catch(() => {})); }
  });
  await Promise.all(espera);
}
const tl = gsap.timeline({ paused: true, defaults: { ease: 'power3.out' } });
const corte = (id, de, ate) => { tl.set('#' + id, { visibility: 'visible' }, de); if (ate) tl.set('#' + id, { visibility: 'hidden' }, ate); };
const IR = { immediateRender: false };
function placar(n, t) {
  tl.set('.num span', { opacity: 0 }, t).set('.num .n' + n, { opacity: 1 }, t)
    .fromTo('.placar', { scale: 1.16 }, Object.assign({ scale: 1, duration: .4, ease: 'back.out(3)' }, IR), t);
}
function revela(id, t, rapido) {
  const c = document.querySelector('#' + id + ' .anel circle');
  tl.fromTo('#' + id + ' .veu-c', { opacity: 0 }, Object.assign({ opacity: 1, duration: rapido ? .12 : .3, ease: 'power2.out' }, IR), t)
    .to(c, { strokeDashoffset: 0, duration: rapido ? .25 : .45, ease: 'power2.inOut' }, t + .04)
    .fromTo('#' + id + ' .achou', { opacity: 0, y: 18 }, Object.assign({ opacity: 1, y: 0, duration: .35 }, IR), t + .08);
}
function monta() {
  // tudo que entra com fromTo começa escondido (sem isso aparece no primeiro quadro da cena)
  gsap.set('.topo p, #ACHOU p, .f-sub, .f-assin, .f-cta, .f-legal', { opacity: 0 });
  // o primeiro quadro já mostra o arco e o placar (um set no tempo 0 não dispara no seek(0))
  gsap.set('#L0, #PLACAR', { visibility: 'visible' });
  RODADAS.forEach(r => {
    corte(r.id, r.ts, r.te);
    const s = '#' + r.id;
    if (r.ts > 0) tl.fromTo(s + ' .arco-w', { scale: .93 }, Object.assign({ scale: 1, duration: .3 }, IR), r.ts);
    if (r.tipo === 'lenta') {
      tl.fromTo(s + ' .topo p', { opacity: 0, y: 34 }, Object.assign({ opacity: 1, y: 0, duration: .45, stagger: .5 }, IR), r.ts + .02)
        .fromTo(s + ' .procura', { opacity: 0 }, Object.assign({ opacity: 1, duration: .3 }, IR), r.bar - .1)
        .fromTo(s + ' .barra i', { scaleX: 0 }, Object.assign({ scaleX: 1, duration: r.tr - r.bar, ease: 'none' }, IR), r.bar)
        .to(s + ' .procura', { opacity: 0, duration: .15 }, r.tr);
      revela(r.id, r.tr, false);
      placar(r.n, r.tr + .1);
      // a câmera entra no coração
      tl.to(s + ' .zoom', { scale: r.z, x: r.dx, y: r.dy, duration: r.te - r.tr - .5, ease: 'power2.inOut' }, r.tr + .5)
        .to(s + ' .anel circle', { attr: { 'stroke-width': 7 / r.z }, duration: r.te - r.tr - .5, ease: 'power2.inOut' }, r.tr + .5);
    } else if (r.tipo === 'rapida') {
      revela(r.id, r.tr, true);
      placar(r.n, r.tr + .05);
    }
  });
  // títulos que atravessam várias cenas
  corte('TRAP', __T_RAP__, __T_RES__);
  tl.fromTo('#TRAP .topo p', { opacity: 0, y: 34 }, Object.assign({ opacity: 1, y: 0, duration: .45, stagger: .5 }, IR), __T_RAP__ + .02);
  corte('TRES', __T_RES__, __T_GRADE__);
  tl.fromTo('#TRES .topo p', { opacity: 0, y: 34 }, Object.assign({ opacity: 1, y: 0, duration: .4, stagger: .25 }, IR), __T_RES__ + .02);
  // o par na areia de Ipanema
  corte('PROD', __P0__, __P1__);
  tl.fromTo('#PROD .foto', { scale: 1.12 }, Object.assign({ scale: 1, duration: __P1__ - __P0__, ease: 'none' }, IR), __P0__)
    .fromTo('#PROD .topo p', { opacity: 0, y: 34 }, Object.assign({ opacity: 1, y: 0, duration: .45, stagger: .5 }, IR), __P0__ + .05);
  // placar: some no produto e no fim
  tl.set('#PLACAR', { visibility: 'hidden' }, __P0__);
  corte('PLACAR', __P1__, __T_GRADE__);
  // os 14 pares
  corte('GRADE', __T_GRADE__, __T_ACHOU__);
  tl.from('.gp', { y: -260, opacity: 0, duration: .45, stagger: .045, ease: 'back.out(1.4)' }, __T_GRADE__ - .15)
    .fromTo('#GRADE .topo p', { opacity: 0, y: 34 }, Object.assign({ opacity: 1, y: 0, duration: .45, stagger: .5 }, IR), __T_GRADE__ - .12);
  // achou todos?
  corte('ACHOU', __T_ACHOU__, __T_FIM__);
  tl.fromTo('#ACHOU p', { opacity: 0, y: 50 }, Object.assign({ opacity: 1, y: 0, duration: .4, stagger: .5 }, IR), __T_ACHOU__ + .02);
  // fim: as duas folhas caem juntas e formam o coração; o nome sobe letra a letra
  const F = __T_FIM__;
  corte('FIM', F, null);
  gsap.set('.fe', { x: -430, y: -620, rotation: -75, opacity: 0 });
  gsap.set('.fd', { x: 430, y: -660, rotation: 80, opacity: 0 });
  gsap.set('.f-nome .ch', { opacity: 0, y: 60 });
  tl.to('.fe', { keyframes: { x: [-430, -170, -250, -60, 0], y: [-620, -430, -250, -90, 0], rotation: [-75, -20, -48, -8, 0], easeEach: 'sine.inOut' }, opacity: 1, duration: 1.5, ease: 'none' }, F)
    .to('.fd', { keyframes: { x: [430, 180, 240, 50, 0], y: [-660, -460, -270, -100, 0], rotation: [80, 25, 50, 10, 0], easeEach: 'sine.inOut' }, opacity: 1, duration: 1.5, ease: 'none' }, F + .1)
    .to('#simb', { scale: 1.09, duration: .2, ease: 'power2.out' }, F + 1.6)
    .to('#simb', { scale: 1, duration: .45, ease: 'back.out(3)' }, F + 1.8)
    .to('.f-nome .ch', { opacity: 1, y: 0, duration: .8, stagger: .05 }, F + 1.7)
    .fromTo('.f-sub, .f-assin, .f-cta, .f-legal', { opacity: 0, y: 22 }, Object.assign({ opacity: 1, y: 0, duration: .6, stagger: .2 }, IR), F + 2.3);
}
window.FILME = { dur: DUR, seek: async t => { tl.seek(t, false); await trocaQuadros(t); } };
window.PRONTO = document.fonts.ready.then(() => new Promise(r => setTimeout(r, 300))).then(monta);
'''
for k, v in {'__FPS__': FPS, '__NQ__': json.dumps(NQ), '__RODADAS__': json.dumps(rodadas), '__DUR__': DUR,
             '__T_RAP__': T_RAP, '__T_RES__': T_RES, '__T_GRADE__': T_GRADE, '__T_ACHOU__': T_ACHOU, '__T_FIM__': T_FIM,
             '__P0__': PROD[0], '__P1__': PROD[1]}.items():
    JS = JS.replace(k, str(v))

doc = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>reel</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Jost:wght@400;500&display=block">
<style>{CSS}</style></head><body><div id="palco">
{chr(10).join(secoes)}
</div><script src="../../site/js/gsap.min.js"></script><script>{JS}</script></body></html>'''
open(os.path.join(FIL, 'reel-coracao.html'), 'w', encoding='utf8').write(doc)
print('ok: filmes/reel-coracao.html;', f'{DUR:.1f} s;', 'zoom', {r['id']: r.get('z') for r in rodadas if r.get('z')})
