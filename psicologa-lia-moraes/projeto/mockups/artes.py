# Gera artes.html com as artes planas das aplicações (cartão, aviso de porta, canecas, calendário).
# uso: python3 -I artes.py && node ../ferramentas/artes.cjs artes.html artes
import re, os, calendar
AQUI = os.path.dirname(os.path.abspath(__file__))
L = os.path.join(AQUI, '..', 'logo', 'final')

def svg(nome, cor, larg):
    s = open(os.path.join(L, nome)).read()
    s = re.sub(r'<rect[^>]*/>|<circle[^>]*/>', '', s)
    s = re.sub(r'<g fill="#[0-9A-Fa-f]{6}">', '<g fill="%s">' % cor, s)
    return s.replace('<svg ', '<svg style="width:%dpx;display:block" ' % larg)

MONO, VERT = 'lia-moraes-monograma.svg', 'lia-moraes-vertical.svg'
C, CREME, P, P2, C2 = '#2742C2', '#F5EEE3', '#F3C6A8', '#EDB592', '#3150CC'

# calendário: novembro de 2026 começa num domingo
semanas = calendar.Calendar(firstweekday=6).monthdayscalendar(2026, 11)
dias = ''.join('<span>%s</span>' % (d if d else '') for w in semanas for d in w)
cab = ''.join('<span class="sem">%s</span>' % d for d in 'DSTQQSS')

padrao = ''
for j, y in enumerate(range(-120, 1200, 330)):
    for x in range(-160 + (j % 2) * 210, 1800, 420):
        padrao += '<div class="tile" style="left:%dpx;top:%dpx">%s</div>' % (x, y, svg(MONO, P2, 230))

modelo = open(os.path.join(AQUI, 'artes-modelo.html')).read()
html = (modelo.replace('{{VERT_CREME_520}}', svg(VERT, CREME, 520))
              .replace('{{MONO_P2_900}}', svg(MONO, P2, 900))
              .replace('{{MONO_CREME_210}}', svg(MONO, CREME, 210))
              .replace('{{MONO_C2_1150}}', svg(MONO, C2, 1150))
              .replace('{{PADRAO}}', padrao)
              .replace('{{MONO_C_230}}', svg(MONO, C, 230))
              .replace('{{MONO_C2_1100}}', svg(MONO, C2, 1100))
              .replace('{{VERT_CREME_420}}', svg(VERT, CREME, 420))
              .replace('{{MONO_CREME_400}}', svg(MONO, CREME, 400))
              .replace('{{VERT_C_560}}', svg(VERT, C, 560))
              .replace('{{VERT_CREME_400}}', svg(VERT, CREME, 400))
              .replace('{{CAB}}', cab).replace('{{DIAS}}', dias))
open(os.path.join(AQUI, 'artes.html'), 'w').write(html)
print('ok')
