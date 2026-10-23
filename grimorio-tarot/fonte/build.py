# Gera grimorio.html a partir de dados/*.json (as fichas transcritas).
# Uso: python3 -I build.py
import json, os, html, re
DIR = os.path.dirname(os.path.abspath(__file__))
esc = html.escape

NAIPES = [
    ('copas',   'Copas',   'Água',  'o naipe das emoções',
     'Copas fala do que se sente: amor, afeto, amizade, intuição, os vínculos e a vida emocional. É a água que corre, enche e transborda.'),
    ('paus',    'Paus',    'Fogo',  'o naipe da ação',
     'Paus fala do que se faz: vontade, criatividade, coragem, projetos e iniciativa. É o fogo que acende, move e às vezes queima.'),
    ('espadas', 'Espadas', 'Ar',    'o naipe da mente',
     'Espadas fala do que se pensa: ideias, palavras, decisões, verdades e conflitos. É o ar que corta, clareia e também fere.'),
    ('ouros',   'Ouros',   'Terra', 'o naipe da matéria',
     'Ouros fala do que se constrói: trabalho, dinheiro, corpo, casa e segurança. É a terra que sustenta, dá fruto e pede paciência.'),
]
ORD = ['Ás', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valete', 'Cavaleiro', 'Rainha', 'Rei']
ROM = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'Valete', 'Cavaleiro', 'Rainha', 'Rei']

# ---------- desenhos a traço ----------
INK = '#5b4a3d'; RED = '#9e3b28'
def svg_naipe(n, cls='naipe'):
    g = {
     'copas': '<path d="M22 14 h56 c0 26 -10 40 -28 44 c-18 -4 -28 -18 -28 -44z"/><path d="M28 22 h44" opacity=".6"/><path d="M50 58 v20"/><path d="M44 66 c4 2 8 2 12 0" opacity=".6"/><path d="M32 90 c4 -8 12 -12 18 -12 c6 0 14 4 18 12z"/><path d="M50 8 v-4 M42 9 l-2 -3 M58 9 l2 -3" opacity=".7"/>',
     'paus':  '<path d="M42 96 L54 6 L62 7 L50 97 Z"/><path d="M47 80 l2 -14 M51 50 l2 -14" opacity=".55"/><path d="M53 24 c-9 -1 -15 -7 -16 -13 c8 0 14 5 16 13z"/><path d="M59 42 c8 -6 16 -5 19 0 c-7 5 -14 5 -19 0z"/><path d="M49 62 c-9 1 -15 -3 -18 -9 c8 -2 14 2 18 9z"/><path d="M37 11 l9 6 M78 42 l-12 0 M31 53 l11 5" opacity=".5"/>',
     'espadas': '<path d="M50 4 L56 16 L56 68 L44 68 L44 16 Z"/><path d="M50 8 V66" opacity=".55"/><path d="M30 68 h40 c0 4 -4 6 -8 6 h-24 c-4 0 -8 -2 -8 -6z"/><path d="M46 74 h8 v16 h-8z"/><circle cx="50" cy="94" r="4"/>',
     'ouros': '<circle cx="50" cy="50" r="40"/><circle cx="50" cy="50" r="34" opacity=".6"/><path d="M50 18 L69 76 L19 40 L81 40 L31 76 Z"/>',
    }[n]
    return f'<svg class="{cls}" viewBox="0 0 100 100" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round">{g}</svg>'

def svg_elemento(el):
    e = (el or '').lower()
    up = 'fogo' in e or e.startswith('ar')
    tri = 'M10 2 L18 16 L2 16 Z' if up else 'M2 2 L18 2 L10 16 Z'
    bar = ''
    if e.startswith('ar'): bar = '<path d="M5 11 H15"/>'
    if 'terra' in e: bar = '<path d="M5 7 H15"/>'
    return f'<svg class="el" viewBox="0 0 20 18" fill="none" stroke="{RED}" stroke-width="1.5" stroke-linejoin="round"><path d="{tri}"/>{bar}</svg>'

PLANETAS = {'sol': '☉', 'lua': '☽', 'mercúrio': '☿', 'vênus': '♀', 'marte': '♂', 'júpiter': '♃',
            'saturno': '♄', 'urano': '♅', 'netuno': '♆', 'plutão': '♇'}
SIGNOS = {'áries': '♈', 'touro': '♉', 'gêmeos': '♊', 'câncer': '♋', 'leão': '♌', 'virgem': '♍',
          'libra': '♎', 'escorpião': '♏', 'sagitário': '♐', 'capricórnio': '♑', 'aquário': '♒', 'peixes': '♓'}
