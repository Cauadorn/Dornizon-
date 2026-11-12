# Abre o enquadramento da foto da mesa (menos zoom no post 5).
# Lado: insere 91 px de parede lisa entre a luz da janela e a Lia (repete a parede de x 220..310 com emenda em degradê),
#       assim a luz da janela continua inteira e nada fica espelhado.
# Baixo: faixa de mesa sem objetos (fitinha do caderno apagada), espelhada em sanfona para emendar sem costura.
import numpy as np, cv2
im = cv2.imread('ia/filme-lia/mesa-a.jpg').astype(np.float32)
h, w = im.shape[:2]
A, N, F = 220, 91, 44            # onde insere, quantos px, largura da emenda
cols = []
for n in range(w + N):
    if n < A + N - F: cols.append(im[:, min(n, w - 1)])
    elif n < A + N:
        t = (n - (A + N - F)) / F; t = t * t * (3 - 2 * t)
        cols.append(im[:, n] * (1 - t) + im[:, n - N] * t)
    else: cols.append(im[:, n - N])
im = np.stack(cols, axis=1)
faixa = im[1345:1408].copy()
m = np.zeros(faixa.shape[:2], np.uint8); m[0:24, 576 + N:628 + N] = 255
faixa = cv2.inpaint(np.clip(faixa, 0, 255).astype(np.uint8), m, 11, cv2.INPAINT_TELEA).astype(np.float32)
ext = np.concatenate([faixa[::-1], faixa, faixa[::-1]])[:150]
im = np.concatenate([im, ext])
cv2.imwrite('ia/filme-lia/mesa-a-ampla.jpg', np.clip(im, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 94])
print(im.shape)
