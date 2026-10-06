import React, {useEffect, useState} from 'react';
import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  OffthreadVideo,
  Sequence,
  continueRender,
  delayRender,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
} from 'remotion';
import wordsData from './words.json';

export const FPS = 24;
const OFF = 1.5; // seconds of picture before the narration starts
const W = 1920;
const H = 1080;
const BAR = 138; // 2.39:1 letterbox inside 16:9
const IVORY = '#FFFBDE';
const VIOLET = '#6225D8';

/** narration seconds -> composition frame */
const f = (n: number) => Math.round((n + OFF) * FPS);
export const TOTAL_FRAMES = f(51.6);

type Word = {w: string; s: number; e: number};
const WORDS = wordsData as Word[];

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const ease = Easing.bezier(0.65, 0, 0.35, 1);
const easeOut = Easing.bezier(0.16, 1, 0.3, 1);

/* ------------------------------------------------------------------ fonts */
const FontLoader: React.FC = () => {
  const [handle] = useState(() => delayRender('fonts'));
  useEffect(() => {
    const faces = [
      new FontFace('Serif', `url(${staticFile('fonts/InstrumentSerif-Regular.ttf')})`),
      new FontFace('Serif', `url(${staticFile('fonts/InstrumentSerif-Italic.ttf')})`, {style: 'italic'}),
      new FontFace('Sans', `url(${staticFile('fonts/Inter.ttf')})`, {weight: '100 900'}),
    ];
    Promise.all(faces.map((ff) => ff.load()))
      .then((loaded) => {
        loaded.forEach((ff) => (document as any).fonts.add(ff));
        continueRender(handle);
      })
      .catch(() => continueRender(handle));
  }, [handle]);
  return null;
};

/* ---------------------------------------------------- motion-blur filters */
const BLUR_LEVELS = [0, 8, 18, 32, 55, 85];
const BlurDefs: React.FC = () => (
  <svg width="0" height="0" style={{position: 'absolute'}}>
    <defs>
      {BLUR_LEVELS.slice(1).map((b) => (
        <filter key={b} id={`mbx${b}`} x="-20%" y="-5%" width="140%" height="110%">
          <feGaussianBlur stdDeviation={`${b} 0`} />
        </filter>
      ))}
      {BLUR_LEVELS.slice(1).map((b) => (
        <filter key={'y' + b} id={`mby${b}`} x="-5%" y="-20%" width="110%" height="140%">
          <feGaussianBlur stdDeviation={`0 ${b}`} />
        </filter>
      ))}
    </defs>
  </svg>
);
const dirBlur = (amount: number, axis: 'x' | 'y') => {
  let pick = 0;
  for (const b of BLUR_LEVELS) if (amount >= b) pick = b;
  return pick === 0 ? 'none' : `url(#mb${axis}${pick})`;
};

/* ------------------------------------------------------------------ shots */
type Trans = 'cut' | 'fade' | 'whip' | 'whipUp' | 'flip' | 'zoom' | 'iris' | 'push3d';
type Move = {
  s?: [number, number];
  ry?: [number, number];
  rx?: [number, number];
  x?: [number, number];
  y?: [number, number];
};
const T = 9; // transition length in frames

type ShotDef = {
  id: string;
  clip: string;
  a: number; // narration second where the shot starts
  b: number; // narration second where the next shot takes over
  srcStart?: number;
  enter?: Trans;
  exit?: Trans;
  move?: Move;
  vol?: number;
  kodak?: boolean; // show inside a 3D film gate instead of full frame
};

const lerp = (p: number, r?: [number, number], d = 0) => (r ? r[0] + (r[1] - r[0]) * p : d);

