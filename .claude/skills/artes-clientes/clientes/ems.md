# EMS (@itsemsdesign · Emilly Silva)

- **Motor (Design System no Claude):** https://claude.ai/artifact/DNhPwJnJSH9f4gih32oQGa (versão 17 em 12/11/2026)
  - Ler sempre: `project/README.md` (voz, cor, tipografia, grafismos, selo), `project/conteudo.md` (pilares, estruturas de carrossel, banco de ideias, legenda), `project/geracao-de-imagem.md` (prompts) e o componente do formato pedido em `project/components/<Nome>/README.md`.
  - Artes finais mais novas: grupo de assets **Posts** do DS (subir lá toda arte nova, com registro no índice `assetGroups.Posts`).
- **Skill própria:** `marca-ems` (abre o DS). Este arquivo guarda o que foi aprendido fazendo as peças.
- **Projetos no repositório:** `reel-ems/` (reel "provas"), `capas/` (capa de reel), `Emi/ems-5-direcoes-pet/` (carrossel de curadoria).

## Processo para errar menos (pedido da Emi, 12/11/2026)

O carrossel pet levou 6 rodadas até ser aprovado. A Emi pediu para salvar tudo e seguir este processo em todo post:

1. **Pesquisar referência antes de desenhar, sempre.** Nunca diagramar de cabeça.
   - **Pinterest:** `node .claude/skills/artes-clientes/referencias/pinterest.mjs "<busca>" <pasta> [qtd]` baixa os pins e monta `folha.jpg`. Funciona sem login. Fazer 2 ou 3 buscas por peça, por exemplo "capa revista <tema> tipografia", "instagram carousel cover editorial", "instagram carousel last slide poll design".
   - **Instagram:** ver o que os designers andam postando. `node .claude/skills/artes-clientes/referencias/instagram.mjs <link-do-post> <pasta>` baixa as lâminas de um carrossel público. Perfis de referência: @pivocriativo (quando a Emi mandar outros, anotar aqui).
   - **Web:** busca de "como diagramar X", capas de revista, adesivos de story. O Freepik (`stock_search`, `content_type: psd,design`) também mostra diagramação.
   - Olhar a folha, escolher **um conceito de diagramação que caiba no tema** (capa de revista, enquete, ficha...) e guardar a folha em `<projeto>/referencias/` com o que se pega e o que não se pega.
2. **Da referência que a Emi manda, pegar a ideia, nunca a estrutura**: grade, posição dos elementos, frases-chave.
3. **Cada post do Instagram é diferente dos outros**: "senão eu postava a mesma coisa todo dia". Não reaproveitar recursos de outro post da EMS:
   - anotação à mão com linha curva;
   - seleção do Figma decorativa;
   - marca d'água em fila;
   - colagem em selo do "cpf x cnpj".

   A identidade (cor, fonte, selo, voz) fica; a diagramação muda.
4. **Dentro de um carrossel**: as lâminas de conteúdo seguem uma estrutura só, e capa e chamada têm diagramação especial. Um layout diferente por lâmina foi reprovado.
5. **Fotos**:
   - cena inteira, nada de recorte colado em cor chapada;
   - nenhuma foto repetida no carrossel, e variações da mesma cena contam como repetição;
   - por tema, cenas realmente diferentes.

   O recorte só entra para pôr o bicho **na frente** de um texto ou de um cartão, com a mesma foto por baixo.
6. **Mandar prévia cedo** pelo celular (SendUserFile) e iterar por lâmina; não propagar para Figma, Drive e DS antes da aprovação.

**Margem: capa e chamada com 90px livres nos quatro lados** (pedido da Emi, 12/11). Todo texto e elemento fica dentro de [90, 990] × [90, 1260]; só a foto e as texturas sangram. Conferir com a guia (`carrossel.html?guia` desenha a margem tracejada).

**Checklist antes de mandar:**
- A capa não dá spoiler do conteúdo.
- O título é um bloco só, sem espaço grande entre as partes.
- Nenhuma seleção, cursor ou selo está fora do lugar (seleção em volta do que importa, nunca no vazio).
- A composição está equilibrada, sem todo o texto empilhado num lado só.
- Fundo liso ganhou textura (retícula, grão).
- Os elementos se encostam e se invadem um pouco, sem cobrir rosto nem texto.
- Nada foi copiado da referência nem de outro post.
- Capa e chamada respeitam a margem de 90px.
- Letra que cai atrás do bicho continua legível. O "ç" de "direções" sumia atrás da cabeça do gato e virava "direcões"; a solução foi repetir só o cedilha por cima do recorte.
- Nenhuma foto se repete.

