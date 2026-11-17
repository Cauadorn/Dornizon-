# EMS · quem não tem cão caça com gato (carrossel 8 × 1080 × 1350)

Pedido: "um post assim" a partir do carrossel da @costavictoria__ (`referencias/ref-costavictoria.jpg`), que conta uma história em cima de um ditado ("a grama do vizinho...") com cenas do Shaun, o carneiro. Da referência ficou só a ideia: **um ditado virando história, com um elenco carregando a narrativa**. Nada do Shaun, nada da estrutura dela (a Emi: "não quero copiar").

**Status:** v1, esperando aprovação. Finais em `entrega/` (`lamina-01..08.png`, `visao-geral.jpg`, `legenda.txt`).

| Lâmina | Texto | Cena |
| --- | --- | --- |
| 1 | quem não tem cão caça com *gato.* | o gato na casinha do cachorro, de coleira grande demais |
| 2 | quem não tem marca caça com *template.* | de costas pra bolinha e pro frisbee |
| 3 | e *funciona.* (até certo ponto) | cão de guarda dormindo no telhado |
| 4 | o improviso, na *prática:* | suéter de cachorro sobrando, enrolado na guia |
| 5 | tudo que é emprestado fica *sobrando.* | pequeno numa cama de cachorro enorme |
| 6 | quando a marca é feita pra *você:* | no pedestal, tudo do tamanho dele |
| 7 | a sua marca tá caçando com *o quê?* | retrato, cabeça inclinada |
| 8 | eu faço uma marca do seu *tamanho.* | tocando a campainha do balcão |

## Como é feito

- **Cenas:** foto inteira já no cenário e na paleta (parede e chão roxos, coleira rosa, plaquinha manteiga), geradas pelo gerador do Figma (`gpt-image-2.5-sunburst`, 1024 × 1280) no arquivo "EMS · caça com gato · geração de cenas". Originais em `projeto/origem/`, ampliadas para 1080 × 1350 em `projeto/fotos/`. A cena 6 foi encolhida e a parede continuada pra sobrar espaço pro texto.
- **Montagem:** `projeto/carrossel.html` + `estilo.css`. Instrument Serif + Poppins, uma palavra em itálico por título, cabeçalho fino, estrela em retícula atravessando cada corte, brilhos da marca, grão por cima.
- `node projeto/render.mjs` (use `--saida previa` para testar); `node projeto/conferir-palavra-curta.js projeto/carrossel.html`.

## Pendências

- O gato é gerado e muda um pouco de uma cena pra outra (mancha, cor do olho). Se a Emi quiser um dos gatos dela (Olivia, Bruno ou Marrone), refazer as cenas com foto real de referência.
- Magnific e Higgsfield estavam sem crédito em 17/11/2026; o Canva gera, mas só devolve miniatura pelo conector.
