# Junta cada cena (saida/cena-lamina-NN.json) com o montador em saida/codigo-NN.js,
# pronto para colar no use_figma (uma chamada por lâmina).
# uso: python3 -I figma/compacta.py ["<nome da página>"]   (com página: monta numa página própria, criada se não existir)
import json, pathlib, sys
F = pathlib.Path(__file__).resolve().parent
mont = (F / 'montador.js').read_text()
pagina = sys.argv[1] if len(sys.argv) > 1 else None
pre = ''
if pagina:
    nome = json.dumps(pagina, ensure_ascii=False)
    pre = (f'const PG=figma.root.children.find(p=>p.name==={nome})||(()=>{{const p=figma.createPage();p.name={nome};return p}})();'
           'await figma.setCurrentPageAsync(PG);\n')
for cena in sorted((F / 'saida').glob('cena-lamina-*.json')):
    n = int(cena.stem[-2:])
    S = json.dumps(json.loads(cena.read_text()), ensure_ascii=False, separators=(',', ':'))
    out = F / 'saida' / f'codigo-{n:02d}.js'
    out.write_text(pre + f'const S={S};const IDX={n - 1};\n' + mont)
    print(out.name, out.stat().st_size, 'bytes')
