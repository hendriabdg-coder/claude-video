// Reel 9:16 · "Lima aplikasi mati, gaji nyangkut" (Mekari kena malware 25 Nov 2026) · VO manual Endrich (63,2 dtk, opsi B).
// Timing: motion/proyek/2026-11-27-mekari-malware/align.py -> mekari-data.json. Helper sama dengan CeoNvidia/OpenaiDigugat.
// Aset logo 5 aplikasi, foto CEO, surat maaf: di-crop dari video Course-Net kiriman Endrich. Efek 3D CSS.
import React from "react";
import { AbsoluteFill, Audio, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, continueRender, delayRender } from "remotion";
import D from "./mekari-data.json";

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

// ---------- S1 hook: 5 aplikasi mati
const S1: React.FC = () => {
  const { t } = useT();
  const op = win(t, 0, T[11] - 0.05, 0.01);
  const sp = useSp();
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1400 }}>
      <Words text="5 APLIKASI MATI" at={0} size={110} top={330} color={K.r} accent={["5"]} />
      <div style={{ position: "absolute", left: 0, top: 540, width: 1080, height: 700, transformStyle: "preserve-3d", transform: `rotateX(10deg) rotateY(${Math.sin(t * 0.9) * 10}deg)`,
        opacity: 1 - ease(t, T[3] - 0.1, T[3] + 0.2) * 0.75 }}>
        {APPS.map((n, i) => {
          const s = sp(0.1 + i * 0.1, 12);
          const off = ease(t, T[2] + i * 0.08, T[2] + i * 0.08 + 0.25);
          return <AppCard key={n} n={n} off={off} w={470} style={{ position: "absolute", left: 305 + (i % 2 ? 60 : -60), top: i * 135,
            opacity: s, transform: `translateZ(${(1 - s) * -800}px) rotateY(${(i % 2 ? -1 : 1) * 14}deg)` }} />;
        })}
      </div>
      <div style={{ position: "absolute", left: 230, top: 760, opacity: ease(t, T[3], T[3] + 0.2) * (1 - ease(t, T[7] - 0.1, T[7] + 0.1)), transform: `rotateX(${ease(t, T[3], T[3] + 0.4, 60, 6)}deg) scale(1.15)` }}>
        <PayCard co="Gaji ribuan karyawan" st="PENDING" c={K.y} />
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 760, display: "flex", justifyContent: "center", alignItems: "center", gap: 20,
        opacity: ease(t, T[7], T[7] + 0.2), transform: `scale(${0.6 + 0.4 * ease(t, T[7], T[7] + 0.3)})`, background: "rgba(10,8,18,.92)", padding: "40px 0" }}>
        <Bug size={170} /><div style={{ fontFamily: "IDBlack", fontSize: 100, color: K.cr }}>1 MALWARE</div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- S2 rangkuman 1 menit
const S2: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[11] - 0.08, T[24] - 0.05);
  const p = ease(t, T[11], T[17] + 0.6);
  const C = 2 * Math.PI * 200;
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1200 }}>
      <Words text="KASUS MEKARI" at={T[11] - 0.05} size={110} top={330} color={K.g2} />
      <div style={{ position: "absolute", left: 290, top: 560, width: 500, height: 500, transform: `rotateX(${Math.sin(t) * 12}deg) rotateY(${Math.cos(t * 0.8) * 16}deg)` }}>
        <svg viewBox="0 0 500 500" style={{ width: 500, height: 500 }}>
          <circle cx="250" cy="250" r="200" stroke="rgba(244,241,234,.15)" strokeWidth={26} fill="none" />
          <circle cx="250" cy="250" r="200" stroke={K.g} strokeWidth={26} fill="none" strokeLinecap="round" strokeDasharray={C} strokeDashoffset={C * (1 - p)} transform="rotate(-90 250 250)" />
        </svg>
        <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
          <div style={{ fontFamily: "IDBlack", fontSize: 150, color: K.cr, lineHeight: 1 }}>1</div>
          <div style={{ fontFamily: "IDBold", fontSize: 46, color: K.g2, letterSpacing: ".1em" }}>MENIT</div>
        </div>
      </div>
      <Chip at={T[18]} left={270} top={1140} bg={K.y} size={46}>+1 pelajaran langka</Chip>
    </AbsoluteFill>
  );
};