## Marca fictícia (logo dentro de post) sem cara de IA

A Emi reprovou, por "cara de IA", estas marcas da primeira versão:
- o balão "AU!";
- o monograma no círculo;
- o sol listrado;
- o brasão universitário.

Só passou a MIAU.LAB, que é um rótulo aplicado. A regra:
1. Pesquisar no Pinterest marcas **reais** do universo (embalagem de snack pop, marca pet de luxo, logo anos 70, run club) antes de desenhar.
2. **Desenhar a letra**, sem só digitar uma fonte. Exemplos: letras que pulam (cada uma girada e numa altura), contorno e volume, sombras empilhadas em cores, caixa-alta bem espaçada com um detalhe.
3. **Aplicar num objeto**: adesivo recortado, etiqueta de couro, número de peito, rótulo, embalagem. Nunca logo boiando no meio do quadro.
4. Detalhe que só marca de verdade tem: ™, "desde 1974", "nº 001", código de barras, costura, alfinete.
5. Texto centralizado na forma (não na caixa); espaçamento entre letras compensado com recuo igual à esquerda.

6. A primeira versão do AU! (adesivo de explosão com letra bojuda 3D e faixa) ainda tinha "cara de IA": é o "logo de gibi" padrão de gerador. A versão aprovada é um **pacote de petisco** chapado, com quadrinho impresso, "AU!" fora de registro (azul deslocado atrás do preto, como impressão), selo "nº1 do bairro" e textos de embalagem (sabor, peso).

Referências e o que saiu de cada uma: `Emi/ems-5-direcoes-pet/referencias/marcas/`.

**Logo e aplicação gerados com IA, não desenhados em código** (Emi, 12/11: "não quero vetorizado assim, pode gerar em algum lugar, se vira").
- Logo de marca fictícia: gerar com modelo de imagem que escreve bem (pelo Figma, `gpt-image-2.5-flare` ou `-sunburst`; o Gemini também acerta) e mostrar 3 ou 4 caminhos diferentes para ela escolher. Conferir a grafia.
- Aplicação (mockup): seguir as referências dela em `Emi/ems-5-direcoes-pet/referencias/mockups-da-emi/`. A marca fica numa cena real, o bicho é o protagonista, o rosto da pessoa é cortado e o material aparece (bordado, outdoor, jaleco, embalagem em set).
- **Mandar para aprovação antes de colocar no post.**
- **Mockup segue a referência ao pé da letra** (a Emi, irritada: "te mandei exatamente exemplos de mockups"). Caixa ou pacote no esquema do PAWLY:
  - cor chapada da marca;
  - grafismos grandes da marca (formas da pata) cortados pela borda;
  - o nome enorme no topo, quase da largura toda;
  - linhas finas com texto curto;
  - janela em arco com o cachorro;
  - dois selos (ícone e texto em círculo);
  - etiqueta de sabor serrilhada;
  - peso no rodapé.

  Reprovado: textura de foto como fundo da embalagem com logo pequeno (parece amador). Depois ela mandou o Pikku (`referencias/mockups-da-emi/pikku-pacote-ilustrado.jpg`): pacote em duas cores, nome enorme, ilustração chapada de bicho numa cor só e etiqueta embaixo. No TOTÓ ficou:
  - vermelho e creme;
  - "PETISCO DE FORNO" em Bungee;
  - o cachorro pulando para pegar o biscoito, ilustração gerada e convertida em creme chapado por limiar;
  - farelos em retícula de gibi;
  - etiqueta com borda de selo.

  "Algo assim, mas na identidade da marca e sem copiar exatamente": muda o bicho, a ação, a borda e as fontes.
  - Ajustes que ela pediu depois:
    - logo centralizado;
    - a etiqueta em grade estava "feia, estranha" e cópia do Pikku, e virou uma faixa amarela de sabor com selo de peso;
    - amarelo no nome do produto, porque usar uma cor da paleta da direção tira a cara de cópia;
    - o pé dos "T" estava cortado.
