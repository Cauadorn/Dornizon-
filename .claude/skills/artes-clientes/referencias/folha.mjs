// Folha de referências: junta imagens numa grade e salva um JPG (Chromium do Playwright, sem Python).
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs';
export async function folha(arquivos, destino, colunas = 6, largura = 300) {
  if (!arquivos.length) return;
  const imgs = arquivos.map((f) => `<figure><img src="data:image/jpeg;base64,${fs.readFileSync(f).toString('base64')}"><figcaption>${f.split('/').pop()}</figcaption></figure>`).join('');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: colunas * (largura + 12) + 12, height: 800 } });
  await p.setContent(`<style>body{margin:0;padding:12px;background:#fff;font:12px sans-serif;display:grid;
    grid-template-columns:repeat(${colunas},${largura}px);gap:12px;align-items:start}
    figure{margin:0}img{width:100%;display:block;border-radius:6px}figcaption{color:#666;margin-top:3px}</style>${imgs}`);
  await p.waitForLoadState('load');
  await p.screenshot({ path: destino, fullPage: true, type: 'jpeg', quality: 85 });
  await b.close();
}
