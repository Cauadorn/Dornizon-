# EMS · how to trap me (carrossel 9 × 1080 × 1350)

Trend do Instagram "how to trap me" (referências da Emi: @leticiasmalheiro e @designtroia, prints em `referencias/`): a caixa armada com o graveto e, embaixo, o que prende a pessoa. Uma isca por lâmina; a última é a caixa vazia com a pergunta pra quem segue.

**Status:** v1 decorada, esperando aprovação. Finais em `entrega/` (`lamina-01..09.png`, `visao-geral.jpg`, `legenda.txt`).

| Lâmina | Isca | Fundo |
| --- | --- | --- |
| 1 | gatos | violeta |
| 2 | música: Taylor Swift, Olivia Rodrigo, Sabrina Carpenter, Olivia Dean e Avenged Sevenfold | plum |
| 3 | séries: Gossip Girl, Gilmore Girls, American Horror Story | violeta-2 |
| 4 | massas | ameixa |
| 5 | câmeras | violeta |
| 6 | doces | plum |
| 7 | livros | violeta-2 |
| 8 | ferramentas de design | ameixa |
| 9 | caixa vazia: "how to trap *you?*" | violeta |

## Como é feito

- **Caixa:** uma foto só, gerada no Magnific (Nano Banana Pro 2K, Space "EMS · how to trap me · carrossel da trend") já na paleta: caixa lilás, graveto rosa, barbante marfim. Recortada em duas camadas: `fotos/caixa.png` (adesivo com contorno marfim e sombra dura) e `fotos/frente.png` (tampa, lateral, graveto e barbante, que passam por cima das iscas). As faces ganham estampa presa em perspectiva (`face()` em `carrossel.html`).
- **Iscas:** recortes em `recortes/`, posicionados em `iscas.js`. Objetos gerados em folhas sobre fundo #E9E9E9 (`folhas/`) e separados por `recortar.py`; gatos, massas, câmeras e donut reais, capas de álbum e pôsteres vêm do Pinterest (`referencias/fontes-pinterest.txt`).
- **Fundo:** estrela em retícula grande, papel com fibra e grão; a cor muda a cada lâmina.

`node projeto/render.mjs` (use `--saida previa` para testar).

## O que a Emi pediu (15/11/2026)

- Sem nome das coisas escrito na lâmina; sem contagem de lâminas; **sem o selo** ("tira esse selo").
- Iscas como imagens recortadas, igual às referências, em pilha cheia. Gatos e massas com poucas peças geradas foram reprovados.
- Capas e pôsteres: pesquisar no Pinterest pelo nome, sem pedir pra ela mandar.
- Visual decorado como o das referências: fundo trabalhado, caixa que não pareça papelão cru, nada de grafismo solto sem motivo (o "xoxo" saiu).

## Pendências

- Aprovação do visual decorado (estampa da caixa, cor da lateral, título em adesivo).
- Gato branco da folha gerada ficou de fora (recorte ruim em fundo claro).
- Capas, pôsteres e fotos do Pinterest são de terceiros: conferir se a Emi quer manter todos.