- **MIAU.LAB é marca de suplemento para gatos, não clínica.** A aplicação é o produto (potes), não o jaleco. A Emi perguntou "a MIAU.LAB é sobre o quê?" quando eu fui pelo jaleco do Vet Union. Antes de escolher a aplicação, conferir o que a marca vende.
  - Referências dela: Pawfy, com o bicho passando ao lado dos potes empilhados em fundo pastel, e DOG by Dr Lisa, com frascos e vidraria de laboratório. Ficou o Pawfy com gato tigrado cinza em fundo menta, rótulo nº07 em azul clínico e nº12 branco com faixa menta.
  - Rótulo em pote cilíndrico: `marcas/aplica_cilindro.py`, que enrola a arte (meia volta, de borda a borda) com theta = asin(x/r), herda sombra e brilho, e deixa o conteúdo no miolo.
  - **A primeira identidade (rótulo azul e branco em Space Mono) foi reprovada** ("não ficou bonito") **e o mockup saiu "torto"**: a borda do rótulo era reta e a boca do pote é curva.
    - Pesquisa: `referencias/miaulab/quadro.jpg`, 20 refs. Ela escolheu o 2 (PELZ), desistiu vendo de perto e foi para **um misto do 13 ONCE, 15 wllab e 16 CURAME**:
      - o pote inteiro numa cor;
      - uma molécula de bolhas na segunda cor;
      - etiquetas pretas;
      - o nome gigante e condensado.
    - Da molécula, ficou a primeira versão.
  - **Logo com animal** ("falta ter animal por causa do nome") e o ".lab" embaixo. Pesquisa: `referencias/miaulab/gato-espiando/`. O que ela pediu em cada rodada:
    - gato preto espiando por trás das letras: gostou da ideia, mas "não tá bem executado";
    - "muito grande, vetorizado, no negativo fica tudo preto": o gato encolheu para metade e foi para dentro do U, com uma pata em cada haste; ganhou um respiro na cor do fundo na versão preta; perdeu o branco do olho, o brilho e o nariz;
    - "não entendi os olhos": a pupila de cápsula virou olho de gato (íris rosa, pupila em fenda);
    - "patas de gato mesmo, refina": cada pata virou um traço só, com três dedos e risquinhos;
    - "as unhas e um rastrinho delicado": unhas brancas e arranhões finos recortados na letra.

    Ela aprovou ("perfeitoooo"). O código está em `marcas/miaulab/logo.js`.
  - **Pote pintado inteiro** (`marcas/miaulab/mockup/pinta_potes.py`):
    - a silhueta é medida linha a linha na borda limpa da foto e espelhada no eixo;
    - a tampa e o corpo são pintados em linear com a luz da foto;
    - o rótulo é enrolado pelo cilindro descontando a curva da elipse, b(h) = K·(h − H0), com a curva crescendo de cima para baixo.

    Ela achou que "ficou lindo".
  - **Gerar imagem com a arte de verdade como referência: Canva.** O `generate-image` do Canva aceita `imageReferences`.
  - Para subir cada imagem: `create-upload-url` e depois POST com os bytes crus (`Content-Type: application/octet-stream`).
  - O `prompt` vai com as palavras da Emi; o pedido detalhado vai no `user_intent`.
  - O gerador do Figma (`generate_image`) só aceita texto.
  - O Weave do Figma pede conta vinculada (não está vinculada).
  - **Não mandar a foto de referência de outra marca para o Canva editar.** Com a Grandorf junto, ele copiou a foto quase igual, com o pacote de ração GRANDORF na mão. Para editar uma versão aprovada, mandar só ela e o logo.
  - Para baixar em alta, coloca a mídia num design (`read-design` com `open_transaction`, depois `edit-design` com `insert_fill`/`update_fill`, depois `commit`) e roda `export-design` em PNG. O design-contêiner é o DAHarvHevXI, 1728 x 2304.
  - O resultado vem como mídia do Canva (`MAHart5B9Rw`, por exemplo). Pela API só sai a miniatura de 149 px; o arquivo grande só abre pelo link `canva.com/M/<id>` ou exportando um design que contenha a imagem.
- **Mais qualidade em foto gerada (a Emi: "só preciso de mais qualidade"):**
  - O Canva gera em ~1088 px e o Freepik estava sem crédito. Use o upscaler local `.claude/skills/artes-clientes/ferramentas/upscale.py`, com o modelo 4xNomosWebPhoto (ESRGAN em ONNX, baixado de huggingface.co/nesaorg/4xNomosWebPhoto_esrgan_fp32_opset17).
  - Ele roda na CPU, em blocos: 1088 px viram 2400 px em ~4 min.
  - O tecido e o fio do bordado ficam nítidos, sem inventar coisa.
