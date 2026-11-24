// Reel 9:16 · "Satu orang pergi, saham anjlok" (Jensen Huang mundur 12 Nov, kembali 23 Nov 2026) · VO manual Endrich (52,7 dtk)
// Timing kata: motion/proyek/2026-11-24-ceo-nvidia/align.py -> ceo-nvidia-data.json (T = awal kata, detik, sudah +0,2 lead).
// Gaya campuran + efek 3D CSS (perspective): kartu flip, foto mengambang + parallax, tumpukan kartu berita, logo ekstrusi,
// bagan dewan, kalender flip, chart miring 3D, menara balok, chibi di CTA. Sumber fakta: riset.md di folder proyek.
import React from "react";
import { AbsoluteFill, Audio, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, continueRender, delayRender } from "remotion";
import D from "./ceo-nvidia-data.json";

const T: number[] = D.T;
const K = { k: "#07090A", g: "#76B900", g2: "#9BE22D", r: "#FF4F3A", cr: "#F4F1EA", gy: "#8A918A", y: "#F5B301", card: "#12160F" };
const f = (n: string) => staticFile(`ceo-nvidia/${n}`);
const fontCss = `
@font-face { font-family: IDBlack; src: url(${staticFile("fonts/InterDisplay-Black.ttf")}); }
@font-face { font-family: IDBold; src: url(${staticFile("fonts/InterDisplay-Bold.ttf")}); }
@font-face { font-family: IDSemi; src: url(${staticFile("fonts/InterDisplay-SemiBold.ttf")}); }`;

const useFonts = () => {
  const [h] = React.useState(() => delayRender("fonts"));
  React.useEffect(() => {
    const fs = [["IDBlack", "InterDisplay-Black.ttf"], ["IDBold", "InterDisplay-Bold.ttf"], ["IDSemi", "InterDisplay-SemiBold.ttf"]].map(
      ([n, p]) => new FontFace(n, `url(${staticFile("fonts/" + p)})`).load().then((ff) => (document as any).fonts.add(ff)));
    Promise.all(fs).then(() => continueRender(h)).catch(() => continueRender(h));
  }, [h]);
};

// ---------- helpers waktu
const useT = () => { const fr = useCurrentFrame(), { fps } = useVideoConfig(); return { t: fr / fps, fr, fps }; };
const cl = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };
const useSp = () => { const { fr, fps } = useT(); return (t0: number, damping = 13, mass = 0.6) => spring({ frame: fr - Math.round(t0 * fps), fps, config: { damping, mass } }); };
const win = (t: number, a: number, b: number, fi = 0.18, fo = 0.2) => interpolate(t, [a, a + fi, b - fo, b], [0, 1, 1, 0], cl);
const ease = (t: number, a: number, b: number, v0 = 0, v1 = 1) => interpolate(t, [a, b], [v0, v1], { ...cl, easing: (x) => 1 - Math.pow(1 - x, 3) });

// teks kata per kata (masuk dari bawah + sedikit rotasi 3D)
const Words: React.FC<{ text: string; at: number; size: number; color?: string; top: number; accent?: string[]; stagger?: number }> =
  ({ text, at, size, color = K.cr, top, accent = [], stagger = 0.07 }) => {
    const sp = useSp();
    return (
      <div style={{ position: "absolute", left: 60, right: 60, top, textAlign: "center", fontFamily: "IDBlack", fontSize: size, lineHeight: 1.02,
        letterSpacing: "-0.02em", color, perspective: 900, textShadow: "0 6px 30px rgba(0,0,0,.7)" }}>
        {text.split(" ").map((w, i) => {
          const s = sp(at + i * stagger, 12, 0.5);
          const isA = accent.includes(w.replace(/[^\w%+-]/g, "").toUpperCase());
          return (
            <span key={i} style={{ display: "inline-block", marginRight: size * 0.22, opacity: s, color: isA ? K.g2 : color,
              transform: `translateY(${(1 - s) * 60}px) rotateX(${(1 - s) * -70}deg)`, transformOrigin: "50% 100%" }}>{w}</span>
          );
        })}
      </div>
    );
  };

