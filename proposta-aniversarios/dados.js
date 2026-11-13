/* Dados desta proposta. O resto do site (index.html, style.css, app.js) é o modelo e só lê o que está aqui. */
window.PROPOSTA = {
  numero: "002",
  data: "13.11.2026",
  validade: "Cada data fica reservada na agenda com o sinal de 30%.",
  cliente: "",                      // nome do cliente. Vazio: o topo mostra o título curto no lugar do nome.
  tituloCurto: "Dois aniversários",
  titulo: "Fotos e vídeo de duas datas em família",
  tituloDestaque: "duas datas",
  resumo:
    "O aniversário do seu filho, no sábado 20/02, e o da sua esposa, num day use com piscina. Você escolhe as datas e o que quer receber: só fotos, só vídeo ou os dois.",
  heroVideo: "assets/portfolio/topo-eventos.mp4",
  heroPoster: "assets/portfolio/topo-eventos.jpg",
  heroSelo: "Trabalho recente",
  faixa: ["Fotos tratadas", "Vídeo do dia", "Aniversário do filho", "Day use com piscina"],

  pedido: [
    { pediu: "Aniversário do seu filho", entrega: "Sábado, 20/02, das 12h às 17h. Cinco horas de cobertura, dentro de uma diária." },
    { pediu: "Aniversário da sua esposa", entrega: "Day use com piscina, das 09h às 18h. Nove horas de cobertura: uma diária e uma hora extra." },
    { pediu: "Fotos", entrega: "Câmera profissional com flash. As fotos saem tratadas, em alta resolução, por link." },
    { pediu: "Vídeos", entrega: "Câmera de cinema em 4K e um vídeo editado de cada data, na vertical, com corte, cor, som e trilha." }
  ],

  eventos: [
    {
      dia: "Sábado",
      data: "20/02",
      ano: 2027,
      nome: "Aniversário do seu filho",
      curto: "Aniversário do filho",
      local: "A confirmar",
      cobertura: "12h às 17h",
      horas: 5,
      nota: "Chego antes do meio-dia para preparar a câmera e a luz."
    },
    {
      dia: "Day use",
      data: "",
      semData: "Data a confirmar",
      nome: "Aniversário da sua esposa",
      curto: "Aniversário da esposa",
      local: "Day use com piscina",
      cobertura: "09h às 18h",
      horas: 9,
      nota: "Dia inteiro no local, da chegada ao fim da tarde."
    }
  ],

  equipe: [
    {
      nome: "Cauã Dorn",
      papel: "Direção, fotografia, vídeo e edição",
      texto:
        "Dirijo, fotografo, filmo e edito. São mais de 6 anos em direção de arte e audiovisual, com casamentos, debutantes, festas e making of. Nas duas datas, fico com a câmera de cinema e a fotografia. Depois, com o tratamento das fotos e a edição dos vídeos.",
      fotos: ["assets/equipe/caua-retrato.jpg", "assets/equipe/caua-palestra.jpg"],
      links: [
        { rotulo: "Instagram", url: "https://instagram.com/ohdorn" },
        { rotulo: "Behance", url: "https://www.behance.net/cauaalencar" },
        { rotulo: "Site", url: "https://cauadorn.com.br" }
      ]
    }
  ],

  equipamentos: [
    { nome: "Câmera de cinema", texto: "Captação em 4K com cor de cinema, para o vídeo de cada aniversário.", foto: "assets/equipamentos/camera.jpg" },
    { nome: "Lentes", texto: "Zoom Tamron 28-200 mm, da mesa do bolo ao detalhe sem trocar de lente, e lentes fixas Viltrox para pouca luz e fundo desfocado.", foto: "assets/equipamentos/lentes.jpg" },
    { nome: "Iluminação profissional", texto: "Bastão de LED (tocha) e luzes de LED, para as fotos e o vídeo não dependerem da luz do local.", foto: "assets/equipamentos/iluminacao.jpg" },
    { nome: "Áudio", texto: "Microfone sem fio, para gravar o parabéns e os recados com som limpo.", foto: "assets/equipamentos/audio.jpg" },
    { nome: "Gimbal", texto: "Estabilizador para os movimentos de câmera entre os convidados e na beira da piscina.", foto: "assets/equipamentos/gimbal.jpg" }
  ],
  extrasEquipamento: ["Câmera profissional com flash para as fotos", "Baterias e cartões para o dia inteiro"],

  portfolio: [
    { titulo: "Topo do Mundo · Eventos no Topo", tipo: "Evento", video: "assets/portfolio/topo-eventos.mp4", poster: "assets/portfolio/topo-eventos.jpg" },
    { titulo: "Topo do Mundo · Caipirinha", tipo: "Happy hour", video: "assets/portfolio/topo-caipirinha.mp4", poster: "assets/portfolio/topo-caipirinha.jpg" },
    { titulo: "Topo do Mundo · Fondue", tipo: "Restaurante", video: "assets/portfolio/topo-fondue.mp4", poster: "assets/portfolio/topo-fondue.jpg" }
  ],

  /* Preço: a diária cobre a captação por até 8 horas. Passou disso, hora extra proporcional (diária ÷ 8).
     Fotos e vídeo são valores à parte, por data. */
  preco: {
    diaria: 900,
    horasDiaria: 8,
    fotos: 300,     // tratamento e entrega das fotos, por data
    video: 300,     // um vídeo editado, por data
    sinal: 0.3,
    datas: [
      { id: "filho", rotulo: "Filho", nome: "o aniversário do seu filho (20/02)", eventos: [0] },
      { id: "esposa", rotulo: "Esposa", nome: "o aniversário da sua esposa (day use)", eventos: [1] },
      { id: "duas", rotulo: "As duas", nome: "as duas datas", eventos: [0, 1] }
    ],
    entregas: [
      { id: "fotos", rotulo: "Fotos", nome: "só fotos", fotos: true },
      { id: "video", rotulo: "Vídeo", nome: "só vídeo", video: true },
      { id: "completo", rotulo: "Fotos + vídeo", nome: "fotos e vídeo", fotos: true, video: true }
    ],
    padrao: { datas: "duas", entrega: "completo" },
    nota: "A diária cobre até 8 horas no local. O day use tem 9 horas, por isso entra 1 hora extra, proporcional à diária. Vídeo extra de cada data: R$ 300."
  },

  prazos: [
    { quando: "Na reserva", oque: "O sinal de 30% reserva a data na agenda." },
    { quando: "Sábado, 20/02", oque: "Aniversário do seu filho, das 12h às 17h." },
    { quando: "Dia do day use", oque: "Aniversário da sua esposa, das 09h às 18h." },
    { quando: "Depois de cada data", oque: "Fotos tratadas em até 3 dias úteis. Vídeo editado em até 5 dias úteis." },
    { quando: "Na entrega", oque: "O restante do valor." }
  ],

  condicoes: [
    "Sinal de 30% para reservar cada data. O restante na entrega.",
    "A diária cobre até 8 horas. Hora extra só com o seu OK, proporcional à diária.",
    "Fotos em alta resolução, entregues por link.",
    "Vídeo na vertical, pronto para o Instagram e o WhatsApp, com uma rodada de ajuste.",
    "Deslocamento e entrada no day use não estão no valor. Combinamos quando o local estiver definido.",
    "Você pode fechar uma data agora e a outra depois, pelos mesmos valores."
  ],

  contato: { whatsapp: "5511970696237" }
};