- **Upscale + arte com texto: aumentar a foto ANTES de aplicar a arte.** Se o upscaler passa por cima do logo e das letras, elas ficam mastigadas. Aumente a foto base (e o recorte da pessoa, pelo alfa) e só depois aplique a arte, em alta, com o quadrilátero multiplicado pela escala.
- **Maison Caramelo (direção 02, clube de grife).**
  - Rodada 1: o medalhão oval com o retrato do caramelo em relevo no vinho (ref. 3) estava "literalmente copiando o outro". A porta em arco com o cachorro sentado também não serviu ("assim não").
  - O brasão gerado com escudo, cachorros em pé, coroa e louro ficou "horrível".
  - Na pesquisa de brasão ela escolheu 15 (oval floral em relevo) e 14 (Eros & Co.).
  - Ficou assim:
    - um caramelo empinado com uma florzinha na boca, em silhueta de vaso grego, gerado e vetorizado;
    - o nome em Cormorant espaçada;
    - o selo oval de borda recortada, prensado tom sobre tom.
  - A pose saltando foi descartada ("quero o sem ser ele correndo").
  - Mockup: rua gerada com o outdoor em branco, arte aplicada (painel vinho com o logo + a foto da campanha) e a pessoa recortada por cima.
- **Bordado:** fazer bordado em código (pontos, relevo, sombra) não convence: "nem parece bordado". Mande a foto com o logo aplicado e a referência de bordado para o Canva refazer só o bordado e, depois, passe pelo upscaler.
- **Toda etiqueta em branco que aparece na lâmina vira rótulo da marca** (a Emi: "tem um rótulo embaixo do logo que tá sem nada").
  - **Conferir se os objetos da cena fazem sentido entre si.** A foto antiga tinha frasco com tampa de rosca e um conta-gotas solto ao lado. A Emi: "tem que substituir a rosca por uma de conta-gotas".
    - O gerador do Figma não edita foto, só cria a partir de texto. Então a cena foi gerada de novo, já com conta-gotas e com a etiqueta em branco.
    - A arte foi aplicada com `marcas/aplica_etiqueta.py`: a borda de cima e a de baixo da etiqueta são medidas na foto e ajustadas como arco de elipse com inclinação.
    - Mesmo refeita (com supersampling, sem filete branco e com rótulo mais simples), a Emi achou "horrível" e pediu "um de comprimido, uma caixa".
    - Ficou a caixa (`marcas/miaulab/mockup/caixa/monta_caixa.py`), montada assim:
      - a caixa branca é gerada a 3/4;
      - os cantos são medidos com zoom de 5x;
      - a frente e a lateral recebem a arte por homografia, com a arte reduzida antes e a luz em linear;
      - a aba de cima é pintada;
      - a cartela de comprimidos, recortada com BiRefNet, volta por cima.
    - **Lição:** etiqueta pequena em vidro curvo fica com cara de colada. Caixa e faces planas aceitam a arte muito melhor. Em frasco, só com arte grande e simples. Antes de pintar, olhar onde o bicho encosta: uma máscara do gato por luminância pegava a borda escura do pote e deixava uma faixa branca.
  - **Exportar logo com letras giradas:** fotografar o palco inteiro e aparar pelo alfa (`marcas/toto/exporta-logo.mjs`). Recortar pela caixa do elemento corta o que passa dela. Para aplicar num pacote, recortar o pacote com BiRefNet (`marcas/aplica_pacote.py`); a máscara por cor falha na parte em sombra. Composição em `projeto/marcas/aplica.py`, que deforma a arte em perspectiva e herda a luz da foto; a lateral usa a luz da frente.
- **Logo no quadro da marca: centralizar pela tinta, dentro da moldura de seleção roxa.**
  - O olho lê a moldura (x 651-1067, y 12-406 da lâmina) como a caixa. A borda verde, com a sangria, não conta.
  - Medir a caixa dos pixels da cor do logo e igualar as folgas esquerda/direita e cima/baixo até a moldura.
  - Cada peça do logo (bicho, nome, linha de baixo) também fica no mesmo eixo.
  - Histórico da Emi: "não tá centralizado" (TOTÓ), "ainda tá sem equilíbrio" (MATILHA com o cachorro 17 px fora do eixo) e "claramente ainda não tá centralizado" (eu centralizava pela área verde, 9 px fora da moldura).
  - Na MIAU.LAB estava 10 px fora.
  - O dx positivo leva a tinta para a direita: para tirar folga da esquerda, dx diminui.
  - Depois, centralizado na moldura, ela achou que "foi demais" e pediu "um pouquinho de nada de volta". Ficou 3 px para a direita e para cima. O ponto certo, para o olho dela, fica entre a moldura e a área verde, um pouco mais perto da moldura.
