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

### `PostCuradoria` · "5 direções criativas pra marcas pet" (12/11/2026, v3)
- Pedido: "um post assim [carrossel da @pivocriativo de direções criativas para marcas de beleza] mas em outra área, com a ID visual da EMS".
- Histórico de aprovação:
  - v1, recortes pousados em cor chapada: reprovada ("parece copia e cola").
  - v2, fotos inteiras na grade 3 × 3 da referência: "amei, mas as imagens se repetem e queria menos cópia da ref".
  - v3, um layout por direção e nenhuma foto repetida: atual.
- **Da referência só se pega a ideia** (5 universos por nicho), nunca a estrutura. Não repetir:
  - a mesma grade em todas as lâminas;
  - o cartão no meio de uma 3 × 3;
  - o "5" gigante com pílula na capa;
  - o fecho "quer uma marca…?".
- **"Os posts têm que ser diferentes":** cada lâmina de direção tem estrutura própria, que conversa com o universo dela:
  - tirinha de gibi;
  - página de revista;
  - arcos anos 70;
  - foto de ação com patch;
  - ficha de laboratório com cápsula.
- O vocabulário é o mesmo nas 5 lâminas: marfim entre quadros de raio 22, cartão na cor da série (`violeta` → `plum` → `wine` → `creative-purple` → `ameixa`), paleta com nome e hex, letra da direção, marca fictícia desenhada, `SelectionBox` + cursor "emi".
- **Foto não se repete no carrossel**, e variações da mesma cena contam como repetição. Por direção, 3 cenas diferentes: o bicho, o produto e uma cena extra (outro bicho, detalhe de material ou bastidor). O resto dos quadros é gráfico: marca, paleta, letra.
- **Capa:** fundo marfim, gancho em serifa ("marca pet sem *patinha*"), índice das 5 direções com bolinhas de cor e foto em quadro.
- **Chamada:** "qual das 5 é a *sua*?" com as 5 paletas em fichas numeradas, "comenta o número", dm e selo.
- Código reaproveitável: `Emi/ems-5-direcoes-pet/projeto/` (`direcoes.js` tem conteúdo e layout; trocar o nicho = trocar esse arquivo e as fotos).
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
