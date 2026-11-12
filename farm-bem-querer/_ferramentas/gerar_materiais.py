"""Página de materiais (site/materiais/): tudo para postar, na ordem, com vídeos que tocam no navegador,
botão de baixar em cada arquivo e botão de copiar nos textos. Não aparece no menu do site (noindex).
Depende de behance_pacote.py, behance_pdf.py, insta_pacote.py e da pasta linkedin/ já gerados.
Uso: python3 -I gerar_materiais.py"""
import glob
import html
import os
import re
import shutil

AQUI = os.path.dirname(os.path.abspath(__file__))
AP = os.path.join(AQUI, '..', '07-apresentacao')
SITE = os.path.join(AP, 'site')
M = os.path.join(SITE, 'materiais')
ARQ = os.path.join(M, 'arquivos')
if os.path.isdir(ARQ):
    shutil.rmtree(ARQ)
for d in ('behance', 'instagram', 'linkedin', 'reel', 'filmes'):
    os.makedirs(os.path.join(ARQ, d))
e = lambda s: html.escape(s or '', quote=True)


def copia(src, sub, nome=None):
    nome = nome or os.path.basename(src)
    shutil.copy(src, os.path.join(ARQ, sub, nome))
    return f'arquivos/{sub}/{nome}'


def tam(caminho):
    return f'{os.path.getsize(os.path.join(M, caminho)) / 1e6:.1f} MB'


def midia(caminho, rot, capa=None):
    if caminho.endswith('.mp4'):
        pst = f' poster="{capa}"' if capa else ''
        corpo = f'<video src="{caminho}"{pst} controls playsinline muted loop preload="metadata"></video>'
    else:
        corpo = f'<img src="{caminho}" alt="{e(rot)}" loading="lazy">'
    return (f'<figure class="item">{corpo}<figcaption><span>{e(rot)}</span>'
            f'<a class="baixar" href="{caminho}" download>baixar · {tam(caminho)}</a></figcaption></figure>')


n_texto = [0]


def texto(titulo, conteudo):
    n_texto[0] += 1
    i = f't{n_texto[0]}'
    return (f'<div class="texto"><div class="texto-cab"><b>{e(titulo)}</b><button type="button" data-copia="{i}">copiar</button></div>'
            f'<pre id="{i}">{e(conteudo.strip())}</pre></div>')


def secoes(txt):
    """Divide um .txt em seções pelos títulos em maiúsculas."""
    out, atual = {}, None
    for linha in txt.splitlines():
        lt = linha.strip()
        base = lt.split('(')[0].strip()
        if base and base == base.upper() and re.search(r'[A-ZÁÉÍÓÚÃÕÇ]{3}', base) and not lt.startswith(('#', '1', '2', '3', '4', '-', '=')):
            atual = lt
            out[atual] = []
        elif atual is not None and not set(lt) <= set('-='):
            out[atual].append(linha)
    return {k: '\n'.join(v).strip() for k, v in out.items()}


# ---------------- Behance ----------------
PK = os.path.join(AP, 'behance', 'pacote')
bt = secoes(open(os.path.join(PK, 'textos-e-ordem.txt'), encoding='utf8').read())
pega = lambda prefixo: next(v for k, v in bt.items() if k.startswith(prefixo))
capa = copia(os.path.join(PK, '1-capa-do-projeto', 'capa-1616x1264.jpg'), 'behance')
def capa_de(f, sub):
    nome = os.path.splitext(os.path.basename(f))[0]
    still = os.path.join(PK, '3-alternativas-paradas', nome + '.jpg')
    return copia(still, sub, nome + '-capa.jpg') if f.endswith('.mp4') and os.path.exists(still) else None


mods = ''.join(midia(copia(f, 'behance'), os.path.splitext(os.path.basename(f))[0].replace('-', ' ', 1).replace('-', ' '), capa_de(f, 'behance'))
               for f in sorted(glob.glob(os.path.join(PK, '2-modulos-em-ordem', '*'))))