const Chip: React.FC<{ at: number; left: number; top: number; bg: string; color?: string; children: React.ReactNode; size?: number }> =
  ({ at, left, top, bg, color = K.k, children, size = 34 }) => {
    const s = useSp()(at, 10, 0.5);
    return <div style={{ position: "absolute", left, top, padding: "12px 26px", borderRadius: 40, background: bg, color, fontFamily: "IDBold", fontSize: size,
      letterSpacing: ".05em", whiteSpace: "nowrap", opacity: Math.min(1, s * 1.5), transform: `scale(${0.5 + 0.5 * s})` }}>{children}</div>;
  };

const Stamp: React.FC<{ at: number; text: string; color: string; top: number; size?: number; rot?: number }> = ({ at, text, color, top, size = 70, rot = -8 }) => {
  const { t } = useT();
  const p = ease(t, at, at + 0.22);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top, textAlign: "center", opacity: p, transform: `scale(${2.2 - 1.2 * p})` }}>
      <span style={{ display: "inline-block", fontFamily: "IDBlack", fontSize: size, color, border: `8px solid ${color}`, borderRadius: 16,
        padding: "4px 30px 10px", transform: `rotate(${rot}deg)`, background: "rgba(7,9,10,.75)" }}>{text}</span>
    </div>
  );
};

// ---------- latar: medan partikel 3D + grid lantai
const Particles: React.FC = () => {
  const { t } = useT();
  const pts = React.useMemo(() => Array.from({ length: 70 }, (_, i) => ({ x: ((i * 397) % 1000) / 1000, y: ((i * 613) % 1000) / 1000, z: ((i * 271) % 1000) / 1000 })), []);
  return (
    <AbsoluteFill style={{ perspective: 800, overflow: "hidden" }}>
      {pts.map((p, i) => {
        const z = ((p.z + t * 0.06) % 1);
        const sc = 0.3 + z * 1.8;
        const x = 540 + (p.x - 0.5) * 1400 * sc, y = 960 + (p.y - 0.5) * 2200 * sc;
        return <div key={i} style={{ position: "absolute", left: x, top: y, width: 6 * sc, height: 6 * sc, borderRadius: "50%", background: K.g,
          opacity: 0.12 + z * 0.35, filter: `blur(${(1 - z) * 2}px)` }} />;
      })}
      <div style={{ position: "absolute", left: -600, right: -600, bottom: -200, height: 900, transform: "rotateX(72deg)", transformOrigin: "50% 100%",
        backgroundImage: `linear-gradient(rgba(118,185,0,.22) 2px, transparent 2px), linear-gradient(90deg, rgba(118,185,0,.22) 2px, transparent 2px)`,
        backgroundSize: "90px 90px", backgroundPosition: `0 ${(t * 60) % 90}px`, opacity: 0.5,
        maskImage: "linear-gradient(transparent, black 60%)", WebkitMaskImage: "linear-gradient(transparent, black 60%)" }} />
    </AbsoluteFill>
  );
};

