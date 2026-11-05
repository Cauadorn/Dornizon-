"""Carrossel do Instagram (1080 x 1440, 3:4) na identidade do Bem-Querer.
Uso: cd /tmp && python3 -I /home/user/Dornizon-/farm-bem-querer/_ferramentas/gerar_insta.py
     node /home/user/Dornizon-/farm-bem-querer/_ferramentas/insta_render.js
A menção a IA fica só no último slide (pedido da Emilly)."""
import html
import json
import os

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(AQUI, 'gerar_site.py'), encoding='utf8').read().split('def e(s)')[0]
exec(compile(_src, 'gerar_site_dados', 'exec'))   # data, V, T, COR, LEGENDA, REGIAO, P, SITE
OUT = os.path.join(P, '07-apresentacao', 'instagram')
IMG = os.path.join(OUT, '_img')
os.makedirs(IMG, exist_ok=True)
POR = {s['uf']: s for s in data}


def e(s):
    return html.escape(s or '', quote=True)


def autor(a):
    return (a or '').split(' - ')[0].split(' from ')[0].strip()


def jpg(nome, lado=1300, q=88, origem=None):
    dst = os.path.join(IMG, os.path.splitext(os.path.basename(nome))[0] + '.jpg')
    if not os.path.exists(dst):
        im = Image.open(origem or os.path.join(SITE, 'img', nome)).convert('RGB')
        im.thumbnail((lado, lado), Image.LANCZOS)
        im.save(dst, quality=q, optimize=True)
    return '_img/' + os.path.basename(dst)


def par(uf, lado=700):
    dst = os.path.join(IMG, f'{uf}-par.png')
    if not os.path.exists(dst):
        im = Image.open(os.path.join(SITE, 'img', f'{uf}-par.webp')).convert('RGBA')
        im.thumbnail((lado, lado), Image.LANCZOS)
        im.save(dst, optimize=True)
    return '_img/' + os.path.basename(dst)


_s = open(P + '/03-marca/identidade-bem-querer/simbolo-cor.svg', encoding='utf8').read()
SIMB = _s[_s.index('>') + 1:_s.rindex('</svg>')]
_s = open(P + '/03-marca/identidade-bem-querer/simbolo-tinta.svg', encoding='utf8').read()
SIMB_T = _s[_s.index('>') + 1:_s.rindex('</svg>')]
svg = lambda c=SIMB, w=34: f'<svg viewBox="-6 6 212 196" width="{w}" aria-hidden="true">{c}</svg>'
mono = lambda cor, veia: SIMB_T.replace('#1D1915', cor).replace('#FCFAF6', veia)
caixas = {c['estado']: c['caixa'] for c in json.load(open(os.path.join(AQUI, 'mapa_coracoes_caixas.json'), encoding='utf8'))}

slides, alts = [], []
N = 13


def sl(corpo, alt, classe='', topo=True):
    n = len(slides) + 1
    cab = f'<div class="cab"><span>{svg(w=30)}bem-querer</span><span>{n:02d} / {N}</span></div>' if topo else ''
    slides.append(f'<section class="sl {classe}">{cab}{corpo}</section>')
    alts.append(alt)


def arco_estado(uf):
    s, t = POR[uf], V[uf]
    sl(f'''<p class="eb">{data.index(s) + 1:02d} / 14 · {REGIAO[uf]}</p><h2 class="nome">{e(s["nome"])}</h2><p class="est">{e(t["nome"])}</p>
<div class="arte"><div class="arco"><img src="{jpg(s["ilu"])}" alt=""></div><img class="flutua" src="{par(uf)}" alt=""></div>
<p class="cor-l"><b>o coração:</b> {e(s["coracao_texto"])}</p>''',
       f'{s["nome"]}: ilustração "{t["nome"]}" num arco, com o par de chinelos por cima. {t["conceito"]} O coração escondido: {s["coracao_texto"]}.', 'estado')


def holofote(uf, revela):
    s = POR[uf]
    x0, y0, x1, y1 = caixas[s['nome']]
    d = max(x1 - x0, y1 - y0) * 1.3
    alvo = (f'<span class="alvo{" on" if revela else ""}" style="left:{(x0 + x1) / 2 / 1744 * 100:.2f}%;top:{(y0 + y1) / 2 / 2336 * 100:.2f}%;'
            f'width:{d / 1744 * 100:.2f}%;height:{d / 2336 * 100:.2f}%"></span>')
    img = jpg(f'{uf}-ilu-sem-g.jpg')
    if revela:
        txt = f'<h2>Achou?</h2><p class="sub">{e(s["coracao_texto"][:1].upper() + s["coracao_texto"][1:])}. Ele não foi desenhado: são os próprios elementos que formam o coração.</p>'
        alt = f'A mesma ilustração escurecida, com só o coração aceso: {s["coracao_texto"]}.'
    else:
        txt = '<h2>Consegue achar <em>o coração?</em></h2><p class="sub">Em cada estampa tem um, escondido. Procure antes de passar.</p>'
        alt = f'Ilustração de {s["nome"]} ({V[uf]["nome"]}) com um coração escondido nos elementos. Desafio: achar o coração.'
    sl(f'{txt}<div class="quadro"><img src="{img}" alt="">{alvo}</div>', alt, 'busca' + (' revelado' if revela else ''))


