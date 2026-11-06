"""Gera o texto do ebook "Prato Pequeno, Proteína Grande" (ebook.md).

Cada receita lista os ingredientes em gramas; a proteína e as calorias por porção são calculadas com a
tabela abaixo (por 100 g). Para mudar uma receita, edite aqui e rode:

    python3 receitas.py

Valores por 100 g: TACO (Unicamp, 4ª ed.) quando o alimento está lá; USDA FoodData Central ou rótulo
médio de mercado quando não está (marcados com *). São aproximados: a nutricionista deve conferir.
"""

from pathlib import Path

# alimento: (kcal, proteína g) por 100 g
ALIMENTOS = {
    "ovo": (143, 13.0),
    "clara": (52, 10.9),  # *
    "frango_cru": (119, 21.5),
    "frango_cozido": (163, 31.5),
    "patinho_cru": (133, 21.7),
    "tilapia_crua": (96, 20.1),  # *
    "camarao_cru": (85, 20.1),  # *
    "atum_agua": (116, 25.5),  # * escorrido
    "iogurte_natural": (51, 4.1),
    "leite_desnatado": (35, 3.3),
    "leite_po_desnatado": (362, 34.7),
    "ricota": (140, 12.6),
    "cottage": (90, 11.0),  # *
    "minas_frescal": (264, 17.4),
    "mussarela": (330, 22.6),
    "parmesao": (453, 35.6),
    "requeijao_light": (190, 10.0),  # * rótulo médio
    "aveia": (394, 13.9),
    "goma_tapioca": (240, 0.0),  # * goma hidratada
    "pao_integral": (253, 9.4),
    "wrap_integral": (290, 8.0),  # * rótulo médio
    "grao_de_bico_cozido": (164, 8.9),  # *
    "feijao_cozido": (76, 4.8),
    "farinha_mandioca": (365, 1.2),
    "amido_milho": (361, 0.6),
    "abobora_cozida": (48, 1.4),
    "couve_flor_cozida": (19, 1.2),
    "abobrinha": (19, 1.1),
    "espinafre": (16, 2.0),
    "alface": (11, 1.3),
    "pepino": (10, 0.9),
    "tomate": (15, 1.1),
    "cebola": (39, 1.7),
    "pimentao": (21, 1.1),
    "cenoura": (34, 1.3),
    "champignon": (25, 1.9),  # * em conserva
    "couve": (27, 2.9),
    "brocolis_cozido": (25, 2.1),
    "molho_tomate": (32, 1.5),  # * passata
    "banana": (98, 1.3),
    "maca": (56, 0.3),
    "morango": (30, 0.9),
    "frutas_vermelhas": (45, 0.8),  # *
    "chia": (486, 16.5),  # *
    "pasta_amendoim": (588, 25.0),  # *
    "amendoim": (590, 24.0),  # *
    "cacau": (228, 19.6),  # *
    "gelatina_incolor": (335, 85.6),  # *
    "azeite": (884, 0.0),
    "shoyu": (53, 8.1),  # *
}

# Como cada alimento aparece na lista de despensa.
NOME_DESPENSA = {
    "ovo": "Ovos", "clara": "Ovos", "frango_cru": "Peito de frango", "frango_cozido": "Peito de frango",
    "patinho_cru": "Patinho moído", "tilapia_crua": "Filé de tilápia", "camarao_cru": "Camarão limpo",
    "atum_agua": "Atum em lata (em água)", "iogurte_natural": "Iogurte natural",
    "leite_desnatado": "Leite desnatado", "leite_po_desnatado": "Leite em pó desnatado",
    "ricota": "Ricota", "cottage": "Queijo cottage", "minas_frescal": "Queijo minas frescal",
    "mussarela": "Mussarela", "parmesao": "Parmesão ralado", "requeijao_light": "Requeijão light",
    "aveia": "Aveia em flocos", "goma_tapioca": "Goma de tapioca", "pao_integral": "Pão integral",
    "wrap_integral": "Wrap integral", "grao_de_bico_cozido": "Grão-de-bico",
    "feijao_cozido": "Feijão carioca", "farinha_mandioca": "Farinha de mandioca",
    "amido_milho": "Amido de milho", "abobora_cozida": "Abóbora cabotiá", "couve_flor_cozida": "Couve-flor",
    "abobrinha": "Abobrinha", "espinafre": "Espinafre", "alface": "Alface", "pepino": "Pepino",
    "tomate": "Tomate", "cebola": "Cebola", "pimentao": "Pimentão", "cenoura": "Cenoura",
    "champignon": "Champignon em conserva", "couve": "Couve", "brocolis_cozido": "Brócolis",
    "molho_tomate": "Molho de tomate (passata)", "banana": "Banana", "maca": "Maçã", "morango": "Morango",
    "frutas_vermelhas": "Frutas vermelhas congeladas", "chia": "Chia", "pasta_amendoim": "Pasta de amendoim",
    "amendoim": "Amendoim torrado sem sal", "cacau": "Cacau em pó 100%",
    "gelatina_incolor": "Gelatina incolor sem sabor", "azeite": "Azeite", "shoyu": "Shoyu",
}

