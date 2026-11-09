"""Dois filmes para o Behance, animados em HTML (GSAP) e renderizados quadro a quadro:
  abertura.html  só tipografia: a assinatura da collab se revela, as duas folhas caem e formam o coração,
                 o coração desce e "Bem-Querer" sobe letra a letra, com "coleção" em cima
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

# ------------------------------------------------------------------ abertura (1400 x 900): só o nome e a coleção
pagina('abertura', """
#palco{width:1400px;height:900px;background:var(--creme)}
#assin{position:absolute;left:50%;top:360px;width:600px;margin-left:-300px;transform-origin:50% 0}
#assin img{width:100%;display:block}
#assin .eb{text-align:center;margin-top:26px}
.topo-eb{position:absolute;left:0;right:0;top:118px;text-align:center}
#simb{position:absolute;left:590px;top:330px;width:220px;height:203px}
#simb svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible;transform-origin:50% 87.8%}
.col-eb{position:absolute;left:0;right:0;top:300px;text-align:center;color:var(--tinta)}
.titulo{position:absolute;left:0;right:0;top:350px;margin:0;text-align:center;font:400 190px/.8 var(--serif);letter-spacing:-.035em;white-space:nowrap}
.titulo .ch{display:inline-block}
.titulo .q{font-style:italic;color:var(--vinho)}
.frase{position:absolute;left:0;right:0;top:654px;margin:0;text-align:center;font:italic 400 30px/1.3 var(--serif);color:var(--suave)}
.legal{position:absolute;left:0;right:0;bottom:56px;margin:0;text-align:center;font:500 13px/1.4 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--suave)}
.veu{background:var(--creme)}
""", f"""<div id="palco">
<div id="assin"><img src="../_img/assinatura-topo.svg" alt=""><p class="eb">uma V2 conceitual da collab</p></div>
<p class="eb topo-eb">uma V2 conceitual da collab</p>
<p class="eb col-eb">coleção</p>
<h1 class="titulo">{letras("Bem-", "")}<span class="q">{letras("Querer", "")}</span></h1>
<div id="simb"><svg class="fe" viewBox="-6 6 212 196">{FOLHA_E[FOLHA_E.index('>') + 1:-6]}</svg><svg class="fd" viewBox="-6 6 212 196">{FOLHA_D[FOLHA_D.index('>') + 1:-6]}</svg></div>
<p class="frase">quatorze estados, quatorze pares, um coração escondido em cada estampa</p>
<p class="legal">projeto conceitual de portfólio · sem vínculo com FARM&nbsp;Rio e havaianas</p>
<div class="veu"></div></div>""", """
const DUR = 11.2;
const tl = gsap.timeline({ paused: true, defaults: { ease: 'power3.out' } });
function monta() {
  gsap.set('.ch', { opacity: 0, y: 70 });
  gsap.set('#assin img', { clipPath: 'inset(0% 100% 0% 0%)' });
  gsap.set('#assin .eb, .topo-eb, .col-eb, .frase', { opacity: 0 });
  gsap.set('.fe', { x: -430, y: -620, rotation: -75, opacity: 0 });
  gsap.set('.fd', { x: 430, y: -660, rotation: 80, opacity: 0 });
  // 1. a assinatura da collab
  tl.to('#assin img', { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.1, ease: 'power2.inOut' }, 0.3)
    .fromTo('#assin', { y: 14 }, { y: 0, duration: 1.4 }, 0.3)
    .fromTo('#assin .eb', { opacity: 0, letterSpacing: '.5em' }, { opacity: 1, letterSpacing: '.22em', duration: 1 }, 1.0)
    .to('#assin .eb', { opacity: 0, duration: .35, ease: 'power1.in' }, 2.2)
    .to('#assin', { y: -296, scale: .5, duration: 1.1, ease: 'power3.inOut' }, 2.3)
    .to('.topo-eb', { opacity: 1, duration: .8 }, 3.1)
  // 2. as duas folhas de amendoeira caem juntas e formam o coração
    .to('.fe', { keyframes: { x: [-430, -170, -250, -60, 0], y: [-620, -430, -250, -90, 0], rotation: [-75, -20, -48, -8, 0], easeEach: 'sine.inOut' }, opacity: 1, duration: 2.0, ease: 'none' }, 2.4)
    .to('.fd', { keyframes: { x: [430, 180, 240, 50, 0], y: [-660, -460, -270, -100, 0], rotation: [80, 25, 50, 10, 0], easeEach: 'sine.inOut' }, opacity: 1, duration: 2.0, ease: 'none' }, 2.55)
    .to('#simb', { scale: 1.09, duration: .22, ease: 'power2.out' }, 4.55)
    .to('#simb', { scale: 1, duration: .5, ease: 'back.out(3)' }, 4.77)
  // 3. o coração desce e fica embaixo do nome; Bem-Querer sobe letra a letra
    .to('#simb', { y: 152, scale: .3, duration: .8, ease: 'power3.inOut' }, 5.05)
    .to('.ch', { opacity: 1, y: 0, duration: 1, stagger: .055 }, 5.55)
    .fromTo('.col-eb', { opacity: 0, letterSpacing: '.6em' }, { opacity: 1, letterSpacing: '.22em', duration: 1.1 }, 6.6)
    .fromTo('.frase', { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 1 }, 7.0)
    .fromTo('.legal', { opacity: 0 }, { opacity: 1, duration: 1 }, 7.6)
  // 4. some no creme para o loop recomeçar limpo
    .to('.veu', { opacity: 1, duration: .6, ease: 'power1.inOut' }, DUR - .6);
}
window.FILME = { dur: DUR, seek: async t => { tl.seek(t, false); await trocaQuadros(t); } };
window.PRONTO = document.fonts.ready.then(() => new Promise(r => setTimeout(r, 300))).then(monta);
""")

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
# ------------------------------------------------------------------ linkedin (1080 x 1350, 4:5): o vídeo do post
caixas = {c['estado']: c['caixa'] for c in json.load(open(os.path.join(P, '_ferramentas', 'mapa_coracoes_caixas.json'), encoding='utf8'))}
A_W = 620
A_H = round(A_W * 2336 / 1744)
grade, focos = '', ''
for i, s_ in enumerate(data):
    grade += (f'<figure class="cel" data-i="{i}"><div class="arco"><img data-uf="{s_["uf"]}" data-t0="5.3" alt=""></div>'
              f'<img class="pc" src="../_img/{s_["uf"]}-par.png" alt=""></figure>')
ESTRELAS = [('sc', 11.6), ('ba', 15.0), ('rj', 18.4)]
for k, (uf, t0) in enumerate(ESTRELAS):
    x0, y0, x1, y1 = caixas[POR[uf]['nome']]
    cx, cy = (x0 + x1) / 2 / 1744 * 100, (y0 + y1) / 2 / 2336 * 100
    raio = max(max(x1 - x0, y1 - y0) * .62 / 1744 * A_W, 58)
    focos += (f'<div class="foco" data-k="{k}"><div class="arco grande"><img data-uf="{uf}" data-t0="{t0 - .4:.2f}" alt="">'
              f'<div class="veu-c" style="-webkit-mask-image:radial-gradient(circle {raio:.0f}px at {cx:.2f}% {cy:.2f}%,transparent 97%,#000 100%);'
              f'mask-image:radial-gradient(circle {raio:.0f}px at {cx:.2f}% {cy:.2f}%,transparent 97%,#000 100%)"></div>'
              f'<div class="anel" style="left:{cx:.2f}%;top:{cy:.2f}%;width:{2 * raio:.0f}px;height:{2 * raio:.0f}px"></div></div>'
              f'<p class="leg"><b>{e(POR[uf]["nome"])}</b>{e(POR[uf]["coracao_texto"])}</p></div>')

pagina('linkedin', f"""
#palco{{width:1080px;height:1350px;background:var(--creme)}}
.cena{{position:absolute;inset:0}}
#assin{{position:absolute;left:50%;top:250px;width:520px;margin-left:-260px}}
#assin img{{width:100%;display:block}}
#simb{{position:absolute;left:440px;top:470px;width:200px;height:185px}}
#simb svg{{position:absolute;inset:0;width:100%;height:100%;overflow:visible;transform-origin:50% 87.8%}}
.titulo{{position:absolute;left:0;right:0;top:640px;margin:0;text-align:center;font:400 158px/.8 var(--serif);letter-spacing:-.035em;white-space:nowrap}}
.titulo .ch{{display:inline-block}}
.titulo .q{{font-style:italic;color:var(--vinho)}}
.sub{{position:absolute;left:0;right:0;top:900px;text-align:center;font:italic 400 34px/1.3 var(--serif);color:var(--suave);margin:0}}
.cab{{position:absolute;left:70px;right:70px;top:120px;height:120px;overflow:hidden}}
.cab h2{{position:absolute;left:0;top:0;margin:0;font:400 104px/1 var(--serif);letter-spacing:-.025em}}
.cab h2 em{{color:var(--vinho)}}
.grade{{position:absolute;left:70px;right:70px;top:330px;display:flex;flex-wrap:wrap;justify-content:center;gap:34px 22px}}
.cel{{position:relative;width:170px;height:228px;margin:0}}
.cel .arco{{inset:0}}
.cel .arco img,.arco.grande img{{opacity:1}}
.cab-sub{{position:absolute;left:70px;top:250px;margin:0;font:italic 400 36px/1.2 var(--serif);color:var(--suave);opacity:0}}
.cel .pc{{position:absolute;left:8%;top:6%;width:84%;opacity:0;filter:drop-shadow(0 16px 14px rgba(40,10,10,.25))}}
.foco{{position:absolute;inset:0;opacity:0}}
.arco.grande{{left:{(1080 - A_W) // 2}px;top:300px;width:{A_W}px;height:{A_H}px}}
.veu-c{{position:absolute;inset:0;background:rgba(30,16,14,.74);opacity:0}}
.anel{{position:absolute;transform:translate(-50%,-50%);border:3px solid #FFF3E6;border-radius:50%;opacity:0;box-shadow:0 0 0 6px rgba(255,243,230,.18)}}
.leg{{position:absolute;left:90px;right:90px;top:{300 + A_H + 34}px;margin:0;text-align:center;font:italic 400 40px/1.2 var(--serif)}}
.leg b{{display:block;font:500 15px/1 var(--sans);font-style:normal;letter-spacing:.24em;text-transform:uppercase;color:var(--vinho);margin-bottom:14px}}
.fim{{position:absolute;inset:0;background:var(--vinho);color:#FFF3E6;clip-path:inset(100% 0 0 0);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
.fim svg{{width:96px;margin-bottom:46px}}
.fim h2{{margin:0;font:400 132px/.95 var(--serif);letter-spacing:-.03em}}
.fim h2 em{{display:block;font-size:104px;color:#F2B98A}}
.fim .pe{{position:absolute;left:0;right:0;bottom:90px;font:500 15px/1.6 var(--sans);letter-spacing:.22em;text-transform:uppercase;color:rgba(255,243,230,.66);margin:0}}
.veu{{background:var(--creme)}}
""", f"""<div id="palco">
<div class="cena" id="cA">
  <div id="assin"><img src="../_img/assinatura-topo.svg" alt=""></div>
  <div id="simb"><svg class="fe" viewBox="-6 6 212 196">{FOLHA_E[FOLHA_E.index('>') + 1:-6]}</svg><svg class="fd" viewBox="-6 6 212 196">{FOLHA_D[FOLHA_D.index('>') + 1:-6]}</svg></div>
  <h1 class="titulo">{letras("Bem-", "")}<span class="q">{letras("Querer", "")}</span></h1>
  <p class="sub">uma V2 conceitual da collab havaianas ♥ FARM&nbsp;Rio</p>
</div>
<div class="cena" id="cB">
  <div class="cab"><h2 class="h1">14 <em>estados.</em></h2><h2 class="h2">14 <em>pares.</em></h2><h2 class="h3">14 <em>corações.</em></h2></div>
  <p class="cab-sub">e nenhum foi desenhado.</p>
  <div class="grade">{grade}</div>
  {focos}
</div>
<div class="fim"><svg viewBox="-6 6 212 196"><g stroke-linecap="round">{"".join(caminhos)}</g></svg><h2>E aí,<em>achou todos os corações?</em></h2>
<p class="pe">Bem-Querer · Emilly Silva<br>projeto conceitual de portfólio · sem vínculo com FARM&nbsp;Rio e havaianas</p></div>
<div class="veu"></div></div>""", """
const DUR = 26.0;
const tl = gsap.timeline({ paused: true, defaults: { ease: 'power3.out' } });
function monta() {
  gsap.set('.ch', { opacity: 0, y: 60 });
  gsap.set('#assin img', { clipPath: 'inset(0% 100% 0% 0%)' });
  gsap.set('.sub, .grade .arco', { opacity: 0 });
  gsap.set('.cab h2', { yPercent: 110 });
  gsap.set('.fe', { x: -360, y: -560, rotation: -75, opacity: 0 });
  gsap.set('.fd', { x: 360, y: -600, rotation: 80, opacity: 0 });
  // A. assinatura, folhas, coração, nome
  tl.to('#assin img', { clipPath: 'inset(0% 0% 0% 0%)', duration: .8, ease: 'power2.inOut' }, .15)
    .to('.fe', { keyframes: { x: [-360, -140, -200, -50, 0], y: [-560, -380, -220, -80, 0], rotation: [-75, -20, -45, -8, 0], easeEach: 'sine.inOut' }, opacity: 1, duration: 1.5, ease: 'none' }, .6)
    .to('.fd', { keyframes: { x: [360, 150, 200, 40, 0], y: [-600, -400, -240, -90, 0], rotation: [80, 25, 48, 10, 0], easeEach: 'sine.inOut' }, opacity: 1, duration: 1.5, ease: 'none' }, .7)
    .to('#simb', { scale: 1.1, duration: .2, ease: 'power2.out' }, 2.2)
    .to('#simb', { scale: 1, duration: .45, ease: 'back.out(3)' }, 2.4)
    .to('#simb', { y: 273, scale: .32, duration: .7, ease: 'power3.inOut' }, 2.75)
    .to('.ch', { opacity: 1, y: 0, duration: .8, stagger: .045 }, 2.85)
    .fromTo('.sub', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .8 }, 3.5)
    .to('#cA', { opacity: 0, y: -60, duration: .55, ease: 'power2.in' }, 4.6)
  // B. 14 estados -> 14 pares
    .to('.cab .h1', { yPercent: 0, duration: .7 }, 5.15)
    .fromTo('.grade .arco', { opacity: 0, y: 40, scale: .9 }, { opacity: 1, y: 0, scale: 1, duration: .7, stagger: .055 }, 5.3)
    .to('.cab .h1', { yPercent: -110, duration: .45, ease: 'power2.in' }, 7.75)
    .to('.cab .h2', { yPercent: 0, duration: .7 }, 8.05)
    .to('.grade .arco', { opacity: 0, duration: .45, stagger: .04, ease: 'power1.inOut' }, 7.9)
    .fromTo('.grade .pc', { opacity: 0, y: -30, rotation: -14 }, { opacity: 1, y: 0, rotation: 0, duration: .7, stagger: .04, ease: 'back.out(1.6)' }, 8.0)
    .to('.grade', { opacity: 0, y: -30, duration: .5, ease: 'power2.in' }, 10.4)
    .to('.cab .h2', { yPercent: -110, duration: .45, ease: 'power2.in' }, 10.5)
    .to('.cab .h3', { yPercent: 0, duration: .7 }, 10.85)
    .fromTo('.cab-sub', { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .7 }, 11.3);
  // C. três corações acesos
  const T = [11.2, 14.6, 18.0];
  T.forEach(function (t, k) {
    const f = '.foco[data-k="' + k + '"]';
    tl.to(f, { opacity: 1, duration: .45, ease: 'power1.inOut' }, t)
      .fromTo(f + ' .leg', { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: .7 }, t + 1.15)
      .to(f + ' .veu-c', { opacity: 1, duration: .6, ease: 'power2.inOut' }, t + 1.0)
      .fromTo(f + ' .anel', { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: .7, ease: 'back.out(1.8)' }, t + 1.05);
    if (k < T.length - 1) tl.to(f, { opacity: 0, duration: .45, ease: 'power1.inOut' }, T[k + 1] + .05);
  });
  // D. pergunta final
  tl.to('.fim', { clipPath: 'inset(0% 0 0 0)', duration: .9, ease: 'power3.inOut' }, 21.6)
    .from('.fim svg', { opacity: 0, y: 20, duration: .7 }, 22.2)
    .from('.fim h2', { opacity: 0, y: 30, duration: .8 }, 22.35)
    .from('.fim .pe', { opacity: 0, duration: .8 }, 22.9)
    .to('.veu', { opacity: 1, duration: .6, ease: 'power1.inOut' }, DUR - .6);
}
window.FILME = { dur: DUR, seek: async t => { tl.seek(t, false); await trocaQuadros(t); } };
window.PRONTO = document.fonts.ready.then(() => new Promise(r => setTimeout(r, 300))).then(monta);
""")
print('ok: filmes/abertura.html e filmes/colecao.html;', sum(NQ.values()), 'quadros de motion')
