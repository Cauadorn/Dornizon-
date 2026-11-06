# Prompts do Flow

Ordem: imagens 1 a 5 (Nano Banana no Flow ou ChatGPT), depois o teste de voz (6), depois os modelos de
vídeo (7). Ficha completa da personagem em [`personagem.md`](personagem.md).

Regras para todos:

- Sempre anexar o **rosto oficial** como referência, e a ficha quando for corpo inteiro.
- Testar no **Veo 3.1 Lite** (~10 créditos). Só passar pro Fast (~20) o take que já está bom.
- Vídeo sempre **9:16**. Nada de texto na tela: legenda, título e música entram no CapCut.
- Gerar 2 a 4 variações e escolher. Não aceitar clipe com rosto diferente, mão deformada ou objeto
  mudando de lugar.

## 1. Rosto oficial

Gerar umas 8 opções, escolher uma e salvar como `rosto-oficial`.

```
Foto de celular, retrato do peito pra cima, de uma mulher brasileira de 36 anos, pele morena clara com
subtom quente e textura real de pele (poros visíveis, sem filtro de beleza), cabelo castanho-escuro liso
com leve onda preso num coque baixo com uma piranha de cabelo cor caramelo, alguns fios soltos na frente,
rosto oval, maçãs do rosto marcadas, sobrancelhas naturais, olhos castanhos, sorriso largo e simpático.
Veste camiseta básica off-white e avental verde-sálvia de alça cruzada. Fundo: cozinha clara desfocada.
Luz natural de janela vindo da esquerda. Aparência de pessoa comum, não de modelo. Fotorrealista.
```

## 2. Ficha de referência

Com o rosto oficial anexado. Salvar como `ficha`.

```
Folha de referência de personagem da mulher da imagem anexada, mantendo o rosto exatamente igual.
Fundo cinza claro liso, quatro vistas lado a lado na mesma altura: de frente, três quartos, perfil e
corpo inteiro de frente. Mesma roupa em todas: camiseta básica off-white, avental verde-sálvia de alça
cruzada, calça jeans, tênis branco. Cabelo preso em coque baixo com piranha caramelo. Corpo comum,
estatura média. Luz de estúdio suave e uniforme. Fotorrealista, sem texto.
```

## 3. A cozinha (sem ninguém)

Salvar como `cozinha`. Gerar também uma versão vista de cima da bancada (troque a primeira linha por
"Vista de cima, a 90 graus, da bancada").

```
Cozinha de apartamento brasileiro pequena e clara, vista de frente para a bancada, na altura dos olhos.
Bancada de quartzo branco, azulejo de metrô branco, armários de madeira clara, janela à esquerda com
vasinhos de manjericão e cebolinha, luz natural de manhã entrando pela janela. Sobre a bancada: tábua de
madeira, pote de vidro com aveia e fruteira com bananas. Sem pessoas. Fotorrealista, foto de celular.
```

## 4. Cena base (ela na cozinha)

Com `rosto-oficial` + `cozinha`. É o quadro inicial dos vídeos de fala.

```
A mulher da primeira imagem, com o rosto exatamente igual, em pé atrás da bancada da cozinha da segunda
imagem, olhando para a câmera e sorrindo. Enquadramento vertical 9:16 da cintura pra cima, câmera na
altura dos olhos, como se o celular estivesse apoiado na bancada. Camiseta off-white, avental
verde-sálvia, cabelo preso com piranha caramelo. Luz natural da janela à esquerda. Fotorrealista.
```

## 5. Foto de perfil

```
Close do rosto da mulher da imagem anexada, rosto exatamente igual, sorrindo para a câmera, cabeça e
ombros, avental verde-sálvia aparecendo, cozinha clara bem desfocada atrás, luz natural suave. Formato
quadrado, rosto centralizado com espaço em volta para o recorte redondo do Instagram.
```

## 6. Teste de voz (Veo 3.1, Ingredients to Video)

Ingredientes: `rosto-oficial`, `ficha`, `cozinha`. Gerar os 3 com a **mesma** descrição de voz e comparar:
parece a mesma pessoa? A boca acompanha o português?

```
Vertical 9:16, 8 segundos. A mulher das referências, rosto exatamente igual, atrás da bancada da cozinha
da referência, avental verde-sálvia e piranha caramelo no cabelo. Ela olha para a câmera e diz, em
português do Brasil, com voz feminina adulta, por volta de 35 anos, timbre médio e caloroso, sotaque
paulista leve, fala animada e um pouco rápida, sorrindo enquanto fala:
"[FALA]"
Câmera de celular parada, apoiada na bancada. Luz natural de janela à esquerda. Som ambiente baixo de
cozinha. Sem texto na tela, sem legenda, sem música.
```