// ---------- S1 hook: kartu flip 3D
const S1: React.FC = () => {
  const { t } = useT();
  const flip = ease(t, T[5] - 0.15, T[5] + 0.45, 0, 180);
  const op = win(t, 0, T[11] - 0.05, 0.01);
  const face = (back: boolean): React.CSSProperties => ({ position: "absolute", inset: 0, borderRadius: 40, backfaceVisibility: "hidden", padding: 50,
    display: "flex", flexDirection: "column", justifyContent: "space-between", transform: back ? "rotateY(180deg)" : undefined,
    background: back ? "linear-gradient(160deg,#1b2a08,#0d1405)" : "linear-gradient(160deg,#2a0f0c,#140706)",
    border: `4px solid ${back ? K.g : K.r}`, boxShadow: `0 40px 120px ${back ? "rgba(118,185,0,.35)" : "rgba(255,79,58,.35)"}` });
  const arrow = (up: boolean, at: number) => {
    const p = ease(t, at, at + 0.5);
    return <svg viewBox="0 0 100 100" style={{ width: 260, height: 260, alignSelf: "center" }}>
      <path d={up ? "M15 80 L45 50 L60 62 L88 22" : "M15 22 L45 52 L60 40 L88 80"} fill="none" stroke={up ? K.g2 : K.r} strokeWidth={9} strokeLinecap="round"
        strokeLinejoin="round" strokeDasharray={140} strokeDashoffset={140 * (1 - p)} />
      <path d={up ? "M70 20 L90 20 L90 40" : "M70 82 L90 82 L90 62"} fill="none" stroke={up ? K.g2 : K.r} strokeWidth={9} strokeLinecap="round" opacity={p > 0.9 ? 1 : 0} />
    </svg>;
  };
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1600 }}>
      <div style={{ position: "absolute", left: 140, top: 430, width: 800, height: 900, transformStyle: "preserve-3d",
        transform: `rotateY(${flip}deg) rotateX(${Math.sin(t * 1.3) * 4}deg) translateZ(${ease(t, 0, 0.5, -400, 0)}px)` }}>
        <div style={face(false)}>
          <div style={{ fontFamily: "IDBold", fontSize: 40, letterSpacing: ".14em", color: K.r }}>1 ORANG PERGI</div>
          {arrow(false, 0.6)}
          <div style={{ fontFamily: "IDBlack", fontSize: 130, color: K.cr, lineHeight: 1 }}>SAHAM<br /><span style={{ color: K.r }}>ANJLOK</span></div>
        </div>
        <div style={face(true)}>
          <div style={{ fontFamily: "IDBold", fontSize: 40, letterSpacing: ".14em", color: K.g2 }}>1 ORANG KEMBALI</div>
          {arrow(true, T[5] + 0.3)}
          <div style={{ fontFamily: "IDBlack", fontSize: 130, color: K.cr, lineHeight: 1 }}>SAHAM<br /><span style={{ color: K.g2 }}>+30%</span></div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- foto Jensen: kartu 3D mengambang (dipakai S2, S3, S6)
const Photo: React.FC<{ gray: number; z: number; rotY: number; scale?: number; top?: number }> = ({ gray, z, rotY, scale = 1, top = 520 }) => {
  const { t } = useT();
  return (
    <div style={{ position: "absolute", left: 190, top, width: 700, height: 700, transformStyle: "preserve-3d",
      transform: `translateZ(${z}px) rotateY(${rotY + Math.sin(t * 0.9) * 6}deg) rotateX(${Math.cos(t * 0.7) * 4}deg) scale(${scale})` }}>
      <div style={{ position: "absolute", inset: -40, borderRadius: 60, background: `radial-gradient(circle, rgba(118,185,0,${0.45 * (1 - gray)}), transparent 70%)`, transform: "translateZ(-80px)" }} />
      <Img src={f("jensen.png")} style={{ width: 700, height: 700, borderRadius: 36, objectFit: "cover", filter: `grayscale(${gray}) contrast(${1 + gray * 0.15})`,
        boxShadow: "0 50px 120px rgba(0,0,0,.7)", border: `4px solid ${gray > 0.5 ? K.gy : K.g}` }} />
      <div style={{ position: "absolute", left: 40, bottom: -50, padding: "16px 30px", borderRadius: 18, background: K.cr, color: K.k, fontFamily: "IDBlack",
        fontSize: 46, transform: "translateZ(90px)", boxShadow: "0 20px 50px rgba(0,0,0,.5)" }}>Jensen Huang<span style={{ fontFamily: "IDBold", fontSize: 26,
        color: "#556", marginLeft: 14 }}>CEO NVIDIA</span></div>
    </div>
  );
};

