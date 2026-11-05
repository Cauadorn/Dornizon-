"""Junta texto do estado (textos_estados_*.py) + curadoria de fotos (sel/<uf>.json) e exporta o caderno.
Uso: python monta_estado.py UF"""
import importlib.util
import json
import os
import subprocess
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = '/home/user/Dornizon-/farm-bem-querer/pesquisa-de-campo'


def carrega(nome):
    spec = importlib.util.spec_from_file_location(nome, os.path.join(HERE, nome + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.T


def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return '-'.join(s.split())


if __name__ == '__main__':
    uf = sys.argv[1].upper()
    T = {**carrega('textos_estados_1'), **carrega('textos_estados_2')}
    cfg = dict(T[uf])
    sel = json.load(open(os.path.join(HERE, 'sel', f'{uf.lower()}.json'), encoding='utf8'))
    cfg.update(sel)
    cfg['estampa'] = dict(cfg['estampa'])
    spec = importlib.util.spec_from_file_location('textos_bichos', os.path.join(HERE, 'textos_bichos.py'))
    mb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mb)
    if uf in mb.B:
        if mb.B[uf].get('bicho'):
            cfg['bicho'] = mb.B[uf]['bicho']
        cfg['estampa'].update(mb.B[uf].get('estampa', {}))
    cfg['estampa']['fontes'] = cfg['estampa']['fontes'].replace(
        'Fotos: Wikimedia Commons, licenças CC indicadas em cada imagem.',
        'Fotos: Flickr e Wikimedia Commons (via Openverse), autor e licença em cada imagem; local conferido no título, nas tags ou na descrição.')
    os.makedirs(os.path.join(HERE, 'cfg'), exist_ok=True)
    cfg_p = os.path.join(HERE, 'cfg', f'caderno_{uf.lower()}.json')
    json.dump(cfg, open(cfg_p, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    destino = os.path.join(PROJ, f"{cfg['numero']}-{slug(cfg['nome'])}")
    subprocess.run([sys.executable, '-I', os.path.join(HERE, 'exportar_caderno.py'), cfg_p,
                    os.path.join(HERE, 'campo2', uf.lower()), destino], check=True)
