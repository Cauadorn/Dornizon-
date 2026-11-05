"""Gera o site de apresentação (07-apresentacao/site/index.html) a partir do data.json e dos textos.
Uso: python gerar_site.py"""
import html
import importlib.util
import json
import re

P = '/home/user/Dornizon-/farm-bem-querer'
SITE = P + '/07-apresentacao/site'
data = json.load(open(SITE + '/data.json', encoding='utf8'))

spec = importlib.util.spec_from_file_location('v', P + '/_ferramentas/textos_v2.py')
mv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mv)
V = {k.lower(): v['estampa'] for k, v in mv.V.items()}

# caderno de campo: crônica, palavras, trilha e o que a gente evitou
T = {}
for nome in ('textos_estados_1', 'textos_estados_2'):
    sp = importlib.util.spec_from_file_location(nome, P + f'/_ferramentas/{nome}.py')
    mm = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mm)
    T.update({k.lower(): v for k, v in mm.T.items()})
T['mg'] = json.load(open(P + '/_ferramentas/caderno_mg.json', encoding='utf8'))
T['go']['cronica'] = T['go']['cronica'].replace(' Em 2026 a festa fez 200 anos.', '')
EVITAR_EXTRA = {
    'mg': ['**Jabuticaba como símbolo de Minas:** tem jabuticaba no quintal de meio Brasil; ficou na primeira versão e saiu.'],
    'sc': ['**A baleia debaixo da ponte:** ela não aparece no centro de Florianópolis; a ilustração foi para Garopaba.'],
}

# lote 1, no mesmo formato do textos_v2
V['mg'] = {
    'nome': 'Barroco de Minas',
    'conceito': 'O ouro das igrejas de Ouro Preto, mas visto de perto: a talha que sobe pelos altares e as rosas que o Mestre Ataíde pintou no forro da São Francisco de Assis.',
    'ancora': 'o **barroco mineiro**: volutas e conchas douradas como as talhas do Aleijadinho e as guirlandas do forro do Ataíde.',
    'chinelo': 'pé esquerdo com a talha dourada de volutas e concha; pé direito com a guirlanda de rosas e a fita azul-colonial.',
    'fundo': 'branco-caiado das igrejas mineiras; tira azul-colonial.',
    'ilustracao': 'a janela de um casarão de Ouro Preto, coroada pela mesma talha dourada, com a guirlanda no parapeito e as torres da São Francisco ao fundo.',
}
V['ba'] = {
    'nome': 'Cacau e Fita',
    'conceito': 'O sul da Bahia que dá o cacau e a Salvador que amarra fita no portão do Bonfim, juntos no mesmo par.',
    'ancora': 'a **fita do Senhor do Bonfim**, que qualquer brasileiro reconhece de longe.',
    'chinelo': 'pé esquerdo com o galho de cacau e um fruto aberto; pé direito com as fitas do Bonfim, sem letreiro, descendo em ondas.',
    'fundo': 'azul do céu de Salvador; tira vermelho-fita.',
    'ilustracao': 'o Largo do Pelourinho visto de baixo, com a igreja do Rosário dos Pretos no alto, fitas entre as sacadas, uma baiana de costas e o cacau emoldurando a cena.',
}
V['pe'] = {
    'nome': 'Passo de Frevo',
    'conceito': 'A sombrinha que abre o carnaval de Recife e Olinda, girando entre as buganvílias das ladeiras.',
    'ancora': 'a **sombrinha de frevo**, que só existe em Pernambuco.',
    'chinelo': 'pé esquerdo com buganvília de Olinda e duas sombrinhas pequenas; pé direito com a sombrinha grande e o celofane do caboclo de lança.',
    'fundo': 'areia morna; tira azul-frevo.',
    'ilustracao': 'a sombrinha no céu de Olinda, o celofane do caboclo de lança explodindo como fogos e o casario colorido da ladeira embaixo.',
}
V['go'] = {
    'nome': 'Cavalhada',
    'conceito': 'As Cavalhadas de Pirenópolis, quando os cavalos saem enfeitados de flor de papel e fita, com o pequi do cerrado em volta.',
    'ancora': 'o **cavalo enfeitado das Cavalhadas** de Pirenópolis.',
    'chinelo': 'pé esquerdo com o galho de pequi, frutos e flores de papel; pé direito com a cabeça do cavalo enfeitado de fita azul e vermelha.',
    'fundo': 'azul do céu do cerrado; tira azul-cristão.',
    'ilustracao': 'o cavalo enfeitado de frente, no centro, com a Matriz de Pirenópolis ao fundo e os pequizeiros emoldurando.',
}