def glifos(txt, tabela):
    t = (txt or '').lower(); out = []
    for k, g in tabela.items():
        for m in re.finditer(k, t): out.append((m.start(), g))
    seen = []; [seen.append(g) for _, g in sorted(out) if g not in seen]
    return ''.join(f'<span class="gl">{g}︎</span>' for g in seen[:3])

CORES = [('dourad', '#d9a441'), ('ouro', '#d9a441'), ('amarel', '#e8c547'), ('laranj', '#e08a3c'),
         ('vermelh', '#c0392b'), ('carmim', '#a61e2e'), ('rosa', '#e7a2b4'), ('pink', '#e7a2b4'),
         ('roxo', '#6d3f8f'), ('violeta', '#7b4fa3'), ('púrpura', '#6d3f8f'), ('lilás', '#b9a0d6'), ('lavanda', '#b9a0d6'),
         ('azul-escuro', '#284a8a'), ('azul escuro', '#284a8a'), ('azul marinho', '#24386e'), ('azul claro', '#8cc3e8'),
         ('anil', '#3b4d9b'), ('índigo', '#3b4d9b'), ('turquesa', '#3fb3b0'), ('azul', '#4a90d9'), ('celeste', '#8cc3e8'),
         ('verde-escuro', '#2f6b3a'), ('verde escuro', '#2f6b3a'), ('verde', '#3e9a4f'),
         ('marrom', '#7a4e2d'), ('castanh', '#7a4e2d'), ('terra', '#8b5a2b'), ('bege', '#d8c3a0'), ('ocre', '#c08a2e'),
         ('cinz', '#9a9a9a'), ('prat', '#c3c6cc'), ('pret', '#222222'), ('branc', '#ffffff'), ('bronze', '#a8713a'), ('cobre', '#b5683c')]
def cor_hex(nome):
    n = nome.lower()
    for k, h in CORES:
        if k in n: return h
    return '#cccccc'

def simnao(v):
    v = (v or '').strip().lower()
    out = []; ops = ['Sim', 'Não', 'Talvez']
    if v and not any(v.startswith(w.lower()[:3]) for w in ops): ops[2] = v.capitalize()   # ex.: "Dúvida"
    for w in ops:
        on = v.startswith(w.lower()[:3])
        out.append(f'<span class="sn{" on" if on else ""}">{w}' + (
            '<svg viewBox="0 0 60 28" preserveAspectRatio="none"><path d="M8 6 C 22 0, 50 1, 56 10 C 61 19, 44 27, 26 26 C 10 25, 1 19, 4 11 C 6 7, 12 4, 18 3" fill="none" stroke="#b23a2a" stroke-width="1.6" stroke-linecap="round"/></svg>' if on else '') + '</span>')
    return ''.join(out)

def md(t):
    """negrito simples **x** e setas."""
    t = esc(t or '')
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    return t.replace('-&gt;', '→')

def limpa_item(s):
    return md(s.strip().rstrip('.'))

def medalhao():
    import math
    C, R1, R2, Rt, Rr = 200, 192, 178, 160, 146
    ticks = ''
    for i in range(120):
        a = i * math.pi * 2 / 120; l = 11 if i % 5 == 0 else 6
        ticks += f'<line x1="{C+math.cos(a)*R1:.1f}" y1="{C+math.sin(a)*R1:.1f}" x2="{C+math.cos(a)*(R1-l):.1f}" y2="{C+math.sin(a)*(R1-l):.1f}"/>'
    sq = Rr * math.sqrt(.5)
    pts = [(C + math.cos(math.radians(d)) * Rr, C + math.sin(math.radians(d)) * Rr) for d in (0, 90, 180, 270)]
    def ic(n, x, y, s=74):
        inner = svg_naipe(n).split('>', 1)[1].rsplit('</svg>', 1)[0]
        return f'<svg x="{x-s/2:.1f}" y="{y-s/2:.1f}" width="{s}" height="{s}" viewBox="0 0 100 100" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round">{inner}</svg>'
    d = 72
    icons = ic('copas', C, C-d) + ic('paus', C+d, C) + ic('espadas', C, C+d) + ic('ouros', C-d, C)
    star = f'<path d="M{C} {C-16} L{C+4.5} {C-4.5} L{C+16} {C} L{C+4.5} {C+4.5} L{C} {C+16} L{C-4.5} {C+4.5} L{C-16} {C} L{C-4.5} {C-4.5}Z" fill="{RED}"/>'
    return f'''<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:100%">
    <defs><path id="arcTop" d="M {C-Rt},{C} A {Rt},{Rt} 0 0 1 {C+Rt},{C}"/><path id="arcBot" d="M {C-Rt+8},{C} A {Rt-8},{Rt-8} 0 0 0 {C+Rt-8},{C}"/></defs>
    <circle cx="{C}" cy="{C}" r="{R1}" fill="none" stroke="{INK}" stroke-width="1.6"/>
    <g stroke="{INK}" stroke-width="1">{ticks}</g>
    <circle cx="{C}" cy="{C}" r="{R2}" fill="none" stroke="{INK}" stroke-width=".8"/>
    <circle cx="{C}" cy="{C}" r="{Rr}" fill="none" stroke="{RED}" stroke-width="1.1"/>
    <g fill="none" stroke="{INK}" stroke-width=".7" opacity=".45"><rect x="{C-sq:.1f}" y="{C-sq:.1f}" width="{2*sq:.1f}" height="{2*sq:.1f}"/></g>
    {''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{RED}"/>' for x, y in pts)}
    <text font-family="Fondamento" font-style="italic" font-size="15.5" fill="{RED}" letter-spacing=".4"><textPath href="#arcTop" startOffset="50%" text-anchor="middle">Copas ✦ Paus ✦ Espadas ✦ Ouros</textPath></text>
    <text font-family="Fondamento" font-style="italic" font-size="15.5" fill="{RED}" letter-spacing=".4" dominant-baseline="hanging"><textPath href="#arcBot" startOffset="50%" text-anchor="middle">Água ✦ Fogo ✦ Ar ✦ Terra</textPath></text>
    {icons}{star}</svg>'''

