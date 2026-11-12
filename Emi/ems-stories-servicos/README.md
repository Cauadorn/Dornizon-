# EMS · stories "toda marca tem fase" (7 × 1080 × 1920)

Sequência de stories da @itsemsdesign no pilar **case e oferta**: um serviço para cada fase da marca. Ponto de partida: stories da @pivocriativo ("te indicando nossos serviços de acordo com a fase do seu negócio"), 12/11/2026. Dela ficou **só a ideia** (indicar o serviço pela fase).

**Status:** v3, esperando aprovação. Finais em `entrega/` (`story-01..07.png` + `visao-geral.jpg`).

## Conceito

Jogo de palavras com **fase**: as fases da lua. Cada story é uma fase, da lua nova (a marca ainda não tem cara) à cheia (pronta pra ser vista de perto). **A lua é foto real** (NASA/GSFC Scientific Visualization Studio, domínio público), tratada na paleta da EMS por `projeto/luas.py` e usada como a cena inteira do story, espelhada porque no hemisfério sul a crescente acende pela esquerda.

| Story | Fase | Estado da marca | Serviço | Composição | Chamada |
| --- | --- | --- | --- | --- | --- |
| 1 | capa | toda marca tem *fase.* | | a lua nascendo por baixo; o "fase." se põe atrás dela | toca pra achar a sua |
| 2 | 01 · nova | a marca ainda não tem cara | identidade *visual* | tudo centrado no disco escuro, entregas nos quatro cantos | quero uma marca |
| 3 | 02 · crescente | tem cara, mas não tem casa | web design *& ux/ui* | título em cima, a crescente subindo por baixo | quero um site |
| 4 | 03 · quarto | tem casa, mas some do feed | social *media* | meia-lua cortada pela borda, frase em tiras à direita | bora conversar? |
| 5 | 04 · gibosa | tem evento, lançamento ou bastidor chegando | story*maker* | a lua dentro da tela de gravação do celular | quero cobertura |
| 6 | 05 · cheia | tá pronta pra ser vista de perto | foto*grafia* | lua cheia em manteiga no foco, título escrito nela | quero fotos |
| 7 | fecho | não sabe em qual *fase* tá? | | as cinco luas em fila + bilhete + selo | dm |

Referências de diagramação (Pinterest, `referencias/pinterest/`): foto inteira com serifa gigante por cima ("falando verdades duras"), texto centrado com rótulos nos cantos ("deixar mais consciente"), frase em tiras ("instagram parece um hobby"), tela de celular ("story chato x story estratégico").

## O que a Emi disse da v2 (12/11/2026)

Gostou da ideia da lua ("achei incrível"), mas: "muitos vetores", "mais do mesmo", "queria mais elementos reais e que seguisse mais as referências que você busca". E: não é copia e cola, não é colagem. Quando viu as luas reais tratadas: "gosto muito das da lua real, tá linda". Não quis cena gerada no Canva.

## O que a Emi reprovou na v1 (12/11/2026)

- "Você tá literalmente copiando": a v1 repetia a estrutura da referência (faixa de pergunta em cima, carimbo de estrela, "te indico" + lista + botão) e a foto da capa imitava a dela. Referência é a ideia, nunca a estrutura.
- Faltou pesquisar diagramação no Pinterest antes de desenhar (folhas em `referencias/pinterest/`).
- Faltaram serviços: ela também é **fotógrafa e storymaker**.
- Nada do que ela ensinou aparecia: todos os stories iguais, sem tipografia gigante, sem matéria, sem composição própria.

## Pendências

- Texto escrito a partir do design system; conferir as entregas de cada serviço com a Emi.
- Produtos personalizados ficou de fora.
- Os botões são desenho: no Instagram, colar o adesivo de link por cima.

`node projeto/render.mjs` (use `--guia` para ver a área segura: 250px em cima e embaixo, 90px nos lados).