COR = {  # fundo da estampa, depois as cores de apoio (tiradas dos briefings de cada arte)
    'mg': ['#F2ECE0', '#D6A13D', '#2D5686', '#7C2420', '#D98A8E'],
    'rj': ['#E7B9A8', '#F2C230', '#8C2F1F', '#4F7A3A', '#E08A3C'],
    'ba': ['#6FA8EE', '#E8BE48', '#C2303A', '#6B1F18', '#F4F0E2'],
    'pe': ['#F3E3C6', '#F2B705', '#D7262E', '#1E8A4C', '#1F4FA0'],
    'ce': ['#F2C14E', '#D2372B', '#F08A24', '#3E7A3A', '#FBF6EA'],
    'ma': ['#1E2A4A', '#E0402F', '#F4C63D', '#2E9A5B', '#E46F9C'],
    'am': ['#2A1E17', '#C08A4E', '#E9A1A8', '#4F8A3C', '#F6EFE3'],
    'pa': ['#4B1F3F', '#D93A2E', '#F2C53D', '#2E9A55', '#2F6DB5'],
    'to': ['#C9652E', '#E8B83A', '#2F5E3A', '#7A2E1C', '#39B5B0'],
    'ms': ['#1FA3A8', '#D9963A', '#1C1714', '#C8302B', '#A99AD8'],
    'go': ['#5FA3CF', '#EDC64A', '#B8283C', '#2B3F8F', '#E2729C'],
    'pr': ['#C7D3CB', '#24452F', '#2C63C6', '#8A4A2B', '#B98A4E'],
    'sc': ['#BFD8E3', '#1F4E6E', '#3A4249', '#E8DFCC', '#C49A5A'],
    'rs': ['#D4A23C', '#7A4526', '#4E8A2E', '#B7322A', '#C9C6BE'],
}
LEGENDA = {
    'mg': ['Igreja das Mercês entre os casarões, Ouro Preto', 'Rua de Tiradentes', 'Casario da Rua Geraldo Resende, Tiradentes'],
    'rj': ['O bonde amarelo em Santa Teresa', 'O bondinho subindo a ladeira', 'O bonde nos trilhos de Santa Teresa'],
    'ba': ['Largo do Pelourinho, Salvador', 'Fitas do Senhor do Bonfim', 'Amêndoas de cacau secando'],
    'pe': ['Passistas de frevo em Olinda', 'Caboclos de lança', 'Bonecos gigantes nas ladeiras de Olinda'],
    'ce': ['Jangadas na areia', 'Cajueiral em Pacajus', 'Falésias de Canoa Quebrada'],
    'ma': ['Lagoa Bonita, Lençóis Maranhenses', 'Revoada de guarás', 'Boi do bumba-meu-boi em São Luís'],
    'am': ['Encontro das Águas, Manaus', 'Boto-cor-de-rosa', 'Vitória-régia em Manaus'],
    'pa': ['Mercado do Ver-o-Peso, Belém', 'Barquinhos de miriti', 'Paneiros de açaí no cais'],
    'to': ['Dunas do Jalapão', 'Fervedouro no Jalapão', 'Rio entre as dunas do Jalapão'],
    'ms': ['Rio cristalino em Bonito', 'Aguapés no rio Salobra', 'Gruta do Lago Azul, Bonito'],
    'go': ['Cavalhadas de Pirenópolis', 'Rua de Pirenópolis em dia de festa', 'Pequi aberto'],
    'pr': ['Araucárias nos Campos Gerais', 'Araucária na neblina'],
    'sc': ['APA da Baleia Franca, litoral sul', 'Costão na APA da Baleia Franca'],
    'rs': ['Cuia de chimarrão', 'Fim de tarde no pampa, Pelotas', 'Chimarrão perto do fogo'],
}
REGIAO = {'mg': 'Sudeste', 'rj': 'Sudeste', 'ba': 'Nordeste', 'pe': 'Nordeste', 'ce': 'Nordeste', 'ma': 'Nordeste',
          'am': 'Norte', 'pa': 'Norte', 'to': 'Norte', 'ms': 'Centro-Oeste', 'go': 'Centro-Oeste', 'pr': 'Sul', 'sc': 'Sul', 'rs': 'Sul'}


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


