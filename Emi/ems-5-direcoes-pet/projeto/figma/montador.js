const NM={q:'quadro',cartao:'cartão',sel:'seleção',i:'alça','sel-inline':'seleção',tag:'etiqueta @',estrela:'estrela em retícula',marcadagua:"marca d'água",adesivo:'adesivo',small:'hex',nome:'nome da fonte',span:'etiqueta emi',div:'grupo',dm:'me chama na dm',pergunta:'pergunta'};
const fn=r=>{let s={400:'Regular',500:'Medium',600:'SemiBold',700:'Bold'}[r.fw]||'Regular';if(r.it)s=s==='Regular'?'Italic':s+' Italic';if(['Bagel Fat One','Shrikhand','Graduate'].includes(r.ff))s='Regular';if(r.ff==='Instrument Serif')s=r.it?'Italic':'Regular';return{family:r.ff,style:s}};
const need=new Set();(function c(n){if(n.k==='t')n.runs.forEach(r=>r.ff&&need.add(JSON.stringify(fn(r))));(n.kids||[]).forEach(c)})(S);
await Promise.all([...need].map(s=>figma.loadFontAsync(JSON.parse(s))));
const so=c=>({type:'SOLID',color:{r:c[0],g:c[1],b:c[2]},opacity:c[3]});
const ef=a=>a.map(s=>({type:'DROP_SHADOW',color:{r:s.c[0],g:s.c[1],b:s.c[2],a:s.c[3]},offset:{x:s.x,y:s.y},radius:s.b,spread:0,visible:true,blendMode:'NORMAL'}));
const BL={multiply:'MULTIPLY',screen:'SCREEN'};const imgs=[];
const pos=(o,n)=>{if(n.m){const[a,b,c,d]=n.m,cx=n.x+n.w/2,cy=n.y+n.h/2;o.relativeTransform=[[a,c,cx-(a*n.w/2+c*n.h/2)],[b,d,cy-(b*n.w/2+d*n.h/2)]]}else{o.x=n.x;o.y=n.y}};
const com=(o,n)=>{if(n.op!=null)o.opacity=n.op;if(n.bl&&BL[n.bl])o.blendMode=BL[n.bl];if(n.sh)o.effects=ef(n.sh)};
function b(n,p){let o;
if(n.k==='f'){o=figma.createFrame();o.name=NM[n.n]||n.n;o.resize(Math.max(.01,n.w),Math.max(.01,n.h));o.fills=n.fill?[so(n.fill)]:[];o.clipsContent=!!n.clip;if(n.r)o.cornerRadius=n.r;if(n.rr){o.topLeftRadius=n.rr[0];o.topRightRadius=n.rr[1];o.bottomRightRadius=n.rr[2];o.bottomLeftRadius=n.rr[3]}if(n.st){o.strokes=[so(n.st.c)];o.strokeWeight=n.st.w;o.strokeAlign='INSIDE'}com(o,n);p.appendChild(o);pos(o,n);(n.kids||[]).forEach(k=>b(k,o))}
else if(n.k==='i'){o=figma.createRectangle();o.name=n.n;o.resize(n.w,n.h);o.fills=[{type:'SOLID',color:{r:.85,g:.85,b:.85}}];com(o,n);p.appendChild(o);pos(o,n);imgs.push([o.id,n.src+(n.flip?'#flip':'')])}
else if(n.k==='s'){o=figma.createNodeFromSvg(n.svg);o.name='vetor';o.fills=[];p.appendChild(o);pos(o,n)}
else if(n.k==='t'){o=figma.createText();const ch=n.runs.map(r=>r.s).join('');const f0=n.runs.find(r=>r.ff);o.fontName=fn(f0);o.fontSize=f0.fs;o.characters=ch;let i=0;
for(const r of n.runs){const L=r.s.length;if(r.ff&&L){o.setRangeFontName(i,i+L,fn(r));o.setRangeFontSize(i,i+L,r.fs);o.setRangeFills(i,i+L,[so(r.c)]);if(r.ls)o.setRangeLetterSpacing(i,i+L,{unit:'PIXELS',value:r.ls})}i+=L}
if(n.lh)o.lineHeight={unit:'PIXELS',value:n.lh};o.textAlignHorizontal={L:'LEFT',C:'CENTER',R:'RIGHT'}[n.al];if(n.st){o.strokes=[so(n.st.c)];o.strokeWeight=n.st.w;o.strokeAlign='OUTSIDE'}com(o,n);p.appendChild(o);
const quebras=(ch.match(/\n/g)||[]).length+1;
if(n.linhas>quebras){o.textAutoResize='HEIGHT';o.resize(n.w+2,o.height);o.x=n.x-1}else{o.textAutoResize='WIDTH_AND_HEIGHT';o.x=n.al==='C'?n.x+n.w/2-o.width/2:n.al==='R'?n.x+n.w-o.width:n.x}o.y=n.y}
return o}
const top=b(S,figma.currentPage);top.x=IDX*1180;top.y=0;top.clipsContent=true;
return{frame:top.id,name:top.name,imgs};
