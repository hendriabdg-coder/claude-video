// Reel 9:16 · "OpenAI dihantam 3 masalah hukum dalam 3 hari" (California 16 Nov, Oregon 17 Nov, Arizona 18 Nov 2026) · VO manual Endrich (63,8 dtk)
// Timing: motion/proyek/2026-11-25-openai-digugat/align.py -> openai-digugat-data.json. Helper sama dengan CeoNvidia.tsx. Sumber: riset.md.
// Efek 3D CSS: kalender flip, panel ilustrasi parallax, 80 titik insiden, timbangan, dokumen bertumpuk, kartu berita miring,
// pita police line 3D, simpul logo ekstrusi, gedung pengadilan, chibi di penutup.
import React from "react";
import { AbsoluteFill, Audio, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, continueRender, delayRender } from "remotion";
import D from "./openai-digugat-data.json";

const T: number[] = D.T;
const K = { k: "#07090C", g: "#10A37F", g2: "#3EE6B8", r: "#FF4F3A", cr: "#F4F1EA", gy: "#8A909A", y: "#F5B301", card: "#11151A", b: "#5B8CFF" };
const f = (n: string) => staticFile(`openai-digugat/${n}`);
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
        backgroundImage: `linear-gradient(rgba(16,163,127,.22) 2px, transparent 2px), linear-gradient(90deg, rgba(16,163,127,.22) 2px, transparent 2px)`,
        backgroundSize: "90px 90px", backgroundPosition: `0 ${(t * 60) % 90}px`, opacity: 0.5,
        maskImage: "linear-gradient(transparent, black 60%)", WebkitMaskImage: "linear-gradient(transparent, black 60%)" }} />
    </AbsoluteFill>
  );
};

// ---------- komponen bersama
const DayCard: React.FC<{ day: string; state: string; at: number; x: number; y: number; w?: number; color?: string; rot?: number }> =
  ({ day, state, at, x, y, w = 260, color = K.r, rot = 0 }) => {
    const s = useSp()(at, 12, 0.6);
    return (
      <div style={{ position: "absolute", left: x, top: y, width: w, height: w * 1.15, transformStyle: "preserve-3d", opacity: Math.min(1, s * 1.4),
        transform: `rotateX(${(1 - s) * -90}deg) rotateZ(${rot}deg)`, transformOrigin: "50% 0" }}>
        <div style={{ position: "absolute", inset: 0, borderRadius: 26, background: K.cr, overflow: "hidden", boxShadow: "0 40px 80px rgba(0,0,0,.6)" }}>
          <div style={{ height: w * 0.28, background: color, color: K.cr, fontFamily: "IDBold", fontSize: w * 0.11, letterSpacing: ".12em",
            display: "flex", alignItems: "center", justifyContent: "center" }}>NOV 2026</div>
          <div style={{ fontFamily: "IDBlack", fontSize: w * 0.42, color: K.k, textAlign: "center", marginTop: w * 0.04 }}>{day}</div>
          <div style={{ fontFamily: "IDBold", fontSize: w * 0.1, color: "#444", textAlign: "center", letterSpacing: ".06em" }}>{state}</div>
        </div>
      </div>
    );
  };

const Knot: React.FC<{ size: number; x: number; y: number; ry: number; rx?: number; layers?: number; tint?: string }> = ({ size, x, y, ry, rx = 0, layers = 12, tint = K.cr }) => (
  <div style={{ position: "absolute", left: x, top: y, width: size, height: size, transformStyle: "preserve-3d", transform: `rotateY(${ry}deg) rotateX(${rx}deg)` }}>
    {Array.from({ length: layers }, (_, i) => (
      <div key={i} style={{ position: "absolute", inset: 0, transform: `translateZ(${-i * 3}px)`, backgroundColor: i ? `rgba(16,163,127,${0.9 - i * 0.06})` : tint,
        WebkitMaskImage: `url(${f("knot.png")})`, maskImage: `url(${f("knot.png")})`, WebkitMaskSize: "contain", maskSize: "contain" }} />
    ))}
  </div>
);

