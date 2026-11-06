"""Tipografia comum ao site, ao PDF e ao carrossel: nada de viúvas, Bem-Querer nunca quebra."""
import re

ALVO_VIUVA = {'p', 'h1', 'h2', 'h3', 'h4', 'li', 'figcaption', 'dd', 'dt', 'blockquote', 'span', 'strong', 'em', 'small', 'b'}
VAZIAS = {'img', 'br', 'source', 'input', 'meta', 'link', 'hr', 'wbr', 'col', 'area', 'base', 'track', 'embed', 'param'}
CRUAS = {'script', 'style', 'title', 'textarea'}


def sem_viuvas(html):
    """Cola as duas últimas palavras de cada bloco de texto com espaço não separável,
    para nenhuma linha final ficar com uma palavra só; e impede a quebra de 'Bem-Querer'."""
    tok = re.split(r'(<[^>]+>)', html)
    pilha = []
    cru = None
    for i, t in enumerate(tok):
        if not t.startswith('<'):
            continue
        m = re.match(r'<\s*(/?)\s*([a-zA-Z0-9]+)', t)
        if not m:
            continue
        fecha, nome = m.group(1) == '/', m.group(2).lower()
        if cru:
            if fecha and nome == cru:
                cru = None
            continue
        if not fecha:
            if nome in CRUAS:
                cru = nome
            elif nome not in VAZIAS and not t.endswith('/>'):
                pilha.append((nome, i))
            continue
        # fechamento: acha a abertura correspondente
        while pilha and pilha[-1][0] != nome:
            pilha.pop()
        if not pilha:
            continue
        _, ini = pilha.pop()
        if nome not in ALVO_VIUVA:
            continue
        # texto do próprio bloco; o que está dentro de <span> filho já foi tratado
        # como bloco à parte (legenda + crédito, por exemplo)
        textos, dentro = [], 0
        for j in range(ini + 1, i):
            t2 = tok[j]
            if t2.startswith('<'):
                m2 = re.match(r'<\s*(/?)\s*span\b', t2)
                if m2:
                    dentro += -1 if m2.group(1) else 1
            elif dentro == 0:
                textos.append(j)
        visivel = re.sub(r'&[a-z]+;|&#\d+;', 'x', ''.join(tok[j] for j in textos)).strip()
        if len(visivel.split()) < 3:
            continue
        viu = False  # já passou por letra da última palavra?
        feito = False
        for j in reversed(textos):
            s = tok[j]
            k = len(s)
            while k > 0:
                c = s[k - 1]
                if c in ' \n\t\r':
                    if viu:
                        a = k - 1
                        while a > 0 and s[a - 1] in ' \n\t\r':
                            a -= 1
                        if a == 0 and not s[:a].strip() and j == textos[0]:
                            feito = True  # espaço inicial do bloco: nada a colar
                            break
                        cauda = (s[k:] + ''.join(tok[x] for x in textos if x > j)).strip()
                        antes = s[:a].replace('&nbsp;', ' ').split()[-1:] or ['']
                        if len(re.sub(r'&[a-z]+;|&#\d+;', 'x', antes[0] + ' ' + cauda)) <= 26:
                            # o trecho colado também não quebra no hífen (word joiner após cada hífen)
                            i0 = max(s.rfind(' ', 0, a), s.rfind('\n', 0, a)) + 1
                            tok[j] = s[:i0] + (s[i0:a] + '&nbsp;' + s[k:]).replace('-', '-&#8288;')
                        feito = True
                        break
                else:
                    viu = True
                k -= 1
            if feito:
                break
    # Bem-Querer nunca quebra no hífen (só em texto, nunca em atributo ou <title>)
    cru = None
    for i, t in enumerate(tok):
        if t.startswith('<'):
            m = re.match(r'<\s*(/?)\s*([a-zA-Z0-9]+)', t)
            if m and m.group(2).lower() in CRUAS:
                cru = None if m.group(1) else m.group(2).lower()
            continue
        if not cru and 'Bem-Querer' in t:
            tok[i] = t.replace('Bem-Querer', '<span class="nw">Bem-Querer</span>')
    return ''.join(tok)


CSS_TEXTO = "h1,h2,h3{text-wrap:balance}p,li,dd,figcaption,blockquote{text-wrap:pretty}.nw{white-space:nowrap}"
