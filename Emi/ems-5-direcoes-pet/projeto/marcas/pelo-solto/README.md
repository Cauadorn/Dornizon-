# pelo solto · identidade (direção 03, retrô setentinha)

Referências que a Emi escolheu (`referencias/pelo-solto/quadro.jpg`): **2** Haley Sue, **3** Moon Gazer e **principalmente 20**, The Barking Barber.

- **Do 20:**
  - letra de papel recortado com tesoura;
  - cada letra dançando (ângulo, altura e tamanho diferentes);
  - um bicho geométrico ao lado do nome;
  - tinta com grão.
- **Do 3:** as duas palavras em duas cores, a sombra escura deslocada e os brilhos de quatro pontas.
- **Do 2:** a paleta anos 70 (tijolo, mostarda, creme, café e oliva).

## Como é feito

1. `logo-base.html`: a composição em camadas de cor pura (PELO, SOLTO, poodle, brilhos e BANHO & TOSA). A letra é a Ranchers.
   - O poodle é uma silhueta gerada (gpt-image, no Figma) e passada pelo `recorte.py` (`poodle-recorte.png`).
   - Tem de ser fotografada por um servidor http local, porque o `mask-image` com `file://` não carrega.
2. `monta_logo.py base-logo.png saida.png [fundo pelo solto poodle sombra brilho]`:
   - separa as camadas;
   - recorta cada uma "com tesoura" (approxPolyDP: as curvas viram cortes retos);
   - pinta e põe a sombra escura deslocada;
   - aplica o grão de tinta.
3. `recorte.py`: o mesmo efeito de tesoura para qualquer forma.

Arquivos:
- `logo-pelo-solto.png` (creme);
- `prancha-pelo-solto.jpg`, com as variações tijolo e oliva e a paleta.
