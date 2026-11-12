import React from "react";
import { AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { C } from "../theme";
import { VIDEO, Seg } from "../timeline";
import { Chip, Words, Wipe, useIn } from "./anim";

type H = Extract<Seg, { type: "hybrid" }>;
// video talking head mulai dari detik yang sama dengan segmen (audio global, video di sini di-mute)
const TH: React.FC<{ startSec: number; style?: React.CSSProperties }> = ({ startSec, style }) => {
  const { fps } = useVideoConfig();
  return <OffthreadVideo src={staticFile(VIDEO)} startFrom={Math.round(startSec * fps)} muted
    style={{ width: "100%", height: "100%", objectFit: "cover", ...style }} />;
};

export const Hybrid: React.FC<{ seg: H; startSec: number }> = ({ seg, startSec }) => {
  const f = useCurrentFrame(), { durationInFrames } = useVideoConfig();
  const zoom = interpolate(f, [0, durationInFrames], [1.0, 1.06]);          // punch-in pelan
  const card = useIn(2, 16);

  if (seg.variant === "split") return (
    <Wipe>
      <AbsoluteFill style={{ background: C.k }}>
        <div style={{ position: "absolute", left: 60, top: 60, width: 900, height: 960, borderRadius: 36, overflow: "hidden",
          transform: `translateX(${(1 - card) * -120}px) rotate(${(1 - card) * -2}deg)`, boxShadow: "0 40px 80px rgba(0,0,0,.5)" }}>
          <div style={{ width: "100%", height: "100%", transform: `scale(${zoom})` }}><TH startSec={startSec} /></div>
        </div>
        <div style={{ position: "absolute", left: 1030, top: 200, width: 820 }}>
          {seg.label && <Chip text={seg.label} delay={4} />}
          <div style={{ marginTop: 34 }}><Words text={seg.title} accent={seg.accent} size={92} delay={6} /></div>
          <div style={{ marginTop: 50 }}>
            {(seg.points || []).map((p, i) => <Point key={i} i={i} text={p} delay={18 + i * 10} />)}
          </div>
        </div>
      </AbsoluteFill>
    </Wipe>
  );

  if (seg.variant === "pip") {
    const ring = interpolate(f % 30, [0, 30], [1, 1.25]);
    return (
      <Wipe color={C.b}>
        <AbsoluteFill style={{ background: C.b }}>
          <Grid />
          <div style={{ position: "absolute", left: 120, top: 280, width: 980 }}>
            {seg.label && <Chip text={seg.label} color={C.cr} delay={4} />}
            <div style={{ marginTop: 34 }}><Words text={seg.title} accent={seg.accent} size={104} delay={6} /></div>
          </div>
          <div style={{ position: "absolute", right: 170, top: 250, width: 520, height: 520 }}>
            <div style={{ position: "absolute", inset: -20, borderRadius: "50%", border: `4px solid ${C.cr}`, opacity: 2 - ring, transform: `scale(${ring})` }} />
            <div style={{ width: "100%", height: "100%", borderRadius: "50%", overflow: "hidden", border: `8px solid ${C.cr}`,
              transform: `scale(${card})` }}><TH startSec={startSec} /></div>
          </div>
        </AbsoluteFill>
      </Wipe>
    );
  }

  // lower: video penuh + kata kunci besar di bawah + garis aksen
  const bar = useIn(4);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", inset: 0, transform: `scale(${zoom})` }}><TH startSec={startSec} /></div>
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 420, background: "linear-gradient(transparent, rgba(0,0,0,.85))" }} />
      <div style={{ position: "absolute", left: 90, bottom: 120, width: 1300 }}>
        <div style={{ width: 140 * bar, height: 10, background: C.c, marginBottom: 24 }} />
        <Words text={seg.title} accent={seg.accent} size={96} delay={6} />
      </div>
    </AbsoluteFill>
  );
};

const Point: React.FC<{ i: number; text: string; delay: number }> = ({ i, text, delay }) => {
  const s = useIn(delay);
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 24, margin: "22px 0", opacity: s, transform: `translateX(${(1 - s) * 60}px)` }}>
      <div style={{ width: 64, height: 64, borderRadius: 16, background: C.c, color: C.cr, fontFamily: "IDBlack", fontSize: 34,
        display: "flex", alignItems: "center", justifyContent: "center" }}>{i + 1}</div>
      <div style={{ fontFamily: "IDBold", fontSize: 44, color: C.cr }}>{text}</div>
    </div>
  );
};
const Grid: React.FC = () => {
  const f = useCurrentFrame();
  return <div style={{ position: "absolute", inset: 0, opacity: 0.18, backgroundImage: `linear-gradient(${C.cr} 2px, transparent 2px), linear-gradient(90deg, ${C.cr} 2px, transparent 2px)`,
    backgroundSize: "80px 80px", backgroundPosition: `${f * 1.2}px ${f * 0.6}px` }} />;
};
