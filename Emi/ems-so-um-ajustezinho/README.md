# EMS: "é só um ajustezinho"

Carrossel de 6 lâminas (1080 × 1350) para a @itsemsdesign, pilar **Bastidor e processo**, no design system EMS. Tema: como a falta de briefing transforma "só um ajustezinho" em refação, e por que um briefing bem feito economiza tempo dos dois lados. A culpa fica no processo, nunca no cliente ("ninguém é o vilão dessa história").

Referência de formato: post da @agrizzart sobre manter o perfil ativo com a agenda cheia (`referencias/post-agrizzart/`). Da referência veio só o **ritmo**. Tema, texto, cores, letras, objetos e diagrama são da EMS.

| Da referência (o "assim") | Na EMS (o que muda) |
| --- | --- |
| Capa com frase grande e um objeto 3D por cima do texto (semáforo) | "ajuste*z*inho”" em `serif-hero`, em escada, com a pilha de versões amassadas por cima e etiquetas de arquivo em `label` |
| Slide de "ciclo" com triângulo tracejado | "o loop da *refação*" em quadros de Figma (briefing → versão 1 → ajustezinho → versão 27) com setas de protótipo violeta e a borracha gasta no meio |
| Slide escuro de virada com meme de celebridade | Piada própria: a pasta do projeto com `logo_final_agora_vai.png` e companhia, `SelectionBox` + cursor "emi" na v1 e o adesivo "spoiler: aprovaram a versão 1". Sem foto de terceiros |
| Slide de solução com objeto (caderno) | "o que cansa é ajuste sem *norte.*" com a bússola: o briefing |
| Fundos cinza, preto e rosa; letra condensada em CAIXA ALTA; azul de destaque | Violeta, marfim, ameixa, lavanda-2 e plum; Instrument Serif + Poppins em minúsculas; manteiga e rosa só como acento |
| "DESIGN DE POST" nos cantos | Marca d'água @ITSEMSDESIGN 3x no topo + `HandleTag` com cursor |
| Chamada "comenta DESTRAVA" | Pergunta aberta (lâmina 5, a primeira pergunta do briefing da Emi) + "comenta BRIEFING que eu te mando na dm" (lâmina 6), com o selo original |

## Versões

- **v1** (`entrega/v1/`, `projeto/carrossel.html`): primeira versão, digital e chapada, no sistema EMS.
- **v5** (`entrega/v5/`, `projeto/carrossel-v5.html`): **a atual.** Desenhada como **uma faixa só** (6480 × 1350) e cortada em 6. Textura de verdade (tecido, papel, linho, xadrez da paleta, letra com falha de impressão, objetos em duotone) e **um recurso diferente em cada lâmina**:

| Lâmina | Recurso | Princípio de onde veio |
| --- | --- | --- |
| 1 · capa | "ajuste" e "zinho”" se atropelando com falha de impressão + papel amassado em duotone (tinta → violeta-2 → marfim) | @carolrech, jantar (matéria, letra impressa) |
| 2 · loop | Página de caderno pontilhado com espiral, divisórias por fase do projeto, post-its e a borracha reta no meio (**só nesta lâmina**) | @carolrech, agenda (a peça como objeto) |
| 3 · pasta | Janela de computador retrô com os ícones da EMS na barra e a v1 selecionada pelo cursor "emi" | @danibloom.design (um cenário que é o roteiro) |
| 4 · norte | "*norte.*" gigante + bilhete com fita + bússola em duotone (tinta → plum → manteiga) | @carolrech, jantar |
| 5 · pergunta | A primeira pergunta do briefing numa conversa no celular (avatar = mascote da EMS) | @rafaelalimadesigner_ |
| 6 · chamada | "brie*f*ing?" impresso + pílula com cursor "emi", selo e xoxo | sistema EMS |

**Conectividade (composição contínua, nunca fio):** em todo corte o fundo continua e um objeto atravessa de verdade, metade de cada lado.

| Corte | O que atravessa | Fundo |
| --- | --- | --- |
| 1 \| 2 | pilha de papel amassado | tecido violeta contínuo |
| 2 \| 3 | a janela começa no fim da lâmina 2 (bolinhas da barra) | diagonal violeta → xadrez cruzando o corte |
| 3 \| 4 | bilhete colado por cima da janela, fita em cima do corte | diagonal xadrez → ameixa |
| 4 \| 5 | bússola com o centro no corte | diagonal ameixa → linho |
| 5 \| 6 | estrela da EMS colada por cima do celular | diagonal linho → violeta |

O fundo inteiro está em `.fundo` (coordenadas da faixa); cada lâmina posiciona o que atravessa com coordenadas além de 0–1080 (ex.: bússola em `left:760px; width:640px` = centro em 1080).

Grafismos: só os do design system (brilho, espiral, coração, estrela, xoxo, `SelectionBox`, cursor "emi", `HandleTag`), tingidos na cor da paleta, com motivo. Traço à mão só nas setas do diagrama do loop.

Descartadas: v2 (caderno repetido em 3 lâminas, brilhos que não são da EMS), v3 (voltou demais para a v1) e v4 (tinha um fio atravessando as lâminas como "conexão": reprovado, nunca mais). As regras ficaram registradas no Design System da EMS (README › "Regras de carrossel" e conteúdo › "Carrossel: regras aprendidas").

Referências em `referencias/outras/`.

## Lâminas

