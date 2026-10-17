# Duda — personagem de IA para o TikTok Shop

Persona feminina gerada por IA para vídeos de achadinhos no TikTok Shop (todos os nichos).

## Quem é

- **Duda**, 22 anos, paulistana, descontraída, fala rápido, a amiga que sempre acha a coisa boa.
- Pele morena bronzeada, cabelo longo cacheado castanho-escuro (3B), olhos castanhos amendoados,
  sobrancelha cheia, covinhas. **Marcas registradas:** pinta na bochecha e argolinhas douradas.

## Referências (`referencias/`)

| Arquivo | Uso |
|---|---|
| `rosto-oficial.jpg` | identidade do rosto — sempre como primeira referência |
| `ficha-referencia.jpg` | frente, 3/4, perfil e close com a mesma roupa |
| `cena-conjunto-lot.jpg` | cena de abertura do vídeo do conjunto LOT |

Em qualquer ferramenta (Freepik Spaces, Gemini, ElevenLabs), suba o rosto oficial + a ficha e peça
para **manter a identidade exatamente igual**.

## Voz

- ElevenLabs, voz salva como **"Duda - TikTok Shop"** (`OFOPGZVavWeQGlN54pSl`).
- Gerar com `eleven_v3` e tags de expressão: `[excited]`, `[laughs]`, `[sighs]`, mais "gente", "tipo", "meu".
- Ela lê "LOT" como "Lote": evite marcas com sigla na fala ou escreva como se pronuncia.

## Fluxo e custos

O ElevenLabs usa créditos da agência (300 mil). Regra combinada:

| Etapa | Onde | Custo aproximado |
|---|---|---|
| Fala/narração (~20s) | ElevenLabs | ~280 créditos |
| Imagens da Duda com o produto | Freepik Spaces no navegador (ilimitado no plano) | 0 |
| Vídeo: 2 clipes de 10s, Kling 2.5 Turbo, 9:16 | ElevenLabs | ~8,5 mil créditos |
| Montagem (clipes + narração) | ffmpeg local | 0 |

**Formato que funciona:** a Duda **não fala** no vídeo. Ela mostra a roupa (frente e lado, boca fechada,
sorrindo) e a narração entra por cima. Lip-sync (OmniHuman 1.5, ~18,5 mil créditos por 19s) deformou o
rosto e foi descartado. Seedance 2.5 de 20s custaria ~56 mil — não usar.

Não mostrar as costas de um produto sem ter a foto real das costas: a IA inventa o modelo.
Sempre pedir orçamento (`estimate_only`) antes de gerar vídeo **e imagem** — imagem com 4 referências
no Nano Banana Pro custa ~3,6 mil créditos cada.

### Receita que funciona (~9 mil créditos por vídeo)

1. **Imagens no Freepik Spaces, gerado por uma pessoa no site/app** (0 créditos, confirmado).
   Pela integração do Claude o ilimitado não vale (75 créditos/imagem e a conta não tem saldo avulso).
   Space: https://www.magnific.com/app/spaces/a301317b-f6c4-441f-b00d-435873d30eb8 — um painel por produto,
   referências da Duda já ligadas.
2. Narração no ElevenLabs com a voz da Duda (~320 créditos por take).
3. Clipe 1 (Kling 2.5 Turbo, 10s) a partir da cena de frente, ela vindo até a câmera mostrar detalhe.
4. Clipe 2 a partir do **último quadro do clipe 1** (continuidade, sem gerar imagem nova): vira de lado e
   termina com a mão na lente.
5. Montagem local com ffmpeg, narração por cima, `loudnorm` em -14 LUFS.

Evitar cena de bastidor com tripé: a IA erra a orientação do celular (tela virada para a câmera errada).

Flow no ElevenLabs com tudo do primeiro vídeo:
https://elevenlabs.io/app/flows/OMaQG5ueD5MnwaeymOkd

## Regras do TikTok Shop

- Ativar o selo de **conteúdo gerado por IA** em todo post.
- A Duda mostra e demonstra o produto; **nunca** diz que usou e teve resultado.

## Vídeos

- `narracao-conjunto-lot.mp3` — narração do conjunto LOT (voz 1, sem o trecho "é da Lote").
- Os `.mp4` renderizados não vão para o repositório (`.gitignore`).