function enterStyle(t: Trans | undefined, p: number): React.CSSProperties {
  const q = easeOut(p);
  switch (t) {
    case 'fade':
      return {opacity: q};
    case 'whip':
      return {transform: `translateX(${(1 - q) * W * 0.9}px)`, filter: dirBlur((1 - p) * 90, 'x')};
    case 'whipUp':
      return {transform: `translateY(${(1 - q) * H * 0.9}px)`, filter: dirBlur((1 - p) * 90, 'y')};
    case 'flip':
      return {transform: `rotateY(${(1 - q) * 80}deg)`, transformOrigin: '0% 50%', opacity: interpolate(p, [0, 0.3], [0.4, 1], clamp)};
    case 'zoom':
      return {transform: `scale(${1.5 - 0.5 * q})`, opacity: q, filter: `blur(${(1 - q) * 22}px)`};
    case 'iris':
      return {clipPath: `circle(${q * 120}% at 50% 50%)`};
    case 'push3d':
      return {transform: `translateZ(${-900 * (1 - q)}px) rotateY(${(1 - q) * -35}deg)`, opacity: q};
    default:
      return {};
  }
}
function exitStyle(t: Trans | undefined, p: number): React.CSSProperties {
  const q = ease(p);
  switch (t) {
    case 'whip':
      return {transform: `translateX(${-q * W * 0.9}px)`, filter: dirBlur(p * 90, 'x')};
    case 'whipUp':
      return {transform: `translateY(${-q * H * 0.9}px)`, filter: dirBlur(p * 90, 'y')};
    case 'flip':
      return {transform: `rotateY(${-q * 80}deg)`, transformOrigin: '100% 50%', opacity: 1 - q * 0.6};
    case 'zoom':
      return {transform: `scale(${1 + q * 0.9})`, opacity: 1 - q, filter: `blur(${q * 22}px)`};
    case 'push3d':
      return {transform: `translateZ(${600 * q}px) rotateY(${q * 30}deg)`, opacity: 1 - q};
    default:
      return {};
  }
}

const Video: React.FC<{clip: string; srcStart?: number; vol?: number; style?: React.CSSProperties}> = ({
  clip,
  srcStart = 0,
  vol = 0.1,
  style,
}) => (
  <OffthreadVideo
    src={staticFile(`clips/${clip}.mp4`)}
    startFrom={Math.round(srcStart * FPS)}
    volume={vol}
    style={{width: '100%', height: '100%', objectFit: 'cover', ...style}}
  />
);

/** A 4:3 Kodak clip shown like a projected memory: rounded gate, date stamp. */
const KodakGate: React.FC<{clip: string; srcStart?: number; width: number; vol?: number; glow?: number}> = ({
  clip,
  srcStart = 0,
  width,
  vol = 0.04,
  glow = 0.35,
}) => {
  const h = (width * 3) / 4;
  return (
    <div
      style={{
        width,
        height: h,
        padding: width * 0.018,
        background: '#0b0a09',
        borderRadius: width * 0.03,
        boxShadow: `0 40px 120px rgba(0,0,0,0.7), 0 0 ${width * 0.12}px rgba(255,190,140,${glow * 0.25})`,
        boxSizing: 'border-box',
        position: 'relative',
      }}
    >
      <div style={{width: '100%', height: '100%', borderRadius: width * 0.022, overflow: 'hidden', position: 'relative'}}>
        <Video clip={clip} srcStart={srcStart} vol={vol} />
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)',
          }}
        />
        <div
          style={{
            position: 'absolute',
            right: width * 0.045,
            bottom: width * 0.035,
            fontFamily: 'monospace',
            fontWeight: 700,
            fontSize: width * 0.034,
            letterSpacing: width * 0.004,
            color: '#ff9a3c',
            textShadow: '0 0 6px rgba(255,120,30,0.9)',
            opacity: 0.85,
          }}
        >
          10 06 '26
        </div>
      </div>
    </div>
  );
};