# ---------- páginas ----------
pages = []           # (html, classes)
def page(body, cls='', furo=True, num=True):
    pages.append(f'<section class="page {cls}{"" if num else " sem-num"}">{body}' +
                 ('<div class="pnum"></div>' if num else '') + ('<div class="furo"></div>' if furo else '') + '</section>')

def carregar():
    dados = {}
    for n, *_ in NAIPES:
        f = os.path.join(DIR, 'dados', f'{n}.json')
        dados[n] = json.load(open(f, encoding='utf-8'))
        assert len(dados[n]) == 14, (n, len(dados[n]))
    return dados

dados = carregar()

# numeração: 1 capa, 2 sobre, 3 como ler; cada naipe = abertura (2) + 14 cartas x 2
inicio = {}; p = 4
for n, *_ in NAIPES:
    inicio[n] = p; p += 2 + 28
TOTAL = p   # última página (sobre a autora)
def pag_carta(n, i): return inicio[n] + 2 + 2 * i

# 1 · capa
page(f'''<div class="inner" style="top:18mm">
  <p class="kick c" style="font-size:11.5pt">Arcanos Menores · fichas rápidas</p>
  <h1 class="t c" style="font-size:72pt;margin-top:1mm">Tarot</h1>
  <p class="c" style="font-style:italic;font-size:17pt;color:var(--ink2);margin-top:-1mm">grimório das cinquenta e seis cartas</p>
  <div class="medalhao" style="width:96mm;height:96mm;margin:7mm auto 0">{medalhao()}</div>
  <p class="c" style="font-family:'Fondamento';font-size:12pt;margin-top:8mm;color:var(--ink)">a partir das fichas da Prof. Edite Pedro</p>
  <p class="c mao" style="font-size:12.5pt;margin-top:5mm;color:var(--ink2)">este grimório pertence a</p>
  <div class="linha-nome"></div>
</div>''', 'capa', furo=True, num=False)

# 2 · sobre estas fichas (texto da Edite Pedro)
page('''<div class="inner">
  <p class="kick">Antes de começar</p>
  <h1 class="t">Sobre estas fichas</h1>
  <svg class="flor" data-flor></svg>
  <p class="ni"><span class="cap">L</span>er o Tarot não precisa ser um caminho de memorização cansativa, onde cada arcano se torna uma lista interminável de palavras-chave para decorar. As <em>Fichas Rápidas dos Arcanos Menores</em> surgem exatamente como uma aliada prática e transformadora: em vez de sobrecarregar a mente, elas funcionam como um atalho inteligente, permitindo uma breve consulta no momento da leitura.</p>
  <p>Assim, basta um simples olhar para desbloquear aquela informação que parecia esquecida, trazendo de volta a clareza e a confiança.</p>
  <p>Mas o valor das fichas vai muito além da praticidade. Elas também ampliam o poder <span class="hl">terapêutico do Tarot</span>, pois cada arcano está associado a ervas e cristais específicos.</p>
  <p>Isso significa que, ao consultar uma carta, você não apenas acessa seus significados simbólicos, mas também pode integrar na prática ferramentas energéticas e naturais que harmonizam corpo, mente e espírito.</p>
  <p>Dessa forma, a leitura deixa de ser apenas uma interpretação e se torna uma experiência completa de cura e autoconhecimento, onde os símbolos do Tarot se entrelaçam com a força da natureza.</p>
  <p>Com as fichas em mãos, cada leitura ganha mais fluidez, profundidade e conexão, transformando o Tarot em um verdadeiro instrumento terapêutico e intuitivo — acessível, claro e cheio de poder.</p>
  <p class="c mao red" style="font-size:14pt;margin-top:4mm">Bjs com carinho da prof. Edite Pedro</p>
</div>''')

