"""Prepara as imagens do site de apresentação (tamanho de web) e o data.json com paleta e créditos.
Uso: python site_assets.py <scratchpad>"""
import glob, json, os, sys
import numpy as np
from PIL import Image, ImageOps

S = sys.argv[1]
P = '/home/user/Dornizon-/farm-bem-querer'
E = P + '/05-estampas'
OUT = P + '/07-apresentacao/site/img'
os.makedirs(OUT, exist_ok=True)

EST = [('mg', '01-minas-gerais', 'Minas Gerais'), ('rj', '02-rio-de-janeiro', 'Rio de Janeiro'), ('ba', '03-bahia', 'Bahia'),
       ('pe', '04-pernambuco', 'Pernambuco'), ('ce', '05-ceara', 'Ceará'), ('ma', '06-maranhao', 'Maranhão'),
       ('am', '07-amazonas', 'Amazonas'), ('pa', '08-para', 'Pará'), ('to', '09-tocantins', 'Tocantins'),
       ('ms', '10-mato-grosso-do-sul', 'Mato Grosso do Sul'), ('go', '11-goias', 'Goiás'), ('pr', '12-parana', 'Paraná'),
       ('sc', '13-santa-catarina', 'Santa Catarina'), ('rs', '14-rio-grande-do-sul', 'Rio Grande do Sul')]
CAMP = {'mg': 'janela', 'rj': 'escadaria', 'ba': 'pelourinho', 'pe': 'olinda', 'ce': 'renda', 'ma': 'lencois', 'am': 'barco',
        'pa': 'ver-o-peso', 'to': 'dunas', 'ms': 'deque', 'go': 'pirenopolis', 'pr': 'mata', 'sc': 'garopaba', 'rs': 'poncho'}


def save(src, dst, w, q=80):
    im = Image.open(src).convert('RGB')
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(os.path.join(OUT, dst), quality=q, optimize=True, progressive=True)
    return dst


def paleta(src, n=5):
    im = Image.open(src).convert('RGB').resize((200, 250))
    q = im.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:n * 3]
    cont = sorted(q.getcolors(), reverse=True)
    return ['#%02X%02X%02X' % tuple(pal[i * 3:i * 3 + 3]) for _, i in cont]


campo = json.load(open(S + '/site_fotos_campo.json'))
mapa = {m['estado']: m for m in json.load(open(S + '/mapa_todos.json'))}
data = []
for uf, pasta, nome in EST:
    d = E + '/' + pasta
    ilu = [f for f in glob.glob(d + '/*__com-logo.png')][0]
    pal = glob.glob(d + '/chinelo/palmilha-*.png')[0]
    st = {'uf': uf, 'nome': nome, 'slug': os.path.basename(ilu).split('__')[0]}
    st['ilu'] = save(ilu, f'{uf}-ilustracao.jpg', 1100)
    st['ilu_sem'] = save(ilu.replace('__com-logo', '__sem-logo'), f'{uf}-ilu-sem.jpg', 700, 78)
    st['palmilha'] = save(pal, f'{uf}-palmilha.jpg', 1000)
    st['estudio'] = save(d + f'/chinelo/estudio-{uf}.jpg', f'{uf}-estudio.jpg', 1000)
    lug = sorted(glob.glob(d + '/campanha/lugar-*.jpg'))
    st['lugar'] = [save(f, f'{uf}-lugar-{i+1}.jpg', 800) for i, f in enumerate(lug[:2])]
    cp = d + f'/campanha/campanha-{uf}-{CAMP[uf]}.jpg'
    st['campanha'] = save(cp, f'{uf}-campanha.jpg', 1000) if os.path.exists(cp) else None
    st['campo'] = []
    for i, c in enumerate(campo[uf]):
        st['campo'].append({'img': save(c['arquivo'], f'{uf}-campo-{i+1}.jpg', 900, 78), 'titulo': c['titulo'], 'autor': c['autor'],
                            'licenca': c['licenca'], 'pagina': c['pagina']})
    m = mapa[nome]
    x0, y0, x1, y1 = m['caixa']
    a = Image.open(m['arte'] if m['arte'].startswith('/') else os.path.join(S, m['arte'])).convert('RGB')
    lado = max(x1 - x0, y1 - y0)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    a.crop((cx - lado // 2, cy - lado // 2, cx + lado // 2, cy + lado // 2)).resize((640, 640), Image.LANCZOS).save(
        os.path.join(OUT, f'{uf}-coracao.jpg'), quality=82, optimize=True)
    st['coracao'] = f'{uf}-coracao.jpg'
    st['coracao_texto'] = m['texto']
    st['paleta'] = paleta(pal)
    data.append(st)
    print(uf, 'ok')

# processo: versões descartadas
V = E + '/01-minas-gerais/chinelo/_versoes-anteriores/palmilha-elementos-mg.png'
extra = {'mg-antes-jabuticaba': V, 'mg-antes-janela': E + '/01-minas-gerais/_versoes-anteriores/janela-de-minas__sem-logo.png',
         'sc-antes-ponte': E + '/13-santa-catarina/_versoes-anteriores/baleia-na-ponte__sem-logo.png',
         'sc-depois-enseada': E + '/13-santa-catarina/enseada-da-baleia__sem-logo.png',
         'mg-depois-barroco': E + '/01-minas-gerais/chinelo/palmilha-barroco-mg.png',
         'mg-mockup-antigo': E + '/01-minas-gerais/chinelo/_versoes-anteriores/mockup-elementos-mg.jpg'}
for k, v in extra.items():
    if os.path.exists(v):
        save(v, k + '.jpg', 900)
json.dump(data, open(P + '/07-apresentacao/site/data.json', 'w'), ensure_ascii=False, indent=1)
tot = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
print('imagens', len(os.listdir(OUT)), round(tot / 1e6, 1), 'MB')
