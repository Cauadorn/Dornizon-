"""Apresentação compacta em PDF (16:9, 16 páginas) na identidade do site Bem-Querer.
Uso: cd /tmp && python3 -I /home/user/Dornizon-/farm-bem-querer/_ferramentas/gerar_pdf.py
     node /home/user/Dornizon-/farm-bem-querer/_ferramentas/pdf_render.js
Grava 07-apresentacao/pdf/apresentacao.html (fonte) e, com o node, bem-querer-apresentacao.pdf + prévias PNG."""
import html
import json
import os
import re

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(AQUI, 'gerar_site.py'), encoding='utf8').read().split('def e(s)')[0]
exec(compile(_src, 'gerar_site_dados', 'exec'))   # data, V, T, COR, LEGENDA, REGIAO, P, SITE
OUT = os.path.join(P, '07-apresentacao', 'pdf')
IMG = os.path.join(OUT, '_img')
os.makedirs(IMG, exist_ok=True)
POR = {s['uf']: s for s in data}
CREME = (244, 237, 227)


def e(s):
    return html.escape(s or '', quote=True)


def autor(a):
    return (a or '').split(' - ')[0].split(' from ')[0].strip()


def jpg(nome, lado=1300, q=80):
    """Cópia reduzida para o PDF não passar de ~10 MB."""
    dst = os.path.join(IMG, os.path.splitext(nome)[0] + '.jpg')
    if not os.path.exists(dst):
        im = Image.open(os.path.join(SITE, 'img', nome)).convert('RGB')
        im.thumbnail((lado, lado), Image.LANCZOS)
        im.save(dst, quality=q, optimize=True, progressive=True)
    return '_img/' + os.path.basename(dst)


def par(uf, alfa=False, lado=560):
    """Par recortado: PNG com transparência (quando passa por cima da arte) ou JPG sobre o creme."""
    im = Image.open(os.path.join(SITE, 'img', f'{uf}-par.webp')).convert('RGBA')
    im.thumbnail((lado, lado), Image.LANCZOS)
    if alfa:
        dst = os.path.join(IMG, f'{uf}-par.png')
        im.save(dst, optimize=True)
    else:
        fundo = Image.new('RGB', im.size, CREME)
        fundo.paste(im, mask=im.split()[3])
        dst = os.path.join(IMG, f'{uf}-par.jpg')
        fundo.save(dst, quality=84, optimize=True)
    return '_img/' + os.path.basename(dst)


_s = open(P + '/03-marca/identidade-bem-querer/simbolo-cor.svg', encoding='utf8').read()
SIMB = _s[_s.index('>') + 1:_s.rindex('</svg>')]
_s = open(P + '/03-marca/identidade-bem-querer/simbolo-tinta.svg', encoding='utf8').read()
SIMB_T = _s[_s.index('>') + 1:_s.rindex('</svg>')]
svg = lambda c=SIMB, w=40: f'<svg viewBox="-6 6 212 196" width="{w}" aria-hidden="true">{c}</svg>'
mono = lambda cor, veia: SIMB_T.replace('#1D1915', cor).replace('#FCFAF6', veia)
ASSIN = open(os.path.join(SITE, 'img', 'assinatura-collab.svg'), encoding='utf8').read()
ASSIN = ASSIN[ASSIN.index('<svg'):]

TOTAL = 16


def pg(n, corpo, classe='', rodape=True):
    rod = (f'<div class="rod"><span>{svg(w=22)}bem-querer</span><span>havaianas ♥ FARM Rio · cápsula V2</span><span>{n:02d} / {TOTAL}</span></div>'
           if rodape else '')
    return f'<section class="pg {classe}">{corpo}{rod}</section>'


def credito(f):
    return f'foto: {e(autor(f["autor"]))} · {e(f["licenca"])}'


paginas = []