const Shot: React.FC<{d: ShotDef; nextEnter?: Trans}> = ({d}) => {
  const frame = useCurrentFrame(); // local to the Sequence
  const start = f(d.a);
  const end = f(d.b);
  const len = end - start;
  const pMove = interpolate(frame, [0, len + T], [0, 1], clamp);
  const m = d.move ?? {};
  const camera: React.CSSProperties = {
    transform: `translate3d(${lerp(ease(pMove), m.x)}px, ${lerp(ease(pMove), m.y)}px, 0) rotateY(${lerp(
      ease(pMove),
      m.ry,
    )}deg) rotateX(${lerp(ease(pMove), m.rx)}deg) scale(${lerp(ease(pMove), m.s, 1.06)})`,
  };
  const pIn = interpolate(frame, [0, T], [0, 1], clamp);
  const pOut = interpolate(frame, [len, len + T], [0, 1], clamp);
  const eIn = d.enter && d.enter !== 'cut' ? enterStyle(d.enter, pIn) : {};
  const eOut = d.exit && d.exit !== 'cut' ? exitStyle(d.exit, pOut) : {};

  const inner = d.kodak ? (
    <AbsoluteFill style={{background: '#050505', alignItems: 'center', justifyContent: 'center'}}>
      <div style={{position: 'absolute', inset: 0, filter: 'blur(60px) brightness(0.35)', transform: 'scale(1.3)'}}>
        <Video clip={d.clip} srcStart={d.srcStart} vol={0} />
      </div>
      <div style={{...camera}}>
        <KodakGate clip={d.clip} srcStart={d.srcStart} width={1000} vol={d.vol ?? 0.04} />
      </div>
    </AbsoluteFill>
  ) : (
    <AbsoluteFill style={{...camera}}>
      <Video clip={d.clip} srcStart={d.srcStart} vol={d.vol ?? 0.1} />
    </AbsoluteFill>
  );

  return (
    <AbsoluteFill style={{perspective: 1800, overflow: 'hidden'}}>
      <AbsoluteFill style={{...eIn, transformStyle: 'preserve-3d'}}>
        <AbsoluteFill style={{...eOut, overflow: 'hidden', background: '#000'}}>{inner}</AbsoluteFill>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/* -------------------------------------------------- 3D memory wall scenes */
type Card = {clip: string; x: number; y: number; z: number; ry: number; w: number; srcStart?: number};
const MemoryWall: React.FC<{cards: Card[]; len: number; camFrom: number; camTo: number; dim?: number; driftY?: number}> = ({
  cards,
  len,
  camFrom,
  camTo,
  dim = 0,
  driftY = 8,
}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, len], [0, 1], clamp);
  const camZ = camFrom + (camTo - camFrom) * Easing.bezier(0.33, 0, 0.2, 1)(p);
  const rotY = interpolate(p, [0, 1], [-driftY, driftY]);
  return (
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 60%, #1a1310 0%, #050404 70%)', perspective: 1300}}>
      <AbsoluteFill style={{transformStyle: 'preserve-3d', transform: `translateZ(${camZ}px) rotateY(${rotY}deg)`}}>
        {cards.map((c, i) => (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: W / 2 - c.w / 2,
              top: H / 2 - (c.w * 3) / 8,
              transform: `translate3d(${c.x}px, ${c.y}px, ${c.z}px) rotateY(${c.ry}deg)`,
            }}
          >
            <KodakGate clip={c.clip} srcStart={c.srcStart} width={c.w} />
          </div>
        ))}
      </AbsoluteFill>
      {dim > 0 && <AbsoluteFill style={{background: `rgba(0,0,0,${dim})`}} />}
    </AbsoluteFill>
  );
};

/* -------------------------------------------------------- motion lettering */
const OffsetCtx = React.createContext(0);
const wordIn = (frame: number, at: number, dur = 8) => interpolate(frame, [f(at), f(at) + dur], [0, 1], clamp);

const Reveal: React.FC<{at: number; children: React.ReactNode; style?: React.CSSProperties; rise?: number}> = ({
  at,
  children,
  style,
  rise = 28,
}) => {
  const frame = useCurrentFrame() + React.useContext(OffsetCtx);
  const p = easeOut(wordIn(frame, at, 10));
  return (
    <span
      style={{
        display: 'inline-block',
        opacity: p,
        transform: `translateY(${(1 - p) * rise}px)`,
        filter: `blur(${(1 - p) * 10}px)`,
        ...style,
      }}
    >
      {children}
    </span>
  );
};