pdf_b = copia(os.path.join(AP, 'behance', 'behance-bem-querer.pdf'), 'behance')
behance = f'''
<section id="behance"><p class="eb">01 · Behance</p><h2>O post do <em>Behance</em></h2>
<ol class="passos">
  <li>Entre em <b>behance.net</b> com a sua conta e clique em <b>Criar &gt; Projeto</b>.</li>
  <li>Suba os 17 itens abaixo, <b>na ordem</b>. Nos vídeos, ative a reprodução automática e a repetição se o editor oferecer.</li>
  <li>Na capa, use a imagem da capa (o Behance recorta; ela não tem texto, de propósito).</li>
  <li>Cole título, descrição, tags, campos criativos e ferramentas (botão <b>copiar</b> em cada um).</li>
  <li>Só publique quando estiver tudo pronto: a curadoria do Behance olha cada projeto uma vez.</li>
</ol>
<div class="textos">{texto('Título', pega('TÍTULO'))}{texto('Descrição do projeto', pega('DESCRIÇÃO'))}{texto('Tags', pega('TAGS'))}{texto('Campos criativos', pega('CAMPOS'))}{texto('Ferramentas', pega('FERRAMENTAS'))}</div>
<h3>Capa</h3><div class="grade um">{midia(capa, 'capa do projeto')}</div>
<h3>Módulos, na ordem</h3><div class="grade">{mods}</div>
<p class="extra"><a class="baixar" href="{pdf_b}" download>PDF do post inteiro · {tam(pdf_b)}</a></p>
</section>'''

# ---------------- LinkedIn ----------------
LI = os.path.join(AP, 'linkedin')
lt = open(os.path.join(LI, 'post-linkedin.txt'), encoding='utf8').read()
post = lt.split('TEXTO DO POST')[1].split('PRIMEIRO COMENTÁRIO')[0].strip('\n -')
coment = lt.split('PRIMEIRO COMENTÁRIO')[1].strip('\n -')
vid_li = copia(os.path.join(LI, 'bem-querer-linkedin.mp4'), 'linkedin')
import subprocess  # noqa: E402
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '4', '-i', os.path.join(M, vid_li), '-frames:v', '1', '-q:v', '3',
                os.path.join(ARQ, 'linkedin', 'capa.jpg')], check=True)
pdf_li = copia(os.path.join(LI, 'bem-querer-linkedin.pdf'), 'linkedin')
linkedin = f'''
<section id="linkedin"><p class="eb">02 · LinkedIn</p><h2>O post do <em>LinkedIn</em></h2>
<ol class="passos">
  <li>Em <b>Começar um post</b>, adicione o vídeo e cole o texto.</li>
  <li>Publique e, logo em seguida, coloque o link e as hashtags no <b>primeiro comentário</b>.</li>
  <li>Não marque as páginas da FARM nem da havaianas: é um projeto não oficial.</li>
</ol>
<div class="duas"><div class="grade um">{midia(vid_li, 'vídeo do post · 26 s · 4:5', 'arquivos/linkedin/capa.jpg')}</div>
<div class="textos">{texto('Texto do post', post)}{texto('Primeiro comentário', coment)}</div></div>
<p class="extra">Se preferir carrossel em vez de vídeo: <a class="baixar" href="{pdf_li}" download>PDF do carrossel · {tam(pdf_li)}</a></p>
</section>'''

# ---------------- Instagram ----------------
IG = os.path.join(AP, 'instagram')
def capa_ig(f):
    nn = os.path.basename(f)[:2]
    jpg = os.path.join(IG, 'slides', f'bem-querer-{nn}.jpg')
    return copia(jpg, 'instagram', f'{nn}-capa.jpg') if f.endswith('.mp4') and os.path.exists(jpg) else None


ig_itens = ''.join(midia(copia(f, 'instagram'), f'slide {os.path.basename(f)[:2]}', capa_ig(f))
                   for f in sorted(glob.glob(os.path.join(IG, 'carrossel-final', '[0-9]*'))))
legenda = open(os.path.join(IG, 'legenda.txt'), encoding='utf8').read()
alt = open(os.path.join(IG, 'alt-text.txt'), encoding='utf8').read()
instagram = f'''
<section id="instagram"><p class="eb">03 · Instagram</p><h2>O carrossel do <em>Instagram</em></h2>
<ol class="passos">
  <li>Suba os 13 itens na ordem (os slides 1 e 5 a 8 são vídeos).</li>
  <li>Cole a legenda. O texto alternativo de cada slide fica em Configurações avançadas &gt; Acessibilidade.</li>
</ol>
<div class="textos">{texto('Legenda', legenda)}{texto('Texto alternativo dos slides', alt)}</div>
<div class="grade">{ig_itens}</div>
</section>'''