Falas do teste:

1. `Oi, eu sou a Bia. Aqui é receita com muita proteína em porção pequena. Bora?`
2. `Isso aqui tem vinte e dois gramas de proteína e fica pronto em quatro minutos.`
3. `Salva esse vídeo, porque amanhã você vai querer fazer de novo.`

Escreva números por extenso na fala ("vinte e dois gramas"): o Veo lê melhor.

**Se a voz mudar muito entre os 3:** a Bia passa a falar só no gancho (1 clipe por Reel) e o resto do
vídeo é sem fala, com texto na tela. Se nem o gancho ficar bom, ela fica muda e o texto conta tudo.

## 7. Modelos de vídeo

Todos com os mesmos ingredientes do teste e o mesmo bloco de voz quando houver fala.

### A. Gancho falando pra câmera (abre o Reel)

```
Vertical 9:16, 8 segundos. A mulher das referências, rosto exatamente igual, atrás da bancada da cozinha
da referência, segurando [INGREDIENTE OU PRATO] na altura do peito. Ela olha para a câmera e diz, em
português do Brasil, com [BLOCO DE VOZ]: "[GANCHO DE ATÉ 20 PALAVRAS]"
Câmera de celular parada. Luz natural de janela à esquerda. Sem texto na tela, sem legenda, sem música.
```

### B. Mostrando o prato pronto (fecha o Reel)

```
Vertical 9:16, 8 segundos. A mulher das referências, rosto exatamente igual, na cozinha da referência,
aproxima da câmera um prato com [PRATO], inclina o prato para mostrar, sorri e faz sinal de positivo com
a outra mão. Boca fechada, sem falar. Câmera de celular na mão, leve movimento. Luz natural. Som ambiente
baixo. Sem texto na tela, sem música.
```

### C. Mãos na massa, vista de cima (sem rosto, sem fala)

O mais barato de acertar: não tem rosto pra errar.

```
Vertical 9:16, 8 segundos, vista de cima a 90 graus da bancada de quartzo branco da referência. Mãos de
mulher de pele morena clara, com a ponta do avental verde-sálvia aparecendo, [AÇÃO: batendo ovos num
bowl de vidro / picando tomate na tábua de madeira / despejando a massa na frigideira]. Movimentos
naturais, ritmo real. Luz natural de janela. Som real da ação. Sem texto na tela, sem música.
```

### D. Reação provando (usar pouco)

A IA erra comida entrando na boca. Gerar várias e só usar se ficar natural.

```
Vertical 9:16, 6 segundos. A mulher das referências, rosto exatamente igual, na cozinha da referência,
pega um pedaço de [PRATO] com o garfo, prova, fecha os olhos por um instante e faz cara de aprovação,
balançando a cabeça. Boca fechada depois de mastigar, sem falar. Câmera parada. Luz natural. Sem texto.
```

## 8. Imagens dos passos (carrossel e miolo do Reel)

Custam menos que vídeo. No CapCut, cada imagem ganha um zoom lento de 2 a 3 segundos.

```
Foto de cima a 90 graus, bancada de quartzo branco da referência, luz natural de janela. [PASSO: ex.
"bowl de vidro com 2 ovos batidos e cottage, garfo ao lado"]. Mãos de mulher de pele morena clara com
avental verde-sálvia entrando pelo canto. Estilo foto de celular, cores naturais, sem texto.
```

Prato final (capa do Reel e do carrossel):

```
Foto de [PRATO] num prato de cerâmica creme, sobre a bancada de quartzo branco, ângulo de 45 graus, luz
natural de janela vindo da esquerda, garfo ao lado, fundo da cozinha desfocado. Porção pequena e bem
servida, comida de verdade, sem exagero de brilho. Fotorrealista, sem texto.
```

## Montagem de um Reel de receita (CapCut)

1. Clipe A (gancho, 8s) → 4 ou 5 imagens dos passos (2 a 3s cada, com zoom) ou clipes C → clipe B (prato).
2. Texto na tela no 1º segundo com o gancho escrito.
3. Legenda automática em português, revisada.
4. Ingredientes e quantidades em texto sobre as imagens dos passos.
5. Final: "Receita completa + 39 outras no ebook. Link na bio." ou "Comenta RECEITA".
6. Música: escolher no próprio Instagram na hora de postar, volume baixo sob a fala.
7. Exportar 1080 × 1920.
