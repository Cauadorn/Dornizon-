// servidor local simples (o fetch do meta.json não funciona em file://)
const http = require('node:http'), fs = require('node:fs'), path = require('node:path');
const T = { '.html': 'text/html', '.png': 'image/png', '.json': 'application/json', '.ttf': 'font/ttf', '.jpg': 'image/jpeg', '.js': 'text/javascript' };
http.createServer((q, r) => { const f = path.join(__dirname, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); } else { r.writeHead(200, { 'Content-Type': T[path.extname(f)] || 'application/octet-stream' }); r.end(d); } }); }).listen(8765);
