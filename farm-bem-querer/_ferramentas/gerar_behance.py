"""Post do Behance: módulos de 1400 px (exportados a 2800 px), vídeos com os motions (1280 px), capa e textos.
Ordem:  node behance_telas.js            (fotos do site)
        cd /tmp && python3 -I .../gerar_behance.py
        node behance_render.js           (módulos JPG + capa + prévia)
        node motion_camadas.js ../07-apresentacao/behance/behance.html .mod ../07-apresentacao/behance/_camadas <módulos com vídeo>
        python3 -I motion_compor.py ../07-apresentacao/behance/_camadas ../07-apresentacao/behance/videos modulo 3 1280"""
import glob
import html
import json
import os
import shutil
import sys

from PIL import Image, ImageChops, ImageStat

AQUI = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(AQUI, 'gerar_site.py'), encoding='utf8').read().split('def e(s)')[0]
exec(compile(_src, 'gerar_site_dados', 'exec'))   # data, V, T, COR, LEGENDA, REGIAO, P, SITE
sys.path.insert(0, AQUI)
from tipografia import CSS_TEXTO, sem_viuvas  # noqa: E402

OUT = os.path.join(P, '07-apresentacao', 'behance')
IMG = os.path.join(OUT, '_img')
os.makedirs(IMG, exist_ok=True)
POR = {s['uf']: s for s in data}
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from notas_estado import notas_html  # noqa: E402
PASTA = {s['uf']: glob.glob(os.path.join(P, '05-estampas', f'{i + 1:02d}-*'))[0] for i, s in enumerate(data)}


def e(s):
    return html.escape(s or '', quote=True)


def autor(a):
    return (a or '').split(' - ')[0].split(' from ')[0].strip()


_alta = {}


def alta(uf, nome_site):
    """O original em alta da pasta do estado que corresponde à imagem do site (mesma proporção, mais parecido)."""
    if (uf, nome_site) in _alta:
        return _alta[(uf, nome_site)]
    site = Image.open(os.path.join(SITE, 'img', nome_site)).convert('RGB')
    alvo = site.resize((40, round(40 * site.height / site.width)))
    melhor, dmin = os.path.join(SITE, 'img', nome_site), 14.0
    for f in glob.glob(os.path.join(PASTA[uf], '**', '*.*'), recursive=True):
        if '_versoes' in f or 'teste' in f or not f.lower().endswith(('.png', '.jpg', '.jpeg')) or 'sem-logo' in f:
            continue
        try:
            im = Image.open(f)
        except Exception:
            continue
        if im.width <= site.width or abs(im.width / im.height - site.width / site.height) > .012:
            continue
        d = sum(ImageStat.Stat(ImageChops.difference(im.convert('RGB').resize(alvo.size), alvo)).mean) / 3
        if d < dmin:
            melhor, dmin = f, d
    _alta[(uf, nome_site)] = melhor
    return melhor


def jpg(origem, lado, nome):
    dst = os.path.join(IMG, nome + '.jpg')
    if not os.path.exists(dst):
        im = Image.open(origem).convert('RGB')
        im.thumbnail((lado, lado), Image.LANCZOS)
        im.save(dst, quality=90, optimize=True)
    return '_img/' + nome + '.jpg'


def img(uf, chave, lado=1400):
    s = POR[uf]
    nome = s[chave] if isinstance(s[chave], str) else s[chave][0]
    return jpg(alta(uf, nome), lado, f'{uf}-{chave}')


def site_img(nome, lado=1000):
    return jpg(os.path.join(SITE, 'img', nome), lado, os.path.splitext(nome)[0])


def par(uf, lado=700):
    dst = os.path.join(IMG, f'{uf}-par.png')
    if not os.path.exists(dst):
        im = Image.open(os.path.join(SITE, 'img', f'{uf}-par.webp')).convert('RGBA')
        im.thumbnail((lado, lado), Image.LANCZOS)
        im.save(dst, optimize=True)
    return '_img/' + os.path.basename(dst)


