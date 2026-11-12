# upscale 4x em blocos com sobreposição (4xNomosWebPhoto, ONNX na CPU)
import sys, time, numpy as np, onnxruntime as ort
from PIL import Image
ent, sai, base_w, final_w = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
im = Image.open(ent).convert('RGB')
im = im.resize((base_w, round(im.height * base_w / im.width)), Image.LANCZOS)
x = np.asarray(im).astype(np.float32) / 255
H, W = x.shape[:2]
so = ort.SessionOptions(); so.intra_op_num_threads = 4
s = ort.InferenceSession(sys.argv[5] if len(sys.argv) > 5 else 'nomos.onnx', so, providers=['CPUExecutionProvider'])
T, P = 192, 16
out = np.zeros((H * 4, W * 4, 3), np.float32); peso = np.zeros((H * 4, W * 4, 1), np.float32)
t0 = time.time(); n = 0
for y0 in range(0, H, T):
    for x0 in range(0, W, T):
        ya, xa = max(0, y0 - P), max(0, x0 - P); yb, xb = min(H, y0 + T + P), min(W, x0 + T + P)
        tile = x[ya:yb, xa:xb].transpose(2, 0, 1)[None]
        r = s.run(None, {'input': tile})[0][0].transpose(1, 2, 0)
        # só o miolo (sem a borda de sobreposição)
        iy0, ix0 = (y0 - ya) * 4, (x0 - xa) * 4; iy1, ix1 = iy0 + min(T, H - y0) * 4, ix0 + min(T, W - x0) * 4
        out[y0 * 4:(y0 + min(T, H - y0)) * 4, x0 * 4:(x0 + min(T, W - x0)) * 4] = r[iy0:iy1, ix0:ix1]
        n += 1
print('blocos', n, 'em', round(time.time() - t0, 1), 's')
res = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8))
res = res.resize((final_w, round(res.height * final_w / res.width)), Image.LANCZOS)
res.save(sai, quality=95); print('ok', res.size)
