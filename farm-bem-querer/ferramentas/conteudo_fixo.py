"""Partes fixas da tese (direcao de arte, coracao, anti-IA, marca, produto, etica, processo)."""

SUMARIO = [
    ('A tese em uma página', 'proposta, oportunidade e entregas'),
    ('FARM Rio', 'quem é a marca e como ela trabalha estampa'),
    ('Havaianas', 'quem é a marca e o que ela já fez com o Brasil'),
    ('A collab que já existe (V1)', 'o que foi lançado e como foi assinado'),
    ('Como a FARM assina suas collabs', 'pesquisa dos logos: padrão ou logo novo?'),
    ('Por que uma V2', 'o argumento'),
    ('O conceito Bem-Querer', 'nome, frase e narrativa do coração'),
    ('Como escolhemos os 14 estados', 'critério do bater o olho'),
    ('Direção de arte', 'o DNA das 10 referências'),
    ('O coração como assinatura', 'sistema de 3 níveis'),
    ('O que evitar', 'por que imagem com cara de IA não entra'),
    ('Os 14 estados do Drop 1', 'uma página por estado, pronta para produzir'),
    ('Drop 2', 'os 13 estados restantes'),
    ('Sistema de marca', 'assinatura V2, selos e arte com/sem logo'),
    ('Produto, embalagem e lançamento', 'chinelo, cápsula FARM, passaporte'),
    ('Ética e crédito cultural', 'quem precisa ser citado e remunerado'),
    ('Processo de produção', 'do briefing à arte final, sem desperdício'),
    ('Fontes', 'todas as referências consultadas'),
]

TESE = {
    'titulo': 'Um coração em cada canto do Brasil',
    'frase': 'Na collab que já existe, o coração é o sinal que une **havaianas** e **FARM RIO** na sola do chinelo. '
             'Na V2, ele sai do logo e entra no desenho: cada estado ganha a sua estampa, e o coração se esconde dentro dela '
             '(nas pintas, nos frutos, no bordado, no casario).',
    'blocos': [
        ('A oportunidade', 'A parceria havaianas ♥ FARM Rio é longa e bem-sucedida, mas suas estampas falam de um Brasil tropical '
                           'de assinatura FARM (tucano, coco, flores). O país tem 27 identidades regionais que ainda não viraram estampa nessa collab.'),
        ('A proposta', 'Uma cápsula em drops: **um chinelo + uma peça FARM por estado**. O Drop 1 traz 14 estados das cinco regiões; '
                       'o Drop 2 completa os 27.'),
        ('O diferencial autoral', 'Corações escondidos na forma real de cada ícone, num sistema de 3 níveis (composição, padrão e detalhe). '
                                  'A estampa vira jogo de descoberta, e a assinatura é a mesma do logo da collab.'),
        ('O critério', '**Teste do bater o olho:** quem é do estado reconhece na hora. Entram ícones que o próprio povo reivindica; '
                       'saem os clichês que servem para qualquer lugar.'),
    ],
    'numeros': [('27', 'estados no total, em dois drops'), ('14', 'estados no Drop 1, com as 5 regiões'),
                ('3', 'níveis de coração em cada estampa')],
}

REFS = [
    ('Caju', 'guache digital solto, sombra em 2 tons, fruta vazando a borda'),
    ('Castanha-do-pará', 'pincel seco, sol em círculo chapado, formas simplificadas'),
    ('Mico-leão-dourado', 'moldura de carta, pelo em pinceladas direcionais, fundo único'),
    ('Açaí', 'fundo terracota, folhas em faixas de 3 tons, frutos com variação'),
    ('Arara', 'formas facetadas, contorno branco recortado, assinatura do autor'),
    ('Jacaré', 'arte folk chapada, moldura ondulada listrada, 4 cores'),
    ('Pavão', 'padrão do leque simplificado e repetido, fundo liso'),
    ('Bananeira', 'colagem de planos, respingos e linhas finas, contraste alto'),
    ('Cacau', 'fundo escuro, composição de papel de parede'),
    ('Onça rosa', 'hachura fina, animal monocromático, fundo amarelo liso'),
]

