---
name: artes-clientes
description: Motor de criação de artes da 4D para qualquer cliente (IDEX, Quero Mais Crédito, LamCred, Credleve, Arium e os demais). Use sempre que o pedido for fazer, refazer ou ajustar uma arte, post, carrossel ou story de um card do Runrun.it, ou citar um cliente pelo nome. Antes de desenhar, abre a identidade visual e as artes mais recentes do cliente no Drive. Ao terminar, sobe a arte na pasta do cliente.
---

# Artes de clientes (motor 4D)

Regra do Cauã, vale para **todos os clientes**:

1. **O motor de criação é o Design System do cliente no Claude** (artifacts do tipo "Design System", tabela abaixo). Antes de criar, ler dele: `project/README.md`, `project/guidelines/*`, `project/tokens.css`, os templates e as pastas de assets (logo, grafismo, references, referencias-direcao, Uploads). O Drive é só fonte secundária (cronograma, pasta do card).
2. **Depois de criar**, subir a arte final no asset store do Design System do cliente (Artifact publish com `url` do DS, `asset: true`), para o motor sempre ter as artes mais novas como referência. Se o Cauã pedir, subir também no Drive.
3. Registrar o que foi aprendido no arquivo do cliente em `clientes/<cliente>.md` e fazer commit.

## Design Systems (motor) por cliente

| Cliente | Design System |
|---|---|
| IDEX | https://claude.ai/artifact/2KgLdSoAFWtbQHTtT8pLKC |
| CREDFRANCO | https://claude.ai/artifact/9FcPBfHChAXCSyWh924PS7 |
| Quero +Crédito | https://claude.ai/artifact/WfsBkHA9rMfKxTuQw6ZhNG |
| X3 Promotora | https://claude.ai/artifact/9Lg4J1Pc2qZxFhKSgUJP9t |
| i3Cred | https://claude.ai/artifact/SRz9MHLCDgdCKJeyhiAjW2 |
| Chat Doutor | https://claude.ai/artifact/GFJPCRUnoywHemwBwKkGij |

Há outros artifacts chamados só "Design System" (sem cliente no título): ler o README de cada um para descobrir o cliente e completar a tabela.

## Passo a passo

1. **Card**: pegar o ID e o título no Runrun.it (`search_tasks` com o ID). O conector só devolve título, projeto e etapa. Briefing, tipo, alocados e prazo ficam na descrição do card:
   - Se existirem `RUNRUNIT_APP_KEY` e `RUNRUNIT_USER_TOKEN` no ambiente, ler pela API: `GET https://runrun.it/api/v1.0/tasks/<id>` com os headers `App-Key` e `User-Token` (a descrição vem em `/tasks/<id>/description`).
   - Se não, pedir ao Cauã o texto do briefing. **Nunca inventar copy**: sem briefing, não há arte.
2. **Cliente**: abrir `clientes/<cliente>.md`. Se o arquivo não existir, achar no Drive (`search_files`, `title contains '<cliente>'`) a pasta do cliente, o manual/brandbook, os logos e a pasta de publicações do ano, e criar o arquivo seguindo o modelo de `clientes/idex.md`.
3. **Referências**: listar as 3 a 5 pastas de card mais recentes do mês (`parentId = '<pasta do mês>'`) e ler as artes (`read_file_content` em PNG devolve o texto da peça; `download_file_content` traz a imagem). Seguir grid, hierarquia, tom e assinatura dessas peças.
4. **Produção**: montar em HTML/CSS e exportar com o Chromium do Playwright (ver `Emi/badaue-teste-vitoria-regia/projeto/render.mjs`). Formatos padrão: feed 1080x1350, story 1080x1920, carrossel 1080x1350 por lâmina. Projeto em `<cliente>/<id>-<slug>/` no repositório, com `projeto/` e `entrega/`.
5. **Conferência**: rodar o checklist da skill `avaliacao-de-design` (Modo 2: texto x briefing e padrão visual) antes de entregar.
6. **Entrega no Drive**: na pasta de publicações do cliente, dentro do mês da publicação:
   - se a Flávia já criou a pasta do card (nome = título do card), subir lá;
   - se não, criar a pasta com o título exato do card.
   - Nome do arquivo: `#<id> - <título curto> [<CLIENTE>] - feed 1080x1350.png` (ou `story 1080x1920`, `slide-01`...).
   - Subir com `create_file` (`base64Content`, `contentMimeType: image/png`, `disableConversionToGoogleType: true`, `parentId` da pasta).
7. **Runrun.it**: não mover, não comentar e não editar o card sem autorização explícita do Cauã naquele pedido. Só reportar o link da pasta.

## Clientes cadastrados

| Cliente | Arquivo |
|---|---|
| IDEX Brasil | `clientes/idex.md` |
| Quero Mais Crédito | `clientes/quero-mais-credito.md` |
| Topo do Mundo | `clientes/topo-do-mundo.md` |

LamCred tem skill própria (`lamcred-artes`) e EMS também (`marca-ems`): usar a skill do cliente quando existir e, mesmo assim, cumprir os passos 1 e 2 das regras acima.
