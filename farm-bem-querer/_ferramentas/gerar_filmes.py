"""Dois filmes para o Behance, animados em HTML (GSAP) e renderizados quadro a quadro:
  abertura.html  a assinatura da collab se revela, as duas folhas caem e formam o coração,
                 "Bem-Querer" sobe letra a letra, se abre e o arco cresce com os motions (MS e PA)
  colecao.html   a coleção em movimento: os 14 estados passando no arco, com número, nome e coração
Os motions entram como sequência de quadros (_quadros/<uf>/0001.jpg...), tirados de site/video/<uf>.mp4.
Uso: cd /tmp && python3 -I .../gerar_filmes.py  (depois do gerar_behance.py, que cria os _img)
     node filme_render.js abertura ; node filme_render.js colecao"""
import html
import json
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(AQUI, 'gerar_site.py'), encoding='utf8').read().split('def e(s)')[0]
exec(compile(_src, 'gerar_site_dados', 'exec'))   # data, V, T, COR, LEGENDA, REGIAO, P, SITE

B = os.path.join(P, '07-apresentacao', 'behance')
FIL = os.path.join(B, 'filmes')
QD = os.path.join(B, '_quadros')
VID = os.path.join(P, '07-apresentacao', 'site', 'video')
os.makedirs(FIL, exist_ok=True)
POR = {s['uf']: s for s in data}
FPS = 24


def e(s):
    return html.escape(s or '', quote=True)


# quadros dos motions (600 px de largura, 24 por segundo)
NQ = {}
for s in data:
    uf = s['uf']
    d = os.path.join(QD, uf)
    if not os.path.isdir(d) or not os.listdir(d):
        os.makedirs(d, exist_ok=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(VID, uf + '.mp4'), '-vf', f'fps={FPS},scale=600:-2:flags=lanczos',
                        '-q:v', '3', os.path.join(d, '%04d.jpg')], check=True)
    NQ[uf] = len(os.listdir(d))

_s = open(P + '/03-marca/identidade-bem-querer/simbolo-cor.svg', encoding='utf8').read()
caminhos = _s[_s.index('<path'):_s.rindex('</g>')].split('/>')
caminhos = [c + '/>' for c in caminhos if c.strip()]
# 0 haste esq, 1 haste dir, 2 folha esq, 3 folha dir, 4 veio esq, 5 veio dir
folha = lambda idx: f'<svg viewBox="-6 6 212 196"><g stroke-linecap="round">{"".join(caminhos[i] for i in idx)}</g></svg>'
FOLHA_E, FOLHA_D = folha([0, 2, 4]), folha([1, 3, 5])

COMUM_CSS = '''
*{box-sizing:border-box}
:root{--creme:#F4EDE3;--creme2:#EBE2D5;--tinta:#2A1A17;--vinho:#6A1B29;--suave:#857568;--serif:"Instrument Serif",Georgia,serif;--sans:"Jost",system-ui,sans-serif}
html,body{margin:0;background:#000}
#palco{position:relative;overflow:hidden;color:var(--tinta);font:400 21px/1.5 var(--sans);-webkit-font-smoothing:antialiased}
.eb{font:500 14px/1.3 var(--sans);letter-spacing:.22em;text-transform:uppercase;color:var(--suave);margin:0}
.arco{position:absolute;overflow:hidden;border-radius:999px 999px 0 0;background:var(--creme2)}
.arco img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 100%;opacity:0}
.par{position:absolute;opacity:0;filter:drop-shadow(0 22px 20px rgba(40,10,10,.3));transform-origin:50% 50%}
.veu{position:absolute;inset:0;opacity:0;pointer-events:none}
'''

JS_COMUM = '''
const FPS = %d, NQ = %s, QD = '../_quadros/';
const quadro = (uf, t) => QD + uf + '/' + String((Math.floor(Math.max(0, t) * FPS) %% NQ[uf]) + 1).padStart(4, '0') + '.jpg';
async function trocaQuadros(t) {
  const espera = [];
  document.querySelectorAll('img[data-uf][data-t0]').forEach(im => {
    if (+gsap.getProperty(im, 'opacity') <= 0.001 && im.dataset.ja) return;
    const src = quadro(im.dataset.uf, t - +im.dataset.t0);
    if (im.getAttribute('src') !== src) { im.setAttribute('src', src); im.dataset.ja = 1; espera.push(im.decode().catch(() => {})); }
  });
  await Promise.all(espera);
}
''' % (FPS, json.dumps(NQ))


def pagina(nome, css, corpo, js):
    doc = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{nome}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Jost:wght@400;500&display=block">
