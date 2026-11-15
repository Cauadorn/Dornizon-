// Render em alta: cada quadro é capturado em PNG (sem perda) no dobro da resolução e reduzido no final (bordas e letra mais limpas);
// o mp4 sai com compressão leve (crf 12) para o grão e o degradê não virarem bloco.
// uso: node render-hq.cjs <url ou arquivo.html> <saida.mp4> <largura> <altura>
const { chromium } = require('playwright'); const path = require('node:path'); const fs = require('node:fs'); const { spawnSync } = require('node:child_process');
(async () => {
  const [html, out, w, h] = process.argv.slice(2); const FPS = 30, ESC = 2;
  const b = await chromium.launch();
  const open = async () => { const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: ESC }); await p.goto(html.startsWith('http') ? html : 'file://' + path.resolve(html)); await p.waitForFunction(() => window.READY === true); return p; };
  const p0 = await open(); const dur = await p0.evaluate(() => window.DURATION); await p0.close();
  const total = Math.round(dur * FPS), W = 4, per = Math.ceil(total / W);
  const tmp = fs.mkdtempSync(path.join(process.env.TMPDIR || '/tmp', 'quadros-hq-'));
  await Promise.all(Array.from({ length: W }, async (_, k) => { const p = await open();
    for (let f = k * per; f < Math.min(total, (k + 1) * per); f++) { await p.evaluate((t) => window.render(t), f / FPS); await p.screenshot({ path: path.join(tmp, `f${String(f).padStart(5, '0')}.png`), clip: { x: 0, y: 0, width: +w, height: +h } }); } await p.close(); }));
  await b.close();
  const r = spawnSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(tmp, 'f%05d.png'), '-vf', `scale=${w}:${h}:flags=lanczos`, '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '12', '-preset', 'slow', '-tune', 'grain', '-movflags', '+faststart', out], { stdio: 'inherit' });
  fs.rmSync(tmp, { recursive: true, force: true }); console.log(r.status === 0 ? `ok → ${out} (${total} quadros)` : 'ffmpeg falhou');
})();