# 1 capa
rj = POR['rj']
paginas.append(pg(1, f'''
<div class="capa-arco"><img src="{jpg(rj["ilu"], 1100)}" alt=""></div>
<p class="capa-p capa-bem">Bem-</p><p class="capa-p capa-querer">Querer</p>
<div class="capa-topo">{svg(w=34)}<span>bem-querer</span></div>
<p class="eb capa-e">havaianas ♥ FARM Rio · cápsula V2</p>
<p class="eb capa-d">projeto de portfólio · Emilly Silva</p>''', 'capa', rodape=False))

# 2 manifesto
paginas.append(pg(2, f'''
<p class="eb">a ideia</p>
<p class="manif">A gente saiu do Rio <span class="pil"><img src="{jpg(rj["campo"][0]["img"], 500)}" alt=""></span> e foi até quatorze estados. Em cada um, um par de chinelos <span class="pil"><img src="{par("ms", lado=300)}" alt="" style="object-fit:contain"></span> feito com os elementos de lá, e um coração <span class="pil redonda"><img src="{jpg(POR["sc"]["coracao"], 400)}" alt=""></span> que só aparece <em>na segunda olhada</em>.</p>''', 'centro'))

# 3 a collab
paginas.append(pg(3, f'''
<div class="duas">
  <div><p class="eb">o projeto</p><h2>Uma participação dentro da <em>collab</em></h2>
    <p class="txt">A collab havaianas ♥ FARM Rio já existe e já deu certo. A V2 não cria outra marca nem outro logo: entra como uma participação, com a mesma assinatura no calcanhar, e muda só o mapa. Em vez de olhar para o Rio, olha para o Brasil.</p>
    <div class="v12"><div><b>V1</b><p>o coração une as duas marcas no logo</p></div><div><b>V2</b><p>o coração sai do logo e se esconde no desenho, formado pelos elementos de cada estado</p></div></div></div>
  <div class="painel">{ASSIN}</div>
</div>'''))

# 4 pesquisa
fotos = ''.join(f'<figure><img src="{jpg(s["campo"][0]["img"], 600)}" alt=""><figcaption>{e(s["nome"])}<span>{credito(s["campo"][0])}</span></figcaption></figure>'
                for s in data[:7])
paginas.append(pg(4, f'''
<p class="eb">a pesquisa</p><h2>Antes do desenho, <em>a rua</em></h2>
<div class="nums"><div><b>14</b><span>estados, das cinco regiões</span></div><div><b>312</b><span>fotos reais de campo</span></div><div><b>139</b><span>fotógrafos creditados</span></div><div><b>1</b><span>âncora por estado</span></div></div>
<div class="tira-fotos">{fotos}</div>'''))

# 5 método
passos = [('Campo', 'Fotos reais do lugar, com autor, licença e local conferidos.', 'mg-campo-1.jpg'),
          ('Âncora', 'Um elemento que é daquele estado e de nenhum outro.', 'mg-coracao.jpg'),
          ('Chinelo', 'Díptico: cada pé conta metade da mesma história.', 'mg-palmilha.jpg'),
          ('Ilustração', 'O lugar inteiro, feito com os mesmos elementos.', 'mg-ilustracao.jpg'),
          ('O par', 'A tira repete uma cor; a assinatura vai no calcanhar.', 'mg-estudio.jpg')]
cols = ''.join(f'<div><div class="arco"><img src="{jpg(img, 600)}" alt=""></div><span>{k + 1:02d}</span><h3>{t}</h3><p>{d}</p></div>' for k, (t, d, img) in enumerate(passos))
paginas.append(pg(5, f'<p class="eb">o método · Minas Gerais como exemplo</p><h2>Como cada par <em>nasce</em></h2><div class="cinco">{cols}</div>'))

# 6 os 14 pares
pares = ''.join(f'<div><img src="{par(s["uf"], lado=420)}" alt=""><b>{e(s["nome"])}</b><span>{e(V[s["uf"]]["nome"])}</span></div>' for s in data)
paginas.append(pg(6, f'<p class="eb">a coleção</p><h2>Quatorze pares, <em>um em cada estado</em></h2><div class="sete pares">{pares}</div>'))

