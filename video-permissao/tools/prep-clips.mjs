// Cuts and color-grades the clips used in the edit.
// Usage: npm run clips -- "C:\\Users\\Linki\\Videos\\Motion\\brutos"
// Needs ffmpeg on PATH (winget install Gyan.FFmpeg) and the raw files from the Drive folder "video 2".
import {spawnSync} from 'node:child_process';
import {readFileSync, existsSync, mkdirSync} from 'node:fs';
import path from 'node:path';

const rawDir = process.argv[2] ?? path.resolve('..', 'brutos');
const outDir = path.resolve('public', 'clips');
mkdirSync(outDir, {recursive: true});

const grade = readFileSync('tools/grade.txt', 'utf8').trim(); // flat-profile footage (C25xx.MP4)
const kodak = 'eq=contrast=1.05:saturation=1.1:gamma=1.02,colorbalance=rh=0.03:bh=-0.03,unsharp=5:5:0.6';

const lines = readFileSync('tools/clips.txt', 'utf8').split(/\r?\n/).filter(Boolean);
for (const line of lines) {
  const [name, src, start, dur, kind] = line.trim().split(/\s+/);
  const input = path.join(rawDir, src);
  if (!existsSync(input)) {
    console.error(`faltando: ${input}`);
    continue;
  }
  const vf =
    kind === 'k'
      ? `fps=24,scale=1440:1080:flags=lanczos,${kodak}`
      : kind === 'v'
        ? `fps=24,scale=1080:1920:flags=lanczos,${grade}`
        : `fps=24,scale=1920:1080:flags=lanczos,${grade}`;
  const args = ['-nostdin', '-v', 'error', '-y', '-ss', start, '-t', dur, '-i', input, '-vf', vf,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '128k', '-ar', '48000', path.join(outDir, `${name}.mp4`)];
  const r = spawnSync('ffmpeg', args, {stdio: 'inherit'});
  console.log(r.status === 0 ? `ok ${name}` : `erro ${name}`);
}