const DayHead: React.FC<{ n: string; state: string; at: number; color: string }> = ({ n, state, at, color }) => (
  <>
    <Chip at={at} left={60} top={330} bg={color} color={K.cr} size={40}>HARI {n}</Chip>
    <Words text={state} at={at + 0.15} size={state.length > 12 ? 64 : 110} top={420} />
  </>
);

// ---------- S1 hook
const S1: React.FC = () => {
  const { t } = useT();
  const op = win(t, 0, T[9] - 0.05, 0.01);
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1500 }}>
      <div style={{ position: "absolute", left: 60, top: 560, width: 960, height: 640, transformStyle: "preserve-3d",
        transform: `rotateY(${ease(t, 0, 3.5, -18, 10)}deg) rotateX(6deg) translateZ(${ease(t, 0, 0.6, -500, 0)}px)` }}>
        <Img src={f("altman.png")} style={{ width: 960, height: 640, objectFit: "cover", borderRadius: 30, boxShadow: "0 50px 120px rgba(0,0,0,.7)",
          filter: `brightness(${0.85 - ease(t, T[5], T[6], 0, 0.35)})` }} />
        <div style={{ position: "absolute", left: 30, bottom: 30, padding: "10px 22px", borderRadius: 14, background: "rgba(7,9,12,.8)", color: K.cr,
          fontFamily: "IDBold", fontSize: 26, transform: "translateZ(60px)" }}>Sam Altman · CEO OpenAI</div>
      </div>
      <Words text="3 HARI · 3 MASALAH HUKUM" at={0} size={92} top={330} accent={["3"]} />
      {[["16", "CALIFORNIA"], ["17", "OREGON"], ["18", "ARIZONA"]].map(([d, s], i) => (
        <DayCard key={d} day={d} state={s} at={T[5] + i * 0.25} x={90 + i * 320} y={1180} w={260} rot={(i - 1) * 4} />
      ))}
    </AbsoluteFill>
  );
};

// ---------- S2 California: agent lolos & serang Hugging Face
const S2: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[9] - 0.08, T[34] - 0.05);
  const pz = ease(t, T[13], T[34], 0, 1);
  const hrs = ease(t, T[30], T[33] + 0.4, 0, 60);
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1300 }}>
      <DayHead n="1" state="CALIFORNIA MENGGUGAT" at={T[9] - 0.05} color={K.r} />
      <div style={{ position: "absolute", left: 90, top: 580, width: 900, height: 795, transformStyle: "preserve-3d", opacity: ease(t, T[13] - 0.2, T[13] + 0.3),
        transform: `rotateY(${-14 + pz * 20}deg) rotateX(8deg) translateZ(${ease(t, T[13] - 0.2, T[13] + 0.5, -600, 0)}px)` }}>
        <div style={{ position: "absolute", inset: 0, borderRadius: 30, overflow: "hidden", boxShadow: "0 50px 120px rgba(0,0,0,.7)" }}>
          <Img src={f("ilustrasi.png")} style={{ position: "absolute", left: -40, top: -30, width: 980, height: 866, transform: `translate(${pz * 40}px, ${pz * 20}px) scale(${1.04 + pz * 0.06})` }} />
        </div>
        <div style={{ position: "absolute", right: 20, top: 20, padding: "6px 14px", borderRadius: 8, background: "rgba(7,9,12,.7)", color: K.gy, fontFamily: "IDBold",
          fontSize: 20, letterSpacing: ".14em", transform: "translateZ(40px)" }}>ILUSTRASI AI</div>
        <div style={{ position: "absolute", left: 24, top: 24, padding: "16px 24px", borderRadius: 18, background: "rgba(7,9,12,.82)", transform: "translateZ(90px)", opacity: ease(t, T[14], T[14] + 0.3) }}>
          <div style={{ fontFamily: "IDBlack", fontSize: 64, color: K.cr, textShadow: "0 4px 20px #000" }}>±700 AI agent</div>
          <div style={{ fontFamily: "IDBold", fontSize: 30, color: K.g2 }}>lolos dari lingkungan uji · Juli 2026</div>
        </div>
        <div style={{ position: "absolute", left: 30, bottom: 30, padding: "18px 26px", borderRadius: 20, background: "rgba(255,79,58,.92)", color: K.cr,
          transform: "translateZ(120px)", opacity: ease(t, T[27], T[27] + 0.3) }}>
          <div style={{ fontFamily: "IDBold", fontSize: 26, letterSpacing: ".1em" }}>MENYERANG HUGGING FACE</div>
          <div style={{ fontFamily: "IDBlack", fontSize: 64 }}>±{Math.round(hrs)} JAM <span style={{ fontSize: 34 }}>(≈2,5 hari)</span></div>
        </div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1420, textAlign: "center", fontFamily: "IDBold", fontSize: 22, letterSpacing: ".14em", color: K.gy,
        opacity: ease(t, T[14], T[14] + 0.3) }}>MENURUT GUGATAN · 16 NOV 2026</div>
    </AbsoluteFill>
  );
};

