"""Monta 07-apresentacao/behance/pacote/ (capa, módulos em ordem com vídeo onde houver, alternativas paradas,
textos e prévia) e o ZIP.  Uso: python3 -I behance_pacote.py [caminho-do-zip]"""
import glob
import json
import os
import shutil
import sys
import zipfile

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(AQUI, '..', '07-apresentacao', 'behance')
PK = os.path.join(B, 'pacote')
ZIP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(B, 'behance-bem-querer.zip')
if os.path.isdir(PK):
    shutil.rmtree(PK)
d_capa, d_mod, d_alt = [os.path.join(PK, x) for x in ('1-capa-do-projeto', '2-modulos-em-ordem', '3-alternativas-paradas')]
for x in (d_capa, d_mod, d_alt):
    os.makedirs(x)

capa = Image.open(os.path.join(B, 'capa-behance-1616x1264.jpg'))
capa.save(os.path.join(d_capa, 'capa-1616x1264.jpg'), quality=92)
capa.resize((808, 632), Image.LANCZOS).save(os.path.join(d_capa, 'capa-808x632.jpg'), quality=92)

mods = json.load(open(os.path.join(B, 'modulos.json')))
VIDS = os.path.join(B, 'videos')
REND = os.path.join(B, '_render')
# cada item: (nome, arquivo para subir, imagem parada equivalente)
itens = []
for m in mods:
    nn = f'{m["n"]:02d}'
    jpg = os.path.join(B, 'modulos', f'{nn}-{m["id"]}.jpg')
    mp4 = os.path.join(VIDS, f'modulo-{nn}.mp4')
    if m['id'] == 'capa' and os.path.exists(os.path.join(VIDS, 'filme-abertura.mp4')):
        still = os.path.join(REND, 'abertura', '0217.jpg')
        itens.append(('abertura', os.path.join(VIDS, 'filme-abertura.mp4'), still if os.path.exists(still) else jpg))
    elif m['video'] and os.path.exists(mp4):
        itens.append((m['id'], mp4, jpg))
    else:
        itens.append((m['id'], jpg, None))
    if m['id'] == 'campanha' and os.path.exists(os.path.join(VIDS, 'filme-colecao.mp4')):
        still = os.path.join(REND, 'colecao', '0505.jpg')
        itens.append(('colecao-em-movimento', os.path.join(VIDS, 'filme-colecao.mp4'), still if os.path.exists(still) else None))
ordem, paradas = [], []
for k, (nome, arq, parada) in enumerate(itens, 1):
    ext = os.path.splitext(arq)[1]
    alvo = f'{k:02d}-{nome}{ext}'
    shutil.copy(arq, os.path.join(d_mod, alvo))
    if ext == '.mp4':
        if parada:
            shutil.copy(parada, os.path.join(d_alt, f'{k:02d}-{nome}.jpg'))
        ordem.append(alvo + '  (vídeo)')
    else:
        ordem.append(alvo)
    paradas.append(parada or arq)

# prévia do post inteiro (versões paradas), 700 px de largura
ims = [Image.open(f) for f in paradas]
W = 700
hs = [round(i.height * W / i.width) for i in ims]
prev = Image.new('RGB', (W, sum(hs)), 'white')
y = 0
for i, h in zip(ims, hs):
    prev.paste(i.convert('RGB').resize((W, h), Image.LANCZOS), (0, y))
    y += h
prev.save(os.path.join(PK, 'previa-do-post.jpg'), quality=82)

lista = '\n'.join(f'{k + 1:>2}. {o}' for k, o in enumerate(ordem))
TXT = f'''BEM-QUERER · POST DO BEHANCE
============================

COMO SUBIR
1. Crie o projeto e suba os arquivos da pasta 2-modulos-em-ordem, nesta ordem:
{lista}
   O primeiro vídeo é a abertura (11,2 s), só tipografia: a assinatura da collab, as duas folhas que caem
   e formam o coração e Bem-Querer letra a letra. \"A coleção em movimento\" passa os 14 estados (32 s).
   Os outros vídeos têm 12,9 s. Todos com 1280 px de largura (o máximo do Behance para vídeo enviado) e sem som.
   Se o editor oferecer reprodução automática e repetição para o vídeo, ative as duas.
   Se o vídeo der problema, use a imagem de mesmo número da pasta 3-alternativas-paradas.
2. Capa: use capa-1616x1264.jpg (ou a de 808x632). Ela não tem texto, como o Behance recomenda.
3. Preencha os campos com os textos abaixo.
4. Só publique quando estiver tudo pronto: a curadoria do Behance olha cada projeto uma vez só, na primeira publicação.

TÍTULO
Bem-Querer · havaianas ♥ FARM Rio (conceito)

DESCRIÇÃO DO PROJETO
Bem-Querer é uma V2 conceitual da collab havaianas ♥ FARM Rio: quatorze pares de chinelos, um por estado, cada um feito com os elementos de lá e com um coração escondido na estampa, formado pelos próprios elementos.
Conceito, direção de arte e curadoria: Emilly Silva. Ilustrações, estampas, mockups e motions gerados com IA (Nano Banana, via Freepik; Kling, via Higgsfield) a partir dessa direção. Pesquisa, textos, site e animações de texto com apoio de IA (Claude). Fotos de campo reais, de fotógrafos creditados no site.
Projeto fictício de portfólio, sem vínculo com a FARM Rio ou a havaianas.
Site completo: cauadorn.github.io/Dornizon-

CAMPOS CRIATIVOS (até 3)
Ilustração · Design de estampas (Pattern Design) · Direção de arte

TAGS (10)
estamparia, design de superfície, ilustração, chinelo, havaianas, FARM Rio, direção de arte, projeto conceitual, Brasil, motion

FERRAMENTAS (campo "Ferramentas usadas"; o Behance pede que projetos com IA generativa declarem as ferramentas)
Nano Banana (Google) · Freepik · Kling AI · Higgsfield · Claude

TEXTOS OPCIONAIS ENTRE OS MÓDULOS (blocos de texto do Behance; ajudam na busca)
Depois do módulo 05 (processo):
Cada estado começou por fotos reais do lugar, com autor e local conferidos, e por uma âncora: um elemento que é daquele estado e de nenhum outro. Só depois vieram o chinelo em díptico e a ilustração do lugar inteiro, sempre com os mesmos elementos.

Depois do módulo 10 (solução):
Quatorze cenas, quatorze pares e uma regra que amarra tudo: o coração nunca é desenhado em cima de nada. Ele aparece quando os elementos se encontram. As ilustrações ganharam movimento para o site e para as redes.

Depois do módulo 17 (reflexão):
Gerar imagem com IA não tirou o trabalho de direção: cada estado passou por pesquisa, escolha de âncora, paleta e várias rodadas de ajuste até o coração aparecer sem ser desenhado. O que ficou é o que passou por esse crivo.

CRÉDITOS DAS FOTOS DE CAMPO DO MÓDULO 04
Os autores e licenças estão escritos embaixo de cada foto. A lista completa (139 fotógrafos) está no site, em Créditos.
'''
open(os.path.join(PK, 'textos-e-ordem.txt'), 'w', encoding='utf8').write(TXT)

with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_STORED) as z:
    for raiz, _, fs in os.walk(PK):
        for f in sorted(fs):
            caminho = os.path.join(raiz, f)
            z.write(caminho, os.path.join('behance-bem-querer', os.path.relpath(caminho, PK)))
print('ok', len(ordem), 'itens', round(os.path.getsize(ZIP) / 1e6, 1), 'MB')
print(lista)
