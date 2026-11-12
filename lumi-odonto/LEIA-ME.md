# Lumi Odonto: identidade visual (projeto conceitual)

Marca inventada para o carrossel de portfólio no formato "E se uma clínica odontológica me contratasse para criar seus posts?". Referência do formato: post de 07/11/2026 da @rafaelalimadesigner_ (pet shop "Mundo Pet"). A Lumi não existe e não tem relação com nenhuma clínica real.

## Conceito

**Lumi** vem de lúmen (luz). A ideia é uma clínica que parece casa e não hospital: calma, clara e sem medo.

O símbolo é um arco com um sol nascendo dentro, e tem três leituras:

- **A arcada:** o arco repete o desenho dos dentes.
- **A porta:** uma porta aberta, de uma clínica que recebe em vez de assustar.
- **A luz:** o sol pêssego. O mesmo pêssego vira o pingo do i em "lumi".

Slogan: *odontologia que acolhe*.

## Briefing fictício (texto do slide "A ideia")

**Sobre a marca**
- Nome: Lumi Odonto.
- Segmento: clínica odontológica (clínico geral, clareamento, alinhadores e implantes).
- Público: adultos de 25 a 45 anos que adiam o dentista por medo ou falta de tempo.

**O que estou procurando**
Quero uma identidade que tire a cara de consultório frio. Ela precisa passar calma, confiança e modernidade, sem parecer spa nem clínica de estética.

**Estilo**
- Limpo, com bastante respiro.
- Fotos reais com luz natural.
- Nada de dente 3D nem de "sorriso de banco de imagem".

**Cores**
Verde-sálvia, areia e um toque de pêssego. Não quero azul nem branco puro.

**Tipografia**
Uma serifada elegante para os títulos e uma sem serifa fácil de ler para os textos.

## Sistema

| Cor | Hex | Uso |
|---|---|---|
| Areia | `#EDE6DA` | fundo principal |
| Leite | `#F8F5EF` | fundo de respiro e cards |
| Sálvia | `#9BB5A0` | cor da marca, em áreas grandes |
| Folha | `#4F6F5C` | logo, títulos e botões |
| Grafite | `#2E2E2E` | texto |
| Pêssego | `#F2B8A0` | a luz: só detalhes, nunca texto |

- **Contraste:**
  - Grafite sobre areia dá 11:1.
  - Leite sobre folha dá 5,1:1.
  - Sobre sálvia, o texto é sempre grafite, porque leite sobre sálvia dá só 2:1.
- **Fontes:** Instrument Serif nos títulos (o itálico em folha marca a palavra que importa, uma por título) e Manrope nos textos e rótulos. As duas são gratuitas e estão em `_fontes/`.
- **Grafismos:**
  - Moldura em arco para as fotos.
  - Sol nascendo (meio círculo pêssego saindo da borda, com anéis finos).
  - Pílulas de cantos redondos ("Dica Lumi", "Mito / Verdade").
  - Ponto pêssego como marcador.
- **Foto:**
  - Luz de janela, tons quentes, pele real, sorriso no meio da conversa.
  - Evitar azul gelado e luz de hospital.
- **Voz:**
  - Clara, calma e sem jargão. Explica antes de vender.
  - Evitar "sorriso perfeito", "procedimentos de excelência" e "agende já!!!".

## Arquivos

| Pasta | O que tem |
|---|---|
| `01-marca/svg/` | Logo em curvas (não depende de fonte). Versões horizontal, vertical, nome e símbolo, cada uma em `cor`, `negativo` (para fundo folha), `grafite` e `branco`. Tem também o `lumi-avatar.svg` para a foto de perfil. |
| `01-marca/png/` | Os mesmos logos em PNG com fundo transparente (4x), prontos para o Canva ou Figma. |
| `02-identidade/identidade.html` | As 7 pranchas da identidade (1080 x 1350). |
| `02-identidade/png/` | As pranchas em PNG: capa, símbolo, versões, cores, tipografia, grafismos, foto e voz. |
| `_fontes/` | Instrument Serif e Manrope (licença OFL). |
| `_ferramentas/` | Scripts que geram os arquivos. Não precisa abrir. |

Para gerar tudo de novo:

```
python3 lumi-odonto/_ferramentas/marca.py        # logos SVG (precisa de: pip install fonttools)
node lumi-odonto/_ferramentas/logos_png.js       # logos PNG
node lumi-odonto/_ferramentas/render.js          # pranchas PNG
```

## Próximo passo: os 6 posts do grid

A ideia é alternar post com foto e post de marca, como no carrossel de referência.

1. **Foto:** "Cuidar do sorriso *não precisa* assustar." Paciente sorrindo em moldura de arco.
2. **Marca:** logo sobre sálvia, com o sol nascendo.
3. **Mito ou verdade:** "Clareamento enfraquece os dentes?"
4. **Dica Lumi:** "3 sinais de que está na hora de voltar ao dentista."
5. **Marca:** frase "Seu sorriso, *sob uma luz melhor*."
6. **Foto:** "Aqui a primeira consulta *começa com uma conversa*." com o botão "Agende sua avaliação".

Faltam as fotos, que podem ser geradas no Magnific como nos carrosséis do Dr. Pedro. Falta também a moldura do carrossel de portfólio (capa, "A ideia" e "O resultado"), que leva a marca do designer, não a da Lumi.
