import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { C, fontCss } from "./theme";
import { SEGMENTS, VIDEO } from "./timeline";
import { Hybrid } from "./scenes/Hybrid";
import { Full } from "./scenes/Full";

// Audio talking head jalan terus; tiap segmen menggambar visualnya sendiri (video di-mute di dalam segmen).
export const SplitEdit: React.FC = () => {
  const { fps, durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: C.k }}>
      <style>{fontCss}</style>
      <Audio src={staticFile(VIDEO)} />
      {SEGMENTS.map((s, i) => {
        const from = Math.round(s.from * fps), dur = Math.round((s.to - s.from) * fps);
        return (
          <Sequence key={i} from={from} durationInFrames={dur} premountFor={fps}>
            {s.type === "hybrid" ? <Hybrid seg={s} startSec={s.from} /> : <Full seg={s} />}
          </Sequence>
        );
      })}
      {/* progress + watermark */}
      <div style={{ position: "absolute", left: 0, bottom: 0, height: 6, width: `${(frame / durationInFrames) * 100}%`, background: C.c }} />
      <div style={{ position: "absolute", right: 56, bottom: 36, fontFamily: "IDBlack", fontSize: 30, color: C.cr, background: "rgba(14,14,14,.72)", padding: "6px 16px", borderRadius: 10, opacity: interpolate(frame, [0, 15], [0, 0.9]) }}>
        Endrich<span style={{ color: C.c }}>Tech</span>
      </div>
    </AbsoluteFill>
  );
};
