"""Coleta de fotos reais (Wikimedia Commons, licencas livres) para o painel de pesquisa de campo.
Uso: python campo_fotos.py consultas.json saida_dir  (requisicoes espacadas, com credito e licenca)."""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

UA = 'BemQuererResearch/1.0 (portfolio research; non-commercial)'
API = 'https://commons.wikimedia.org/w/api.php'
OK_LIC = ('cc-by', 'cc by', 'cc0', 'public domain', 'pd', 'cc-zero')


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read()
        except Exception as e:  # 429 / timeouts
            time.sleep(6 * (i + 1))
            last = e
    raise last


def busca(q, n=6):
    p = {'action': 'query', 'format': 'json', 'generator': 'search', 'gsrsearch': q + ' filetype:bitmap',
         'gsrnamespace': 6, 'gsrlimit': 20, 'prop': 'imageinfo', 'iiprop': 'url|extmetadata|size|mime',
         'iiurlwidth': 900, 'maxlag': 5}
    d = json.loads(get(API + '?' + urllib.parse.urlencode(p)))
    pages = sorted(d.get('query', {}).get('pages', {}).values(), key=lambda x: x.get('index', 99))
    out = []
    for pg in pages:
        ii = (pg.get('imageinfo') or [{}])[0]
        if ii.get('mime') not in ('image/jpeg', 'image/png'):
            continue
        if ii.get('width', 0) < 900:
            continue
        md = ii.get('extmetadata', {})
        lic = (md.get('LicenseShortName', {}).get('value') or '').strip()
        if not any(k in lic.lower() for k in OK_LIC):
            continue
        autor = md.get('Artist', {}).get('value', '')
        import re
        autor = re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', autor)).strip()[:80]
        out.append({'titulo': pg['title'], 'thumb': ii.get('thumburl'), 'pagina': ii.get('descriptionurl'),
                    'autor': autor or 'autor no Wikimedia Commons', 'licenca': lic})
        if len(out) >= n:
            break
    return out


def main():
    consultas = json.load(open(sys.argv[1], encoding='utf8'))
    saida = sys.argv[2]
    os.makedirs(saida, exist_ok=True)
    meta = {}
    for chave, q in consultas.items():
        try:
            res = busca(q)
        except Exception as e:
            print('falhou', chave, e)
            continue
        meta[chave] = []
        for i, r in enumerate(res):
            fn = f'{chave}-{i}.jpg'
            try:
                open(os.path.join(saida, fn), 'wb').write(get(r['thumb']))
                r['arquivo'] = fn
                meta[chave].append(r)
            except Exception as e:
                print('  sem download', fn, e)
            time.sleep(1.2)
        print(chave, len(meta[chave]))
        time.sleep(2.5)
    json.dump(meta, open(os.path.join(saida, 'creditos.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