// ---------- S3 kronologi
const S3: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[24] - 0.08, T[54] - 0.05);
  const sp = useSp();
  const ph2 = ease(t, T[47] - 0.2, T[47] + 0.1);
  const logs = [[T[30], "aktivitas tidak biasa", K.y], [T[33], "termasuk sistem pihak ketiga", K.y], [T[43], "DIKONFIRMASI: SERANGAN SIBER", K.r]] as const;
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1300 }}>
      <div style={{ opacity: 1 - ph2 }}>
        <Chip at={T[24]} left={60} top={330} bg={K.r} color={K.cr} size={44}>RABU, 25 NOV · PAGI</Chip>
        <div style={{ position: "absolute", left: 90, top: 470, width: 900, height: 600, borderRadius: 26, background: "#110F18", border: "2px solid rgba(255,79,58,.45)",
          padding: "28px 34px", fontFamily: "Consolas, 'Courier New', monospace", fontSize: 36, color: "#FFD9D2",
          transform: `rotateX(${(1 - sp(T[28] - 0.2, 14)) * 50 + 6}deg)`, opacity: sp(T[28] - 0.2, 14) }}>
          <div style={{ fontFamily: "IDBold", fontSize: 22, letterSpacing: ".16em", color: K.gy, marginBottom: 20 }}>LOG KEAMANAN · ILUSTRASI</div>
          {logs.map(([at, msg, c], i) => <div key={i} style={{ margin: "22px 0", opacity: ease(t, at, at + 0.15), whiteSpace: "nowrap" }}>
            <span style={{ color: K.gy }}>{["07:4x", "07:5x", "--:--"][i]}</span> <span style={{ color: c }}>● {msg}</span></div>)}
          <div style={{ position: "absolute", right: 40, bottom: 30, opacity: ease(t, T[37], T[37] + 0.3) }}>
            <svg viewBox="0 0 200 120" style={{ width: 300, height: 180 }} fill="none" strokeWidth={4}>
              <rect x="10" y="40" width="60" height="40" rx="8" stroke={K.g2} /><rect x="130" y="10" width="60" height="40" rx="8" stroke={K.y} />
              <rect x="130" y="70" width="60" height="40" rx="8" stroke={K.y} /><path d="M70 60L130 30M70 60L130 90" stroke={K.r} strokeDasharray="8 6" />
            </svg>
          </div>
        </div>
        <Stamp at={T[43]} text="SERANGAN SIBER" color={K.r} top={1130} size={90} />
      </div>
      <div style={{ opacity: ph2 }}>
        <Words text="SEMUA APLIKASI DIMATIKAN" at={T[47]} size={62} top={340} />
        {APPS.map((n, i) => {
          const s = sp(T[47] + i * 0.1, 12);
          const sw = ease(t, T[50] + i * 0.1, T[50] + i * 0.1 + 0.25);
          return (
            <div key={n} style={{ position: "absolute", left: 120, top: 460 + i * 160, display: "flex", alignItems: "center", gap: 40, opacity: s,
              transform: `translateX(${(1 - s) * -300}px) rotateY(${(1 - s) * 50}deg)` }}>
              <AppCard n={n} off={sw} w={420} />
              <div style={{ width: 150, height: 74, borderRadius: 37, background: sw > 0.5 ? "#3A3448" : K.ok, position: "relative" }}>
                <div style={{ position: "absolute", top: 7, left: 7 + (1 - sw) * 76, width: 60, height: 60, borderRadius: 30, background: K.cr }} /></div>
            </div>
          );
        })}
        <Chip at={T[52]} left={300} top={1290} bg={K.ok} size={36}>🛡 biar datanya aman</Chip>
      </div>
    </AbsoluteFill>
  );
};