/** "teve dia que eu ___" slot machine over the Kodak wall. */
const SlotLettering: React.FC = () => {
  const frame = useCurrentFrame();
  const items = [
    {t: 'duvidei.', at: 12.1},
    {t: 'achei bobagem insistir.', at: 13.42},
    {t: 'quase guardei tudo.', at: 15.56},
  ];
  let idx = 0;
  items.forEach((it, i) => {
    if (frame >= f(it.at) - 2) idx = i;
  });
  const sp = (i: number) => spring({frame: frame - (f(items[i].at) - 2), fps: FPS, config: {damping: 18, mass: 0.7}});
  let y = 0;
  for (let i = 1; i < items.length; i++) y += sp(i);
  const LINE = 132;
  const show = interpolate(frame, [f(11.5), f(11.5) + 8, f(16.15), f(16.15) + 8], [0, 1, 1, 0], clamp);
  return (
    <AbsoluteFill style={{opacity: show}}>
      <div style={{position: 'absolute', left: 230, top: 330, color: IVORY}}>
        <div style={{fontFamily: 'Sans', fontWeight: 500, fontSize: 54, letterSpacing: -1, lineHeight: 1.1}}>
          <Reveal at={11.56}>teve</Reveal> <Reveal at={11.74}>dia</Reveal>
          <br />
          <Reveal at={11.88}>que</Reveal> <Reveal at={12.0}>eu</Reveal>
        </div>
        <div style={{height: LINE * 1.05, overflow: 'visible', position: 'relative', marginTop: 6}}>
          <div style={{transform: `translateY(${-y * LINE}px)`}}>
            {items.map((it, i) => {
              const a = i === idx ? 1 : 0.16;
              const vis = frame >= f(it.at) - 2 || i === idx + 1 ? 1 : 0;
              return (
                <div
                  key={i}
                  style={{
                    height: LINE,
                    fontFamily: 'Serif',
                    fontStyle: 'italic',
                    fontSize: 128,
                    lineHeight: `${LINE}px`,
                    whiteSpace: 'nowrap',
                    opacity: a * (vis ? 1 : 0.6) * (frame >= f(items[0].at) - 2 ? 1 : 0),
                    transition: 'none',
                  }}
                >
                  {it.t}
                </div>
              );
            })}
          </div>
        </div>
      </div>
      <div
        style={{
          position: 'absolute',
          left: 230 - 46,
          top: 330 + 128 + 52,
          width: 18,
          height: 18,
          borderRadius: 9,
          background: VIOLET,
          boxShadow: '0 0 24px rgba(98,37,216,0.9)',
          opacity: frame >= f(12.1) - 2 ? 1 : 0,
        }}
      />
    </AbsoluteFill>
  );
};

/** Violet block: "ela nunca ia vir / de fora." */
const ColorBlock: React.FC<{len: number}> = ({len}) => {
  const frame = useCurrentFrame();
  const grow = easeOut(interpolate(frame, [0, 12], [0, 1], clamp));
  const leave = ease(interpolate(frame, [len - 8, len + 4], [0, 1], clamp));
  const g = (at: number) => f(at) - f(22.75);
  const big = (at: number) => easeOut(interpolate(frame, [g(at), g(at) + 12], [0, 1], clamp));
  return (
    <AbsoluteFill
      style={{
        clipPath: `circle(${grow * 130}% at 50% 52%)`,
        transform: `translateY(${-leave * H}px)`,
        filter: dirBlur(leave * 70 * (1 - leave) * 4, 'y'),
      }}
    >
      <AbsoluteFill style={{background: VIOLET}} />
      <AbsoluteFill
        style={{
          background: 'radial-gradient(ellipse at 30% 20%, rgba(255,255,255,0.12), rgba(0,0,0,0) 60%)',
        }}
      />
      <div style={{position: 'absolute', left: 240, top: 300, color: IVORY}}>
        <div style={{fontFamily: 'Sans', fontWeight: 500, fontSize: 58, letterSpacing: -1}}>
          <Reveal at={22.88}>ela</Reveal> <Reveal at={23.08}>nunca</Reveal> <Reveal at={23.46}>ia</Reveal>{' '}
          <Reveal at={23.62}>vir</Reveal>
        </div>
        <div style={{fontFamily: 'Serif', fontSize: 270, lineHeight: 1, marginTop: 10, whiteSpace: 'nowrap'}}>
          <span style={{opacity: big(23.8), display: 'inline-block', transform: `translateY(${(1 - big(23.8)) * 40}px)`}}>de </span>
          <span
            style={{
              fontStyle: 'italic',
              opacity: big(24.04),
              display: 'inline-block',
              letterSpacing: `${(1 - big(24.04)) * 40}px`,
              filter: `blur(${(1 - big(24.04)) * 14}px)`,
            }}
          >
            fora
          </span>
          <span
            style={{
              display: 'inline-block',
              width: 34,
              height: 34,
              borderRadius: 17,
              background: IVORY,
              marginLeft: 12,
              transform: `scale(${big(24.3)})`,
            }}
          />
        </div>
      </div>
    </AbsoluteFill>
  );
};

