# Contornos de "MIAU" na Archivo (largura 62, peso 900), em unidades da fonte, para o take do logo sendo desenhado.
# Saída: glifos.js  → GLIFOS = { upm, asc, desc, letras: [{ch, x (avanço acumulado), d}] }
import json, os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
f = TTFont(os.path.join(os.path.dirname(__file__), '../../../../fonts/Archivo-var-latin.woff2'))
print('eixos', [(a.axisTag, a.minValue, a.defaultValue, a.maxValue) for a in f['fvar'].axes])
f = instantiateVariableFont(f, {'wdth': 62, 'wght': 900})
gs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f['hmtx']
x, letras = 0, []
for ch in 'MIAU':
    g = cmap[ord(ch)]; pen = SVGPathPen(gs); gs[g].draw(pen)
    letras.append({'ch': ch, 'x': x, 'd': pen.getCommands()}); x += hmtx[g][0]
hh, os2 = f['hhea'], f['OS/2']
out = {'upm': f['head'].unitsPerEm, 'asc': hh.ascent, 'desc': -hh.descent, 'win': [os2.usWinAscent, os2.usWinDescent], 'typo': [os2.sTypoAscender, -os2.sTypoDescender], 'largura': x, 'letras': letras}
open(os.path.join(os.path.dirname(__file__), 'glifos.js'), 'w').write('const GLIFOS = ' + json.dumps(out) + ';\n')
print({k: v for k, v in out.items() if k != 'letras'})
