# Reel EMS: "provas"

Vídeo em motion 1080 × 1920 (reels), 30 fps, com as cores, fontes e grafismos do design system EMS. Todas as cenas são desenhadas em código (HTML/CSS/SVG), sem imagens de terceiros.

Conceito: a história acontece numa tela infinita de design. Cada trecho da narração é um quadro, e a câmera voa de um para o outro. Dois cursores dividem a tela: **voz** (lavanda) apaga, copia e sabota; **eu** (manteiga) desenha, refaz e no fim fala mais alto. No fechamento, a câmera abre e mostra todos os quadros juntos: todas as provas.

- `index.html`: roteiro (`BEATS`) e as cenas (`S.<cena>`). Abra com `?t=12` para ver um quadro, `?play=1` para assistir e `&cap=1` para ligar a legenda palavra por palavra.
- `render.mjs`: renderiza com o Chromium do Playwright e gera `reel-ems.mp4`.
- `sync.py`: lê a narração gravada e cria `timings.json` para cada animação bater com a palavra falada.

## Com a narração gravada

```
pip install faster-whisper
python3 sync.py narracao.m4a
node render.mjs --audio narracao.m4a
```

Sem `timings.json`, o ritmo é estimado (cerca de 1min40).
