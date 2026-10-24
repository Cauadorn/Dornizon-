# Ícones a traço (viewBox 12x12) para os símbolos do mapa da carta.
ICONES = {
 'pessoa': '<circle cx="6" cy="3.2" r="1.8"/><path d="M2.5 11 C 2.8 7.4, 4.2 6, 6 6 C 7.8 6, 9.2 7.4, 9.5 11"/>',
 'mao': '<path d="M3.5 11 V6.5 M3.5 7 V3.2 a.9 .9 0 0 1 1.8 0 V6 M5.3 6 V2.2 a.9 .9 0 0 1 1.8 0 V6 M7.1 6 V3 a.9 .9 0 0 1 1.8 0 V7.5 C 8.9 9.5, 8 11, 6 11 H3.5"/>',
 'coroa': '<path d="M1.5 9.5 L2 3.5 L4.3 6.5 L6 2.5 L7.7 6.5 L10 3.5 L10.5 9.5 Z M1.8 11 H10.2"/>',
 'roupa': '<path d="M4 1.5 L6 3 L8 1.5 L11 3.5 L9.6 5.5 L8.6 5 L9 11 H3 L3.4 5 L2.4 5.5 L1 3.5 Z"/>',
 'animal': '<path d="M1.5 6 C 2.5 4.5, 7 4.5, 8.5 5.5 L10 3.5 L10.8 5.5 L10 7 L8.8 7 M2.2 6.5 V10.5 M4.2 7 V10.5 M7 7 V10.5 M8.6 7 V10.5 M1.5 6 L1 8"/>',
 'ave': '<path d="M1 6 C 2.5 3.2, 4.8 3.4, 6 6 C 7.2 3.4, 9.5 3.2, 11 6 M6 6 L6 8.5"/>',
 'flor': '<circle cx="6" cy="6" r="1.2"/><circle cx="6" cy="2.9" r="1.6"/><circle cx="9" cy="5" r="1.6"/><circle cx="7.9" cy="8.6" r="1.6"/><circle cx="4.1" cy="8.6" r="1.6"/><circle cx="3" cy="5" r="1.6"/>',
 'arvore': '<circle cx="6" cy="4.5" r="3.4"/><path d="M6 7.9 V11.2 M4.2 11.2 H7.8"/>',
 'folha': '<path d="M2 10 C 2 4, 6 1.5, 10.5 1.5 C 10.5 6.5, 7.5 10, 2 10 Z M2 10 L7.5 4.5"/>',
 'agua': '<path d="M1 4.5 C 2.5 3.2, 3.5 5.8, 5 4.5 S 7.5 3.2, 9 4.5 S 10.5 5.5, 11 4.8 M1 8 C 2.5 6.7, 3.5 9.3, 5 8 S 7.5 6.7, 9 8 S 10.5 9, 11 8.3"/>',
 'nuvem': '<path d="M3 9.5 H9.2 a2 2 0 0 0 .2 -4 a2.8 2.8 0 0 0 -5.3 -.8 a2.4 2.4 0 0 0 -1.1 4.8 Z"/>',
 'sol': '<circle cx="6" cy="6" r="2.4"/><path d="M6 .8 V2.2 M6 9.8 V11.2 M.8 6 H2.2 M9.8 6 H11.2 M2.3 2.3 L3.3 3.3 M8.7 8.7 L9.7 9.7 M2.3 9.7 L3.3 8.7 M8.7 3.3 L9.7 2.3"/>',
 'lua': '<path d="M8.5 1.8 A4.6 4.6 0 1 0 10.2 8.6 A3.8 3.8 0 1 1 8.5 1.8 Z"/>',
 'estrela': '<path d="M6 1 L7.3 4.6 L11 4.7 L8.1 7 L9.1 10.8 L6 8.6 L2.9 10.8 L3.9 7 L1 4.7 L4.7 4.6 Z"/>',
 'montanha': '<path d="M.8 10.5 L4.5 3.5 L7 7.5 L8.5 5.5 L11.2 10.5 Z M3.6 5.2 L4.5 6 L5.3 5"/>',
 'castelo': '<path d="M2 11 V4 H3.5 V5.3 H5 V4 H7 V5.3 H8.5 V4 H10 V11 Z M5 11 V8.5 a1 1 0 0 1 2 0 V11"/>',
 'caminho': '<path d="M3 11 C 4.5 8, 5.2 5, 5.6 1.5 M9 11 C 7.5 8, 6.8 5, 6.4 1.5 M6 9.5 V8.5 M6 6.5 V5.8"/>',
 'barco': '<path d="M1 7.5 H11 L9.5 10 H2.5 Z M6 7.5 V1.5 L9.5 6 H6"/>',
 'taca': '<path d="M3 1.5 H9 C 9 5, 7.8 6.5, 6 6.8 C 4.2 6.5, 3 5, 3 1.5 Z M6 6.8 V9.5 M3.8 11 C 4.2 9.8, 7.8 9.8, 8.2 11 Z"/>',
 'bastao': '<path d="M3 11 L9 1 M6.8 4.6 C 8.4 4.6, 9.6 5.4, 10 6.4 C 8.6 6.6, 7.4 6, 6.8 4.6 Z M5.2 7.6 C 3.8 7.2, 2.8 7.6, 2.2 8.4 C 3.4 8.8, 4.6 8.6, 5.2 7.6 Z"/>',
 'espada': '<path d="M6 .8 L7 2.5 V7.5 H5 V2.5 Z M3 7.5 H9 M6 7.5 V10"/><circle cx="6" cy="10.8" r=".7"/>',
 'pentaculo': '<circle cx="6" cy="6" r="5"/><path d="M6 2 L8.4 9.2 L2.2 4.7 H9.8 L3.6 9.2 Z"/>',
 'coracao': '<path d="M6 10.8 C 1.5 7.8, 1 5.5, 1.5 4 C 2.2 1.8, 5 1.6, 6 3.8 C 7 1.6, 9.8 1.8, 10.5 4 C 11 5.5, 10.5 7.8, 6 10.8 Z"/>',
 'olho': '<path d="M1 6 C 3 2.8, 9 2.8, 11 6 C 9 9.2, 3 9.2, 1 6 Z"/><circle cx="6" cy="6" r="1.6"/>',
 'fogo': '<path d="M6 11 C 3 11, 2 8.6, 3 6.6 C 3.6 7.8, 4.4 7.8, 4.4 7.8 C 4 5.4, 5.2 3, 7 1.2 C 7 3.6, 10 5.4, 9.6 8 C 9.3 9.8, 7.8 11, 6 11 Z"/>',
 'trono': '<path d="M3.2 1.5 H8.8 V6.5 H3.2 Z M2.5 6.5 H9.5 V8 H2.5 Z M3 8 V11 M9 8 V11"/>',
 'numero': '<circle cx="6" cy="6" r="4.6"/><path d="M5 4.2 L6.3 3.4 V8.6"/>',
 'outro': '<path d="M6 1 L7 5 L11 6 L7 7 L6 11 L5 7 L1 6 L5 5 Z"/>',
 'ampulheta': '<path d="M2.5 1 H9.5 M2.5 11 H9.5 M3.3 1 C 3.3 4, 6 4.6, 6 6 C 6 7.4, 3.3 8, 3.3 11 M8.7 1 C 8.7 4, 6 4.6, 6 6 C 6 7.4, 8.7 8, 8.7 11 M4.6 10.2 C 5 9.2, 7 9.2, 7.4 10.2"/>',
 'cristal': '<path d="M3 4 L6 1 L9 4 L6 11 Z M3 4 H9 M6 1 L4.8 4 L6 11 L7.2 4 Z"/>',
}

def icone(nome, cls='ico'):
    g = ICONES.get(nome or 'outro', ICONES['outro'])
    return (f'<svg class="{cls}" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width=".9" '
            f'stroke-linejoin="round" stroke-linecap="round">{g}</svg>')