- **Banho e tosa (direção 03): pelo solto.**
  - Pesquisa: `referencias/pelo-solto`. Ela escolheu 2 Haley Sue, 3 Moon Gazer e "principalmente" 20 Barking Barber.
  - v1, papel recortado (approxPolyDP): "quero mais refinado e arredondado, bem vintage". O BANHO & TOSA estava desalinhado: "péssimo".
  - v2, serifa macia com o poodle gerado ao lado: "a A tá melhor, mas tá com cara de IA". A cara de IA vem de:
    - **o bicho de clip-art gerado ao lado do nome;**
    - os brilhos genéricos;
    - o bloco todo centralizado.
  - v3 tira o clip-art e vira lettering:
    - "Pelo" e "Solto" escalonados e encaixados;
    - o "o" vira um pompom de poodle tosado (o bicho fica dentro da letra, como a pata no "O" do TOTÓ);
    - flores do Haley Sue;
    - o subtítulo com a largura exata de "Solto" (`textLength`).
  - v3 também foi reprovada ("não gosto ainda, busque mais referências até acertar; pode mudar o nome"). Na rodada 2 (`referencias/pelo-solto/rodada-2`) ela escolheu **3 Puff Paw + 4 The Tail Club** e manteve o nome.
  - Gerei um poodle sentado e ela disse "gosto dele assim". **Quando ela aprova um elemento gerado, usar do jeito que está.** Eu já estava simplificando as formas sem ela pedir.
  - Na v4, o poodle chapado fica colado no nome empilhado em minúsculas bolhudas (Gluten), com as gotinhas de brilho e as estrelinhas do Puff Paw.
  - Na v4, ela escolheu a A e pediu três coisas:
    - "brilhinhos 100% vetor": estrela de quatro pontas e gota lisa são clichê de vetor; trocar por respingo de pincel com borda tremida (feTurbulence + feDisplacementMap) e grão de tinta leve;
    - "mais movimento na fonte": letras dançando;
    - "banho & tosa igual ao título, pode ser mais delicado": subtítulo em fonte de outra família (itálico leve), entre fios finos que vão de margem a margem.
  - Alinhamento pela tinta com `measureText().actualBoundingBox*`: a mesma margem à esquerda nas três linhas, e o corpo e o espaçamento do "banho & tosa" são calculados juntos para ele terminar junto com "solto". Conferido em pixel.
- **Run club (direção 04): virou MATILHA running club.**
  - A identidade "AU" (número de peito na Graduate) foi reprovada: "feia, xoxa".
  - Pesquisa: `referencias/au-running-club/identidade`. Ela escolheu misturar 1 (RUN CLUB), 7 (TRC) e 18 (Wild Pup), lembrando que é corrida **com** cachorro.
  - Letras com pernas e tênis desenhadas à mão: "q porra feia eh essa". Desenhar figura à mão em SVG não funciona. Para silhueta de bicho, gerar (gpt-image) e limpar a borda (`marcas/au/limpa_silhueta.py`).
  - Ficou assim:
    - o cachorro gerado salta solto acima do nome;
    - MATILHA em Rubik Black Italic com balanço líquido;
    - RUNNING CLUB leve, espaçado e numa curva suave;
    - o vão entre o cachorro e o nome é igual ao vão entre o nome e o RUNNING CLUB (24 px, medido em pixel).
  - O nome "AU" era "feio". Ela pediu o cachorro desgrudado do nome, a curva "com menos curva e mais delicada" e depois "aproxima só um pouquinho, os dois na mesma distância".
  - Mockup:
    - a Grandorf (câmera baixa) + a Juicy Kibbles (roupa combinando), gerado no Canva com o logo de referência;
    - na rua, mangas lisas e só a guia na mão (a garrafinha "parece que ele tá segurando");
    - estampa de cachorros de corrida em raias, em `marcas/au/estampa`.
