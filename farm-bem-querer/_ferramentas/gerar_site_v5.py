"""Bem-Querer · site completo (v5): várias páginas com o mesmo topo, menu, transição e rodapé.
Uso: cd /tmp && python3 -I /home/user/Dornizon-/farm-bem-querer/_ferramentas/gerar_site_v5.py
Grava em 07-apresentacao/site/: index, projeto, pesquisa, colecao, processo, campanha, identidade, creditos e estados/*.html"""
import colorsys
import glob
import html
import json
import os
import re
import shutil
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(AQUI, 'gerar_site.py'), encoding='utf8').read().split('def e(s)')[0]
exec(compile(_src, 'gerar_site_dados', 'exec'))   # data, V, T, COR, LEGENDA, REGIAO, EVITAR_EXTRA, P, SITE


def e(s):
    return html.escape(s or '', quote=True)


def autor(a):
    return (a or '').split(' - ')[0].split(' from ')[0].strip()


def md(s):
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', e(s))
    return re.sub(r'(?<![\w])_(.+?)_(?![\w])', r'<em>\1</em>', t)


def lum(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def acento(uf):
    """A cor mais viva da paleta do estado que ainda lê sobre o creme (contraste >= 3:1)."""
    cands = []
    for h in COR[uf]:
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
        if (0.86 + 0.05) / (lum(h) + 0.05) >= 3:
            cands.append((colorsys.rgb_to_hls(r, g, b)[2], h))
    if cands:
        return max(cands)[1]
    r, g, b = (int(COR[uf][0][i:i + 2], 16) / 255 for i in (1, 3, 5))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(hh, 0.32, min(1, ss + .1))
    return '#%02X%02X%02X' % (int(r * 255), int(g * 255), int(b * 255))


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFKD', s.lower()).encode('ascii', 'ignore').decode()).strip('-')


for s in data:
    s['url'] = 'estados/' + slug(s['nome']) + '.html'
    s['est'] = V[s['uf']]['nome']
POR = {s['uf']: s for s in data}

_s = open(P + '/03-marca/identidade-bem-querer/simbolo-cor.svg', encoding='utf8').read()
SIMB = _s[_s.index('>') + 1:_s.rindex('</svg>')]
_s = open(P + '/03-marca/identidade-bem-querer/simbolo-tinta.svg', encoding='utf8').read()
SIMB_T = _s[_s.index('>') + 1:_s.rindex('</svg>')]
svg_simb = lambda conteudo=SIMB, extra='': f'<svg viewBox="-6 6 212 196" aria-hidden="true"{extra}>{conteudo}</svg>'


def simb_mono(cor, veia):
    """Símbolo numa cor só (troca as cores do arquivo tinta)."""
    return SIMB_T.replace('#1D1915', cor).replace('#FCFAF6', veia)


PAGINAS = [('index', 'Início', 'A abertura, o manifesto e a roda dos pares.'),
           ('projeto', 'Projeto', 'Por que uma V2 da collab, e por que o coração.'),
           ('pesquisa', 'Pesquisa', 'Antes do desenho, a rua: fotos reais dos quatorze estados.'),
           ('colecao', 'Coleção', 'Os quatorze pares, por região, e onde mora cada coração.'),
           ('processo', 'Processo', 'Como cada par nasce e as decisões que mudaram o desenho.'),
           ('campanha', 'Campanha', 'Cada par fotografado no lugar da sua arte.'),
           ('identidade', 'Identidade', 'A assinatura da collab, o emblema da cápsula, fontes e cores.'),
           ('creditos', 'Créditos', 'Ficha técnica, fotos de campo e aviso.')]
NO_TOPO = ['projeto', 'pesquisa', 'colecao', 'processo', 'campanha', 'identidade']
FONTES = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Jost:wght@400;500&display=swap">'


def casca(pid, titulo, descricao, corpo, r='', estilo_body='', carregador=False):
    nome = dict((p, n) for p, n, _ in PAGINAS)
    links = ''.join(f'<a href="{r}{p}.html"{" aria-current=page" if p == pid else ""}>{nome[p]}</a>' for p in NO_TOPO)
    m_pag = ''.join(f'<li><a href="{r}{p}.html">{n}</a></li>' for p, n, _ in PAGINAS)
    m_est = ''.join(f'<li><a href="{r}{s["url"]}"><span>{i + 1:02d}</span>{e(s["nome"])}</a></li>' for i, s in enumerate(data))
    f_pag = ''.join(f'<li><a href="{r}{p}.html">{n}</a></li>' for p, n, _ in PAGINAS) + f'<li><a href="{r}bem-querer-apresentacao.pdf" target="_blank" rel="noopener">Apresentação em PDF ↓</a></li>'
    f_est1 = ''.join(f'<li><a href="{r}{s["url"]}">{e(s["nome"])}</a></li>' for s in data[:7])
    f_est2 = ''.join(f'<li><a href="{r}{s["url"]}">{e(s["nome"])}</a></li>' for s in data[7:])
    carrega = (f'<div class="carrega" aria-hidden="true"><div class="cl">{svg_simb(extra=" class=vazio")}{svg_simb(extra=" class=cheio")}</div><span class="pct">0</span></div>'
               if carregador else '')
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titulo}</title>
<meta name="description" content="{e(descricao)}">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{e(descricao)}">
<script>try{{if(sessionStorage.getItem('bq-cortina')==='1'){{document.documentElement.classList.add('chegando');sessionStorage.removeItem('bq-cortina')}}}}catch(e){{}}</script>
{FONTES}
<link rel="stylesheet" href="{r}css/bq.css">
</head>
<body{estilo_body}>
<a class="pular" href="#conteudo">pular para o conteúdo</a>
<div class="cortina" aria-hidden="true"></div>
{carrega}
<header class="topo">
  <a class="marca" href="{r}index.html" aria-label="Bem-Querer, início">{svg_simb()}bem-querer</a>
  <nav class="links" aria-label="Páginas">{links}</nav>
  <button class="pilula" type="button" aria-expanded="false" aria-controls="menu"><i></i>menu</button>
