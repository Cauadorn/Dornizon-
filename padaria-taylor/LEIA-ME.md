# Padaria da Taylor: pesquisa e conceito

Projeto conceitual de fã para o portfólio, no formato "E se a Taylor Swift me contratasse…". Não tem vínculo com a Taylor Swift, a gravadora ou qualquer marca dela.

## Marca: Loaf Story, era folklore/evermore (versão atual)

Segue o estilo das referências (Don Rollos, The Little Oven e o café "mode"): mascote, rabiscos de traço único, letra gorda e simpática, poucas cores com nome e as peças aplicadas.

- **Mascote, a betty.** Uma gata em posição de pão (na internet, *cat loaf*), Scottish Fold de orelha dobrada como as gatas da Taylor, vestindo o cardigã de tricô com estrela bordada. O nome vem de uma personagem do *folklore*.
- **Assinatura.** "loaf story" em minúsculas, como os títulos de *folklore* e *evermore*, em Fraunces Black macia. Embaixo, "a small, free business" em IM Fell DW Pica itálico, a mesma família de serifa antiga dos dois discos.
- **Rabiscos:** pão, pote de fermento, cabana, pinheiro, caneca, cesta, rolo e colher, biscoito, estrela e raminho. Viram padronagem e cena.
- **Cores:**
  - cardigã `#F2EADB`
  - neblina `#D9DCD3`
  - musgo `#6E7A55`
  - ferrugem `#B5582D` (o casaco xadrez do *evermore*)
  - lenha `#3A2A20` (o traço)
- **Peças:**
  - saco de papel impresso (foto);
  - cardápio em que tudo custa "free";
  - selo sobre a padronagem;
  - a cena da mesa da cabana.

| Pasta | O que tem |
|---|---|
| `01-marca/ilustracao/` | `betty.svg` (colorida), `betty-impressao.svg` (a uma cor), `cena.svg`, `padrao-*.svg` e `rabiscos/` (um SVG por desenho). |
| `02-apresentacao/` | 7 lâminas (HTML e PNG 1080 x 1350). |
| `03-mockups/` | Saco impresso (foto e recorte 4:5). |
| `fotos-geradas/` | Fotos-base dos sacos (ElevenLabs). |
| `_ferramentas/` | Scripts: `betty.py`, `rabiscos.py`, `cena.py`, `camadas.js`, `mockup.py` e `render.js`. |

---|---|
| `01-marca/ilustracao/` | A Doughgirl em SVG, com uma versão para fundo menta. |
| `02-apresentacao/` | As lâminas (HTML e PNG 1080 x 1350). |
| `03-mockups/` | Saco com o adesivo (foto e recorte 4:5). |
| `fotos-geradas/` | Fotos-base dos sacos, geradas na ElevenLabs. |
| `_ferramentas/` | Scripts: `doughgirl.py` (mascote), `adesivo.js` e `escrita.js` (camadas), `mockup.py` (colagem na foto) e `render.js` (lâminas). |

---

Pesquisa feita em 12/11/2026. As fontes estão no fim do arquivo.

---

## 1. O que encontrei

A Taylor não tem padaria. Ela tem uma piada: num vídeo de bastidor do clipe de "Patient Zero" (set./out. 2026), ela entrega pão caseiro para a equipe às 4h da manhã. Quando agradecem, responde: **"Thank you for supporting my small, free business"** ("obrigada por apoiar meu pequeno negócio gratuito"). Essa frase saiu de uma fonte só (Reality Tea), então é melhor citar como "relatado".

**Esse é o gancho do projeto: dar marca ao negócio que ela inventou de brincadeira.**

### Linha do tempo do pão

