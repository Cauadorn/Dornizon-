"""Coleta de fotos reais por estado, com checagem de LOCAL.
Para cada busca: pega ate 30 candidatas no Wikimedia Commons, le titulo + descricao + categorias
e marca local_ok quando aparece uma cidade/regiao do estado. Prioriza as com local confirmado.
Uso: python campo_estados.py estados_consultas.json campo_dir [UF ...]"""
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

UA = 'BemQuererResearch/1.0 (portfolio research; non-commercial)'
API = 'https://commons.wikimedia.org/w/api.php'
OK_LIC = ('cc-by', 'cc by', 'cc0', 'public domain', 'pd', 'cc-zero')


def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode()
    return s.lower()


def get(url, tries=5):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read()
        except Exception as e:
            last = e
            time.sleep(15 * (i + 1) if '429' in str(e) else 4)
    raise last


def limpa(html_txt):
    return re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', html_txt or '')).strip()


def busca(q, chaves, n=3, exigir_local=True):
    p = {'action': 'query', 'format': 'json', 'generator': 'search', 'gsrsearch': q + ' filetype:bitmap',
         'gsrnamespace': 6, 'gsrlimit': 30, 'prop': 'imageinfo', 'iiprop': 'url|extmetadata|size|mime',
         'iiurlwidth': 960, 'maxlag': 5}
    d = json.loads(get(API + '?' + urllib.parse.urlencode(p)))
    pages = sorted(d.get('query', {}).get('pages', {}).values(), key=lambda x: x.get('index', 99))
    com_local, sem_local = [], []
    for pg in pages:
        ii = (pg.get('imageinfo') or [{}])[0]
        if ii.get('mime') not in ('image/jpeg', 'image/png') or ii.get('width', 0) < 900:
            continue
        md = ii.get('extmetadata', {})
        lic = (md.get('LicenseShortName', {}).get('value') or '').strip()
        if not any(k in lic.lower() for k in OK_LIC):
            continue
        texto = ' | '.join([pg['title'], limpa(md.get('ImageDescription', {}).get('value')),
                            md.get('Categories', {}).get('value', '')])
        t = norm(texto)
        achou = [k for k in chaves if norm(k) in t]
        item = {'titulo': pg['title'], 'thumb': ii.get('thumburl'), 'pagina': ii.get('descriptionurl'),
                'autor': limpa(md.get('Artist', {}).get('value'))[:80] or 'autor no Wikimedia Commons',
                'licenca': lic, 'local_ok': bool(achou), 'onde': achou[:3],
                'descricao': limpa(md.get('ImageDescription', {}).get('value'))[:200]}
        (com_local if achou else sem_local).append(item)
    escolhidas = com_local[:n]
    if not exigir_local and len(escolhidas) < n:
        escolhidas += sem_local[:n - len(escolhidas)]
    return escolhidas


def main():
    cfg = json.load(open(sys.argv[1], encoding='utf8'))
    base = sys.argv[2]
    ufs = sys.argv[3:] or list(cfg.keys())
    for uf in ufs:
        e = cfg[uf]
        saida = os.path.join(base, uf.lower())
        os.makedirs(saida, exist_ok=True)
        meta_p = os.path.join(saida, 'creditos.json')
        meta = json.load(open(meta_p, encoding='utf8')) if os.path.exists(meta_p) else {}
        for chave, q in e['buscas'].items():
            if meta.get(chave):
                continue
            exigir = not chave.startswith('obj-')  # objetos/comidas podem vir sem local, marcados
            try:
                res = busca(q, e['locais'], exigir_local=exigir)
            except Exception as ex:
                print(uf, 'falhou', chave, ex, flush=True)
                continue
            meta[chave] = []
            for i, r in enumerate(res):
                fn = f'{chave}-{i}.jpg'
                try:
                    open(os.path.join(saida, fn), 'wb').write(get(r['thumb']))
                    r['arquivo'] = fn
                    meta[chave].append(r)
                except Exception as ex:
                    print(uf, '  sem download', fn, ex, flush=True)
                time.sleep(2.5)
            json.dump(meta, open(meta_p, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
            print(uf, chave, len(meta[chave]), 'local_ok:', sum(x['local_ok'] for x in meta[chave]), flush=True)
            time.sleep(4)
        print(uf, 'FIM', flush=True)


if __name__ == '__main__':
    main()
