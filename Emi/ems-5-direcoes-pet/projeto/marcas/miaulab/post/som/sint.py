# MIAU.LAB · instrumentos e efeitos sintetizados (usados por trilha2.py). 48 kHz, mono; quem chama posiciona e mistura.
import subprocess, numpy as np
from scipy.signal import butter, sosfilt
SR = 48000
rng = np.random.default_rng(11)
tt = lambda d: np.arange(int(SR * d)) / SR
ruido = lambda d: rng.standard_normal(int(SR * d))
def filt(x, tipo, f, ordem=2): return sosfilt(butter(ordem, f, tipo, fs=SR, output='sos'), x)
def nota(n):
    nomes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    nm, oit = n[:-1], int(n[-1]); return 440 * 2 ** ((nomes.index(nm) + 12 * (oit + 1) - 69) / 12)
def fade(a, i=.005, o=.05):
    n = len(a); e = np.ones(n); ni, no = min(n, int(i * SR)), min(n, int(o * SR))
    if ni: e[:ni] = np.linspace(0, 1, ni)
    if no: e[n - no:] *= np.linspace(1, 0, no)
    return a * e
# ---------- bateria de funk ----------
def kick808(d=.42, f0=52):
    t = tt(d); f = f0 + 150 * np.exp(-t * 45); ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 6.5); c = filt(ruido(.005), 'highpass', 1800) * .6; s[:len(c)] += c
    return np.tanh(s * 2.2) * .9
def palma():
    s = np.zeros(int(SR * .25)); t = tt(.25)
    for k, d in enumerate([0, .008, .016]): i = int(d * SR); s[i:] += np.exp(-(t[:len(s) - i]) * (95 if k < 2 else 20))
    return filt(ruido(.25) * s, 'bandpass', [900, 3400]) * 1.5
def caixa():   # caixa seca de funk (corpo + esteira)
    t = tt(.2); corpo = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30)
    return (corpo * .6 + filt(ruido(.2), 'bandpass', [1500, 7000]) * np.exp(-t * 22)) * .9
def tambor(alto=True):   # "tamborzão": atabaque curto com a altura caindo
    d = .16; t = tt(d); f0 = 260 if alto else 175; f = f0 * (1 + .5 * np.exp(-t * 40))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 24) + filt(ruido(d), 'bandpass', [400, 2500]) * np.exp(-t * 60) * .3
    return s * .8
def chimbal(aberto=False):
    d = .16 if aberto else .045; t = tt(d); return filt(ruido(d), 'highpass', 7500) * np.exp(-t * (18 if aberto else 85)) * .5
def baixo808(f, d):
    t = tt(d); s = np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * 2 * f * t)
    env = np.minimum(1, t / .006) * np.exp(-t * 1.6) * np.clip((d - t) / .04, 0, 1)
    return np.tanh(s * env * 1.8) * .7
def prato():
    t = tt(1.6); return filt(ruido(1.6), 'highpass', 5000) * np.exp(-t * 2.6) * .35
def marimba(f, d=.6):
    t = tt(d); s = np.sin(2 * np.pi * f * t) * np.exp(-t * 6.5) + .35 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-t * 28)
    s += .12 * np.sin(2 * np.pi * 9.2 * f * t) * np.exp(-t * 60); return s * np.minimum(1, t / .002) * .5
# ---------- efeitos ----------
def vento(d, f0, f1, g=1.0):
    n = int(SR * d); out = np.zeros(n); src = ruido(d); B = 2048
    for i in range(0, n, B // 2):
        fc = f0 + (f1 - f0) * (i / n); seg = src[i:i + B]
        y = filt(seg, 'bandpass', [max(60, fc * .6), min(20000, fc * 1.6)]) * np.hanning(len(seg)); out[i:i + len(seg)] += y
    t = tt(d); return out * np.sin(np.pi * t / d) ** 1.5 * g
def baque():
    t = tt(.12); return (np.sin(2 * np.pi * 95 * t) * np.exp(-t * 38) + filt(ruido(.12), 'lowpass', 600) * np.exp(-t * 60) * .5) * .9
def arranhao(d=.24):
    t = tt(d); n = len(t); trem = np.zeros(n); pos = 0
    while pos < n:
        trem[pos:pos + 90] += np.exp(-np.arange(min(90, n - pos)) / 18) * rng.uniform(.5, 1); pos += int(SR / rng.uniform(140, 260))
    s = filt(ruido(d), 'bandpass', [1400, 6500]) * trem
    return s * np.minimum(1, t / .01) * (1 - t / d) ** .6 * 1.3
def bolha():
    t = tt(.16); f = 260 + 900 * (1 - np.exp(-t * 28)); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 20) * np.minimum(1, t / .004) * .7