for f in ['assinatura-topo.svg']:
    shutil.copy(os.path.join(SITE, 'img', f), IMG)
_s = open(P + '/03-marca/identidade-bem-querer/simbolo-cor.svg', encoding='utf8').read()
SIMB = _s[_s.index('>') + 1:_s.rindex('</svg>')]
_s = open(P + '/03-marca/identidade-bem-querer/simbolo-tinta.svg', encoding='utf8').read()
SIMB_T = _s[_s.index('>') + 1:_s.rindex('</svg>')]
svg = lambda c=SIMB, w=34: f'<svg viewBox="-6 6 212 196" width="{w}" aria-hidden="true">{c}</svg>'
mono = lambda cor, veia: SIMB_T.replace('#1D1915', cor).replace('#FCFAF6', veia)

mods = []   # (id, html, video?)


def mod(ident, corpo, classe='', video=False, estilo=''):
    mods.append((ident, f'<section class="mod {classe}" id="{ident}"{f" style={chr(34)}{estilo}{chr(34)}" if estilo else ""}>{corpo}</section>', video))


def arco(uf, extra=''):
    return f'<div class="arco"><img data-uf="{uf}" src="{img(uf, "ilu", 1300)}" alt="">{extra}</div>'


# 01 capa
mod('capa', f'''<p class="eb topo-c">havaianas ♥ FARM Rio · uma V2 conceitual da collab</p>
<div class="c-arte">{arco("ms")}<img class="flutua" src="{par("ms")}" alt=""></div>
<h1 class="w-bem">Bem-</h1><h1 class="w-que">Querer</h1>
<div class="c-pe"><p>Uma cápsula de quatorze pares, um por estado, com um coração escondido em cada estampa.</p>
<p class="aviso">Projeto fictício de portfólio de Emilly Silva. Sem vínculo com a FARM Rio ou a havaianas.</p></div>''', 'capa', video=True)

# 02 manifesto
mod('ideia', f'''<p class="eb">a ideia</p><p class="manif">A gente saiu do Rio e foi até <em>quatorze estados</em>. Em cada um, um par de chinelos feito com os elementos de lá, e um coração que só aparece na segunda olhada.</p>{svg(mono("#FFF3E6", "#6A1B29"), 92)}
<p class="aviso-i">Projeto fictício de portfólio de Emilly Silva. Sem vínculo com a FARM Rio ou a havaianas.</p>''', 'vinho centro')

# 03 desafio
mod('desafio', '''<p class="eb">o desafio</p><h2 class="h-larga">Levar o Rio para conhecer o Brasil, <em>sem virar cartão-postal</em></h2>
<div class="duas"><p class="txt">A collab havaianas ♥ FARM Rio já existe, e a FARM é carioca até no nome. A V2 imagina uma cápsula dentro dela: quatorze estados, um par por estado e a mesma assinatura no calcanhar.</p>
<p class="txt">O risco era cair no clichê de cada lugar. A resposta foi começar pela rua: cada estado foi lido por fotos reais antes de virar desenho, e cada par ganhou uma âncora, um elemento que é daquele lugar e de nenhum outro.</p></div>
<div class="numeros"><div><b>14</b><span>estados, das cinco regiões</span></div><div><b>14</b><span>pares, cada um em díptico</span></div><div><b>312</b><span>fotos de campo, de 139 fotógrafos</span></div><div><b>1</b><span>coração escondido em cada estampa</span></div></div>''')

# 04 pesquisa de campo
fotos = ''
for uf in ['mg', 'ba', 'pa', 'ms', 'sc', 'ce']:
    s = POR[uf]
    f0 = s['campo'][0]
    fotos += (f'<figure><img src="{site_img(f0["img"], 900)}" alt=""><figcaption><b>{e(s["nome"])}</b> · {e(LEGENDA[uf][0])}'
              f'<span>foto: {e(autor(f0["autor"]))} · {e(f0["licenca"])}</span></figcaption></figure>')