// ---------- S4 dampak gaji
const S4: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[54] - 0.08, T[63] - 0.05);
  const sp = useSp();
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1300 }}>
      <Words text="DAMPAKNYA LANGSUNG TERASA" at={T[54] - 0.05} size={76} top={330} color={K.y} />
      {["Perusahaan A", "Perusahaan B", "Perusahaan C"].map((co, i) => {
        const s = sp(T[55] + i * 0.3, 13);
        return <div key={co} style={{ position: "absolute", left: 230 + (i - 1) * 40, top: 520 + i * 250, opacity: s,
          transform: `translateZ(${(1 - s) * 600}px) rotateX(${(1 - s) * 60 + 10}deg) rotateZ(${(i - 1) * 3}deg)` }}>
          <PayCard co={co} st={i === 1 ? "GAGAL" : "TERTUNDA"} c={i === 1 ? K.r : K.y} /></div>;
      })}
      <div style={{ position: "absolute", left: 0, right: 0, top: 1360, textAlign: "center", fontFamily: "IDBold", fontSize: 22, letterSpacing: ".14em", color: K.gy,
        opacity: ease(t, T[58], T[58] + 0.3) }}>ILUSTRASI · NAMA PERUSAHAAN BUKAN DATA ASLI</div>
    </AbsoluteFill>
  );
};

// ---------- S5 CEO minta maaf + infrastruktur baru + target pulih
const S5: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[63] - 0.08, T[83] - 0.05);
  const ph2 = ease(t, T[71] - 0.2, T[71] + 0.1);
  const split = ease(t, T[74], T[75] + 0.5);
  const prog = interpolate(t, [T[79], T[81], T[82], T[82] + 0.6], [0, 0.45, 0.55, 0.62], cl);
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1300 }}>
      <div style={{ opacity: 1 - ph2 }}>
        <Words text="CEO MINTA MAAF" at={T[63] - 0.05} size={92} top={330} />
        <div style={{ position: "absolute", left: 70, top: 540, width: 470, height: 391, transform: `rotateY(${ease(t, T[63], T[63] + 0.6, -50, 12)}deg)`, opacity: ease(t, T[63], T[63] + 0.3) }}>
          <Img src={f("ceo.png")} style={{ width: 470, height: 391, borderRadius: 24, objectFit: "cover", boxShadow: "0 40px 90px rgba(0,0,0,.6)", border: `4px solid ${K.g}` }} />
          <div style={{ position: "absolute", left: 20, bottom: -40, padding: "10px 20px", borderRadius: 14, background: K.cr, color: K.k, fontFamily: "IDBlack", fontSize: 32 }}>
            Suwandi Soh <span style={{ fontFamily: "IDBold", fontSize: 20, color: "#666" }}>CEO MEKARI</span></div>
        </div>
        <div style={{ position: "absolute", left: 560, top: 520, width: 460, height: 548, opacity: ease(t, T[65], T[65] + 0.3),
          transform: `rotateY(${ease(t, T[65], T[65] + 0.7, 70, -10)}deg) rotateZ(3deg) translateZ(${ease(t, T[65], T[65] + 0.7, 400, 0)}px)` }}>
          <Img src={f("surat.png")} style={{ width: 460, height: 548, borderRadius: 10, boxShadow: "0 40px 90px rgba(0,0,0,.6)" }} />
        </div>
        <div style={{ position: "absolute", left: 0, right: 0, top: 1180, textAlign: "center", fontFamily: "IDBold", fontSize: 22, letterSpacing: ".14em", color: K.gy }}>
          SURAT RESMI MEKARI · 25 NOV 2026 · VIA COURSE-NET</div>
      </div>
      <div style={{ opacity: ph2 }}>
        <Words text="INFRASTRUKTUR BARU" at={T[71]} size={80} top={330} color={K.g2} />
        <div style={{ position: "absolute", left: 90, top: 520, width: 900, height: 560, transformStyle: "preserve-3d", transform: `rotateX(18deg) rotateY(${-10 + Math.sin(t * 0.7) * 8}deg)` }}>
          {[0, 1].map((side) => (
            <div key={side} style={{ position: "absolute", left: side ? 520 + split * 60 : 60 - split * 60, top: 60, width: 320, height: 420, transformStyle: "preserve-3d" }}>
              {[0, 1, 2, 3].map((r) => <div key={r} style={{ position: "absolute", left: 0, top: r * 100, width: 320, height: 86, borderRadius: 14,
                background: side ? "#173A2A" : "#3A1717", border: `3px solid ${side ? K.ok : K.r}`, transform: `translateZ(${r * 6}px)`,
                display: "flex", alignItems: "center", gap: 12, padding: "0 20px" }}>
                {[0, 1, 2].map((d) => <i key={d} style={{ width: 14, height: 14, borderRadius: 7, background: side ? K.ok : (t * 6 + d) % 2 < 1 ? K.r : "#5a2a2a" }} />)}</div>)}
              <div style={{ position: "absolute", left: 0, right: 0, top: 430, textAlign: "center", fontFamily: "IDBlack", fontSize: 40, color: side ? K.ok : K.r }}>{side ? "SISTEM BARU" : "SISTEM LAMA ✕"}</div>
            </div>
          ))}
        </div>
        <Chip at={T[74]} left={330} top={1110} bg={K.cr} size={40}>↔ TERPISAH TOTAL</Chip>
        <div style={{ position: "absolute", left: 140, top: 1240, width: 800, opacity: ease(t, T[79], T[79] + 0.3) }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontFamily: "IDBold", fontSize: 32, color: K.cr, marginBottom: 12 }}>
            <span>TARGET PULIH: JUMAT</span><span style={{ color: K.y }}>BERTAHAP</span></div>
          <div style={{ height: 30, borderRadius: 15, background: "rgba(244,241,234,.15)", overflow: "hidden" }}>
            <div style={{ height: "100%", width: `${prog * 100}%`, background: `linear-gradient(90deg, ${K.g}, ${K.ok})` }} /></div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- diagram: database bersama vs terpisah
