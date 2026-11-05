"""Monta a tese (HTML) da colecao conceitual Bem-Querer — havaianas ♥ FARM Rio V2.
Conteudo de contexto e estados vem de conteudo.json; logos sao lidos dos SVGs gerados."""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = '/home/user/Dornizon-/farm-bem-querer'
C = json.load(open(os.path.join(HERE, 'conteudo.json'), encoding='utf8'))
EST = {e['uf']: e for e in json.load(open(os.path.join(HERE, 'estados.json'), encoding='utf8'))}
CSS = open(os.path.join(HERE, 'tese_base.css'), encoding='utf8').read()

TOTAL = []


def inline_svg(path, width=None, style=''):
    s = open(path, encoding='utf8').read()
    w = f'width="{width}"' if width else 'width="100%"'
    s = re.sub(r'width="[\d.]+" height="[\d.]+"', f'{w} style="{style}"', s, count=1)
    # ids unicos por insercao (filtros)
    n = len(TOTAL)
    TOTAL.append(1)
    s = s.replace('id="tinta"', f'id="tinta{n}"').replace('url(#tinta)', f'url(#tinta{n})')
    s = re.sub(r'id="(f[ih][0-9A-Fa-f]{6})"', lambda m: f'id="{m.group(1)}_{n}"', s)
    s = re.sub(r'url\(#(f[ih][0-9A-Fa-f]{6})\)', lambda m: f'url(#{m.group(1)}_{n})', s)
    return s


def e(t):
    return html.escape(t, quote=False)


