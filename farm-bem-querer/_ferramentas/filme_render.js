// Renderiza um filme de 07-apresentacao/behance/filmes/<nome>.html quadro a quadro (24 fps) e gera o MP4 (1280 px).
// uso: node filme_render.js abertura [segundos-de-teste]
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');
const B = path.join(__dirname, '..', '07-apresentacao', 'behance');
const nome = process.argv[2];
const so = process.argv[3] ? +process.argv[3] : 0;
(async () => {
  const pasta = path.join(B, '_render', nome);
  fs.mkdirSync(pasta, { recursive: true });
  for (const f of fs.readdirSync(pasta)) fs.unlinkSync(path.join(pasta, f));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 1200 }, deviceScaleFactor: 1 });
  const erros = []; p.on('pageerror', e => erros.push(e.message));
  await p.goto('file://' + path.join(B, 'filmes', nome + '.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => window.PRONTO);
  const dur = await p.evaluate(() => window.FILME.dur);
  const fim = so || dur;
  const palco = await p.$('#palco');
  const n = Math.round(fim * 24);
  for (let k = 0; k < n; k++) {
    await p.evaluate(t => window.FILME.seek(t), k / 24);
    await palco.screenshot({ path: path.join(pasta, String(k + 1).padStart(4, '0') + '.jpg'), type: 'jpeg', quality: 94 });
  }
  await b.close();
  if (erros.length) console.log('erros:', erros.join(' | '));
  fs.mkdirSync(path.join(B, 'videos'), { recursive: true });
  const saida = path.join(B, 'videos', `filme-${nome}.mp4`);
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', '24', '-i', path.join(pasta, '%04d.jpg'),
    '-vf', 'scale=1280:-2:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-profile:v', 'high', '-crf', '17', '-preset', 'slow',
    '-movflags', '+faststart', saida]);
  console.log(nome, n, 'quadros', (n / 24).toFixed(1) + 's', (fs.statSync(saida).size / 1e6).toFixed(1), 'MB');
})();