</header>
<nav class="menu" id="menu" aria-label="Menu">
  <div><p class="eb">o site</p><ol class="m-pag">{m_pag}</ol></div>
  <div><p class="eb">os quatorze estados</p><ol class="m-est">{m_est}</ol></div>
</nav>
<main id="conteudo">
{corpo}
</main>
<footer class="fim">
  <p class="fim-grande">bem-querer</p>
  <div class="fim-cols">
    <div><p class="eb" style="margin-bottom:12px">o site</p><ul>{f_pag}</ul></div>
    <div><p class="eb" style="margin-bottom:12px">os estados</p><ul>{f_est1}</ul></div>
    <div><p class="eb" style="margin-bottom:12px">&nbsp;</p><ul>{f_est2}</ul></div>
    <div><p class="eb" style="margin-bottom:12px">aviso</p><p>Bem-Querer é um projeto fictício de portfólio de Emilly Silva. Não é uma coleção oficial e não tem vínculo com a FARM Rio nem com a havaianas; as marcas aparecem só para contar a ideia.</p></div>
  </div>
</footer>
<img class="foto-mouse" alt="" aria-hidden="true">
<script src="{r}js/gsap.min.js" defer></script>
<script src="{r}js/ScrollTrigger.min.js" defer></script>
<script src="{r}js/lenis.min.js" defer></script>
<script src="{r}js/bq.js" defer></script>
</body>
</html>
'''


def proxima(pid, r=''):
    ordem = [p for p, _, _ in PAGINAS]
    i = ordem.index(pid)
    p, n, d = PAGINAS[(i + 1) % len(PAGINAS)]
    img = {'projeto': POR['rj']['ilu'], 'pesquisa': POR['pa']['campo'][0]['img'], 'colecao': POR['ms']['ilu'], 'processo': POR['mg']['ilu'],
           'campanha': POR['ce']['campanha'], 'identidade': POR['sc']['ilu'], 'creditos': POR['rs']['ilu'], 'index': POR['go']['ilu']}[p]
    return (f'<a class="prox" href="{r}{p}.html"><span><span class="eb">próxima página</span><strong>{n}</strong><em>{d}</em></span>'
            f'<span class="mini"><img src="{r}img/{e(img)}" alt="" loading="lazy"></span></a>')


def pg_hero(eb, titulo, intro):
    return f'<section class="pg-hero"><p class="eb">{eb}</p><h1>{titulo}</h1><p class="intro">{intro}</p></section>'


def figura_campo(s, k, f, link=False, r=''):
    leg = LEGENDA[s['uf']][k]
    cap = f'{e(leg)}<span>foto: {e(autor(f["autor"]))} · {e(f["licenca"])}</span>'
    if link:
        cap = f'<b style="font-weight:500">{e(s["nome"])}</b> · {cap}'
    corpo = f'<div class="moldura"><img src="{r}img/{e(f["img"])}" alt="{e(leg)}" loading="lazy"></div><figcaption>{cap}</figcaption>'
    return f'<figure><a href="{r}{s["url"]}">{corpo}</a></figure>' if link else f'<figure>{corpo}</figure>'


def escrever(nome, conteudo):
    caminho = os.path.join(SITE, nome)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    open(caminho, 'w', encoding='utf8').write(conteudo)
    assert '{{' not in conteudo


# ---------------- início ----------------
def tem_video(uf):
    return os.path.exists(os.path.join(SITE, 'video', f'{uf}.mp4'))


def midia(s, r='', classe='', auto=False, extra=''):
    """A ilustração em movimento quando o vídeo existe (site/video/<uf>.mp4); senão, a imagem parada."""
    if tem_video(s['uf']):
        tocar = ' data-auto loop' if auto else ''
        return f'<video src="{r}video/{s["uf"]}.mp4" poster="{r}img/{e(s["ilu"])}" muted playsinline preload="metadata"{tocar}{classe}{extra}></video>'
    return f'<img src="{r}img/{e(s["ilu"])}" alt="Ilustração de {e(s["nome"])}" loading="lazy"{classe}{extra}>'


ordem_janela = data[data.index(POR['ms']):] + data[:data.index(POR['ms'])]   # abre com a onça
janela = ''.join(midia(s, classe=' class="on"' if k == 0 else '', extra=f' data-n="{data.index(s) + 1:02d}" data-nome="{e(s["nome"])}" data-est="{e(s["est"])}"')
                 .replace('loading="lazy"', 'loading="eager"') for k, s in enumerate(ordem_janela))
trilho = ''.join(f'<a href="{s["url"]}"><div class="arco">{midia(s, auto=True)}</div><strong>{e(s["nome"])}</strong><em>{e(s["est"])}</em></a>' for s in data)
_vistas = []
for _s in data:
    for _w in T[_s['uf']]['palavras'][:3]:
        if _w.lower().strip('!?') not in [v.lower().strip('!?') for v in _vistas] and len([v for v in _vistas if v in T[_s['uf']]['palavras']]) < 2:
            _vistas.append(_w)
todas_palavras = ' <i>♥</i> '.join(e(w) for w in _vistas)
roda = ''.join(f'<a class="item" href="{s["url"]}" style="--i:{i}" data-n="{i + 1:02d}" data-nome="{e(s["nome"])}" data-est="{e(s["est"])}">'
               f'<img src="img/{s["uf"]}-par.webp" alt="Par de {e(s["nome"])}" loading="lazy"></a>' for i, s in enumerate(data))
IMG_PAG = {'projeto': POR['rj']['ilu'], 'pesquisa': POR['mg']['campo'][0]['img'], 'colecao': POR['ms']['estudio'], 'processo': POR['mg']['palmilha'],
           'campanha': POR['ce']['campanha'], 'identidade': POR['pa']['coracao'], 'creditos': POR['ba']['campo'][0]['img']}
indice = ''.join(f'<li data-img="img/{e(IMG_PAG[p])}"><a href="{p}.html"><span>{k:02d}</span><h3>{n}</h3><p>{d}</p></a></li>'
                 for k, (p, n, d) in enumerate(PAGINAS[1:], 1))
corpo = f'''
<section class="hero" id="topo">
  <div class="janela" aria-hidden="true">{janela}</div>
  <h1 class="palavra p-bem">Bem-</h1>
  <p class="palavra p-querer" aria-hidden="true">Querer</p>
  <div class="rodape-h"><p class="eb">havaianas ♥ FARM Rio · cápsula V2</p><p class="eb">role para descobrir</p></div>
  <p class="eb janela-leg" aria-live="polite"></p>
