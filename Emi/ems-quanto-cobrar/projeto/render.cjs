// Renderiza um HTML animado (window.render(t), window.DURATION) quadro a quadro e junta em mp4.
// uso: node render.cjs <arquivo.html> <saida.mp4|png> <largura> <altura> [--still t]
const { chromium } = require('playwright'); const path = require('node:path'); const fs = require('node:fs'); const { spawnSync } = require('node:child_process');
(async () => {
  const [html, out, w, h, flag, tt] = process.argv.slice(2); const FPS = 30;
  const b = await chromium.launch();
  const open = async () => { const p = await b.newPage({ viewport: { width: +w, height: +h } }); await p.goto('file://' + path.resolve(html)); await p.waitForFunction(() => window.READY === true); return p; };
  if (flag === '--still') { const p = await open(); for (const [i, t] of tt.split(',').entries()) { await p.evaluate((t) => window.render(t), +t); await p.screenshot({ path: tt.includes(',') ? out.replace('.png', `-${i}.png`) : out, clip: { x: 0, y: 0, width: +w, height: +h } }); } await b.close(); return; }
  const p0 = await open(); const dur = await p0.evaluate(() => window.DURATION); await p0.close();
  const total = Math.round(dur * FPS), W = 4, per = Math.ceil(total / W);
  const tmp = fs.mkdtempSync(path.join(process.env.TMPDIR || '/tmp', 'quadros-'));
  await Promise.all(Array.from({ length: W }, async (_, k) => { const p = await open();
    for (let f = k * per; f < Math.min(total, (k + 1) * per); f++) { await p.evaluate((t) => window.render(t), f / FPS); await p.screenshot({ path: path.join(tmp, `f${String(f).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 94, clip: { x: 0, y: 0, width: +w, height: +h } }); } await p.close(); }));
  await b.close();
  const r = spawnSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(tmp, 'f%05d.jpg'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', '-movflags', '+faststart', out], { stdio: 'inherit' });
  fs.rmSync(tmp, { recursive: true, force: true }); console.log(r.status === 0 ? `ok → ${out} (${total} quadros)` : 'ffmpeg falhou');
})();
