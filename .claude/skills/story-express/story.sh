#!/usr/bin/env bash
# story-express: junta clipes num story 1080x1920 em ~1 minuto.
#   corte de ~5s por clipe, orientação corrigida, estabilização máxima (vidstab 2 passes),
#   transição em flash delicado, bossa nova (Kevin MacLeod, CC BY 4.0) e versão sem áudio.
#
# uso: story.sh [opções] clipe1 clipe2 ...      (a ordem dos argumentos é a ordem do story)
#   clipe@2.3   começa aquele clipe em 2.3s (senão pula só o 0.4s inicial, onde a câmera treme)
#   -o saida.mp4   arquivo final (padrão ./story.mp4; a versão muda vira saida_sem_audio.mp4)
#   -s 5           segundos por clipe
#   -f 0.35        força do flash (0 = só dissolve, 1 = branco total)
#   -m musica.mp3  outra trilha
#   -F             primeiro clipe vira abertura travada: 1º quadro + aproximação lenta (fachada/letreiro), ~2.5s
#   -a 3           duração da abertura travada (com a transição; padrão 3 = ~2.5s na tela)
#   -c W:H:X:Y     recorte (em pixels do original) da abertura travada, ex. 769:1367:445:205
#   -b             abertura travada com fundo preto limpo (tira parede/telhado escuro em volta do letreiro)
#   -n             sem estabilização (mais rápido ainda)
set -euo pipefail

SEG=5; T=0.5; OUT="$PWD/story.mp4"; STAB=1; FIXA=0; MUSIC=""; FLASH=0.35; CROPF=""; LIMPO=0; ABRE=3
while getopts "o:s:m:f:c:a:nFbh" opt; do
  case $opt in
    o) OUT=$OPTARG ;; s) SEG=$OPTARG ;; m) MUSIC=$OPTARG ;; f) FLASH=$OPTARG ;;
    c) CROPF=$OPTARG ;; a) ABRE=$OPTARG ;; n) STAB=0 ;; F) FIXA=1 ;; b) LIMPO=1 ;;
    *) sed -n '2,18p' "$0"; exit 1 ;;
  esac
