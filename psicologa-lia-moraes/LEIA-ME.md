# Lia Moraes, psicóloga (case conceitual de identidade + social media)

Projeto conceitual de portfólio: cliente fictícia. Imagens geradas com IA (Nano Banana / GPT Image no Figma). Arquivo do Figma: "vírgula · psicóloga (case conceitual)".

## Etapas
1. **Pesquisa**: Pinterest (identidades de psicólogas, feeds, posts, logos com letra desenhada) + 5 refs enviadas pelo Cauã (`referencias/pinterest-cliente/`).
2. **Logo (aprovado)**: monograma **lm** com laço fino atravessando o "l", vetorizado de um esboço gerado (`projeto/logo/geracoes/1a-monograma-gpt.png`) + "Lia Moraes" em Playfair Display 400 + "PSICÓLOGA" em Jost 300 espaçada (0,7 em). Centralização ótica (70% centro de massa, 30% caixa).
   - Arquivos finais em `projeto/logo/final/` (vertical, horizontal, monograma, perfil; creme, cobalto, pêssego).
   - Regerar: `python3 -I projeto/logo/vetorizar.py ...` (monograma) e `python3 -I projeto/logo/logo_final.py` (lockups).
3. **Paleta**: cobalto #2742C2, pêssego #F3C6A8, creme #F5EEE3, tinta #1C1D3A (aprovada).
4. **Mockups (aprovados)**: cartão (frente cobalto com o logo, verso pêssego com dados), canecas e calendário de mesa.
   Cenas em branco geradas no Nano Banana (`projeto/ia/mockups/base-*.png`), artes planas em `projeto/mockups/artes-modelo.html`,
   aplicadas com perspectiva/curvatura e a luz da foto, enquadradas no centro em 1080x1350.
   - Regerar: `cd projeto/mockups && python3 -I artes.py && node ../ferramentas/artes.cjs artes.html artes && python3 -I compor.py`
   - Regras que o Cauã pediu: tudo reto e centralizado (objetos alinhados ao quadro, conteúdo das artes no eixo).
5. **Carrossel da cliente (aprovado)**: `projeto/posts/carrossel-v3.html` → `carrossel-v3/s1..s8.png`. Fotos do Pinterest, Instrument Serif, blocos de texto colados.
6. **6 posts** em `projeto/posts/posts-v5.html` → `posts-v5/p1..p6.png` (`node projeto/ferramentas/artes.cjs projeto/posts/posts-v5.html projeto/posts/posts-v5`).
   - Aprovados: p2 bilhete, p3 telefone ("desmoronar"), p4 chá de pausa, p6 etiquetas ("engolir o choro").
   - p1 e p5 (refeitos com as refs de `referencias/pinterest-cliente-3/`): fotos da Lia geradas no Canva com o rosto de referência,
     tratadas com `projeto/ia/filme.py` (menos laranja, fundo mais neutro que a pessoa, pretos levantados, grão) e riscos de filme
     (`projeto/texturas/riscos.py`). p1: "Lia" gigante em Playfair Display 900 com a cabeça na frente (recorte rembg), bilhete
     recortado cobalto, selo girando com o monograma, texto vertical. p5: rascunhos riscados do que dizer, título em Fraunces com
     contorno de adesivo pêssego (filtro SVG `#adesivo`), balão de fala terracota.
7. Próximo: feed (grade do perfil com destaques, menos azul) e o carrossel do case.

## Descartado (não usar)
- Prancha de identidade em formato de "documentação" (caixinhas, rótulos, o laço em volta da palavra, a bolinha com legenda): reprovada.
- Aviso de porta (mockup).
- Conceito "vírgula" como nome da marca (a cliente usa o próprio nome).
- p1/p5 com título centralizado sobre a foto laranja crua (`ia/lia-p1.jpg`, `ia/lia-p5.jpg`): "cara de ChatGPT".
- Modelo de banco de imagem no lugar da Lia (a Lia é sempre o rosto de `ia/lia-retrato-v1.png`).
- Logos só com fonte digitada ("lia moraes," em 4 fontes; "lia," desenhado): reprovados.
