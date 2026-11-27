// Reel 9:16 · "Apartemen vs rumah sendiri" (Mekari kena malware, opsi C) · VO manual Endrich (58,8 dtk).
// Timing: motion/proyek/2026-11-27-mekari-malware/align.py -> mekari-data.json. Helper sama dengan CeoNvidia/OpenaiDigugat.
// Aset logo 5 aplikasi, foto CEO, surat maaf: di-crop dari video Course-Net kiriman Endrich. Efek 3D CSS.
import React from "react";
import { AbsoluteFill, Audio, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, continueRender, delayRender } from "remotion";
import D from "./mekari-c-data.json";

const T: number[] = D.T;
const K = { k: "#0A0812", g: "#7B4DFF", g2: "#A98BFF", r: "#FF4F3A", cr: "#F4F1EA", gy: "#8E8AA0", y: "#F5B301", card: "#15121F", b: "#3A5BFF", ok: "#22C55E" };
const f = (n: string) => staticFile(`mekari/${n}`);
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
        backgroundImage: `linear-gradient(rgba(123,77,255,.22) 2px, transparent 2px), linear-gradient(90deg, rgba(123,77,255,.22) 2px, transparent 2px)`,
        backgroundSize: "90px 90px", backgroundPosition: `0 ${(t * 60) % 90}px`, opacity: 0.5,
        maskImage: "linear-gradient(transparent, black 60%)", WebkitMaskImage: "linear-gradient(transparent, black 60%)" }} />
    </AbsoluteFill>
  );
};