const S2S3: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[11] - 0.1, T[34] - 0.05);
  const gray = ease(t, T[20], T[20] + 0.6);
  const z = ease(t, T[11] - 0.1, T[11] + 0.6, -900, 0) + ease(t, T[20], T[20] + 0.8, 0, -500);
  const rot = ease(t, T[20], T[20] + 0.8, 0, -18);
  const news = [
    { at: T[20], k: "12 NOV 2026", h: "CEO Nvidia mundur", c: K.r },
    { at: T[22], k: "DILAPORKAN MEDIA", h: "Mengakui perselingkuhan", c: K.y },
    { at: T[26] + 0.2, k: "PENYELIDIKAN DEWAN", h: "Jadi sasaran intelijen asing?", c: K.cr },
  ];
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1500 }}>
      <div style={{ opacity: ease(t, T[15] - 0.25, T[15], 1, 0) }}><Words text="KEKUATAN JENSEN HUANG" at={T[11] - 0.05} size={92} top={330} accent={["JENSEN", "HUANG"]} /></div>
      <div style={{ opacity: ease(t, T[15] - 0.1, T[15] + 0.1, 1, 0) }}><Photo gray={0} z={z} rotY={0} /></div>
      <div style={{ opacity: ease(t, T[15] - 0.1, T[15] + 0.1, 0, 1) }}><Photo gray={gray} z={z} rotY={rot} top={460} scale={0.92} /></div>
      <Chip at={T[15]} left={90} top={330} bg={K.r} color={K.cr} size={44}>12 NOVEMBER</Chip>
      {news.map((n, i) => {
        const s = useSp()(n.at, 14, 0.7);
        return (
          <div key={i} style={{ position: "absolute", left: 110 + i * 24, top: 940 + i * 150, width: 860, padding: "22px 30px", borderRadius: 20,
            background: "#F2EDE2", color: "#141414", opacity: s, boxShadow: "0 30px 70px rgba(0,0,0,.6)",
            transform: `translateZ(${(1 - s) * 500 + i * 40}px) rotateX(${(1 - s) * 50 + 8}deg) rotateZ(${(i - 1) * 1.5}deg)` }}>
            <div style={{ fontFamily: "IDBold", fontSize: 22, letterSpacing: ".16em", color: n.c === K.cr ? "#6b6b6b" : n.c }}>{n.k}</div>
            <div style={{ fontFamily: "IDBlack", fontSize: 50, marginTop: 6 }}>{n.h}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ---------- S4 pasar panik + logo ekstrusi 3D
const S4: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[34] - 0.08, T[50] - 0.05);
  const gone = ease(t, T[48], T[48] + 0.5);
  const glitch = t > T[48] && t < T[48] + 0.5 ? Math.sin(t * 90) * 18 : 0;
  const ry = Math.sin(t * 0.8) * 28;
  const bars = Array.from({ length: 9 }, (_, i) => i);
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1400 }}>
      <AbsoluteFill style={{ background: "radial-gradient(70% 40% at 50% 30%, rgba(255,79,58,.3), transparent 70%)", opacity: win(t, T[34], T[37] + 0.4) }} />
      <Words text="PASAR LANGSUNG PANIK" at={T[34] - 0.05} size={100} top={330} color={K.r} />
      {bars.map((i) => {
        const p = ease(t, T[35] + i * 0.05, T[35] + i * 0.05 + 0.6);
        return <div key={i} style={{ position: "absolute", left: 120 + i * 95, top: 560, width: 70, height: 420 * (0.4 + ((i * 37) % 60) / 100),
          background: `linear-gradient(${K.r}, rgba(255,79,58,.15))`, borderRadius: 10, transformOrigin: "50% 0",
          opacity: win(t, T[35], T[37] + 0.3), transform: `rotateX(25deg) translateY(${p * 260}px) scaleY(${1 - p * 0.5})` }} />;
      })}
      <div style={{ opacity: ease(t, T[37] - 0.1, T[37] + 0.3) * (1 - gone), position: "absolute", left: 140, top: 640, width: 800, height: 452,
        transformStyle: "preserve-3d", transform: `rotateY(${ry}deg) rotateX(10deg) translateX(${glitch}px)` }}>
        {Array.from({ length: 14 }, (_, i) => (
          <Img key={i} src={f("logo.png")} style={{ position: "absolute", inset: 0, width: 800, height: 452, borderRadius: 26,
            transform: `translateZ(${-i * 4}px)`, filter: i ? `brightness(${0.45 - i * 0.02})` : "none" }} />
        ))}
      </div>
      <Words text="TULANG PUNGGUNG AI DUNIA" at={T[39]} size={70} top={1190} accent={["AI"]} />
      <Stamp at={T[48]} text="TIBA-TIBA HILANG" color={K.r} top={800} size={74} />
    </AbsoluteFill>
  );
};