# ---------------- reel ----------------
RL = os.path.join(IG, 'reel')
vid_rl = copia(os.path.join(RL, 'bem-querer-reel.mp4'), 'reel')
capa_rl = copia(os.path.join(RL, 'capa-reel.jpg'), 'reel')
leg_rl = open(os.path.join(RL, 'legenda-reel.txt'), encoding='utf8').read().split('LEGENDA', 1)[1]
reel = f'''
<section id="reel"><p class="eb">04 · Reel</p><h2>O reel do <em>Bem-Querer</em></h2>
<ol class="passos">
  <li>Suba o vídeo como Reel. Ele já vem com a trilha: um samba instrumental original, com os cortes do vídeo caindo na batida.</li>
  <li>Não coloque música da biblioteca por cima; deixe o áudio original do vídeo.</li>
  <li>Em <b>Editar capa</b>, use a capa abaixo (adicionar da galeria).</li>
  <li>Cole a legenda. Não marque a FARM nem a havaianas: é um projeto não oficial.</li>
</ol>
<div class="duas"><div class="grade um">{midia(vid_rl, 'reel · 41 s · 9:16', capa_rl)}{midia(capa_rl, 'capa do reel')}</div>
<div class="textos">{texto('Legenda do reel', leg_rl)}</div></div>
</section>'''

# ---------------- motions e filmes ----------------
import json  # noqa: E402
data = json.load(open(os.path.join(SITE, 'data.json'), encoding='utf8'))
motions = ''.join(f'<figure class="item"><video src="../video/{s["uf"]}.mp4" poster="../img/{s["uf"]}-ilustracao.jpg" controls playsinline muted loop preload="metadata"></video>'
                  f'<figcaption><span>{e(s["nome"])}</span><a class="baixar" href="../video/{s["uf"]}.mp4" download>baixar</a></figcaption></figure>'
                  for s in data)
VB = os.path.join(AP, 'behance', 'videos')
REND = os.path.join(AP, 'behance', '_render')
filmes = ''.join(midia(copia(os.path.join(VB, f'filme-{n}.mp4'), 'filmes'), r, copia(os.path.join(REND, n, q), 'filmes', f'{n}-capa.jpg'))
                 for n, r, q in [('abertura', 'abertura · só tipografia', '0217.jpg'), ('colecao', 'a coleção em movimento', '0505.jpg')])
motion_sec = f'''
<section id="motions"><p class="eb">05 · motions</p><h2>As 14 ilustrações <em>em movimento</em></h2>
<div class="grade">{motions}</div>
<h3>Os filmes</h3><div class="grade">{filmes}</div>
</section>'''

