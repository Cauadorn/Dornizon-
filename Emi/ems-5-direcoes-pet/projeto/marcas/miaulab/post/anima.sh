#!/bin/bash
# Telas animadas do post MIAU.LAB: cor trocando seca, 0,5 s por estado (como as lâminas 1 e 4 da Melt), 3 s no total.
# Entrada: quadros/t1-*.png, t4-*.png e t9-*.png (1440x1800, de tela.html). Saída: lamina-01.mp4, lamina-04.mp4 e lamina-09.mp4 (1080x1350).
cd "$(dirname "$0")"
monta() { # $1 saída, $2.. quadros na ordem do ciclo; repete o ciclo até 3 s
  out=$1; shift; lista=$(mktemp); n=$#; voltas=$(( 6 / n ))
  for v in $(seq $voltas); do for q in "$@"; do echo "file '$PWD/quadros/$q.png'" >> $lista; echo "duration 0.5" >> $lista; done; done
  echo "file '$PWD/quadros/${@: -1}.png'" >> $lista
  ffmpeg -v error -y -f concat -safe 0 -i $lista -vf "scale=1080:1350:flags=lanczos,fps=30,format=yuv420p" -c:v libx264 -crf 14 -preset slow -movflags +faststart -t 3 $out
  rm $lista
}
monta lamina-01.mp4 t1-0 t1-1 t1-2
monta lamina-04.mp4 t4-0 t4-1
monta lamina-09.mp4 t9-0 t9-1 t9-2