# 7 as 14 ilustrações
ilus = ''.join(f'<div><div class="arco"><img src="{jpg(s["ilu"], 520)}" alt=""></div><b>{e(s["nome"])}</b></div>' for s in data)
paginas.append(pg(7, f'<p class="eb">as ilustrações</p><h2>O lugar inteiro, <em>com os mesmos elementos</em></h2><div class="sete ilus">{ilus}</div>', 'p-ilus'))

# 8–11 estados em destaque
for n, uf in zip(range(8, 12), ['mg', 'pa', 'ms', 'sc']):
    s, t = POR[uf], V[uf]
    f0 = s['campo'][0]
    paginas.append(pg(n, f'''
<div class="estado">
  <div class="e-txt"><p class="eb">{data.index(s) + 1:02d} / 14 · {REGIAO[uf]}</p><h2 class="e-nome">{e(s["nome"])}</h2><p class="e-est">{e(t["nome"])}</p>
    <p class="txt">{e(t["conceito"])}</p>
    <div class="e-cor"><img src="{jpg(s["coracao"], 300)}" alt=""><p><b>onde está o coração</b>{e(s["coracao_texto"])}</p></div></div>
  <div class="e-arte"><div class="arco grande"><img src="{jpg(s["ilu"], 1100)}" alt=""></div><img class="flutua" src="{par(uf, alfa=True, lado=520)}" alt=""></div>
  <div class="e-fotos"><figure><img src="{jpg(s["campanha"], 800)}" alt=""><figcaption>o par no lugar · campanha</figcaption></figure>
    <figure><img src="{jpg(f0["img"], 600)}" alt=""><figcaption>{e(LEGENDA[uf][0])}<span>{credito(f0)}</span></figcaption></figure></div>
</div>''', 'pg-estado'))

# 12 onde o coração mora
cors = ''.join(f'<div><img src="{jpg(s["coracao"], 300)}" alt=""><b>{e(s["nome"])}</b><span>{e(s["coracao_texto"])}</span></div>' for s in data)
paginas.append(pg(12, f'<p class="eb">o fio da coleção</p><h2>Onde o coração <em>mora</em></h2><div class="sete cors">{cors}</div>'))

# 13 decisões
paginas.append(pg(13, f'''
<p class="eb">o que ficou pelo caminho</p><h2>Decisões que <em>mudaram o desenho</em></h2>
<div class="decisoes">
  <div><div class="ad"><figure class="antes"><img src="{jpg("mg-antes-jabuticaba.jpg", 600)}" alt=""><figcaption>antes</figcaption></figure><figure><img src="{jpg("mg-depois-barroco.jpg", 600)}" alt=""><figcaption>depois</figcaption></figure></div>
    <h3>Minas não é só jabuticaba</h3><p>Jabuticaba tem em meio Brasil. Ficou o barroco: a talha do Aleijadinho e as rosas do Mestre Ataíde.</p></div>
  <div><div class="ad"><figure class="antes"><img src="{jpg("sc-antes-ponte.jpg", 600)}" alt=""><figcaption>antes</figcaption></figure><figure><img src="{jpg("sc-depois-enseada.jpg", 600)}" alt=""><figcaption>depois</figcaption></figure></div>
    <h3>A baleia não passa debaixo da ponte</h3><p>A baleia-franca chega perto da areia nas enseadas do sul, não no centro de Florianópolis. Foi para Garopaba.</p></div>
</div>'''))

# 14 campanha
camp = ''.join(f'<figure><img src="{jpg(POR[u]["campanha"], 900)}" alt=""><figcaption>{e(POR[u]["nome"])}</figcaption></figure>' for u in ['ce', 'ba', 'pa', 'rs', 'am', 'mg'])
paginas.append(pg(14, f'<p class="eb">a campanha</p><h2>O par <em>no lugar</em></h2><div class="seis">{camp}</div>'))

