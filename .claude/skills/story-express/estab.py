#!/usr/bin/env python3
"""Estabilização forte para clipes de story (1080x1920).

Rastreia pontos (Shi-Tomasi + Lucas-Kanade), estima translação+rotação+escala
quadro a quadro, troca o caminho da câmera por uma curva lisa (polinômio de grau
baixo = panorâmica de trilho) e aplica um zoom fixo mínimo para não aparecer borda.

uso: estab.py entrada saida.mp4 [--ss 0.5] [--t 5.5] [--fps 24] [--grau 2] [--noautorotate] [--vf filtros]
     estab.py --medir arquivo [--noautorotate]   -> imprime o tremor residual
"""
import argparse, subprocess, sys
import numpy as np, cv2
from scipy.ndimage import gaussian_filter1d

W, H = 1080, 1920
AW, AH = 540, 960  # resolução da análise


def frames(src, ss, t, fps, w, h, fmt, noauto):
    cmd = ['ffmpeg', '-v', 'error']
    if noauto:
        cmd.append('-noautorotate')
    if ss:
        cmd += ['-ss', str(ss)]
    if t:
        cmd += ['-t', str(t)]
    cmd += ['-i', src, '-vf',
            f'scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h},fps={fps}',
            '-f', 'rawvideo', '-pix_fmt', fmt, '-']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    ch = 3 if fmt == 'bgr24' else 1
    n = w * h * ch
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, ch) if ch == 3 else np.frombuffer(b, np.uint8).reshape(h, w)
    p.wait()


def trajetoria(src, ss, t, fps, noauto):
    prev = None
    steps = [(0.0, 0.0, 0.0, 0.0)]
    for g in frames(src, ss, t, fps, AW, AH, 'gray', noauto):
        g = cv2.GaussianBlur(g, (3, 3), 0)
        if prev is not None:
            p0 = cv2.goodFeaturesToTrack(prev, maxCorners=500, qualityLevel=0.005, minDistance=12, blockSize=5)
            m = None
            if p0 is not None and len(p0) >= 8:
                p1, st, _ = cv2.calcOpticalFlowPyrLK(prev, g, p0, None, winSize=(31, 31), maxLevel=4)
                ok = st.ravel() == 1
                if ok.sum() >= 8:
                    m, _ = cv2.estimateAffinePartial2D(p0[ok], p1[ok], method=cv2.RANSAC, ransacReprojThreshold=2.0)
            if m is None:
                steps.append(steps[-1] if len(steps) > 1 else (0, 0, 0, 0))
            else:
                da = np.arctan2(m[1, 0], m[0, 0])
                ds = np.log(np.hypot(m[0, 0], m[1, 0]))
                c = np.array([AW / 2, AH / 2])
                tc = m[:, 2] + m[:, :2] @ c - c  # translação medida em relação ao centro
                steps.append((tc[0], tc[1], da, ds))
        prev = g
    return np.cumsum(np.array(steps), axis=0)  # x, y (px de análise), ângulo, log-escala


def tremor(traj):
    hf = traj - gaussian_filter1d(traj, sigma=4, axis=0, mode='nearest')
    return np.sqrt((hf[:, 0] ** 2 + hf[:, 1] ** 2).mean()) * (W / AW), np.degrees(np.sqrt((hf[:, 2] ** 2).mean()))


def matriz(dx, dy, da, ds, z):
    c = np.array([W / 2, H / 2])
    s = np.exp(ds) * z
    a = np.array([[np.cos(da), -np.sin(da)], [np.sin(da), np.cos(da)]]) * s
    t = c + np.array([dx, dy]) - a @ c
    return np.hstack([a, t[:, None]])


def zoom_min(corr):
    cs = np.array([[0, 0], [W, 0], [0, H], [W, H]], float)
    lo, hi = 1.0, 1.6
    for _ in range(30):
        z = (lo + hi) / 2
        ok = True
        for dx, dy, da, ds in corr:
            m = cv2.invertAffineTransform(matriz(dx, dy, da, ds, z))
            src = cs @ m[:, :2].T + m[:, 2]
            if (src < -0.5).any() or (src[:, 0] > W + 0.5).any() or (src[:, 1] > H + 0.5).any():
                ok = False
                break
        lo, hi = (lo, z) if ok else (z, hi)
    return hi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('out', nargs='?')
    ap.add_argument('--ss', type=float, default=0); ap.add_argument('--t', type=float, default=0)
    ap.add_argument('--fps', type=float, default=24); ap.add_argument('--grau', type=int, default=2)
    ap.add_argument('--noautorotate', action='store_true'); ap.add_argument('--medir', action='store_true')
    ap.add_argument('--crf', default='12'); ap.add_argument('--vf', default='')
    a = ap.parse_args()

    traj = trajetoria(a.src, a.ss, a.t, a.fps, a.noautorotate)
    if a.medir:
        px, deg = tremor(traj)
        print(f'tremor residual: {px:.2f}px  {deg:.3f}°  ({len(traj)} quadros)')
        return

    n = len(traj)
    x = np.arange(n)
    lisa = np.column_stack([np.polyval(np.polyfit(x, traj[:, k], a.grau), x) for k in range(4)])
    corr = lisa - traj
    corr[:, :2] *= W / AW  # análise -> resolução final
    z = zoom_min(corr)
    px0, deg0 = tremor(traj)
    print(f'antes: {px0:.2f}px {deg0:.3f}°  | zoom {z:.3f}', file=sys.stderr)

    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}',
                            '-r', str(a.fps), '-i', '-'] + (['-vf', a.vf] if a.vf else []) + ['-an', '-c:v', 'libx264', '-preset', 'ultrafast',
                            '-crf', a.crf, '-pix_fmt', 'yuv420p', a.out], stdin=subprocess.PIPE)
    for i, f in enumerate(frames(a.src, a.ss, a.t, a.fps, W, H, 'bgr24', a.noautorotate)):
        if i >= n:
            break
        m = matriz(*corr[i], z)
        enc.stdin.write(cv2.warpAffine(f, m, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT).tobytes())
    enc.stdin.close(); enc.wait()


if __name__ == '__main__':
    main()
