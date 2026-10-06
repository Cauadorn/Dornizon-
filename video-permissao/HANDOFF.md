# Prompt de passagem: vídeo "permissão" da Emily

Cole o texto abaixo numa sessão nova do Claude Code aberta em `C:\Users\Linki\Videos\Motion`.

---

Você vai continuar a edição de um vídeo da Emily (Emilly Silva, @itsemsdesign) no Remotion, rodando neste computador Windows. Esta pasta, `C:\Users\Linki\Videos\Motion`, é a pasta de trabalho: todos os vídeos brutos dela e o projeto ficam aqui.

## Onde está tudo

- **Projeto Remotion:** pasta `video-permissao` no repositório GitHub `Cauadorn/Dornizon-`, branch `claude/instagram-video-transcription-f82k8p`. Traga só essa pasta para `C:\Users\Linki\Videos\Motion\video-permissao`.
- **Vídeos brutos e áudio original:** pasta do Google Drive "video 2", da conta contatoemillyss@gmail.com, compartilhada por link: https://drive.google.com/drive/folders/14oXrtupIfk4-La7axSy2JfO1VXtMuS5o . Baixe todos os 35 arquivos para `C:\Users\Linki\Videos\Motion\brutos`. A lista de nomes e ids está em `video-permissao/tools/drive_files.tsv`.
- **Narração já editada:** `video-permissao/public/narracao.wav`, com 48,1 s. Ela já está limpa.

## Primeiros passos

1. Confira se o Node 20 ou mais novo e o ffmpeg estão instalados. Se faltar o ffmpeg: `winget install Gyan.FFmpeg`.
2. Em `video-permissao`, rode `npm install`.
3. Gere os clipes tratados: `npm run clips -- "C:\Users\Linki\Videos\Motion\brutos"`. Isso corta e trata a cor dos 23 trechos listados em `tools/clips.txt` e salva tudo em `public/clips`.
4. Abra o estúdio: `npm run studio`. Ele abre em http://localhost:3000, e a Emily quer acompanhar por ali.
5. Revise cena por cena com ela antes do render final: `npm run render`, que gera `out/permissao-1920x1080.mp4`.

Importante: o código em `src/Film.tsx` foi escrito e o estúdio compilou sem erro, mas o vídeo ainda não foi renderizado inteiro nem revisado visualmente. Espere ajustes de tempo, de enquadramento e de texto.

## O pedido da Emily

- Vídeo motivacional para o Instagram, mas no formato filme: **1920 × 1080**, estética de cinema. Faixas pretas de 2.39:1, grão, vinheta, cor de filme.
- Usar só os vídeos que fazem sentido com a narração. O vídeo não deve ficar longo.
- Transições, jogo de câmera e movimento em 3D. Ela não quer cara de vídeo cortado no CapCut.
- Pode ter cenas só de motion lettering, sem vídeo.
- As imagens da câmera Kodak (arquivos `102_18xx.AVI`, 640×480, 4:3) têm qualidade baixa de propósito, pelo efeito vintage. Os arquivos `C25xx.MP4` são 4K em perfil plano e precisam de tratamento de cor (já está em `tools/grade.txt`).
- Nada de vender o trabalho dela. É conteúdo para as pessoas se identificarem e compartilharem.
- Ela é direta e se frustra com volta e explicação longa. Mostre o resultado, pergunte pouco.

## Referências que ela mandou

- Reel https://www.instagram.com/reels/DeIHQZWxLNr/ : montagem de Nova York com cor de filme quente e teal, moldura redonda tipo lente antiga, cortes com borrão de movimento, trem e rua.
- Reel https://www.instagram.com/reels/DeJlw4NysOv/ : planos lentos e íntimos, rosto de perto, natureza, cor verde suave.
- Pinterest https://br.pinterest.com/pin/10977592838065054/ : lettering sans pequeno surgindo palavra por palavra, com um ponto laranja de destaque, e um círculo de cor que cresce até virar a tela inteira.
- Pinterest https://br.pinterest.com/pin/659988520429404280/ : "branding is ___" com a palavra rolando na horizontal, a atual em branco e as vizinhas em cinza, fundo preto.

## Narração final (falada pela Emily)

Por muito tempo, eu pedi desculpa por fazer o que eu amo. Explicava demais por que escolhi a arte. Comparava o meu tempo com o dos outros. E ficava esperando alguém me dizer que agora podia.

Teve dia que eu duvidei. Teve dia que eu achei bobagem insistir. Teve dia que eu quase guardei tudo e segui o caminho mais seguro.

Mas ninguém apareceu pra me dar essa permissão. E foi aí que eu entendi: ela nunca ia vir de fora.

Nem todo mundo vai entender o que você faz. E tá tudo bem. Não precisa ser pra todo mundo. Precisa ser de verdade pra você.

