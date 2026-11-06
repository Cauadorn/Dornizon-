# Avatar IA + ebook no Instagram

Plano para criar um perfil com personagem de IA no Instagram e vender um ebook, no modelo do fio do
@Luvidonviski (107 posts em menos de 30 dias, números dele, não conferidos). Vídeo só no **Google Flow**
(ElevenLabs fora). Pesquisa de 6/11/2026.

## Nicho

**Emagrecimento**, o nicho saturado mais forte do Brasil, com o ângulo do momento: **comida para quem está
emagrecendo, inclusive com caneta**.

- Saúde e emagrecimento aparece entre os nichos que mais vendem na Hotmart. Finanças disputa o primeiro
  lugar, mas não há ranking oficial recente.
- 2026 é o ano das canetas: a patente da semaglutida caiu em 20/3, a Anvisa aprovou os primeiros genéricos
  em agosto e a projeção é o mercado ir de R$ 11 bi (2025) para R$ 20 bi (2026). É muita gente nova
  procurando o que comer.
- Receita é o conteúdo que mais se salva e compartilha, e o algoritmo distribui por salvamento, envio e
  tempo assistido.
- Ebook de receitas é o produto de entrada clássico (R$ 19 a 37), compra por impulso a partir de um Reel.

Plano B, com o mesmo passo a passo: **finanças pessoais** (organizar o salário e sair das dívidas).

## Arquivos

| Arquivo | O que é |
|---|---|
| [`personagem.md`](personagem.md) | ficha da Bia: aparência, cozinha, voz, bordões, marca, bio do Instagram |
| [`prompts-flow.md`](prompts-flow.md) | prompts de imagem e vídeo do Flow, na ordem, e a montagem no CapCut |
| [`ebook/ebook.md`](ebook/ebook.md) | texto completo do ebook *Prato Pequeno, Proteína Grande* (40 receitas) |
| [`ebook/receitas.py`](ebook/receitas.py) | fonte das receitas; recalcula proteína e kcal e gera o `ebook.md` |

## Personagem (rascunho)

- Mulher de uns 35 anos, cozinha prática, "receitas proteicas em 15 minutos". Uma amiga que cozinha
  bem, **não** uma nutricionista e **não** alguém que diz ter emagrecido.
- Nome curto e comum. Duas marcas fixas fáceis de repetir (ex.: avental de uma cor, pulseira).
- Cenário fixo: a cozinha dela, sempre a mesma.

## Ebook (rascunho)

- 40 receitas proteicas em porção pequena: café, almoço, lanche, jantar e doce. Proteína e tempo de preparo
  em cada uma, lista de compras no fim.
- Preço R$ 27 (âncora R$ 47). Order bump de R$ 9,90: planner semanal e lista de compras.
- Ideal: revisão de um(a) nutricionista com o nome e o CRN no ebook. Para uma personagem de IA, é o que
  mais dá confiança.
- Conta: com taxa de ~R$ 5 por venda de R$ 27, fazer R$ 1,7 mil (o resultado do fio) são ~80 vendas.

## Ferramentas e custo

| Ferramenta | Para quê | Custo (conferir na hora) |
|---|---|---|
| Google AI Pro (Flow) | vídeos com Veo 3.1 e imagens com Nano Banana | ~R$ 97/mês, 1.000 créditos |
| ChatGPT | imagens (como no fio) | grátis pra começar |
| CapCut | juntar clipes, legenda automática, música | grátis |
| Kiwify ou Cakto | checkout e entrega do PDF | sem mensalidade, taxa por venda |
| ManyChat | "comenta RECEITA" → link no direct | grátis no começo |
| Canva ou Figma | diagramar o ebook | já tem |

**Créditos do Flow:** Veo 3.1 Lite ~10 por clipe, Fast ~20, Quality ~100. Sem assinatura, o Google dá
50 créditos por dia (uns 5 clipes Lite) e dá pra testar de graça antes de assinar. O Pro rende uns 100
clipes Lite ou 50 Fast por mês, então **cada Reel usa no máximo 1 ou 2 clipes de vídeo** e o resto é
imagem com movimento no CapCut. O Ultra (a partir de ~R$ 780) só quando o perfil já estiver vendendo.

## Passo a passo

### Dia 1: contas

1. Criar um **Gmail novo** só para o projeto. Ele vai em tudo: Instagram, Flow, checkout, ManyChat.
2. Entrar em **labs.google/flow** com esse Gmail e testar com os 50 créditos grátis do dia. Se funcionar
   (principalmente a fala em português), assinar o **Google AI Pro**.
3. **Instagram, no celular:** Perfil → trocar de conta → Adicionar conta → Criar nova, com o Gmail novo.
   - Nome de usuário com o nome e o nicho (ex.: `@nome.receitasleves`).
   - Campo "Nome" com palavra-chave, porque ele entra na busca (ex.: `Nome | Receitas proteicas`).
   - Configurações → Tipo de conta e ferramentas → **Mudar para conta profissional** → Criador de
     conteúdo → categoria **Criador digital**.
   - Se aparecer a opção de **rótulo de perfil gerado por IA**, ligar. Há relatos de que o Instagram corta
     o alcance de perfis de personagem de IA sem rótulo.
4. Criar a conta na **Kiwify ou Cakto** (CPF e conta bancária). O produto entra no dia 6.
5. Instalar o **CapCut**.
6. Usar a conta nova como gente normal por 1 ou 2 dias: seguir uns 30 perfis do nicho, assistir Reels,
   curtir, comentar.

### Dias 2 e 3: a personagem no Flow

