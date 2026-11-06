"""Monta o ebook diagramado (ebook.html) a partir das receitas de ../receitas.py.

    python3 build.py      # gera ebook.html e as imagens-guia das fotos
    node render.mjs       # gera ebook.pdf (A4) para importar no Canva

As áreas de foto são imagens-guia: no Canva, arraste a foto do prato em cima e ela substitui a guia.
"""

import html
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
import receitas as R  # noqa: E402

TITULO = "Prato Pequeno, Proteína Grande"
FONTE_GUIA = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"

CORES = {
    "salvia": "#8FA38A",
    "salvia_escura": "#566B50",
    "salvia_clara": "#E4E9DE",
    "creme": "#F4EEE3",
    "papel": "#FBF8F2",
    "terracota": "#C8693F",
    "grafite": "#2E2E2C",
    "cinza": "#66645F",
}

e = html.escape


# ------------------------------------------------------------------ imagens-guia das fotos
def guia(nome, largura, altura, titulo, sub):
    escala = 2
    w, h = largura * escala, altura * escala
    img = Image.new("RGB", (w, h), CORES["salvia_clara"])
    d = ImageDraw.Draw(img)
    cx, cy = w // 2, int(h * 0.44)
    r = int(min(w, h) * 0.20)
    linha = "#C3CDB8"
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=linha, width=6 * escala // 2)
    r2 = int(r * 0.66)
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=linha, width=4 * escala // 2)
    # garfo e faca
    gx = cx - r - int(r * 0.45)
    d.line([gx, cy - r * 0.9, gx, cy + r * 0.9], fill=linha, width=5 * escala // 2)
    for dx in (-14, 0, 14):
        d.line([gx + dx * escala // 2, cy - r * 0.9, gx + dx * escala // 2, cy - r * 0.45], fill=linha,
               width=4 * escala // 2)
    fx = cx + r + int(r * 0.45)
    d.line([fx, cy - r * 0.9, fx, cy + r * 0.9], fill=linha, width=5 * escala // 2)
    d.ellipse([fx - 10 * escala // 2, cy - r * 0.9, fx + 10 * escala // 2, cy - r * 0.1], outline=linha,
              width=4 * escala // 2)
    f1 = ImageFont.truetype(FONTE_GUIA, 22 * escala)
    f2 = ImageFont.truetype(FONTE_GUIA, 14 * escala)
    ty = cy + r + 28 * escala
    d.text((cx, ty), titulo, font=f1, fill=CORES["salvia_escura"], anchor="mt")
    d.text((cx, ty + 34 * escala), sub, font=f2, fill="#7D8C76", anchor="mt")
    img.save(AQUI / nome, optimize=True)


# ------------------------------------------------------------------ páginas
def pagina(classe, corpo, numero=None):
    rodape = f'<p class="folio">{numero}</p>' if numero else ""
    return f'<section class="page {classe}">{corpo}{rodape}</section>'


def tempo_partes(tempo):
    if " + " in tempo:
        principal, extra = tempo.split(" + ", 1)
        return principal, "+ " + extra
    if " (" in tempo:
        principal, extra = tempo.split(" (", 1)
        return principal, extra.rstrip(")")
    return tempo, "de preparo"


def capa():
    return pagina("capa", f"""
      <p class="sobre-titulo">Ebook de receitas</p>
      <h1>Prato Pequeno,<br><em>Proteína Grande</em></h1>
      <p class="sub">40 receitas proteicas em porção pequena, sem complicação</p>
      <p class="autora">por <strong>Bia</strong></p>
      <img class="foto-capa" src="guia-capa.png" alt="Foto da capa">
      <div class="selo"><strong>40</strong><span>receitas</span></div>
    """)


def antes():
    return pagina("texto", f"""
      <p class="kicker">Antes de começar</p>
      <h2>Receitas, não um plano alimentar</h2>
      <p>Este ebook traz receitas. Ele não substitui consulta com nutricionista ou médico.</p>
      <p>Se você usa medicação para emagrecer, tem diabetes, doença renal ou outra condição de saúde, está
      grávida ou amamentando, siga a orientação do seu profissional de saúde sobre quanto e o que comer.</p>
      <p>Confira alergias e intolerâncias: as receitas usam ovo, leite e derivados, amendoim, peixe, frutos do
      mar e aveia (que pode conter glúten).</p>
      <div class="bloco-bia">
        <p class="kicker">Quem é a Bia</p>
        <p>A Bia é uma personagem criada com inteligência artificial para o perfil
        <span class="preencher">[@perfil]</span>. Ela cozinha prático, com ingrediente de mercado comum, e
        acredita que comida boa não precisa de frescura.</p>
        <p>As receitas foram desenvolvidas por <span class="preencher">[autor]</span> e revisadas por
        <span class="preencher">[nome da nutricionista], CRN [número]</span>.</p>
      </div>
    """, 2)


def como_usar(com_frango):
    return pagina("texto", f"""
      <p class="kicker">Como usar este ebook</p>
      <h2>Cada garfada precisa valer mais</h2>
      <p class="lead">Quando a gente come menos, a proteína faz falta. Por isso todas as receitas daqui são
      <strong>porções pequenas com bastante proteína</strong>, feitas com coisas que você acha em qualquer
      mercado.</p>
      <div class="legenda">
        <div><b>22 g</b><span>proteína por porção</span></div>
        <div><b>260</b><span>kcal por porção</span></div>
        <div><b>4 min</b><span>do primeiro passo ao prato</span></div>
        <div><b>1</b><span>quantas porções rende</span></div>
      </div>
      <p class="nota">Proteína e calorias são aproximadas e mudam com a marca e o tamanho dos ingredientes.
      Sal, alho, ervas, limão e especiarias não entram na conta. Colher de sopa de aveia ou de leite em pó:
      cerca de 10 g. Xícara: 240 ml.</p>
      <h3 class="titulo-dicas">Três coisas que deixam a semana mais fácil</h3>
      <div class="dicas">
        <div class="card"><b>1</b><h4>Frango desfiado pronto</h4><p>Cozinhe 1 kg de peito no domingo, desfie
        e guarde em potes. Ele aparece em {com_frango} receitas.</p></div>
        <div class="card"><b>2</b><h4>Ovos cozidos</h4><p>Cozidos e com casca, duram até 1 semana na
        geladeira.</p></div>
        <div class="card"><b>3</b><h4>Leite em pó desnatado</h4><p>O truque mais barato para pôr proteína em
        doce, mingau e vitamina.</p></div>
      </div>
    """, 3)


def despensa(usados):
    grupos = []
    ordem = ["Proteínas", "Laticínios", "Grãos e farinhas", "Despensa", "Hortifrúti"]
    for grupo in ordem:
        nomes = []
        for c in R.GRUPOS_DESPENSA[grupo]:
            if c in usados and R.NOME_DESPENSA[c] not in nomes:
                nomes.append(R.NOME_DESPENSA[c])
        itens = "<br>".join(e(n) for n in nomes)
        classe = "grupo largo" if grupo == "Hortifrúti" else "grupo"
        grupos.append(f'<div class="{classe}"><h4>{e(grupo)}</h4><p>{itens}</p></div>')
    return pagina("texto", f"""
      <p class="kicker">Despensa básica</p>
      <h2>Tudo o que aparece nas 40 receitas</h2>
      <p class="lead">Fora os temperos. Com isso na geladeira e no armário, você faz o ebook inteiro.</p>
      <div class="despensa">{''.join(grupos)}</div>
    """, 4)


def sumario(paginas):
    blocos = []
    for cap, titulo in R.CAPITULOS.items():
        linhas = "".join(
            f'<p><span>{r["numero"]}. {e(r["nome"])}</span><span class="pg">{paginas[r["numero"]]}</span></p>'
            for r in R.RECEITAS if r["cap"] == cap)
        blocos.append(f'<div class="cap"><h4>{e(titulo)}</h4>{linhas}</div>')
    return pagina("texto sumario", f"""
      <p class="kicker">Sumário</p>
      <h2>40 receitas</h2>
      <div class="indice">{''.join(blocos)}</div>
    """, 5)


def abertura(n, cap, titulo, numero_pagina, paginas):
    lista = [r for r in R.RECEITAS if r["cap"] == cap]
    nomes = "<br>".join(f'{r["numero"]}. {e(r["nome"])}' for r in lista)
    return pagina("abertura", f"""
      <p class="cap-num">0{n}</p>
      <h2>{e(titulo)}</h2>
      <p class="cap-qtd">{len(lista)} receitas · páginas {paginas[lista[0]["numero"]]} a {paginas[lista[-1]["numero"]]}</p>
      <p class="cap-lista">{nomes}</p>
    """, numero_pagina)


def receita(r, numero_pagina):
    principal, extra = tempo_partes(r["tempo"])
    porcoes = "porção" if r["porcoes"] == 1 else "porções"
    ingredientes = "".join(f'<li><span class="m">•</span>{e(txt)}</li>' for _, _, txt in r["ingredientes"])
    if r["temperos"]:
        ingredientes += f'<li class="temperos"><span class="m"></span>{e(r["temperos"])}</li>'
    passos = "".join(f'<p><b>{i}</b>{e(p)}</p>' for i, p in enumerate(r["passos"], 1))
    extras = ""
    if r["dica"]:
        extras += f'<div class="dica"><h4>Dica da Bia</h4><p>{e(r["dica"])}</p></div>'
    if r["congela"]:
        extras += f'<div class="dica congela"><h4>Congela</h4><p>{e(r["congela"])}</p></div>'
    return pagina("receita", f"""
      <img class="foto" src="guia-receita.png" alt="Foto: {e(r['nome'])}">
      <div class="conteudo">
        <p class="kicker">{e(R.CAPITULOS[r['cap']])} · {r['numero']:02d}</p>
        <h2>{e(r['nome'])}</h2>
        <div class="stats">
          <div class="destaque"><b>{r['prot']} g</b><span>proteína</span></div>
          <div><b>{r['kcal']}</b><span>kcal</span></div>
          <div><b>{e(principal)}</b><span>{e(extra)}</span></div>
          <div><b>{r['porcoes']}</b><span>{porcoes}</span></div>
        </div>
        <div class="colunas">
          <div class="ingredientes"><h3>Ingredientes</h3><ul>{ingredientes}</ul></div>
          <div class="preparo"><h3>Modo de preparo</h3>{passos}</div>
        </div>
        {extras}
      </div>
    """, numero_pagina)


def top10(paginas, numero_pagina):
    linhas = "".join(
        f'<p><span>{e(r["nome"])}</span><span class="v">{r["prot"]} g</span><span class="k">{r["kcal"]} kcal</span>'
        f'<span class="pg">p. {paginas[r["numero"]]}</span></p>'
        for r in sorted(R.RECEITAS, key=lambda r: -r["prot"])[:10])
    rapidas = [r for r in R.RECEITAS
               if r["tempo"].split()[0].isdigit() and int(r["tempo"].split()[0]) <= 15 and "+" not in r["tempo"]]
    lista_rapidas = ", ".join(f'{e(r["nome"])} ({paginas[r["numero"]]})' for r in rapidas)
    return pagina("texto", f"""
      <p class="kicker">Atalhos</p>
      <h2>As 10 com mais proteína</h2>
      <div class="ranking">{linhas}</div>
      <h3 class="titulo-dicas">Prontas em até 15 minutos</h3>
      <p class="rapidas">{lista_rapidas}.</p>
    """, numero_pagina)


def fecho(numero_pagina):
    return pagina("fecho", """
      <h2>Fez?<br><em>Me mostra!</em></h2>
      <p>Tira uma foto do seu prato e marca <span class="preencher-claro">[@perfil]</span> nos stories.
      Eu reposto as minhas favoritas.</p>
      <p class="assina">Com carinho,<br><strong>Bia</strong></p>
      <p class="rodape-ia">A Bia é uma personagem criada com inteligência artificial.</p>
    """, numero_pagina)


# ------------------------------------------------------------------ montagem
def montar():
    for r in R.RECEITAS:
        r["prot"], r["kcal"] = R.nutricao(r)

    # numeração das receitas e das páginas
    paginas = {}
    p = 5  # capa, antes, como usar, despensa, sumário
    n = 0
    plano = []
    for i, (cap, titulo) in enumerate(R.CAPITULOS.items(), 1):
        p += 1
        plano.append(("abertura", i, cap, titulo, p))
        for r in [r for r in R.RECEITAS if r["cap"] == cap]:
            n += 1
            p += 1
            r["numero"] = n
            paginas[n] = p
            plano.append(("receita", r, p))
    p_top10, p_fecho = p + 1, p + 2

    usados = {a for r in R.RECEITAS for a, _, _ in r["ingredientes"]}
    com_frango = sum(any(a == "frango_cozido" for a, _, _ in r["ingredientes"]) for r in R.RECEITAS)

    corpo = [capa(), antes(), como_usar(com_frango), despensa(usados), sumario(paginas)]
    for item in plano:
        if item[0] == "abertura":
            _, i, cap, titulo, pg = item
            corpo.append(abertura(i, cap, titulo, pg, paginas))
        else:
            _, r, pg = item
            corpo.append(receita(r, pg))
    corpo.append(top10(paginas, p_top10))
    corpo.append(fecho(p_fecho))

    css = (AQUI / "ebook.css").read_text(encoding="utf-8")
    doc = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{TITULO}</title>
<style>{css}</style>
</head>
<body>
{''.join(corpo)}
</body>
</html>"""
    (AQUI / "ebook.html").write_text(doc, encoding="utf-8")

    guia("guia-receita.png", 794, 400, "foto do prato", "arraste a foto aqui no Canva")
    guia("guia-capa.png", 794, 520, "foto da capa", "a Bia com o prato, ou o prato sozinho")
    print(f"ebook.html: {len(corpo)} páginas")


if __name__ == "__main__":
    montar()