# 1 capa
pa = POR['pa']
sl(f'''<h1><span>Bem-</span><em>Querer</em></h1><p class="eb capa-eb">uma V2 da collab havaianas ♥ FARM Rio · conceito</p>
<div class="capa-arte"><div class="arco"><img src="{jpg(pa["ilu"])}" alt=""></div><img class="flutua" src="{par("pa")}" alt=""></div>''',
   'Capa: "Bem-Querer", uma V2 conceitual da collab havaianas ♥ FARM Rio. Ilustração do Pará num arco, com o par de chinelos por cima.', 'capa', topo=False)
# 2 manifesto
sl(f'''<p class="eb">a ideia</p><p class="manif">A gente saiu do Rio e foi até <em>quatorze estados</em>. Em cada um, um par de chinelos feito com os elementos de lá, e um coração que só aparece na segunda olhada.</p>{svg(w=96)}''',
   'Texto: A gente saiu do Rio e foi até quatorze estados. Em cada um, um par de chinelos feito com os elementos de lá, e um coração que só aparece na segunda olhada.', 'centro')
# 3 campo x estampa
mg = POR['mg']
f0 = mg['campo'][0]
sl(f'''<h2>Antes do desenho, <em>a rua</em></h2>
<div class="dupla"><figure><img src="{jpg(f0["img"])}" alt=""><figcaption>a rua · {e(LEGENDA["mg"][0])}<span>foto: {e(autor(f0["autor"]))} · {e(f0["licenca"])}</span></figcaption></figure>
<figure><div class="arco"><img src="{jpg(mg["ilu"])}" alt=""></div><figcaption>a estampa · Barroco de Minas</figcaption></figure></div>
<p class="sub">Cada estado começou por fotos reais do lugar, com autor e local conferidos. São 312 fotos de 139 fotógrafos.</p>''',
   'Lado a lado: foto real de Ouro Preto (Igreja das Mercês entre os casarões) e a ilustração Barroco de Minas, com janela azul, talha dourada e rosas.')
# 4 díptico
sl(f'''<h2>Dois pés, <em>uma história</em></h2><div class="palm"><img src="{jpg(mg["palmilha"], 1400)}" alt=""></div>
<p class="sub">O pé esquerdo e o direito contam metades da mesma cena. Em Minas: a talha dourada de um lado, a guirlanda de rosas do outro.</p>''',
   'Arte da palmilha de Minas Gerais em díptico: talha dourada barroca no pé esquerdo, guirlanda de rosas e fita azul no direito.')
# 5 decisão
sl(f'''<h2>Minas não é <em>só jabuticaba</em></h2>
<div class="dupla"><figure class="antes"><img src="{jpg("mg-antes-jabuticaba.jpg")}" alt=""><figcaption>antes</figcaption></figure><figure><img src="{jpg("mg-depois-barroco.jpg")}" alt=""><figcaption>depois</figcaption></figure></div>
<p class="sub">O primeiro par tinha jabuticaba e sabiá. Bonito, mas tem jabuticaba em meio Brasil. Ficou o barroco, que só Minas tem.</p>''',
   'Antes e depois da palmilha de Minas: a primeira, com jabuticaba e sabiá, desbotada; a final, com o barroco dourado e as rosas.')
# 6-8 estados
for uf in ['pa', 'ms', 'sc']:
    arco_estado(uf)
# 9-10 ache o coração (Rio: duas folhas de amendoeira, que viraram o símbolo)
holofote('rj', False)
holofote('rj', True)
# 11 os 14 pares
pares = ''.join(f'<div><img src="{par(s["uf"])}" alt=""><b>{e(s["nome"])}</b></div>' for s in data)
sl(f'<h2>Quatorze pares, <em>um em cada estado</em></h2><div class="grade">{pares}</div><p class="sub">Folha, bicho, fruta e objeto de cada lugar, grandes e recortados pela borda da palmilha, como a FARM já faz. A assinatura da collab vai no calcanhar.</p>',
   'Os quatorze pares de chinelos lado a lado, um por estado: ' + ', '.join(s['nome'] for s in data) + '.')