// ---------- S3 80+ kehilangan kendali + timbangan
const S3: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[34] - 0.08, T[54] - 0.05);
  const n = Math.round(ease(t, T[38], T[43] + 0.5, 0, 80));
  const phase2 = ease(t, T[45] - 0.2, T[45] + 0.1);
  const tilt = ease(t, T[51], T[52] + 0.6, 0, -14);
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1300 }}>
      <div style={{ opacity: 1 - phase2 }}>
        <Words text="KEHILANGAN KENDALI" at={T[34] - 0.05} size={80} top={330} color={K.r} />
        <div style={{ position: "absolute", left: 0, right: 0, top: 470, textAlign: "center", fontFamily: "IDBlack", fontSize: 300, color: K.cr, lineHeight: 1,
          textShadow: "0 0 80px rgba(255,79,58,.45)" }}>{n}+</div>
        <div style={{ position: "absolute", left: 140, top: 820, width: 800, height: 420, transformStyle: "preserve-3d", transform: `rotateX(48deg) rotateZ(${Math.sin(t * 0.8) * 8}deg)` }}>
          {Array.from({ length: 80 }, (_, i) => {
            const on = i < n;
            return <div key={i} style={{ position: "absolute", left: (i % 10) * 80 + 20, top: Math.floor(i / 10) * 52, width: 40, height: 40, borderRadius: 10,
              background: on ? K.r : "#1c2128", boxShadow: on ? "0 0 20px rgba(255,79,58,.7)" : "none", transform: `translateZ(${on ? 20 : 0}px)` }} />;
          })}
        </div>
        <div style={{ position: "absolute", left: 0, right: 0, top: 1300, textAlign: "center", fontFamily: "IDBold", fontSize: 36, color: K.gy }}>kali agent lepas kendali (diakui OpenAI)</div>
      </div>
      <div style={{ opacity: phase2 }}>
        <Words text="BUDAYA PERUSAHAAN" at={T[45]} size={84} top={330} />
        <div style={{ position: "absolute", left: 90, top: 620, width: 900, height: 600, transformStyle: "preserve-3d", transform: `rotateX(10deg) rotateY(${Math.sin(t) * 10}deg)` }}>
          <div style={{ position: "absolute", left: 442, top: 120, width: 16, height: 440, background: "rgba(244,241,234,.5)", borderRadius: 8 }} />
          <div style={{ position: "absolute", left: 90, top: 110, width: 720, height: 18, borderRadius: 9, background: K.cr, transform: `rotate(${tilt}deg)` }}>
            {[["PERTUMBUHAN", K.g, -1], ["KESELAMATAN", K.r, 1]].map(([lab, c, side], i) => (
              <div key={i} style={{ position: "absolute", left: i ? 600 : -60, top: 18, width: 240, textAlign: "center", transform: `rotate(${-tilt}deg)`, transformOrigin: "50% 0" }}>
                <div style={{ width: 4, height: 120, background: "rgba(244,241,234,.6)", margin: "0 auto" }} />
                <div style={{ height: 30, borderRadius: "0 0 120px 120px", background: c as string }} />
                <div style={{ fontFamily: "IDBlack", fontSize: 38, color: c as string, marginTop: 14 }}>{lab}</div>
              </div>
            ))}
          </div>
        </div>
        <Words text="PERTUMBUHAN > KESELAMATAN" at={T[49]} size={60} top={1260} color={K.y} />
      </div>
    </AbsoluteFill>
  );
};