- **Logo do petisco: o que a Emi aprovou como caminho.** Foi a referência NOSY (`referencias/logo-petisco/12-nosy.jpg`): letra desenhada, gordinha e orgânica, com um detalhe só (a pata no lugar do "O"), em creme chapado sobre uma foto de textura com marcas de pata. Ela liberou mudar o nome, e a marca virou **TOTÓ**. A pata entra no **primeiro "O"**, na altura exata das maiúsculas, e o "Ó" final mantém o acento. A pata no fim lia "TOT" e quebrava a simetria ("não sei se parece totó").
- **Logo de letra desenhada precisa de assimetria**: as letras dançam, cada uma numa altura e num ângulo (como no NOSY, Puff Paw, Sandy Paws). Uma versão toda reta, alinhada e com o mesmo espaço ficou "muito estranha". Atenção: no recado "n tem aimetria" ela quis dizer *assimetria*; eu li "simetria" e endureci o logo.
- **Símbolo dentro da letra tem que manter a forma da letra**: a pata no lugar do "O" precisa de almofada redonda (o próprio O da fonte, maciço ou com o furo) e dedos por cima. A almofada em sino (triângulo) lia "A". Referências em `referencias/logo-petisco/pinterest-pata-no-o-*.jpg`.
- O que ela reprovou no caminho:
  - fonte técnica e reta (Nunito: "a fonte não tem nada a ver, a outra é desenhadinha, linda"); a escolhida foi a Cherry Bomb One, com cada letra levemente girada;
  - traços de "farejar" ao lado da pata ("esses bigodes nada a ver");
  - logos gerados por IA ("cara de IA horrível");
  - wordmark montado em código sem acabamento ("vetorizado assim não dá"). Vetor pode, mas com letra desenhada e bem resolvida.

## Frases da Emi (para lembrar o gosto)

- "legal a ideia mas a execução não, os recortes não se encaixam, parece literalmente copia e cola"
- "as imagens se repetem em alguns e eu queria que fosse menos cópia da ref"
- "eu não quero de jeito nenhum igual ao estilo cpf cnpj"
- "a capa anterior mil x melhor"
- "o quadradinho do Figma, a seleção tá fora do rosto do gatinho; aquele diretoria criativa, claramente na cara que você copiou do outro"
- "muito xoxo, muito sem graça. tem mil formas de fazer isso. pesquisa referência no Pinterest"
- "não é porque um post ficou bom que você vai fazer todos iguais. os posts precisam ser diferentes"
- "qual sentido de dar spoiler no que tá vindo?" · "muuuuito espaçamento entre o título" · "texto empilhado de um lado só"
- "falta uma textura" · "gostava mais quando a orelha do gato encostava na pílula" · "não tem problema encostar, passar um pouquinho, fica estilizado"
- "sempre pesquisar na internet, no Pinterest, dar uma olhada no Instagram, no que os designers andam postando, pra gente errar menos"
- "com exceção do último, TODOS tão com cara de IA, pegue referências e refaça" (marcas fictícias; o último era o rótulo MIAU.LAB)

## Referências que a Emi gostou (para calibrar o gosto)

- **Capas de revista com gato** (Pinterest, 12/11), três circuladas por ela, guardadas em `Emi/ems-5-direcoes-pet/referencias/favoritas-da-emi/`:
  - "Your Cat";
  - gato preto na frente de um nome condensado gigante;
  - "MEOW" amarelo com brilhos.
- O padrão das três: nome **gigante e pesado**, o bicho **na frente** das letras, cor chapada forte, pouco texto, brilho de quatro pontas.
- Na próxima capa, começar por aí.

## Identidade (resumo do DS)

- Cores: `violeta` #6225D8 domina, roxos (`ameixa` #3D1C46, `creative-purple` #482952, `plum` #5B216C), `ivory` #FFFBDE de respiro, `pink` #DD34A8 e `manteiga` #F2CF7A só como acento (1 ou 2 por tela).
- Fontes dos posts: Poppins + Instrument Serif, uma palavra em itálico por título (`manteiga` no escuro, `pink` no claro).
- Grafismos: `HalftoneStar`, grão, `SelectionBox`, `HandleTag` com cursor, marca d'água @ITSEMSDESIGN x3, selo original (nunca redesenhar).
- Voz: minúsculas, gen z na forma, profissional no conteúdo; fecha com pergunta aberta.
- **Encostar e passar um pouco é estilo (pedido da Emi, 12/11):** elementos podem se tocar e invadir um pouco uns aos outros. Exemplos:
  - a orelha do gato encostando na pílula;
  - a cabeça do gato na frente do nome da revista;
  - a pata em cima da enquete;
  - a etiqueta @ saindo do cartão;
  - um selo por cima da foto.

  "Fica bonito, fica algo estilizado." Evitar composição em que tudo fica certinho dentro da própria caixa, com respiro de segurança em volta de cada peça. O que não pode é cobrir rosto, olhos ou o texto que precisa ser lido.

