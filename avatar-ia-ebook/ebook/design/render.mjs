// Gera ebook.pdf (A4) a partir de ebook.html e confere se algum texto passou do fim da página.
//   node render.mjs              -> ebook.pdf
//   node render.mjs --previa 1,7 -> também salva previa-01.png, previa-07.png
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";

const { chromium } = createRequire(import.meta.url)("playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const iPrevia = args.indexOf("--previa");
const previas = iPrevia >= 0 ? args[iPrevia + 1].split(",").map(Number) : [];

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
await page.goto("file://" + path.join(aqui, "ebook.html"));
await page.evaluate(() => document.fonts.ready);

const problemas = await page.evaluate(() => {
  const out = [];
  document.querySelectorAll(".page").forEach((pg, i) => {
    const limite = pg.getBoundingClientRect().bottom - 50; // espaço do número da página
    pg.querySelectorAll("p, li, h2, h4, .dica, .stats").forEach((el) => {
      if (el.classList.contains("folio") || el.classList.contains("rodape-ia")) return;
      if (el.getBoundingClientRect().bottom > limite) out.push(`página ${i + 1}: "${el.textContent.trim().slice(0, 40)}"`);
    });
  });
  return out;
});
const fontes = await page.evaluate(() => [...document.fonts].filter((f) => f.status === "loaded").length);
console.log(`fontes carregadas: ${fontes}`);
console.log(problemas.length ? "PASSOU DO LIMITE:\n" + problemas.join("\n") : "nenhum texto passou do limite");

await page.pdf({ path: path.join(aqui, "ebook.pdf"), preferCSSPageSize: true, printBackground: true });

// Partes menores para importar no Canva (limite de elementos por PDF importado).
const PARTES = ["1-14", "15-31", "32-51"];
for (const [i, faixa] of PARTES.entries()) {
  await page.pdf({ path: path.join(aqui, `ebook-parte-${i + 1}.pdf`), preferCSSPageSize: true, printBackground: true,
    pageRanges: faixa });
}

for (const n of previas) {
  const el = (await page.$$(".page"))[n - 1];
  await el.screenshot({ path: path.join(aqui, `previa-${String(n).padStart(2, "0")}.png`) });
}
await browser.close();