</section>
<section class="manif">
  <p class="m-txt">A gente saiu do Rio <span class="pil"><img src="img/{e(POR['rj']['campo'][0]['img'])}" alt=""></span> e foi até quatorze estados. Em cada um, um par de chinelos <span class="pil"><img src="img/ms-par.webp" alt="" style="object-fit:contain"></span> feito com os elementos de lá, e um coração <span class="pil redonda"><img src="img/{e(POR['sc']['coracao'])}" alt=""></span> que só aparece <em>na segunda olhada</em>.</p>
  <p class="eb m-assina">projeto de portfólio de Emilly Silva · fictício, sem vínculo com as marcas</p>
</section>
<section class="estados-h">
  <div class="secao-t"><div><p class="eb">os quatorze estados</p><h2>Um lugar <em>em cada arte</em></h2></div><p class="eb">arraste para o lado →</p></div>
  <div class="trilho">{trilho}</div>
</section>
<section class="roda" aria-label="A coleção: os quatorze pares">
  <div class="roda-palco">
    <div class="roda-topo"><p class="eb">a coleção</p><h2>Quatorze pares,<br><em>um em cada estado</em></h2></div>
    <div class="cupula" aria-hidden="true">
      <svg class="anel" viewBox="0 0 1000 1000"><defs><path id="circ" d="M500,500 m-430,0 a430,430 0 1,1 860,0 a430,430 0 1,1 -860,0"/></defs>
        <text><textPath href="#circ" textLength="2690" lengthAdjust="spacing">bem-querer · do Rio para o Brasil · quatorze estados · quatorze pares · bem-querer · do Rio para o Brasil · quatorze estados ·</textPath></text></svg>
    </div>
    <div class="aro">{roda}</div>
    <div class="roda-info" aria-live="polite"><span class="n">01</span><strong>{e(data[0]["nome"])}</strong><em>{e(data[0]["est"])}</em>
      <div class="roda-bts"><button type="button" class="r-ant" aria-label="Par anterior">‹</button><a class="r-ver" href="{data[0]["url"]}">ver o estado</a><button type="button" class="r-prox" aria-label="Próximo par">›</button></div></div>
  </div>
</section>
<section class="faixa-pal" aria-label="Palavras ouvidas na rua"><div class="fp-in"><span>{todas_palavras} <i>♥</i></span><span aria-hidden="true">{todas_palavras} <i>♥</i></span></div></section>
<section class="indice">
  <p class="eb">o site</p>
  <h2>Por onde <em>começar</em></h2>
  <ol class="linhas">{indice}</ol>
</section>'''
escrever('index.html', casca('index', 'Bem-Querer · havaianas ♥ FARM Rio', 'Projeto de portfólio: uma cápsula V2 da collab havaianas ♥ FARM Rio, com 14 estados, 14 pares e um coração escondido em cada estampa.', corpo, carregador=True))

# ---------------- projeto ----------------
corpo = pg_hero('o projeto', 'Do Rio <em>para o Brasil</em>', 'Uma participação dentro da collab havaianas ♥ FARM Rio que muda só o mapa: em vez de olhar para o Rio, olha para o país.') + f'''
<section class="duas">
  <div class="prosa">
    <h2>Por que uma V2</h2>
    <p>A collab entre a havaianas e a FARM Rio já existe e já deu certo: arara, bananeira, folhagem, o Rio inteiro na palmilha. A V2 não cria outra marca nem outro logo. Ela entra como uma participação dentro da collab, com a mesma assinatura no calcanhar.</p>
    <p>Cada estado ganhou um par. O par carrega os elementos do lugar do jeito que a FARM já faz nos chinelos: folha, bicho, fruta e objeto, grandes e recortados pela borda da palmilha. Junto do par vem uma ilustração com o lugar inteiro, para quem é de lá olhar e reconhecer na hora.</p>
    <p>O ponto de partida foi sempre a rua, não o cartão-postal: feira, mesa, festa, ofício e quintal antes do monumento.</p>
  </div>
  <div class="prosa">
    <p class="citacao">“A gente se considera uma escola de estamparia.”</p>
    <p class="eb">Tati Viana, FARM, ao InvestNews</p>
    <p style="margin-top:40px">E a escola da FARM sempre foi a viagem: paisagem, festa, arquitetura e arte de rua viram estampa. A V2 segue a mesma regra, só que atravessa quatorze estados.</p>
  </div>