# 12 o par no lugar
ce = POR['ce']
sl(f'''<div class="cheia"><img src="{jpg(ce["campanha"], 1500)}" alt=""></div><div class="leg-cheia"><p class="eb">a campanha</p><h2>O par <em>no lugar</em></h2><p class="sub">Cada par foi fotografado onde a arte acontece. O Ceará, na areia, entre o caju e a renda.</p></div>''',
   'Foto de campanha: o par do Ceará na areia, com cajus e renda de bilro.', 'foto', topo=False)
# 13 fim (único slide com a menção a IA)
sl(f'''<div class="fim-in">{svg(mono("#FFF3E6", "#6A1B29"), 110)}<p class="fim-g">bem-querer</p>
<p class="fim-t">O projeto completo, estado por estado, está no site. <b>Link na bio.</b></p>
<div class="fim-c"><p><b>Ficha</b> Conceito, pesquisa de campo e direção de arte: Emilly Silva. Ilustrações, estampas e fotos dos pares feitas com IA generativa, a partir dessa direção de arte.</p>
<p><b>Fotos de campo</b> 139 fotógrafos, sob licenças Creative Commons, com crédito completo no site.</p>
<p><b>Aviso</b> Projeto conceitual de portfólio. Não é uma coleção oficial e não tem vínculo com a FARM Rio nem com a havaianas.</p></div></div>''',
   'Último slide, em vinho: bem-querer, link na bio, ficha técnica (direção de arte de Emilly Silva; ilustrações, estampas e fotos dos pares feitas com IA generativa), créditos das fotos de campo e aviso de projeto conceitual sem vínculo com as marcas.', 'fim', topo=False)
assert len(slides) == N, len(slides)

