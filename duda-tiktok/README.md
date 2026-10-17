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
| Vídeo com lip-sync | ElevenLabs só no gancho de 4–5s, resto narração sobre cenas | ~5 mil créditos |

Referência: lip-sync completo de 19s em 720p (OmniHuman 1.5) custou ~18,5 mil créditos.
Sempre pedir orçamento (`estimate_only`) antes de gerar vídeo.

Flow no ElevenLabs com tudo do primeiro vídeo:
https://elevenlabs.io/app/flows/OMaQG5ueD5MnwaeymOkd

## Regras do TikTok Shop

- Ativar o selo de **conteúdo gerado por IA** em todo post.
- A Duda mostra e demonstra o produto; **nunca** diz que usou e teve resultado.

## Vídeos

- `narracao-conjunto-lot.mp3` — narração do conjunto LOT (voz 1, sem o trecho "é da Lote").
- Os `.mp4` renderizados não vão para o repositório (`.gitignore`).
