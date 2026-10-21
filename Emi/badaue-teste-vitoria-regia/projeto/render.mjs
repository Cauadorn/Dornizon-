// Exporta o carrossel com o Chromium do Playwright.
// uso: node render.mjs              -> entrega/lamina-01..07.png + entrega/visao-geral.jpg
//      node render.mjs --vetor      -> idem, forçando as ilustrações vetoriais (sem imagens/)
//      node render.mjs --capa       -> entrega/capa-motion.mp4 (quadro a quadro, 30 fps)
//      node render.mjs --capa --stills 0,2.5,5  -> stills/capa-t.png para conferir
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { spawn } from 'node:child_process';
import http from 'node:http';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const dir = path.dirname(fileURLToPath(import.meta.url));
const saida = path.join(dir, '..', 'entrega');
const args = process.argv.slice(2);
const opt = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
fs.mkdirSync(saida, { recursive: true });

const tipos = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.woff2': 'font/woff2', '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml' };
const server = http.createServer((req, res) => {
  const p = path.join(dir, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!p.startsWith(dir) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': tipos[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const base = `http://127.0.0.1:${server.address().port}`;
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });

async function abrir(pagina, vp) {
  const page = await browser.newPage({ viewport: vp, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => console.error('erro na página:', e.message));
  await page.goto(`${base}/${pagina}`);
  await page.waitForFunction(() => window.READY === true, null, { timeout: 60000 });
  return page;
}

function ffmpeg(a) {
  return new Promise((ok, falha) => {
    const p = spawn('ffmpeg', a, { stdio: ['ignore', 'ignore', 'inherit'] });
    p.on('close', (c) => (c === 0 ? ok() : falha(new Error('ffmpeg ' + c))));
  });
}

if (args.includes('--capa')) {
  const stills = opt('--stills');
  const page = await abrir('capa.html' + (args.includes('--vetor') ? '?vetor' : ''), { width: 1080, height: 1350 });
  const dur = await page.evaluate(() => window.DURATION);
  const stage = page.locator('.lamina');
  if (stills) {
    fs.mkdirSync(path.join(dir, 'stills'), { recursive: true });
    for (const s of stills.split(',')) {
      await page.evaluate((t) => window.render(t), +s);
      await stage.screenshot({ path: path.join(dir, 'stills', `capa-${s}.png`) });
    }
  } else {
    const FPS = 30;
    const total = Math.round(dur * FPS);
    const tmp = fs.mkdtempSync(path.join(process.env.TMPDIR || '/tmp', 'capa-'));
    for (let f = 0; f < total; f++) {
      await page.evaluate((t) => window.render(t), f / FPS);
      await stage.screenshot({ path: path.join(tmp, `f${String(f).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 95 });
      if (f % 60 === 0) console.log(`quadro ${f}/${total}`);
    }
    const mp4 = path.join(saida, 'capa-motion.mp4');
    await ffmpeg(['-y', '-framerate', String(FPS), '-i', path.join(tmp, 'f%04d.jpg'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-preset', 'slow', '-movflags', '+faststart', mp4]);
    await ffmpeg(['-y', '-i', mp4, '-vf', 'fps=15,scale=540:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=200[p];[b][p]paletteuse=dither=sierra2_4a', path.join(saida, 'capa-motion-preview.gif')]);
    fs.rmSync(tmp, { recursive: true });
    console.log('ok', mp4);
  }
} else {
  const page = await abrir('carrossel.html' + (args.includes('--vetor') ? '?vetor' : ''), { width: 1080 * 7, height: 1350 });
  const laminas = page.locator('.lamina');
  const n = await laminas.count();
  for (let k = 0; k < n; k++) {
    await laminas.nth(k).screenshot({ path: path.join(saida, `lamina-${String(k + 1).padStart(2, '0')}.png`) });
  }
  // visão geral: as 7 lâminas lado a lado, como no arrastar do carrossel
  await page.screenshot({ path: path.join(dir, 'stills', 'faixa.png'), fullPage: true }).catch(async () => {
    fs.mkdirSync(path.join(dir, 'stills'), { recursive: true });
    await page.screenshot({ path: path.join(dir, 'stills', 'faixa.png'), fullPage: true });
  });
  await ffmpeg(['-y', '-i', path.join(dir, 'stills', 'faixa.png'), '-vf', 'scale=3780:-1:flags=lanczos', '-q:v', '3', '-update', '1', path.join(saida, 'visao-geral.jpg')]);
  console.log('ok', n, 'lâminas');
}

await browser.close();
server.close();
