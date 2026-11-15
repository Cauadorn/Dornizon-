#!/bin/sh
# Refaz todas as camadas da capa do quilo. As duas etapas rodam sempre juntas, nesta ordem
# (a segunda parte dos tamanhos que a primeira mede; rodar só a segunda encolhe as estrelas a cada vez).
PY="${PY:-python3}"
$PY pecas-inteiras.py cenas/pecas && $PY camadas-quilo.py cenas/quilo.png camadas/quilo /tmp/conf-quilo.jpg && $PY camadas-quilo2.py cenas/quilo.png camadas/quilo
