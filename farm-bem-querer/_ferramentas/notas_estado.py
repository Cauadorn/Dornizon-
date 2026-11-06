"""Notas de contexto por estado, usadas no site, no PDF, no carrossel e no Behance.
NOTA (vermelho, o da folha do símbolo): deixa claro o que a arte mostra quando ela pode ser mal lida.
CREDITO (vinho): de quem é o artesanato que inspirou a estampa e como ele entraria numa coleção de verdade.
FOTO_FORA: fotos de lugar que sugerem algo proibido ali e por isso não entram."""
import html

VERMELHO = '#C8321F'
NOTA = {
    'sc': ('Garopaba já foi armação baleeira. Desde 1987 a caça é proibida no Brasil, e hoje a baleia-franca volta '
           'todo inverno para ter filhote, vista da areia. A tarrafa secando na praia é a da pesca artesanal.'),
}
CREDITO = {
    'ce': ('A renda de bilro é das rendeiras de Aquiraz, Prainha e Trairi. Numa coleção de verdade, ela entraria '
           'em parceria com elas, com o nome de cada uma e pagamento justo.'),
    'pa': ('Os brinquedos de miriti são dos artesãos de Abaetetuba. Numa coleção de verdade, eles entrariam em '
           'parceria, com crédito no nome. O Círio fica de fora: é devoção.'),
    'ma': ('O bordado do boi é feito por bordadeiras, e cada couro tem autoria. Aqui o bordado foi criado para a '
           'coleção, inspirado na técnica, sem copiar nenhum boi. O Bumba-meu-boi é patrimônio da humanidade.'),
    'to': ('O capim dourado é trançado pelas artesãs do Jalapão, como as da comunidade quilombola Mumbuca, e tem '
           'indicação geográfica. A colheita só acontece depois da floração. Numa coleção de verdade, entraria com elas.'),
}
# a pedra dentro do rio de Bonito, o recife das piscinas naturais e o monte de capim dourado colhido
FOTO_FORA = {'ms-lugar-2.jpg', 'pe-lugar-2.jpg', 'to-lugar-1.jpg'}


def notas_html(uf, esc=html.escape):
    h = ''
    if uf in NOTA:
        h += f'<p class="nota-v">{esc(NOTA[uf])}</p>'
    if uf in CREDITO:
        h += f'<p class="nota-v nota-c">{esc(CREDITO[uf])}</p>'
    return h