def md(t):
    """negrito **x** e links [a](b) simples."""
    t = e(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\[(.+?)\]\((https?://[^)]+)\)', r'<a href="\2">\1</a>', t)
    return t


def ul(items):
    return '<ul>' + ''.join(f'<li>{md(i)}</li>' for i in items) + '</ul>'


PAG = [0]


def pagina(conteudo, classe='', secao=''):
    PAG[0] += 1
    rod = (f'<div class="rodape"><span>bem-querer · havaianas ♥ FARM Rio V2 · coleção conceitual de portfólio</span>'
           f'<span>{e(secao)} · {PAG[0]:02d}</span></div>')
    return f'<section class="pagina {classe}">{conteudo}{rod}</section>'


def contraste(hexc):
    h = hexc.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return '#2B1D16' if (0.299 * r + 0.587 * g + 0.114 * b) > 150 else '#FFFDF7'


def paleta(cores, nomes=None):
    out = '<div class="paleta">'
    for i, c in enumerate(cores):
        n = (nomes[i] + '<br>') if nomes and i < len(nomes) else ''
        out += f'<div style="background:{c};color:{contraste(c)}">{e(n) if not n else n}{c}</div>'
    return out + '</div>'


def fontes(lista):
    return '<p class="fonte">Fontes: ' + ' · '.join(f'<a href="{u}">{e(t)}</a>' for t, u in lista) + '</p>'


def build():
    P = []
    L = f'{PROJ}/logo'

    # CAPA
    P.append(pagina(f'''
      <div>
        <div class="kicker" style="color:#E8B04A">Tese de coleção conceitual · portfólio</div>
        <div style="width:150mm;margin-top:28mm">{inline_svg(f"{L}/capa-wordmark.svg")}</div>
        <p class="lead" style="margin-top:10mm;color:#EFE6D3">havaianas ♥ FARM Rio — V2<br>Drop 1: 14 estados, um coração escondido em cada estampa.</p>
      </div>
      <div style="width:120mm">{inline_svg(f"{L}/assinatura-v2/assinatura-mg-horizontal-claro.svg")}</div>
      <div>
        <p class="aviso">Autoria: ______________________ · Novembro de 2026</p>
        <p class="aviso">Projeto acadêmico/de portfólio, fictício e sem vínculo com FARM Rio, Havaianas, Azzas 2154 ou Alpargatas. As marcas citadas pertencem a seus titulares e aparecem apenas para ilustrar a proposta.</p>
      </div>''', 'capa', 'capa'))

    # SUMARIO
    itens = C['sumario']
    P.append(pagina('<div class="kicker">Sumário</div><h2>O caminho da defesa</h2><ol class="sumario">' +
                    ''.join(f'<li>{e(t)}<span>{e(d)}</span></li>' for t, d in itens) + '</ol>', '', 'sumário'))

    # TESE EM UMA PAGINA
    t = C['tese']
    P.append(pagina(f'''<div class="kicker">01 · A tese em uma página</div><h2>{e(t["titulo"])}</h2>
      <blockquote>{md(t["frase"])}</blockquote>
      <div class="grid2">{"".join(f'<div class="caixa"><h4>{e(k)}</h4><p>{md(v)}</p></div>' for k, v in t["blocos"])}</div>
      <div class="grid3" style="margin-top:4mm">{"".join(f'<div><div class="num">{e(n)}</div><p>{e(d)}</p></div>' for n, d in t["numeros"])}</div>''',
                    '', 'a tese'))

    # CONTEXTO (paginas livres vindas do JSON)
    for sec in C['contexto']:
        corpo = f'<div class="kicker">{e(sec["kicker"])}</div><h2>{e(sec["titulo"])}</h2>'
        if sec.get('lead'):
            corpo += f'<p class="lead">{md(sec["lead"])}</p>'
        for bloco in sec['blocos']:
            if bloco['tipo'] == 'texto':
                corpo += ''.join(f'<p>{md(p)}</p>' for p in bloco['ps'])
            elif bloco['tipo'] == 'lista':
                corpo += (f'<h3>{e(bloco["titulo"])}</h3>' if bloco.get('titulo') else '') + ul(bloco['itens'])
            elif bloco['tipo'] == 'caixa':
                cl = 'caixa escura' if bloco.get('escura') else 'caixa'
                corpo += f'<div class="{cl}"><h4>{e(bloco["titulo"])}</h4>' + ''.join(f'<p>{md(p)}</p>' for p in bloco['ps']) + '</div>'
            elif bloco['tipo'] == 'tabela':
                corpo += '<table><tr>' + ''.join(f'<th>{e(h)}</th>' for h in bloco['cab']) + '</tr>' + ''.join(
                    '<tr>' + ''.join(f'<td>{md(c)}</td>' for c in linha) + '</tr>' for linha in bloco['linhas']) + '</table>'
            elif bloco['tipo'] == 'imagem':
                corpo += f'<figure style="margin:0 0 4mm"><img src="{bloco["src"]}" style="border-radius:2mm"><figcaption class="fonte">{md(bloco["legenda"])}</figcaption></figure>'
            elif bloco['tipo'] == 'html':
                corpo += bloco['html'].replace('{L}', L)
        if sec.get('fontes'):
            corpo += fontes(sec['fontes'])
        P.append(pagina(corpo, '', sec['rodape']))

    # ESTADOS
    for st in C['estados']:
        uf = st['uf']
        meta = EST[uf]
        icones = ''.join(f'<div class="icone"><b>{i + 1}</b><div><strong>{e(ic[0])}</strong> — {md(ic[1])}</div></div>'
                         for i, ic in enumerate(st['icones']))
        coracao = ''.join(f'<div><strong>{e(n)}</strong>{md(t)}</div>' for n, t in zip(('Macro', 'Médio', 'Micro'), st['coracao']))
        selo = inline_svg(f'{L}/selo-{uf.lower()}-tinta.svg')
        corpo = f'''<div class="estado-topo"><div>
            <div class="kicker">{e(meta["regiao"])} · estampa {e(st["numero"])}</div>
            <h2 style="margin-bottom:1mm">{e(meta["nome"])}</h2>
            <p class="lead" style="margin-bottom:2mm">“{e(st["estampa"])}” — {md(st["conceito"])}</p></div>
            <div>{selo}</div></div>
          <div class="grid2"><div>
            <h4>Teste do bater o olho — os ícones</h4>{icones}
            <h4>Por que é inconfundível</h4><p>{md(st["porque"])}</p>
          </div><div>
            <h4>Paleta nativa</h4>{paleta(st["paleta"], st.get("paleta_nomes"))}
            <h4>Composição</h4><p><strong>Protagonista:</strong> {md(st["protagonista"])}<br><strong>Coadjuvantes:</strong> {md(st["coadjuvantes"])}<br><strong>Fundo:</strong> {md(st["fundo"])}<br><strong>Recurso gráfico:</strong> {md(st["recurso"])}</p>
            <h4>Produto</h4><p>{md(st["produto"])}</p>
          </div></div>
          <h4>Onde o coração mora</h4><div class="coracao3">{coracao}</div>
          <div class="grid2" style="margin-top:3mm"><div><h4>Cuidado e crédito</h4><p style="font-size:9pt">{md(st["cuidado"])}</p></div>
          <div><h4>Reconhecimentos</h4><p style="font-size:9pt">{md(st["reconhecimentos"])}</p></div></div>
          {fontes(st["fontes"])}'''
        P.append(pagina(corpo, '', meta['nome'].lower()))

    # PAGINAS FINAIS
    for sec in C['final']:
        corpo = f'<div class="kicker">{e(sec["kicker"])}</div><h2>{e(sec["titulo"])}</h2>'
        if sec.get('lead'):
            corpo += f'<p class="lead">{md(sec["lead"])}</p>'
        for bloco in sec['blocos']:
            if bloco['tipo'] == 'texto':
                corpo += ''.join(f'<p>{md(p)}</p>' for p in bloco['ps'])
            elif bloco['tipo'] == 'lista':
                corpo += (f'<h3>{e(bloco["titulo"])}</h3>' if bloco.get('titulo') else '') + ul(bloco['itens'])
            elif bloco['tipo'] == 'caixa':
                cl = 'caixa escura' if bloco.get('escura') else 'caixa'
                corpo += f'<div class="{cl}"><h4>{e(bloco["titulo"])}</h4>' + ''.join(f'<p>{md(p)}</p>' for p in bloco['ps']) + '</div>'
            elif bloco['tipo'] == 'tabela':
                corpo += '<table><tr>' + ''.join(f'<th>{e(h)}</th>' for h in bloco['cab']) + '</tr>' + ''.join(
                    '<tr>' + ''.join(f'<td>{md(c)}</td>' for c in linha) + '</tr>' for linha in bloco['linhas']) + '</table>'
            elif bloco['tipo'] == 'html':
                h = bloco['html'].replace('{L}', L)
                h = re.sub(r'\{SVG:([^}]+)\}', lambda m: inline_svg(m.group(1).replace('{L}', L)), h)
                corpo += h
            elif bloco['tipo'] == 'selos':
                corpo += '<div class="mini-estados">' + ''.join(
                    f'<div>{inline_svg(f"{L}/selo-{u.lower()}-tinta.svg")}</div>' for u in bloco['ufs']) + '</div>'
        if sec.get('fontes'):
            corpo += fontes(sec['fontes'])
        P.append(pagina(corpo, '', sec['rodape']))

    doc = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bem-Querer — tese</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'''
    out = f'{PROJ}/tese-bem-querer.html'
    open(out, 'w', encoding='utf8').write(doc)
    print('ok', out, PAG[0], 'paginas')


if __name__ == '__main__':
    build()