/** Overlay lettering on top of footage. */
const Overlay: React.FC<{children: React.ReactNode; from: number; to: number}> = ({children, from, to}) => {
  const frame = useCurrentFrame();
  const len = f(to) - f(from);
  const o = interpolate(frame, [len - 8, len], [1, 0], clamp);
  return (
    <AbsoluteFill style={{opacity: o}}>
      <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.0) 60%)'}} />
      {children}
    </AbsoluteFill>
  );
};

const FinalWord: React.FC<{len: number}> = ({len}) => {
  const frame = useCurrentFrame();
  const word = 'coragem';
  const base = f(47.32) - f(47.2);
  const out = interpolate(frame, [len - 20, len], [1, 0], clamp);
  return (
    <AbsoluteFill style={{background: '#050404', alignItems: 'center', justifyContent: 'center', opacity: out}}>
      <div style={{fontFamily: 'Serif', fontStyle: 'italic', fontSize: 300, color: IVORY, whiteSpace: 'nowrap'}}>
        {word.split('').map((ch, i) => {
          const p = easeOut(interpolate(frame, [base + i * 2, base + i * 2 + 14], [0, 1], clamp));
          return (
            <span
              key={i}
              style={{display: 'inline-block', opacity: p, transform: `translateY(${(1 - p) * 60}px)`, filter: `blur(${(1 - p) * 12}px)`}}
            >
              {ch}
            </span>
          );
        })}
        <span
          style={{
            display: 'inline-block',
            width: 40,
            height: 40,
            borderRadius: 20,
            background: VIOLET,
            marginLeft: 16,
            boxShadow: '0 0 40px rgba(98,37,216,0.9)',
            transform: `scale(${spring({frame: frame - base - 20, fps: FPS, config: {damping: 9}})})`,
          }}
        />
      </div>
      <div
        style={{
          position: 'absolute',
          bottom: BAR + 60,
          fontFamily: 'Sans',
          fontSize: 22,
          letterSpacing: 6,
          color: IVORY,
          opacity: interpolate(frame, [base + 50, base + 64], [0, 0.55], clamp),
        }}
      >
        @ITSEMSDESIGN
      </div>
    </AbsoluteFill>
  );
};

/* -------------------------------------------------------------- subtitles */
const NO_SUBS: [number, number][] = [
  [11.4, 16.25],
  [22.75, 25.65],
  [30.85, 33.3],
  [38.9, 40.85],
  [47.2, 60],
];
type Chunk = {t: string; s: number; e: number};
const CHUNKS: Chunk[] = (() => {
  const out: Chunk[] = [];
  let cur: Word[] = [];
  const flush = () => {
    if (!cur.length) return;
    out.push({t: cur.map((w) => w.w).join(' '), s: cur[0].s, e: cur[cur.length - 1].e});
    cur = [];
  };
  WORDS.forEach((w, i) => {
    const gap = i > 0 ? w.s - WORDS[i - 1].e : 0;
    if (gap > 0.5) flush();
    cur.push(w);
    if (/[,.]$/.test(w.w) && cur.length >= 3) flush();
    else if (cur.length >= 7) flush();
  });
  flush();
  return out;
})();