</section>
<section class="destaque">
  {svg_simb(simb_mono('#FFF3E6', '#6A1B29'))}
  <p>O coração nunca é desenhado em cima de nada. Ele aparece quando <em>os elementos se encontram</em>.</p>
  <p class="eb">duas folhas que caem juntas · a cauda da baleia · a franja da sombrinha de frevo</p>
</section>
<section class="duas">
  <div class="prosa">
    <h2>A collab que já existe</h2>
    <p>A FARM não cria um logo novo a cada parceria. Ela usa um sistema fixo: o logo do parceiro, um conector e FARM Rio. O coração aparece nas parcerias mais longas e de mais afeto, e é assim que a havaianas assina com a FARM.</p>
    <p>Na V1, o coração unia as duas marcas no logo. Na V2, ele sai do logo e entra no desenho: se esconde em cada estampa, formado pelos próprios elementos do estado.</p>
  </div>
  <div style="display:grid;place-items:center;background:var(--creme2);padding:10svh 4vw"><img src="img/assinatura-collab.svg" alt="Assinatura havaianas ♥ FARM Rio" style="width:min(320px,70%)"></div>
</section>
<section class="numeros" aria-label="Em números">
  <div><b>14</b><span>estados, das cinco regiões do país</span></div>
  <div><b>14</b><span>pares, um por estado, em díptico</span></div>
  <div><b>14</b><span>ilustrações do lugar inteiro, com os mesmos elementos</span></div>
  <div><b>1</b><span>coração escondido em cada estampa</span></div>
</section>''' + proxima('projeto')
escrever('projeto.html', casca('projeto', 'Projeto · Bem-Querer', 'Por que uma V2 da collab havaianas ♥ FARM Rio, e por que o coração.', corpo))

# ---------------- pesquisa ----------------
mural = ''.join(figura_campo(s, 0, s['campo'][0], link=True) for s in data)
corpo = pg_hero('a pesquisa', 'Antes do desenho, <em>a rua</em>', 'Cada estado começou por fotos reais do lugar, com autor, licença e local conferidos. O desenho só veio depois.') + f'''
<section class="numeros" aria-label="A pesquisa em números">
  <div><b>14</b><span>estados, das cinco regiões</span></div>
  <div><b>312</b><span>fotos reais reunidas na pesquisa de campo</span></div>
  <div><b>139</b><span>fotógrafos, todos creditados</span></div>
  <div><b>1</b><span>âncora por estado: o que é dali e de nenhum outro lugar</span></div>
</section>
<section class="tres">
  <div><p class="eb">regra 1</p><h3>O lugar confere</h3><p>Cada foto só entrou depois de o local aparecer no título, nas tags ou na descrição. Pinhão de Portugal e “capim dourado” que era foto de reunião ficaram de fora.</p></div>
  <div><p class="eb">regra 2</p><h3>Cotidiano antes do postal</h3><p>Feira, mesa, festa, ofício e quintal vêm primeiro. O cartão-postal só entra quando é a âncora do lugar.</p></div>
  <div><p class="eb">regra 3</p><h3>O que é sagrado fica</h3><p>Imagem de santo, coroa de Congado e estandarte não viram enfeite. A festa entra pela cor, pela fita e pela flor de papel.</p></div>
</section>
<section class="duas">
  <div class="prosa">
    <h2>Como a FARM pesquisa</h2>
    <p>Antes de cada coleção, a FARM faz workshops com os artistas e viaja pelo país estudando flora e fauna. O estúdio guarda mais de 16 mil desenhos autorais e cria cerca de 800 estampas por ano.</p>
    <p>A brasilidade vem de símbolos populares, como fruta, praia e feira, sem virar caricatura. A fundadora Kátia Barros já disse que não queria uma “marca de resort, exótica”. E as campanhas são feitas no lugar real.</p>
  </div>
  <div class="prosa">
    <h2>O que a V2 copiou disso</h2>
    <p>A viagem como método: cada estado foi lido pela rua antes de virar desenho. A regra contra a caricatura: nada de chapéu de cangaceiro ou cocar como enfeite. E a campanha no lugar: cada par foi fotografado onde a arte acontece.</p>
  </div>