# 15 identidade
pal = ''.join('<div class="faixas">' + ''.join(f'<span style="background:{c}"></span>' for c in COR[s['uf']]) + '</div>' for s in data)
paginas.append(pg(15, f'''
<div class="duas">
  <div class="marca-g">{svg(w=150)}<p class="wm">bem-querer</p><p class="eb">o emblema da cápsula · duas folhas de amendoeira que caem juntas</p></div>
  <div><p class="eb">identidade</p><h2>A assinatura é a da collab; <em>o emblema é da cápsula</em></h2>
    <div class="fontes"><div><b class="serif">Aa</b><span>Instrument Serif · títulos</span></div><div><b class="sans">Aa</b><span>Jost · texto</span></div></div>
    <div class="base"><span style="background:#F4EDE3;box-shadow:inset 0 0 0 1px rgba(42,26,23,.2)"></span><span style="background:#6A1B29"></span><span style="background:#E07A2E"></span><p>creme, vinho e laranja, e uma paleta por estado, tirada da própria estampa</p></div>
    <div class="pals">{pal}</div></div>
</div>'''))

# 16 fim
paginas.append(pg(16, f'''
<p class="fim-g">bem-querer</p>
<div class="fim-c">
  <div><p class="eb">o site</p><p class="link">cauadorn.github.io/Dornizon-</p><p>Os quatorze estados por inteiro: o caderno de campo, o coração escondido e o par no lugar.</p></div>
  <div><p class="eb">ficha técnica</p><p>Conceito, pesquisa de campo, direção de arte, estampas, ilustrações e chinelos: Emilly Silva. Assinatura: a da collab havaianas ♥ FARM Rio, sem alteração. Fotos de campo: 139 fotógrafos sob licenças Creative Commons, com crédito completo no site.</p></div>
  <div><p class="eb">aviso</p><p>Bem-Querer é um projeto fictício de portfólio. Não é uma coleção oficial e não tem vínculo com a FARM Rio nem com a havaianas; as marcas aparecem só para contar a ideia.</p></div>
</div>''', 'fim', rodape=False))

