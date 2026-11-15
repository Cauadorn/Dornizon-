# MIAU.LAB · som do reel final = take do gatinho sendo desenhado (desenho/desenho.html) + reel (reel.html).
# Duas versões, como a Emi escolheu:
#   final-efeitos.wav → só efeitos e gatos (para postar com a música em alta escolhida no próprio Instagram)
#   final-funk.wav    → os mesmos efeitos + trilha nova: funk a 120 BPM com o miado picotado virando melodia
# O tempo do reel começa depois do take do desenho (D segundos, lido de desenho/roteiro.json).
# uso: python3 trilha3.py
import os, json, subprocess, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from sint import *
rot = json.load(open('../desenho/roteiro.json')); D = round(rot['dur'] * 30) / 30; R = rot['roteiro']
DUR = D + 14.4
fx = np.zeros((2, int(SR * DUR))); mus = np.zeros((2, int(SR * DUR)))
def poe(dest, t0, sig, g=1.0, pan=0.0):
    i = int(t0 * SR); sig = sig[:max(0, dest.shape[1] - i)]; a = (pan + 1) * np.pi / 4
    dest[0, i:i + len(sig)] += sig * g * np.cos(a); dest[1, i:i + len(sig)] += sig * g * np.sin(a)
# ---------- take do desenho ----------
def tecla():
    t = tt(.05); return (filt(ruido(.05), 'bandpass', [1200, 3500]) * np.exp(-t * 160) + np.sin(2 * np.pi * 160 * t) * np.exp(-t * 70) * .5) * .8
