# MIAU.LAB · trilha do reel v2: "funk do miau" a 130 BPM (batida de funk com tamborzão, 808 e o miado picotado
# virando melodia) + os efeitos sincronizados com reel2.html. Gera duas saídas:
#   trilha2.wav  → música + efeitos (versão pronta)
#   efeitos2.wav → só os efeitos e os gatos (para postar com uma música em alta escolhida no próprio Instagram)
# uso: python3 trilha2.py
import os, subprocess, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from sint import *
BT = 60 / 130; b = lambda n: n * BT; S16 = BT / 4
DUR = b(43.5) + .3
mus = np.zeros((2, int(SR * DUR))); fx = np.zeros((2, int(SR * DUR)))
def poe(dest, t0, sig, g=1.0, pan=0.0):
    i = int(t0 * SR); sig = sig[:max(0, dest.shape[1] - i)]; a = (pan + 1) * np.pi / 4
    dest[0, i:i + len(sig)] += sig * g * np.cos(a); dest[1, i:i + len(sig)] += sig * g * np.sin(a)
# ---------- o miado como instrumento ----------
miau = carrega('fontes/miau-gatinha.ogg', 0, 1.0); f0 = altura(miau)
chop = fade(miau[:int(.30 * SR)], .003, .07)
def miado(n, d=None, g=1.0):
    s = transpoe(chop, nota(n) / f0); return fade(s[:int(d * SR)] if d else s, .003, .04) * g
# ---------- A · abertura (0–6 tempos) ----------
for i, n in enumerate(['C5', 'E5', 'G5', 'C6']): poe(fx, b(.1) + i * b(.18), marimba(nota(n), .5), .75, -.3 + .2 * i)
poe(fx, b(1.0), vento(.5, 300, 1400, .25))
poe(fx, b(1.3), fade(carrega('fontes/miau-gatinha.ogg', 0, .95), .005, .18), .95, .05)
poe(fx, b(2.2), baque(), .7, -.25); poe(fx, b(2.28), baque(), .65, .25)
poe(fx, b(2.5), arranhao(.26), .6, -.3); poe(fx, b(2.75), arranhao(.24), .55, .3)
poe(fx, b(3.4), bolha(), .75)
poe(fx, b(4.3), piscadinha(), .6)
poe(fx, b(4.8), olhadinha(-1), .8, -.5); poe(fx, b(5.3), olhadinha(1), .8, .5)
# música da abertura: kick abafado nos tempos 2–5, gancho do miado baixinho, "mi-mi-mi" antes do drop
for k in range(2, 6): poe(mus, b(k), filt(kick808(), 'lowpass', 300), .5)
for st, n in [(0, 'G4'), (3, 'G4'), (6, 'A#4'), (10, 'C5')]: poe(mus, b(2) + st * S16, filt(miado(n, .22), 'lowpass', 2500), .3)
for k, x in enumerate([5.25, 5.5, 5.625, 5.75]): poe(mus, b(x), miado(['C5', 'C5', 'D#5', 'G5'][k], .1), .55)
poe(mus, b(4.5), vento(b(1.5), 500, 8000, .25))
# ---------- groove de funk (6–36 tempos, com respiro no 22–26) ----------
KICK = [(0, 1), (3, .7), (6, .9), (8, 1), (11, .7), (14, .9)]
TAMB = [(2, 1), (5, 0), (7, 1), (10, 0), (13, 1), (15, 0)]
BAIXO = [(0, 'C2', 3), (3, 'C2', 3), (6, 'D#2', 2), (8, 'C2', 3), (11, 'G1', 3), (14, 'A#1', 2)]
GANCHO = [[(0, 'G4', .2), (3, 'G4', .2), (6, 'A#4', .2), (10, 'C5', .25), (13, 'A#4', .2)],
          [(0, 'G4', .2), (3, 'F4', .2), (6, 'D#4', .2), (10, 'F4', .2), (12, 'G4', .3)]]