REGRAS_DNA = [
    '**Um protagonista**, no máximo dois coadjuvantes. A arte tem um assunto.',
    '**Fundo de cor única e forte.** Sem céu degradê, sem paisagem realista dentro da ilustração.',
    '**Paleta curta:** 4 a 6 cores, travadas em hex no briefing.',
    '**Uma textura por arte** (guache seco, granulado ou hachura), aplicada com coerência.',
    '**Volume em 2 a 3 tons chapados.** Nada de degradê suave nem brilho plástico.',
    '**Recorte ousado:** o protagonista vaza a borda; a composição é assimétrica.',
    '**Um recurso gráfico de assinatura** (sol em círculo, moldura, borda listrada, contorno recortado) e **respiro na base** para a assinatura da collab.',
]

CORACAO_REGRAS = [
    'O coração **herda a cor do elemento** que ele substitui: a pinta da onça continua preta, a lantejoula continua dourada.',
    'Ele **se deforma com a anatomia**: acompanha a curva do corpo, muda de tamanho e nunca é perfeitamente simétrico.',
    '**No máximo um coração óbvio por arte**; o resto é descoberta.',
    'Proibido: coração de emoji, contorno de adesivo, coração carimbado ou entalhado.',
    'O coração do conector **havaianas ♥ FARM RIO** e o das estampas são **o mesmo desenho**, feito à mão. É isso que amarra marca e ilustração.',
]

SINAIS_IA = [
    '**Detalhe demais por toda parte**, na mesma intensidade; ilustração humana escolhe onde detalhar.',
    '**Brilho especular e degradê suave** (cara de 3D ou airbrush).',
    '**Paisagem realista** encaixada dentro de uma ilustração chapada.',
    '**Anatomia errada**: no teste, o lobo-guará virou raposa (focinho laranja, cauda cheia).',
    '**Coração carimbado**: no teste, corações "entalhados" no tronco da jabuticabeira; parece adesivo, não descoberta.',
    '**Simetria perfeita e elementos demais** competindo pela atenção.',
    '**Texto gerado por IA** sai deformado; por isso **o logo nunca é gerado**, é aplicado depois em vetor.',
]