GRUPOS_DESPENSA = {
    "Proteínas": ["ovo", "frango_cru", "patinho_cru", "tilapia_crua", "camarao_cru", "atum_agua"],
    "Laticínios": ["iogurte_natural", "leite_desnatado", "leite_po_desnatado", "ricota", "cottage",
                   "minas_frescal", "mussarela", "parmesao", "requeijao_light"],
    "Grãos e farinhas": ["aveia", "goma_tapioca", "pao_integral", "wrap_integral", "grao_de_bico_cozido",
                         "feijao_cozido", "farinha_mandioca", "amido_milho", "chia"],
    "Hortifrúti": ["abobora_cozida", "couve_flor_cozida", "abobrinha", "espinafre", "alface", "pepino",
                   "tomate", "cebola", "pimentao", "cenoura", "couve", "brocolis_cozido", "banana", "maca",
                   "morango", "frutas_vermelhas"],
    "Despensa": ["molho_tomate", "champignon", "pasta_amendoim", "amendoim", "cacau", "gelatina_incolor",
                 "azeite", "shoyu"],
}

CAPITULOS = {
    "cafe": "Café da manhã",
    "refeicao": "Almoço e jantar",
    "lanche": "Lanches",
    "doce": "Doces",
}


def R(nome, cap, porcoes, tempo, ingredientes, temperos, passos, dica=None, congela=None):
    return dict(nome=nome, cap=cap, porcoes=porcoes, tempo=tempo, ingredientes=ingredientes,
                temperos=temperos, passos=passos, dica=dica, congela=congela)


