"""Caderno de campo de um estado (A4 paisagem): abertura, painel de fotos reais, do campo para a estampa.
Uso: python caderno.py estado.json fotos_dir saida.html"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, 'caderno.css'), encoding='utf8').read()


def e(t):
    return html.escape(t or '', quote=False)


def md(t):
    t = e(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'_(.+?)_', r'<em>\1</em>', t)
    return t


def contraste(hexc):
    h = hexc.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return '#1E1A17' if (0.299 * r + 0.587 * g + 0.114 * b) > 145 else '#FFFFFF'


def autor_limpo(a):
    a = re.sub(r'\[?https?://\S+', '', a or '')
    a = re.sub(r'[\[\]]', '', a).strip(' -·|')
    return a or 'autor no Wikimedia Commons'


def credito(c):
    lic = f' · {e(c["licenca"])}' if c.get('licenca') else ''
    nc = ' (uso não comercial)' if c.get('nc') else ''
    fonte = {'flickr': 'Flickr', 'wikimedia': 'Wikimedia Commons'}.get(c.get('fonte'), 'Wikimedia Commons')
    return f'{e(autor_limpo(c["autor"]))}{lic}{nc} · {fonte}'


def build(cfg, fotos_rel, creditos):
    nome = cfg['nome']
    n = cfg['numero']
    rod = lambda s, cl='': f'<div class="rod {cl}"><span>caderno de campo · {e(nome)}</span><span>havaianas ♥ farm rio · bem-querer · {s}</span></div>'
    cred = {c['arquivo']: c for lista in creditos.values() for c in lista}
    PEND = {'autor': '(crédito em verificação)', 'licenca': ''}
    cred_get = lambda a: cred.get(a, PEND)

    def img(arq):
        return f'{fotos_rel}/{arq}'

    # 1. abertura
    hero = cfg['hero']
    pal = ''.join(
        f'<div style="background:{p["estampa"]};color:{contraste(p["estampa"])};flex-direction:column;align-items:stretch;justify-content:flex-end;padding:0">'
        f'<span style="padding:1.2mm">{e(p["nome"])}<br>{p["estampa"]}</span>'
        f'<span style="background:{p["foto"]};color:{contraste(p["foto"])};padding:.8mm 1.2mm;font-size:5.2pt">na foto {p["foto"]}</span></div>'
        for p in cfg['paleta'])
    chips = ''.join(f'<span>{e(p)}</span>' for p in cfg['palavras'])
    p1 = f'''<section class="pg"><div class="abertura">
      <div class="foto"><img src="{img(hero)}" style="object-position:{cfg.get('hero_pos', '50% 50%')}"><div class="credito">{e(cfg["hero_legenda"])} — {credito(cred_get(hero))}</div></div>
      <div class="texto">
        <div class="kicker">caderno de campo · {e(n)} · {e(cfg["regiao"])}</div>
        <h1>{e(nome)}</h1>
        <div class="cronica">{md(cfg["cronica"])}</div>
        <h3>palavras do lugar</h3><div class="chips">{chips}</div>
        <h3 style="margin-top:3mm">trilha de campo</h3><p style="font-size:8.6pt">{md(cfg["trilha"])}</p>
        <div style="margin-top:auto"><h3>paleta tirada das fotos</h3><div class="paleta">{pal}</div></div>
      </div></div>{rod("abertura", "direita")}</section>'''

    # 2. painel
    figs = ''
    for item in cfg['painel']:
        arq, cat, leg, cls = item[:4]
        pos = item[4] if len(item) > 4 else '50% 50%'
        c = cred_get(arq)
        figs += (f'<figure class="{cls}"><img src="{img(arq)}" style="object-position:{pos}"><figcaption><b>{e(cat)}</b>{e(leg)}'
                 f'<br><span style="opacity:.75;font-size:5.4pt">{credito(c)}</span></figcaption></figure>')
    p2 = f'''<section class="pg"><div class="painel">
      <div class="kicker">o que a gente viu</div><h2>{e(cfg["painel_titulo"])}</h2>
      <div class="grade">{figs}</div></div>{rod("painel")}</section>'''

    # 3. do campo para a estampa
    mot = ''.join(f'<div class="motivo"><img src="{img(a)}"><p><strong>{e(t)}</strong> — {md(d)}</p></div>' for a, t, d in cfg['motivos'])
    evit = ''.join(f'<li>{md(x)}</li>' for x in cfg['evitar'])
    est = cfg['estampa']
    tres = ''.join(f'<div><b>{lbl}</b>{md(t)}</div>' for lbl, t in zip(('macro', 'médio', 'micro'), est['coracoes']))
    p3 = f'''<section class="pg"><div class="do-campo">
      <div><div class="kicker">do campo para a estampa</div><h2>O que a gente puxou</h2>{mot}
        <h3 style="margin-top:4mm">o que a gente evitou</h3><ul class="evitar">{evit}</ul></div>
      <div><div class="caixa"><div class="kicker">estampa {e(n)}</div><h2 style="margin-bottom:2mm">{e(est["nome"])}</h2>
        <p>{md(est["conceito"])}</p>
        <p><strong>Protagonista:</strong> {md(est["protagonista"])}<br><strong>Em volta:</strong> {md(est["coadjuvantes"])}<br>
        <strong>Fundo:</strong> {md(est["fundo"])}{('<br><strong>Decorações:</strong> ' + md(est["decoracao"])) if est.get("decoracao") else ''}</p>
        {('<p class="kicker" style="margin:2mm 0 0">bicho-guia · ' + e(cfg["bicho"]) + '</p>') if cfg.get("bicho") else ''}</div>
        <h3>onde o coração mora</h3><div class="tres">{tres}</div>
        <h3 style="margin-top:4mm">peças</h3><p>{md(est["pecas"])}</p>
        <h3>crédito e cuidado</h3><p style="font-size:8.4pt">{md(est["cuidado"])}</p>
        <p class="credito" style="margin-top:3mm">{md(est["fontes"])}</p>
      </div></div>{rod("do campo para a estampa")}</section>'''
    return p1 + p2 + p3


if __name__ == '__main__':
    cfg = json.load(open(sys.argv[1], encoding='utf8'))
    fotos_dir = sys.argv[2]
    out = sys.argv[3]
    creditos = {}
    for _f in sorted(os.listdir(fotos_dir)):
        if _f.startswith("creditos") and _f.endswith(".json"):
            _d = json.load(open(os.path.join(fotos_dir, _f), encoding="utf8"))
            creditos.update(_d if "fotos" not in _d else {"fotos": _d["fotos"]})
    rel = os.path.relpath(fotos_dir, os.path.dirname(out))
    corpo = build(cfg, rel, creditos)
    doc = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
           f'<title>Caderno de campo — {e(cfg["nome"])}</title><style>{CSS}</style></head><body>{corpo}</body></html>')
    open(out, 'w', encoding='utf8').write(doc)
    print('ok', out)
