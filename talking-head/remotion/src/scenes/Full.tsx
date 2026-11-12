import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { C } from "../theme";
import { Seg } from "../timeline";
import { Chip, Words, Wipe, useIn } from "./anim";

type F = Extract<Seg, { type: "full" }>;
export const Full: React.FC<{ seg: F }> = ({ seg }) => {
  switch (seg.variant) {
    case "kinetic": return <Kinetic words={seg.words} />;
    case "stat": return <Stat seg={seg} />;
    case "list": return <List title={seg.title} items={seg.items} />;
    case "quote": return <Quote quote={seg.quote} source={seg.source} />;
  }
};

// kata raksasa satu per satu, hard cut warna latar tiap kata, teks berulang di latar
const BG = [C.k, C.b, C.c, C.cr];
const Kinetic: React.FC<{ words: string[] }> = ({ words }) => {
  const f = useCurrentFrame(), { durationInFrames, fps } = useVideoConfig();
  const per = durationInFrames / words.length, i = Math.min(words.length - 1, Math.floor(f / per));
  const lf = f - i * per, s = spring({ frame: lf, fps, config: { damping: 11, mass: 0.5 } });
  const bg = BG[i % BG.length], fg = bg === C.cr ? C.k : C.cr;
  const shake = lf < 4 ? (4 - lf) * 3 : 0;
  return (
    <AbsoluteFill style={{ background: bg, alignItems: "center", justifyContent: "center", transform: `translate(${shake}px, ${-shake}px)` }}>
      {[0, 1, 2].map((r) => (
        <div key={r} style={{ position: "absolute", top: 80 + r * 330, left: -200 - ((f * 6 + r * 300) % 800), whiteSpace: "nowrap", fontFamily: "IDBlack",
          fontSize: 260, color: "transparent", WebkitTextStroke: `3px ${fg}22` }}>{(words[i] + " ").repeat(6)}</div>
      ))}
      <div style={{ fontFamily: "IDBlack", fontSize: 300, letterSpacing: "-0.03em", color: fg, transform: `scale(${1.6 - 0.6 * s})`, opacity: Math.min(1, s * 2) }}>{words[i]}</div>
    </AbsoluteFill>
  );
};

const Stat: React.FC<{ seg: Extract<F, { variant: "stat" }> }> = ({ seg }) => {
  const f = useCurrentFrame(), { fps } = useVideoConfig();
  const k = interpolate(f, [6, 6 + fps * 1.2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: (x) => 1 - Math.pow(1 - x, 3) });
  const v = (seg.value * k).toFixed(seg.decimals ?? 0).replace(".", ",");
  const max = Math.max(...(seg.bars || [["", 1]]).map((b) => b[1]));
  return (
    <Wipe color={C.b}>
      <AbsoluteFill style={{ background: C.k, padding: "150px 120px" }}>
        <div style={{ fontFamily: "IDBlack", fontSize: 280, lineHeight: 1, color: C.cr, fontVariantNumeric: "tabular-nums" }}>{seg.prefix}{v}<span style={{ color: C.c }}>{seg.suffix}</span></div>
        <div style={{ marginTop: 30, width: 1100 }}><Words text={seg.label} size={64} delay={20} /></div>
        {seg.source && <div style={{ position: "absolute", left: 120, bottom: 110 }}><Chip text={`SUMBER: ${seg.source.toUpperCase()}`} color={C.g} delay={30} /></div>}
        {seg.bars && <div style={{ position: "absolute", right: 140, bottom: 180, display: "flex", gap: 40, alignItems: "flex-end", height: 520 }}>
          {seg.bars.map(([l, b], i) => {
            const s = spring({ frame: f - 14 - i * 6, fps, config: { damping: 14 } });
            return <div key={i} style={{ textAlign: "center" }}>
              <div style={{ width: 120, height: (b / max) * 480 * s, background: i === seg.bars!.length - 1 ? C.c : C.b, borderRadius: 14 }} />
              <div style={{ fontFamily: "IDBold", fontSize: 30, color: C.g, marginTop: 14 }}>{l}</div></div>;
          })}</div>}
      </AbsoluteFill>
    </Wipe>
  );
};

const List: React.FC<{ title: string; items: string[] }> = ({ title, items }) => (
  <Wipe>
    <AbsoluteFill style={{ background: C.cr, padding: "130px 140px" }}>
      <Words text={title} size={110} color={C.k} accent={title.split(" ")[0]} />
      <div style={{ marginTop: 70 }}>{items.map((t, i) => <Item key={i} i={i} t={t} />)}</div>
    </AbsoluteFill>
  </Wipe>
);
const Item: React.FC<{ i: number; t: string }> = ({ i, t }) => {
  const s = useIn(14 + i * 12);
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 34, margin: "26px 0", transform: `translateX(${(1 - s) * -200}px)`, opacity: s }}>
      <div style={{ width: 96, height: 96, borderRadius: "50%", background: C.k, color: C.cr, fontFamily: "IDBlack", fontSize: 48,
        display: "flex", alignItems: "center", justifyContent: "center" }}>{i + 1}</div>
      <div style={{ fontFamily: "IDBlack", fontSize: 66, color: C.k }}>{t}</div>
    </div>
  );
};

const Quote: React.FC<{ quote: string; source: string }> = ({ quote, source }) => {
  const s = useIn(2, 12), f = useCurrentFrame();
  return (
    <Wipe color={C.cr}>
      <AbsoluteFill style={{ background: C.c, alignItems: "center", justifyContent: "center" }}>
        <div style={{ width: 1400, background: C.cr, borderRadius: 40, padding: "90px 100px", transform: `rotate(${(1 - s) * 4 - 1}deg) scale(${0.8 + 0.2 * s})`,
          boxShadow: "0 50px 100px rgba(0,0,0,.3)" }}>
          <div style={{ fontFamily: "IDBlack", fontSize: 180, lineHeight: 0.6, color: C.c }}>“</div>
          <Words text={quote} size={100} color={C.k} delay={8} />
          <div style={{ marginTop: 40, fontFamily: "IDBold", fontSize: 34, letterSpacing: "0.12em", color: C.g, opacity: interpolate(f, [20, 30], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }}>— {source.toUpperCase()}</div>
        </div>
      </AbsoluteFill>
    </Wipe>
  );
};