Então, se hoje você tá nesse lugar, de dúvida, de medo, de quase desistir... vai com calma. Mas vai.

E cá entre nós, daqui a alguns anos, você nem vai lembrar das vezes em que deu errado. Vai lembrar somente das vezes em que teve coragem.

## Como a narração foi editada

O áudio original é "WhatsApp Audio 2026-10-06 at 16.17.31.mp4", com 61 s. Ele tinha duas repetições: "mas ninguém apareceu" dito duas vezes, e a frase final gravada duas vezes (ficou a segunda). Os trechos usados do original foram 0,90–11,40 / 12,95–19,50 / 23,30–28,95 / 30,20–37,20 / 37,45–44,00 / 53,30–60,60 s, com pausas de 0,85 / 1,05 / 0,9 / 0,55 / 1,2 s entre eles. Depois o áudio passou por filtro passa-alta, redução de ruído, compressão e normalização a −16 LUFS. O tempo de cada palavra do áudio editado está em `src/words.json`.

## Estrutura do filme (tempos da narração editada; o vídeo começa 1,5 s antes)

| Narração (s) | Cena | Clipe |
| --- | --- | --- |
| −1,5–3,7 | abre as faixas pretas, ela de perfil esperando na plataforma | plataforma-espera (C2536) |
| 3,7–6,0 | "explicava demais por que escolhi a arte": mãos com cartão postal na livraria | carta-livraria (C2552) |
| 6,0–7,95 | "comparava o meu tempo": ela parada com o trem passando borrado | trem-passando-ela (C2540) |
| 7,95–10,95 | "ficava esperando alguém me dizer que agora podia" | ela-esperando-tela (C2537) |
| 10,95–16,3 | parede 3D de filmes Kodak voando + lettering "teve dia / que eu" com a palavra rolando: duvidei / achei bobagem insistir / quase guardei tudo | k-paulista-placa, k-masp-1867, k-escada-metro |
| 16,3–18,95 | "segui o caminho mais seguro": escada rolante descendo, na moldura Kodak em 3D | k-escada-metro (102_1876) |
| 18,95–21,15 | "mas ninguém apareceu": portas do metrô fechando, porta vazia | portas-fechando (C2535) |
| 21,15–22,75 | "foi aí que eu entendi": rosto virando pra câmera | rosto-virando (C2547) |
| 22,75–25,7 | bloco violeta #6225D8 cresce em círculo: "ela nunca ia vir / *de fora*." | só lettering |
| 25,65–28,2 | "nem todo mundo vai entender o que você faz": Cauã desenhando | caua-desenhando (C2560) |
| 28,2–29,35 | close do lápis | lapis-close (C2559) |
| 29,35–31,0 | ela na livraria | ela-livraria (C2555) |
| 31,0–33,3 | livro "Memórias póstumas de Brás Cubas" + lettering "precisa ser / *de verdade* / pra você." | livro-bras-cubas (C2553) |
| 33,3–35,95 | "se hoje você tá nesse lugar de dúvida": homem na plataforma, trem passando | homem-trem (C2532) |
| 35,95–38,05 | "de medo, de quase desistir": Kodak dela no banco da estátua | k-banco-monica (102_1868) |
| 38,05–38,95 | "vai com calma": mãos paradas na mesa | maos-calma (C2546) |
| 38,95–40,85 | "mas vai.": ela vira e sorri + lettering grande "mas *vai.*" | ela-vira-sorri (C2537) |
| 40,85–45,55 | "daqui a alguns anos...": segunda parede 3D de memórias Kodak, com data no canto tipo câmera antiga | k-estatua-monica, k-masp-1869, k-estatua-branca, k-caua-selfie |
| 45,55–47,3 | "vai lembrar das vezes em que teve coragem": ela sorrindo pra câmera | final-sorriso (C2540) |
| 47,3–51,6 | tela preta, "*coragem*" letra por letra + ponto violeta + @ITSEMSDESIGN pequeno | só lettering |

Acabamento em todas as cenas: faixas 2.39:1 que abrem no começo e fecham no fim, legenda pequena em minúsculas dentro da faixa de baixo (some quando há lettering grande), grão animado, vinheta, flicker leve e três vazamentos de luz quentes nas viradas de parte. Transições usadas: whip com borrão direcional, giro 3D tipo cubo, zoom com desfoque, empurrão 3D em profundidade, íris circular.

Fontes: Instrument Serif (itálico na palavra de destaque) e Inter. Cores: marfim #FFFBDE nos textos e violeta #6225D8 como único destaque.

O que ainda não entrou e pode ser sugerido: trilha sonora instrumental, que hoje só tem o som ambiente baixo dos próprios clipes. O clipe vertical do trem (trem-vertical, C2543) foi preparado e não foi usado.