# ingredientes: (alimento, gramas, como aparece na receita)
RECEITAS = [
    # ---------------------------------------------------------------- café da manhã
    R("Omelete de caneca", "cafe", 1, "4 min",
      [("ovo", 100, "2 ovos"),
       ("cottage", 30, "2 colheres de sopa de cottage (30 g)"),
       ("minas_frescal", 30, "1 fatia média de queijo minas frescal picada (30 g)"),
       ("espinafre", 20, "1 punhado de espinafre picado"),
       ("tomate", 50, "1/2 tomate picado")],
      "Sal, pimenta-do-reino e orégano a gosto; óleo em spray para untar",
      ["Unte uma caneca grande e bata os ovos com um garfo dentro dela.",
       "Misture o cottage, o queijo, o espinafre, o tomate e os temperos.",
       "Leve ao micro-ondas por 1 minuto, mexa e volte por mais 1 minuto a 1min30, até firmar."],
      dica="A caneca precisa ser grande: o ovo sobe no micro-ondas e depois baixa."),

    R("Crepioca de queijo", "cafe", 1, "7 min",
      [("ovo", 50, "1 ovo"),
       ("clara", 66, "2 claras"),
       ("goma_tapioca", 30, "2 colheres de sopa de goma de tapioca (30 g)"),
       ("minas_frescal", 40, "40 g de queijo minas frescal"),
       ("tomate", 50, "1/2 tomate em rodelas")],
      "Sal e orégano a gosto",
      ["Bata o ovo, as claras, a goma e uma pitada de sal com um garfo.",
       "Despeje numa frigideira antiaderente untada, em fogo médio, e tampe por 2 minutos.",
       "Vire, coloque o queijo e o tomate numa metade, dobre e deixe mais 1 minuto para o queijo amolecer."]),

    R("Overnight oats de pote", "cafe", 1, "5 min + 1 noite na geladeira",
      [("aveia", 30, "3 colheres de sopa de aveia em flocos (30 g)"),
       ("iogurte_natural", 170, "1 pote de iogurte natural (170 g)"),
       ("leite_po_desnatado", 20, "2 colheres de sopa de leite em pó desnatado (20 g)"),
       ("chia", 10, "1 colher de sopa de chia (10 g)"),
       ("frutas_vermelhas", 50, "1/2 xícara de frutas vermelhas (50 g)")],
      "Canela e adoçante a gosto",
      ["Num pote com tampa, misture a aveia, o iogurte, o leite em pó, a chia, a canela e o adoçante.",
       "Cubra com as frutas vermelhas, tampe e deixe na geladeira de um dia para o outro.",
       "Coma gelado, direto do pote."],
      dica="Faça 3 potes de uma vez no domingo: duram até 3 dias na geladeira."),

    R("Pão de queijo de frigideira", "cafe", 1, "8 min",
      [("ovo", 50, "1 ovo"),
       ("clara", 33, "1 clara"),
       ("goma_tapioca", 30, "2 colheres de sopa de goma de tapioca (30 g)"),
       ("cottage", 40, "2 colheres de sopa cheias de cottage (40 g)"),
       ("parmesao", 6, "1 colher de sopa de parmesão ralado")],
      "1 pitada de sal",
      ["Bata tudo com um garfo até virar uma massa mole.",
       "Despeje numa frigideira pequena antiaderente untada, em fogo baixo.",
       "Tampe e deixe 3 minutos de cada lado, até dourar."]),

    R("Mingau de aveia com ovo", "cafe", 1, "6 min",
      [("aveia", 30, "3 colheres de sopa de aveia em flocos (30 g)"),
       ("leite_desnatado", 200, "1 xícara de leite desnatado (200 ml)"),
       ("ovo", 50, "1 ovo"),
       ("banana", 50, "1/2 banana amassada")],
      "Canela a gosto",
      ["Leve o leite, a aveia e a banana ao fogo baixo, mexendo, por 3 minutos.",
       "Desligue. Bata o ovo à parte e junte ao mingau mexendo rápido.",
       "Volte ao fogo por 1 minuto sem parar de mexer. Sirva com canela."],
      dica="Ninguém percebe o ovo: ele só deixa o mingau mais cremoso e mais proteico."),

    R("Tapioca de frango com requeijão", "cafe", 1, "6 min",
      [("goma_tapioca", 40, "3 colheres de sopa de goma de tapioca (40 g)"),
       ("frango_cozido", 60, "60 g de frango cozido desfiado"),
       ("requeijao_light", 20, "1 colher de sopa de requeijão light")],
      "Orégano a gosto",
      ["Espalhe a goma numa frigideira antiaderente fria e leve ao fogo médio até as bordas soltarem.",
       "Vire e espalhe o requeijão e o frango numa metade.",
       "Dobre e deixe mais 1 minuto."],
      dica="Deixe frango desfiado pronto na geladeira: serve aqui, no wrap e na pizza de frigideira."),

    R("Ovos mexidos cremosos com ricota", "cafe", 1, "5 min",
      [("ovo", 100, "2 ovos"),
       ("ricota", 30, "2 colheres de sopa de ricota esfarelada (30 g)"),
       ("pao_integral", 25, "1 fatia de pão integral")],
      "Sal, pimenta-do-reino e cebolinha a gosto",
      ["Bata os ovos com sal e leve a uma frigideira antiaderente em fogo baixo.",
       "Mexa devagar com uma espátula. Quando estiverem quase firmes, junte a ricota.",
       "Desligue (eles terminam no calor da panela) e sirva sobre o pão tostado com cebolinha."]),

    R("Vitamina de banana e cacau", "cafe", 1, "3 min",
      [("leite_desnatado", 200, "1 copo de leite desnatado gelado (200 ml)"),
       ("banana", 70, "1 banana pequena"),
       ("cacau", 6, "1 colher de sopa de cacau em pó 100%"),
       ("leite_po_desnatado", 20, "2 colheres de sopa de leite em pó desnatado (20 g)")],
      "Gelo e adoçante a gosto",
      ["Bata tudo no liquidificador por 1 minuto.",
       "Sirva na hora."],
      dica="Banana congelada em rodelas deixa a vitamina com textura de milk-shake."),

    # ---------------------------------------------------------------- almoço e jantar
    R("Frango cremoso de frigideira", "refeicao", 2, "15 min",
      [("frango_cru", 250, "250 g de peito de frango em cubos"),
       ("cebola", 50, "1/2 cebola picada"),
       ("tomate", 100, "1 tomate picado"),
       ("requeijao_light", 45, "3 colheres de sopa de requeijão light"),
       ("azeite", 5, "1 colher de chá de azeite")],
      "Alho, sal, páprica e salsinha a gosto",
      ["Tempere o frango com sal, alho e páprica.",
       "Doure no azeite em fogo alto por 5 a 6 minutos.",
       "Junte a cebola e o tomate e cozinhe por 3 minutos.",
       "Desligue o fogo, misture o requeijão e finalize com salsinha."],
      dica="Sirva com legumes no vapor ou uma colher de arroz."),

    R("Carne moída com abobrinha", "refeicao", 2, "15 min",
      [("patinho_cru", 250, "250 g de patinho moído"),
       ("abobrinha", 200, "1 abobrinha média em cubos"),
       ("cebola", 50, "1/2 cebola picada"),
       ("tomate", 100, "1 tomate picado"),
       ("azeite", 5, "1 colher de chá de azeite")],
      "Alho, sal, cominho e cheiro-verde a gosto",
      ["Doure a carne no azeite em fogo alto, soltando bem com a colher.",
       "Junte a cebola, o alho e o tomate e refogue por 2 minutos.",
       "Acrescente a abobrinha e os temperos e cozinhe tampado por 5 minutos (ela deve ficar al dente)."],
      congela="Congela em porções por até 2 meses."),

    R("Omelete de forno de legumes", "refeicao", 3, "30 min (25 no forno)",
      [("ovo", 300, "6 ovos"),
       ("ricota", 100, "100 g de ricota esfarelada"),
       ("parmesao", 30, "3 colheres de sopa de parmesão ralado"),
       ("abobrinha", 200, "1 abobrinha ralada"),
       ("cenoura", 100, "1 cenoura ralada"),
       ("cebola", 50, "1/2 cebola picada"),
       ("espinafre", 30, "1 punhado de espinafre")],
      "Sal e pimenta-do-reino a gosto",
      ["Preaqueça o forno a 200 °C e unte um refratário de uns 20 × 20 cm.",
       "Bata os ovos e misture todos os outros ingredientes.",
       "Despeje no refratário e asse por 25 minutos, até dourar e firmar no centro."],
      congela="Corte em 3 e congele em potes separados."),

    R("Tilápia de frigideira com limão", "refeicao", 1, "12 min",
      [("tilapia_crua", 150, "1 filé de tilápia (150 g)"),
       ("azeite", 5, "1 colher de chá de azeite"),
       ("brocolis_cozido", 100, "1 xícara de brócolis")],
      "Sal, alho, páprica e limão a gosto",
      ["Tempere o peixe com sal, alho, páprica e limão.",
       "Aqueça bem a frigideira com o azeite e coloque o filé. Não mexa por 3 a 4 minutos.",
       "Vire com cuidado e deixe mais 3 minutos.",
       "Cozinhe o brócolis no vapor ou no micro-ondas com um pouco de água por 3 minutos."],
      dica="Peixe gruda quando a frigideira está fria ou quando você mexe antes da hora."),

    R("Escondidinho de frango com couve-flor", "refeicao", 3, "25 min",
      [("couve_flor_cozida", 400, "1 couve-flor pequena cozida (400 g)"),
       ("requeijao_light", 45, "3 colheres de sopa de requeijão light"),
       ("frango_cozido", 200, "200 g de frango cozido desfiado"),
       ("cebola", 50, "1/2 cebola picada"),
       ("tomate", 100, "1 tomate picado"),
       ("mussarela", 40, "40 g de mussarela ralada")],
      "Sal, alho e noz-moscada a gosto",
      ["Cozinhe a couve-flor até ficar bem macia e amasse (ou processe) com o requeijão, sal e noz-moscada.",
       "Refogue o frango com a cebola, o alho e o tomate por 3 minutos.",
       "Num refratário, faça uma camada de frango, cubra com o purê e espalhe a mussarela.",
       "Gratine no forno a 200 °C ou na air fryer por 10 minutos."],
      congela="Congela montado, em potes individuais."),

    R("Strogonoff de frango com iogurte", "refeicao", 3, "20 min",
      [("frango_cru", 400, "400 g de peito de frango em tiras"),
       ("cebola", 50, "1/2 cebola picada"),
       ("champignon", 100, "1 vidro pequeno de champignon fatiado (100 g)"),
       ("molho_tomate", 60, "3 colheres de sopa de molho de tomate"),
       ("iogurte_natural", 170, "1 pote de iogurte natural (170 g)"),
       ("azeite", 5, "1 colher de chá de azeite")],
      "1 colher de sopa de mostarda, sal e alho a gosto",
      ["Doure o frango no azeite em fogo alto.",
       "Junte a cebola e o alho, depois o champignon, o molho de tomate e a mostarda. Cozinhe 3 minutos.",
       "Desligue o fogo, espere 1 minuto e só então misture o iogurte."],
      dica="O segredo é desligar o fogo antes do iogurte: se ferver, ele talha."),

    R("Salada morna de atum e grão-de-bico", "refeicao", 2, "15 min",
      [("atum_agua", 120, "1 lata de atum em água, escorrido (120 g)"),
       ("grao_de_bico_cozido", 160, "1 xícara de grão-de-bico cozido (160 g)"),
       ("ovo", 100, "2 ovos cozidos"),
       ("tomate", 100, "1 tomate picado"),
       ("cebola", 25, "1/4 de cebola roxa fatiada fina"),
       ("azeite", 5, "1 colher de chá de azeite")],
      "Alho, sal, limão e salsinha a gosto",
      ["Cozinhe os ovos por 10 minutos, esfrie e corte em quartos.",
       "Aqueça o grão-de-bico numa frigideira com o azeite e o alho por 2 minutos.",
       "Misture com o atum, o tomate e a cebola. Tempere com limão, sal e salsinha e cubra com os ovos."],
      dica="Grão-de-bico em conserva, bem lavado, resolve em dia corrido."),

    R("Panqueca de carne com massa de ovo", "refeicao", 1, "15 min",
      [("ovo", 100, "2 ovos"),
       ("aveia", 10, "1 colher de sopa de aveia em flocos finos"),
       ("patinho_cru", 100, "100 g de patinho moído"),
       ("molho_tomate", 40, "2 colheres de sopa de molho de tomate"),
       ("cebola", 20, "1 colher de sopa de cebola picada")],
      "Sal, alho e orégano a gosto",
      ["Refogue a carne com a cebola, o alho e metade do molho de tomate.",
       "Bata os ovos com a aveia e uma pitada de sal.",
       "Faça 2 discos finos numa frigideira antiaderente untada, 1 minuto de cada lado.",
       "Recheie, enrole e cubra com o resto do molho e orégano."]),

    R("Creme de abóbora com frango", "refeicao", 3, "25 min",
      [("abobora_cozida", 500, "500 g de abóbora cabotiá descascada em cubos"),
       ("cebola", 50, "1/2 cebola"),
       ("frango_cozido", 200, "200 g de frango cozido desfiado"),
       ("requeijao_light", 45, "3 colheres de sopa de requeijão light")],
      "2 dentes de alho, sal e cheiro-verde a gosto; 500 ml de água",
      ["Cozinhe a abóbora com a cebola, o alho e a água por 15 minutos, até desmanchar.",
       "Bata no liquidificador com o requeijão.",
       "Volte à panela, junte o frango, acerte o sal e aqueça por 2 minutos. Finalize com cheiro-verde."],
      congela="Congela por até 3 meses."),

    R("Kafta de frigideira com molho de iogurte", "refeicao", 3, "20 min",
      [("patinho_cru", 400, "400 g de patinho moído"),
       ("cebola", 50, "1/2 cebola ralada"),
       ("iogurte_natural", 170, "1 pote de iogurte natural (170 g), para o molho"),
       ("azeite", 5, "1 colher de chá de azeite")],
      "Hortelã, salsinha, cominho, sal, alho e limão a gosto",
      ["Misture a carne com a cebola, hortelã e salsinha picadas, cominho e sal.",
       "Modele 9 kaftas compridas.",
       "Doure na frigideira com o azeite, 4 minutos de cada lado.",
       "Para o molho, misture o iogurte com limão, alho amassado, hortelã e sal."],
      congela="Congele as kaftas cruas, separadas por papel-manteiga."),

    R("Tropeiro de frango", "refeicao", 3, "20 min",
      [("frango_cozido", 200, "200 g de frango cozido desfiado"),
       ("feijao_cozido", 300, "2 xícaras de feijão carioca cozido e escorrido (300 g)"),
       ("ovo", 100, "2 ovos"),
       ("couve", 60, "2 folhas de couve fatiadas fino"),
       ("cebola", 50, "1/2 cebola picada"),
       ("farinha_mandioca", 30, "3 colheres de sopa de farinha de mandioca"),
       ("azeite", 5, "1 colher de chá de azeite")],
      "Alho, sal e cheiro-verde a gosto",
      ["Refogue a cebola e o alho no azeite.",
       "Quebre os ovos na panela e mexa até firmar.",
       "Junte o frango e o feijão e cozinhe por 3 minutos. Acrescente a couve por 1 minuto.",
       "Desligue e misture a farinha aos poucos. Finalize com cheiro-verde."]),

    R("Ovos no molho de tomate", "refeicao", 1, "15 min",
      [("molho_tomate", 200, "1 xícara de molho de tomate (200 g)"),
       ("cebola", 25, "1/4 de cebola picada"),
       ("pimentao", 30, "1/4 de pimentão picado"),
       ("ovo", 100, "2 ovos"),
       ("minas_frescal", 30, "30 g de queijo minas frescal esfarelado")],
      "Cominho, páprica, sal e salsinha a gosto",
      ["Numa frigideira pequena, refogue a cebola e o pimentão em 2 colheres de sopa do próprio molho.",
       "Junte o resto do molho e os temperos e cozinhe por 5 minutos.",
       "Abra 2 espaços no molho, quebre um ovo em cada, tampe e deixe 5 a 6 minutos.",
       "Finalize com o queijo e salsinha."],
      dica="Gema mole: 5 minutos. Gema firme: 7."),

    R("Frango xadrez rápido", "refeicao", 3, "20 min",
      [("frango_cru", 400, "400 g de peito de frango em cubos"),
       ("pimentao", 120, "1/2 pimentão verde e 1/2 vermelho em quadrados"),
       ("cebola", 100, "1 cebola em pétalas"),
       ("shoyu", 30, "2 colheres de sopa de shoyu"),
       ("amido_milho", 10, "1 colher de sopa de amido de milho"),
       ("amendoim", 20, "2 colheres de sopa de amendoim torrado sem sal"),
       ("azeite", 5, "1 colher de chá de azeite")],
      "Alho e gengibre ralado a gosto; 1/2 xícara de água",
      ["Doure o frango no azeite em fogo alto.",
       "Junte alho, gengibre, pimentões e cebola e salteie por 3 minutos (eles devem ficar crocantes).",
       "Dissolva o amido na água com o shoyu, despeje e mexa por 1 minuto, até engrossar.",
       "Sirva com o amendoim por cima."]),

    R("Abobrinha recheada com carne", "refeicao", 2, "25 min",
      [("abobrinha", 400, "2 abobrinhas médias"),
       ("patinho_cru", 200, "200 g de patinho moído"),
       ("cebola", 50, "1/2 cebola picada"),
       ("tomate", 100, "1 tomate picado"),
       ("mussarela", 40, "40 g de mussarela ralada")],
      "Alho, sal e orégano a gosto",
      ["Corte as abobrinhas ao meio no comprimento e tire o miolo com uma colher. Pique o miolo.",
       "Refogue a carne com a cebola, o alho, o tomate e o miolo picado por 5 minutos.",
       "Recheie as abobrinhas e cubra com a mussarela e orégano.",
       "Asse na air fryer a 180 °C por 12 minutos ou no forno a 200 °C por 15 a 20 minutos."]),

    R("Camarão no alho com abobrinha em fita", "refeicao", 1, "12 min",
      [("camarao_cru", 150, "150 g de camarão limpo"),
       ("abobrinha", 200, "1 abobrinha cortada em fitas com descascador"),
       ("azeite", 5, "1 colher de chá de azeite")],
      "3 dentes de alho fatiados, sal, limão, salsinha e pimenta calabresa a gosto",
      ["Doure o alho no azeite por 30 segundos.",
       "Junte o camarão e deixe 2 minutos de cada lado, até ficar rosado. Retire.",
       "Na mesma frigideira, salteie a abobrinha por 2 minutos.",
       "Volte o camarão, tempere com limão, sal e salsinha."],
      dica="Camarão passa do ponto rápido: rosado e curvado em C está pronto."),

    R("Salpicão leve de frango", "refeicao", 3, "15 min",
      [("frango_cozido", 300, "300 g de frango cozido desfiado"),
       ("iogurte_natural", 170, "1 pote de iogurte natural (170 g)"),
       ("cenoura", 100, "1 cenoura ralada"),
       ("maca", 130, "1 maçã picada com casca")],
      "1 colher de sopa de mostarda, limão, sal e salsinha a gosto",
      ["Misture o iogurte com a mostarda, limão e sal.",
       "Junte o frango, a cenoura e a maçã.",
       "Finalize com salsinha e sirva gelado."],
      dica="Dura 3 dias na geladeira e vira recheio de wrap ou de pão integral."),

    # ---------------------------------------------------------------- lanches
    R("Wrap de atum", "lanche", 1, "5 min",
      [("wrap_integral", 40, "1 wrap integral"),
       ("atum_agua", 60, "1/2 lata de atum em água, escorrido"),
       ("requeijao_light", 20, "1 colher de sopa de requeijão light"),
       ("alface", 20, "2 folhas de alface"),
       ("tomate", 50, "1/2 tomate em rodelas")],
      "Limão e pimenta-do-reino a gosto",
      ["Misture o atum com o requeijão, limão e pimenta.",
       "Espalhe no wrap com a alface e o tomate.",
       "Enrole bem apertado e aqueça 1 minuto de cada lado numa frigideira seca, se quiser."]),

    R("Muffin salgado de frango", "lanche", 3, "25 min",
      [("ovo", 150, "3 ovos"),
       ("frango_cozido", 150, "150 g de frango cozido desfiado"),
       ("ricota", 50, "3 colheres de sopa de ricota"),
       ("aveia", 30, "3 colheres de sopa de aveia em flocos"),
       ("cenoura", 50, "1/2 cenoura ralada"),
       ("cebola", 25, "1/4 de cebola picada")],
      "1 colher de chá de fermento em pó, sal e orégano a gosto",
      ["Misture tudo, deixando o fermento por último.",
       "Distribua em 6 forminhas de silicone.",
       "Asse na air fryer a 170 °C por 15 minutos ou no forno a 180 °C por 20 minutos."],
      dica="Rende 6 muffins; a porção é 2.",
      congela="Congela por até 2 meses. Aqueça na air fryer."),

    R("Ovos recheados com atum", "lanche", 1, "15 min",
      [("ovo", 100, "2 ovos"),
       ("atum_agua", 30, "1/4 de lata de atum em água, escorrido"),
       ("iogurte_natural", 20, "1 colher de sopa de iogurte natural")],
      "1 colher de chá de mostarda, páprica e cebolinha a gosto",
      ["Cozinhe os ovos por 10 minutos e passe para água fria.",
       "Descasque, corte ao meio e retire as gemas.",
       "Amasse as gemas com o atum, o iogurte e a mostarda.",
       "Recheie as claras e finalize com páprica e cebolinha."]),

    R("Torrada de ricota, tomate e ovo", "lanche", 1, "8 min",
      [("pao_integral", 25, "1 fatia de pão integral"),
       ("ricota", 50, "3 colheres de sopa de ricota"),
       ("ovo", 50, "1 ovo"),
       ("tomate", 50, "1/2 tomate em rodelas")],
      "Sal, pimenta-do-reino e orégano a gosto",
      ["Toste o pão.",
       "Amasse a ricota com sal e orégano e espalhe no pão.",
       "Cubra com o tomate e um ovo frito na frigideira antiaderente sem óleo."]),

    R("Iscas de frango crocantes na air fryer", "lanche", 3, "20 min",
      [("frango_cru", 300, "300 g de peito de frango em tiras"),
       ("ovo", 50, "1 ovo batido"),
       ("aveia", 40, "4 colheres de sopa de aveia em flocos finos"),
       ("parmesao", 6, "1 colher de sopa de parmesão ralado")],
      "Sal, páprica e alho em pó a gosto",
      ["Tempere as tiras de frango.",
       "Passe no ovo e depois na mistura de aveia com parmesão e páprica.",
       "Asse na air fryer a 200 °C por 12 a 15 minutos, virando na metade."],
      dica="Molho rápido: iogurte natural com limão, alho e sal."),

    R("Pasta de ricota com ervas e palitos", "lanche", 1, "5 min",
      [("ricota", 100, "100 g de ricota"),
       ("iogurte_natural", 20, "1 colher de sopa de iogurte natural"),
       ("cenoura", 80, "1/2 cenoura em palitos"),
       ("pepino", 80, "1/2 pepino em palitos")],
      "Cebolinha, salsinha, limão, sal e pimenta-do-reino a gosto",
      ["Amasse a ricota com o iogurte até ficar cremosa.",
       "Misture as ervas picadas, limão, sal e pimenta.",
       "Sirva com os palitos de legumes."]),

    R("Hambúrguer de frango caseiro", "lanche", 5, "20 min",
      [("frango_cru", 500, "500 g de peito de frango moído"),
       ("ovo", 50, "1 ovo"),
       ("cebola", 50, "1/2 cebola ralada"),
       ("aveia", 20, "2 colheres de sopa de aveia em flocos finos")],
      "Alho, páprica defumada, salsinha e sal a gosto",
      ["Misture tudo com as mãos (ou bata o peito no processador, se comprou inteiro).",
       "Faça 5 bolas e achate em discos.",
       "Doure em frigideira untada, 4 a 5 minutos de cada lado, ou na air fryer a 180 °C por 12 minutos."],
      dica="Rende 5 hambúrgueres; a porção é 1. Fica ótimo no pão integral com alface e tomate.",
      congela="Congele cru, separado por papel-manteiga."),

    R("Pizza de frigideira", "lanche", 1, "10 min",
      [("ovo", 100, "2 ovos"),
       ("goma_tapioca", 15, "1 colher de sopa de goma de tapioca"),
       ("molho_tomate", 40, "2 colheres de sopa de molho de tomate"),
       ("mussarela", 30, "30 g de mussarela ralada"),
       ("frango_cozido", 30, "30 g de frango cozido desfiado"),
       ("tomate", 30, "algumas rodelas de tomate")],
      "Sal e orégano a gosto",
      ["Bata os ovos com a goma e uma pitada de sal.",
       "Despeje numa frigideira antiaderente untada, em fogo baixo, e tampe por 3 minutos.",
       "Vire, espalhe o molho, o frango, a mussarela e o tomate.",
       "Tampe até o queijo derreter e finalize com orégano."]),

    # ---------------------------------------------------------------- doces
    R("Mousse de cacau proteica", "doce", 3, "10 min + 2 h na geladeira",
      [("iogurte_natural", 340, "2 potes de iogurte natural (340 g)"),
       ("leite_po_desnatado", 40, "4 colheres de sopa de leite em pó desnatado (40 g)"),
       ("cacau", 12, "2 colheres de sopa de cacau em pó 100%"),
       ("gelatina_incolor", 12, "1 envelope de gelatina incolor sem sabor (12 g)")],
      "5 colheres de sopa de água; adoçante a gosto",
      ["Hidrate a gelatina na água por 5 minutos e derreta no micro-ondas por 10 a 15 segundos.",
       "Bata o iogurte, o leite em pó, o cacau e o adoçante no liquidificador.",
       "Com o liquidificador ligado, junte a gelatina.",
       "Distribua em 3 potinhos e leve à geladeira por 2 horas."]),

    R("Brigadeiro de colher proteico", "doce", 1, "3 min",
      [("leite_po_desnatado", 30, "3 colheres de sopa de leite em pó desnatado (30 g)"),
       ("cacau", 6, "1 colher de sopa de cacau em pó 100%"),
       ("leite_desnatado", 40, "3 colheres de sopa de leite desnatado")],
      "Adoçante a gosto",
      ["Misture tudo até virar um creme liso. Se ficar grosso, pingue mais leite.",
       "Coma morno (20 segundos no micro-ondas) ou deixe 15 minutos na geladeira para firmar."]),

    R("Bolo de caneca de banana", "doce", 1, "4 min",
      [("ovo", 50, "1 ovo"),
       ("banana", 70, "1 banana pequena bem madura"),
       ("aveia", 20, "2 colheres de sopa de aveia em flocos"),
       ("leite_po_desnatado", 10, "1 colher de sopa de leite em pó desnatado")],
      "Canela a gosto; 1/2 colher de chá de fermento em pó",
      ["Amasse a banana dentro de uma caneca grande.",
       "Junte o ovo, a aveia, o leite em pó e a canela e misture bem. Por último, o fermento.",
       "Micro-ondas por 1min30 a 2 minutos."],
      dica="Quanto mais madura a banana, menos adoçante você precisa (às vezes nenhum)."),

    R("Panqueca de ricota com frutas vermelhas", "doce", 1, "10 min",
      [("ovo", 50, "1 ovo"),
       ("ricota", 50, "3 colheres de sopa de ricota"),
       ("aveia", 20, "2 colheres de sopa de aveia em flocos finos"),
       ("frutas_vermelhas", 50, "1/2 xícara de frutas vermelhas")],
      "1/2 colher de chá de fermento em pó, canela e adoçante a gosto",
      ["Bata o ovo, a ricota, a aveia, a canela e o adoçante com um garfo. Junte o fermento.",
       "Faça 3 panquecas pequenas numa frigideira antiaderente untada, em fogo baixo, 2 minutos de cada lado.",
       "Aqueça as frutas vermelhas no micro-ondas por 1 minuto e sirva por cima."]),

    R("Cheesecake de pote", "doce", 2, "10 min + 30 min na geladeira",
      [("aveia", 20, "2 colheres de sopa de aveia em flocos"),
       ("ricota", 150, "150 g de ricota"),
       ("iogurte_natural", 170, "1 pote de iogurte natural (170 g)"),
       ("frutas_vermelhas", 100, "1 xícara de frutas vermelhas")],
      "Raspas e suco de 1/2 limão; adoçante a gosto",
      ["Toste a aveia numa frigideira seca por 2 minutos.",
       "Bata a ricota, o iogurte, o limão e o adoçante até ficar liso.",
       "Em 2 potes, monte: aveia, creme e frutas vermelhas amassadas com um garfo.",
       "Geladeira por 30 minutos."]),

    R("Picolé de iogurte com morango", "doce", 5, "10 min + 6 h no congelador",
      [("iogurte_natural", 510, "3 potes de iogurte natural (510 g)"),
       ("leite_po_desnatado", 60, "6 colheres de sopa de leite em pó desnatado (60 g)"),
       ("morango", 150, "1 xícara de morango picado")],
      "Adoçante a gosto",
      ["Bata o iogurte, o leite em pó e o adoçante.",
       "Misture o morango picado com uma colher.",
       "Distribua em 5 forminhas de picolé e congele por 6 horas."],
      dica="Rende 5 picolés; a porção é 1."),

    R("Maçã assada com ricota e canela", "doce", 1, "10 min",
      [("maca", 130, "1 maçã em cubos"),
       ("ricota", 50, "3 colheres de sopa de ricota"),
       ("leite_po_desnatado", 10, "1 colher de sopa de leite em pó desnatado"),
       ("aveia", 10, "1 colher de sopa de aveia em flocos")],
      "Canela e adoçante a gosto",
      ["Coloque a maçã num pote com canela, cubra e leve ao micro-ondas por 3 minutos.",
       "Amasse a ricota com o leite em pó e o adoçante até virar creme.",
       "Toste a aveia numa frigideira seca por 1 minuto.",
       "Sirva a maçã quente com o creme e a aveia por cima."]),

    R("Sorvete de banana com pasta de amendoim", "doce", 1, "5 min",
      [("banana", 100, "1 banana congelada em rodelas"),
       ("leite_po_desnatado", 20, "2 colheres de sopa de leite em pó desnatado (20 g)"),
       ("pasta_amendoim", 15, "1 colher de sopa de pasta de amendoim"),
       ("leite_desnatado", 45, "3 colheres de sopa de leite desnatado")],
      "",
      ["Bata tudo no processador, parando para raspar as laterais, até virar um creme.",
       "Coma na hora ou congele por 30 minutos para ficar mais firme."],
      dica="Congele bananas maduras em rodelas sempre que sobrarem: é a base do sorvete e da vitamina."),
]