| Quando | O que aconteceu |
|---|---|
| 2014 | Faz **cookies de açúcar com chai e cobertura de eggnog com canela** para as *Secret Sessions* do 1989 (fãs ouvindo o disco na casa dela). No Instagram, chama de **"Christmas in September"**. A receita, escrita à mão, sai no Tumblr e é uma variação da massa da Joy the Baker. |
| 2023–2024 | Faz **Pop-Tarts caseiras** para a linha ofensiva dos Chiefs (contado pelo técnico Andy Reid em fev./2024). Em jun./2024, o Travis diz que ela "faz uma ótima Pop-Tart e um ótimo cinnamon roll". |
| mai./2025 | Manda uma caixa de Pop-Tarts (morango, framboesa e mirtilo) para a equipe de uma sessão de fotos do Travis, com o bilhete à mão "Have a great shoot! Love Taylor". A marca Pop-Tarts pede a receita em público. |
| jul./2025 | Aniversário de 33 anos da Selena Gomez: pão de **blueberry com limão** com corte em folhas e flores, etiqueta "Selena Super + Benny Bowl", bilhete **"It's a loaf story"** (trocadilho com "Love Story") e uma cesta com vela da Le Labo. |
| 13/ago./2025 | No podcast *New Heights* (o mesmo em que anuncia o *The Life of a Showgirl*), diz que está **"muito fundo numa obsessão por sourdough que tomou conta da minha vida"**. Detalhes do podcast: <ul><li>Sabores: canela com passas, mirtilo, limão e espiral de canela.</li><li>Um **Funfetti** (com granulado colorido) para as sobrinhas do Travis, que amam arco-íris.</li><li>O favorito do Travis é o de **mirtilo**; ele pediu dois pães no treino.</li><li>Ela manda mensagem para os amigos pedindo opinião sobre o pão.</li><li>Ela tem **"uma obsessão de confeitaria diferente a cada seis meses"**.</li></ul> |
| out./2025 | Jenny Han recebe pão com **adesivos de gato** e bilhete à mão. |
| fim de 2025 | Jimmy Fallon recebe pão com a etiqueta **"The Loaf of a Doughgirl"** (trocadilho com o álbum). |
| nov./2025 | Kylie Kelce: ela "faz um sourdough de respeito". |
| 9/jan./2026 | Jantar no Bird Streets Club, em Los Angeles. As irmãs Haim e o Sombr saem com pão em **saco de papel pardo** e **adesivo "Original Sourdough!"**. Os detalhes: <ul><li>Etiqueta escrita à mão: **"Are you bready for it?"** (trocadilho com "...Ready For It?").</li><li>Corte em **folha e flor**.</li><li>O do Sombr era de mirtilo.</li><li>**A Taylor não aparece em nenhuma foto, só o pão saindo pela porta.**</li></ul> |
| abr./2026 | JuJu Smith-Schuster (Chiefs): os doces dela são "fire". |
| 3/jul./2026 | Casa com o Travis Kelce no Madison Square Garden. |
| set./2026 | No Emmy, Kelli Giddish conta que ela levou **cookies de sourdough com manteiga noisette e gotas de chocolate** para o elenco de *Law & Order*. A gata dela, Olivia Benson, tem o nome da personagem dessa série. |
| set./out. 2026 | Clipe de **"Patient Zero"** (single do *Showgirl: The Encore*, com Dakota Johnson e Colin Farrell, dirigido por ela). A era nova troca o laranja por **preto e cinza**. No bastidor, ela leva pão às 4h e solta a piada do "small, free business". |

### O que é "a cara dela" nisso tudo

- **Ela dá, não vende.** O pão é presente, sempre com nome de quem recebe.
- **Escreve à mão.** Etiqueta, bilhete, receita. É o mesmo hábito das cartas para fãs.
- **Faz trocadilho com as próprias músicas:** "It's a loaf story", "Are you bready for it?", "The Loaf of a Doughgirl".
- **A embalagem é simples e caseira:** saco pardo, adesivo redondo, adesivo de gato e cesta. Não tem cara de confeitaria de luxo.
- **O pão tem desenho:** o corte (*scoring*) em folhas e flores.
- **Ela tem eras:** uma obsessão de confeitaria a cada seis meses, como os álbuns. Primeiro o cookie de chai, depois a Pop-Tart, agora o sourdough.
- **De onde ela vem:**
  - Cresceu numa fazenda de árvores de Natal na Pensilvânia (Pine Ridge Farm). Daí o "Natal em setembro" do cookie.
  - O número da sorte dela é o 13 (nasceu num dia 13). **Na padaria, a "dúzia de padeiro" tem 13.**
  - Tem três gatos: Meredith, Olivia e Benjamin. Esses dois detalhes são conhecidos dos fãs, mas não achei fonte boa na busca de hoje.

---

## 2. Conceito

**A marca do pequeno negócio gratuito da Taylor.** Uma padaria que não vende nada: tudo é presente.

### Nome: três caminhos

1. **Loaf Story** (recomendado). É trocadilho dela mesma, escrito no bilhete da Selena. Qualquer fã reconhece, é curto e funciona como assinatura. O slogan seria a frase do clipe: *a small, free business*.
2. **Small, Free Business.** A própria piada vira o nome. É o mais engraçado, mas soa menos como marca.
3. **Baker's Dozen (13).** A dúzia de padeiro tem 13, o número dela. É o mais sutil, mas só pega quem conhece as duas coisas.

**Sugestão de assinatura:** `Loaf Story` + `a small, free business`. O 13 entra escondido (ver abaixo).

