"""Trilha do reel: o samba instrumental (ElevenLabs Music, 120 bpm) estendido para 41,5 s e colocado no MP4.
- corta 0,034 s do começo: assim as batidas caem em 0; 0,5; 1,0... (a grade dos cortes do vídeo);
- repete os 8 s entre 2,0 e 10,0 logo depois dos 10,0 (esse trecho se repete quase igual na própria música,
  então a emenda some); o golpe final passa de 32,0 para 40,0 s, no cartão final;
- volume no padrão das redes (-14 LUFS) e silêncio até completar a duração do vídeo.
Uso: python3 -I reel_trilha.py  (depois de node filme_render.js reel)"""
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
AP = os.path.join(AQUI, '..', '07-apresentacao')
TR = os.path.join(AP, 'instagram', 'reel', '_trilha')
ORIG = os.path.join(TR, 'samba-original.mp3')
WAV = os.path.join(TR, 'samba-reel.wav')
VIDEO = os.path.join(AP, 'behance', 'videos', 'filme-reel.mp4')
SAIDA = os.path.join(AP, 'instagram', 'reel', 'bem-querer-reel.mp4')
OFF, DUR = .034, 41.5

grafo = (f'[0]atrim=start={OFF}:end={OFF + 10},asetpts=PTS-STARTPTS[a];'
         f'[0]atrim=start={OFF + 2}:end={OFF + 10},asetpts=PTS-STARTPTS[b];'
         f'[0]atrim=start={OFF + 10},asetpts=PTS-STARTPTS[c];'
         '[a][b]acrossfade=d=0.01:c1=tri:c2=tri[ab];'
         '[ab][c]concat=n=2:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=11,'
         f'afade=t=in:d=0.02,afade=t=out:st={DUR - .6}:d=0.6,apad,atrim=end={DUR}[s]')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', ORIG, '-filter_complex', grafo, '-map', '[s]', '-ar', '48000', WAV], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', VIDEO, '-i', WAV, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                '-af', 'apad', '-c:a', 'aac', '-b:a', '192k', '-t', str(DUR), '-movflags', '+faststart', SAIDA], check=True)
print('ok:', os.path.relpath(SAIDA, AP), f'{os.path.getsize(SAIDA) / 1e6:.1f} MB')