mod('pesquisa', f'''<p class="eb">processo · pesquisa de campo</p><h2>Antes do desenho, <em>a rua</em></h2>
<div class="fotos">{fotos}</div>
<p class="nota">312 fotos de 139 fotógrafos, com autor, licença e local conferidos.</p>''', 'c2')

# 05 método
mg = POR['mg']
passos = [('Campo', 'Fotos reais do lugar, com autor e licença, e o local conferido.', site_img(mg['campo'][0]['img'], 900)),
          ('Âncora', 'Um elemento que é daquele estado e de nenhum outro.', site_img(mg['coracao'], 700)),
          ('Chinelo', 'Díptico: o pé esquerdo e o direito contam metades da mesma cena.', img('mg', 'palmilha', 900)),
          ('Ilustração', 'O lugar inteiro, centralizado, com os mesmos elementos do chinelo.', img('mg', 'ilu', 900)),
          ('O par', 'A tira repete uma cor da estampa; a assinatura vai no calcanhar.', img('mg', 'estudio', 900))]
cols = ''.join(f'<div><div class="m-img"><img src="{src}" alt=""></div><span>{k + 1:02d}</span><h3>{t}</h3><p class="txt">{d}</p></div>'
               for k, (t, d, src) in enumerate(passos))
mod('metodo', f'''<p class="eb">processo · o método, com Minas Gerais de exemplo</p><h2>Cinco passos, <em>sempre na mesma ordem</em></h2><div class="cinco">{cols}</div>''')

# 06 as 14 ilustrações (vídeo)
grade = ''.join(f'<figure>{arco(s["uf"])}<figcaption><b>{e(s["nome"])}</b><i>{e(V[s["uf"]]["nome"])}</i></figcaption></figure>' for s in data)
mod('ilustracoes', f'''<p class="eb">a coleção</p><h2>Uma cena <em>para cada lugar</em></h2>
<p class="txt lead">Rio, mercado, duna, pampa, mata, janela, largo: cada estado tem uma cena própria, escolhida pelo que é dele e de nenhum outro.</p>
<div class="grade14">{grade}</div>''', video=True)


# 07 a 10: estados em destaque (vídeo)
def destaque(uf):
    s, t = POR[uf], V[uf]
    ac = '#6A1B29'
    mod(f'estado-{uf}', f'''<div class="d-topo"><div class="d-txt"><p class="eb">{data.index(s) + 1:02d} / 14 · {REGIAO[uf]}</p><h2>{e(s["nome"])}</h2>
<p class="d-est" style="color:{ac}">{e(t["nome"])}</p><p class="txt">{e(t["conceito"])}</p>{notas_html(uf, e)}
<div class="d-cor"><img src="{site_img(s["coracao"], 500)}" alt=""><p><b>onde está o coração</b>{e(s["coracao_texto"])}</p></div></div>
<div class="d-arte">{arco(uf)}<img class="flutua" src="{par(uf)}" alt=""></div></div>
<div class="d-tres"><figure><img src="{img(uf, "palmilha", 1000)}" alt=""><figcaption>o díptico: os dois pés contam a mesma cena</figcaption></figure>
<figure><img src="{img(uf, "estudio", 1000)}" alt=""><figcaption>o par</figcaption></figure>
<figure><img src="{img(uf, "campanha", 1000)}" alt=""><figcaption>no lugar · campanha</figcaption></figure></div>''', 'dest', video=True)


for uf in ['mg', 'pa', 'ms', 'sc']:
    destaque(uf)

# 11 os 14 pares
pares = ''.join(f'<figure><img src="{par(s["uf"])}" alt=""><figcaption>{e(s["nome"])}</figcaption></figure>' for s in data)
mod('pares', f'<p class="eb">a coleção</p><h2>Quatorze <em>pares</em></h2><div class="pares">{pares}</div>', 'c2')