const Building: React.FC<{ x: number; y: number; bad: number; label?: string }> = ({ x, y, bad, label }) => (
  <div style={{ position: "absolute", left: x - 60, top: y - 60, width: 120, height: 120, borderRadius: 22, background: bad > 0.5 ? "#3A1717" : "#1E1A2C",
    border: `4px solid ${bad > 0.5 ? K.r : K.g2}`, display: "flex", alignItems: "center", justifyContent: "center", boxShadow: bad > 0.5 ? "0 0 40px rgba(255,79,58,.6)" : "none" }}>
    <svg viewBox="0 0 100 100" style={{ width: 70, height: 70 }} fill="none" stroke={bad > 0.5 ? K.r : K.cr} strokeWidth={6}>
      <rect x="22" y="14" width="56" height="76" rx="4" /><path d="M34 28h8M58 28h8M34 44h8M58 44h8M34 60h8M58 60h8M44 90V76h12v14" /></svg>
    {label && <div style={{ position: "absolute", top: 126, fontFamily: "IDBold", fontSize: 22, color: K.gy, whiteSpace: "nowrap" }}>{label}</div>}
  </div>
);
const DB: React.FC<{ x: number; y: number; s: number; bad: number }> = ({ x, y, s, bad }) => (
  <svg viewBox="0 0 100 100" style={{ position: "absolute", left: x - s / 2, top: y - s / 2, width: s, height: s }} fill={bad > 0.5 ? "#3A1717" : "#1E1A2C"} stroke={bad > 0.5 ? K.r : K.g} strokeWidth={5}>
    <path d="M18 22v56c0 6 14 11 32 11s32-5 32-11V22" /><ellipse cx="50" cy="22" rx="32" ry="11" /><path d="M18 50c0 6 14 11 32 11s32-5 32-11" fill="none" />
  </svg>
);
const S6: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[83] - 0.08, T[101] - 0.05);
  const inf = ease(t, T[94], T[100] + 0.3);
  const N = 6, cx = 540, cy = 900, R = 330;
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1300 }}>
      <Words text="PELAJARANNYA: TERPISAH" at={T[83] - 0.05} size={80} top={330} color={K.y} accent={["TERPISAH"]} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 430, textAlign: "center", fontFamily: "IDBold", fontSize: 40, color: K.gy, opacity: ease(t, T[91], T[91] + 0.3) }}>APLIKASI BERSAMA</div>
      <AbsoluteFill style={{ transform: `rotateX(28deg) rotateZ(${Math.sin(t * 0.4) * 6}deg)`, transformOrigin: `${cx}px ${cy}px`, opacity: ease(t, T[91] - 0.2, T[91] + 0.4) }}>
        <svg style={{ position: "absolute", inset: 0, width: 1080, height: 1920 }}>
          {Array.from({ length: N }, (_, i) => { const a = (i / N) * Math.PI * 2 - Math.PI / 2; return <line key={i} x1={cx} y1={cy} x2={cx + Math.cos(a) * R} y2={cy + Math.sin(a) * R}
            stroke={inf * N > i ? K.r : "rgba(169,139,255,.5)"} strokeWidth={6} strokeDasharray="14 10" strokeDashoffset={-t * 60} />; })}
        </svg>
        <DB x={cx} y={cy} s={220} bad={inf > 0.02 ? 1 : 0} />
        {Array.from({ length: N }, (_, i) => { const a = (i / N) * Math.PI * 2 - Math.PI / 2; return <Building key={i} x={cx + Math.cos(a) * R} y={cy + Math.sin(a) * R} bad={inf * N > i + 0.5 ? 1 : 0} />; })}
      </AbsoluteFill>
      <Words text="1 MASALAH → SEMUA KENA" at={T[97]} size={70} top={1330} color={K.r} />
    </AbsoluteFill>
  );
};
const S7: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[101] - 0.08, T[132] - 0.05);
  const ph2 = ease(t, T[114] - 0.2, T[114] + 0.2);
  const bad = ease(t, T[120], T[120] + 0.3);
  const pos = [[260, 760], [540, 700], [820, 760], [260, 1080], [540, 1140], [820, 1080]];
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1300 }}>
      <div style={{ opacity: 1 - ph2 }}>
        <Words text="DATA PALING SENSITIF" at={T[101] - 0.05} size={84} top={330} />
        <Chip at={T[108]} left={150} top={600} bg={K.y} size={56}>💸 GAJI</Chip>
        <Chip at={T[110]} left={530} top={600} bg={K.g2} size={56}>📊 KEUANGAN</Chip>
        <div style={{ position: "absolute", left: 340, top: 760, width: 400, height: 400, transform: `rotateY(${t * 40}deg)`, opacity: ease(t, T[106], T[106] + 0.3) }}>
          <DB x={200} y={200} s={360} bad={0} /></div>
      </div>
      <div style={{ opacity: ph2 }}>
        <Words text="DATABASE KHUSUS PERUSAHAANMU" at={T[114]} size={66} top={330} color={K.g2} />
        <AbsoluteFill style={{ transform: "rotateX(26deg)", transformOrigin: "540px 920px" }}>
          {pos.map(([x, y], i) => (
            <React.Fragment key={i}>
              <div style={{ position: "absolute", left: x - 125, top: y - 150, width: 250, height: 290, borderRadius: 30, border: `3px dashed ${i === 0 && bad > 0.5 ? K.r : "rgba(169,139,255,.45)"}` }} />
              <Building x={x} y={y - 55} bad={i === 0 ? bad : 0} />
              <DB x={x} y={y + 70} s={90} bad={i === 0 ? bad : 0} />
            </React.Fragment>
          ))}
        </AbsoluteFill>
        <Chip at={T[121] + 0.2} left={520} top={1290} bg={K.ok} size={34}>yang lain tetap aman ✓</Chip>
        <Chip at={T[123]} left={90} top={1380} bg={K.cr} size={34}>🛠 Tools kustom</Chip>
        <Chip at={T[127]} left={450} top={1380} bg={K.cr} size={34}>📦 Paket dedicated vendor</Chip>
      </div>
    </AbsoluteFill>
  );
};