def piscadinha():   # "plic" curtinho e agudo para a piscada do gato
    t = tt(.07); f = 1800 - 900 * t / .07; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 60) * .5
def olhadinha(lado=1):   # "fiu" mínimo quando os olhos correm de lado
    t = tt(.09); f = 900 + lado * 500 * t / .09; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / .09) * .25
def ladrilhos():
    s = np.zeros(int(SR * .5))
    for k in range(7):
        for j in range(2):
            i = int((k * .035 + j * .006 + rng.uniform(0, .004)) * SR)
            c = filt(ruido(.006), 'bandpass', [2500 + 400 * k, 6000 + 300 * k]) * np.exp(-tt(.006) * 600); s[i:i + len(c)] += c * (.55 + .06 * k)
    w = vento(.42, 1800, 5200, .35); s[:len(w)] += w; return s
def graos(d, n, f0, f1, dec=.008, tipo='ressoa'):
    s = np.zeros(int(SR * (d + .05)))
    for _ in range(n):
        i = int(rng.uniform(0, d) * SR); f = rng.uniform(f0, f1); t = tt(dec * 3)
        g = np.sin(2 * np.pi * f * t) * np.exp(-t / dec) if tipo == 'ressoa' else filt(ruido(dec * 3), 'highpass', f0) * np.exp(-t / dec)
        s[i:i + len(g)] += g * rng.uniform(.3, 1)
    return s
def chacoalha(d, f0, f1, batidas=2):
    s = np.zeros(int(SR * (d + .1)))
    for k in range(batidas):
        g = graos(.09, 28, f0, f1); i = int(k * d / batidas * SR); s[i:i + len(g)] += g
    return s * .45
def amassado(d=.45):
    s = graos(d, 90, 3500, 9000, .0025, 'ruido') * .7; t = tt(d + .05)
    return s + filt(ruido(d + .05), 'bandpass', [300, 2000]) * np.exp(-t * 6) * .25
def cartela():
    s = graos(.07, 30, 4500, 9000, .002, 'ruido') * .6; t = tt(.12)
    pop = filt(ruido(.12), 'bandpass', [900, 3000]) * np.exp(-t * 55) * 1.2 + np.sin(2 * np.pi * 180 * t) * np.exp(-t * 45) * .5
    s2 = np.zeros(int(SR * .2)); s2[:len(s)] += s; i = int(.05 * SR); s2[i:i + len(pop)] += pop; return s2
def sobe(d=.35):   # embalagem entrando de baixo
    return vento(d, 500, 3500, .5)
# ---------- gatos de verdade ----------
def carrega(f, ini=0, fim=None):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True)
    a = np.frombuffer(r.stdout, np.float32).astype(float)[int(ini * SR):int(fim * SR) if fim else None]
    a = filt(a, 'highpass', 120); return a / (np.abs(a).max() + 1e-9)
def altura(a):   # frequência fundamental pela autocorrelação (300–1500 Hz) no trecho mais forte
    n = int(.12 * SR); i = int(np.argmax(np.convolve(np.abs(a), np.ones(n), 'valid'))); s = a[i:i + n] * np.hanning(n)
    ac = np.correlate(s, s, 'full')[n - 1:]; lo, hi = int(SR / 1500), int(SR / 300)
    return SR / (lo + int(np.argmax(ac[lo:hi])))
def transpoe(a, razao):   # muda a altura por reamostragem (mais agudo = mais curto, como num sampler)
    x = np.arange(0, len(a) - 1, razao); return np.interp(x, np.arange(len(a)), a)
