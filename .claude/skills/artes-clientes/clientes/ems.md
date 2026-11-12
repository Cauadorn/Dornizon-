# EMS (@itsemsdesign, Emi)

- **Motor (Design System)**: https://claude.ai/artifact/DNhPwJnJSH9f4gih32oQGa (ler `project/README.md` e `project/conteudo.md` antes de qualquer post).
- **Skill própria**: `marca-ems` (voz, cor, tipografia, grafismos, selo, geração de imagem).
- **Projetos no repositório**: `Emi/ems-so-um-ajustezinho/`, `reel-ems/` (o carrossel pet `Emi/ems-5-direcoes-pet/` está em outra branch).

## Regras fixas

- **Margem de 90px em todos os lados** (Emi, 12/11/2026): texto, @, marca d'água, selo e qualquer elemento de conteúdo ficam a pelo menos 90px da borda (em cima, embaixo, esquerda e direita). Só sangram o fundo, formas grandes cortadas pela borda e o objeto que atravessa o corte do carrossel. No Design System: token `space-4` = 90px. Para conferir: `node Emi/ems-so-um-ajustezinho/projeto/conferir-margens.js <arquivo.html>` (mede cada texto e assinatura das lâminas `.lamina`).

## Aprendizados (o que já custou refação)

Registrado também no Design System (README › "Regras de carrossel"; conteúdo › "Carrossel: regras aprendidas").

- **12/11/2026, "é só um ajustezinho"** (carrossel de 6):
  - **Seguir a linguagem das referências que a Emi manda**, nas cores da EMS, mesmo saindo um pouco do estilo dela: tipografia gigante e apertada (serifa + sans pesada + uma palavra manuscrita), textura de tela por cima de tudo, formas grandes cortadas pela borda, texto em pílulas de cor, objeto em duotone, chamada como objeto. A v5, "com cara de interface" (muito elemento pequeno), foi reprovada como "horrível".
  - **Conectividade é composição contínua, não linha.** Desenhar o carrossel como uma faixa só (6480 × 1350) e cortar depois: em todo corte um objeto ou forma atravessa de verdade, metade de cada lado (a bússola com o centro no corte foi o exemplo da Emi). Cada lâmina pode ter o seu fundo. Fio ou trilha decorativa ligando as lâminas foi reprovado: nunca usar.
  - **Um recurso por lâmina.** O caderno repetido em 3 lâminas foi reprovado. Caderno, janela, bilhete e celular: cada um numa lâmina só.
  - **Referência é repertório, não molde.** Tirar o princípio e traduzir com o vocabulário da EMS; não trazer o objeto da ref. Ref mandada "pra entender" não entra no post.
  - **Grafismos só da EMS** (ícones tingidos na paleta, `SelectionBox`, cursor "emi", `HandleTag`), um ou dois por lâmina, com motivo. Brilho desenhado que não é da marca foi reprovado. "Pode usar mais grafismos, sem exagero."
  - **Matéria agrada:** tecido, letra com falha de impressão, objetos em duotone da paleta ("a bússola tava linda").
  - **Objeto gerado entra reto:** a borracha com 13° de inclinação + rotação no layout ficou "totalmente torta". Medir e nivelar o recorte antes de compor.
  - **Tema:** *blanding* já tem post no feed da EMS.
  - **Fonte diferente só no destaque** (uma palavra). Título inteiro em Poppins 900 e manuscrita espalhada (v6) foram reprovados.
  - **Pouca coisa por lâmina**, na fórmula da lâmina aprovada (fundo com matéria + título com um destaque + um elemento + um apoio). "Socar tudo" foi reprovado.
  - **Fundo forte, conteúdo calmo:** xadrez chamativo + janela colorida foi reprovado; xadrez tom sobre tom + janela monocromática, rosa só no destaque.
  - **Objeto tem que ter motivo:** a borracha jogada no meio do loop saiu; o loop virou o próprio círculo.