</section>
<section class="secao-t"><p class="eb">pesquisa de campo</p><h2>Uma foto por estado</h2></section>
<div class="campo">{mural}</div>''' + proxima('pesquisa')
escrever('pesquisa.html', casca('pesquisa', 'Pesquisa · Bem-Querer', 'Antes do desenho, a rua: a pesquisa de campo dos quatorze estados.', corpo))

# ---------------- coleção ----------------
REG = ['Sudeste', 'Nordeste', 'Norte', 'Centro-Oeste', 'Sul']
blocos = ''
for rg in REG:
    cartas = ''.join(
        f'<a class="carta-e" href="{s["url"]}" style="--ac:{acento(s["uf"])}"><span class="arco"><span class="n">{data.index(s) + 1:02d}</span>'
        f'<img src="img/{e(s["ilu"])}" alt="Ilustração de {e(s["nome"])}" loading="lazy"></span>'
        f'<img class="par" src="img/{s["uf"]}-par.webp" alt="" loading="lazy"><strong>{e(s["nome"])}</strong><em>{e(s["est"])}</em></a>'
        for s in data if REGIAO[s['uf']] == rg)
    blocos += f'<section class="regiao"><p class="eb">{rg}</p><div class="arcos">{cartas}</div></section>'
cors = ''.join(f'<a href="{s["url"]}#coracao"><img src="img/{e(s["coracao"])}" alt="Coração de {e(s["nome"])}" loading="lazy"><b>{e(s["nome"])}</b><span>{e(s["coracao_texto"])}</span></a>' for s in data)
corpo = pg_hero('a coleção', 'Quatorze <em>pares</em>', 'Um par por estado, com a ilustração do lugar inteiro. Passe o mouse para ver o chinelo; clique para abrir o estado.') + blocos + f'''
<section class="secao-t" style="padding-top:20svh"><p class="eb">o fio da coleção</p><h2>Onde o coração mora</h2></section>
<div class="coracoes" style="margin-top:48px">{cors}</div>''' + proxima('colecao')
escrever('colecao.html', casca('colecao', 'Coleção · Bem-Querer', 'Os quatorze pares da cápsula Bem-Querer, por região.', corpo))

# ---------------- processo ----------------
corpo = pg_hero('o processo', 'Como cada par <em>nasce</em>', 'Cinco passos, sempre na mesma ordem. E duas decisões que mudaram o desenho no meio do caminho.') + f'''
<section class="indice" style="padding-top:4svh">
  <ol class="linhas">
    <li data-img="img/mg-campo-1.jpg"><div class="ln"><span>01</span><h3>Campo</h3><p>Fotos reais do lugar, com autor e licença, e o local de cada uma conferido antes de entrar.</p></div></li>
    <li data-img="img/mg-coracao.jpg"><div class="ln"><span>02</span><h3>Âncora</h3><p>Um elemento que é daquele estado e de nenhum outro. Sem âncora, o chinelo fica só bonito.</p></div></li>
    <li data-img="img/mg-palmilha.jpg"><div class="ln"><span>03</span><h3>Chinelo</h3><p>Díptico: o pé esquerdo e o direito contam metades da mesma história. Só elementos.</p></div></li>
    <li data-img="img/mg-ilustracao.jpg"><div class="ln"><span>04</span><h3>Ilustração</h3><p>O lugar inteiro, centralizado, feito com os mesmos elementos do chinelo.</p></div></li>
    <li data-img="img/mg-estudio.jpg"><div class="ln"><span>05</span><h3>O par</h3><p>A tira repete uma cor da estampa e a assinatura da collab fica no calcanhar, sem mudança.</p></div></li>
  </ol>
</section>
<section class="secao-t"><p class="eb">o que ficou pelo caminho</p><h2>Decisões que mudaram o desenho</h2></section>
<section class="decisao">
  <div class="antes-depois"><figure class="antes"><div class="moldura"><img src="img/mg-antes-jabuticaba.jpg" alt="Primeira palmilha de Minas, com jabuticaba e sabiá" loading="lazy"></div><figcaption>antes</figcaption></figure>
    <figure><div class="moldura"><img src="img/mg-depois-barroco.jpg" alt="Palmilha final de Minas, com o barroco" loading="lazy"></div><figcaption>depois</figcaption></figure></div>
  <div><p class="eb">Minas Gerais</p><h2>Minas não é só jabuticaba</h2><p>O primeiro par tinha jabuticaba, sabiá e sempre-viva. Era bonito e não dizia Minas: tem jabuticaba no quintal de meio Brasil. Queijo também não servia, porque queijo não nasce em galho. Ficou o barroco, com a talha dourada do Aleijadinho e as rosas do forro do Mestre Ataíde.</p></div>
</section>
<section class="decisao">
  <div class="antes-depois"><figure class="antes"><div class="moldura"><img src="img/sc-antes-ponte.jpg" alt="Primeira ilustração de Santa Catarina, com a baleia sob a ponte" loading="lazy"></div><figcaption>antes</figcaption></figure>
    <figure><div class="moldura"><img src="img/sc-depois-enseada.jpg" alt="Ilustração final de Santa Catarina, na enseada de Garopaba" loading="lazy"></div><figcaption>depois</figcaption></figure></div>
  <div><p class="eb">Santa Catarina</p><h2>A baleia não passa debaixo da ponte</h2><p>A primeira versão juntava a Ponte Hercílio Luz e a baleia-franca. Ficou bonito e errado: a baleia não aparece no centro de Florianópolis, ela chega perto da areia nas enseadas do litoral sul. A ilustração foi para Garopaba.</p></div>
