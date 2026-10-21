// Copy do briefing, lâmina por lâmina, exatamente como enviada pela Badauê.
// Únicas intervenções tipográficas: itálico em nomes indígenas, no nome científico
// (convenção de nomenclatura binomial) e na palavra "gingado" do slogan.
// `pos` posiciona o bloco de texto sobre a imagem de cada lâmina (px em 1080 × 1350).

export const LAMINAS = [
  {
    nome: '01_capa',
    pos: 'topo',
    html: `<h1 class="titulo capa">Como a <em>vitória&#8209;régia</em> virou um dos maiores símbolos da&nbsp;Amazônia?</h1>`,
  },
  {
    nome: '02',
    pos: 'topo-base',
    html: `<h2 class="titulo">A vitória&#8209;régia é uma das maiores plantas aquáticas do mundo e habita os rios amazônicos há milhares de&nbsp;anos.</h2>
      <p class="apoio base estreito">Muito antes de receber esse nome, ela já fazia parte da cultura e do cotidiano dos povos indígenas, que a conheciam como <em>uapé</em>, <em>jaçanã</em> ou <em>estrela das&nbsp;águas</em>.</p>`,
  },
  {
    nome: '03',
    pos: 'topo-base',
    html: `<h2 class="titulo">Foi a relação dos povos originários com a planta que deu origem a uma das lendas mais conhecidas do&nbsp;Brasil.</h2>
      <div class="base">
        <p class="apoio">Segundo a tradição indígena, Naiá mergulhou nas águas tentando alcançar Jaci, a lua. Comovida, Jaci a transformou em uma flor que desabrocha apenas durante a&nbsp;noite.</p>
        <p class="fecho">Mais do que uma lenda, essa história revela como natureza e cultura caminham juntas na&nbsp;Amazônia.</p>
      </div>`,
  },
  {
    nome: '04',
    pos: 'topo-base',
    html: `<h2 class="titulo">No século <span class="romano">XIX</span>, botânicos europeus ficaram fascinados pela imponência da&nbsp;planta.</h2>
      <p class="apoio base">Foi nesse período que ela recebeu o nome vitória&#8209;régia, em homenagem à Rainha Vitória. Mais tarde, seu nome científico passou a ser <em class="cientifico">Victoria amazonica</em>, reconhecendo sua&nbsp;origem.</p>`,
  },
  {
    nome: '05',
    pos: 'topo-base',
    html: `<h2 class="titulo">Além do simbolismo, a vitória&#8209;régia também impressiona pela engenharia da&nbsp;natureza.</h2>
      <p class="apoio base estreito">Suas folhas podem ultrapassar dois metros de diâmetro, suportar até 40&nbsp;kg quando o peso é distribuído e suas flores mudam do branco para o rosa após serem polinizadas durante a&nbsp;noite.</p>`,
  },
  {
    nome: '06',
    pos: 'topo',
    html: `<p class="abertura">Hoje, a vitória&#8209;régia representa muito mais do que a biodiversidade&nbsp;amazônica.</p>
      <h2 class="titulo grande">Ela reúne natureza, ciência, memória e ancestralidade em um único&nbsp;símbolo.</h2>
      <p class="apoio">Um lembrete de que alguns dos maiores ícones do Brasil nasceram da relação profunda entre os povos da floresta e o território que&nbsp;habitam.</p>`,
  },
  {
    nome: '07_encerramento',
    pos: 'centro',
    html: `<div class="assinatura">
        <div class="logo-grande">{{LOGO}}</div>
        <p class="slogan">Enaltecendo o <em>gingado</em> brasileiro.</p>
        <p class="site">www.alabadaue.com</p>
      </div>`,
  },
];
