const { chromium } = require('playwright');
(async () => {
  const [,, html, pdf] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + html, { waitUntil: 'networkidle' });
  await p.waitForTimeout(800);
  await p.pdf({ path: pdf, width: '297mm', height: '210mm', printBackground: true, preferCSSPageSize: true });
  await b.close();
  console.log('pdf', pdf);
})();