// ---------- S4 dasar gugatan: 2 dokumen
const S4: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[54] - 0.08, T[64] - 0.05);
  const sp = useSp();
  const docs = [["GANGGUAN PUBLIK", "Public nuisance", T[57]], ["UU PERSAINGAN USAHA", "Unfair Competition Law", T[61]]] as const;
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1300 }}>
      <Words text="PASAL YANG DIPAKAI" at={T[54] - 0.05} size={96} top={330} />
      {docs.map(([a, b, at], i) => {
        const s = sp(at, 13, 0.7);
        return (
          <div key={i} style={{ position: "absolute", left: 130 + i * 60, top: 580 + i * 330, width: 760, height: 300, borderRadius: 18, background: "#F2EDE2",
            color: "#141414", padding: "34px 40px", opacity: s, boxShadow: "0 40px 90px rgba(0,0,0,.6)",
            transform: `translateZ(${(1 - s) * 600}px) rotateX(${(1 - s) * 60 + 10}deg) rotateZ(${i ? 2 : -2}deg)` }}>
            <div style={{ fontFamily: "IDBold", fontSize: 22, letterSpacing: ".16em", color: "#8a2b16" }}>DASAR GUGATAN {i + 1}</div>
            <div style={{ fontFamily: "IDBlack", fontSize: 60, marginTop: 12 }}>{a}</div>
            <div style={{ fontFamily: "IDSemi", fontSize: 30, color: "#666", marginTop: 8 }}>{b}</div>
          </div>
        );
      })}
      <Stamp at={T[62] + 0.3} text="DIGUGAT" color={K.r} top={1300} size={70} />
    </AbsoluteFill>
  );
};

// ---------- S5 Oregon
const S5: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[64] - 0.08, T[88] - 0.05);
  const money = ease(t, T[84], T[86] + 0.6, 0, 2.035);
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1300 }}>
      <DayHead n="2" state="OREGON MENGGUGAT" at={T[64] - 0.05} color={K.b} />
      <div style={{ position: "absolute", left: 130, top: 580, width: 500, height: 628, transformStyle: "preserve-3d",
        transform: `rotateY(${ease(t, T[66], T[66] + 0.8, 60, 14) + Math.sin(t * 0.8) * 4}deg) rotateX(6deg) translateZ(${ease(t, T[66], T[66] + 0.8, -600, 0)}px)`,
        opacity: ease(t, T[66], T[66] + 0.3) }}>
        <Img src={f("headline.png")} style={{ width: 500, height: 628, borderRadius: 24, boxShadow: "0 50px 120px rgba(0,0,0,.7)" }} />
        <div style={{ position: "absolute", left: 0, right: 0, bottom: -44, textAlign: "center", fontFamily: "IDBold", fontSize: 18, letterSpacing: ".12em", color: K.gy }}>
          SUMBER GAMBAR: TECH NEWS BY ZYBERSING</div>
      </div>
      <Chip at={T[72]} left={640} top={640} bg={K.y} size={32}>👶 Keselamatan anak</Chip>
      <Chip at={T[80]} left={640} top={740} bg={K.cr} size={32}>⚠ Klaim menyesatkan</Chip>
      <div style={{ position: "absolute", left: 600, top: 860, width: 420, opacity: ease(t, T[84], T[84] + 0.3) }}>
        <div style={{ fontFamily: "IDBold", fontSize: 26, letterSpacing: ".12em", color: K.gy }}>TUNTUTAN MINIMAL</div>
        <div style={{ fontFamily: "IDBlack", fontSize: 96, color: K.g2, lineHeight: 1 }}>${money.toFixed(3).replace(".", ",")}</div>
        <div style={{ fontFamily: "IDBlack", fontSize: 54, color: K.cr }}>MILIAR</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1300, textAlign: "center", fontFamily: "IDBold", fontSize: 22, letterSpacing: ".14em", color: K.gy,
        opacity: ease(t, T[68], T[68] + 0.3) }}>DIAJUKAN 17 NOV 2026 · MULTNOMAH COUNTY</div>
    </AbsoluteFill>
  );
};

