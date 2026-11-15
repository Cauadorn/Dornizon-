# MIAU.LAB · trilha do reel (14,4 s, 48 kHz estéreo), sincronizada com reel.html.
# Música composta aqui mesmo (120 BPM: um tempo = 0,5 s, o mesmo ritmo dos cortes do vídeo) + efeitos sintetizados
# (letras, patas, arranhão, bolha do .lab, ladrilhos, saquinho, comprimidos, cartela) + gatos de verdade
# (miado e ronronado de domínio público / CC0 do Wikimedia Commons, ver fontes/CREDITOS.txt).
# uso: python3 trilha.py  → som/trilha.wav
import subprocess, os, numpy as np
from scipy.signal import butter, sosfilt
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SR, DUR = 48000, 14.4
mix = np.zeros((2, int(SR * DUR)))
rng = np.random.default_rng(11)
tt = lambda d: np.arange(int(SR * d)) / SR
def filt(x, tipo, f, ordem=2): return sosfilt(butter(ordem, f, tipo, fs=SR, output='sos'), x)
def poe(t0, sig, g=1.0, pan=0.0):   # pan -1..1 (potência constante)
    i = int(t0 * SR); sig = sig[:max(0, mix.shape[1] - i)]
    a = (pan + 1) * np.pi / 4
    mix[0, i:i + len(sig)] += sig * g * np.cos(a); mix[1, i:i + len(sig)] += sig * g * np.sin(a)
def nota(n):   # 'C5', 'A#2'
    nomes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    nm, oit = n[:-1], int(n[-1]); return 440 * 2 ** ((nomes.index(nm) + 12 * (oit + 1) - 69) / 12)
ruido = lambda d: rng.standard_normal(int(SR * d))
# ---------- instrumentos ----------
def bumbo():
    t = tt(.4); f = 44 + 120 * np.exp(-t * 32); ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 8.5); c = filt(ruido(.004), 'highpass', 2000) * .5
    s[:len(c)] += c; return np.tanh(s * 1.6)
def palma():
    s = np.zeros(int(SR * .25)); t = tt(.25)
    for k, d in enumerate([0, .009, .018]): i = int(d * SR); s[i:] += np.exp(-(t[:len(s) - i]) * (90 if k < 2 else 22))
    return filt(ruido(.25) * s, 'bandpass', [900, 3200]) * 1.4
def chimbal(aberto=False):
    d = .18 if aberto else .05; t = tt(d); return filt(ruido(d), 'highpass', 7500) * np.exp(-t * (16 if aberto else 75)) * .55
def estalo():
    t = tt(.06); return filt(ruido(.06), 'bandpass', [1800, 5200]) * np.exp(-t * 70) * 1.2
def prato():
    t = tt(1.6); return filt(ruido(1.6), 'highpass', 5000) * np.exp(-t * 2.6) * .35
def baixo(f, d):
    t = tt(d + .05); s = sum(np.sin(2 * np.pi * k * f * t) / k * np.exp(-t * (2 + k * 5)) for k in range(1, 11))
    s += .6 * np.sin(2 * np.pi * f * t); env = np.minimum(1, t / .004) * np.clip((d + .05 - t) / .05, 0, 1)
    return filt(s * env, 'lowpass', 1400) * .55
def marimba(f, d=.6):
    t = tt(d); s = np.sin(2 * np.pi * f * t) * np.exp(-t * 6.5) + .35 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 28)
    s += .12 * np.sin(2 * np.pi * 9.2 * f * t) * np.exp(-t * 60); s[:96] += filt(ruido(.002), 'highpass', 3000) * .3
    return s * np.minimum(1, t / .002) * .5
def vento(d, f0, f1, g=1.0):   # sopro com o filtro andando de f0 a f1 (feito em blocos que se cruzam)
    n = int(SR * d); out = np.zeros(n); src = ruido(d); B = 2048
    for i in range(0, n, B // 2):
        fc = f0 + (f1 - f0) * (i / n); seg = src[i:i + B] if i + B <= n else src[i:]
        lo, hi = max(60, fc * .6), min(20000, fc * 1.6)
        y = filt(seg, 'bandpass', [lo, hi]) * np.hanning(len(seg)); out[i:i + len(seg)] += y
    t = tt(d); return out * np.sin(np.pi * t / d) ** 1.5 * g
def baque():
    t = tt(.12); return (np.sin(2 * np.pi * 95 * t) * np.exp(-t * 38) + filt(ruido(.12), 'lowpass', 600) * np.exp(-t * 60) * .5) * .9
def arranhao(d=.24):   # garra raspando papelão: ruído granulado no ritmo do "trava-solta" da unha
    t = tt(d); n = len(t); trem = np.zeros(n); pos = 0
    while pos < n:
        trem[pos:pos + 90] += np.exp(-np.arange(min(90, n - pos)) / 18) * rng.uniform(.5, 1); pos += int(SR / rng.uniform(140, 260))
    s = filt(ruido(d), 'bandpass', [1400, 6500]) * trem
    return s * np.minimum(1, t / .01) * (1 - t / d) ** .6 * 1.3
def bolha():
    t = tt(.16); f = 260 + 900 * (1 - np.exp(-t * 28)); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 20) * np.minimum(1, t / .004)
    return s * .7