// ---------- S5 dewan: kursi CEO
const S5: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[50] - 0.08, T[65] - 0.05);
  const swap = ease(t, T[53] - 0.1, T[53] + 0.5);
  const sp = useSp();
  const b = sp(T[50], 14);
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1400 }}>
      <Words text="KEPUTUSAN DEWAN" at={T[50] - 0.05} size={100} top={330} />
      <div style={{ position: "absolute", left: 140, top: 560, width: 800, height: 560, transformStyle: "preserve-3d",
        transform: `rotateX(${18 - b * 8}deg) rotateY(${Math.sin(t) * 5}deg) translateZ(${(1 - b) * -500}px)` }}>
        <div style={{ position: "absolute", left: 200, top: 0, width: 400, height: 250, borderRadius: 26, background: K.card, border: `4px solid ${K.g}`,
          transformStyle: "preserve-3d", transform: `rotateY(${swap * 180}deg)` }}>
          <div style={{ position: "absolute", inset: 0, backfaceVisibility: "hidden", display: "flex", alignItems: "center", gap: 20, padding: 24 }}>
            <Img src={f("jensen.png")} style={{ width: 150, height: 150, borderRadius: 75, objectFit: "cover", filter: "grayscale(1)" }} />
            <div style={{ fontFamily: "IDBlack", fontSize: 38, color: K.cr, lineHeight: 1.05 }}>Jensen<br />Huang<div style={{ fontFamily: "IDBold", fontSize: 22, color: K.r, marginTop: 8 }}>MUNDUR</div></div>
          </div>
          <div style={{ position: "absolute", inset: 0, backfaceVisibility: "hidden", transform: "rotateY(180deg)", display: "flex", flexDirection: "column",
            justifyContent: "center", alignItems: "center", textAlign: "center" }}>
            <div style={{ fontFamily: "IDBold", fontSize: 24, letterSpacing: ".14em", color: K.g2 }}>CEO SEMENTARA</div>
            <div style={{ fontFamily: "IDBlack", fontSize: 58, color: K.cr, marginTop: 8 }}>Colette Kress</div>
            <div style={{ fontFamily: "IDBold", fontSize: 24, color: K.gy, marginTop: 6 }}>CFO NVIDIA</div>
          </div>
        </div>
        <svg style={{ position: "absolute", left: 0, top: 250, width: 800, height: 140 }} viewBox="0 0 800 140">
          <path d="M400 0 V60 M120 60 H680 M120 60 V140 M400 60 V140 M680 60 V140" stroke={K.gy} strokeWidth={5} fill="none" />
        </svg>
        {[0, 1, 2].map((i) => <div key={i} style={{ position: "absolute", left: 40 + i * 280, top: 390, width: 160, height: 110, borderRadius: 18,
          background: "#1A1F17", border: "3px solid #2c3428", fontFamily: "IDBold", fontSize: 22, color: K.gy, display: "flex", alignItems: "center",
          justifyContent: "center", letterSpacing: ".12em", transform: "translateZ(30px)" }}>DEWAN</div>)}
      </div>
      <Stamp at={T[59]} text="TIDAK AKAN DIANGKAT LAGI" color={K.r} top={1210} size={58} rot={-5} />
    </AbsoluteFill>
  );
};

// ---------- S6 11 hari: kalender flip + kembali
const Flip: React.FC<{ from: string; to: string; at: number; left: number; size?: number }> = ({ from, to, at, left, size = 150 }) => {
  const { t } = useT();
  const a = ease(t, at, at + 0.5, 0, 180);
  const card = (txt: string, back: boolean): React.CSSProperties => ({ position: "absolute", inset: 0, borderRadius: 24, background: back ? K.g : K.cr,
    color: K.k, fontFamily: "IDBlack", fontSize: size, display: "flex", alignItems: "center", justifyContent: "center", backfaceVisibility: "hidden",
    transform: back ? "rotateX(180deg)" : undefined, boxShadow: "0 30px 70px rgba(0,0,0,.6)" });
  return (
    <div style={{ position: "absolute", left, top: 600, width: 260, height: 300, transformStyle: "preserve-3d", transform: `rotateX(${a}deg)` }}>
      <div style={card(from, false)}>{from}</div><div style={card(to, true)}>{to}</div>
    </div>
  );
};