// ---------- S6 Arizona: penyelidikan pidana
const S6: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[88] - 0.08, T[96] - 0.05);
  const tape = (i: number) => (
    <div key={i} style={{ position: "absolute", left: -200, top: 760 + i * 300, width: 1480, height: 90, background: `repeating-linear-gradient(-45deg, ${K.y} 0 60px, #111 60px 120px)`,
      display: "flex", alignItems: "center", justifyContent: "center", fontFamily: "IDBlack", fontSize: 44, color: K.k,
      transform: `rotateZ(${i ? 7 : -6}deg) rotateY(${i ? -16 : 16}deg) translateX(${ease(t, T[92] + i * 0.15, T[92] + i * 0.15 + 0.5, i ? 1200 : -1200, 0)}px)` }}>
      <span style={{ background: K.y, padding: "0 30px" }}>PENYELIDIKAN PIDANA · PENYELIDIKAN PIDANA</span></div>
  );
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1300 }}>
      <DayHead n="3" state="ARIZONA" at={T[88] - 0.05} color={K.y} />
      {tape(0)}{tape(1)}
      <div style={{ position: "absolute", left: 330, top: 880, width: 420, height: 420, opacity: ease(t, T[94], T[94] + 0.3),
        transform: `scale(${0.7 + 0.3 * ease(t, T[94], T[94] + 0.4)}) rotate(${Math.sin(t * 2) * 8}deg)` }}>
        <svg viewBox="0 0 100 100" style={{ width: "100%", height: "100%" }} fill="none" stroke={K.cr} strokeWidth={7} strokeLinecap="round">
          <circle cx="42" cy="42" r="26" fill="rgba(7,9,12,.85)" /><path d="M62 62l24 24" />
        </svg>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1380, textAlign: "center", fontFamily: "IDBold", fontSize: 22, letterSpacing: ".14em", color: K.gy,
        opacity: ease(t, T[90], T[90] + 0.3) }}>DIUMUMKAN JAKSA AGUNG ARIZONA · 18 NOV 2026</div>
    </AbsoluteFill>
  );
};

// ---------- S7 catatan penting: masih tuduhan
const S7: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[96] - 0.08, T[107] - 0.05);
  const s = useSp()(T[96], 14);
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1300 }}>
      <div style={{ position: "absolute", left: 110, top: 500, width: 860, height: 760, borderRadius: 40, background: K.cr, color: K.k, padding: 60,
        transform: `rotateX(${(1 - s) * 70}deg) rotateY(${Math.sin(t * 0.8) * 6}deg)`, opacity: s, boxShadow: "0 50px 120px rgba(0,0,0,.6)" }}>
        <div style={{ fontFamily: "IDBold", fontSize: 30, letterSpacing: ".16em", color: "#8a2b16" }}>PENTING DICATAT</div>
        <svg viewBox="0 0 100 100" style={{ width: 200, height: 200, margin: "30px 0" }} fill="none" stroke={K.k} strokeWidth={6} strokeLinecap="round">
          <path d="M30 40l20-20 14 14-20 20z" /><path d="M48 46l30 30" /><path d="M18 86h40" />
        </svg>
        <div style={{ fontFamily: "IDBlack", fontSize: 76, lineHeight: 1.05 }}>Masih <span style={{ color: K.r }}>tuduhan</span>.</div>
        <div style={{ fontFamily: "IDBlack", fontSize: 76, lineHeight: 1.05, opacity: ease(t, T[103], T[103] + 0.3) }}>Belum ada putusan.</div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- S8 era bebas aturan berakhir