CSS = '''
@page{size:1920px 1080px;margin:0}
*{box-sizing:border-box}
:root{--creme:#F4EDE3;--creme2:#EBE2D5;--tinta:#2A1A17;--vinho:#6A1B29;--laranja:#E07A2E;--suave:#857568;--serif:"Instrument Serif",Georgia,serif;--sans:"Jost",system-ui,sans-serif}
html,body{margin:0;background:var(--creme);color:var(--tinta);font:400 24px/1.5 var(--sans);-webkit-print-color-adjust:exact;print-color-adjust:exact}
img{display:block;max-width:100%}
.pg{position:relative;width:1920px;height:1080px;overflow:hidden;padding:96px 110px 120px;break-after:page;page-break-after:always;background:var(--creme)}
.eb{font:500 16px/1.3 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--suave);margin:0}
h2{font:400 96px/.95 var(--serif);letter-spacing:-.02em;margin:16px 0 44px;max-width:20ch}
h2 em,.manif em{color:var(--vinho)}
h3{font:400 40px/1.05 var(--serif);margin:14px 0 8px}
.txt{max-width:40ch;color:#3E2F29;margin:0 0 30px}
.rod{position:absolute;left:110px;right:110px;bottom:44px;display:flex;justify-content:space-between;align-items:center;font:500 14px/1 var(--sans);letter-spacing:.18em;text-transform:uppercase;color:var(--suave)}
.rod span:first-child{display:flex;align-items:center;gap:10px;font:italic 400 24px/1 var(--serif);letter-spacing:0;text-transform:none;color:var(--tinta)}
.arco{border-radius:999px 999px 0 0;overflow:hidden;background:var(--creme2);aspect-ratio:3/4}
.arco img{width:100%;height:100%;object-fit:cover}
/* capa */
.capa-arco{position:absolute;left:50%;bottom:0;width:560px;height:820px;transform:translateX(-50%);border-radius:999px 999px 0 0;overflow:hidden}
.capa-arco img{width:100%;height:100%;object-fit:cover;object-position:50% 30%}
.capa-p{position:absolute;top:560px;margin:0;font:400 230px/.8 var(--serif);letter-spacing:-.035em}
.capa-bem{right:calc(50% + 310px)}
.capa-querer{left:calc(50% + 310px);font-style:italic}
.capa-topo{position:absolute;left:110px;top:70px;display:flex;align-items:center;gap:12px;font:italic 400 34px/1 var(--serif)}
.capa-e{position:absolute;left:110px;bottom:56px;color:var(--tinta)}
.capa-d{position:absolute;right:110px;bottom:56px;color:var(--tinta)}
/* manifesto */
.centro{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.manif{font:400 88px/1.1 var(--serif);letter-spacing:-.015em;max-width:22ch;margin:34px 0 0}
.pil{display:inline-block;width:1.7em;height:.82em;border-radius:99px;overflow:hidden;vertical-align:-.06em;background:var(--creme2)}
.pil img{width:100%;height:100%;object-fit:cover}
.pil.redonda{width:.82em}
/* collab */
.duas{display:grid;grid-template-columns:1fr 1fr;gap:110px;align-items:center;height:100%}
.painel{background:var(--creme2);height:100%;display:grid;place-items:center;padding:120px}
.painel svg{width:100%;max-width:440px;height:auto}
.v12{display:grid;grid-template-columns:1fr 1fr;gap:30px;border-top:1px solid rgba(42,26,23,.18);padding-top:28px}
.v12 b{font:400 56px/1 var(--serif);color:var(--vinho)}
.v12 p{margin:8px 0 0;font-size:21px;color:#3E2F29}
/* pesquisa */
.nums{display:grid;grid-template-columns:repeat(4,1fr);gap:40px;margin:-10px 0 50px}
.nums b{display:block;font:400 130px/.85 var(--serif);color:var(--vinho);letter-spacing:-.03em}
.nums span{display:block;margin-top:10px;font-size:20px;color:#3E2F29}
.tira-fotos{display:grid;grid-template-columns:repeat(7,1fr);gap:18px}
.tira-fotos img{width:100%;aspect-ratio:4/5;object-fit:cover}
figcaption{font-size:15px;line-height:1.35;margin-top:8px;color:#3E2F29}
figcaption span{display:block;font-size:12px;color:var(--suave)}
/* método */
.cinco{display:grid;grid-template-columns:repeat(5,1fr);gap:34px}
.cinco > div > span{display:block;margin-top:18px;font:500 14px/1 var(--sans);letter-spacing:.18em;color:var(--suave)}
.cinco h3{font-size:44px;margin-top:6px}
.cinco p{margin:0;font-size:19px;color:#3E2F29}
.cinco .arco{aspect-ratio:3/4;width:100%;max-height:430px}
/* grades de 7 */
.sete{display:grid;grid-template-columns:repeat(7,1fr);gap:22px 26px}
.sete b{display:block;font:400 26px/1.05 var(--serif);margin-top:10px}
.sete span{display:block;font:italic 400 17px/1.25 var(--serif);color:var(--suave)}
.pares img{width:100%;aspect-ratio:640/710;object-fit:contain}
.ilus{gap:22px 30px}
.ilus .arco{width:100%;aspect-ratio:3/3.55}
.ilus b{font-size:23px}
.p-ilus h2{margin-bottom:30px}
.cors{text-align:center}
.cors img{width:100%;aspect-ratio:1;border-radius:50%;object-fit:cover}
.cors span{font-size:15px;margin-top:4px}
/* estado */
.estado{display:grid;grid-template-columns:.9fr 1.05fr .75fr;gap:70px;align-items:center;height:100%}
.e-nome{font-size:120px;line-height:.86;margin:18px 0 10px}
.e-est{font:italic 400 40px/1.1 var(--serif);color:var(--vinho);margin:0 0 26px}
.e-cor{display:flex;gap:18px;align-items:center;border-top:1px solid rgba(42,26,23,.18);padding-top:22px}
.e-cor img{width:96px;height:96px;border-radius:50%;object-fit:cover;flex:none}
.e-cor p{margin:0;font-size:19px;color:#3E2F29}
.e-cor b{display:block;font:italic 400 26px/1.1 var(--serif);color:var(--vinho);font-weight:400}
.e-arte{position:relative;display:flex;justify-content:center;align-self:center}
.pg-estado .rod span:nth-child(2){visibility:hidden}
.arco.grande{width:100%;max-width:540px;aspect-ratio:3/4}
.flutua{position:absolute;width:44%;left:-14%;bottom:15%;transform:rotate(-9deg);filter:drop-shadow(0 26px 24px rgba(40,10,10,.28))}
.e-fotos{display:grid;gap:22px}
.e-fotos img{width:100%;aspect-ratio:4/3;object-fit:cover}
.e-fotos figure:first-child img{aspect-ratio:1/1}
figure{margin:0}
/* decisões, campanha */
.decisoes{display:grid;grid-template-columns:1fr 1fr;gap:90px}
.ad{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.ad img{width:100%;aspect-ratio:4/5;object-fit:cover;max-height:440px}
.ad .antes img{filter:saturate(.35);opacity:.8}
.ad figcaption{font:500 13px/1 var(--sans);letter-spacing:.18em;text-transform:uppercase;color:var(--suave)}
.decisoes p{margin:0;font-size:20px;color:#3E2F29;max-width:42ch}
.seis{display:grid;grid-template-columns:repeat(6,1fr);gap:18px}
.seis img{width:100%;aspect-ratio:3/4;object-fit:cover}
/* identidade */
.marca-g{background:var(--creme2);height:100%;display:grid;place-items:center;align-content:center;gap:24px;text-align:center}
.marca-g .wm{font:italic 400 130px/.85 var(--serif);letter-spacing:-.03em;margin:0}
.fontes{display:flex;gap:60px;margin-bottom:34px}
.fontes b{display:block;font-weight:400;font-size:120px;line-height:.9}
.fontes .serif{font-family:var(--serif)}
.fontes .sans{font-family:var(--sans);font-weight:500}
.fontes span{font:500 14px/1.3 var(--sans);letter-spacing:.16em;text-transform:uppercase;color:var(--suave)}
.base{display:flex;gap:14px;align-items:center;margin-bottom:26px}
.base span{width:70px;height:70px;border-radius:50%}
.base p{margin:0 0 0 12px;font-size:19px;color:#3E2F29;max-width:30ch}
.pals{display:grid;grid-template-columns:repeat(7,1fr);gap:12px}
.faixas{display:flex;height:46px;border-radius:999px 999px 0 0;overflow:hidden}
.faixas span{flex:1}
/* fim */
.fim{background:var(--vinho);color:#FFF3E6}
.fim .eb{color:rgba(255,243,230,.7);margin-bottom:12px}
.fim-g{font:italic 400 330px/.8 var(--serif);letter-spacing:-.04em;margin:40px 0 90px;color:#FFF3E6}
.fim-c{display:grid;grid-template-columns:repeat(3,1fr);gap:70px;font-size:20px;color:rgba(255,243,230,.88)}
.fim-c p{margin:0}
.fim .link{font:italic 400 40px/1.1 var(--serif);color:var(--laranja);margin-bottom:14px}
'''

doc = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Bem-Querer · apresentação</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Jost:wght@400;500&display=block">
<style>{CSS}</style></head><body>{"".join(paginas)}</body></html>'''
open(os.path.join(OUT, 'apresentacao.html'), 'w', encoding='utf8').write(doc)
print('ok', len(paginas), 'páginas')
