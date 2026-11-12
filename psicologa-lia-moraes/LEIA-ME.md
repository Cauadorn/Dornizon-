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
5. Próximo: carrossel da cliente, 6 posts, feed e o carrossel do case.

## Descartado (não usar)
- Prancha de identidade em formato de "documentação" (caixinhas, rótulos, o laço em volta da palavra, a bolinha com legenda): reprovada.
- Aviso de porta (mockup).
- Conceito "vírgula" como nome da marca (a cliente usa o próprio nome).
- Logos só com fonte digitada ("lia moraes," em 4 fontes; "lia," desenhado): reprovados.
