---
name: story-express
description: Monta story de vídeo (Instagram, 1080x1920) em ~1 minuto a partir de clipes enviados — corte de ~5s por clipe, estabilização máxima, transição em flash delicado e bossa nova de restaurante chique, com versão sem áudio. Use sempre que mandarem vídeos (.mov/.mp4) pedindo story, "storymaker", corte com transição, ou vídeo de restaurante/evento para postar em tempo real.
---

# Story express

Stories são postados **em tempo real**: velocidade é o requisito nº 1. Não analise frames,
não faça contact sheet, não pergunte nada antes. Rode o script e entregue.

## Fazer (≈1 min)

```bash
.claude/skills/story-express/story.sh -o <scratchpad>/story.mp4 clipe1 clipe2 clipe3 ...
```

- **Ordem** = ordem dos argumentos. Se o pedido não disser a ordem: **fachada/letreiro/logo
  primeiro** (é a abertura do restaurante), o resto em ordem cronológica pelo nome do arquivo
  (`A001_..._C002`, `C004`, ...).
- Entrega na hora com `SendUserFile` os dois arquivos: `story.mp4` (com música) e
  `story_sem_audio.mp4` (para pôr música pelo adesivo do Instagram). Resposta curta.

O script já resolve sozinho:
- orientação (câmera grava em pé com tag de rotação errada → ignora a tag);
- corte de ~5s por clipe (pula o 0.4s inicial, onde a câmera treme);
- estabilização máxima (vidstab em 2 passes, suavização 40, zoom automático sem borda);
- flash delicado (dissolve de 0.5s + clarão branco a 35%);
- trilha "Bossa Antigua" (Kevin MacLeod, CC BY 4.0), normalizada, com fade;
- 1080x1920, H.264/AAC, faststart.

## Opções

| flag | uso |
|---|---|
| `clipe@2.3` | começa aquele clipe em 2.3s (quando a melhor parte não é o início) |
| `-F` | abertura travada: 1º quadro do 1º clipe + aproximação lenta. Use quando o take da fachada treme ou sai do letreiro |
| `-c W:H:X:Y` | recorte da abertura travada em pixels do original (só a fachada) |
| `-b` | fundo preto limpo na abertura travada (tira telhado/parede escura em volta do letreiro) |
| `-f 0.2` | flash mais sutil (`0` = só dissolve) |
| `-s 4` | segundos por clipe |
| `-n` | sem estabilização (mais rápido) |
| `-m faixa.mp3` | outra trilha |

## Aprendido com o cliente (O Italiano, nov/2026)

- A fachada com o letreiro "O Italiano" **sempre abre o story**.
- A fachada não pode tremer nem mostrar além dela → `-F -b -c` com recorte no letreiro
  (no take A001_11101913_C008: `-c 769:1367:445:205`).
- Flash **bem delicado**, nunca clarão branco total.
- **Estabilização máxima em tudo.**
- Crédito da trilha, se usar a do script: "Música: Kevin MacLeod (incompetech.com)".
- Sugestões chiques para o adesivo de música: "Estate" (Bruno Martino), "Via con me"
  (Paolo Conte), "The Girl from Ipanema" (Getz/Gilberto), "Corcovado", "Fly Me to the Moon".
