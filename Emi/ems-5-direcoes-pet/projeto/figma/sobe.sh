#!/usr/bin/env bash
# uso: sobe.sh <src> <submitUrl> ...   (pares). src = "raster:rNNN", "arquivo.png" ou "arquivo.png#flip"
set -u
F=$(cd "$(dirname "$0")" && pwd); IMG="$F/../img"; RAS="$F/saida/rasters"; TMP="$F/saida/flip"; mkdir -p "$TMP"
while [ $# -ge 2 ]; do
  src="$1"; url="$2"; shift 2
  case "$src" in
    raster:*) arq="$RAS/${src#raster:}.png" ;;
    *'#flip') base="${src%#flip}"; arq="$TMP/$base"; [ -f "$arq" ] || python3 -I -c "import sys;from PIL import Image,ImageOps;ImageOps.mirror(Image.open(sys.argv[1])).save(sys.argv[2])" "$IMG/$base" "$arq" ;;
    *) arq="$IMG/$src" ;;
  esac
  printf '%s -> ' "$src"; curl -sS -X POST -F "file=@$arq;type=image/png" "$url" | head -c 160; echo
done
