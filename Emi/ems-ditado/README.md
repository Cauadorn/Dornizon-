# EMS · quem vê cara não vê coração (carrossel 8 × 1080 × 1350)

Pedido: "um post assim" a partir do carrossel da @costavictoria__ (ditado + elenco de desenho). Da referência ficou a ideia (um ditado virando história, com um elenco conhecido); nada do Shaun nem da estrutura dela. A Emi recusou: gato/bicho ("meus últimos 4 posts foram de gato"), cena gerada por IA em tudo ("não precisa gerar imagem de tudo") e as capas de natureza-morta ("coisa feia").

**Caminho aprovado para tentar:** colagem editorial (pesquisa no Pinterest em 17/11/2026: recorte em meio-tom com contorno de adesivo, papel rasgado, estrela recortada, tipografia gigante). Elenco: retratos famosos em domínio público, no duotone da marca.

**Status:** v1, esperando aprovação. Finais em `entrega/`.

| Lâmina | Texto | Obra |
| --- | --- | --- |
| 1 | quem vê cara não vê *coração.* | Mona Lisa (Leonardo) |
| 2 | o ditado tá *certo.* e é exatamente esse o problema. | Moça com Brinco de Pérola (Vermeer) |
| 3 | seu produto é bom. seu atendimento, *melhor ainda.* isso é coração. | Autorretrato (Rembrandt) |
| 4 | enquanto isso, a *cara* da sua marca: | O Grito (Munch) |
| 5 | ninguém precisa ler a assinatura pra saber de quem *é.* | Autorretrato (Van Gogh) |
| 6 | marca com cara *própria:* | Autorretrato com chapéu de palha (Vigée Le Brun) |
| 7 | se cobrir o nome, a sua marca ainda tem *cara?* | O Nascimento de Vênus (Botticelli) |
| 8 | o coração é com você. a *cara* é comigo. | O Casal Arnolfini (Van Eyck) |

## Como é feito

- **Obras:** Wikimedia Commons, domínio público (`projeto/obras/`).
- **Peças:** `python3 projeto/colagem.py` recorta (rembg, modelo isnet-general-use; os brutos ficam em `projeto/recortes/`, fora do git), passa para o duotone tinta → plum → lavanda → marfim e gera os papéis rasgados e as estrelas de papel em `projeto/pecas/`. Sem gerador de imagem.
- **Montagem:** `projeto/carrossel.html` + `estilo.css`; `node projeto/render.mjs` (`--saida previa` para testar).
