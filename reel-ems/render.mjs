// Renderiza o reel quadro a quadro com o Chromium do Playwright e junta no ffmpeg.
// uso: node render.mjs                 -> reel-ems.mp4 (sem áudio)
//      node render.mjs --audio voz.m4a -> reel-ems.mp4 com a narração
//      node render.mjs --stills 1,5,12 -> stills/t-<s>.png para conferir cenas
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const dir = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
const FPS = 30;
const out = opt('--out') || path.join(dir, 'reel-ems.mp4');
const audio = opt('--audio');
const stills = opt('--stills');
const workers = parseInt(opt('--workers') || '4', 10);

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }).catch(() => chromium.launch());

async function openPage() {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const timings = path.join(dir, 'timings.json');
  if (fs.existsSync(timings)) await page.addInitScript(`window.TIMINGS=${fs.readFileSync(timings, 'utf8')};`);
  await page.goto('file://' + path.join(dir, 'index.html'));
  await page.waitForFunction(() => window.READY === true);
  return page;
}

const stage = (page) => page.locator('#stage');

if (stills) {
  const page = await openPage();
  fs.mkdirSync(path.join(dir, 'stills'), { recursive: true });
  for (const s of stills.split(',')) {
    const t = parseFloat(s);
    await page.evaluate((t) => window.render(t), t);
    await stage(page).screenshot({ path: path.join(dir, 'stills', `t-${t.toFixed(2)}.png`) });
  }
  await browser.close();
  process.exit(0);
}

const probe = await openPage();
const duration = await probe.evaluate(() => window.DURATION);
await probe.close();
const total = Math.ceil(duration * FPS);
console.log(`duração ${duration.toFixed(2)}s, ${total} quadros`);

// cada worker renderiza um trecho contínuo em JPEG num diretório temporário
const tmp = fs.mkdtempSync(path.join(process.env.TMPDIR || '/tmp', 'reel-frames-'));
const per = Math.ceil(total / workers);
let done = 0;
await Promise.all(Array.from({ length: workers }, async (_, w) => {
  const page = await openPage();
  for (let f = w * per; f < Math.min(total, (w + 1) * per); f++) {
    await page.evaluate((t) => window.render(t), f / FPS);
    await stage(page).screenshot({ path: path.join(tmp, `f${String(f).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 93 });
    if (++done % 150 === 0) console.log(`${done}/${total}`);
  }
  await page.close();
}));
await browser.close();

const ff = ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(tmp, 'f%05d.jpg')];
if (audio) ff.push('-i', audio);
ff.push('-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart');
if (audio) ff.push('-c:a', 'aac', '-b:a', '192k', '-shortest');
ff.push(out);
await new Promise((res, rej) => spawn('ffmpeg', ff, { stdio: 'inherit' }).on('exit', (c) => (c ? rej(new Error('ffmpeg ' + c)) : res())));
fs.rmSync(tmp, { recursive: true, force: true });
console.log('ok →', out);
