# Junta cada cena (saida/cena-lamina-NN.json) com o montador em saida/codigo-NN.js,
# pronto para colar no use_figma (uma chamada por lâmina).
# uso: python3 -I figma/compacta.py
import json, pathlib
F = pathlib.Path(__file__).resolve().parent
mont = (F / 'montador.js').read_text()
for cena in sorted((F / 'saida').glob('cena-lamina-*.json')):
    n = int(cena.stem[-2:])
    S = json.dumps(json.loads(cena.read_text()), ensure_ascii=False, separators=(',', ':'))
    out = F / 'saida' / f'codigo-{n:02d}.js'
    out.write_text(f'const S={S};const IDX={n - 1};\n' + mont)
    print(out.name, out.stat().st_size, 'bytes')