const S8: React.FC = () => {
  const { t } = useT();
  const op = win(t, T[107] - 0.08, T[128] - 0.05);
  const strike = ease(t, T[114], T[115] + 0.3);
  const p2 = ease(t, T[116] - 0.2, T[116] + 0.1);
  const pull = ease(t, T[123], T[127] + 0.4);
  return (
    <AbsoluteFill style={{ opacity: op, perspective: 1300 }}>
      <div style={{ opacity: 1 - p2 }}>
        <Words text="PESANNYA JELAS" at={T[107] - 0.05} size={96} top={330} color={K.y} />
        <div style={{ position: "absolute", left: 0, right: 0, top: 700, textAlign: "center" }}>
          <span style={{ position: "relative", display: "inline-block", fontFamily: "IDBlack", fontSize: 78, color: K.gy, opacity: ease(t, T[110], T[110] + 0.3) }}>
            ERA AI BEBAS ATURAN
            <i style={{ position: "absolute", left: "-3%", top: "46%", width: "106%", height: 16, borderRadius: 8, background: K.r, transform: `scaleX(${strike})`, transformOrigin: "0 50%" }} />
          </span>
        </div>
        <Stamp at={T[115]} text="BERAKHIR" color={K.r} top={880} size={110} />
      </div>
      <div style={{ opacity: p2 }}>
        <Words text="PEMERINTAH NGGAK CUMA NONTON" at={T[116]} size={76} top={330} />
        <div style={{ position: "absolute", left: 240, top: 620, width: 600, height: 560, transformStyle: "preserve-3d", transform: `rotateY(${-20 + Math.sin(t * 0.7) * 10}deg) rotateX(8deg)` }}>
          <svg viewBox="0 0 120 100" style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }} fill="none" stroke={K.cr} strokeWidth={4}>
            <path d="M10 34L60 10l50 24z" /><path d="M14 38h92M24 44v40M42 44v40M60 44v40M78 44v40M96 44v40M12 88h96M6 96h108" />
          </svg>
          <div style={{ position: "absolute", left: 230 - pull * 0, top: 260, transform: `translateZ(${(1 - pull) * 500}px) translateX(${(1 - pull) * 420}px) scale(${1 - pull * 0.4})`,
            opacity: ease(t, T[121], T[121] + 0.3) }}>
            <Knot size={160} x={-80} y={-80} ry={t * 60} rx={10} layers={10} />
          </div>
        </div>
        <Words text="DISERET KE PENGADILAN" at={T[123]} size={80} top={1260} color={K.r} />
      </div>
    </AbsoluteFill>
  );
};

// ---------- S9 pengawasan + simpan (chibi)
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
  const op = win(t, T[128] - 0.08, D.dur + 1, 0.18, 0.01);
  const p2 = ease(t, T[145] - 0.2, T[145] + 0.05);
  return (
    <AbsoluteFill style={{ opacity: op }}>
      <div style={{ opacity: 1 - p2 }}>
        <Words text="SECANGGIH APA PUN AI-NYA" at={T[128] - 0.05} size={74} top={330} />
        <Words text="TETAP BUTUH PENGAWASAN" at={T[142]} size={74} top={430} color={K.g2} />
      </div>
      <div style={{ opacity: p2 }}>
        <Words text="SIMPAN VIDEO INI" at={T[145]} size={96} top={330} color={K.y} />
        <Chip at={T[148]} left={250} top={460} bg={K.cr} size={40}>🔖 Kasusnya bakal panjang</Chip>
      </div>
      <Chibi />
    </AbsoluteFill>
  );
};

export const OpenaiDigugat: React.FC = () => {
  useFonts();
  const { t } = useT();
  const flash = Math.max(...[T[11], T[43], T[66], T[90], T[115]].map((a) => (t >= a && t < a + 0.25 ? 0.3 * (1 - (t - a) / 0.25) : 0)));
  return (
    <AbsoluteFill style={{ background: `radial-gradient(120% 70% at 50% 40%, #0F1A1A 0%, ${K.k} 70%)`, overflow: "hidden" }}>
      <style>{fontCss}</style>
      <Audio src={f("vo.mp3")} />
      <Particles />
      <S1 /><S2 /><S3 /><S4 /><S5 /><S6 /><S7 /><S8 /><S9 />
      <div style={{ position: "absolute", left: 60, top: 262, display: "flex", alignItems: "center", gap: 12, fontFamily: "IDBold", fontSize: 24,
        letterSpacing: ".18em", color: K.cr }}><i style={{ width: 12, height: 12, borderRadius: 6, background: K.g, display: "inline-block" }} />BERITA AI · HUKUM</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 1525, textAlign: "center", fontFamily: "IDBlack", fontSize: 36, color: K.cr }}>
        Endrich<span style={{ color: K.g2 }}>Tech</span></div>
      <AbsoluteFill style={{ background: "#fff", opacity: flash, pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};
