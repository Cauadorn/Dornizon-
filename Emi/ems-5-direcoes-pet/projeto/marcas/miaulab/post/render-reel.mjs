// MIAU.LAB · renderiza reel.html quadro a quadro (30 fps) e monta o MP4 9:16 com grão de filme leve.
// uso: node render-reel.mjs [pagina.html] saida.mp4            → vídeo inteiro (página padrão: reel.html)
//      node render-reel.mjs pasta/ 0.3 1.2 2.6   → só esses instantes, em PNG (para conferir)
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path'; import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, '../../..');
const args = process.argv.slice(2), pagina = args[0].endsWith('.html') ? args.shift() : 'reel.html';
const [saida, ...instantes] = args, FPS = 30;
const tipos = { '.html': 'text/html', '.png': 'image/png', '.woff2': 'font/woff2', '.js': 'text/javascript', '.jpg': 'image/jpeg' };
const srv = http.createServer((rq, rs) => { const f = path.join(raiz, decodeURIComponent(rq.url.split('?')[0]));
  fs.readFile(f, (e, d) => { if (e) { rs.writeHead(404); rs.end(); return; } rs.writeHead(200, { 'content-type': tipos[path.extname(f)] || 'application/octet-stream' }); rs.end(d); }); });
await new Promise(r => srv.listen(0, r));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto(`http://127.0.0.1:${srv.address().port}/marcas/miaulab/post/${pagina}`);
await p.waitForFunction(() => document.body.dataset.pronto === '1');
// garante as fotos decodificadas antes do primeiro quadro
await p.evaluate(() => Promise.all([...document.querySelectorAll('.foto')].map(f => { const i = new Image(); i.src = f.style.backgroundImage.slice(5, -2); return i.decode(); })));
const quadro = async t => { await p.evaluate(t => window.quadro(t), t); return p.screenshot({ type: 'png' }); };
if (instantes.length) {
  fs.mkdirSync(saida, { recursive: true });
  for (const s of instantes) fs.writeFileSync(path.join(saida, `t-${s}.png`), await quadro(+s));
} else {
  const dur = await p.evaluate(() => window.DURACAO), n = Math.round(dur * FPS);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-vf', 'noise=alls=4:allf=t,format=yuv420p', '-c:v', 'libx264', '-crf', '19', '-preset', 'slow', '-movflags', '+faststart', saida], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < n; i++) { const buf = await quadro(i / FPS); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await b.close(); srv.close(); console.log('ok', saida);
