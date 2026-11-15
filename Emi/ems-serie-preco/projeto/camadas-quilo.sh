#!/bin/sh
# Refaz todas as camadas da capa do quilo. As etapas rodam sempre juntas, nesta ordem
# (a segunda parte dos tamanhos que a primeira mede; rodar só a segunda encolhe as estrelas a cada vez).
# A terceira amplia 2x as camadas com Real-ESRGAN: precisa de torch e do modelo RealESRGAN_x2plus.pth (variável ESRGAN).
PY="${PY:-python3}"
$PY pecas-inteiras.py cenas/pecas && $PY camadas-quilo.py cenas/quilo.png camadas/quilo /tmp/conf-quilo.jpg && $PY camadas-quilo2.py cenas/quilo.png camadas/quilo || exit 1
if [ -n "$ESRGAN" ]; then
  $PY ampliar.py "$ESRGAN" camadas/quilo fundo.png palavra.png bal-corpo.png bal-prato.png bal-prato-aro.png ponteiro.png A.png a.png amostra1.png amostra2.png amostra3.png amostra4.png ar1.png ar2.png estrela.png cursor.png
fi
