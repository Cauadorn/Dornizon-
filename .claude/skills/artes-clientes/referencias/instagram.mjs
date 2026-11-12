// Baixa as lâminas de um carrossel público do Instagram e monta a folha.
// uso: node instagram.mjs <link-do-post> <pasta-de-saida>
// Sem login o Instagram mostra o post; cada ?img_index=N carrega 2 ou 3 lâminas em 1080px.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import path from 'node:path';
import { folha } from './folha.mjs';

const [link, saida] = process.argv.slice(2);
if (!link || !saida) { console.log('uso: node instagram.mjs <link-do-post> <pasta>'); process.exit(1); }
fs.mkdirSync(saida, { recursive: true });
const base = link.split('?')[0].replace(/\/?$/, '/');
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1280, height: 1400 }, userAgent: UA, locale: 'pt-BR' });
const vistas = new Map();
for (let i = 1; i <= 20; i += 2) {
  await p.goto(`${base}?img_index=${i}`, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
  await p.waitForTimeout(2000);
  const antes = vistas.size;
  for (const [s, alt] of await p.$$eval('img', (a) => a.filter((x) => x.naturalWidth >= 1000).map((x) => [x.src, x.alt || '']))) {
    const k = s.split('?')[0]; if (!vistas.has(k)) vistas.set(k, { s, alt });
  }
  if (i > 1 && vistas.size === antes) break;     // acabou o carrossel
}
await b.close();
const arquivos = [];
for (const [i, v] of [...vistas.values()].entries()) {
  const r = await fetch(v.s, { headers: { 'User-Agent': UA } });
  if (!r.ok) continue;
  const f = path.join(saida, `lamina-${String(i + 1).padStart(2, '0')}.jpg`);
  fs.writeFileSync(f, Buffer.from(await r.arrayBuffer())); arquivos.push(f);
}
fs.writeFileSync(path.join(saida, 'fontes.txt'), `post: ${link}\n` + [...vistas.values()].map((v) => v.alt).join('\n---\n') + '\n');
await folha(arquivos, path.join(saida, 'folha.jpg'), 7);
console.log(`${arquivos.length} lâminas em ${saida} (folha.jpg; textos alternativos em fontes.txt)`);