</section>
<section class="tres">
  <div><p class="eb">regra que nasceu</p><h3>Menos igrejinha</h3><p>No primeiro lote, quatro estados terminavam numa torre de igreja. A partir do segundo, cada lugar ganhou uma cena diferente: rio, mercado, duna, pampa, mata.</p></div>
  <div><p class="eb">regra que nasceu</p><h3>Coração não é carimbo</h3><p>Nos primeiros testes, o coração aparecia pintado no brilho da jabuticaba. Saiu tudo. Hoje ele é a franja da sombrinha, a cauda da baleia, duas folhas caindo juntas.</p></div>
  <div><p class="eb">regra que nasceu</p><h3>A assinatura não muda</h3><p>O logo da collab vai no calcanhar, centralizado, tom sobre tom. Quando passa por cima de um elemento, ganha só um fio fino na cor do fundo.</p></div>
</section>''' + proxima('processo')
escrever('processo.html', casca('processo', 'Processo · Bem-Querer', 'Como cada par nasce e as decisões que mudaram o desenho.', corpo))

# ---------------- campanha ----------------
gal = ''
for s in data:
    fotos = ([(s['campanha'], 'campanha')] if s.get('campanha') else []) + [(x, 'no lugar') for x in s['lugar'][:2]]
    gal += ''.join(f'<figure><a href="{s["url"]}"><div class="moldura"><img src="img/{e(src)}" alt="O par de {e(s["nome"])}, {rot}" loading="lazy"></div>'
                   f'<figcaption>{e(s["nome"])} · {rot}</figcaption></a></figure>' for src, rot in fotos)
est = ''.join(f'<figure><a href="{s["url"]}"><div class="moldura"><img src="img/{e(s["estudio"])}" alt="O par de {e(s["nome"])} no estúdio" loading="lazy"></div>'
              f'<figcaption>{e(s["nome"])}<span>{e(s["est"])}</span></figcaption></a></figure>' for s in data)
corpo = pg_hero('a campanha', 'O par <em>no lugar</em>', 'Cada par foi fotografado no lugar da sua arte. Areia só onde o lugar tem praia ou duna; Minas em Ouro Preto, o Pará no Ver-o-Peso, o Rio Grande do Sul no pampa.') + f'''
<div class="galeria">{gal}</div>
<section class="secao-t" style="padding-top:14svh"><p class="eb">no estúdio</p><h2>Os quatorze, lado a lado</h2></section>
<div class="campo">{est}</div>''' + proxima('campanha')
escrever('campanha.html', casca('campanha', 'Campanha · Bem-Querer', 'Os quatorze pares fotografados no lugar da sua arte.', corpo))

# ---------------- identidade ----------------
pal = ''.join(f'<a href="{s["url"]}"><div class="faixas">' + ''.join(f'<span style="background:{c}"></span>' for c in COR[s['uf']]) + f'</div><b>{e(s["nome"])}</b></a>' for s in data)
corpo = pg_hero('identidade', 'Uma marca que <em>não é nova</em>', 'A V2 não ganha logo próprio: a assinatura é a da collab. O que a cápsula ganha é um emblema, como a FARM fez com a flor exclusiva da adidas FW23.') + f'''
<section class="assin">
  <img src="img/assinatura-collab.svg" alt="Assinatura havaianas ♥ FARM Rio">
  <div class="prosa"><h2>A assinatura da collab</h2><p>FARM Rio, o coração e havaianas, empilhados e centralizados no calcanhar, exatamente como já vai na palmilha da collab. A cor acompanha o fundo de cada estampa, tom sobre tom.</p><p>Os logos oficiais não ganham textura nem distorção. Quando passam por cima de um elemento, levam só um fio fino na cor do fundo para continuar legíveis.</p></div>
</section>
<section class="marca-g">
  {svg_simb()}
  <p class="wm">bem-querer</p>
  <p class="eb">o emblema da cápsula · duas folhas de amendoeira que caem juntas</p>
</section>
<section class="duas">
  <div class="prosa"><h2>Por que duas folhas</h2><p>É a regra da coleção virando símbolo: o coração nunca é desenhado, ele é formado pelos elementos. A folha é de amendoeira, a árvore das calçadas do Rio, porque a viagem sai do Rio. No outono carioca ela fica vermelha e laranja, e essas viraram as cores da marca.</p></div>
  <div class="prosa"><h2>Como ele muda</h2><p>Na campanha, o símbolo muda de estado: em cada um, o coração é o que se esconde na estampa de lá. Duas folhas de aguapé no Mato Grosso do Sul, dois pássaros de miriti no Pará, a cauda da baleia em Santa Catarina.</p></div>
</section>
<div class="aplic">
  <div style="background:var(--vinho);color:#FFF3E6">{svg_simb(simb_mono('#FFF3E6', '#6A1B29'))}<span class="wm">bem-querer</span></div>
  <div style="background:var(--laranja);color:#2A1A17">{svg_simb(simb_mono('#2A1A17', '#E07A2E'))}<span class="wm">bem-querer</span></div>
  <div style="background:#59173B;color:#FCE9D2">{svg_simb(simb_mono('#FCE9D2', '#59173B'))}<span class="wm">bem-querer</span></div>
</div>
<section class="tipos">
  <div><p class="amostra">Aa</p><p class="eb" style="margin-top:20px">Instrument Serif · títulos e emblema</p><p>Uma serifa fina e alta, que fica elegante grande e conversa com a letra das revistas de moda. Itálico para os nomes das estampas.</p></div>
  <div><p class="amostra s">Aa</p><p class="eb" style="margin-top:20px">Jost · texto, etiqueta e linha da cápsula</p><p>Geométrica como o FARM RIO do logo da collab, para o texto não brigar com a assinatura. As duas são livres, do Google Fonts.</p></div>