## Formatos já feitos (referência)

### `PostCuradoria` · "5 direções criativas pra marcas pet" (12/11/2026, **aprovado**)
- Pedido: "um post assim [carrossel da @pivocriativo de direções criativas para marcas de beleza] mas em outra área, com a ID visual da EMS".
- Histórico de aprovação (leia antes de mexer):
  - v1, recortes em cor chapada: reprovada, "parece copia e cola".
  - v2, fotos inteiras na grade 3 × 3 da referência: "amei, mas as imagens se repetem e queria menos cópia da ref".
  - v3, um layout diferente por lâmina, capa marfim com índice e chamada com paletas: reprovada. A Emi **não quer layout diferente em cada lâmina**, e "a capa anterior mil x melhor".
  - v4: as lâminas de direção numa estrutura só, que foram aprovadas. Capa e chamada da v2 reprovadas.
  - v5 e v6: capa de revista e chamada em enquete, depois os ajustes de spoiler, título, equilíbrio e textura. **Aprovado** ("gostei muito do carrossel").
  - Referências usadas, com o que se pegou de cada uma: `Emi/ems-5-direcoes-pet/referencias/`.
- **Estrutura das lâminas de direção: uma só, repetida nas 5, própria da EMS** (não a grade 3 × 3 com cartão no meio da referência):
  - pet em destaque 640 × 860 em cima à esquerda;
  - coluna direita com a marca fictícia (com `SelectionBox` + cursor "emi") e uma foto quadrada;
  - faixa de baixo com o cartão na cor da série (`violeta` → `plum` → `wine` → `creative-purple` → `ameixa`), uma foto alta e a coluna paleta + letra ("Aa").
  - Respiro `ivory` de 18px, raio 22.
- **Foto não se repete no carrossel**, e variações da mesma cena contam como repetição. Por direção, 3 cenas diferentes: o bicho, o produto e uma cena extra (outro bicho, detalhe de material ou bastidor).
- **Capa** (v5): capa de revista.
  - Nome "direções" em Instrument Serif gigante atrás da cabeça do gato: recorte da mesma foto, alinhado, por cima do texto.
  - "criativas pra marcas *pet*" colado embaixo do nome, formando um bloco só. A Emi reclamou de "muito espaçamento entre o título".
  - Chamada de capa que não entrega o conteúdo: "5 universos pra sua marca pet sair do *óbvio*". **Capa não dá spoiler**: a lista das 5 direções foi reprovada ("qual sentido de dar spoiler no que tá vindo?").
  - Selo redondo `pink` "nenhuma é patinha + osso" e código de barras com o @.
  - A v4 foi reprovada por diagramação: seleção do Figma fora do rosto do gato, anotação "diretoria criativa" (cópia) e "5" gigante + pílula (estrutura da referência).
- **Chamada** (v5): enquete.
  - "qual delas tem a cara da sua *marca*?" e cartão de enquete com as 5 opções.
  - O gato levanta a pata e "aperta" uma opção (recorte por cima do cartão).
  - **Composição equilibrada**: título centralizado em cima, cartão à esquerda, "comenta o número da sua favorita" e a dm à direita acima do gato, assinatura embaixo à esquerda. A Emi reprovou "texto empilhado de um lado só".
  - Textura: estrelas em retícula de pontos iguais "pintadas" na parede (o mesmo grafismo da parede da capa), por trás do gato e da enquete, e grão mais forte. A Emi achou que faltava textura no fundo liso.
  - A orelha do gato encostando na pílula da dm ficou "mais bonito": deixar elementos se tocarem dá vida à composição.
  - A v4, com texto + gato + pílula, foi reprovada: "muito xoxo, sem graça".
- **Regra da Emi: "os posts precisam ser diferentes, senão eu postava a mesma coisa todo dia".**
  - Cada post do Instagram da EMS tem diagramação própria.
  - Não reaproveitar os recursos de outro post: anotação à mão com linha curva, seleção do Figma decorativa, marca d'água em fila, colagem em selo do "cpf x cnpj" (esse estilo ela não quer de jeito nenhum).
  - Não reaproveitar a estrutura da referência.
  - A identidade (cor, fonte, selo) se mantém; a diagramação muda.
  - Antes de diagramar capa e chamada, procurar referências de diagramação (Pinterest, capas de revista, adesivos de story) e escolher um conceito que caiba no tema.
