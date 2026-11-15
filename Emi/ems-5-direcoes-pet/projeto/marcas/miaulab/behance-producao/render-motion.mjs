// MIAU.LAB · renderiza uma prancha animada de motion.html (1400x1050, 30 fps) em MP4 e GIF (para o Behance).
// uso: node behance/render-motion.mjs gato   → behance/motion/gato.mp4 e gato.gif
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { spawn, spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, '../../..'), modo = process.argv[2], FPS = 30;
const out = path.join(aqui, 'motion'); fs.mkdirSync(out, { recursive: true });
const tipos = { '.html': 'text/html', '.png': 'image/png', '.woff2': 'font/woff2', '.js': 'text/javascript', '.jpg': 'image/jpeg' };
const srv = http.createServer((rq, rs) => { const f = path.join(raiz, decodeURIComponent(rq.url.split('?')[0]));
  fs.readFile(f, (e, d) => { if (e) { rs.writeHead(404); rs.end(); return; } rs.writeHead(200, { 'content-type': tipos[path.extname(f)] || 'application/octet-stream' }); rs.end(d); }); });
await new Promise(r => srv.listen(0, r));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 1050 } });
await p.goto(`http://127.0.0.1:${srv.address().port}/marcas/miaulab/behance-producao/motion.html?m=${modo}`);
await p.waitForFunction(() => document.body.dataset.pronto === '1');
await p.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
const n = Math.round(await p.evaluate(() => window.DURACAO) * FPS), mp4 = path.join(out, `${modo}.mp4`);
const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-vf', 'format=yuv420p',
  '-c:v', 'libx264', '-crf', '17', '-preset', 'slow', '-movflags', '+faststart', mp4], { stdio: ['pipe', 'inherit', 'inherit'] });
for (let i = 0; i < n; i++) { await p.evaluate(t => window.quadro(t), i / FPS); const buf = await p.screenshot({ type: 'png' });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
ff.stdin.end(); await new Promise(r => ff.on('close', r));
await b.close(); srv.close();
// GIF em loop (paleta própria, cores chapadas da marca ficam limpas); 3 voltas no MP4 para quem preferir vídeo
spawnSync('ffmpeg', ['-v', 'error', '-y', '-i', mp4, '-vf', 'fps=25,scale=1400:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96:stats_mode=diff[p];[b][p]paletteuse=dither=none', '-loop', '0', path.join(out, `${modo}.gif`)]);

console.log('ok', modo, n, 'quadros');
