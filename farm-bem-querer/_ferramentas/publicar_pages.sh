#!/usr/bin/env bash
# Publica 07-apresentacao/site no branch gh-pages (GitHub Pages: https://cauadorn.github.io/Dornizon-/).
# Uso: bash publicar_pages.sh "mensagem do commit"
set -euo pipefail
RAIZ=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
SITE="$RAIZ/farm-bem-querer/07-apresentacao/site"
TMP=$(mktemp -d)
git -C "$RAIZ" fetch -q origin gh-pages
git -C "$RAIZ" worktree add -q "$TMP" origin/gh-pages --detach
find "$TMP" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp -r "$SITE/." "$TMP/"
touch "$TMP/.nojekyll"
git -C "$TMP" add -A
if git -C "$TMP" diff --cached --quiet; then echo "nada mudou"; else
  git -C "$TMP" commit -qm "${1:-Atualiza o site}"
  git -C "$TMP" push -q origin HEAD:gh-pages
  echo "publicado"
fi
git -C "$RAIZ" worktree remove --force "$TMP"