const Subtitles: React.FC = () => {
  const frame = useCurrentFrame();
  const n = frame / FPS - OFF;
  const c = CHUNKS.find((ch) => n >= ch.s - 0.05 && n <= ch.e + 0.35);
  if (!c) return null;
  if (NO_SUBS.some(([a, b]) => n >= a && n <= b)) return null;
  const o = interpolate(n, [c.s - 0.05, c.s + 0.12], [0, 1], clamp);
  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        bottom: 0,
        height: BAR,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'Sans',
        fontWeight: 400,
        fontSize: 30,
        letterSpacing: 0.3,
        color: IVORY,
        opacity: o * 0.92,
      }}
    >
      {c.t.replace(/[,.]$/, '').toLowerCase()}
    </div>
  );
};

/* ------------------------------------------------------------ film finish */
const FilmFinish: React.FC = () => {
  const frame = useCurrentFrame();
  const open = easeOut(interpolate(frame, [4, 34], [0, 1], clamp));
  const close = ease(interpolate(frame, [TOTAL_FRAMES - 14, TOTAL_FRAMES - 1], [0, 1], clamp));
  const bar = BAR + (H / 2 - BAR) * (1 - open) + (H / 2 - BAR) * close;
  const g = frame % 8;
  const flicker = 0.035 + 0.025 * Math.sin(frame * 2.3) * Math.sin(frame * 0.71);
  // warm light leaks at a few scene changes
  const leaks = [f(10.95), f(25.7), f(40.85)];
  const leak = Math.max(...leaks.map((l) => interpolate(frame, [l - 6, l, l + 14], [0, 1, 0], clamp)));
  return (
    <>
      <AbsoluteFill
        style={{
          background: 'radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 58%, rgba(0,0,0,0.5) 100%)',
          pointerEvents: 'none',
        }}
      />
      {leak > 0 && (
        <AbsoluteFill
          style={{
            mixBlendMode: 'screen',
            opacity: leak * 0.85,
            background: `radial-gradient(circle at ${20 + leak * 40}% 40%, rgba(255,140,60,0.95) 0%, rgba(255,60,40,0.45) 25%, rgba(0,0,0,0) 60%)`,
          }}
        />
      )}
      <AbsoluteFill style={{background: `rgba(0,0,0,${flicker})`}} />
      <AbsoluteFill style={{mixBlendMode: 'overlay', opacity: 0.55}}>
        <Img
          src={staticFile(`grain/g${g}.png`)}
          style={{
            width: W * 1.1,
            height: H * 1.1,
            transform: `translate(${-((frame * 37) % 90)}px, ${-((frame * 53) % 50)}px)`,
            imageRendering: 'pixelated',
          }}
        />
      </AbsoluteFill>
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: bar, background: '#000'}} />
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: bar, background: '#000'}} />
      <Subtitles />
    </>
  );
};

