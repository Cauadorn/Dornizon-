# EMS (@itsemsdesign · Emilly Silva)

- **Motor (Design System no Claude):** https://claude.ai/artifact/DNhPwJnJSH9f4gih32oQGa (versão 10 em 12/11/2026)
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

### `PostCuradoria` · "5 direções criativas pra marcas pet" (12/11/2026)
- Pedido: "um post assim [carrossel da @pivocriativo de direções criativas para marcas de beleza] mas em outra área, com a ID visual da EMS".
- Estrutura (7 lâminas 1080 × 1350): capa com foto recortada + número gigante + adesivo de trocadilho; 5 lâminas em grade 3 × 3 (colunas 308/428/308, linhas 408/506/408, respiro `ivory`, raio 22) com cartão central na cor da série (`violeta` → `plum` → `wine` → `creative-purple` → `ameixa`); chamada em `plum` com pergunta + "me chama na dm" + selo.
- Cada direção: 5 fotos recortadas pousadas na cor da direção + paleta (nome e hex) + tipografia ("Aa", amostra, nome da fonte) + marca fictícia desenhada em código (o quadro com `SelectionBox` e cursor "emi").
- Código reaproveitável: `Emi/ems-5-direcoes-pet/projeto/` (`direcoes.js` concentra todo o conteúdo; trocar o nicho = trocar esse arquivo e as fotos).
- Figma editável: https://www.figma.com/design/elmpB2QlAid4OFWruJL31H (time 4D) · Drive: pasta `EMS · @itsemsdesign` → `2026-11 · 5 direções criativas pra marcas pet` (`1BihRkZXTpaY704VBm0gmCygNapc3i9SP`), com os 7 PNGs, a visão geral e a legenda em Doc.
- Próximos nichos sugeridos no DS: cafeterias, confeitarias, estúdio de tatuagem, academia e luta, moda autoral, clínica de estética.

## Aprendizados de produção

- **Magnific/Freepik** pode estar sem créditos (só 2 em 12/11) e o Higgsfield também: o **Nano Banana Pro** roda pelo ElevenLabs (`gemini-3-pro-image`), 4 variações por prompt (~US$ 0,22 cada), saída 1376 × 768. Peça de capa grande: ampliar antes (ver Topaz abaixo).
- Prompt sempre em português, fundo **#E9E9E9**, "sem texto"; para tênis e afins, "sem logotipo" (uma variação veio com listras de marca conhecida: descartada).
- **Recorte local** com `rembg` (venv no scratchpad): `isnet-general-use` faz 44 fotos em 1 minuto; `birefnet-general` é melhor para branco perto do cinza (rótulo, tênis, tricô, tigela) mas estoura a memória se processar várias no mesmo processo: um processo por imagem.
- Instagram: as lâminas de um carrossel saem carregando `instagram.com/p/<id>/?img_index=N` no Chromium headless e lendo as `<img>` de 1080px (o embed não traz as imagens).
- **Figma editável a partir do HTML:** `projeto/figma/exporta.mjs` mede o carrossel no Chromium e gera uma cena por lâmina (quadros, textos com fontes reais, fotos, SVGs; padrões e retículas viram PNG); `montador.js` monta no Figma via `use_figma` (uma chamada por lâmina, ~11 KB) e `sobe.sh` envia as imagens para os IDs devolvidos (`upload_assets` com `nodeIds`). Saiu idêntico ao PNG. Não existe importador HTML→camadas nativo nesta sessão.
- **Foto pequena para capa:** ampliar 2x com Topaz (`topaz-image-upscale-v2` no ElevenLabs, ~US$ 0,09) antes de recortar.
- Drive: a EMS não tinha pasta; criada `EMS · @itsemsdesign` no Meu Drive do Cauã, uma subpasta por post (`AAAA-MM · título`). Runrun.it: não há card da EMS (marca pessoal da Emi).
- Sem pedir confirmação: escolher nicho, fotos e enquadramento sozinho e explicar no relatório.