### Linha de produtos

Os produtos vêm todos da pesquisa, nada inventado. Cada um ganha uma etiqueta e uma cor, como as variações da Oliva Club.

| Produto | Etiqueta (em inglês, como as dela) | Cor |
|---|---|---|
| Sourdough tradicional | Original Sourdough! | papel pardo e tinta |
| Mirtilo | Blueberry (the favorite) | azul de mirtilo |
| Mirtilo com limão | Blueberry Lemon | amarelo-limão |
| Espiral de canela | Cinnamon Swirl | canela |
| Funfetti | Funfetti, for the nieces | granulado colorido |
| Cookie de chai | Chai Sugar Cookies · Christmas in September | verde-pinheiro (a fazenda de Natal) |
| Pop-Tart caseira | Homemade Pop-Tarts | laranja com menta (era *Showgirl*) |
| Cookie de sourdough com chocolate | Brown Butter Chocolate Chip | marrom-manteiga |

### Direção visual

- **A marca é um kit de presente, mais que um logo.**
  - Saco de papel pardo dobrado.
  - Adesivo redondo.
  - Etiqueta escrita à mão com o nome de quem recebe.
  - Folha de adesivos de gato.
  - Carimbo de borracha.
- **Logo escrito à mão por você**, com caneta ou pincel, digitalizado. Nada de fonte de "letra à mão": é isso que denuncia IA.
- **O símbolo é o corte do pão:** um ramo de folha desenhado à mão, com **13 talhos** como easter egg. Ele funciona como carimbo no saco, na etiqueta e no avatar.
- **Tipografia de apoio quase nenhuma.** Uma serifada simples ou uma de máquina de escrever, para lista de ingredientes e receita. O resto é letra à mão.
- **Cores-base:**
  - pardo do saco;
  - branco de farinha;
  - marrom de casca;
  - azul de caneta, para a escrita à mão.
  - Os sabores trazem as cores de destaque.
- **A Taylor nunca aparece**, nem o rosto, nem uma versão gerada dela. É fiel ao que aconteceu no Bird Streets, onde só o pão saiu nas fotos, e evita problema de direito de imagem.

### O que você faz à mão (é aqui que entra a alma)

1. O logo "Loaf Story" escrito à mão, em várias tentativas. Fica com a mais viva, não com a mais certinha.
2. As etiquetas de cada produto, com caneta azul em papel de verdade. Fotografe ou escaneie.
3. O desenho do corte com 13 talhos, a lápis ou a caneta.
4. Se der, um carimbo de verdade (borracha ou EVA) batido num saco de pão de padaria.

---

## 3. Fotos para gerar no Space (Magnific)

Regras gerais:
- Só mãos e objetos, nunca pessoas reconhecíveis.
- Peça sempre a etiqueta em branco e coloque a sua etiqueta escrita à mão por cima no Figma, porque a IA estraga o texto.

1. **Capa.** *A rustic sourdough loaf with leaf and floral scoring, dusted with flour, on a wooden kitchen counter at 4 a.m., a single warm lamp, dark quiet kitchen, 35mm film grain, editorial, no people, no text.*
2. **O presente.** *A brown kraft paper bag folded at the top with a blank round sticker and a blank paper tag, a sourdough loaf peeking out, on the passenger seat of a car at night, soft streetlight, film grain, candid, no text.*
3. **O set às 4h.** *Hands of film crew members receiving loaves of sourdough in paper bags on a dark film set before dawn, light stands and cables behind, documentary style, 35mm film grain, no faces, no text.*
4. **A cesta.** *Gift basket with a blueberry lemon sourdough loaf, a lit candle and a linen napkin, a blank handwritten-style card, warm afternoon light, film grain, no text.*
5. **O gato.** *A cat's paw reaching onto a floured kitchen counter next to a cooling loaf, soft morning light, playful, film grain, no text.*
6. **Pop-Tarts.** *Homemade pop tarts with pink strawberry icing and rainbow sprinkles cooling on a wire rack, warm kitchen light, imperfect handmade look, film grain, no text.*
7. **Natal em setembro.** *Chai sugar cookies with cinnamon eggnog icing on a plate beside a small potted Christmas tree, late-summer light through the window, cozy, film grain, no text.*

---

## 4. Roteiro do carrossel