</section>
<section class="cores">
  <p class="eb">cores</p>
  <div class="base">
    <div style="background:var(--creme);box-shadow:inset 0 0 0 1px var(--linha)">creme<br>#F4EDE3</div>
    <div style="background:var(--vinho);color:#FFF3E6">vinho<br>#6A1B29</div>
    <div style="background:var(--laranja)">laranja<br>#E07A2E</div>
  </div>
  <p class="eb" style="margin-bottom:24px">e uma paleta por estado, tirada da própria estampa</p>
  <div class="paletas">{pal}</div>
</section>''' + proxima('identidade')
escrever('identidade.html', casca('identidade', 'Identidade · Bem-Querer', 'A assinatura da collab, o emblema da cápsula, fontes e cores.', corpo))

# ---------------- créditos ----------------
cred = ''.join(
    f'<li><b>{e(s["nome"])}</b> · ' + '; '.join(
        f'{e(LEGENDA[s["uf"]][k])}: {e(autor(f["autor"]))}, {e(f["licenca"])}' + (f' (<a href="{e(f["pagina"])}">fonte</a>)' if f.get('pagina') else '')
        for k, f in enumerate(s['campo'])) + '</li>' for s in data)
corpo = pg_hero('créditos', 'Ficha <em>técnica</em>', 'Quem fez o quê, de onde vieram as fotos de campo e o aviso de que tudo isto é um projeto de portfólio.') + f'''
<section class="miolo" style="padding-bottom:10svh">
  <dl class="ficha">
    <dt>Conceito, pesquisa de campo e direção de arte</dt><dd>Emilly Silva</dd>
    <dt>Estampas, ilustrações e chinelos</dt><dd>Emilly Silva</dd>
    <dt>Fotos de campo</dt><dd>139 fotógrafos, creditados abaixo, sob licenças Creative Commons</dd>
    <dt>Assinatura</dt><dd>a da collab havaianas ♥ FARM Rio, sem alteração</dd>
    <dt>Fontes</dt><dd>Instrument Serif e Jost, licença livre (Google Fonts)</dd>
  </dl>
</section>
<section class="secao-t"><p class="eb">fotos de campo</p><h2>Os fotógrafos</h2></section>
<section class="miolo" style="padding-top:36px;padding-bottom:10svh"><ul class="creditos">{cred}</ul>
  <p style="margin-top:40px;max-width:70ch;color:#4C3C35">As fotos de campo são de seus autores, sob as licenças Creative Commons indicadas, e foram usadas como pesquisa. Bem-Querer é um projeto fictício de portfólio de Emilly Silva. Não é uma coleção oficial e não tem vínculo com a FARM Rio nem com a havaianas.</p></section>''' + proxima('creditos')
escrever('creditos.html', casca('creditos', 'Créditos · Bem-Querer', 'Ficha técnica e créditos das fotos de campo do projeto Bem-Querer.', corpo))

# ---------------- estados ----------------
caixas = {c['estado']: c['caixa'] for c in json.load(open(os.path.join(AQUI, 'mapa_coracoes_caixas.json'), encoding='utf8'))}
R = '../'
for i, s in enumerate(data):
    uf, t, cad = s['uf'], V[s['uf']], T[s['uf']]
    x0, y0, x1, y1 = caixas[s['nome']]
    d = max(x1 - x0, y1 - y0) * 1.3
    campo = ''.join(figura_campo(s, k, f, r=R) for k, f in enumerate(s['campo'][:3]))
    lug = [(x, 'no lugar') for x in s['lugar'][:2]]
    pal_estado = ' <i>♥</i> '.join(e(w) for w in cad['palavras'])
    lugar = ''.join(f'<figure><div class="moldura"><img src="{R}img/{e(src)}" alt="O par de {e(s["nome"])}, {rot}" loading="lazy"></div><figcaption>{rot}</figcaption></figure>' for src, rot in lug)
    evitar = ''.join(f'<li><span>{k + 1:02d}</span><p>{md(x)}</p></li>' for k, x in enumerate((EVITAR_EXTRA.get(uf, []) + list(cad['evitar']))[:3]))
    prox, ant = data[(i + 1) % len(data)], data[i - 1]
    cred = ''.join(f'<li>{e(LEGENDA[uf][k])}: {e(autor(f["autor"]))}, {e(f["licenca"])}' + (f' (<a href="{e(f["pagina"])}">fonte</a>)' if f.get('pagina') else '') + '</li>'
                   for k, f in enumerate(s['campo']))
    paleta = ''.join(f'<span style="background:{c}"></span>' for c in COR[uf])
    corpo = f'''
<section class="e-hero cena">
  <div class="cena-in">
    <div class="cena-txt">
      <a class="e-volta" href="{R}colecao.html">← coleção</a>
      <h1>{e(s["nome"])}</h1>
      <p class="est">{e(t["nome"])}</p>
      <p class="conc">{e(t["conceito"])}</p>
      <p class="num"><b>{i + 1:02d}</b> / 14 · {REGIAO[uf]}</p>
    </div>
    <div class="cena-arte">
      <figure class="arco-ilu">{midia(s, r=R, auto=True).replace('loading="lazy"', 'loading="eager"')}</figure>
      <img class="par-flutua" src="{R}img/{uf}-par.webp" alt="O par de {e(s["nome"])}" loading="eager">
    </div>
  </div>