pdf_ap = '../bem-querer-apresentacao.pdf'
doc = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Materiais · Bem-Querer</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Jost:wght@400;500&display=swap">
<style>
:root{{--creme:#F4EDE3;--creme2:#EBE2D5;--tinta:#2A1A17;--vinho:#6A1B29;--laranja:#E07A2E;--suave:#857568;--serif:"Instrument Serif",Georgia,serif;--sans:"Jost",system-ui,sans-serif}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--creme);color:var(--tinta);font:400 17px/1.55 var(--sans)}}
header{{position:sticky;top:0;z-index:5;background:rgba(244,237,227,.94);backdrop-filter:blur(8px);border-bottom:1px solid rgba(42,26,23,.12)}}
.cab{{max-width:1240px;margin:0 auto;padding:14px 24px;display:flex;gap:24px;align-items:center;justify-content:space-between;flex-wrap:wrap}}
.cab a.marca{{font:italic 400 26px/1 var(--serif);color:var(--tinta);text-decoration:none}}
nav{{display:flex;gap:8px;flex-wrap:wrap}}
nav a{{font:500 12px/1 var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--tinta);text-decoration:none;padding:9px 14px;border:1px solid rgba(42,26,23,.25);border-radius:30px}}
nav a:hover{{background:var(--tinta);color:var(--creme)}}
main{{max-width:1240px;margin:0 auto;padding:0 24px 120px}}
.intro{{padding:70px 0 20px}}
.intro h1{{font:400 clamp(48px,7vw,96px)/.95 var(--serif);letter-spacing:-.02em;margin:0 0 18px}}
.intro h1 em,h2 em{{color:var(--vinho)}}
.intro p{{max-width:62ch;color:#4C3C35;margin:0 0 10px}}
.eb{{font:500 12px/1.3 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--suave);margin:0 0 12px}}
section{{padding-top:80px;border-top:1px solid rgba(42,26,23,.18);margin-top:70px}}
h2{{font:400 clamp(40px,5vw,72px)/1 var(--serif);letter-spacing:-.02em;margin:0 0 26px}}
h3{{font:400 32px/1.1 var(--serif);margin:46px 0 18px}}
.passos{{margin:0 0 30px;padding-left:22px;max-width:70ch}}
.passos li{{margin-bottom:6px}}
.grade{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:22px}}
.grade.um{{grid-template-columns:minmax(0,520px)}}
#reel .grade.um{{grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:start}}
.item{{margin:0;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 14px 34px -24px rgba(40,10,10,.5)}}
.item img,.item video{{display:block;width:100%;background:var(--creme2)}}
.item figcaption{{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:10px 12px;font-size:14px}}
.baixar{{font:500 12px/1 var(--sans);letter-spacing:.08em;text-transform:uppercase;color:#FFF3E6;background:var(--vinho);padding:9px 12px;border-radius:30px;text-decoration:none;white-space:nowrap}}
.baixar:hover{{background:var(--tinta)}}
.textos{{display:grid;gap:14px;margin:0 0 10px}}
.texto{{background:#fff;border-radius:10px;padding:14px 16px;box-shadow:0 14px 34px -26px rgba(40,10,10,.45)}}
.texto-cab{{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}}
.texto-cab b{{font:500 12px/1 var(--sans);letter-spacing:.16em;text-transform:uppercase;color:var(--vinho)}}
.texto button{{font:500 12px/1 var(--sans);letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--tinta);background:transparent;border-radius:30px;padding:8px 14px;cursor:pointer}}
.texto button.ok{{background:var(--tinta);color:var(--creme)}}
pre{{margin:0;white-space:pre-wrap;font:400 15px/1.55 var(--sans);color:#3E2F29;max-height:340px;overflow:auto}}
.duas{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:26px;align-items:start}}
.extra{{margin-top:26px}}
@media (max-width:800px){{.duas{{grid-template-columns:minmax(0,1fr)}}}}
</style></head><body>
<header><div class="cab"><a class="marca" href="../index.html">Bem-Querer · materiais</a>
<nav><a href="#behance">Behance</a><a href="#linkedin">LinkedIn</a><a href="#instagram">Instagram</a><a href="#reel">Reel</a><a href="#motions">Motions</a><a href="{pdf_ap}" download>PDF da apresentação</a></nav></div></header>
<main><div class="intro"><p class="eb">tudo para postar</p><h1>Materiais do <em>Bem-Querer</em></h1>
<p>Tudo o que você precisa para postar, já na ordem. Os vídeos tocam aqui mesmo; cada arquivo tem o botão de baixar, e cada texto, o botão de copiar.</p>
<p>Esta página não aparece no menu do site.</p></div>
{behance}{linkedin}{instagram}{reel}{motion_sec}</main>
<script>
document.querySelectorAll('[data-copia]').forEach(function (b) {{
  b.addEventListener('click', function () {{
    var t = document.getElementById(b.dataset.copia).innerText;
    var feito = function () {{ b.textContent = 'copiado ✓'; b.classList.add('ok'); setTimeout(function () {{ b.textContent = 'copiar'; b.classList.remove('ok'); }}, 1800); }};
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(feito, function () {{ velho(t); feito(); }});
    else {{ velho(t); feito(); }}
  }});
}});
function velho(t) {{ var a = document.createElement('textarea'); a.value = t; document.body.appendChild(a); a.select(); try {{ document.execCommand('copy'); }} catch (e) {{}} a.remove(); }}
// um vídeo de cada vez
document.querySelectorAll('video').forEach(function (v) {{ v.addEventListener('play', function () {{ document.querySelectorAll('video').forEach(function (o) {{ if (o !== v) o.pause(); }}); }}); }});
</script></body></html>'''
open(os.path.join(M, 'index.html'), 'w', encoding='utf8').write(doc)
total = sum(os.path.getsize(f) for f in glob.glob(os.path.join(ARQ, '**', '*'), recursive=True) if os.path.isfile(f))
print('ok: materiais/index.html,', round(total / 1e6, 1), 'MB de arquivos')