1. Fechar a ficha: idade, rosto, cabelo, roupa fixa, marcas, jeito de falar, bordões.
2. Gerar o **rosto oficial** (Nano Banana no Flow ou ChatGPT). Gerar várias opções e escolher uma.
3. Com o rosto oficial como referência, gerar a **ficha**: frente, 3/4, perfil e corpo inteiro com a
   mesma roupa. Gerar também a **cozinha** dela, vazia.
4. Salvar rosto, ficha e cozinha como **Ingredientes** no Flow. O Veo 3.1 aceita até 3 referências.
5. Teste de voz: gerar 3 clipes de 8s com a mesma descrição de voz e ver se ela soa como a mesma pessoa
   e se a boca acompanha o português. Se a voz variar demais, ela fica muda na maioria dos vídeos e o
   texto entra na tela ou numa narração do CapCut.

Modelo de prompt (Ingredients to Video, 9:16):

```
Vertical 9:16, 8 segundos. A mulher da referência, na cozinha da referência.
Ela olha para a câmera segurando [objeto] e diz, em português do Brasil, com voz feminina
calorosa, sotaque paulista e ritmo rápido: "[fala de até 8 segundos]".
Câmera de celular na mão, movimento leve, luz natural de janela.
Sem texto na tela, sem legenda, sem música.
```

Texto, legenda e música entram no CapCut. A IA escreve errado na tela.

### Dias 3 a 7: ebook e checkout

1. Eu escrevo o conteúdo (receitas, introdução, avisos). Você diagrama em Canva ou Figma e exporta o PDF.
2. Capa e mockup do ebook para usar nos posts e nos stories.
3. Na Kiwify/Cakto: criar o produto, subir o PDF, preço R$ 27, order bump R$ 9,90. Fazer uma compra de
   teste.
4. Link do checkout na bio.

### Dia 4 em diante: postar

Meta: **2 a 3 Reels por dia + stories todo dia**, no mesmo horário. O fio fez ~3,5 por dia.

Formatos:

| Formato | Como | Créditos |
|---|---|---|
| Receita em 20s | 1 clipe dela falando o gancho + 4 ou 5 imagens dos passos com zoom no CapCut | 1 clipe |
| Fala pra câmera | 1 ou 2 clipes: "3 erros de quem...", "o que eu comeria se..." | 1 ou 2 clipes |
| Carrossel | "5 lanches com mais de 20 g de proteína", só imagens | 0 |
| Story | enquete, caixinha, mockup do ebook com link | 0 |

Cada Reel: gancho escrito na tela no 1º segundo, 15 a 30s, CTA no fim ("salva" ou "comenta RECEITA").
Fixar no perfil os 3 melhores posts.

### Quando os comentários começarem: ManyChat

Conectar o Instagram ao ManyChat e criar a automação: comentou a palavra → recebe no direct o link do
ebook (e uma receita grátis, se quiser). Começar no plano grátis e passar pro pago quando lotar.

### Toda semana: medir

Por Reel: visualizações, salvamentos, envios, seguidores ganhos. Por semana: cliques no link e vendas.
Repetir o formato e o tema que mais salvou. Testar ganchos novos nos **Trial Reels** quando o Instagram
liberar pra conta.

## Regras

1. Rótulo de IA no perfil e em todo post. A bio diz que é uma personagem criada com IA.
2. Ela **nunca** diz que usa caneta nem que emagreceu. Sem antes e depois.
3. Nada sobre o remédio: dose, marca, onde comprar, como aplicar. Ela fala de comida.
4. Ela não é nutricionista e não se apresenta como profissional de saúde.
5. O ebook é de **receitas**, não dieta nem cardápio prescrito. Leva o aviso de que não substitui
   acompanhamento profissional.
6. Não prometer quilos nem prazo.

## Fontes

- Nichos: [Sellfy](https://sellfy.com/blog/instagram-niches/), [Creator Lane](https://creatorlanehq.com/blog/faceless-ai-creator-playbook-2026),
  [Accio (Hotmart 2026)](https://pt.accio.com/business/hotmart-best-selling-courses), [Loja Integrada](https://lojaintegrada.com.br/hub/infoprodutos-mais-vendidos-estrategias/)
- Canetas: [Poder360](https://www.poder360.com.br/poder-saude/canetas-emagrecedoras-quais-sao-as-novas-opcoes-no-brasil/),
  [Mercado&Consumo](https://mercadoeconsumo.com.br/25/08/2026/economia/anvisa-aprova-segundo-generico-de-semaglutida-em-caneta-injetavel/),
  [ICTQ](https://ictq.com.br/varejo-farmaceutico/4822-mercado-de-canetas-emagrecedoras-pode-atingir-r-20-bilhoes-no-brasil-com-chegada-de-genericos-em-2026)
- Flow e Veo: [Google: créditos do Flow](https://support.google.com/flow/answer/16526234),
  [Google: Ingredients to Video](https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/),
  [IA do Brasil (preços em R$)](https://iadobrasil.com/google-flow-o-que-e-preco-como-usar/), [CostGoat](https://costgoat.com/pricing/google-flow)
- Rótulo de IA: [Let's Data Science](https://letsdatascience.com/news/instagram-demotes-unlabeled-ai-influencer-accounts-0cbd924b),
  [BetaNews](https://betanews.com/article/meta-will-limit-the-reach-of-ai-profiles-on-instagram-that-are-not-transparent/)
- Checkout: [Vini Ensina](https://viniensina.com.br/?p=4267)
- ManyChat: [eesel](https://www.eesel.ai/pt/blog/precos-manychat), [Chatarmin](https://chatarmin.com/en/blog/manychat-pricing)
- Trial Reels: [Publer](https://publer.com/blog/instagram-trial-reels-guide/)

Preços e taxas vêm de blogs e mudam. Conferir no site oficial antes de pagar.
