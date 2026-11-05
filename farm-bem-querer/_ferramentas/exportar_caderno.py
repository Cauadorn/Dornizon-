"""Copia as fotos usadas + creditos para o projeto, monta o HTML e exporta o PDF do caderno."""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
cfg_path, fotos_src, destino = sys.argv[1], sys.argv[2], sys.argv[3]
cfg = json.load(open(cfg_path, encoding='utf8'))
os.makedirs(os.path.join(destino, 'fotos'), exist_ok=True)

usadas = {cfg['hero']} | {p[0] for p in cfg['painel']} | {m[0] for m in cfg['motivos']}
cred = {}
for f in os.listdir(fotos_src):
    if f.startswith('creditos') and f.endswith('.json'):
        for lista in json.load(open(os.path.join(fotos_src, f), encoding='utf8')).values():
            for c in lista:
                cred[c['arquivo']] = c
faltando = [u for u in sorted(usadas) if u not in cred]
for u in sorted(usadas):
    shutil.copyfile(os.path.join(fotos_src, u), os.path.join(destino, 'fotos', u))
json.dump({'fotos': [cred[u] for u in sorted(usadas) if u in cred]},
          open(os.path.join(destino, 'fotos', 'creditos.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
html = os.path.join(destino, 'caderno-de-campo.html')
subprocess.run([sys.executable, '-I', os.path.join(HERE, 'caderno.py'), cfg_path, os.path.join(destino, 'fotos'), html], check=True)
subprocess.run(['node', os.path.join(HERE, 'html2pdf.js'), html, os.path.join(destino, 'caderno-de-campo.pdf')], check=True)
print('fotos sem credito:', faltando or 'nenhuma')