# 12 corações
cors = ''.join(f'<figure><img src="{site_img(s["coracao"], 500)}" alt=""><figcaption><b>{e(s["nome"])}</b>{e(s["coracao_texto"])}</figcaption></figure>' for s in data)
mod('coracoes', f'''<p class="eb">o fio da coleção</p><h2>O coração é formado, <em>nunca desenhado</em></h2>
<p class="txt lead">Em cada estampa tem um, escondido nos próprios elementos: a franja da sombrinha de frevo, a cauda da baleia, duas folhas caindo juntas.</p>
<div class="cors">{cors}</div>''')

# 13 campanha
camp = ''.join(f'<figure><img src="{img(u, "campanha", 1100)}" alt=""><figcaption>{e(POR[u]["nome"])}</figcaption></figure>' for u in ['ce', 'ba', 'pe', 'rj', 'am', 'rs'])
mod('campanha', f'''<p class="eb">a campanha</p><h2>O par <em>no lugar</em></h2>
<p class="txt lead">Cada par foi fotografado onde a arte acontece: na areia do Ceará, no Pelourinho, no frevo do Recife.</p><div class="camp">{camp}</div>''')

# 14 o site
mod('site', '''<p class="eb">o site</p><h2>Um estado <em>por página</em></h2>
<p class="txt lead">Oito páginas e quatorze estados, com o motion de cada ilustração, a busca pelo coração e a roda dos pares para arrastar com o dedo.</p>
<div class="navegador"><span class="barra"><i></i><i></i><i></i><b>cauadorn.github.io/Dornizon-</b></span><img src="_img/tela-desk-home.png" alt=""></div>
<div class="fones"><img src="_img/tela-mob-estado.png" alt=""><img src="_img/tela-mob-roda.png" alt=""><img src="_img/tela-mob-colecao.png" alt=""></div>''', 'c2')

# 15 identidade
paleta = ''.join(f'<div><span style="background:{c}"></span><b>{n}</b><i>{c}</i></div>' for n, c in
                 [('creme', '#F4EDE3'), ('creme 2', '#EBE2D5'), ('tinta', '#2A1A17'), ('vinho', '#6A1B29'), ('laranja', '#E07A2E')])
mod('identidade', f'''<p class="eb">identidade</p><h2>A assinatura <em>não muda</em></h2>
<p class="txt lead">O logo da collab vai no calcanhar, centralizado, tom sobre tom. A cápsula só ganha um nome, Bem-Querer, e um símbolo: duas folhas de amendoeira que caem juntas e formam um coração.</p>
<div class="lockup"><img src="_img/assinatura-topo.svg" alt=""><span class="sep"></span><span class="col"><small>coleção</small>Bem-Querer</span></div>
<div class="id-grade"><div class="simb">{svg(SIMB, 230)}<p class="eb">símbolo</p></div>
<div class="tipos"><p class="t-serif">Bem-<em>Querer</em></p><p class="eb">Instrument Serif · títulos</p><p class="t-sans">quatorze estados</p><p class="eb">Jost · texto e etiqueta</p></div>
<div class="paleta">{paleta}</div></div>''')

# 16 ficha técnica
mod('ficha', '''<p class="eb">ficha técnica</p><h2>Obrigada por <em>chegar até aqui</em></h2>
<dl class="ficha-b"><dt>Conceito, pesquisa, textos e direção de arte</dt><dd>Emilly Silva</dd><dt>Imagens e motions</dt><dd>gerados com IA, sob a minha direção de arte</dd><dt>Fotos de campo</dt><dd>139 fotógrafos, sob licenças Creative Commons, com crédito completo no site</dd><dt>Assinatura</dt><dd>a da collab havaianas ♥ FARM Rio, sem alteração</dd></dl>
<div class="rodape-f"><p><b>o projeto inteiro</b>cauadorn.github.io/Dornizon-</p><p class="aviso">Bem-Querer é um projeto fictício de portfólio de Emilly Silva. Não é uma coleção oficial e não tem vínculo com a FARM Rio nem com a havaianas; as marcas aparecem só para contar a ideia.</p></div>''', 'vinho')

CAPA = f'''<section class="capa-b" id="capa-behance"><div class="cb-arte">{arco("ms")}<img class="flutua" src="{par("ms")}" alt=""></div></section>'''

