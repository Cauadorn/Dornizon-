"""Conta-gotas: cor mediana de uma regiao (coordenadas na miniatura de ate 890x640)."""
import json, sys
import numpy as np
from PIL import Image
def amostra(path, box):
    im = Image.open(path).convert('RGB'); im.thumbnail((890, 640))
    a = np.asarray(im.crop(tuple(box)), dtype=np.float32).reshape(-1, 3)
    return '#%02X%02X%02X' % tuple(int(v) for v in np.median(a, axis=0))
if __name__ == '__main__':
    cfg = json.load(open(sys.argv[1])); d = sys.argv[2]
    print(json.dumps({k: amostra(d + '/' + v[0], v[1]) for k, v in cfg.items()}, ensure_ascii=False, indent=0))