/* -------------------------------------------------------------- shot list */
const SHOTS: ShotDef[] = [
  {id: 's1', clip: 'plataforma-espera', a: -1.5, b: 3.7, exit: 'whip', move: {s: [1.22, 1.08], ry: [7, -2], x: [60, -20]}},
  {id: 's2', clip: 'carta-livraria', a: 3.7, b: 6.0, srcStart: 0.3, enter: 'whip', exit: 'flip', move: {s: [1.08, 1.18], rx: [4, 0]}},
  {id: 's3', clip: 'trem-passando-ela', a: 6.0, b: 7.95, srcStart: 0.2, enter: 'flip', exit: 'cut', move: {s: [1.1, 1.16], ry: [-4, 2]}},
  {id: 's4', clip: 'ela-esperando-tela', a: 7.95, b: 10.95, enter: 'fade', exit: 'zoom', move: {s: [1.06, 1.2], x: [-30, 30]}},
  // 10.95 -> 16.3 memory wall + slot lettering (component scene)
  {id: 's6', clip: 'k-escada-metro', a: 16.3, b: 18.95, enter: 'push3d', exit: 'whipUp', kodak: true, move: {s: [0.92, 1.08], ry: [-14, 6], rx: [6, -2]}},
  {id: 's7', clip: 'portas-fechando', a: 18.95, b: 21.15, srcStart: 0.3, enter: 'whipUp', exit: 'cut', move: {s: [1.05, 1.14]}},
  {id: 's8', clip: 'rosto-virando', a: 21.15, b: 22.75, srcStart: 0.4, enter: 'cut', exit: 'cut', move: {s: [1.08, 1.0]}},
  // 22.75 -> 25.7 violet block (component scene)
  {id: 's10', clip: 'caua-desenhando', a: 25.65, b: 28.2, srcStart: 0.3, enter: 'cut', exit: 'flip', move: {s: [1.25, 1.1], rx: [14, 4], ry: [-6, 4]}},
  {id: 's11', clip: 'lapis-close', a: 28.2, b: 29.35, enter: 'flip', exit: 'whip', move: {s: [1.1, 1.2]}},
  {id: 's12', clip: 'ela-livraria', a: 29.35, b: 31.0, srcStart: 0.2, enter: 'whip', exit: 'fade', move: {s: [1.06, 1.14], ry: [5, -3]}},
  {id: 's13', clip: 'livro-bras-cubas', a: 31.0, b: 33.3, srcStart: 0.2, enter: 'fade', exit: 'whip', move: {s: [1.12, 1.22], ry: [-8, 4], rx: [6, 0]}},
  {id: 's14', clip: 'homem-trem', a: 33.3, b: 35.95, enter: 'whip', exit: 'push3d', move: {s: [1.06, 1.16], x: [40, -40]}},
  {id: 's15', clip: 'k-banco-monica', a: 35.95, b: 38.05, srcStart: 0.3, enter: 'push3d', exit: 'zoom', kodak: true, move: {s: [0.9, 1.04], ry: [16, -8]}},
  {id: 's16', clip: 'maos-calma', a: 38.05, b: 38.95, srcStart: 0.2, enter: 'zoom', exit: 'cut', move: {s: [1.1, 1.06]}},
  {id: 's17', clip: 'ela-vira-sorri', a: 38.95, b: 40.85, srcStart: 0.4, enter: 'cut', exit: 'zoom', move: {s: [1.14, 1.06]}},
  // 40.85 -> 45.55 memory wall 2
  {id: 's19', clip: 'final-sorriso', a: 45.55, b: 47.3, srcStart: 0.4, enter: 'iris', exit: 'fade', move: {s: [1.12, 1.04], ry: [3, -2]}},
];

const WALL1: Card[] = [
  {clip: 'k-paulista-placa', x: -560, y: -60, z: -300, ry: 24, w: 760, srcStart: 0.5},
  {clip: 'k-masp-1867', x: 520, y: 40, z: -700, ry: -22, w: 820},
  {clip: 'k-escada-metro', x: -60, y: 260, z: -1400, ry: 6, w: 760},
  {clip: 'k-paulista-placa', x: 700, y: -330, z: -2000, ry: -18, w: 700, srcStart: 3},
];
const WALL2: Card[] = [
  {clip: 'k-estatua-monica', x: -470, y: -40, z: -200, ry: 20, w: 780},
  {clip: 'k-masp-1869', x: 480, y: 60, z: -800, ry: -20, w: 820},
  {clip: 'k-estatua-branca', x: -520, y: 120, z: -1500, ry: 16, w: 760},
  {clip: 'k-caua-selfie', x: 60, y: -20, z: -2300, ry: 0, w: 900},
];

