"""Coleta de fotos reais via Openverse (Flickr + Wikimedia, licencas CC), com checagem de LOCAL.
Mesmo formato de saida do campo_estados.py (creditos.json por UF). Prioriza: local confirmado,
licenca livre para qualquer uso (by, by-sa, cc0, pdm); NC entra so como reserva, marcada.
Uso: python campo_openverse.py estados_consultas.json saida_dir [UF ...]"""
import json
import os
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

UA = 'BemQuererResearch/1.0 (portfolio research; non-commercial)'
API = 'https://api.openverse.org/v1/images/'
LIVRES = {'by', 'by-sa', 'cc0', 'pdm'}
NC = {'by-nc', 'by-nc-sa', 'by-nd', 'by-nc-nd'}


def norm(s):
    return unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()


def get(url, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read()
        except Exception as e:
            last = e
            if '424' in str(e) or '404' in str(e):
                break
            time.sleep(10 * (i + 1) if '429' in str(e) else 3)
    raise last


def busca(q, chaves, n=3, exigir_local=True):
    p = {'q': q, 'page_size': 20, 'license_type': 'all-cc', 'mature': 'false'}
    d = json.loads(get(API + '?' + urllib.parse.urlencode(p)))
    cand = []
    for r in d.get('results', []):
        if r.get('source') != 'flickr':  # thumbs do Wikimedia via Openverse falham (424)
            continue
        lic = (r.get('license') or '').lower()
        if lic not in LIVRES | NC:
            continue
        if (r.get('width') or 1000) < 700:
            continue
        tags = ' '.join(t.get('name', '') for t in (r.get('tags') or []))
        texto = norm(' | '.join([r.get('title') or '', tags, r.get('description') or '']))
        achou = [k for k in chaves if norm(k) in texto]
        url = r['url'] if r.get('source') == 'flickr' else (r.get('thumbnail') or r['url'])
        cand.append({
            'titulo': r.get('title') or '', 'thumb': url, 'pagina': r.get('foreign_landing_url'),
            'autor': (r.get('creator') or 'autor desconhecido')[:80],
            'licenca': f"CC {lic.upper()} {r.get('license_version') or ''}".replace('CC CC0', 'CC0').replace('CC PDM', 'Domínio público').strip(),
            'nc': lic in NC, 'fonte': r.get('source'), 'local_ok': bool(achou), 'onde': achou[:3],
            'descricao': tags[:200]})
    # ordem: local+livre, local+nc, (sem local se permitido)
    ordem = sorted(cand, key=lambda c: (not c['local_ok'], c['nc']))
    if exigir_local:
        ordem = [c for c in ordem if c['local_ok']]
    return ordem[:n]


def main():
    cfg = json.load(open(sys.argv[1], encoding='utf8'))
    base = sys.argv[2]
    for uf in (sys.argv[3:] or list(cfg)):
        e = cfg[uf]
        saida = os.path.join(base, uf.lower())
        os.makedirs(saida, exist_ok=True)
        meta_p = os.path.join(saida, 'creditos.json')
        meta = json.load(open(meta_p, encoding='utf8')) if os.path.exists(meta_p) else {}
        for chave, q in e['buscas'].items():
            if meta.get(chave):
                continue
            try:
                res = busca(q, e['locais'], exigir_local=not chave.startswith('obj-'))
            except Exception as ex:
                print(uf, 'falhou', chave, ex, flush=True)
                time.sleep(5)
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
                time.sleep(0.6)
            json.dump(meta, open(meta_p, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
            print(uf, chave, len(meta[chave]), 'local:', sum(x['local_ok'] for x in meta[chave]),
                  'nc:', sum(x['nc'] for x in meta[chave]), flush=True)
            time.sleep(2.5)
        print(uf, 'FIM', flush=True)


if __name__ == '__main__':
    main()