def ladrilhos():   # cascata de cliques (um por diagonal de ladrilho) + sopro curto
    s = np.zeros(int(SR * .5))
    for k in range(7):
        for j in range(2):
            i = int((k * .035 + j * .006 + rng.uniform(0, .004)) * SR); c = filt(ruido(.006), 'bandpass', [2500 + 400 * k, 6000 + 300 * k]) * np.exp(-tt(.006) * 600)
            s[i:i + len(c)] += c * (.55 + .06 * k)
    w = vento(.42, 1800, 5200, .35); s[:len(w)] += w; return s
def graos(d, n, f0, f1, dec=.008, tipo='ressoa'):
    s = np.zeros(int(SR * (d + .05)))
    for _ in range(n):
        i = int(rng.uniform(0, d) * SR); f = rng.uniform(f0, f1); t = tt(dec * 3)
        g = np.sin(2 * np.pi * f * t) * np.exp(-t / dec) if tipo == 'ressoa' else filt(ruido(dec * 3), 'highpass', f0) * np.exp(-t / dec)
        s[i:i + len(g)] += g * rng.uniform(.3, 1)
    return s
def chacoalha(d, f0, f1, batidas=2):   # sacudidas: grãos agrupados em "batidas"
    s = np.zeros(int(SR * (d + .1)))
    for b in range(batidas):
        g = graos(.09, 28, f0, f1); i = int(b * d / batidas * SR); s[i:i + len(g)] += g
    return s * .45
def amassado(d=.45):   # saquinho fosco: estalinhos agudos + roçar grave
    s = graos(d, 90, 3500, 9000, .0025, 'ruido') * .7
    t = tt(d + .05); s += filt(ruido(d + .05), 'bandpass', [300, 2000]) * np.exp(-t * 6) * .25; return s
def cartela():
    s = graos(.07, 30, 4500, 9000, .002, 'ruido') * .6; t = tt(.12)
    pop = filt(ruido(.12), 'bandpass', [900, 3000]) * np.exp(-t * 55) * 1.2 + np.sin(2 * np.pi * 180 * t) * np.exp(-t * 45) * .5
    s2 = np.zeros(int(SR * .2)); s2[:len(s)] += s; i = int(.05 * SR); s2[i:i + len(pop)] += pop; return s2
def carrega(f, ini=0, fim=None, g=1.0):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True)
    a = np.frombuffer(r.stdout, np.float32).astype(float)[int(ini * SR):int(fim * SR) if fim else None]
    a = filt(a, 'highpass', 120); a /= (np.abs(a).max() + 1e-9); return a * g
def fade(a, i=.01, o=.1):
    n = len(a); e = np.ones(n); ni, no = int(i * SR), int(o * SR); e[:ni] = np.linspace(0, 1, ni); e[n - no:] *= np.linspace(1, 0, no); return a * e