# 3 · como ler + os quatro naipes
linhas = ''.join(f'''<div class="nrow">{svg_naipe(n, 'naipe mini')}<div><p class="nn">{nome} <span class="ne">{svg_elemento(el)} {el}</span></p><p class="nd">{sub[0].upper()+sub[1:]}</p></div><p class="np">p. {inicio[n]}</p></div>''' for n, nome, el, sub, _ in NAIPES)
page(f'''<div class="inner">
  <p class="kick">Como usar</p>
  <h1 class="t">Como ler a ficha</h1>
  <svg class="flor" data-flor></svg>
  <p class="ni">Cada carta ocupa duas páginas, uma de frente para a outra. Abra o caderno na carta que saiu e leia da esquerda para a direita:</p>
  <div class="esquema">
    <div class="folha"><p class="ft">página da esquerda</p><p class="fs">a leitura rápida</p>
      <ul><li>a carta</li><li>sim ou não</li><li>elemento, planeta, signo e tempo</li><li>a afirmação</li><li>luz e sombra</li></ul></div>
    <div class="folha"><p class="ft">página da direita</p><p class="fs">para aprofundar</p>
      <ul><li>os símbolos da carta</li><li>as cores</li><li>a numerologia</li><li>ervas e cristais</li></ul></div>
  </div>
  <p class="ni small"><span class="hl">Luz</span> são os aspectos positivos da carta; <span class="hl">sombra</span>, os negativos. O círculo vermelho marca a resposta para perguntas de sim ou não.</p>
  <h3 class="ic">Os quatro naipes</h3>
  {linhas}
</div>''')

def abertura(n, nome, el, sub, texto):
    cartas = dados[n]
    rows = ''.join(f'''<tr><td><span class="cn">{esc(c['nome'])}</span><span class="kw">{limpa_item((c.get('positivos') or [''])[0])}</span></td><td class="s">{esc((c.get('sim_nao') or '').strip())}</td><td class="pg">{pag_carta(n, i)}</td></tr>''' for i, c in enumerate(cartas))
    page(f'''<div class="inner abre">
  <p class="kick c">Naipe</p>
  <h1 class="t c" style="font-size:60pt">{nome}</h1>
  <svg class="flor c" data-flor></svg>
  {svg_naipe(n, 'naipe grande')}
  <p class="c el-linha">{svg_elemento(el)} elemento {el}</p>
  <p class="c mao" style="font-size:13pt;color:var(--ink2)">{sub}</p>
  <p class="c abre-txt">{texto}</p>
  <p class="c small" style="color:var(--ink2);margin-top:4mm">Do Ás ao 10, as etapas de uma história. Valete, Cavaleiro, Rainha e Rei: as pessoas e as posturas.</p>
</div>''', 'abertura')
    page(f'''<div class="inner">
  <div class="kick-row"><p class="kick">{nome} · {el}</p><p class="mao">as catorze cartas</p></div>
  <h1 class="t">As cartas de {nome}</h1>
  <svg class="flor" data-flor></svg>
  <table class="indice"><tr class="th"><td>a carta e a sua primeira luz</td><td class="s">sim/não</td><td class="pg">pág.</td></tr>{rows}</table>
</div>''')

