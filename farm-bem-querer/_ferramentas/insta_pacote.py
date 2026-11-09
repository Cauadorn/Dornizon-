"""Monta instagram/carrossel-final/ na ordem de postagem (vídeo onde houver motion, JPG no resto) e o ZIP."""
import glob
import os
import shutil
import sys
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
INSTA = os.path.join(AQUI, '..', '07-apresentacao', 'instagram')
FIM = os.path.join(INSTA, 'carrossel-final')
ZIP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(INSTA, 'carrossel-bem-querer.zip')
os.makedirs(FIM, exist_ok=True)
for f in glob.glob(os.path.join(FIM, '*')):
    os.remove(f)
slides = sorted(glob.glob(os.path.join(INSTA, 'slides', 'bem-querer-*.jpg')))
ordem = []
for jpg in slides:
    nn = os.path.basename(jpg)[11:13]
    mp4 = os.path.join(INSTA, 'videos', f'bem-querer-{nn}.mp4')
    src = mp4 if os.path.exists(mp4) else jpg
    dst = os.path.join(FIM, f'{nn}-' + ('video.mp4' if src == mp4 else 'imagem.jpg'))
    shutil.copy(src, dst)
    ordem.append(os.path.basename(dst))
for t in ['legenda.txt', 'alt-text.txt']:
    shutil.copy(os.path.join(INSTA, t), FIM)
open(os.path.join(FIM, 'LEIA-ME.txt'), 'w', encoding='utf8').write(
    'Carrossel Bem-Querer · 13 itens, 1080x1440 (3:4)\n\n'
    'Suba nesta ordem (o número no nome do arquivo é a posição):\n' + '\n'.join('  ' + o for o in ordem) + '\n\n'
    'Os vídeos têm 12,9 s, sem som, e repetem sem emenda.\n'
    'Legenda em legenda.txt; texto alternativo de cada slide em alt-text.txt\n'
    '(no app: Configurações avançadas > Acessibilidade > Escrever texto alternativo).\n'
    'A menção à IA está no último slide, na ficha técnica.\n')
with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_STORED) as z:
    for f in sorted(os.listdir(FIM)):
        z.write(os.path.join(FIM, f), f)
print('ok', len(ordem), 'itens', round(os.path.getsize(ZIP) / 1e6, 1), 'MB')
print(' '.join(ordem))