CSS = '''
*{box-sizing:border-box}
:root{--creme:#F4EDE3;--creme2:#EBE2D5;--tinta:#2A1A17;--vinho:#6A1B29;--laranja:#E07A2E;--suave:#857568;--serif:"Instrument Serif",Georgia,serif;--sans:"Jost",system-ui,sans-serif}
body{margin:0;background:#999}
img{display:block;max-width:100%}
.sl{position:relative;width:1080px;height:1440px;overflow:hidden;background:var(--creme);color:var(--tinta);font:400 30px/1.45 var(--sans);padding:150px 84px 90px;margin-bottom:20px}
.cab{position:absolute;left:84px;right:84px;top:54px;display:flex;justify-content:space-between;align-items:center;font:500 18px/1 var(--sans);letter-spacing:.18em;color:var(--suave)}
.cab span:first-child{display:flex;align-items:center;gap:10px;font:italic 400 32px/1 var(--serif);letter-spacing:0;color:var(--tinta)}
.eb{font:500 20px/1.3 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--suave);margin:0}
h1,h2{font-family:var(--serif);font-weight:400;margin:0}
h2{font-size:104px;line-height:.92;letter-spacing:-.02em;margin:0 0 44px}
h2 em,h1 em,.manif em{color:var(--vinho)}
.sub{font-size:30px;line-height:1.4;color:#3E2F29;margin:36px 0 0;max-width:30ch}
.arco{border-radius:999px 999px 0 0;overflow:hidden;background:var(--creme2);aspect-ratio:3/4}
.arco img{width:100%;height:100%;object-fit:cover}
.flutua{position:absolute;filter:drop-shadow(0 26px 22px rgba(40,10,10,.3))}
figure{margin:0}
figcaption{font:500 18px/1.35 var(--sans);letter-spacing:.12em;text-transform:uppercase;color:var(--suave);margin-top:14px}
figcaption span{display:block;text-transform:none;letter-spacing:0;font-weight:400;font-size:17px;margin-top:4px}
/* capa */
.capa{padding-top:90px}
.capa h1{font-size:220px;line-height:.84;letter-spacing:-.035em}
.capa h1 span{display:block}
.capa h1 em{display:block;text-align:right}
.capa-eb{margin-top:26px;color:var(--tinta)}
.capa-arte{position:absolute;left:50%;bottom:0;width:600px;transform:translateX(-50%)}
.capa-arte .arco{aspect-ratio:3/4.1}
.capa .flutua{width:300px;left:-160px;bottom:40px;transform:rotate(-10deg)}
/* manifesto */
.centro{display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}
.manif{font:400 84px/1.1 var(--serif);letter-spacing:-.015em;margin:34px 0 60px}
/* duplas */
.dupla{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:end}
.dupla img{width:100%;aspect-ratio:3/4;object-fit:cover}
.dupla .arco img{aspect-ratio:auto}
.antes img{filter:saturate(.35);opacity:.8}
.palm{background:var(--creme2);padding:40px;display:grid;place-items:center}
.palm img{max-height:780px}
/* estado */
.estado .nome{font-size:130px;line-height:.86;margin:18px 0 10px}
.est{font:italic 400 48px/1.1 var(--serif);color:var(--vinho);margin:0}
.estado .arte{position:absolute;left:50%;bottom:150px;width:620px;transform:translateX(-30%)}
.estado .arte .arco{aspect-ratio:3/3.6}
.estado .flutua{width:330px;left:-250px;bottom:-30px;transform:rotate(-10deg)}
.cor-l{position:absolute;left:84px;right:84px;bottom:60px;margin:0;font:italic 400 34px/1.25 var(--serif);color:var(--tinta)}
.cor-l b{font:500 18px/1 var(--sans);letter-spacing:.18em;text-transform:uppercase;color:var(--vinho);font-style:normal;margin-right:8px}
/* busca */
.busca h2{font-size:92px;margin-bottom:24px}
.busca .sub{margin:0 0 40px}
.quadro{position:relative;width:760px;margin:0 auto;aspect-ratio:1744/2336;max-height:900px;border-radius:999px 999px 0 0;overflow:hidden}
.quadro img{width:100%;height:100%;object-fit:cover}
.alvo{position:absolute;border-radius:50%;transform:translate(-50%,-50%)}
.alvo.on{box-shadow:0 0 0 2000px rgba(26,8,10,.68);border:4px solid #FFF3E6}
.revelado{background:var(--vinho);color:#FFF3E6}
.revelado h2,.revelado .sub{color:#FFF3E6}
.revelado .cab span:first-child,.revelado .cab{color:#FFF3E6}
/* grade dos 14 */
.grade{display:grid;grid-template-columns:repeat(5,1fr);gap:22px 18px;margin-top:-10px}
.grade img{width:100%;aspect-ratio:640/710;object-fit:contain}
.grade b{display:block;font:400 23px/1.05 var(--serif);text-align:center;margin-top:4px}
/* foto cheia */
.foto{padding:0}
.cheia{position:absolute;inset:0}
.cheia img{width:100%;height:100%;object-fit:cover}
.leg-cheia{position:absolute;left:0;right:0;bottom:0;padding:360px 84px 84px;background:linear-gradient(rgba(30,12,10,0),rgba(30,12,10,.72) 45%,rgba(30,12,10,.9));color:#FFF3E6}
.leg-cheia .eb{color:rgba(255,243,230,.8)}
.leg-cheia h2{color:#FFF3E6;margin:14px 0 0}
.leg-cheia h2 em{color:#FFD9B0}
.leg-cheia .sub{color:rgba(255,243,230,.9)}
/* fim */
.fim{background:var(--vinho);color:#FFF3E6;display:flex;align-items:center}
.fim-in{width:100%}
.fim-g{font:italic 400 200px/.85 var(--serif);letter-spacing:-.04em;margin:30px 0 40px}
.fim-t{font:400 50px/1.15 var(--serif);margin:0 0 70px;max-width:20ch}
.fim-t b{font-weight:400;color:var(--laranja);font-style:italic}
.fim-c{display:grid;gap:26px;font-size:24px;line-height:1.45;color:rgba(255,243,230,.86)}
.fim-c p{margin:0}
.fim-c b{display:block;font:500 17px/1 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:rgba(255,243,230,.62);margin-bottom:8px}
'''
doc = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Bem-Querer · carrossel</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Jost:wght@400;500&display=block">
<style>{CSS}</style></head><body>{"".join(slides)}</body></html>'''
open(os.path.join(OUT, 'carrossel.html'), 'w', encoding='utf8').write(doc)

legenda = '''A gente saiu do Rio e foi até quatorze estados. Em cada um, um par de chinelos feito com os elementos de lá, e um coração escondido na estampa. Achou o do slide 9?

Bem-Querer é uma V2 conceitual da collab havaianas ♥ FARM Rio. A ideia: a FARM é carioca até no nome, e a cápsula leva o Rio para conhecer o Brasil. Cada estado começou pela rua, com fotos reais do lugar, antes de virar desenho. A regra da coleção é que o coração nunca é desenhado em cima de nada: ele aparece quando os próprios elementos se encontram. Duas folhas de amendoeira caindo juntas no Rio, dois pássaros de miriti no Pará, a cauda da baleia em Santa Catarina.

O projeto inteiro, estado por estado, está no site (link na bio).

Projeto de portfólio, sem vínculo com a FARM Rio ou com a havaianas.

#estamparia #ilustracao #designdesuperficie #projetoconceitual #brasil'''
open(os.path.join(OUT, 'legenda.txt'), 'w', encoding='utf8').write(legenda)
open(os.path.join(OUT, 'alt-text.txt'), 'w', encoding='utf8').write('\n'.join(f'Slide {i + 1:02d}: {a}' for i, a in enumerate(alts)) + '\n')
print('ok', len(slides), 'slides')