1. **Capa** (`violeta`): "“é só um / ajuste*z*inho”" + pilha de papel amassado (v3_ajuste.png, v_final.png, v27_ok.png). "e foi assim que a gente chegou na versão 27."
2. **Tensão** (caderno sobre tecido violeta): "sem briefing, vira isso: / o loop da *refação*". Fecho: "ninguém é o vilão dessa história. / faltou combinar o destino antes de sair."
3. **Piada** (janela retrô sobre xadrez): "teste rápido: / ache o arquivo *final*". "sem briefing, cada versão é um chute. e chute cansa os dois lados."
4. **Virada** (tecido ameixa): "calma: ajuste faz parte. / o que cansa é ajuste sem *norte.*" + bússola. "briefing bem feito é o norte do projeto: todo mundo sabe pra onde vai, e o ajuste vira refinamento, não recomeço."
5. **Pergunta aberta** (linho claro): "a primeira pergunta do meu briefing: / como é a sua marca em *três* palavras?" A pergunta aparece numa conversa no celular; a resposta vai nos comentários.
6. **Chamada** (`violeta`): "quer as outras perguntas do meu / brie*f*ing?" + "comenta “BRIEFING” que eu te mando na dm" + selo + emsdesign.com.br.

> ⚠️ **Antes de postar:** a chamada promete mandar por dm as perguntas do briefing da Emi. Elas precisam estar prontas num formato fácil de mandar (PDF, nota ou link), e alguém precisa responder quem comentar "BRIEFING". A lâmina 5 diz que "como é a sua marca em três palavras?" é a primeira pergunta do briefing: se no briefing dela a primeira for outra, troque o texto da lâmina ou a ordem do briefing.

## Legenda

```
“é só um ajustezinho” — e foi assim que a gente chegou na versão 27.

ajuste faz parte de qualquer projeto. o que cansa (quem pediu e quem desenha) é ajuste sem direção: cada versão vira um chute, e chute quase nunca acerta de primeira.

é pra isso que serve o briefing. não é burocracia, é o norte do projeto: todo mundo sabe pra onde vai, e o ajuste vira refinamento, não recomeço.

comenta “BRIEFING” que eu te mando na dm as perguntas que eu faço antes de desenhar qualquer marca.

e me conta: como é a sua marca em três palavras?

↳ identidade visual, social media e site: dm aberta

#identidadevisual #brandingdesign #designgrafico #branding #processocriativo
```

## Elementos gerados

Nano Banana Pro (`gemini-3-pro-image`, pelo ElevenLabs, 4 variações por prompt, 1376 × 768), prompts em português com fundo #E9E9E9, no modelo "Objeto 3D recortado" de `geracao-de-imagem.md`. Recorte com `rembg` BiRefNet (papel e borracha brancos perto do #E9E9E9). Escolhidas: papel-1, bussola-3 e, para a borracha, a variação 3 (`borracha-reta.png`, nivelada pelo eixo do objeto: a 1 estava 13° torta). Originais em `projeto/geradas/`, recortes em `projeto/recortes/`. As outras variações ficaram no flow "EMS — carrossel ajustezinho (objetos)" no ElevenLabs.

- **Papel amassado (capa):** Fotografia de produto de uma pilha de sete bolas de papel sulfite amassado, papel branco levemente marfim com rabiscos de lápis e traços de caneta violeta #6225D8 aparecendo entre as dobras, amontoadas umas sobre as outras formando um pequeno monte, uma bola rolando um pouco afastada, luz de estúdio suave vinda da esquerda, sombras de contato delicadas entre as bolas, textura realista de papel, foco nítido em toda a peça, enquadramento centralizado com respiro nas bordas, fundo liso #E9E9E9, sem sombra projetada no chão, sem texto legível, sem logotipo, sem outros objetos.
- **Borracha (lâmina 2):** Fotografia de produto de uma borracha escolar branca com cinta de papel violeta #6225D8 lisa e sem texto, muito gasta de tanto apagar, a ponta exposta desgastada, torta e arredondada, alguns farelos de borracha espalhados bem perto dela, objeto deitado em três quartos, luz de estúdio suave vinda da esquerda, sombras de contato delicadas, textura realista de borracha e papel, foco nítido em toda a peça, enquadramento centralizado com respiro nas bordas, fundo liso #E9E9E9, sem sombra projetada no chão, sem texto, sem logotipo, sem outros objetos.
- **Bússola (lâmina 4):** Fotografia de produto de uma bússola de bolso antiga de latão dourado, aberta, mostrador marfim liso sem letras e sem números, apenas marcações finas de traço, agulha bicolor em violeta #6225D8 e manteiga #F2CF7A, vidro limpo e brilhante, vista de cima em três quartos levemente inclinada, luz de estúdio suave vinda da esquerda, sombras de contato delicadas, textura realista de metal escovado, foco nítido em toda a peça, enquadramento centralizado com respiro nas bordas, fundo liso #E9E9E9, sem sombra projetada no chão, sem texto, sem logotipo, sem outros objetos.

O resto é desenhado em código com os tokens: estrela em retícula (`HalftoneStar`), retícula fina e grão, `SelectionBox`, cursor "emi", `HandleTag`, marca d'água, os quadros do loop, a janela da pasta e os campos de resposta. O selo é o arquivo original (`selo-ems.png` do design system), sem alteração.

## Arquivos

- `projeto/carrossel.html` (v1) e `projeto/carrossel-v5.html` (v5): as 6 lâminas lado a lado. Abra no navegador para editar texto e posição.
- `projeto/render.mjs`: `node render.mjs` gera a v1 em `entrega/v1/`; `node render.mjs carrossel-v5.html v5` gera a v5 em `entrega/v5/` (lamina-01..06.png + visao-geral.jpg).
- `entrega/v5/`: PNGs finais 1080 × 1350 para subir no Instagram.