<style>{COMUM_CSS}{css}</style></head><body>{corpo}
<script src="../../site/js/gsap.min.js"></script><script>{JS_COMUM}{js}</script></body></html>'''
    open(os.path.join(FIL, nome + '.html'), 'w', encoding='utf8').write(doc)


letras = lambda w, cls: ''.join(f'<span class="ch">{c}</span>' for c in w)

# ------------------------------------------------------------------ abertura (1400 x 1130)
pagina('abertura', '''
#palco{width:1400px;height:1130px;background:var(--creme)}
#assin{position:absolute;left:50%;top:500px;width:600px;margin-left:-300px;transform-origin:50% 0}
#assin img{width:100%;display:block}
#assin .eb{text-align:center;margin-top:26px}
.topo-eb{position:absolute;left:0;right:0;top:118px;text-align:center}
#simb{position:absolute;left:590px;top:430px;width:220px;height:203px}
#simb svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible;transform-origin:50% 87.8%}
.arco{left:450px;top:200px;width:500px;height:667px}
.par{left:376px;top:166px;width:160px;transform:rotate(-12deg)}
.w{position:absolute;top:470px;font:400 160px/.8 var(--serif);letter-spacing:-.035em;white-space:nowrap}
.w .ch{display:inline-block}
.wb{right:986px}
.wq{left:986px;font-style:italic;color:var(--vinho)}
.c-pe{position:absolute;left:120px;right:120px;bottom:72px;display:flex;justify-content:space-between;align-items:end;gap:80px}
.c-pe p{margin:0;max-width:470px;font:italic 400 30px/1.25 var(--serif)}
.c-pe .aviso{font:400 16px/1.5 var(--sans);color:var(--suave);text-align:right;max-width:380px}
.veu{background:var(--creme)}
''', f'''<div id="palco">
<div id="assin"><img src="../_img/assinatura-topo.svg" alt=""><p class="eb">uma V2 conceitual da collab</p></div>
<p class="eb topo-eb">uma V2 conceitual da collab</p>
<div id="simb"><svg class="fe" viewBox="-6 6 212 196">{FOLHA_E[FOLHA_E.index('>') + 1:-6]}</svg><svg class="fd" viewBox="-6 6 212 196">{FOLHA_D[FOLHA_D.index('>') + 1:-6]}</svg></div>
<div class="arco"><img data-uf="ms" data-t0="6.9" alt=""><img data-uf="pa" data-t0="10.9" alt=""></div>
<img class="par p-ms" src="../_img/ms-par.png" alt=""><img class="par p-pa" src="../_img/pa-par.png" alt="">
<h1 class="w wb">{letras("Bem-", "")}</h1><h1 class="w wq">{letras("Querer", "")}</h1>
<div class="c-pe"><p>Uma cápsula de quatorze pares, um por estado, com um coração escondido em cada estampa.</p>
<p class="aviso">Projeto fictício de portfólio de Emilly Silva. Sem vínculo com a FARM&nbsp;Rio ou a havaianas.</p></div>
<div class="veu"></div></div>''', '''
const DUR = 15.6;
const tl = gsap.timeline({ paused: true, defaults: { ease: 'power3.out' } });
function monta() {
  // "Bem-Querer" começa inteiro e centralizado; depois cada metade vai para o seu lado do arco
  const wb = document.querySelector('.wb').getBoundingClientRect(), wq = document.querySelector('.wq').getBoundingClientRect();
  const ini = 700 - (wb.width + wq.width) / 2;
  const xb = ini - wb.left, xq = ini + wb.width - wq.left, yc = 560 - (wb.top + wb.height / 2);
  gsap.set('.wb', { x: xb, y: yc }); gsap.set('.wq', { x: xq, y: yc });
  gsap.set('.ch', { opacity: 0, y: 60 });
  gsap.set('#assin img', { clipPath: 'inset(0% 100% 0% 0%)' });
  gsap.set('#assin .eb, .topo-eb, .c-pe > *', { opacity: 0 });
  gsap.set('.fe', { x: -430, y: -620, rotation: -75, opacity: 0 });
  gsap.set('.fd', { x: 430, y: -660, rotation: 80, opacity: 0 });
  gsap.set('.arco', { clipPath: 'inset(100% 0% 0% 0% round 999px 999px 0px 0px)' });
  // 1. a assinatura da collab
  tl.to('#assin img', { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.1, ease: 'power2.inOut' }, 0.3)
    .fromTo('#assin', { y: 14 }, { y: 0, duration: 1.4 }, 0.3)
    .fromTo('#assin .eb', { opacity: 0, letterSpacing: '.5em' }, { opacity: 1, letterSpacing: '.22em', duration: 1 }, 1.0)
    .to('#assin .eb', { opacity: 0, duration: .35, ease: 'power1.in' }, 2.2)
    .to('#assin', { y: -436, scale: .5, duration: 1.1, ease: 'power3.inOut' }, 2.3)
    .to('.topo-eb', { opacity: 1, duration: .8 }, 3.1)
  // 2. as duas folhas de amendoeira caem juntas e formam o coração
    .to('.fe', { keyframes: { x: [-430, -170, -250, -60, 0], y: [-620, -430, -250, -90, 0], rotation: [-75, -20, -48, -8, 0], easeEach: 'sine.inOut' }, opacity: 1, duration: 2.0, ease: 'none' }, 2.4)
    .to('.fd', { keyframes: { x: [430, 180, 240, 50, 0], y: [-660, -460, -270, -100, 0], rotation: [80, 25, 50, 10, 0], easeEach: 'sine.inOut' }, opacity: 1, duration: 2.0, ease: 'none' }, 2.55)
    .to('#simb', { scale: 1.09, duration: .22, ease: 'power2.out' }, 4.55)
    .to('#simb', { scale: 1, duration: .5, ease: 'back.out(3)' }, 4.77)
    .to('#simb', { y: -50, scale: .6, opacity: 0, duration: .55, ease: 'power2.in' }, 4.95)
  // 3. Bem-Querer, letra a letra, e o arco
    .to('.ch', { opacity: 1, y: 0, duration: .9, stagger: .05 }, 5.45)
    .to('.wb, .wq', { x: 0, y: 0, duration: 1.05, ease: 'power3.inOut' }, 6.45)
    .to('.arco', { clipPath: 'inset(0% 0% 0% 0% round 999px 999px 0px 0px)', duration: 1.4, ease: 'power3.inOut' }, 7.0)
    .set('.arco img[data-uf="ms"]', { opacity: 1 }, 6.9)
    .fromTo('.p-ms', { opacity: 0, y: -90, rotation: -40 }, { opacity: 1, y: 0, rotation: -12, duration: .9, ease: 'back.out(1.6)' }, 8.0)
    .fromTo('.c-pe > *', { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 1, stagger: .15 }, 8.4)
  // 4. troca para o Pará
    .to('.arco img[data-uf="pa"]', { opacity: 1, duration: .7, ease: 'power1.inOut' }, 10.9)
    .to('.p-ms', { opacity: 0, y: -20, duration: .5, ease: 'power1.in' }, 10.8)
    .fromTo('.p-pa', { opacity: 0, y: -90, rotation: -40 }, { opacity: 1, y: 0, rotation: -12, duration: .9, ease: 'back.out(1.6)' }, 11.2)
  // 5. some no creme para o loop recomeçar limpo
    .to('.veu', { opacity: 1, duration: .6, ease: 'power1.inOut' }, DUR - .6);
}
window.FILME = { dur: DUR, seek: async t => { tl.seek(t, false); await trocaQuadros(t); } };
window.PRONTO = document.fonts.ready.then(() => new Promise(r => setTimeout(r, 300))).then(monta);
''')

# ------------------------------------------------------------------ a coleção em movimento (1400 x 880)
SEG, XF = 2.3, .45
blocos_txt, imgs, pares, cors, pontos = '', '', '', '', ''
for i, s in enumerate(data):
    uf, t0 = s['uf'], round(i * SEG, 3)
    blocos_txt += (f'<div class="est" data-i="{i}"><div class="m"><p class="num">{i + 1:02d}</p></div>'
                   f'<div class="m"><p class="nome">{e(s["nome"])}</p></div><div class="m"><p class="estampa">{e(V[uf]["nome"])}</p></div>'
                   f'<div class="m"><p class="reg">{e(REGIAO[uf])}</p></div></div>')
    imgs += f'<img data-uf="{uf}" data-t0="{max(0, t0 - XF):.3f}" data-i="{i}" alt="">'
    pares += f'<img class="par" data-i="{i}" src="../_img/{uf}-par.png" alt="">'
    cors += (f'<div class="cor" data-i="{i}"><img src="../_img/{os.path.splitext(s["coracao"])[0]}.jpg" alt="">'
             f'<p><b>onde está o coração</b>{e(s["coracao_texto"])}</p></div>')
    pontos += f'<i data-i="{i}"></i>'

pagina('colecao', '''
#palco{width:1400px;height:880px;background:var(--creme2)}
.topo-c{position:absolute;left:120px;top:76px}
.topo-c .eb{color:var(--tinta)}
.simb-c{position:absolute;right:120px;top:66px;width:44px}
.arco{left:470px;top:150px;width:460px;height:613px}
.par{left:400px;top:118px;width:150px;transform:rotate(-12deg)}
.est{position:absolute;left:120px;top:250px;width:330px}
.m{overflow:hidden;padding-bottom:.08em}
.m p{margin:0}
.num{font:400 150px/.9 var(--serif);color:var(--vinho);letter-spacing:-.03em}
.nome{font:400 50px/1.02 var(--serif);margin-top:18px;letter-spacing:-.01em}
.estampa{font:italic 400 30px/1.2 var(--serif);color:var(--suave);margin-top:8px}
.reg{font:500 13px/1 var(--sans);letter-spacing:.22em;text-transform:uppercase;color:var(--suave);margin-top:26px}
.cor{position:absolute;left:1000px;top:330px;width:290px;opacity:0}
.cor img{width:120px;height:120px;border-radius:50%;object-fit:cover;display:block}
.cor p{margin:22px 0 0;font:italic 400 28px/1.22 var(--serif)}
.cor b{display:block;font:500 13px/1 var(--sans);letter-spacing:.2em;text-transform:uppercase;font-style:normal;color:var(--vinho);margin-bottom:10px}
.pontos{position:absolute;left:0;right:0;bottom:56px;display:flex;justify-content:center;gap:10px}
.pontos i{display:block;width:26px;height:3px;border-radius:2px;background:rgba(42,26,23,.18)}
.pontos i.on{background:var(--vinho)}
.veu{background:var(--creme2)}
''', f'''<div id="palco"><div class="topo-c"><p class="eb">a coleção em movimento</p></div>
<svg class="simb-c" viewBox="-6 6 212 196"><g stroke-linecap="round">{"".join(caminhos)}</g></svg>
<div class="arco">{imgs}</div>{pares}{blocos_txt}{cors}<div class="pontos">{pontos}</div><div class="veu"></div></div>''', f'''
const SEG = {SEG}, XF = {XF}, N = {len(data)}, DUR = +(N * SEG + .2).toFixed(2);
const tl = gsap.timeline({{ paused: true, defaults: {{ ease: 'power3.out' }} }});
const sel = (c, i) => document.querySelectorAll(c + '[data-i="' + i + '"]');
function monta() {{
  gsap.set('.est .m p', {{ yPercent: 105 }});
  gsap.set('.cor, .par', {{ opacity: 0 }});
  for (let i = 0; i < N; i++) {{
    const t = i * SEG, sai = t + SEG;
    const ps = document.querySelectorAll('.est[data-i="' + i + '"] .m p');
    tl.to(sel('.arco img', i), {{ opacity: 1, duration: i ? XF : .01, ease: 'power1.inOut' }}, i ? t - XF : 0)
      .to(ps, {{ yPercent: 0, duration: .7, stagger: .06 }}, i ? t - .1 : 0)
      .fromTo(sel('.par', i), {{ opacity: 0, y: -70, rotation: -36 }}, {{ opacity: 1, y: 0, rotation: -12, duration: .8, ease: 'back.out(1.6)' }}, i ? t : .15)
      .fromTo(sel('.cor', i), {{ opacity: 0, y: 18 }}, {{ opacity: 1, y: 0, duration: .6 }}, i ? t + .1 : .2)
      .set(sel('.pontos i', i), {{ className: 'on' }}, i ? t - .1 : 0);
    if (i < N - 1) {{
      tl.to(ps, {{ yPercent: -105, duration: .45, stagger: .04, ease: 'power2.in' }}, sai - .55)
        .to(sel('.par', i), {{ opacity: 0, y: -16, duration: .35, ease: 'power1.in' }}, sai - .4)
        .to(sel('.cor', i), {{ opacity: 0, duration: .35, ease: 'power1.in' }}, sai - .4)
        .to(sel('.arco img', i), {{ opacity: 0, duration: .01 }}, sai + .02)
        .set(sel('.pontos i', i), {{ className: '' }}, sai - .1);
    }}
  }}
  tl.fromTo('.veu', {{ opacity: 1 }}, {{ opacity: 0, duration: .4, ease: 'power1.out' }}, 0)
    .to('.veu', {{ opacity: 1, duration: .5, ease: 'power1.inOut' }}, DUR - .5);
}}
window.FILME = {{ dur: DUR, seek: async t => {{ tl.seek(t, false); await trocaQuadros(t); }} }};
window.PRONTO = document.fonts.ready.then(() => new Promise(r => setTimeout(r, 300))).then(monta);
''')
print('ok: filmes/abertura.html e filmes/colecao.html;', sum(NQ.values()), 'quadros de motion')