# ---------- 0,0–2,4 · abertura ----------
for i, n in enumerate(['C5', 'E5', 'G5', 'C6']): poe(.05 + i * .07, marimba(nota(n), .5), .8, -.3 + .2 * i)
poe(.45, vento(.55, 300, 1400, .25))                                   # cabeça subindo por trás do U
poe(.58, fade(carrega('fontes/miau-gatinha.ogg', 0, .95), .005, .18), .95, .05)   # MIAU
poe(.98, baque(), .7, -.25); poe(1.02, baque(), .65, .25)               # patas agarrando a borda
poe(1.16, arranhao(.26), .6, -.3); poe(1.27, arranhao(.24), .55, .3)  # arranhões riscando
poe(1.5, bolha(), .75)                                                  # .lab
for k, x in enumerate(np.arange(1.9, 2.4, .0625)): poe(x, palma() * .5, .15 + .5 * k / 8)   # rufada até o drop
poe(1.75, vento(.65, 600, 7000, .22))
# ---------- 2,4–12,9 · groove a 120 BPM ----------
B0, T = 2.4, .5
poe(B0, prato(), .5)
BX1 = [(0, 'C2', .2), (3, 'C3', .1), (6, 'G2', .15), (8, 'A#2', .2), (10, 'C3', .1), (12, 'G2', .12), (14, 'F2', .2)]
BX2 = [(0, 'C2', .2), (3, 'C3', .1), (6, 'G2', .15), (8, 'A#2', .2), (10, 'C3', .1), (12, 'D#2', .12), (14, 'E2', .12)]
GA1 = [(0, 'C6', .5), (3, 'G5', .4), (6, 'A5', .4), (8, 'G5', .4), (10, 'E5', .4), (12, 'D5', .4), (14, 'E5', .5)]
GA2 = [(0, 'C6', .5), (3, 'G5', .4), (6, 'A5', .4), (8, 'C6', .4), (10, 'D6', .3), (12, 'E6', .3), (14, 'D6', .5)]
for b in range(21):                      # 21 tempos: 2,4 → 12,4
    x = B0 + b * T
    poe(x, bumbo(), .9)
    if b % 2: poe(x, palma(), .42, .1)
    poe(x + T / 2, chimbal(b % 4 == 3), .5, .35)
    if b % 2 == 0 and b >= 6: poe(x + .375, estalo(), .25, -.4)          # estalos de dedo a partir das fotos
for barra in range(5):                   # 5 compassos de 2 s: 2,4 → 12,4
    x0 = B0 + barra * 2
    for st, n, d in (BX1 if barra % 2 == 0 else BX2):
        poe(x0 + st * .125, baixo(nota(n), d), .8)
    gan = .34 if barra < 2 else .2       # gancho da marimba mais baixo nas fotos (espaço para os efeitos)
    for st, n, d in (GA1 if barra % 2 == 0 else GA2):
        poe(x0 + st * .125, marimba(nota(n), d), gan, .2)
# leve "abaixa" do baixo a cada bumbo (sidechain simples): feito no fim, por envelope
# ---------- 5,4–11,4 · fotos ----------
for x in [5.4, 6.4, 7.4, 8.4, 9.4, 11.4]: poe(x, ladrilhos(), .5)
poe(5.45, amassado(), .55, -.2)                       # pouch na mão
poe(6.45, chacoalha(.4, 2500, 5200), .6, .2)          # potes de comprimidos
poe(7.45, cartela(), .7, -.1)                         # caixa + cartela
poe(8.45, chacoalha(.45, 1100, 2400), .65, .15)       # linha de pouches (petiscos)
ron = carrega('fontes/ronrom-bertie.ogg', .3, 6.9)     # ronronado contínuo
ron2 = carrega('fontes/ronrom-whiskers.ogg', .5, 6.0)
r = np.concatenate([ron, ron2]); r = filt(r, 'lowpass', 2500)
env = np.ones(len(r)); ts = np.arange(len(r)) / SR
env *= np.clip(ts / .8, 0, 1) * .45 + np.clip((ts - 2.0) / .3, 0, 1) * .55   # entra baixo na panorâmica, sobe no "ronrona"
env *= np.clip((5.0 - ts) / 1.2, 0, 1)                                    # some no fim (14,4 s)
poe(9.4, r * env, .55)
# ---------- 11,4–14,4 · fecho "Ciência que ronrona." ----------
for i, (x, n) in enumerate(zip([11.4, 11.9, 12.4, 12.9], ['C5', 'E5', 'G5', 'C6'])):
    poe(x, marimba(nota(n), .7), .5, -.2 + .15 * i)
for nn in ['C4', 'E4', 'G4', 'C5']: poe(12.9, marimba(nota(nn), 1.2), .3)    # acorde final
poe(12.9, bumbo(), .9); poe(12.9, palma(), .4); poe(12.9, baixo(nota('C2'), .6), .9); poe(12.9, prato(), .35)
poe(13.25, fade(carrega('fontes/miau-grego.flac', .2, .95), .005, .15), .8, -.05)   # miadinho de despedida
# ---------- master ----------
for c in range(2): mix[c] = filt(mix[c], 'highpass', 28)
pk = np.abs(mix).max(); mix = np.tanh(mix / pk * 1.25) / np.tanh(1.25) * .89
fim = int(SR * .35); mix[:, -fim:] *= np.linspace(1, 0, fim)
pcm = (np.clip(mix.T, -1, 1) * 32767).astype('<i2').tobytes()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', '-', 'trilha.wav'], input=pcm, check=True)
print('ok trilha.wav', DUR, 's')