</section>
<section class="faixa-pal" aria-label="Palavras ouvidas na rua"><div class="fp-in"><span>{pal_estado} <i>♥</i></span><span aria-hidden="true">{pal_estado} <i>♥</i></span></div></section>
<section class="busca" id="coracao" aria-labelledby="busca-t">
  <div class="busca-in">
    <div>
      <p class="eb">o coração</p>
      <h2 id="busca-t">Encontre o coração</h2>
      <p>Ele não está desenhado em cima de nada. Aparece quando os próprios elementos da cena se encontram. Procure na ilustração e toque nele.</p>
      <button class="bt-claro" type="button">mostrar o coração</button>
      <p class="resp" aria-live="polite">♥ {e(s["coracao_texto"])}</p>
    </div>
    <figure class="quadro-cor"><img src="{R}img/{uf}-ilu-sem-g.jpg" alt="Ilustração de {e(s["nome"])} sem a assinatura" loading="lazy"><button class="alvo" type="button" aria-label="Este é o coração" style="left:{(x0 + x1) / 2 / 1744 * 100:.2f}%;top:{(y0 + y1) / 2 / 2336 * 100:.2f}%;width:{d / 1744 * 100:.2f}%;height:{d / 2336 * 100:.2f}%"></button></figure>
  </div>
</section>
<section class="e-par">
  <figure class="foto-est moldura" style="margin:0"><img src="{R}img/{e(s["estudio"])}" alt="O par de {e(s["nome"])} no estúdio" loading="lazy"></figure>
  <div>
    <p class="eb">o par</p>
    <h2>Dois pés, uma história</h2>
    <div class="bloco"><p class="eb">na palmilha</p><p>{md(t["chinelo"])}</p></div>
    <div class="bloco"><p class="eb">borracha e tira</p><p>{md(t["fundo"])}</p><div class="paleta">{paleta}</div></div>
  </div>
</section>
<section class="diptico" style="--bgd:{COR[uf][0]};--inkd:{"#FFF3E6" if lum(COR[uf][0]) < .3 else "#2A1A17"}">
  <p class="eb">a arte da palmilha</p>
  <h2>Em díptico</h2>
  <img src="{R}img/{e(s["palmilha"])}" alt="Arte da palmilha de {e(s["nome"])}, em díptico: o pé esquerdo e o direito contam metades da mesma cena" loading="lazy">
  <div class="dp-leg"><span>pé esquerdo</span><span>pé direito</span></div>
</section>
<section class="caderno">
  <p class="eb">caderno de campo</p>
  <p class="cronica">{md(cad["cronica"])}</p>
  <p class="trilha-e">trilha · {md(cad["trilha"])}</p>
  <p class="ancora-e">A âncora: {md(t["ancora"])}</p>
</section>
<section class="e-campo">
  <div class="secao-t"><p class="eb">pesquisa de campo</p><h2>Na rua, antes do desenho</h2></div>
  <div class="campo tres-col">{campo}</div>
</section>
<section class="cinema"><img src="{R}img/{e(s.get("campanha") or s["lugar"][0])}" alt="O par de {e(s["nome"])} na campanha" loading="lazy">
  <div class="cin-leg"><p class="eb">campanha</p><h2>O par <em>no lugar</em></h2></div></section>
<section class="e-lugar" style="padding-top:12svh">
  <div class="lugar dois">{lugar}</div>
</section>
<section class="e-evitar">
  <p class="eb">o que ficou de fora</p>
  <h2 class="titulo-sec">O que a gente evitou</h2>
  <ol class="evita">{evitar}</ol>
</section>
<section class="miolo" style="padding-top:8svh"><p class="eb" style="margin-bottom:14px">fotos de campo deste estado</p><ul class="creditos">{cred}</ul></section>
<a class="prox" href="{R}{prox["url"]}"><span><span class="eb">próximo estado · {(i + 1) % len(data) + 1:02d} / 14</span><strong>{e(prox["nome"])}</strong><em>{e(prox["est"])}</em></span><span class="mini"><img src="{R}img/{e(prox["ilu"])}" alt="" loading="lazy"></span></a>
<a class="ant" href="{R}{ant["url"]}">← {e(ant["nome"])}</a>'''
    escrever(s['url'], casca('colecao', f'{e(s["nome"])} · Bem-Querer', f'Bem-Querer em {s["nome"]}: {t["nome"]}. Um par de chinelos, uma ilustração e um coração escondido.',
                              corpo, r=R, estilo_body=f' style="--ac:{acento(uf)}"'))

# ---------------- arquivos comuns e limpeza ----------------
os.makedirs(SITE + '/css', exist_ok=True)
shutil.copy(os.path.join(AQUI, 'v5', 'bq.css'), SITE + '/css/bq.css')
shutil.copy(os.path.join(AQUI, 'v5', 'bq.js'), SITE + '/js/bq.js')
_pdf = os.path.join(P, '07-apresentacao', 'pdf', 'bem-querer-apresentacao.pdf')
if os.path.exists(_pdf):
    shutil.copy(_pdf, SITE + '/bem-querer-apresentacao.pdf')
for velho in ['v4.html'] + [f'{s["uf"]}.html' for s in data]:
    p_ = os.path.join(SITE, velho)
    if os.path.exists(p_):
        os.remove(p_)
print('ok', sorted(os.path.basename(x) for x in glob.glob(SITE + '/*.html')), len(glob.glob(SITE + '/estados/*.html')), 'estados')