1. **Capa:** "E se a Taylor Swift me contratasse para criar a marca do 'pequeno negócio gratuito' dela?"
2. **O contexto:** ela dá pão para os amigos, com etiqueta escrita à mão e trocadilho, e chamou isso de "small, free business".
3. **A ideia (briefing fictício):** nome, público (os amigos dela), o que ela quer ("que pareça feito em casa, porque é") e o que não quer (cara de confeitaria de luxo).
4. **Logo e corte com 13 talhos**, com anotações à mão, como no slide da Oliva.
5. **O kit:** saco, adesivo, etiqueta e adesivos de gato.
6. **A linha de sabores:** uma etiqueta por produto.
7. **Post 1:** Blueberry, the favorite.
8. **Post 2:** Christmas in September.
9. **Fechamento:** "Projeto de fã. Nada aqui está à venda, nem na vida real."

---

## 5. Cuidados

- Deixe escrito na capa ou no último slide que é **projeto conceitual de fã, sem vínculo** com ela.
- **Sem foto nem rosto gerado dela, sem letra de música e sem logos oficiais dos álbuns.** Trocadilho com título de música pode, porque é o que ela mesma faz.
- Não venda nada com essa marca.

---

## Fontes

- [Taste of Home: Taylor Swift is gifting friends homemade sourdough](https://www.tasteofhome.com/article/taylor-swift-sourdough/)
- [AOL: Taylor Swift gifted her besties homemade sourdough](https://www.aol.com/articles/taylor-swift-gifted-her-besties-184100612.html)
- [Express Tribune: gifts sourdough to Haim sisters and Sombr](https://tribune.com.pk/story/2586538/taylor-swift-gifts-homemade-sourdough-to-haim-sisters-and-sombr-during-la-dinner)
- [AOL: close-up of the sourdough for Selena Gomez](https://www.aol.com/articles/close-taylor-swift-sourdough-selena-140023433.html)
- [AOL: "The Loaf of a Doughgirl" for Jimmy Fallon](https://www.aol.com/articles/taylor-swift-gifts-jimmy-fallon-233254800.html)
- [AOL: Jenny Han's gift](https://www.aol.com/articles/jenny-han-shares-surprising-delicious-233311074.html)
- [KSL: 5 things we learned from New Heights](https://www.ksl.com/article/51360525/5-things-we-learned-from-taylor-swifts-appearance-on-the-new-heights-podcast)
- [The Daily Meal: deep baking obsession with sourdough](https://www.thedailymeal.com/1940177/taylor-swift-baking-obsession-sourdough-bread)
- [Salon: Taylor Swift is in her sourdough era](https://www.salon.com/2025/08/14/taylor-swift-is-in-her-sourdough-era)
- [NBC: Kylie Kelce on Taylor's baking](https://www.nbcmiami.com/entertainment/entertainment-news/kylie-kelce-on-taylor-swifts-baking-skills-thanksgiving-plans/3726082/)
- [CBS Sports: Pop-Tarts for the Chiefs offensive line](https://www.cbssports.com/nfl/news/taylor-swift-made-pop-tarts-for-chiefs-offensive-lineman-who-didnt-share-with-andy-reid)
- [Marie Claire: handwritten note with homemade Pop-Tarts](https://www.marieclaire.com/celebrity/taylor-swift-homemade-pop-tarts-travis-kelce-personal-note)
- [Mental Floss: chai cookies with cinnamon eggnog icing](https://www.mentalfloss.com/posts/taylor-swift-chai-cookie-recipe)
- [Flavour Network: chai cookies and the 1989 Secret Sessions](https://flavournetwork.ca/recipe/taylor-swift-inspired-chai-cookies)
- [Yahoo: she's still baking (2026)](https://www.yahoo.com/entertainment/celebrity/articles/she-still-baking-taylor-swift-195624406.html)
- [Reality Tea: sourdough for the Patient Zero crew](https://www.realitytea.com/2026/10/01/taylor-swift-sourdough-bread-patient-zero-crew-surprise-video/)
- [QNC News: Patient Zero behind-the-scenes cut](https://qncnews.com/taylor-swift-shares-eight-minute-behind-the-scenes-cut-of-patient-zero-video-she-directed/)
- [Rolling Stone: new single "Patient Zero"](https://www.rollingstone.com/music/music-news/taylor-swift-new-single-patient-zero-1235629706/)
- [CNN: Taylor Swift and Travis Kelce tie the knot](https://edition.cnn.com/2026/07/03/entertainment/live-news/taylor-swift-travis-kelce-wedding)
- [Refinery29: the Christmas tree farm](https://www.refinery29.com/en-us/2019/12/8979759/taylor-swift-pine-ridge-christmas-tree-farm-pa)
- [News4JAX: the orange of The Life of a Showgirl](https://www.news4jax.com/entertainment/2025/08/14/taylor-swifts-new-album-has-everyone-seeing-orange-an-exploration-of-the-color/)
