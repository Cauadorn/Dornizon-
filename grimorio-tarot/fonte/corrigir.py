# Correções de rótulo no conteúdo transcrito (nome da cor trocado em relação à bolinha e ao texto).
# Uso: python3 -I corrigir.py  (edita dados/*.json no lugar)
import json, os
DIR = os.path.dirname(os.path.abspath(__file__))
def cor(naipe, pagina, idx, de, para):
    f = os.path.join(DIR, 'dados', naipe + '.json'); d = json.load(open(f, encoding='utf-8'))
    for c in d:
        if c['pagina_pdf'] == pagina and c['cores'][idx]['nome'] == de:
            c['cores'][idx]['nome'] = para; print(f'{c["nome"]}: {de} -> {para}')
    json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
cor('paus', 20, 0, 'Azul', 'Marrom')     # 7 de Paus: bolinha marrom, "conexão com a terra"
cor('ouros', 39, 1, 'Preto', 'Laranja')  # 6 de Ouros: bolinha laranja
cor('ouros', 40, 1, 'Preto', 'Laranja')  # 7 de Ouros: bolinha laranja
cor('ouros', 41, 1, 'Preto', 'Branco')   # 8 de Ouros: bolinha branca, "resultado iluminado"
# Ás de Ouros: rótulo "Solo" solto, sem texto
f = os.path.join(DIR, 'dados', 'ouros.json'); d = json.load(open(f, encoding='utf-8'))
for c in d: c['simbolos'] = [s for s in c['simbolos'] if s['texto'].strip()]
json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
