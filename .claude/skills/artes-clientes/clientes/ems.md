# EMS (@itsemsdesign · Emilly Silva)

- **Motor (Design System no Claude):** https://claude.ai/artifact/DNhPwJnJSH9f4gih32oQGa (versão 12 em 12/11/2026)
  - Ler sempre: `project/README.md` (voz, cor, tipografia, grafismos, selo), `project/conteudo.md` (pilares, estruturas de carrossel, banco de ideias, legenda), `project/geracao-de-imagem.md` (prompts) e o componente do formato pedido em `project/components/<Nome>/README.md`.
  - Artes finais mais novas: grupo de assets **Posts** do DS (subir lá toda arte nova, com registro no índice `assetGroups.Posts`).
- **Skill própria:** `marca-ems` (abre o DS). Este arquivo guarda o que foi aprendido fazendo as peças.
- **Projetos no repositório:** `reel-ems/` (reel "provas"), `capas/` (capa de reel), `Emi/ems-5-direcoes-pet/` (carrossel de curadoria).

## Identidade (resumo do DS)

- Cores: `violeta` #6225D8 domina, roxos (`ameixa` #3D1C46, `creative-purple` #482952, `plum` #5B216C), `ivory` #FFFBDE de respiro, `pink` #DD34A8 e `manteiga` #F2CF7A só como acento (1 ou 2 por tela).
- Fontes dos posts: Poppins + Instrument Serif, uma palavra em itálico por título (`manteiga` no escuro, `pink` no claro).
- Grafismos: `HalftoneStar`, grão, `SelectionBox`, `HandleTag` com cursor, marca d'água @ITSEMSDESIGN x3, selo original (nunca redesenhar).
- Voz: minúsculas, gen z na forma, profissional no conteúdo; fecha com pergunta aberta.

## Formatos já feitos (referência)

### `PostCuradoria` · "5 direções criativas pra marcas pet" (12/11/2026, v4)
- Pedido: "um post assim [carrossel da @pivocriativo de direções criativas para marcas de beleza] mas em outra área, com a ID visual da EMS".
- Histórico de aprovação (leia antes de mexer):
  - v1, recortes em cor chapada: reprovada, "parece copia e cola".
  - v2, fotos inteiras na grade 3 × 3 da referência: "amei, mas as imagens se repetem e queria menos cópia da ref".
  - v3, um layout diferente por lâmina, capa marfim com índice e chamada com paletas: reprovada. A Emi **não quer layout diferente em cada lâmina**, e "a capa anterior mil x melhor".
  - v4: a atual.
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
- Figma editável: https://www.figma.com/design/elmpB2QlAid4OFWruJL31H (time 4D) · Drive: pasta `EMS · @itsemsdesign` → `2026-11 · 5 direções criativas pra marcas pet` (`1BihRkZXTpaY704VBm0gmCygNapc3i9SP`), com os 7 PNGs, a visão geral e a legenda em Doc.
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
- **Figma editável a partir do HTML:** `projeto/figma/exporta.mjs` mede o carrossel no Chromium e gera uma cena por lâmina (quadros, textos com fontes reais, fotos, SVGs; padrões e retículas viram PNG); `montador.js` monta no Figma via `use_figma` (uma chamada por lâmina, ~11 KB) e `sobe.sh` envia as imagens para os IDs devolvidos (`upload_assets` com `nodeIds`). Saiu idêntico ao PNG. Não existe importador HTML→camadas nativo nesta sessão.
- **Foto pequena para capa:** ampliar 2x com Topaz (`topaz-image-upscale-v2` no ElevenLabs, ~US$ 0,09) antes de recortar.
- Drive: a EMS não tinha pasta; criada `EMS · @itsemsdesign` no Meu Drive do Cauã, uma subpasta por post (`AAAA-MM · título`). Runrun.it: não há card da EMS (marca pessoal da Emi).
- Sem pedir confirmação: escolher nicho, fotos e enquadramento sozinho e explicar no relatório.