poe(mus, b(6), prato(), .5)
for barra in range(int((36 - 6) / 4)):          # 7,5 compassos de 4 tempos
    x0 = b(6 + 4 * barra)
    respiro = 22 <= 6 + 4 * barra < 26
    for st, v in KICK:
        if respiro and st not in (0, 8): continue
        poe(mus, x0 + st * S16, kick808(), .95 * v)
    for st in (4, 12): poe(mus, x0 + st * S16, palma(), .5, .1); poe(mus, x0 + st * S16, caixa(), .35)
    if not respiro:
        for st, alto in TAMB: poe(mus, x0 + st * S16, tambor(alto), .45, .3 if alto else -.3)
        for st in range(16): poe(mus, x0 + st * S16, chimbal(st % 4 == 2), .35 if st % 2 else .2, .35)
        for st, n, dur in BAIXO: poe(mus, x0 + st * S16, baixo808(nota(n), dur * S16), .6)
    for st, n, d in GANCHO[barra % 2]: poe(mus, x0 + st * S16, miado(n, d), .55 if not respiro else .7, -.15)
# ---------- efeitos das seções ----------
for k in range(4): poe(fx, b(14 + 2 * k) + .05, sobe(.32), .5); poe(fx, b(14.6 + 2 * k), baque(), .45)
poe(fx, b(22), vento(.5, 800, 4000, .3)); poe(fx, b(24), vento(.5, 800, 4000, .3))
for x in [26, 28, 30, 32, 34, 36, 40]: poe(fx, b(x), ladrilhos(), .5)
poe(fx, b(26) + .05, amassado(), .6, -.2)
poe(fx, b(28) + .05, chacoalha(.4, 2500, 5200), .65, .2)
poe(fx, b(30) + .05, cartela(), .75, -.1)
poe(fx, b(32) + .05, chacoalha(.45, 1100, 2400), .7, .15)
# ronronado: entra na panorâmica, cresce no "ronrona" e fica até o fim
r = np.concatenate([carrega('fontes/ronrom-bertie.ogg', .3, 6.9), carrega('fontes/ronrom-whiskers.ogg', .5, 6.0)])
r = filt(r, 'lowpass', 2500); ts = np.arange(len(r)) / SR; t0r = b(34)
env = np.clip(ts / .8, 0, 1) * .4 + np.clip((ts - (b(36) - t0r)) / .3, 0, 1) * .6
env *= np.clip((DUR - t0r - ts) / 1.2, 0, 1); poe(fx, t0r, r * env, .6)
# ---------- F · "Ciência que ronrona." (36–40): bateria sai, o miado sobe uma nota por troca de cor ----------
for k, n in enumerate(['C5', 'D#5', 'G5', 'C6']): poe(mus, b(36 + k), miado(n, .28), .6, -.1 + .07 * k); poe(mus, b(36 + k), kick808(), .45)
# ---------- G · logo final (40–43,5) ----------
for nn in ['C4', 'D#4', 'G4', 'C5']: poe(mus, b(40), marimba(nota(nn), 1.3), .32)
poe(mus, b(40), kick808(), 1); poe(mus, b(40), palma(), .45); poe(mus, b(40), baixo808(nota('C2'), 1.2), .8); poe(mus, b(40), prato(), .4)
poe(fx, b(41.6), piscadinha(), .6)
poe(fx, b(42.1), fade(carrega('fontes/miau-grego.flac', .2, .95), .005, .15), .85, -.05)
# ---------- master ----------
def master(m, alvo=.89):
    for c in range(2): m[c] = filt(m[c], 'highpass', 28)
    pk = np.abs(m).max(); m = np.tanh(m / pk * 1.3) / np.tanh(1.3) * alvo
    n = int(SR * .3); m[:, -n:] *= np.linspace(1, 0, n); return m
def grava(m, nome):
    pcm = (np.clip(m.T, -1, 1) * 32767).astype('<i2').tobytes()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', '-', nome], input=pcm, check=True)
grava(master(mus * .85 + fx.copy()), 'trilha2.wav')
grava(master(fx.copy(), .8), 'efeitos2.wav')
print('ok', round(DUR, 2), 's · miado base %.0f Hz' % f0)