const S6: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[65] - 0.08, T[76] - 0.05);
  const back = ease(t, T[74] - 0.1, T[74] + 0.6);
  const days = Math.round(ease(t, T[66], T[67] + 0.4, 0, 11));
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1400 }}>
      <div style={{ opacity: 1 - back }}>
        <Words text="TAPI…" at={T[65] - 0.05} size={110} top={330} />
        <Flip from="12" to="23" at={T[66]} left={250} />
        <Flip from="NOV" to="NOV" at={T[66] + 0.1} left={570} size={96} />
        <div style={{ position: "absolute", left: 0, right: 0, top: 960, textAlign: "center", fontFamily: "IDBlack", fontSize: 120, color: K.g2 }}>{days} HARI</div>
        <Words text="DEWAN BERBALIK ARAH" at={T[71]} size={80} top={1150} color={K.y} />
      </div>
      <div style={{ opacity: back }}>
        <Photo gray={0} z={ease(t, T[74] - 0.1, T[74] + 0.6, -700, 0)} rotY={ease(t, T[74] - 0.1, T[74] + 0.6, 40, 0)} top={500} />
        <Words text="JENSEN KEMBALI" at={T[74]} size={110} top={330} color={K.g2} />
      </div>
    </AbsoluteFill>
  );
};

// ---------- S7 chart TradingView di bidang 3D + Trump
const S7: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[76] - 0.08, T[91] - 0.05);
  const z = ease(t, T[76], T[76] + 3.2, 0, 1);
  const pct = ease(t, T[78], T[79] + 0.6, 0, 31.48);
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1300 }}>
      <Words text="INVESTOR LEGA" at={T[76] - 0.05} size={110} top={330} color={K.g2} />
      <div style={{ position: "absolute", left: 60, top: 560, width: 1000, height: 437, transformStyle: "preserve-3d",
        transform: `rotateX(${22 - z * 10}deg) rotateY(${-16 + z * 10}deg) scale(${0.86 + z * 0.2}) translateX(${-z * 60}px)`, transformOrigin: "75% 50%" }}>
        <Img src={f("chart.png")} style={{ width: 1000, height: 437, borderRadius: 20, boxShadow: "0 50px 120px rgba(0,0,0,.7)" }} />
        <div style={{ position: "absolute", inset: 0, borderRadius: 20, background: `linear-gradient(90deg, transparent ${60 + z * 20}%, rgba(118,185,0,.25))`, transform: "translateZ(2px)" }} />
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1060, textAlign: "center", fontFamily: "IDBlack", fontSize: 150, color: K.g2,
        opacity: ease(t, T[78], T[78] + 0.2), textShadow: "0 0 60px rgba(118,185,0,.5)" }}>+{pct.toFixed(2).replace(".", ",")}%</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1240, textAlign: "center", fontFamily: "IDBold", fontSize: 26, letterSpacing: ".14em",
        color: K.gy, opacity: ease(t, T[79], T[79] + 0.3) }}>NVDA · 23 NOV 2026 · SUMBER: TRADINGVIEW</div>
      <Chip at={T[83]} left={120} top={1320} bg={K.cr} size={36}>TRUMP: “ikut berperan” dalam keputusan ini</Chip>
    </AbsoluteFill>
  );
};

// ---------- S8 menara balok di atas 1 orang
const S8: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[91] - 0.08, T[109] - 0.05);
  const sp = useSp();
  const wob = t > T[106] ? Math.sin((t - T[106]) * 7) * 6 * Math.exp(-(t - T[106]) * 0.8) : 0;
  const rows = [3, 3, 3, 3, 2];
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1300 }}>
      <Words text="PELAJARAN BUAT BISNIS" at={T[91] - 0.05} size={88} top={330} />
      <div style={{ position: "absolute", left: 290, top: 560, width: 500, height: 720, transformStyle: "preserve-3d",
        transform: `rotateX(-12deg) rotateY(${30 + Math.sin(t * 0.6) * 10}deg) rotateZ(${wob}deg)`, transformOrigin: "50% 100%" }}>
        {rows.map((n, r) => Array.from({ length: n }, (_, i) => {
          const s = sp(T[97] + (r * 3 + i) * 0.06, 12);
          return <div key={`${r}-${i}`} style={{ position: "absolute", left: 50 + i * 140 + (3 - n) * 70, top: 480 - r * 100 - (1 - s) * 500, width: 130, height: 90,
            borderRadius: 10, background: r % 2 ? "#2B3324" : "#3A4630", border: "3px solid #56663f", opacity: s, transform: "translateZ(0)" }} />;
        }))}
        <div style={{ position: "absolute", left: 175, top: 580, width: 150, height: 120, borderRadius: 12, background: K.g, color: K.k, fontFamily: "IDBlack",
          fontSize: 30, display: "flex", alignItems: "center", justifyContent: "center", textAlign: "center", lineHeight: 1, opacity: sp(T[101], 12),
          boxShadow: "0 0 50px rgba(118,185,0,.6)", transform: "translateZ(40px)" }}>1<br />ORANG</div>
      </div>
      <Chip at={T[105]} left={110} top={1320} bg={K.g} size={40}>KEKUATAN</Chip>
      <Chip at={T[107]} left={560} top={1320} bg={K.r} color={K.cr} size={40}>RISIKO BESAR</Chip>
    </AbsoluteFill>
  );
};

