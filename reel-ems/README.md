# Reel EMS: "a voz"

Vídeo em motion 1080 × 1920 (reels), 30 fps, na identidade do design system EMS. Todas as cenas são desenhadas em código (HTML/CSS/SVG), sem imagens de terceiros.

- `index.html`: roteiro (`BEATS`) e as cenas (`S.<cena>`). Abra com `?t=12` para ver um quadro ou com `?play=1` para assistir.
- `render.mjs`: renderiza com o Chromium do Playwright e gera `reel-ems.mp4`.
- `sync.py`: lê a narração gravada e cria `timings.json` para cada animação bater com a palavra falada.

## Com a narração gravada

```
pip install faster-whisper
python3 sync.py narracao.m4a
node render.mjs --audio narracao.m4a
```

Sem `timings.json`, o ritmo é estimado (cerca de 1min40).
