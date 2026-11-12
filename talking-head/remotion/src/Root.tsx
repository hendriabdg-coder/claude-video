import { Composition } from "remotion";
import { SplitEdit } from "./SplitEdit";
import { SEGMENTS } from "./timeline";
export const FPS = 30;
export const Root = () => (
  <Composition id="SplitEdit" component={SplitEdit} width={1920} height={1080} fps={FPS}
    durationInFrames={Math.round(SEGMENTS[SEGMENTS.length - 1].to * FPS)} />
);
