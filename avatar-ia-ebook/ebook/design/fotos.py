"""Prompts das fotos dos pratos (gerados no Canva, proporção 2:1) e da capa (3:2).

Cada foto salva em fotos/NN.jpg (NN = número da receita) entra no lugar da imagem-guia quando o
build.py roda. Sem a foto, a página usa a guia "foto do prato".
"""

ESTILO = ("Porção pequena, sobre bancada de quartzo branco, luz natural de janela vindo da esquerda, ângulo de "
          "45 graus, fundo de cozinha clara desfocado, cores naturais, estilo foto de livro de receitas, sem "
          "texto, sem pessoas.")

PRATOS = {
    1: "omelete de caneca fofinha e dourada dentro de uma caneca branca grande, com pedacinhos de espinafre, "
       "tomate e queijo branco aparecendo, garfo ao lado",
    2: "crepioca dobrada ao meio num prato de cerâmica creme, recheada com queijo minas e rodelas de tomate, "
       "orégano por cima",
    3: "pote de vidro com overnight oats cremoso de aveia e iogurte, coberto de frutas vermelhas, colher ao lado",
    4: "pão de queijo de frigideira, um disco dourado e fofinho cortado em fatias num prato de cerâmica creme",
    5: "tigela de cerâmica com mingau de aveia cremoso, rodelas de banana e canela polvilhada por cima",
    6: "tapioca dobrada recheada com frango desfiado e requeijão cremoso escorrendo, num prato de cerâmica creme",
    7: "ovos mexidos cremosos com pedaços de ricota sobre uma fatia de pão integral tostado, cebolinha picada",
    8: "copo alto de vidro com vitamina de banana e cacau cremosa, banana e cacau em pó ao lado",
    9: "frigideira de ferro com cubos de frango dourado num molho cremoso de tomate e requeijão, salsinha por cima",
    10: "prato de cerâmica creme com carne moída refogada com cubos de abobrinha, cheiro-verde por cima",
    11: "fatia quadrada de omelete de forno com abobrinha, cenoura e espinafre, num prato, refratário ao fundo",
    12: "filé de tilápia dourado com rodelas de limão e brócolis no vapor num prato de cerâmica creme",
    13: "escondidinho de frango gratinado com purê de couve-flor e queijo dourado num refratário pequeno",
    14: "strogonoff de frango cremoso com champignon num prato fundo de cerâmica creme",
    15: "salada morna de atum, grão-de-bico, tomate, cebola roxa e ovos cozidos cortados em quartos numa tigela",
    16: "duas panquecas finas enroladas, recheadas com carne moída e cobertas de molho de tomate e orégano",
    17: "tigela de creme de abóbora laranja com frango desfiado e cheiro-verde por cima",
    18: "kaftas de carne grelhadas num prato com tigelinha de molho de iogurte com hortelã",
    19: "tropeiro de frango com feijão, ovo, couve e farinha de mandioca numa travessa de cerâmica",
    20: "frigideira pequena com ovos cozidos no molho de tomate, gemas inteiras, queijo branco e salsinha",
    21: "frango xadrez com pimentões verde e vermelho, cebola e amendoim num prato fundo",
    22: "abobrinhas cortadas ao meio recheadas com carne moída e mussarela gratinada numa assadeira",
    23: "camarões dourados no alho com fitas de abobrinha e salsinha num prato de cerâmica creme",
    24: "salpicão de frango com cenoura ralada, maçã e salsinha numa tigela de cerâmica",
    25: "wrap integral de atum com alface e tomate cortado ao meio, mostrando o recheio",
    26: "muffins salgados de frango dourados, seis unidades, dois num prato e o resto numa tábua",
    27: "ovos cozidos cortados ao meio recheados com pasta de atum, páprica e cebolinha por cima",
    28: "torrada de pão integral com ricota, rodelas de tomate e ovo frito por cima",
    29: "iscas de frango empanadas e crocantes numa travessa com tigelinha de molho de iogurte",
    30: "tigela de pasta de ricota com ervas cercada de palitos de cenoura e pepino",
    31: "hambúrguer de frango caseiro dourado num prato com folhas de alface e rodelas de tomate",
    32: "pizza de frigideira com massa de ovo, molho de tomate, frango desfiado, mussarela derretida e orégano",
    33: "três potinhos de vidro com mousse de cacau cremosa, cacau polvilhado por cima",
    34: "tigelinha de cerâmica com brigadeiro de colher cremoso e brilhante, colher ao lado",
    35: "bolo de caneca de banana fofinho dentro de uma caneca branca, rodelas de banana e canela",
    36: "três panquecas pequenas empilhadas cobertas com frutas vermelhas quentes",
    37: "dois potes de vidro com cheesecake em camadas: aveia tostada, creme branco e frutas vermelhas",
    38: "picolés de iogurte com pedaços de morango sobre gelo, morangos frescos ao lado",
    39: "maçã assada em cubos com creme de ricota e canela por cima numa tigelinha",
    40: "tigela de sorvete cremoso de banana com fio de pasta de amendoim por cima, colher ao lado",
}

CAPA = ("Fotografia de comida realista vista de cima, de uma mesa clara com vários pratos pequenos e proteicos "
        "lado a lado: omelete, tilápia com brócolis, frango cremoso, salada de atum com grão-de-bico e potinhos "
        "de mousse de cacau. Pratos de cerâmica creme e verde-sálvia, guardanapo de linho terracota, luz natural "
        "suave, cores naturais, estilo capa de livro de receitas, sem texto, sem pessoas.")


def prompt(numero):
    return f"Fotografia de comida realista: {PRATOS[numero]}. {ESTILO}"
