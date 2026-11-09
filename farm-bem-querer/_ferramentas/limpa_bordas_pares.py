"""Tira a auréola clara que ficou em volta dos pares recortados (sobra do fundo de estúdio).
A cor da beirada passa a ser a cor de dentro do chinelo e a borda fica um pouco mais justa,
para o par assentar em qualquer fundo (no escuro da roda a auréola desenhava um contorno de adesivo).
Os originais ficam em 07-apresentacao/_pares-originais/. Uso: python3 -I limpa_bordas_pares.py"""
import glob
import os
import shutil

import numpy as np
from PIL import Image, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(AQUI, '..', '07-apresentacao', 'site', 'img')
ORIG = os.path.join(AQUI, '..', '07-apresentacao', '_pares-originais')
os.makedirs(ORIG, exist_ok=True)

for f in sorted(glob.glob(os.path.join(IMG, '*-par.webp'))):
    o = os.path.join(ORIG, os.path.basename(f))
    if not os.path.exists(o):
        shutil.copy(f, o)
    im = Image.open(o).convert('RGBA')
    A = np.asarray(im).astype(np.float32)
    rgb, al = A[..., :3], A[..., 3]
    dentro = (al >= 250).astype(np.float32)
    # dentro "encolhido" 2 px: a cor que vale é a de bem dentro do chinelo
    dentro_img = Image.fromarray((dentro * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5))
    d = np.asarray(dentro_img).astype(np.float32) / 255
    # convolução normalizada: espalha a cor de dentro para a beirada
    soma = np.zeros_like(rgb)
    for c in range(3):
        canal = Image.fromarray(np.clip(rgb[..., c] * d, 0, 255).astype(np.uint8), 'L').filter(ImageFilter.GaussianBlur(3))
        soma[..., c] = np.asarray(canal).astype(np.float32)
    peso = np.asarray(Image.fromarray((d * 255).astype(np.uint8), 'L').filter(ImageFilter.GaussianBlur(3))).astype(np.float32) / 255
    cor_dentro = soma / np.maximum(peso[..., None], 1e-3)
    borda = (al < 250) & (al > 0)
    novo = rgb.copy()
    novo[borda] = cor_dentro[borda]
    # borda um pouco mais justa: some o último fio claro
    al2 = np.clip((al - 60) * 255 / 195, 0, 255)
    out = np.dstack([np.clip(novo, 0, 255), al2]).astype(np.uint8)
    Image.fromarray(out, 'RGBA').save(f, quality=92, method=6)
    print(os.path.basename(f), 'ok')