def secoes_finais(drop2_linhas, collabs_linhas):
    return [
        {
            'kicker': '09 · Direção de arte', 'titulo': 'O DNA das 10 referências', 'rodape': 'direção de arte',
            'lead': 'As referências escolhidas parecem feitas por gente porque tomam decisões: poucas cores, um assunto, textura assumida e recorte ousado. Essas decisões viram regra.',
            'blocos': [
                {'tipo': 'html', 'html': '<div class="refs">' + ''.join(
                    f'<figure><img src="referencias/ref-{i + 1:02d}.jpg"><figcaption><strong>{i + 1:02d} · {n}</strong><br>{d}</figcaption></figure>'
                    for i, (n, d) in enumerate(REFS)) + '</div>'},
                {'tipo': 'lista', 'titulo': 'As 7 regras do traço', 'itens': REGRAS_DNA},
                {'tipo': 'texto', 'ps': ['<span class="fonte">As referências são estudo de linguagem. A autoria de cada uma deve ser identificada e creditada antes de qualquer publicação; elas não são usadas como imagem de entrada em ferramentas de IA.</span>']},
            ],
        },
        {
            'kicker': '10 · Assinatura autoral', 'titulo': 'O coração como assinatura', 'rodape': 'o coração',
            'lead': 'O coração não é enfeite colado em cima: ele aparece onde a natureza ou o artesanato já repetem uma forma. Cada estampa tem corações em três níveis de leitura.',
            'blocos': [
                {'tipo': 'html', 'html': '<div class="coracao3">'
                    '<div><strong>1 · Macro (composição)</strong>A forma geral ou o espaço negativo desenha um coração: duas folhas que se encontram, o contorno de um cacho, a curva de um rio. Quase ninguém percebe de primeira.</div>'
                    '<div><strong>2 · Médio (padrão)</strong>O que já se repete vira coração: pintas da onça, escamas, sementes, olhos da pena do pavão, lantejoulas do bordado, gomos da sombrinha.</div>'
                    '<div><strong>3 · Micro (detalhe)</strong>O brilho do olho, o reflexo da fruta, uma mancha no pescoço. É o prêmio de quem olha de perto e o que gera conversa nas redes.</div></div>'},
                {'tipo': 'lista', 'titulo': 'Regras', 'itens': CORACAO_REGRAS},
                {'tipo': 'caixa', 'titulo': 'Exemplo — a onça do Pantanal (MS)', 'ps': [
                    'Macro: o corpo deitado no galho fecha uma curva de coração com a cauda. Médio: cada roseta é um coração aberto, pequeno no rosto e grande no flanco, sempre preto sobre o ocre. Micro: o brilho do olho é um coraçãozinho.']},
            ],
        },
        {
            'kicker': '11 · O que evitar', 'titulo': 'Por que imagem com cara de IA não entra', 'rodape': 'o que evitar',
            'lead': 'Os primeiros testes foram descartados. Eles ensinaram o que denuncia uma imagem gerada e viraram regras do prompt e da revisão.',
            'blocos': [
                {'tipo': 'html', 'html': '<div class="grid3" style="margin-bottom:4mm">'
                    '<figure style="margin:0"><img src="artes/testes-descartados/mg-01-lobo-guara.png" style="border-radius:2mm;height:62mm;width:100%;object-fit:cover"><figcaption class="fonte">Lobo-guará: anatomia de raposa e ícone genérico do Cerrado (não grita Minas).</figcaption></figure>'
                    '<figure style="margin:0"><img src="artes/testes-descartados/mg-02-jabuticabeira.png" style="border-radius:2mm;height:62mm;width:100%;object-fit:cover"><figcaption class="fonte">Jabuticabeira: corações entalhados no tronco parecem carimbo.</figcaption></figure>'
                    '<figure style="margin:0"><img src="artes/testes-descartados/mg-03-barroco-lenco.png" style="border-radius:2mm;height:62mm;width:100%;object-fit:cover"><figcaption class="fonte">Lenço barroco: paisagem realista dentro do ornamento e detalhe homogêneo.</figcaption></figure></div>'},
                {'tipo': 'lista', 'titulo': 'Sinais de IA que a revisão barra', 'itens': SINAIS_IA},
                {'tipo': 'caixa', 'titulo': 'Como o processo evita isso', 'ps': [
                    'O prompt-base descreve **técnica humana** (guache digital no Procreate, 2 a 3 tons chapados, borda imperfeita), trava a **paleta em hex**, pede **um protagonista** e proíbe brilho, degradê e realismo. Cada arte passa por **checklist humano** antes de seguir e, se precisar, é finalizada à mão (anatomia, corações, cor).']},
            ],
        },
        {
            'kicker': '13 · Drop 2', 'titulo': 'Os 13 estados restantes', 'rodape': 'drop 2',
            'lead': 'O Drop 2 completa o mapa com o mesmo critério. Abaixo, os ícones mais fortes de cada estado para o próximo briefing.',
            'blocos': [{'tipo': 'tabela', 'cab': ['UF', 'Estado', 'Ícones mais fortes (bater o olho)'], 'linhas': drop2_linhas}],
        },
        {
            'kicker': '14 · Sistema de marca', 'titulo': 'A assinatura segue a casa; a cápsula ganha nome', 'rodape': 'sistema de marca',
            'lead': 'A pesquisa (seção 5) mostrou que a FARM não cria um logo novo a cada collab: ela usa um sistema fixo (logo do parceiro + conector + FARM RIO), e o ♥ marca as parcerias de afeto. A V2 respeita esse sistema e soma o nome da cápsula.',
            'blocos': [
                {'tipo': 'html', 'html': '<div class="grid2" style="align-items:center">'
                    '<div class="caixa" style="background:#F1E3C2">{SVG:{L}/assinatura-v2/assinatura-mg-empilhado-escuro.svg}</div>'
                    '<div><div class="caixa" style="background:#1F4D47">{SVG:{L}/assinatura-v2/assinatura-ms-horizontal-claro.svg}</div>'
                    '<div class="caixa">{SVG:{L}/assinatura-v2/assinatura-pe-horizontal-escuro.svg}</div>'
                    '<p style="font-size:9pt"><strong>Empilhada</strong> para a arte, a sola e a etiqueta (como no calcanhar da V1). <strong>Horizontal</strong> para banner e site. Versão <strong>clara</strong> sobre fundo escuro e <strong>escura</strong> sobre fundo claro, escolhida automaticamente pela luminância da área.</p></div></div>'},
                {'tipo': 'lista', 'titulo': 'Regras de uso', 'itens': [
                    'Logos oficiais **sem textura, sem distorção e sem troca de cor fora do monocromático**, como pedem os manuais de marca.',
                    'O **coração do conector** é o coração desenhado à mão da coleção, na cor de destaque do estado (na versão clara, monocromático).',
                    'Linha da cápsula: **bem-querer + nome do estado**, em Fraunces Soft (fonte livre, Google Fonts).',
                    'Toda arte tem **duas versões**: sem logo (estampa, rapport, cartão-postal) e com logo (campanha, redes, banner). A assinatura é aplicada em vetor depois da arte pronta, nunca gerada por IA.',
                ]},
            ],
        },
        {
            'kicker': '14 · Sistema de marca', 'titulo': 'Wordmark e selos dos estados', 'rodape': 'sistema de marca',
            'lead': 'O wordmark bem-querer assina a campanha. Os selos funcionam como carimbo de passaporte: um por estado, na embalagem, na tag e no passaporte da coleção.',
            'blocos': [
                {'tipo': 'html', 'html': '<div style="width:120mm;margin:0 auto 6mm">{SVG:{L}/bem-querer-wordmark-tinta.svg}</div>'},
                {'tipo': 'selos', 'ufs': ['MG', 'RJ', 'BA', 'PE', 'CE', 'MA', 'AM', 'PA', 'TO', 'MS', 'GO', 'PR', 'SC', 'RS']},
                {'tipo': 'texto', 'ps': ['<span class="fonte">Tipografia: Fraunces (SIL Open Font License), convertida em contorno nos arquivos SVG. Coração desenhado à mão, levemente assimétrico.</span>']},
            ],
        },
        {
            'kicker': '15 · Produto', 'titulo': 'Produto, embalagem e lançamento', 'rodape': 'produto',
            'blocos': [
                {'tipo': 'lista', 'titulo': 'Havaianas', 'itens': [
                    'Modelos **Top** (unissex) e **Slim** (feminino), seguindo os modelos já usados na collab.',
                    '**Palmilha** com recorte da estampa do estado; **tira** na cor de destaque da paleta.',
                    '**Calcanhar** com a assinatura empilhada, como na V1, mais o nome do estado.',
                    'Um **coração escondido** na palmilha também: quem acha, posta.',
                ]},
                {'tipo': 'lista', 'titulo': 'Cápsula FARM', 'itens': [
                    'Uma **peça-herói por estado** com a estampa em rapport (vestido, kimono, lenço, camisa, biquíni), indicada na página de cada estado.',
                    'Estampa com **duas escalas**: grande (posicionada) e pequena (corrida).',
                ]},
                {'tipo': 'lista', 'titulo': 'Embalagem e colecionabilidade', 'itens': [
                    '**Cartão-postal** com a arte sem logo e o selo do estado no verso.',
                    '**Passaporte Bem-Querer**: um livreto para carimbar os 27 selos; quem completa um drop ganha conteúdo exclusivo.',
                ]},
                {'tipo': 'lista', 'titulo': 'Lançamento', 'itens': [
                    '**Drop 1** (14 estados) no Alto Verão; **Drop 2** (13 estados) na estação seguinte.',
                    'Lançamentos regionais nas capitais, com **artistas e artesãos locais** como parceiros (ver seção 16).',
                    'Campanha em redes: "ache o coração" em cada estampa.',
                ]},
            ],
        },
        {
            'kicker': '16 · Ética', 'titulo': 'Ética e crédito cultural', 'rodape': 'ética',
            'lead': 'Uma coleção sobre o Brasil precisa devolver algo para quem faz o Brasil. Isso também fortalece a defesa.',
            'blocos': [
                {'tipo': 'lista', 'itens': [
                    '**Saberes registrados** (renda de bilro, capim dourado, cerâmica, bordado do boi): crédito nominal às comunidades e artesãs, remuneração ou royalties, e selo de origem no produto.',
                    '**Manifestações de matriz africana e indígena**: nada de símbolo sagrado como enfeite. Inspiração em formas e cores, com consulta e parceria.',
                    '**Grafismos indígenas** (ex.: marajoara): estudar princípios (faixas, simetria) sem copiar peças; o ideal é parceria com ceramistas da região.',
                    '**Referências de estilo**: as obras de outros artistas não são usadas como entrada em IA; a técnica é descrita em palavras.',
                    '**Transparência no portfólio**: declarar que a base das imagens usa IA e que pesquisa, direção de arte, curadoria, sistema de corações, marca e finalização são autorais.',
                ]},
            ],
        },
        {
            'kicker': '17 · Processo', 'titulo': 'Do briefing à arte final, sem desperdício', 'rodape': 'processo',
            'lead': 'A regra é acertar de primeira: o briefing chega travado e cada estado tem uma geração só.',
            'blocos': [
                {'tipo': 'tabela', 'cab': ['Etapa', 'O que acontece', 'Custo'], 'linhas': [
                    ['1 · Briefing', 'Página do estado aprovada: ícones, paleta, composição, corações.', 'zero'],
                    ['2 · Geração', '**Uma** imagem por estado com o prompt-base preenchido.', '0,25 crédito por imagem (14 estados ≈ 3,5 créditos)'],
                    ['3 · Revisão', 'Checklist: ícones legíveis, anatomia, paleta, corações nos 3 níveis, respiro na base.', 'zero'],
                    ['4 · Finalização', 'Ajuste à mão (Procreate/Photoshop) quando o checklist pedir.', 'tempo'],
                    ['5 · Duas versões', 'Script gera a **arte sem logo** e a **arte com logo** (tom claro/escuro automático).', 'zero'],
                    ['6 · Mockups', 'Chinelo, peça FARM, embalagem e passaporte.', 'zero'],
                ]},
                {'tipo': 'lista', 'titulo': 'Prompt-base (preenchido por estado)', 'itens': [
                    'Técnica: ilustração digital à mão, guache texturizado, 2 a 3 tons chapados, borda imperfeita, grão de papel.',
                    'Proibições: degradê, brilho, 3D, realismo, excesso de detalhe, texto.',
                    'Paleta travada em hex, fundo liso, um protagonista, respiro na base, recurso gráfico e os três corações descritos.',
                ]},
            ],
        },
        {
            'kicker': '05 · Pesquisa de marca', 'titulo': 'Como a FARM assina suas collabs', 'rodape': 'assinaturas',
            'lead': 'Pergunta da pesquisa: cada collab ganha um logo novo, ou todas seguem o mesmo padrão? Resposta: **seguem um sistema**. Logo oficial do parceiro + conector + FARM RIO. O conector varia, e o ♥ aparece nas parcerias de afeto e longa duração.',
            'blocos': [
                {'tipo': 'tabela', 'cab': ['Collab', 'Como aparece', 'Conector'], 'linhas': collabs_linhas},
                {'tipo': 'imagem', 'src': 'pesquisa/banners-collabs.jpg', 'legenda': 'Banners oficiais no site da FARM Rio (EUA): Barbour ♥ FARM RIO (empilhado), RIP CURL ♥ FARM RIO, STANLEY | FARM RIO, FARM RIO | WHITESPACE.'},
                {'tipo': 'caixa', 'escura': True, 'titulo': 'O que isso decide para a V2', 'ps': [
                    'Não inventar um logo que concorra com as marcas. A V2 usa a assinatura da casa, **havaianas ♥ FARM RIO**, e cria só o que é dela: o **nome da cápsula (bem-querer)**, o **coração desenhado à mão** e os **selos dos estados**. Assim como a adidas FW23 ganhou uma flor exclusiva, a V2 ganha um coração exclusivo.']},
            ],
            'fontes': [('FARM Rio — coleções (farmrio.com)', 'https://farmrio.com/collections/havaianas'),
                       ('V Magazine — adidas FW23', 'https://vmagazine.com/article/farm-rio-adidas-release-fw23-collaboration'),
                       ('Essence — adidas FW23', 'https://essence.com/fashion/farm-rio-adidas-fall-winter-2023-collection-launch'),
                       ('Mundo do Marketing — Matte Leão', 'https://mundodomarketing.com.br/farm-rio-e-matte-leao-se-reencontram-em-collab-que-celebra-dois-classicos-do-verao-carioca')],
        },
    ]