- **Recorte "na frente do texto":** rembg (`birefnet-general`) salvando a máscara no tamanho da foto (sem cortar), borda endurecida (alfa < 70 vira 0, > 190 vira 255) para o texto de trás não vazar pelo pelo. Posicionar com os mesmos parâmetros da foto.
- Código reaproveitável: `Emi/ems-5-direcoes-pet/projeto/` (`direcoes.js` tem o conteúdo, `GRADE` em `carrossel.html` tem a estrutura; trocar o nicho = trocar `direcoes.js` e as fotos).
- Figma editável: https://www.figma.com/design/elmpB2QlAid4OFWruJL31H (time 4D). A versão aprovada fica na página **"carrossel final · 12/11"**; a página antiga tem as versões anteriores e os quadros das imagens geradas no Figma.
- Drive: pasta `EMS · @itsemsdesign` → `2026-11 · 5 direções criativas pra marcas pet` (`1BihRkZXTpaY704VBm0gmCygNapc3i9SP`), com os 7 PNGs finais, a visão geral e a legenda em Doc. A primeira versão está na subpasta "versão antiga (recortes, reprovada)".
- Próximos nichos sugeridos no DS: cafeterias, confeitarias, estúdio de tatuagem, academia e luta, moda autoral, clínica de estética.

## Aprendizados de produção

- **Geração de imagem, por ordem:**
  1. Nano Banana Pro pelo ElevenLabs (`gemini-3-pro-image`, 3:4 2K, ~US$ 0,22 cada). Os créditos acabaram em 12/11.
  2. Freepik Spaces: o plano é ilimitado no site, mas pelo conector recusa com "limite de uso" (não cobra). Os prompts ficam montados num Space para alguém rodar pelo site.
  3. Gerador de imagem do Figma (`generate_image`, `gemini-3.1-flash-image`). Funciona pelo conector, sai em ~1K (1376 × 768 ou 768 × 1376) e cria um quadro no arquivo: apagar depois de baixar.
  4. Higgsfield (0,78 crédito em 12/11).
- Fundo **#E9E9E9** só para objeto isolado que vai ser recortado (montagem 3D). Para moodboard e posts: **foto inteira na cena**, com o cenário na cor da direção. Recorte colado em cor chapada foi reprovado. Sempre "sem texto"; para tênis e afins, "sem logotipo".
- **Recorte local** com `rembg` (venv no scratchpad): `isnet-general-use` faz 44 fotos em 1 minuto; `birefnet-general` é melhor para branco perto do cinza (rótulo, tênis, tricô, tigela) mas estoura a memória se processar várias no mesmo processo: um processo por imagem.
- Instagram: as lâminas de um carrossel saem carregando `instagram.com/p/<id>/?img_index=N` no Chromium headless e lendo as `<img>` de 1080px (o embed não traz as imagens).
- **Exportar para o Figma, detalhes que já quebraram:**
  - cor por variável CSS (`fill="var(--lavanda)"`) some na imagem gerada, e as estrelas da chamada ficaram invisíveis: o exportador troca a variável pela cor calculada;
  - raio em % virava canto de 50px: o exportador converte para px;
  - arco (cantos diferentes) vai em `rr`;
  - para não mexer no que existe, `compacta.py "<página>"` monta numa página nova.
- **Figma editável a partir do HTML:** `projeto/figma/exporta.mjs` mede o carrossel no Chromium e gera uma cena por lâmina (quadros, textos com fontes reais, fotos, SVGs; padrões e retículas viram PNG); `montador.js` monta no Figma via `use_figma` (uma chamada por lâmina, ~11 KB) e `sobe.sh` envia as imagens para os IDs devolvidos (`upload_assets` com `nodeIds`). Saiu idêntico ao PNG. Não existe importador HTML→camadas nativo nesta sessão.
- **Foto pequena para capa:** ampliar 2x com Topaz (`topaz-image-upscale-v2` no ElevenLabs, ~US$ 0,09) antes de recortar.
- Drive: a EMS não tinha pasta; criada `EMS · @itsemsdesign` no Meu Drive do Cauã, uma subpasta por post (`AAAA-MM · título`). Runrun.it: não há card da EMS (marca pessoal da Emi).
- Sem pedir confirmação: escolher nicho, fotos e enquadramento sozinho e explicar no relatório.