// ---------- S8 checklist
const S8: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[132] - 0.08, T[146] - 0.05);
  const sp = useSp();
  const items = [[T[134], "Tahu data disimpan di mana"], [T[140], "Punya rencana kalau sistem mati"], [T[132] + 0.3, "Tetap butuh keamanan & backup"]] as const;
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1300 }}>
      <Words text="YANG PENTING" at={T[132] - 0.05} size={110} top={330} color={K.y} />
      {[items[0], items[1]].map(([at, txt], i) => {
        const s = sp(at, 13); const c = ease(t, at + 0.4, at + 0.7);
        return <div key={i} style={{ position: "absolute", left: 90, top: 560 + i * 230, width: 900, height: 190, borderRadius: 30, background: K.card,
          border: `3px solid ${c > 0.5 ? K.ok : "rgba(244,241,234,.18)"}`, display: "flex", alignItems: "center", gap: 34, padding: "0 40px", opacity: s,
          transform: `rotateX(${(1 - s) * 70}deg) translateZ(${(1 - s) * 300}px)` }}>
          <div style={{ width: 110, height: 110, borderRadius: 26, border: `6px solid ${K.ok}`, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <span style={{ fontFamily: "IDBlack", fontSize: 76, color: K.ok, transform: `scale(${c})` }}>✓</span></div>
          <div style={{ fontFamily: "IDBlack", fontSize: 50, color: K.cr, lineHeight: 1.05 }}>{txt}</div>
        </div>;
      })}
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
  const op = win(t, T[146] - 0.08, D.dur + 1, 0.18, 0.01);
  const opt = (at: number, l: string, txt: string, c: string, x: number) => {
    const s = useSp()(at, 10, 0.5);
    return <div style={{ position: "absolute", left: x, top: 470, width: 420, height: 130, borderRadius: 24, background: c, color: K.k, display: "flex", alignItems: "center",
      gap: 16, padding: "0 24px", fontFamily: "IDBlack", fontSize: 38, lineHeight: 1.05, opacity: s, transform: `scale(${0.5 + 0.5 * s})` }}>
      <div style={{ width: 64, height: 64, borderRadius: 32, background: K.k, color: c, display: "flex", alignItems: "center", justifyContent: "center", flex: "none" }}>{l}</div>{txt}</div>;
  };
  return (
    <AbsoluteFill style={{ opacity: op }}>
      <Words text="KANTORMU PAKAI APA?" at={T[146] - 0.05} size={78} top={340} />
      {opt(T[152], "A", "Aplikasi bersama", K.g2, 100)}
      {opt(T[155], "B", "Sistem sendiri", K.ok, 560)}
      <Chip at={T[157]} left={290} top={620} bg={K.cr} size={40}>💬 Tulis di komentar</Chip>
      <Chibi />
    </AbsoluteFill>
  );
};

export const Mekari: React.FC = () => {
  useFonts();
  const { t } = useT();
  const flash = Math.max(...[T[2], T[43], T[50], T[74], T[97]].map((a) => (t >= a && t < a + 0.25 ? 0.3 * (1 - (t - a) / 0.25) : 0)));
  return (
    <AbsoluteFill style={{ background: `radial-gradient(120% 70% at 50% 40%, #1A1230 0%, ${K.k} 70%)`, overflow: "hidden" }}>
      <style>{fontCss}</style>
      <Audio src={f("vo.mp3")} />
      <Particles />
      <S1 /><S2 /><S3 /><S4 /><S5 /><S6 /><S7 /><S8 /><S9 />
      <div style={{ position: "absolute", left: 60, top: 262, display: "flex", alignItems: "center", gap: 12, fontFamily: "IDBold", fontSize: 24,
        letterSpacing: ".18em", color: K.cr }}><i style={{ width: 12, height: 12, borderRadius: 6, background: K.r, display: "inline-block" }} />KEAMANAN SIBER · SAAS</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1525, textAlign: "center", fontFamily: "IDBlack", fontSize: 36, color: K.cr }}>
        Endrich<span style={{ color: K.g2 }}>Tech</span></div>
      <AbsoluteFill style={{ background: "#fff", opacity: flash, pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};