const APPS = ["talenta", "jurnal", "qontak", "sign", "flex"];
const AppCard: React.FC<{ n: string; off: number; w?: number; style?: React.CSSProperties }> = ({ n, off, w = 300, style }) => (
  <div style={{ position: "relative", width: w, height: w / 2.95, ...style }}>
    <Img src={f(`app_${n}.png`)} style={{ width: "100%", height: "100%", filter: `grayscale(${off}) brightness(${1 - off * 0.45})`,
      boxShadow: `0 20px 50px rgba(0,0,0,.55)`, borderRadius: 18 }} />
    <div style={{ position: "absolute", right: -14, top: -14, width: 54, height: 54, borderRadius: 27, background: K.r, color: "#fff", fontFamily: "IDBlack",
      fontSize: 34, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${off})` }}>✕</div>
  </div>
);
const Bug: React.FC<{ size: number; color?: string }> = ({ size, color = K.r }) => (
  <svg viewBox="0 0 100 100" style={{ width: size, height: size }} fill="none" stroke={color} strokeWidth={6} strokeLinecap="round">
    <path d="M30 38h40v26a20 20 0 0 1-40 0z" /><path d="M38 38a12 12 0 0 1 24 0M50 44v38M30 50H14M70 50h16M30 66H16M70 66h14M34 30l-8-10M66 30l8-10" />
  </svg>
);
const PayCard: React.FC<{ co: string; st: string; c: string; style?: React.CSSProperties }> = ({ co, st, c, style }) => (
  <div style={{ width: 620, padding: "26px 32px", borderRadius: 26, background: K.cr, color: K.k, boxShadow: "0 40px 90px rgba(0,0,0,.6)", ...style }}>
    <div style={{ fontFamily: "IDBold", fontSize: 24, letterSpacing: ".12em", color: "#777" }}>TRANSFER GAJI · NOV 2026</div>
    <div style={{ fontFamily: "IDBlack", fontSize: 44, marginTop: 6 }}>{co}</div>
    <div style={{ marginTop: 14, display: "inline-block", padding: "8px 22px", borderRadius: 14, background: c, color: "#fff", fontFamily: "IDBlack", fontSize: 34 }}>{st}</div>
  </div>
);

// ---------- balok 3D (kubus CSS) + gedung/rumah
const Box: React.FC<{ w: number; h: number; d: number; front: React.ReactNode; side?: React.ReactNode; col: string; side2: string; top: string; style?: React.CSSProperties }> =
  ({ w, h, d, front, side, col, side2, top, style }) => {
    const face: React.CSSProperties = { position: "absolute", backfaceVisibility: "hidden", overflow: "hidden" };
    return (
      <div style={{ position: "absolute", width: w, height: h, transformStyle: "preserve-3d", ...style }}>
        <div style={{ ...face, width: w, height: h, background: col, transform: `translateZ(${d / 2}px)` }}>{front}</div>
        <div style={{ ...face, width: w, height: h, background: side2, transform: `rotateY(180deg) translateZ(${d / 2}px)` }} />
        <div style={{ ...face, width: d, height: h, left: (w - d) / 2, background: side2, transform: `rotateY(90deg) translateZ(${w / 2}px)` }}>{side}</div>
        <div style={{ ...face, width: d, height: h, left: (w - d) / 2, background: side2, transform: `rotateY(-90deg) translateZ(${w / 2}px)` }} />
        <div style={{ ...face, width: w, height: d, top: (h - d) / 2, background: top, transform: `rotateX(90deg) translateZ(${h / 2}px)` }} />
      </div>
    );
  };
const Windows: React.FC<{ cols: number; rows: number; lit: (i: number) => number; hi?: number }> = ({ cols, rows, lit, hi = -1 }) => (
  <div style={{ position: "absolute", inset: 22, display: "grid", gridTemplateColumns: `repeat(${cols}, 1fr)`, gap: 14 }}>
    {Array.from({ length: cols * rows }, (_, i) => {
      const l = lit(i);
      return <div key={i} style={{ borderRadius: 6, background: l > 0.5 ? "#FFD66B" : "#1A1726", boxShadow: l > 0.5 ? "0 0 18px rgba(255,214,107,.7)" : "none",
        outline: i === hi ? `5px solid ${K.r}` : "none", outlineOffset: 3 }} />;
    })}
  </div>
);
const House: React.FC<{ x: number; y: number; lit: number; bad?: number; ry: number; db?: boolean }> = ({ x, y, lit, bad = 0, ry, db = true }) => (
  <div style={{ position: "absolute", left: x, top: y, width: 220, height: 200, transformStyle: "preserve-3d", transform: `rotateY(${ry}deg)` }}>
    <Box w={220} h={170} d={200} col={bad > 0.5 ? "#4A1E1E" : "#2B2440"} side2={bad > 0.5 ? "#351414" : "#1F1A30"} top="#3A3150"
      style={{ top: 60 }} front={<>
        <div style={{ position: "absolute", left: 30, top: 40, width: 60, height: 50, borderRadius: 6, background: lit > 0.5 ? "#FFD66B" : "#1A1726", boxShadow: lit > 0.5 ? "0 0 20px rgba(255,214,107,.7)" : "none" }} />
        <div style={{ position: "absolute", right: 30, top: 40, width: 60, height: 50, borderRadius: 6, background: lit > 0.5 ? "#FFD66B" : "#1A1726" }} />
        <div style={{ position: "absolute", left: 85, bottom: 0, width: 50, height: 70, borderRadius: "8px 8px 0 0", background: "#15121F" }} /></>} />
    <div style={{ position: "absolute", left: -10, top: -10, width: 240, height: 90, background: bad > 0.5 ? K.r : K.g, clipPath: "polygon(50% 0, 100% 100%, 0 100%)", transform: "translateZ(101px)" }} />
    {db && <svg viewBox="0 0 100 100" style={{ position: "absolute", left: 70, top: 250, width: 80, height: 80 }} fill={bad > 0.5 ? "#3A1717" : "#1E1A2C"} stroke={bad > 0.5 ? K.r : K.g2} strokeWidth={6}>
      <path d="M18 22v56c0 6 14 11 32 11s32-5 32-11V22" /><ellipse cx="50" cy="22" rx="32" ry="11" /><path d="M18 50c0 6 14 11 32 11s32-5 32-11" fill="none" /></svg>}
  </div>
);
const Tower: React.FC<{ lit: (i: number) => number; hi?: number; grow?: number; scale?: number; x?: number; y?: number; ry: number }> = ({ lit, hi, grow = 1, scale = 1, x = 330, y = 520, ry }) => (
  <div style={{ position: "absolute", left: x, top: y, width: 420, height: 760, transformStyle: "preserve-3d", transformOrigin: "50% 100%",
    transform: `scale(${scale}) rotateX(-8deg) rotateY(${ry}deg) scaleY(${grow})` }}>
    <Box w={420} h={760} d={300} col="#2B2440" side2="#1F1A30" top="#3A3150"
      front={<Windows cols={4} rows={9} lit={lit} hi={hi} />} side={<Windows cols={3} rows={9} lit={(i) => lit(i + 7)} />} />
  </div>
);

// ---------- S1 hook: banyak perusahaan telat gaji barengan
const S1: React.FC = () => {
  const { t } = useT();
  const op = win(t, 0, T[11] - 0.05, 0.01);
  const red = ease(t, T[9], T[9] + 0.3);
  const sp = useSp();
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1400 }}>
      <Words text="1 PERETASAN" at={0} size={110} top={330} color={K.r} />
      <div style={{ position: "absolute", left: 0, top: 500, width: 1080, height: 700, transformStyle: "preserve-3d", transform: `rotateX(38deg) rotateZ(${Math.sin(t) * 4}deg)` }}>
        {Array.from({ length: 9 }, (_, i) => {
          const s = sp(0.15 + i * 0.06, 12);
          return <div key={i} style={{ position: "absolute", left: 150 + (i % 3) * 280, top: 40 + Math.floor(i / 3) * 220, width: 220, height: 170, transformStyle: "preserve-3d",
            opacity: s, transform: `translateZ(${(1 - s) * 400}px)` }}>
            <Box w={160} h={120} d={120} col={red > 0.5 ? "#4A1E1E" : "#2B2440"} side2={red > 0.5 ? "#351414" : "#1F1A30"} top={red > 0.5 ? K.r : K.g}
              style={{ left: 30, top: 0, transform: "rotateX(-90deg)", transformOrigin: "50% 100%" }} front={null} />
            <div style={{ position: "absolute", left: 30, top: 130, width: 160, padding: "6px 0", borderRadius: 10, background: red > 0.5 ? K.r : K.ok, color: "#fff",
              fontFamily: "IDBlack", fontSize: 26, textAlign: "center", transform: "translateZ(160px) rotateX(-38deg)" }}>{red > 0.5 ? "GAJI TELAT" : "GAJI ✓"}</div>
          </div>;
        })}
      </div>
      <Words text="GAJI TELAT BARENGAN" at={T[9]} size={80} top={1290} />
    </AbsoluteFill>
  );
};

// ---------- S2 bayangin apartemen
const S2: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[11] - 0.08, T[17] - 0.05);
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1600 }}>
      <Words text="BAYANGIN APARTEMEN" at={T[11] - 0.05} size={76} top={340} color={K.y} />
      <Tower lit={(i) => ((i * 7) % 5 ? 1 : 0)} grow={ease(t, T[13], T[16] + 0.4, 0.05, 1)} ry={-30 + t * 6} scale={0.95} y={540} />
    </AbsoluteFill>
  );
};

// ---------- S3 fakta Mekari
const S3: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[17] - 0.08, T[48] - 0.05);
  const sp = useSp();
  const ph2 = ease(t, T[31] - 0.2, T[31] + 0.1);
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1300 }}>
      <Chip at={T[17]} left={60} top={330} bg={K.r} color={K.cr} size={44}>RABU, 25 NOV</Chip>
      <div style={{ position: "absolute", left: 470, top: 316, display: "flex", alignItems: "center", gap: 10, opacity: ease(t, T[22], T[22] + 0.2) }}>
        <Bug size={80} /><span style={{ fontFamily: "IDBlack", fontSize: 54, color: K.cr }}>MALWARE</span></div>
      <div style={{ opacity: 1 - ph2 }}>
        {APPS.map((n, i) => {
          const s = sp(T[20] + i * 0.1, 12);
          const off = ease(t, T[29] + i * 0.1, T[29] + i * 0.1 + 0.25);
          return <AppCard key={n} n={n} off={off} w={430} style={{ position: "absolute", left: 325 + (i % 2 ? 50 : -50), top: 480 + i * 150, opacity: s,
            transform: `rotateY(${(i % 2 ? -1 : 1) * 16 + (1 - s) * 60}deg)` }} />;
        })}
        <Chip at={T[25]} left={70} top={1300} bg={K.cr} size={32}>HR · GAJI · AKUNTANSI</Chip>
      </div>
      <div style={{ opacity: ph2 }}>
        <div style={{ position: "absolute", left: 230, top: 500, transform: `rotateX(${ease(t, T[31], T[31] + 0.5, 60, 8)}deg)` }}>
          <PayCard co="Gaji karyawan" st="TERTUNDA" c={K.y} /></div>
        <Chip at={T[35]} left={110} top={860} bg="#2B2440" color={K.cr} size={38}>⏳ Per Kamis: belum pulih total</Chip>
        <Chip at={T[41]} left={110} top={970} bg="#2B2440" color={K.cr} size={38}>❓ Data bocor: belum jelas</Chip>
      </div>
    </AbsoluteFill>
  );
};

// ---------- S4 SaaS = apartemen, listrik putus
const S4: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[48] - 0.08, T[84] - 0.05);
  const cut = (i: number) => (t < T[73] + ((i * 13) % 36) * 0.025 ? 1 : 0);
  const base = (i: number) => ((i * 7) % 5 ? 1 : 0) * cut(i);
  const hi = t > T[78] ? 18 : -1;
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1600 }}>
      <AbsoluteFill style={{ background: "rgba(0,0,0,.45)", opacity: ease(t, T[73], T[74] + 0.3) }} />
      <Words text="SaaS = APARTEMEN" at={T[48] - 0.05} size={84} top={340} accent={["SAAS"]} />
      <Tower lit={base} hi={hi} ry={-24 + Math.sin(t * 0.4) * 10} scale={0.82} y={480} x={330} />
      <Chip at={T[57]} left={60} top={620} bg={K.y} size={34}>⚡ Listrik</Chip>
      <Chip at={T[58]} left={60} top={720} bg={K.cr} size={34}>🛗 Lift</Chip>
      <Chip at={T[60]} left={60} top={820} bg={K.cr} size={34}>🛡 Satpam</Chip>
      <div style={{ position: "absolute", left: 60, top: 920, fontFamily: "IDBold", fontSize: 28, color: K.gy, opacity: ease(t, T[61], T[61] + 0.3) }}>dipakai bareng</div>
      <div style={{ opacity: 1 - ease(t, T[69] - 0.1, T[69] + 0.1) }}>
        <Chip at={T[63]} left={720} top={640} bg={K.ok} size={34}>Praktis</Chip>
        <Chip at={T[64]} left={720} top={740} bg={K.ok} size={34}>Murah</Chip>
      </div>
      <Words text="SEMUA IKUT GELAP" at={T[74]} size={84} top={1230} color={K.r} />
      <Chip at={T[79]} left={600} top={1350} bg={K.r} color={K.cr} size={30}>unit kamu nggak salah apa-apa</Chip>
    </AbsoluteFill>
  );
};

// ---------- S5 rumah sendiri
const S5: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[84] - 0.08, T[115] - 0.05);
  const sp = useSp();
  const bad = ease(t, T[107], T[107] + 0.3);
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1400 }}>
      <Words text="PINDAH KE RUMAH SENDIRI?" at={T[84] - 0.05} size={64} top={340} color={K.g2} />
      <div style={{ position: "absolute", left: 0, top: 560, width: 1080, height: 600, transformStyle: "preserve-3d", transform: `rotateX(-6deg) rotateY(${Math.sin(t * 0.5) * 8}deg)` }}>
        {[0, 1, 2].map((i) => {
          const s = sp(T[86] + i * 0.15, 12);
          return <div key={i} style={{ opacity: s, transform: `translateY(${(1 - s) * 300}px)` }}>
            <House x={80 + i * 330} y={60} lit={i === 1 ? 1 : 1 - bad} bad={i === 1 ? 0 : bad} ry={(i - 1) * -18} /></div>;
        })}
        <div style={{ position: "absolute", left: 410, top: 0, padding: "8px 18px", borderRadius: 12, background: K.ok, color: K.k, fontFamily: "IDBlack", fontSize: 28, opacity: ease(t, T[103], T[103] + 0.3) }}>RUMAHMU</div>
      </div>
      <Chip at={T[98]} left={150} top={1000} bg={K.cr} size={34}>🛠 Sistem kustom + database sendiri</Chip>
      <Words text="MASALAH TETANGGA ≠ RUMAHMU" at={T[107]} size={54} top={1150} color={K.y} />
    </AbsoluteFill>
  );
};

// ---------- S6 tapi ingat: kamu yang jaga
const S6: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[115] - 0.08, T[139] - 0.05);
  const fence = ease(t, T[118], T[118] + 0.6);
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1400 }}>
      <Words text="TAPI INGAT…" at={T[115] - 0.05} size={110} top={330} color={K.y} />
      <div style={{ position: "absolute", left: 0, top: 520, width: 1080, height: 520, transformStyle: "preserve-3d", transform: `rotateX(-8deg) rotateY(${-14 + Math.sin(t * 0.6) * 10}deg)` }}>
        <House x={430} y={40} lit={1} ry={0} db={false} />
        <svg viewBox="0 0 600 120" style={{ position: "absolute", left: 240, top: 300, width: 600, height: 120 }}>
          {Array.from({ length: 13 }, (_, i) => <rect key={i} x={i * 46 + 4} y={120 - 100 * Math.min(1, Math.max(0, fence * 13 - i))} width={18} height={100} rx={4} fill={K.cr} />)}
          <rect x={0} y={50} width={600 * fence} height={12} fill={K.cr} />
        </svg>
      </div>
      <Chip at={T[117]} left={90} top={1030} bg={K.y} size={40}>🔑 Kunci</Chip>
      <Chip at={T[118]} left={400} top={1030} bg={K.cr} size={40}>🚧 Pagar</Chip>
      <Chip at={T[120]} left={700} top={1030} bg={K.cr} size={40}>🛡 Satpam</Chip>
      <Words text="KAMU YANG JAGA" at={T[122]} size={84} top={1140} />
      <div style={{ opacity: ease(t, T[129] - 0.1, T[129] + 0.1) }}>
        <AbsoluteFill style={{ background: "rgba(10,8,18,.88)" }} />
        <Words text="KALAU MAU BERALIH" at={T[125]} size={84} top={330} color={K.g2} />
        <Chip at={T[131]} left={160} top={600} bg={K.ok} size={52}>🔐 Keamanan</Chip>
        <Chip at={T[133]} left={560} top={600} bg={K.ok} size={52}>💾 Backup</Chip>
        <Chip at={T[134]} left={180} top={760} bg={K.cr} size={44}>🤝 atau partner yang ngerti</Chip>
      </div>
    </AbsoluteFill>
  );
};

// ---------- S7 CTA + chibi
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
const S7: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[139] - 0.08, D.dur + 1, 0.18, 0.01);
  const opt = (at: number, l: string, txt: string, c: string, x: number) => {
    const s = useSp()(at, 10, 0.5);
    return <div style={{ position: "absolute", left: x, top: 470, width: 420, height: 130, borderRadius: 24, background: c, color: K.k, display: "flex", alignItems: "center",
      gap: 16, padding: "0 24px", fontFamily: "IDBlack", fontSize: 38, lineHeight: 1.05, opacity: s, transform: `scale(${0.5 + 0.5 * s})` }}>
      <div style={{ width: 64, height: 64, borderRadius: 32, background: K.k, color: c, display: "flex", alignItems: "center", justifyContent: "center", flex: "none" }}>{l}</div>{txt}</div>;
  };
  return (
    <AbsoluteFill style={{ opacity: op }}>
      <Words text="KAMU PILIH MANA?" at={T[139] - 0.05} size={92} top={340} />
      {opt(T[145], "A", "Apartemen", K.y, 100)}
      {opt(T[147], "B", "Rumah sendiri", K.ok, 560)}
      <Chip at={T[149]} left={290} top={620} bg={K.cr} size={40}>💬 Tulis di komentar</Chip>
      <Chibi />
    </AbsoluteFill>
  );
};

export const MekariC: React.FC = () => {
  useFonts();
  const { t } = useT();
  const flash = Math.max(...[T[9], T[29], T[73], T[107]].map((a) => (t >= a && t < a + 0.25 ? 0.3 * (1 - (t - a) / 0.25) : 0)));
  return (
    <AbsoluteFill style={{ background: `radial-gradient(120% 70% at 50% 40%, #1A1230 0%, ${K.k} 70%)`, overflow: "hidden" }}>
      <style>{fontCss}</style>
      <Audio src={f("vo_c.mp3")} />
      <Particles />
      <S1 /><S2 /><S3 /><S4 /><S5 /><S6 /><S7 />
      <div style={{ position: "absolute", left: 60, top: 262, display: "flex", alignItems: "center", gap: 12, fontFamily: "IDBold", fontSize: 24,
        letterSpacing: ".18em", color: K.cr }}><i style={{ width: 12, height: 12, borderRadius: 6, background: K.r, display: "inline-block" }} />KEAMANAN SIBER · SAAS</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1525, textAlign: "center", fontFamily: "IDBlack", fontSize: 36, color: K.cr }}>
        Endrich<span style={{ color: K.g2 }}>Tech</span></div>
      <AbsoluteFill style={{ background: "#fff", opacity: flash, pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};
