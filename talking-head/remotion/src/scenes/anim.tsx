import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { C } from "../theme";

export const useIn = (delay = 0, damping = 14) => {
  const f = useCurrentFrame(), { fps } = useVideoConfig();
  return spring({ frame: f - delay, fps, config: { damping, mass: 0.6 } });
};
// masuk segmen: wipe diagonal 8 frame (bukan fade), keluar: wipe kebalikan 6 frame terakhir
export const Wipe: React.FC<{ children: React.ReactNode; color?: string }> = ({ children, color = C.c }) => {
  const f = useCurrentFrame(), { durationInFrames } = useVideoConfig();
  const a = interpolate(f, [0, 8], [0, 120], { extrapolateRight: "clamp" });
  const bar = interpolate(f, [0, 5, 10], [-30, 60, 140], { extrapolateRight: "clamp" });
  const out = interpolate(f, [durationInFrames - 6, durationInFrames], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, clipPath: `polygon(0 0, ${a}% 0, ${a - 20}% 100%, 0 100%)`, transform: `scale(${1 + out * 0.04})` }}>
      {children}
      <div style={{ position: "absolute", top: 0, bottom: 0, width: "18%", left: `${bar}%`, background: color, transform: "skewX(-12deg)", opacity: f < 11 ? 1 : 0 }} />
    </div>
  );
};
// kata per kata, kata aksen berwarna + stabilo
export const Words: React.FC<{ text: string; accent?: string; size: number; color?: string; delay?: number; stagger?: number; align?: "left" | "center" }> =
  ({ text, accent, size, color = C.cr, delay = 0, stagger = 3, align = "left" }) => {
    const f = useCurrentFrame(), { fps } = useVideoConfig();
    const acc = (accent || "").toLowerCase().split(" ");
    return (
      <div style={{ fontFamily: "IDBlack", fontSize: size, lineHeight: 1.02, letterSpacing: "-0.02em", color, textAlign: align }}>
        {text.split(" ").map((w, i) => {
          const s = spring({ frame: f - delay - i * stagger, fps, config: { damping: 13, mass: 0.5 } });
          const isA = acc.includes(w.toLowerCase().replace(/[^\w-]/g, ""));
          return (
            <span key={i} style={{ display: "inline-block", overflow: "hidden", verticalAlign: "top", marginRight: size * 0.22 }}>
              <span style={{ display: "inline-block", transform: `translateY(${(1 - s) * 110}%)`, color: isA ? C.c : color, fontFamily: isA ? "IDItal" : "IDBlack",
                background: isA ? `linear-gradient(transparent 62%, ${C.b}55 62%)` : undefined }}>{w}</span>
            </span>
          );
        })}
      </div>
    );
  };
export const Chip: React.FC<{ text: string; color?: string; delay?: number }> = ({ text, color = C.c, delay = 0 }) => {
  const s = useIn(delay);
  return <div style={{ display: "inline-block", fontFamily: "IDBold", fontSize: 24, letterSpacing: "0.18em", color, border: `2px solid ${color}`,
    borderRadius: 10, padding: "8px 16px", transform: `translateX(${(1 - s) * -40}px)`, opacity: s }}>{text}</div>;
};
