// Pesquisa de referência no Pinterest (sem login) e folha de referências.
// uso: node pinterest.mjs "<busca>" <pasta-de-saida> [quantidade=24]
// Saída: pin-01.jpg ... e folha.jpg (todas lado a lado, para olhar de uma vez).
// O Pinterest abre a busca no Chromium headless com uma janela de login por cima, mas os pins carregam
// por baixo: o script lê os <img> do pinimg.com, troca a miniatura pela versão 736px e baixa.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import path from 'node:path';
import { folha } from './folha.mjs';

const [busca, saida, qtd = '24'] = process.argv.slice(2);
if (!busca || !saida) { console.log('uso: node pinterest.mjs "<busca>" <pasta> [quantidade]'); process.exit(1); }
fs.mkdirSync(saida, { recursive: true });
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36';
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1400, height: 1600 }, userAgent: UA, locale: 'pt-BR' });
await p.goto('https://br.pinterest.com/search/pins/?q=' + encodeURIComponent(busca), { waitUntil: 'domcontentloaded', timeout: 45000 });
const urls = new Set();
for (let i = 0; i < 6 && urls.size < +qtd; i++) {
  await p.waitForTimeout(2500);
  for (const s of await p.$$eval('img', (a) => a.map((x) => x.currentSrc || x.src))) {
    if (s.includes('i.pinimg.com') && !s.includes('/75x75') && !s.includes('/30x30')) urls.add(s.replace(/\/(236x|474x|170x|60x60)\//, '/736x/'));
  }
  await p.mouse.wheel(0, 1400);
}
await b.close();
const lista = [...urls].slice(0, +qtd), arquivos = [];
for (const [i, u] of lista.entries()) {
  try {
    const r = await fetch(u, { headers: { 'User-Agent': UA } });
    if (!r.ok) continue;
    const f = path.join(saida, `pin-${String(i + 1).padStart(2, '0')}.jpg`);
    fs.writeFileSync(f, Buffer.from(await r.arrayBuffer())); arquivos.push(f);
  } catch { /* pin que não baixou: segue */ }
}
fs.writeFileSync(path.join(saida, 'fontes.txt'), `busca: ${busca}\n` + lista.join('\n') + '\n');
await folha(arquivos, path.join(saida, 'folha.jpg'));
console.log(`${arquivos.length} pins em ${saida} (folha.jpg)`);