// ---------- S9 CTA + chibi
const POSES = ["netral", "lambai", "tunjuk", "mikir", "kaget", "keren", "bicara", "kedip"];
const Chibi: React.FC = () => {
  const { t } = useT();
  const track = D.track as [number, string][];
  let pose = "netral";
  for (const [tt, p] of track) if (tt <= t) pose = p;
  const inn = ease(t, D.ctaIn, D.ctaIn + 0.5);
  const bob = Math.sin((t - D.ctaIn) * Math.PI / 0.6) * 5;
  const em = (D.emph as number[]).reduce((a, e) => (t >= e && t < e + 0.35 ? 1 - (t - e) / 0.35 : a), 0);
  const w = 470, h = Math.round(w * 1680 / 944);
  return (
    <div style={{ position: "absolute", left: 305, top: 650 + (1 - inn) * 700 + bob, width: w, height: h, opacity: inn > 0 ? 1 : 0,
      transform: `scale(${1 + em * 0.04}, ${1 - em * 0.06})`, transformOrigin: "50% 100%" }}>
      {POSES.map((p, i) => <Img key={p} src={f(`pose/pose_${i}_${p}.png`)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", opacity: p === pose ? 1 : 0 }} />)}
    </div>
  );
};

const S9: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[109] - 0.08, D.dur + 1, 0.18, 0.01);
  return (
    <AbsoluteFill style={{ opacity: op }}>
      <div style={{ opacity: 1 - ease(t, T[116] - 0.2, T[116]) }}><Words text="KALAU ORANG ITU PERGI?" at={T[109] - 0.05} size={84} top={330} /></div>
      <div style={{ opacity: ease(t, T[116] - 0.2, T[116]) }}><Words text="BISNIS KAMU SIAP TANPA KAMU?" at={T[116]} size={74} top={330} color={K.g2} /></div>
      <Chip at={T[123]} left={270} top={530} bg={K.cr} size={44}>💬 Jawab di komentar</Chip>
      <Chibi />
    </AbsoluteFill>
  );
};

export const CeoNvidia: React.FC = () => {
  useFonts();
  const { t } = useT();
  const flash = Math.max(...[T[5], T[20], T[48], T[74], T[78]].map((a) => (t >= a && t < a + 0.25 ? 0.35 * (1 - (t - a) / 0.25) : 0)));
  return (
    <AbsoluteFill style={{ background: `radial-gradient(120% 70% at 50% 40%, #131A0E 0%, ${K.k} 70%)`, overflow: "hidden" }}>
      <style>{fontCss}</style>
      <Audio src={f("vo.mp3")} />
      <Particles />
      <S1 /><S2S3 /><S4 /><S5 /><S6 /><S7 /><S8 /><S9 />
      <div style={{ position: "absolute", left: 60, top: 262, display: "flex", alignItems: "center", gap: 12, fontFamily: "IDBold", fontSize: 24,
        letterSpacing: ".18em", color: K.cr }}><i style={{ width: 12, height: 12, borderRadius: 6, background: K.g, display: "inline-block" }} />BERITA AI · NVIDIA</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1525, textAlign: "center", fontFamily: "IDBlack", fontSize: 36, color: K.cr }}>
        Endrich<span style={{ color: K.g }}>Tech</span></div>
      <AbsoluteFill style={{ background: "#fff", opacity: flash, pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};