CSS = '''
*{box-sizing:border-box}
:root{--creme:#F4EDE3;--creme2:#EBE2D5;--tinta:#2A1A17;--vinho:#6A1B29;--laranja:#E07A2E;--suave:#857568;--serif:"Instrument Serif",Georgia,serif;--sans:"Jost",system-ui,sans-serif}
body{margin:0;background:#cfc6ba;-webkit-font-smoothing:antialiased}
.mod{position:relative;width:1400px;overflow:hidden;background:var(--creme);color:var(--tinta);font:400 21px/1.55 var(--sans);padding:130px 120px}
.eb{font:500 14px/1.3 var(--sans);letter-spacing:.22em;text-transform:uppercase;color:var(--suave);margin:0 0 20px}
h1,h2,h3{font-family:var(--serif);font-weight:400;margin:0}
h2{font-size:96px;line-height:.95;letter-spacing:-.02em;max-width:1000px}
h2 em{color:var(--vinho)}
h3{font-size:36px;line-height:1.1;margin:8px 0 10px}
p{margin:0}
figure{margin:0}
.txt{color:#4C3C35}
.lead{max-width:760px;margin-top:28px}
.arco{position:relative;border-radius:999px 999px 0 0;overflow:hidden;aspect-ratio:3/4;background:var(--creme2)}
.arco img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 100%}
.flutua{position:absolute;z-index:2;transform:rotate(-12deg);filter:drop-shadow(0 26px 22px rgba(40,10,10,.3))}
.c2{background:var(--creme2)}
.vinho{background:var(--vinho);color:#FFF3E6}
.vinho .eb{color:rgba(255,243,230,.62)}
.vinho h2 em{color:#F2B98A}
.centro{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;min-height:920px}
/* capa */
.capa{height:1130px;padding:0}
.topo-c{position:absolute;top:84px;left:0;right:0;text-align:center;color:var(--tinta)}
.c-arte{position:absolute;left:450px;top:200px;width:500px}
.c-arte .flutua{width:160px;left:-74px;top:-34px}
.w-bem,.w-que{position:absolute;top:470px;font:400 160px/.8 var(--serif);letter-spacing:-.035em;white-space:nowrap}
.w-bem{right:986px}
.w-que{left:986px;font-style:italic;color:var(--vinho)}
.c-pe{position:absolute;left:120px;right:120px;bottom:72px;display:flex;justify-content:space-between;align-items:end;gap:80px}
.c-pe p{max-width:470px;font:italic 400 30px/1.25 var(--serif)}
.c-pe .aviso{font:400 16px/1.5 var(--sans);color:var(--suave);text-align:right;max-width:380px}
/* manifesto */
.manif{font:400 72px/1.1 var(--serif);letter-spacing:-.015em;max-width:1080px;margin:14px 0 56px}
.manif em{color:#F2B98A}
.aviso-i{position:absolute;left:0;right:0;bottom:54px;text-align:center;font:400 15px/1.4 var(--sans);color:rgba(255,243,230,.6)}
/* desafio */
.h-larga{max-width:1160px}
.duas{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:60px;margin-top:56px}
.numeros{display:grid;grid-template-columns:repeat(4,1fr);gap:30px;margin-top:80px;border-top:1px solid rgba(42,26,23,.25);padding-top:34px}
.numeros b{display:block;font:400 92px/.9 var(--serif);color:var(--vinho)}
.numeros span{display:block;margin-top:10px;color:#4C3C35;font-size:18px;line-height:1.4}
/* pesquisa */
.fotos{display:grid;grid-template-columns:repeat(3,1fr);gap:40px 26px;margin-top:60px}
.fotos img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}
.fotos figcaption{font-size:16px;line-height:1.4;margin-top:12px;color:#4C3C35}
.fotos figcaption b{font-weight:500;color:var(--tinta)}
.fotos figcaption span{display:block;font-size:12.5px;color:var(--suave);margin-top:4px}
.nota{margin-top:50px;font:italic 400 28px/1.3 var(--serif);max-width:900px}
/* método */
.cinco{display:grid;grid-template-columns:repeat(5,1fr);gap:26px;margin-top:64px}
.m-img{aspect-ratio:4/5;overflow:hidden;background:var(--creme2)}
.m-img img{width:100%;height:100%;object-fit:cover;object-position:50% 100%;display:block}
.cinco span{display:block;margin-top:20px;font:500 14px/1 var(--sans);letter-spacing:.18em;color:var(--vinho)}
.cinco .txt{font-size:17px;line-height:1.5}
/* 14 ilustrações */
.grade14{display:flex;flex-wrap:wrap;justify-content:center;gap:44px 30px;margin-top:64px}
.grade14 figure{width:208px}
.grade14 figcaption{margin-top:12px;text-align:center;font-size:15px;line-height:1.3}
.grade14 figcaption b{display:block;font-weight:500}
.grade14 figcaption i{display:block;font:italic 400 18px/1.2 var(--serif);color:var(--suave)}
/* destaque */
.d-topo{display:grid;grid-template-columns:minmax(0,1fr) 560px;gap:80px;align-items:center}
.d-txt h2{font-size:104px}
.d-est{font:italic 400 44px/1.1 var(--serif);margin:14px 0 26px}
.nota-c{color:#6A1B29 !important}
.nota-v{color:#C8321F;font-size:17px;line-height:1.5;margin-top:20px;padding-left:14px;border-left:2px solid currentColor;max-width:44ch}
.d-cor{display:flex;gap:22px;align-items:center;margin-top:36px;padding-top:30px;border-top:1px solid rgba(42,26,23,.2)}
.d-cor img{width:96px;height:96px;border-radius:50%;object-fit:cover}
.d-cor p{font:italic 400 24px/1.25 var(--serif)}
.d-cor b{display:block;font:500 13px/1 var(--sans);letter-spacing:.18em;text-transform:uppercase;font-style:normal;color:var(--vinho);margin-bottom:8px}
.d-arte{position:relative;width:560px}
.d-arte .flutua{width:180px;left:-96px;top:-34px}
.d-tres{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:100px}
.d-tres img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}
.d-tres figcaption{margin-top:12px;font-size:15px;color:var(--suave);letter-spacing:.02em}
/* pares */
.pares{display:grid;grid-template-columns:repeat(7,1fr);gap:40px 22px;margin-top:64px}
.pares img{width:100%;display:block;filter:drop-shadow(0 18px 16px rgba(40,10,10,.22))}
.pares figcaption{text-align:center;font-size:14px;margin-top:10px;color:#4C3C35}
/* corações */
.cors{display:grid;grid-template-columns:repeat(7,1fr);gap:40px 22px;margin-top:64px}
.cors img{width:100%;aspect-ratio:1;border-radius:50%;object-fit:cover;display:block}
.cors figcaption{text-align:center;font-size:13px;line-height:1.35;color:var(--suave);margin-top:12px}
.cors b{display:block;font:400 21px/1.15 var(--serif);color:var(--tinta);margin-bottom:4px}
/* campanha */
.camp{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:60px}
.camp img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}
.camp figcaption{margin-top:10px;font-size:15px;color:var(--suave)}
/* site */
.navegador{margin-top:60px;border-radius:14px;overflow:hidden;box-shadow:0 40px 80px -40px rgba(40,10,10,.45);background:#fff}
.barra{display:flex;align-items:center;gap:8px;height:44px;padding:0 18px;background:#E4DACC}
.barra i{width:12px;height:12px;border-radius:50%;background:#CDBFAE}
.barra b{margin:0 auto;font:400 14px/1 var(--sans);color:var(--suave);background:#F4EDE3;padding:7px 40px;border-radius:20px}
.navegador img{width:100%;display:block}
.fones{display:flex;justify-content:center;gap:56px;margin-top:70px}
.fones img{width:300px;border-radius:38px;border:10px solid #1E1412;box-shadow:0 40px 70px -36px rgba(40,10,10,.5);display:block}
/* identidade */
.lockup{display:flex;align-items:center;gap:34px;margin-top:70px;padding:56px 0;border-top:1px solid rgba(42,26,23,.2);border-bottom:1px solid rgba(42,26,23,.2)}
.lockup img{height:62px}
.lockup .sep{width:1.5px;height:92px;background:rgba(42,26,23,.3)}
.lockup .col{display:grid;font:italic 400 70px/1 var(--serif)}
.lockup small{font:500 17px/1 var(--sans);font-style:normal;letter-spacing:.24em;text-transform:uppercase;color:var(--suave);margin-bottom:10px}
.id-grade{display:grid;grid-template-columns:240px minmax(0,1.45fr) minmax(0,1fr);gap:60px;margin-top:64px;align-items:start}
.simb{display:grid;justify-items:start;gap:24px}
.t-serif{font:400 92px/.9 var(--serif);letter-spacing:-.03em;white-space:nowrap}
.t-serif em{color:var(--vinho)}
.t-sans{font:500 28px/1 var(--sans);letter-spacing:.22em;text-transform:uppercase;margin-top:44px;white-space:nowrap}
.tipos .eb{margin-top:14px}
.paleta{display:grid;gap:14px}
.paleta div{display:grid;grid-template-columns:64px 1fr auto;gap:18px;align-items:center}
.paleta span{width:64px;height:64px;border-radius:50%;box-shadow:inset 0 0 0 1px rgba(42,26,23,.15)}
.paleta b{font-weight:500}
.paleta i{font-style:normal;color:var(--suave);font-size:16px}
/* ficha técnica */
.ficha-b{display:grid;grid-template-columns:max-content minmax(0,1fr);gap:18px 56px;margin:70px 0 0;font-size:19px;line-height:1.45}
.ficha-b dt{color:rgba(255,243,230,.6)}
.ficha-b dd{margin:0;color:#FFF3E6}
.tres{display:grid;grid-template-columns:repeat(3,1fr);gap:44px;margin-top:70px}
.tres > div{border-top:1px solid rgba(255,243,230,.35);padding-top:22px}
.tres h3{font-size:38px}
.tres p:not(.eb){color:rgba(255,243,230,.86);font-size:18px;line-height:1.55}
.rodape-f{display:grid;grid-template-columns:1fr 1fr;gap:60px;margin-top:90px;padding-top:30px;border-top:1px solid rgba(255,243,230,.35);align-items:end}
.rodape-f p{font:italic 400 40px/1.1 var(--serif);color:#F2B98A}
.rodape-f p b{display:block;font:500 13px/1 var(--sans);font-style:normal;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,243,230,.62);margin-bottom:12px}
.rodape-f .aviso{font:400 15px/1.55 var(--sans);color:rgba(255,243,230,.7);font-style:normal}
/* capa do Behance (808 x 632, sem texto) */
.capa-b{position:relative;width:808px;height:632px;overflow:hidden;background:var(--creme)}
.cb-arte{position:absolute;left:50%;bottom:0;width:400px;transform:translateX(-50%)}
.cb-arte .flutua{width:132px;left:-70px;top:-24px}
'''

doc = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Bem-Querer · Behance</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Jost:wght@400;500&display=block">
<style>{CSS}{CSS_TEXTO}</style></head><body>{"".join(h for _, h, _ in mods)}{CAPA}</body></html>'''
open(os.path.join(OUT, 'behance.html'), 'w', encoding='utf8').write(sem_viuvas(doc))
json.dump([{'n': k + 1, 'id': i, 'video': v} for k, (i, _, v) in enumerate(mods)], open(os.path.join(OUT, 'modulos.json'), 'w'), indent=1)
print('ok', len(mods), 'módulos;', 'vídeo em', ' '.join(str(k + 1) for k, (_, _, v) in enumerate(mods) if v))
print('originais em alta:', sum(1 for v in _alta.values() if '05-estampas' in v), 'de', len(_alta))