export const Film: React.FC = () => {
  const seq = (a: number, b: number, extra = T) => ({from: Math.max(0, f(a)), durationInFrames: f(b) - Math.max(0, f(a)) + extra});
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <FontLoader />
      <BlurDefs />

      {SHOTS.filter((s) => s.a < 10).map((s) => (
        <Sequence key={s.id} {...seq(s.a, s.b)}>
          <Shot d={s} />
        </Sequence>
      ))}

      {/* Part 2: memory wall + "teve dia que eu..." */}
      <Sequence {...seq(10.95, 16.3, 10)}>
        <AbsoluteFill style={{opacity: 1}}>
          <WallWithEntry len={f(16.3) - f(10.95) + 10} cards={WALL1} camFrom={-200} camTo={1150} dim={0.38} />
        </AbsoluteFill>
      </Sequence>
      <SlotLettering />

      {SHOTS.filter((s) => s.a >= 16 && s.a < 23).map((s) => (
        <Sequence key={s.id} {...seq(s.a, s.b)}>
          <Shot d={s} />
        </Sequence>
      ))}

      {SHOTS.filter((s) => s.a >= 25 && s.a < 40).map((s) => (
        <Sequence key={s.id} {...seq(s.a, s.b)}>
          <Shot d={s} />
        </Sequence>
      ))}

      {/* Violet block sits above the start of the next shot and slides away */}
      <Sequence {...seq(22.75, 25.7, 6)}>
        <OffsetCtx.Provider value={f(22.75)}>
          <ColorBlock len={f(25.7) - f(22.75)} />
        </OffsetCtx.Provider>
      </Sequence>

      {/* "precisa ser de verdade pra você." */}
      <Sequence {...seq(30.9, 33.3, 0)}>
        <OffsetCtx.Provider value={f(30.9)}>
        <Overlay from={30.9} to={33.3}>
          <div style={{position: 'absolute', left: 200, top: 380, color: IVORY}}>
            <div style={{fontFamily: 'Sans', fontWeight: 500, fontSize: 52, letterSpacing: -1}}>
              <Reveal at={30.94}>precisa</Reveal> <Reveal at={31.1}>ser</Reveal>
            </div>
            <div style={{fontFamily: 'Serif', fontSize: 190, lineHeight: 1}}>
              <Reveal at={31.3}>de</Reveal> <Reveal at={31.48} style={{fontStyle: 'italic'}}>verdade</Reveal>
            </div>
            <div style={{fontFamily: 'Sans', fontWeight: 500, fontSize: 52, letterSpacing: -1, marginTop: 8}}>
              <Reveal at={31.76}>pra</Reveal> <Reveal at={32.0}>você.</Reveal>
            </div>
          </div>
        </Overlay>
        </OffsetCtx.Provider>
      </Sequence>

      {/* "mas vai." */}
      <Sequence {...seq(38.95, 40.85, 0)}>
        <OffsetCtx.Provider value={f(38.95)}>
        <Overlay from={38.95} to={40.85}>
          <div style={{position: 'absolute', left: 210, top: 420, color: IVORY, fontFamily: 'Serif', fontSize: 230, lineHeight: 1}}>
            <Reveal at={38.98}>mas</Reveal> <Reveal at={39.16} style={{fontStyle: 'italic'}}>vai.</Reveal>
          </div>
        </Overlay>
        </OffsetCtx.Provider>
      </Sequence>

      {/* Part 5: memories */}
      <Sequence {...seq(40.85, 45.55, 10)}>
        <WallWithEntry len={f(45.55) - f(40.85) + 10} cards={WALL2} camFrom={-150} camTo={1900} dim={0} />
      </Sequence>

      {SHOTS.filter((s) => s.a >= 45).map((s) => (
        <Sequence key={s.id} {...seq(s.a, s.b)}>
          <Shot d={s} />
        </Sequence>
      ))}

      <Sequence from={f(47.2)} durationInFrames={TOTAL_FRAMES - f(47.2)}>
        <FinalWord len={TOTAL_FRAMES - f(47.2)} />
      </Sequence>

      <FilmFinish />

      <Sequence from={f(0)}>
        <Audio src={staticFile('narracao.wav')} volume={1} />
      </Sequence>
    </AbsoluteFill>
  );
};

/** Memory wall with a zoom-through entrance and fade exit. */
const WallWithEntry: React.FC<{len: number; cards: Card[]; camFrom: number; camTo: number; dim: number}> = (p) => {
  const frame = useCurrentFrame();
  const inP = easeOut(interpolate(frame, [0, 12], [0, 1], clamp));
  const outP = interpolate(frame, [p.len - 10, p.len], [0, 1], clamp);
  return (
    <AbsoluteFill style={{opacity: inP * (1 - outP), transform: `scale(${1.25 - 0.25 * inP})`, filter: `blur(${(1 - inP) * 16}px)`}}>
      <MemoryWall len={p.len} cards={p.cards} camFrom={p.camFrom} camTo={p.camTo} dim={p.dim} />
    </AbsoluteFill>
  );
};
