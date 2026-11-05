"""Site v4 (protótipo): editorial, poucas coisas por tela, a arte grande num arco.
Uso: cd /tmp && python3 -I /home/user/Dornizon-/farm-bem-querer/_ferramentas/gerar_v4.py
Lê os mesmos dados do gerar_site.py e grava 07-apresentacao/site/v4.html"""
import colorsys
import html
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(AQUI, 'gerar_site.py'), encoding='utf8').read().split('def e(s)')[0]
exec(compile(_src, 'gerar_site_dados', 'exec'))   # data, V, T, COR, LEGENDA, REGIAO, P, SITE


def e(s):
    return html.escape(s or '', quote=True)


def autor(a):
    return (a or '').split(' - ')[0].split(' from ')[0].strip()


def lum(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def acento(uf):
    """A cor mais viva da paleta do estado que ainda lê sobre o creme (contraste >= 3:1)."""
    cands = []
    for h in COR[uf]:
        L = lum(h)
        contraste = (0.86 + 0.05) / (L + 0.05)
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
        s = colorsys.rgb_to_hls(r, g, b)[2]
        if contraste >= 3:
            cands.append((s, h))
    if cands:
        return max(cands)[1]
    # nenhuma lê: escurece a primeira
    r, g, b = (int(COR[uf][0][i:i + 2], 16) / 255 for i in (1, 3, 5))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(hh, 0.32, min(1, ss + .1))
    return '#%02X%02X%02X' % (int(r * 255), int(g * 255), int(b * 255))


def cena(i, s):
    uf = s['uf']
    t = V[uf]
    lado = 'dir' if i % 2 else 'esq'
    fotos = ''.join(
        f'<figure><div class="moldura"><img src="img/{e(f["img"])}" alt="{e(LEGENDA[uf][k])}" loading="lazy"></div>'
        f'<figcaption>{e(LEGENDA[uf][k])}<span>foto: {e(autor(f["autor"]))} · {e(f["licenca"])}</span></figcaption></figure>'
        for k, f in enumerate(s['campo'][:3]))
    if s.get('campanha'):
        fotos += (f'<figure><div class="moldura"><img src="img/{e(s["campanha"])}" alt="O par de {e(s["nome"])} na campanha" loading="lazy"></div>'
                  f'<figcaption>O par no lugar<span>campanha</span></figcaption></figure>')
    return f'''
<section class="cena {lado}" id="{uf}" style="--ac:{acento(uf)}">
  <div class="cena-in">
    <div class="cena-txt">
      <p class="num"><b>{i:02d}</b> / 14 · {REGIAO[uf]}</p>
      <h2>{e(s["nome"])}</h2>
      <p class="est">{e(t["nome"])}</p>
      <p class="conc">{e(t["conceito"])}</p>
      <div class="cor-mini"><img src="img/{e(s["coracao"])}" alt="Detalhe do coração na ilustração" loading="lazy"><p><b>onde está o coração</b>{e(s["coracao_texto"])}</p></div>
    </div>
    <div class="cena-arte">
      <figure class="arco-ilu"><img src="img/{e(s["ilu"])}" alt="Ilustração de {e(s["nome"])}" loading="lazy"></figure>
      <img class="par-flutua" src="img/{uf}-par.webp" alt="O par de {e(s["nome"])}" loading="lazy">
    </div>
  </div>
  <div class="campo">{fotos}</div>
</section>'''


cenas = ''.join(cena(i + 1, s) for i, s in enumerate(data))
janela = ''.join(f'<img src="img/{e(s["ilu"])}" alt="" {"class=on " if k == 0 else ""}loading="eager">' for k, s in enumerate(data))
roda = ''.join(
    f'<a class="item" href="#{s["uf"]}" style="--i:{i}" data-n="{i + 1:02d}" data-nome="{e(s["nome"])}" data-est="{e(V[s["uf"]]["nome"])}" data-uf="{s["uf"]}">'
    f'<img src="img/{s["uf"]}-par.webp" alt="Par de {e(s["nome"])}" loading="lazy"></a>' for i, s in enumerate(data))
menu = ''.join(f'<li><a href="#{s["uf"]}"><span>{i + 1:02d}</span>{e(s["nome"])}</a></li>' for i, s in enumerate(data))
creditos = ''.join(
    f'<li><b>{e(s["nome"])}</b> · ' + '; '.join(
        f'{e(LEGENDA[s["uf"]][k])}: {e(autor(f["autor"]))}, {e(f["licenca"])}' + (f' (<a href="{e(f["pagina"])}">fonte</a>)' if f.get('pagina') else '')
        for k, f in enumerate(s['campo'])) + '</li>' for s in data)
_s = open(P + '/03-marca/identidade-bem-querer/simbolo-cor.svg', encoding='utf8').read()
simb = _s[_s.index('>') + 1:_s.rindex('</svg>')]
por = {s['uf']: s for s in data}

doc = open(os.path.join(AQUI, 'site_v4_modelo.html'), encoding='utf8').read()
for k, v in {'{{CENAS}}': cenas, '{{JANELA}}': janela, '{{RODA}}': roda, '{{MENU}}': menu, '{{CREDITOS}}': creditos, '{{SIMB}}': simb,
             '{{IMG_RJ}}': 'img/' + por['rj']['campo'][0]['img'], '{{IMG_MS}}': 'img/ms-par.webp', '{{IMG_COR}}': 'img/' + por['sc']['coracao']}.items():
    doc = doc.replace(k, v)
assert '{{' not in doc, re.findall(r'\{\{\w+\}\}', doc)
open(SITE + '/v4.html', 'w', encoding='utf8').write(doc)
print('ok v4', len(doc) // 1024, 'KB', {s['uf']: acento(s['uf']) for s in data})