SETA = ('<svg class="seta" viewBox="0 0 120 60" aria-hidden="true"><path d="M114 8 C 86 4, 52 10, 30 34 C 24 40, 20 46, 16 52" '
        'fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/><path d="M8 40 L16 53 L29 47" fill="none" '
        'stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
ROT = (-2.2, 1.8, -1.2, 2.6, -1.6, 1.2)


def capitulo(i, s):
    uf = s['uf']
    t = V[uf]
    c = COR[uf]
    cad = T[uf]
    escuro = lum(c[0]) < 0.32
    ink = '#FFFBF4' if escuro else '#1D1915'
    sub = 'rgba(255,251,244,.74)' if escuro else 'rgba(29,25,21,.66)'
    lay = 'a' if i % 2 else 'b'
    fotos = ''.join(
        f'<figure class="foto f{k + 1}"><img src="img/{e(f["img"])}" alt="{e(LEGENDA[uf][k])}" loading="lazy">'
        f'<figcaption>{e(LEGENDA[uf][k])}<span>foto: {e(autor(f["autor"]))} · {e(f["licenca"])}</span></figcaption></figure>'
        for k, f in enumerate(s['campo']))
    palavras = ''.join(f'<li style="--r:{(-4, 3, -2, 5, -3, 2, -5, 4)[k % 8]}deg">{e(w)}</li>' for k, w in enumerate(cad['palavras'][:6]))
    evitar = ''.join(f'<li>{md(x)}</li>' for x in (EVITAR_EXTRA.get(uf, []) + list(cad['evitar']))[:3])
    sw = ''.join(f'<span class="sw" style="background:{x}"></span>' for x in c)
    par = [('est', s['estudio'], 'estúdio')] + [('lug', x, 'no lugar') for x in s['lugar'][:1]]
    if s.get('campanha'):
        par.append(('camp', s['campanha'], 'campanha'))
    par += [('lug', x, 'no lugar') for x in s['lugar'][1:2]]
    fotos_par = ''.join(
        f'<figure class="p-{tipo}" style="--r:{ROT[k]}deg;--y:{(0, 38, -10, 26)[k % 4]}px"><img src="img/{e(src)}" alt="O par de {e(s["nome"])}, {rot}" loading="lazy"><figcaption>{rot}</figcaption></figure>'
        for k, (tipo, src, rot) in enumerate(par))
    if s.get('video'):
        ilu = (f'<video src="img/{e(s["video"])}" poster="img/{e(s["ilu"])}" muted loop playsinline preload="none" '
               f'aria-label="Ilustração animada de {e(s["nome"])}"></video>')
    else:
        ilu = f'<img src="img/{e(s["ilu"])}" alt="Ilustração de {e(s["nome"])}" loading="lazy">'
    return f"""
<section class="cap lay-{lay}" id="{uf}" style="--bg:{c[0]};--ink:{ink};--sub:{sub};--ac:{c[1]}">
  <div class="wrap">
    <header class="cap-h">
      <p class="eyebrow">{i:02d} · {REGIAO[uf]}</p>
      <h2>{e(s["nome"])}</h2>
      <p class="estampa">{e(t["nome"])}</p>
      <p class="lead">{e(t["conceito"])}</p>
    </header>
  </div>
  <div class="nomao" aria-hidden="true"><span>{e(s["nome"])} · {e(t["nome"])} · {e(s["nome"])} · {e(t["nome"])} ·</span></div>
  <div class="wrap">

    <div class="colagem">
      <figure class="pc ilu">{ilu}</figure>
      <figure class="pc palm"><img src="img/{e(s["palmilha"])}" alt="Arte da palmilha de {e(s["nome"])}, em díptico" loading="lazy"></figure>
      {fotos}
      <div class="cor">
        <img src="img/{e(s["coracao"])}" alt="Detalhe do coração escondido na ilustração de {e(s["nome"])}" loading="lazy">
        <p class="mao">{e(s["coracao_texto"])}</p>
        {SETA}
      </div>
      <div class="cron"><p class="rot">caderno de campo</p><p>{md(cad["cronica"])}</p><p class="trilha"><span>trilha</span>{md(cad["trilha"])}</p></div>
      <ul class="palavras">{palavras}</ul>
      <p class="anc mao">âncora: {md(t["ancora"])}</p>
    </div>

    <div class="par">{fotos_par}</div>

    <div class="notas-cap">
      <div class="post"><h3 class="mao">no chinelo</h3><p>{md(t["chinelo"])}</p><p class="tira">{md(t["fundo"])}</p><div class="paleta">{sw}</div></div>
      <div class="post"><h3 class="mao">na ilustração</h3><p>{md(t["ilustracao"])}</p></div>
      <div class="post"><h3 class="mao">o que a gente evitou</h3><ul>{evitar}</ul></div>
    </div>
  </div>
</section>"""


HERO = [(1, 3, -6, 12), (13.5, -1, 4, 11), (23.5, 3, -3, 9.5), (66.5, -3, 5, 10.5), (76, 6, -4, 12), (89, 1, 6, 10.5),
        (0, 56, 5, 12), (13, 64, -5, 11), (26, 72, 3, 10), (64, 70, -4, 10), (76, 58, 5, 12), (89, 64, -6, 10.5),
        (40, 80, 2, 9), (51, 82, -3, 9)]
PROF = (1.3, .7, 1.0, .8, 1.4, .6, 1.2, .9, .5, .8, 1.3, .7, .6, 1.1)
hero = ''.join(
    f'<img src="img/{e(s["ilu_sem"])}" alt="" style="left:{x}%;top:{y}%;width:{w}%;--r:{r}deg" data-d="{d}" loading="eager">'
    for s, (x, y, r, w), d in zip(data, HERO, PROF))

def quadro(s):
    midia = (f'<video src="img/{e(s["video"])}" poster="img/{e(s["ilu_sem"])}" muted playsinline preload="none"></video>'
             if s.get('video') else f'<img src="img/{e(s["ilu_sem"])}" alt="" loading="lazy">')
    return (f'<figure class="quadro" data-uf="{s["uf"].upper()}" data-nome="{e(s["nome"])}" data-est="{e(V[s["uf"]]["nome"])}" '
            f'style="--ac:{COR[s["uf"]][1]}">{midia}</figure>')

reel = ''.join(quadro(s) for s in data)

def palavras_linha(ini):
    return ''.join(f'<span>{e(w)}<sup>{s["uf"].upper()}</sup></span><i>♥</i>'
                   for s in data for w in T[s['uf']]['palavras'][ini:ini + 2])

pal1, pal2 = palavras_linha(0), palavras_linha(2)

nav = ''.join(f'<a href="#{s["uf"]}" style="--c:{COR[s["uf"]][0]}">{s["uf"].upper()}</a>' for s in data)
caps = ''.join(capitulo(i + 1, s) for i, s in enumerate(data))
campo_leg = {s['uf']: LEGENDA[s['uf']] for s in data}
coracoes = ''.join(
    f'<figure><img src="img/{e(s["coracao"])}" alt="Coração de {e(s["nome"])}" loading="lazy"><figcaption><b>{e(s["nome"])}</b>{e(s["coracao_texto"])}</figcaption></figure>'
    for s in data)
colecao = ''.join(
    f'<a class="carta" href="#{s["uf"]}" style="--c:{COR[s["uf"]][0]};--r:{ROT[i % 6]}deg">'
    f'<span class="num">{i + 1:02d}</span>'
    f'<span class="im"><img class="a" src="img/{e(s["estudio"])}" alt="Par de {e(s["nome"])} no estúdio" loading="lazy">'
    + (f'<img class="b" src="img/{e(s["campanha"])}" alt="" loading="lazy">' if s.get('campanha') else '') +
    f'</span><strong>{e(s["nome"])}</strong><em>{e(V[s["uf"]]["nome"])}</em></a>'
    for i, s in enumerate(data))
creditos = ''.join(
    f'<li><b>{e(s["nome"])}</b> · ' + '; '.join(
        f'{e(campo_leg[s["uf"]][k])}: {e(autor(f["autor"]))}, {e(f["licenca"])}' + (f' (<a href="{e(f["pagina"])}">fonte</a>)' if f.get('pagina') else '')
        for k, f in enumerate(s['campo'])) + '</li>' for s in data)
mural = ''.join(
    f'<figure class="foto" style="--r:{(-2, 1.5, -1, 2, -1.5, 1, -2.5)[k % 7]}deg"><img src="img/{e(s["campo"][0]["img"])}" alt="{e(LEGENDA[s["uf"]][0])}" loading="lazy"><figcaption>{e(s["nome"])}</figcaption></figure>'
    for k, s in enumerate(data))
faixa = ''.join(f'<img src="img/{e(s["palmilha"])}" alt="" loading="lazy">' for s in data)

doc = open(P + '/_ferramentas/site_modelo.html', encoding='utf8').read()
for k, v in {'{{NAV}}': nav, '{{CAPITULOS}}': caps, '{{CORACOES}}': coracoes, '{{COLECAO}}': colecao,
             '{{CREDITOS}}': creditos, '{{FAIXA}}': faixa, '{{MURAL}}': mural, '{{HERO}}': hero,
             '{{REEL}}': reel, '{{PALAVRAS1}}': pal1, '{{PALAVRAS2}}': pal2}.items():
    doc = doc.replace(k, v)
open(SITE + '/index.html', 'w', encoding='utf8').write(doc)
print('ok', len(doc) // 1024, 'KB')