def nutricao(receita):
    kcal = sum(ALIMENTOS[a][0] * g / 100 for a, g, _ in receita["ingredientes"])
    prot = sum(ALIMENTOS[a][1] * g / 100 for a, g, _ in receita["ingredientes"])
    n = receita["porcoes"]
    return round(prot / n), int(round(kcal / n / 10.0) * 10)


def porcoes_txt(n):
    return "1 porção" if n == 1 else f"{n} porções"


def gerar():
    assert len(RECEITAS) == 40, len(RECEITAS)
    for r in RECEITAS:
        for a, _, _ in r["ingredientes"]:
            assert a in ALIMENTOS, a

    linhas = []
    add = linhas.append

    add("# Prato Pequeno, Proteína Grande")
    add("")
    add("**40 receitas proteicas em porção pequena, sem complicação**")
    add("")
    add("por Bia")
    add("")
    add("---")
    add("")

    add("## Antes de começar")
    add("")
    add("Este ebook traz receitas, não um plano alimentar. Ele não substitui consulta com nutricionista ou "
        "médico.")
    add("")
    add("Se você usa medicação para emagrecer, tem diabetes, doença renal ou outra condição de saúde, está "
        "grávida ou amamentando, siga a orientação do seu profissional de saúde sobre quanto e o que comer.")
    add("")
    add("Confira alergias e intolerâncias: as receitas usam ovo, leite e derivados, amendoim, peixe, "
        "frutos do mar e aveia (que pode conter glúten).")
    add("")

    add("## Quem é a Bia")
    add("")
    add("A Bia é uma personagem criada com inteligência artificial para o perfil [@perfil]. Ela cozinha "
        "prático, com ingrediente de mercado comum, e acredita que comida boa não precisa de frescura.")
    add("")
    add("As receitas foram desenvolvidas por [autor] e revisadas por [nome da nutricionista], "
        "CRN [número].")
    add("")

    add("## Como usar este ebook")
    add("")
    add("Quando a gente come menos, cada garfada precisa valer mais. Por isso todas as receitas daqui são "
        "**porções pequenas com bastante proteína**, feitas com coisas que você acha em qualquer mercado.")
    add("")
    add("- **Tempo:** do primeiro passo até o prato pronto.")
    add("- **Proteína e calorias:** por porção, aproximadas. Mudam com a marca e o tamanho dos ingredientes.")
    add("- **Congela:** receitas que você pode fazer em quantidade e guardar.")
    add("- **Temperos:** sal, alho, ervas, limão e especiarias não entram na conta e vão a gosto.")
    add("- **Medidas:** colher de sopa de aveia ou de leite em pó ≈ 10 g; xícara = 240 ml.")
    add("")
    add("Três coisas deixam a semana mais fácil:")
    add("")
    com_frango = sum(any(a == "frango_cozido" for a, _, _ in r["ingredientes"]) for r in RECEITAS)
    add("1. **Frango desfiado pronto na geladeira.** Cozinhe 1 kg de peito no domingo, desfie e guarde em "
        f"potes. Ele aparece em {com_frango} receitas deste ebook.")
    add("2. **Ovos cozidos.** Cozidos e com casca, duram até 1 semana na geladeira.")
    add("3. **Leite em pó desnatado.** O truque mais barato para pôr proteína em doce, mingau e vitamina.")
    add("")

    usados = {a for r in RECEITAS for a, _, _ in r["ingredientes"]}
    add("## Despensa básica")
    add("")
    add("Tudo o que aparece nas 40 receitas, fora os temperos.")
    add("")
    for grupo, chaves in GRUPOS_DESPENSA.items():
        nomes = []
        for c in chaves:
            if c in usados and NOME_DESPENSA[c] not in nomes:
                nomes.append(NOME_DESPENSA[c])
        add(f"**{grupo}:** " + ", ".join(nomes) + ".")
        add("")
    faltando = usados - {c for cs in GRUPOS_DESPENSA.values() for c in cs} - {"clara", "frango_cozido"}
    assert not faltando, faltando

    numero = 0
    for cap, titulo in CAPITULOS.items():
        add("---")
        add("")
        add(f"## {titulo}")
        add("")
        for r in [r for r in RECEITAS if r["cap"] == cap]:
            numero += 1
            r["numero"] = numero
            prot, kcal = nutricao(r)
            r["prot"], r["kcal"] = prot, kcal
            add(f"### {numero}. {r['nome']}")
            add("")
            add(f"Tempo: {r['tempo']} · Rende: {porcoes_txt(r['porcoes'])} · "
                f"Proteína: ≈ {prot} g · Energia: ≈ {kcal} kcal (por porção)")
            add("")
            add("**Ingredientes**")
            add("")
            for _, _, txt in r["ingredientes"]:
                add(f"- {txt}")
            if r["temperos"]:
                add(f"- {r['temperos']}")
            add("")
            add("**Modo de preparo**")
            add("")
            for i, p in enumerate(r["passos"], 1):
                add(f"{i}. {p}")
            add("")
            if r["dica"]:
                add(f"**Dica da Bia:** {r['dica']}")
                add("")
            if r["congela"]:
                add(f"**Congela:** {r['congela']}")
                add("")

    add("---")
    add("")
    add("## As 10 com mais proteína")
    add("")
    add("| Receita | Proteína | Energia |")
    add("|---|---|---|")
    for r in sorted(RECEITAS, key=lambda r: -r["prot"])[:10]:
        add(f"| {r['numero']}. {r['nome']} | ≈ {r['prot']} g | ≈ {r['kcal']} kcal |")
    add("")
    add("## Até 15 minutos")
    add("")
    rapidas = [r for r in RECEITAS if r["tempo"].split()[0].isdigit() and int(r["tempo"].split()[0]) <= 15
               and "+" not in r["tempo"]]
    add(", ".join(f"{r['numero']}. {r['nome']}" for r in rapidas) + ".")
    add("")
    add("---")
    add("")
    add("## Fez? Me mostra!")
    add("")
    add("Tira uma foto do seu prato e marca [@perfil] nos stories. Eu reposto as minhas favoritas.")
    add("")
    add("Com carinho,  ")
    add("Bia")
    add("")

    destino = Path(__file__).with_name("ebook.md")
    destino.write_text("\n".join(linhas), encoding="utf-8")

    print(f"{'#':>2}  {'receita':<44}{'porç':>5}{'prot':>6}{'kcal':>6}")
    for r in RECEITAS:
        print(f"{r['numero']:>2}  {r['nome']:<44}{r['porcoes']:>5}{r['prot']:>6}{r['kcal']:>6}")
    print(f"\n{destino.name}: {len(linhas)} linhas, {sum(len(l.split()) for l in linhas)} palavras")


if __name__ == "__main__":
    gerar()
