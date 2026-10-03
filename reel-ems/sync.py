"""Gera timings.json a partir da narração gravada, para as animações baterem com a voz.

uso: python3 sync.py narracao.m4a
depois: node render.mjs --audio narracao.m4a

Transcreve com faster-whisper (timestamps por palavra) e alinha com o roteiro de index.html.
Palavras que o Whisper errar ou pular recebem tempo interpolado entre as vizinhas.
"""
import json, re, sys, difflib, unicodedata
from pathlib import Path
from faster_whisper import WhisperModel

here = Path(__file__).parent
audio = sys.argv[1]

html = (here / "index.html").read_text(encoding="utf-8")
beats = re.findall(r"\['[^']+',\s*'([^']+)'\]", html.split("const BEATS=")[1].split("];")[0])
script = [w for b in beats for w in b.split()]

def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))

model = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = model.transcribe(audio, language="pt", word_timestamps=True, beam_size=5)
heard = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
print(f"roteiro: {len(script)} palavras · ouvidas: {len(heard)}")

a = [norm(w) for w in script]
b = [norm(w) for w, _, _ in heard]
times = [None] * len(script)
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
        for k in range(i2 - i1):
            times[i1 + k] = [heard[j1 + k][1], heard[j1 + k][2]]

# interpola o que não casou
known = [i for i, t in enumerate(times) if t]
for i, t in enumerate(times):
    if t:
        continue
    prev = max([k for k in known if k < i], default=None)
    nxt = min([k for k in known if k > i], default=None)
    t0 = times[prev][1] if prev is not None else 0.0
    t1 = times[nxt][0] if nxt is not None else t0 + 0.4
    n0 = prev if prev is not None else -1
    n1 = nxt if nxt is not None else len(script)
    step = (t1 - t0) / (n1 - n0)
    times[i] = [t0 + step * (i - n0 - 1), t0 + step * (i - n0)]

print(f"casadas: {len(known)}/{len(script)}")
(here / "timings.json").write_text(json.dumps([[round(x, 3), round(y, 3)] for x, y in times]))
print("timings.json salvo")