done
shift $((OPTIND-1))
[ $# -ge 1 ] || { sed -n '2,18p' "$0"; exit 1; }

T0=$(date +%s)
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
calc(){ awk "BEGIN{printf \"%.3f\", $1}"; }

# trilha: baixa uma vez e guarda em cache (em paralelo com o resto)
if [ -z "$MUSIC" ]; then
  CACHE=${XDG_CACHE_HOME:-$HOME/.cache}/story-express; mkdir -p "$CACHE"
  MUSIC=$CACHE/bossa-antigua.mp3
  [ -s "$MUSIC" ] || ( curl -sSL --max-time 40 -o "$MUSIC.tmp" \
      "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Bossa%20Antigua.mp3" \
      && mv "$MUSIC.tmp" "$MUSIC" || rm -f "$MUSIC.tmp" ) &
fi

# fps de saída = fps do 1º clipe, no máximo 30
F1=${1%@*}
FPS=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$F1")
FPS=$(awk -v r="$FPS" 'BEGIN{split(r,a,"/"); f=(a[2]?a[1]/a[2]:a[1]); if(f>30.5)f=30; printf "%g", (f>0?f:30)}')

B="scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1"
G="eq=contrast=1.04:saturation=1.06,format=yuv420p"
ENC=(-an -c:v libx264 -preset ultrafast -crf 12 -pix_fmt yuv420p)

declare -a FILE START LEN AR
i=0
for spec in "$@"; do
  f=${spec%@*}; st=""; [[ "$spec" == *@* ]] && st=${spec##*@}
  [ -f "$f" ] || { echo "não achei: $f" >&2; exit 1; }
  read -r w h < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$f" | tr ',' ' ')
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  # gravado em pé (h>w): ignora a tag de rotação da câmera, que costuma vir errada
  if [ "$h" -gt "$w" ]; then AR[$i]="-noautorotate"; else AR[$i]=""; fi
  want=$(calc "$SEG+$T")
  [ -n "$st" ] || st=$(awk -v d="$dur" -v n="$want" 'BEGIN{s=(d>n+0.4)?0.4:((d>n)?d-n:0); printf "%.3f", s}')
  LEN[$i]=$(awk -v d="$dur" -v s="$st" -v n="$want" 'BEGIN{l=d-s; if(l>n)l=n; printf "%.3f", l}')
  FILE[$i]=$f; START[$i]=$st
  i=$((i+1))
done
N=$i
[ "$FIXA" -eq 1 ] && LEN[0]=$ABRE
DIR=$(cd "$(dirname "$0")" && pwd)
OPENCV=0
if [ "$STAB" -eq 1 ]; then
  python3 -c "import cv2, scipy" 2>/dev/null || pip install -q opencv-python-headless scipy >/dev/null 2>&1 || true
  python3 -c "import cv2, scipy" 2>/dev/null && OPENCV=1
fi

prep(){ # $1 = índice
  local k=$1 f=${FILE[$1]} st=${START[$1]} len=${LEN[$1]} ar=${AR[$1]}
  if [ "$k" -eq 0 ] && [ "$FIXA" -eq 1 ]; then
    local nf; nf=$(awk -v l="$len" -v r="$FPS" 'BEGIN{printf "%d", l*r+0.5}')
    local pre="$B"; [ -n "$CROPF" ] && pre="crop=$CROPF,$B"
    [ "$LIMPO" -eq 1 ] && pre="$pre,curves=all='0/0 0.30/0 0.55/0.5 1/1'"
    ffmpeg -v error -y $ar -ss "$st" -i "$f" -vf "select=eq(n\,0),$pre,scale=3240:5760:flags=lanczos,zoompan=z='1.03+0.035*on/$nf':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$nf:s=1080x1920:fps=$FPS,setsar=1,$G" -frames:v "$nf" "${ENC[@]}" "$W/$k.mp4"
  elif [ "$STAB" -eq 1 ] && [ "$OPENCV" -eq 1 ]; then
    python3 "$DIR/estab.py" "$f" "$W/$k.mp4" --ss "$st" --t "$len" --fps "$FPS" ${ar:+--noautorotate} \
      --vf "unsharp=5:5:0.4:3:3:0,$G" 2>/dev/null
  elif [ "$STAB" -eq 1 ]; then
    ffmpeg -v error -y $ar -ss "$st" -t "$len" -i "$f" -vf "$B,fps=$FPS,vidstabdetect=shakiness=8:accuracy=15:result=$W/$k.trf" -f null -
    ffmpeg -v error -y $ar -ss "$st" -t "$len" -i "$f" -vf "$B,fps=$FPS,vidstabtransform=input=$W/$k.trf:smoothing=40:optzoom=1:interpol=bicubic,unsharp=5:5:0.4:3:3:0,$G" "${ENC[@]}" "$W/$k.mp4"
  else
    ffmpeg -v error -y $ar -ss "$st" -t "$len" -i "$f" -vf "$B,fps=$FPS,$G" "${ENC[@]}" "$W/$k.mp4"
  fi
}
for ((k=0; k<N; k++)); do prep $k & done
wait

# xfade (dissolve) + clarão branco suave por eq no meio de cada transição
IN=(); FC=""; OFF=0; FX="0"; prev="[v0]"
for ((k=0; k<N; k++)); do
  IN+=(-noautorotate -i "$W/$k.mp4")
  FC+="[$k:v]settb=AVTB,setpts=PTS-STARTPTS[v$k];"
done
for ((k=1; k<N; k++)); do
  OFF=$(calc "$OFF+${LEN[$((k-1))]}-$T")
  FC+="${prev}[v$k]xfade=transition=fade:duration=$T:offset=$OFF[x$k];"; prev="[x$k]"
  FX+="+between(t\,$OFF\,$OFF+$T)*pow(sin(PI*(t-$OFF)/$T)\,2)"
done
TOTAL=$(calc "$OFF+${LEN[$((N-1))]}")
FO=$(calc "$TOTAL-0.6"); AO=$(calc "$TOTAL-2")
FL="$FLASH*($FX)"
FC+="${prev}eq=eval=frame:contrast='1-$FL':brightness='0.42*$FL':saturation='1-$FL',fade=t=out:st=$FO:d=0.6,format=yuv420p,split[vo][vs]"

OUT_MUDO="${OUT%.*}_sem_audio.${OUT##*.}"
VENC=(-c:v libx264 -preset veryfast -crf 18 -profile:v high -pix_fmt yuv420p -r "$FPS" -movflags +faststart)
if [ -s "$MUSIC" ]; then
  FC+=";[$N:a]atrim=0:$TOTAL,asetpts=PTS-STARTPTS,loudnorm=I=-15:TP=-1.5:LRA=11,afade=t=in:st=0:d=0.3,afade=t=out:st=$AO:d=2,aresample=48000[a]"
  ffmpeg -v error -y "${IN[@]}" -i "$MUSIC" -filter_complex "$FC" \
    -map "[vo]" -map "[a]" "${VENC[@]}" -c:a aac -b:a 192k -shortest "$OUT" \
    -map "[vs]" -an "${VENC[@]}" "$OUT_MUDO"
else
  echo "aviso: sem trilha (download falhou); saindo só sem áudio" >&2
  ffmpeg -v error -y "${IN[@]}" -filter_complex "$FC;[vo]nullsink" -map "[vs]" -an "${VENC[@]}" "$OUT_MUDO"
fi

echo "pronto em $(( $(date +%s) - T0 ))s  |  ${TOTAL}s  1080x1920 @${FPS}fps"
[ -f "$OUT" ] && echo "com música: $OUT"
echo "sem áudio:  $OUT_MUDO"
