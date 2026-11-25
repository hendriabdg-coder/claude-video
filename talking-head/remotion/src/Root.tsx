import { Composition } from "remotion";
import { SplitEdit } from "./SplitEdit";
import { SEGMENTS } from "./timeline";
import { CeoNvidia } from "./reels/CeoNvidia";
import CEO from "./reels/ceo-nvidia-data.json";
import { OpenaiDigugat } from "./reels/OpenaiDigugat";
import OAI from "./reels/openai-digugat-data.json";
export const FPS = 30;
export const Root = () => (
  <>
  <Composition id="SplitEdit" component={SplitEdit} width={1920} height={1080} fps={FPS}
    durationInFrames={Math.round(SEGMENTS[SEGMENTS.length - 1].to * FPS)} />
    {/* reel 9:16 motion (2026-11-24) */}
    <Composition id="CeoNvidia" component={CeoNvidia} width={1080} height={1920} fps={FPS} durationInFrames={Math.round(CEO.dur * FPS)} />
    <Composition id="OpenaiDigugat" component={OpenaiDigugat} width={1080} height={1920} fps={FPS} durationInFrames={Math.round(OAI.dur * FPS)} />
  </>
);