def lapis(d):   # grafite no papel: chiado macio (sem agudo que dá gastura)
    t = tt(d + .06); n = len(t); grao = filt(np.repeat(rng.uniform(.75, 1, n // 240 + 1), 240)[:n], 'lowpass', 40)
    s = filt(filt(ruido(d + .06), 'bandpass', [700, 3000]), 'lowpass', 3500) * grao
    env = np.minimum(1, t / .05) * np.clip((d + .06 - t) / .06, 0, 1); return s * env * .5
def caneta(d):   # caneta no vidro do tablet: mais lisa, com um toque no começo
    t = tt(d + .05); s = filt(ruido(d + .05), 'bandpass', [400, 1600]) * .35
    env = np.minimum(1, t / .04) * np.clip((d + .05 - t) / .05, 0, 1); s = s * env
    toque = filt(ruido(.012), 'bandpass', [1200, 3000]) * np.exp(-tt(.012) * 300) * .4; s[:len(toque)] += toque; return s
for i, x in enumerate(R['letras']): poe(fx, x, tecla(), .32, -.3 + .2 * i)
poe(fx, .78, vento(.45, 300, 1600, .16))
for t0, d, fase in R['tracos']: poe(fx, t0, lapis(d) if fase == 'lapis' else caneta(d), .3 if fase == 'lapis' else .26, rng.uniform(-.15, .15))
for k, (dx, f) in enumerate([(0, 1.0), (.3, 1.25), (.45, 1.5)]):
    b = bolha(); poe(fx, R['balde'] + dx, transpoe(b, f), .4, -.1 + .1 * k)   # balde de tinta
poe(fx, R['fim'] - .75, vento(.6, 1600, 300, .16)); poe(fx, R['fim'] - .3, bolha(), .35)
amb = filt(ruido(D), 'lowpass', 900) * .012; poe(fx, 0, amb)                    # ar do estúdio
# ---------- reel (tudo deslocado de D) ----------
for i, n in enumerate(['C5', 'E5', 'G5', 'C6']): poe(fx, D + .05 + i * .07, marimba(nota(n), .5), .8, -.3 + .2 * i)
poe(fx, D + .45, vento(.55, 300, 1400, .25))
poe(fx, D + .58, fade(carrega('fontes/miau-gatinha.ogg', 0, .95), .005, .18), .95, .05)
poe(fx, D + .98, baque(), .7, -.25); poe(fx, D + 1.02, baque(), .65, .25)
poe(fx, D + 1.16, arranhao(.26), .6, -.3); poe(fx, D + 1.27, arranhao(.24), .55, .3)
poe(fx, D + 1.5, bolha(), .75)
for x in [2.02, 3.54, 5.04, 13.52]: poe(fx, D + x, piscadinha(), .55)              # o gato piscando
for x in [5.4, 6.4, 7.4, 8.4, 9.4, 11.4, 12.9]: poe(fx, D + x, ladrilhos(), .5)
poe(fx, D + 5.45, amassado(), .6, -.2); poe(fx, D + 6.45, chacoalha(.4, 2500, 5200), .65, .2)
poe(fx, D + 7.45, cartela(), .75, -.1); poe(fx, D + 8.45, chacoalha(.45, 1100, 2400), .7, .15)
r = np.concatenate([carrega('fontes/ronrom-bertie.ogg', .3, 6.9), carrega('fontes/ronrom-whiskers.ogg', .5, 6.0)])
r = filt(r, 'lowpass', 2500); ts = np.arange(len(r)) / SR
env = np.clip(ts / .8, 0, 1) * .4 + np.clip((ts - 2.0) / .3, 0, 1) * .6; env *= np.clip((5.0 - ts) / 1.0, 0, 1)
poe(fx, D + 9.4, r * env, .6)
poe(fx, D + 13.75, fade(carrega('fontes/miau-grego.flac', .2, .95), .005, .15), .85, -.05)
# ---------- música: funk do miau a 120 BPM (grade do reel: tempos a cada 0,5 s a partir de 2,4) ----------
S16 = .125
miau = carrega('fontes/miau-gatinha.ogg', 0, 1.0); f0 = altura(miau); chop = fade(miau[:int(.3 * SR)], .003, .07)
def miado(n, d=None): s = transpoe(chop, nota(n) / f0); return fade(s[:int(d * SR)] if d else s, .003, .04)
for k, x in enumerate([R['fim'] - .9, R['fim'] - .4]): poe(mus, x, filt(kick808(), 'lowpass', 250), .35 + .15 * k)   # puxada no fim do desenho
for x in [.4, .9, 1.4, 1.9]: poe(mus, D + x, filt(kick808(), 'lowpass', 300), .45)
for k, x in enumerate([2.025, 2.15, 2.275]): poe(mus, D + x, miado(['C5', 'D#5', 'G5'][k], .1), .55)
poe(mus, D + 1.75, vento(.65, 600, 7000, .2))
KICK = [(0, 1), (3, .7), (6, .9), (8, 1), (11, .7), (14, .9)]
TAMB = [(2, 1), (5, 0), (7, 1), (10, 0), (13, 1), (15, 0)]
BAIXO = [(0, 'C2', 3), (3, 'C2', 3), (6, 'D#2', 2), (8, 'C2', 3), (11, 'G1', 3), (14, 'A#1', 2)]
GANCHO = [[(0, 'G4', .2), (3, 'G4', .2), (6, 'A#4', .2), (10, 'C5', .25), (13, 'A#4', .2)],
          [(0, 'G4', .2), (3, 'F4', .2), (6, 'D#4', .2), (10, 'F4', .2), (12, 'G4', .3)]]
poe(mus, D + 2.4, prato(), .5)
for barra in range(5):                       # 2,4 → 11,4 (4,5 compassos; o último pela metade)
    x0 = D + 2.4 + barra * 2
    for st, v in KICK:
        if x0 + st * S16 < D + 11.4: poe(mus, x0 + st * S16, kick808(), .95 * v)
    for st in (4, 12):
        if x0 + st * S16 < D + 11.4: poe(mus, x0 + st * S16, palma(), .5, .1); poe(mus, x0 + st * S16, caixa(), .35)
    for st, alto in TAMB:
        if x0 + st * S16 < D + 11.4: poe(mus, x0 + st * S16, tambor(alto), .45, .3 if alto else -.3)
    for st in range(16):
        if x0 + st * S16 < D + 11.4: poe(mus, x0 + st * S16, chimbal(st % 4 == 2), .33 if st % 2 else .18, .35)
    for st, n, dd in BAIXO:
        if x0 + st * S16 < D + 11.4: poe(mus, x0 + st * S16, baixo808(nota(n), dd * S16), .6)
    for st, n, d in GANCHO[barra % 2]:
        if x0 + st * S16 < D + 11.4: poe(mus, x0 + st * S16, miado(n, d), .5 if 3.4 <= barra * 2 + 2.4 < 9.4 else .58, -.15)
for k, (x, n) in enumerate(zip([11.4, 11.9, 12.4], ['C5', 'D#5', 'G5'])): poe(mus, D + x, miado(n, .28), .6, -.1 + .07 * k); poe(mus, D + x, kick808(), .45)
for nn in ['C4', 'D#4', 'G4', 'C5']: poe(mus, D + 12.9, marimba(nota(nn), 1.3), .32)
poe(mus, D + 12.9, kick808(), 1); poe(mus, D + 12.9, palma(), .45); poe(mus, D + 12.9, baixo808(nota('C2'), 1.2), .8); poe(mus, D + 12.9, prato(), .4)
# ---------- master ----------
def master(m, alvo=.89):
    m = m.copy()
    for c in range(2): m[c] = filt(m[c], 'highpass', 28)
    pk = np.abs(m).max(); m = np.tanh(m / pk * 1.3) / np.tanh(1.3) * alvo
    n = int(SR * .3); m[:, -n:] *= np.linspace(1, 0, n); return m
def grava(m, nome):
    pcm = (np.clip(m.T, -1, 1) * 32767).astype('<i2').tobytes()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', '-', nome], input=pcm, check=True)
grava(master(fx, .85), 'final-efeitos.wav')
grava(master(mus * .85 + fx), 'final-funk.wav')
print('ok', round(DUR, 2), 's · desenho', D, 's · miado base %.0f Hz' % f0)