def carta(n, nome_naipe, el, i, c):
    img = f'img/cartas/p{c["pagina_pdf"]:02d}.jpg'
    nome = esc(c['nome'])
    pos = ''.join(f'<li>{limpa_item(x)}</li>' for x in c.get('positivos') or [])
    neg = ''.join(f'<li>{limpa_item(x)}</li>' for x in c.get('negativos') or [])
    plan = c.get('planeta') or '—'; zod = c.get('zodiaco') or '—'
    page(f'''<div class="inner fit">
  <div class="kick-row"><p class="kick">{nome_naipe} · {el}</p><p class="mao">leitura rápida</p></div>
  <h1 class="t">{nome}</h1>
  <svg class="flor" data-flor></svg>
  <div class="topo">
    <figure class="carta"><img src="{img}" alt=""></figure>
    <div class="dados">
      <p class="rot">sim ou não</p>
      <p class="simnao">{simnao(c.get('sim_nao'))}</p>
      <table class="ficha">
        <tr><td class="l">Elemento</td><td>{svg_elemento(c.get('elemento') or el)} {md(c.get('elemento') or el)}</td></tr>
        <tr><td class="l">Planeta</td><td>{glifos(plan, PLANETAS)} {md(plan)}</td></tr>
        <tr><td class="l">Signo</td><td>{glifos(zod, SIGNOS)} {md(zod)}</td></tr>
        <tr><td class="l">Tempo</td><td class="tempo">{md(c.get('tempo') or '—')}</td></tr>
      </table>
    </div>
  </div>
  <div class="moldura afirm"><p class="mt">Afirmação</p><p class="fala">“{md((c.get('afirmacao') or '').strip().strip('“”"'))}”</p></div>
  <div class="luzsombra">
    <div><h3 class="ls">✦ Luz</h3><ul class="star">{pos}</ul></div>
    <div><h3 class="ls sombra">✧ Sombra</h3><ul class="star sombra">{neg}</ul></div>
  </div>
  <div class="vaga-cores"></div>
</div>''', 'carta-esq')

    arq = c.get('arquetipo')
    simb = ''.join(f'<li><b>{md(s["nome"].strip().rstrip(":"))}.</b> {md(s.get("texto"))}</li>' for s in c.get('simbolos') or [])
    cores = ''.join(f'''<div class="cor"><span class="dot" style="background:{cor_hex(k['nome'])}"></span><p><b>{md(k['nome'])}</b>{('. ' + md(k['texto'])) if k.get('texto') else ''}</p></div>''' for k in c.get('cores') or [])
    num = c.get('numerologia') or {}
    ervas = ', '.join(esc(x) for x in c.get('ervas') or []) or '—'
    crist = ', '.join(esc(x) for x in c.get('cristais') or []) or '—'
    page(f'''<div class="inner fit">
  <div class="kick-row"><p class="kick">Os símbolos</p><p class="mao">{nome}</p></div>
  {f'<p class="arq">{md(arq)}</p>' if arq else ''}
  <ul class="star simb">{simb}</ul>
  <div class="bloco-cores"><h3 class="ic">As cores</h3>
  <div class="cores">{cores}</div></div>
  <div class="pratica">
    <div class="num"><p class="pt">Numerologia</p><p>{('<span class="nt">' + md(num.get('titulo')) + '</span> ') if num.get('titulo') else ''}{md(num.get('texto'))}</p></div>
    <div class="ec"><p class="pt">Ervas</p><p>{ervas}</p><p class="pt" style="margin-top:2mm">Cristais</p><p>{crist}</p></div>
  </div>
</div>''', 'carta-dir')

for n, nome, el, sub, texto in NAIPES:
    abertura(n, nome, el, sub, texto)
    for i, c in enumerate(dados[n]):
        carta(n, nome, el, i, c)

# última · sobre a autora + anotações
page('''<div class="inner">
  <p class="kick">De onde vêm estas fichas</p>
  <h1 class="t">Edite Pedro</h1>
  <svg class="flor" data-flor></svg>
  <p class="ni small">Taróloga e professora de Tarot, pós-graduada com especialização em Metodologia Científica e Didática de Ensino. Há mais de três décadas desenvolve estratégias de ensino e aprendizado com o tarot, usando-o como ferramenta terapêutica para o autoconhecimento e o desenvolvimento pessoal e profissional. Já inseriu mais de 2.300 alunas no mercado das terapias integrativas.</p>
  <p class="ni small" style="margin-top:1.5mm"><span class="hl">Instagram</span> @Prof.EditePedro · <span class="hl">YouTube</span> Edite Pedro - Professora de Tarot</p>
  <h3 class="ic">Anotações</h3>
  <div class="pauta" style="height:96mm"></div>
</div>''')

assert len(pages) == TOTAL, (len(pages), TOTAL)
assert TOTAL % 4 == 0, TOTAL

tpl = open(os.path.join(DIR, 'modelo.html'), encoding='utf-8').read()
open(os.path.join(DIR, 'grimorio.html'), 'w', encoding='utf-8').write(tpl.replace('<!--PAGINAS-->', '\n'.join(pages)))
print('páginas:', TOTAL, {n: inicio[n] for n in inicio})
