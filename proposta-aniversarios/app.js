/* Monta a proposta a partir de window.PROPOSTA (dados.js) e liga a interação. */
(function () {
  const P = window.PROPOSTA;
  const $ = (id) => document.getElementById(id);
  const brl = (n) => "R$ " + n.toLocaleString("pt-BR", Number.isInteger(n) ? { maximumFractionDigits: 0 } : { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const calmo = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const mouse = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  const temGsap = !!(window.gsap && window.ScrollTrigger) && !calmo;

  /* ---------- conteúdo ---------- */
  const num = "Proposta nº " + P.numero + " · " + P.data;
  $("topo-num").textContent = num;
  $("rodape-num").textContent = num;
  const nome = P.cliente || P.tituloCurto;
  if (P.cliente) document.title = "Proposta · " + P.cliente;
  else $("hero-para").textContent = "Proposta de cobertura";
  $("cliente").innerHTML = nome.split(" ").map((p) => '<span class="palavra"><span>' + p + "</span></span>").join(" ");
  $("titulo").innerHTML = P.tituloDestaque ? P.titulo.replace(P.tituloDestaque, "<em>" + P.tituloDestaque + "</em>") : P.titulo;
  $("resumo").textContent = P.resumo;
  $("hero-selo").textContent = P.heroSelo;

  const hv = $("hero-video");
  hv.poster = P.heroPoster;
  hv.src = P.heroVideo;
  hv.play().catch(() => {});

  const ev = P.eventos;
  ev.forEach((e) => $("pilulas").appendChild(el("span", "pilula", (e.data ? e.dia + " " + e.data : e.dia) + " · " + e.cobertura)));
  $("pilulas").appendChild(el("span", "pilula pilula--presente", "Fotos e vídeo"));
  ["adesivo-a", "adesivo-b"].forEach((id, i) => {
    if (ev[i]) $(id).innerHTML = "<strong>" + (ev[i].data || ev[i].dia) + "</strong>" + (ev[i].data ? ev[i].dia + " · " : "") + ev[i].curto;
  });

  // faixa: a unidade tem nº par de itens, repetida 2x, para o loop não pular
  const unidade = P.faixa.length % 2 ? P.faixa.concat(P.faixa) : P.faixa;
  $("faixa").innerHTML = unidade.concat(unidade).map((t) => "<span>" + t + "</span>").join("");

  // 01 pedido
  P.pedido.forEach((p) => $("lista-pedido").appendChild(el("li", null,
    '<span class="rotulo">Você pediu</span><h3>' + p.pediu + "</h3><p>" + p.entrega + "</p>")));

  // 02 datas, com contagem de dias
  const hoje = new Date(); hoje.setHours(0, 0, 0, 0);
  const faltam = (e) => {
    if (!e.data) return "";
    const [d, m] = e.data.split("/").map(Number);
    const dias = Math.round((new Date(e.ano, m - 1, d) - hoje) / 86400000);
    if (dias < 0) return "";
    return dias === 0 ? "É hoje" : dias === 1 ? "É amanhã" : "Faltam " + dias + " dias";
  };
  ev.forEach((e) => {
    const f = faltam(e);
    $("eventos").appendChild(el("article", "evento",
      '<div class="evento__topo"><div class="evento__data' + (e.data ? "" : " evento__data--texto") + '"><strong>' + (e.data || e.semData) + '</strong><span class="rotulo">' + e.dia + "</span></div>" +
      (f ? '<span class="faltam">' + f + "</span>" : "") + "</div>" +
      "<h3>" + e.nome + "</h3>" +
      "<dl><dt>Local</dt><dd>" + e.local + "</dd><dt>Cobertura</dt><dd>" + e.cobertura + "</dd><dt>Duração</dt><dd>" + e.horas + " horas</dd></dl>" +
      '<p class="nota">' + e.nota + "</p>"));
  });

  // 03 quem faz
  P.equipe.forEach((m, i) => {
    const fotos = m.fotos.map((f) => '<figure><img loading="lazy" src="' + f + '" alt="' + m.nome + '"></figure>').join("");
    const links = m.links.map((l) => '<a href="' + l.url + '" target="_blank" rel="noopener">' + l.rotulo + " ↗</a>").join("");
    $("lista-equipe").appendChild(el("article", "pessoa",
      '<div class="pessoa__fotos">' + fotos + "</div>" +
      '<div><span class="rotulo">' + String(i + 1).padStart(2, "0") + "</span><h3>" + m.nome + "</h3>" +
      '<p class="pessoa__papel"><mark>' + m.papel + "</mark></p>" +
      '<p class="pessoa__texto">' + m.texto + '</p><div class="links">' + links + "</div></div>"));
  });

  // 04 equipamento
  P.equipamentos.forEach((q) => $("lista-equip").appendChild(el("article", "item",
    '<figure><img loading="lazy" src="' + q.foto + '" alt="' + q.nome + '"></figure><h3>' + q.nome + "</h3><p>" + q.texto + "</p>")));
  P.extrasEquipamento.forEach((x) => $("extras").appendChild(el("li", null, x)));

  // 05 trabalhos: passa o mouse, toca mudo; clica, liga o som; clica de novo, para
  const cursor = $("cursor");
  const cursorTexto = cursor.querySelector("span");
  if (!mouse) document.querySelector(".dica").textContent = "Toque no vídeo para assistir com som.";
  P.portfolio.forEach((v) => {
    const f = el("figure", "reel",
      '<video muted loop playsinline preload="none" poster="' + v.poster + '" src="' + v.video + '"></video>' +
      '<span class="reel__som">Mudo</span><figcaption><span>' + v.tipo + "</span>" + v.titulo + "</figcaption>");
    const vid = f.querySelector("video");
    const som = f.querySelector(".reel__som");
    const estado = () => {
      som.textContent = vid.muted ? "Mudo · clique para ouvir" : "Som ligado";
      cursorTexto.textContent = vid.paused ? "Assistir" : vid.muted ? "Ouvir" : "Pausar";
    };
    const tocar = () => { vid.play().catch(() => {}); f.classList.add("tocando"); estado(); };
    const parar = () => { vid.pause(); vid.muted = true; f.classList.remove("tocando"); estado(); };
    if (mouse) {
      f.addEventListener("mouseenter", () => { tocar(); cursor.classList.add("ligado"); });
      f.addEventListener("mouseleave", () => { parar(); cursor.classList.remove("ligado"); });
    }
    f.addEventListener("click", () => {
      if (vid.paused) { vid.muted = false; tocar(); }
      else if (vid.muted) { vid.muted = false; estado(); }
      else parar();
    });
    $("portfolio").appendChild(f);
  });

  /* ---------- 06 investimento: todos os cenários ---------- */
  const pr = P.preco;
  const horaExtra = pr.diaria / pr.horasDiaria;
  const extrasDe = (e) => pr.horaExtra ? Math.max(0, e.horas - pr.horasDiaria) : 0;
  // conta de um cenário: datas escolhidas x entrega escolhida
  function conta(d, t) {
    const evs = d.eventos.map((i) => ev[i]);
    const n = evs.length;
    const horas = evs.reduce((s, e) => s + extrasDe(e), 0);
    const linhas = [["Diária de captação · " + n + " × " + brl(pr.diaria), n * pr.diaria]];
    if (horas) linhas.push(["Hora extra no day use · " + horas + " × " + brl(horaExtra), horas * horaExtra]);
    if (t.fotos) linhas.push(["Fotos tratadas · " + n + " × " + brl(pr.fotos), n * pr.fotos]);
    if (t.video) linhas.push(["Vídeo editado · " + n + " × " + brl(pr.video), n * pr.video]);
    const cheio = linhas.reduce((s, l) => s + l[1], 0);
    const desconto = n > 1 ? (pr.descontoDuas || 0) : 0;
    if (desconto) linhas.push(["Desconto por fechar as duas datas", -desconto]);
    return { linhas, cheio, total: cheio - desconto };
  }

  // valores de referência
  const comExtra = ev.filter((e) => extrasDe(e) > 0);
  $("tabela").innerHTML =
    "<tr><td>Diária de captação<small>Por data</small></td><td>" + brl(pr.diaria) + "</td></tr>" +
    (comExtra.length ? "<tr><td>Hora extra<small>Proporcional à diária, por hora além das " + pr.horasDiaria + "</small></td><td>" + brl(horaExtra) + "</td></tr>" : "") +
    "<tr><td>Fotos tratadas<small>Valor à parte, por data</small></td><td>" + brl(pr.fotos) + "</td></tr>" +
    "<tr><td>Vídeo editado<small>Valor à parte, por data</small></td><td>" + brl(pr.video) + "</td></tr>" +
    (pr.descontoDuas ? "<tr><td>Fechando as duas datas<small>Desconto sobre o total</small></td><td>− " + brl(pr.descontoDuas) + "</td></tr>" : "");
  $("nota-tabela").textContent = pr.nota;

  // matriz com os nove cenários
  $("matriz").innerHTML =
    "<thead><tr><th></th>" + pr.datas.map((d) => '<th scope="col">' + d.rotulo + "</th>").join("") + "</tr></thead><tbody>" +
    pr.entregas.map((t) => '<tr><th scope="row">' + t.rotulo + "</th>" + pr.datas.map((d) =>
      '<td><button type="button" data-d="' + d.id + '" data-t="' + t.id + '">' + brl(conta(d, t).total) + "</button></td>").join("") + "</tr>").join("") +
    "</tbody>";

  // seletores em pílula
  const estado = { datas: pr.padrao.datas, entrega: pr.padrao.entrega };
  const segs = [];
  function seg(id, opcoes, chave) {
    const caixa = $(id);
    const pilula = el("span", "volumes__pilula");
    caixa.appendChild(pilula);
    opcoes.forEach((o) => {
      const b = el("button", null, o.rotulo);
      b.type = "button"; b.dataset.v = o.id; b.setAttribute("role", "radio");
      b.addEventListener("click", () => { estado[chave] = o.id; render(); });
      caixa.appendChild(b);
    });
    const mover = () => {
      caixa.querySelectorAll("button").forEach((b) => b.setAttribute("aria-checked", String(b.dataset.v === estado[chave])));
      const b = caixa.querySelector('[aria-checked="true"]');
      pilula.style.width = b.offsetWidth + "px";
      pilula.style.transform = "translateX(" + (b.offsetLeft - 5) + "px)";
    };
    segs.push(mover);
  }
  seg("seg-datas", pr.datas, "datas");
  seg("seg-entrega", pr.entregas, "entrega");
  $("matriz").addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    estado.datas = b.dataset.d; estado.entrega = b.dataset.t; render();
  });

  const totalEl = $("total-pacote");
  let totalAtual = 0;
  const contar = (de, para) => {
    totalEl.textContent = brl(para);
    if (calmo || !de || de === para || document.hidden) return;
    const t0 = performance.now(), dur = 550;
    const passo = (t) => {
      const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      totalEl.textContent = k < 1 ? brl(Math.round(de + (para - de) * e)) : brl(para);
      if (k < 1) requestAnimationFrame(passo);
    };
    requestAnimationFrame(passo);
  };

  function render() {
    const d = pr.datas.find((x) => x.id === estado.datas);
    const t = pr.entregas.find((x) => x.id === estado.entrega);
    const c = conta(d, t);
    const sinal = c.total * pr.sinal;
    const frase = t.nome.charAt(0).toUpperCase() + t.nome.slice(1) + " para " + d.nome;
    $("total-de").innerHTML = frase + (c.total < c.cheio ? " · de <s>" + brl(c.cheio) + "</s> por" : "");
    contar(totalAtual, c.total); totalAtual = c.total;
    $("resumo-preco").innerHTML =
      c.linhas.map((l) => "<dt>" + l[0] + "</dt><dd>" + (l[1] < 0 ? "− " + brl(-l[1]) : brl(l[1])) + "</dd>").join("") +
      '<dt class="forte">Sinal de ' + Math.round(pr.sinal * 100) + '% para reservar</dt><dd class="forte">' + brl(Math.round(sinal * 100) / 100) + "</dd>" +
      "<dt>Restante na entrega</dt><dd>" + brl(Math.round((c.total - sinal) * 100) / 100) + "</dd>";
    $("barra-total").textContent = t.rotulo + " · " + brl(c.total);
    document.querySelectorAll("#matriz button").forEach((b) =>
      b.setAttribute("aria-pressed", String(b.dataset.d === d.id && b.dataset.t === t.id)));
    segs.forEach((m) => m());
    const msg = "Oi, Cauã! Vi a proposta e quero reservar: " + t.nome + " para " + d.nome + ". Total de " + brl(c.total) + ".";
    const link = "https://wa.me/" + P.contato.whatsapp + "?text=" + encodeURIComponent(msg);
    ["cta", "cta-topo", "cta-barra"].forEach((id) => { $(id).href = link; });
  }
  render();
  window.addEventListener("resize", () => segs.forEach((m) => m()));
  if (document.fonts) document.fonts.ready.then(() => segs.forEach((m) => m()));

  // 07 prazos, 08 condições e fecho
  P.prazos.forEach((p) => $("linha").appendChild(el("li", null, "<strong>" + p.quando + "</strong><p>" + p.oque + "</p>")));
  P.condicoes.forEach((c) => $("lista-condicoes").appendChild(el("li", null, c)));
  $("validade").textContent = P.validade;

  /* ---------- interação ---------- */
  const topo = document.querySelector(".topo");
  const barra = $("cta-barra");
  const hero = $("inicio");
  const fecho = document.querySelector(".fecho");
  const prog = $("progresso");
  const aoRolar = () => {
    const y = window.scrollY, max = document.documentElement.scrollHeight - innerHeight;
    prog.style.transform = "scaleX(" + (max > 0 ? y / max : 0) + ")";
    topo.classList.toggle("rolou", y > 10);
    const noFecho = fecho.getBoundingClientRect().top < innerHeight * 0.85;
    barra.classList.toggle("ligada", y > hero.offsetHeight * 0.6 && !noFecho);
  };
  window.addEventListener("scroll", aoRolar, { passive: true });
  aoRolar();

  // menu marca a seção da vez
  const links = [...document.querySelectorAll(".menu a")];
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    if (e.isIntersecting) links.forEach((a) => a.classList.toggle("ativo", a.getAttribute("href") === "#" + e.target.id));
  }), { rootMargin: "-45% 0px -50% 0px" });
  links.forEach((a) => { const s = document.querySelector(a.getAttribute("href")); if (s) io.observe(s); });

  document.querySelectorAll('a[href^="#"]').forEach((a) => a.addEventListener("click", (e) => {
    const alvo = document.querySelector(a.getAttribute("href"));
    if (!alvo) return;
    e.preventDefault();
    alvo.scrollIntoView({ behavior: calmo ? "auto" : "smooth" });
  }));

  if (mouse) {
    window.addEventListener("mousemove", (e) => {
      cursor.style.left = e.clientX + "px";
      cursor.style.top = e.clientY + "px";
    }, { passive: true });
  }

  if (!temGsap) return;

  /* ---------- GSAP ---------- */
  const gsap = window.gsap;
  gsap.registerPlugin(window.ScrollTrigger);
  const ST = window.ScrollTrigger;

  // entrada do topo
  const intro = gsap.timeline({ defaults: { ease: "power4.out" } });
  intro.from(".hero__nome .palavra > span", { yPercent: 115, duration: 1.1, stagger: 0.08 })
    .from("#hero-reel", { opacity: 0, scale: 0.88, rotate: 4, duration: 1.3 }, 0.15)
    .from(".adesivo", { opacity: 0, scale: 0.6, duration: 0.8, stagger: 0.15, ease: "back.out(2)" }, 0.8);

  // vídeo do topo sobe devagar ao rolar
  gsap.to("#hero-reel", { yPercent: -10, ease: "none", scrollTrigger: { trigger: "#inicio", start: "top top", end: "bottom top", scrub: true } });
  gsap.to(".adesivo--a", { y: -60, ease: "none", scrollTrigger: { trigger: "#inicio", start: "top top", end: "bottom top", scrub: true } });
  gsap.to(".adesivo--b", { y: -120, ease: "none", scrollTrigger: { trigger: "#inicio", start: "top top", end: "bottom top", scrub: true } });

  if (mouse) {
    // inclina o vídeo com o mouse
    const reel = $("hero-reel");
    const rx = gsap.quickTo(reel, "rotationX", { duration: 0.6, ease: "power3.out" });
    const ry = gsap.quickTo(reel, "rotationY", { duration: 0.6, ease: "power3.out" });
    gsap.set(reel, { transformPerspective: 900 });
    hero.addEventListener("mousemove", (e) => {
      const r = hero.getBoundingClientRect();
      ry(((e.clientX - r.left) / r.width - 0.5) * 14);
      rx(-((e.clientY - r.top) / r.height - 0.5) * 10);
    });
    hero.addEventListener("mouseleave", () => { rx(0); ry(0); });

    // botão magnético
    document.querySelectorAll(".ima").forEach((b) => {
      const mx = gsap.quickTo(b, "x", { duration: 0.5, ease: "power3.out" });
      const my = gsap.quickTo(b, "y", { duration: 0.5, ease: "power3.out" });
      b.addEventListener("mousemove", (e) => {
        const r = b.getBoundingClientRect();
        mx((e.clientX - r.left - r.width / 2) * 0.35);
        my((e.clientY - r.top - r.height / 2) * 0.45);
      });
      b.addEventListener("mouseleave", () => { mx(0); my(0); });
    });
  }

  // fotos com parallax e linha do tempo que desenha ao rolar
  gsap.utils.toArray(".pessoa__fotos img").forEach((img, i) => {
    gsap.fromTo(img, { yPercent: -8 }, { yPercent: i % 2 ? 4 : 0, ease: "none", scrollTrigger: { trigger: img, start: "top bottom", end: "bottom top", scrub: true } });
  });
  gsap.fromTo("#risco", { scaleX: 0 }, { scaleX: 1, ease: "none", scrollTrigger: { trigger: ".linha-wrap", start: "top 80%", end: "bottom 55%", scrub: true } });

  window.addEventListener("load", () => ST.refresh());
})();
