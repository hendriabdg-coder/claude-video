import { staticFile } from "remotion";
// Palet EndrichTech (dasar PULSE) + Inter Display, sama dengan reel motion.
export const C = { k: "#0E0E0E", b: "#3A5BFF", c: "#FF4F3A", cr: "#F4F1EA", g: "#8A8F9C", k2: "#17181C" };
export const fontCss = `
@font-face { font-family: IDBlack; src: url(${staticFile("fonts/InterDisplay-Black.ttf")}); }
@font-face { font-family: IDBold; src: url(${staticFile("fonts/InterDisplay-Bold.ttf")}); }
@font-face { font-family: IDSemi; src: url(${staticFile("fonts/InterDisplay-SemiBold.ttf")}); }
@font-face { font-family: IDItal; src: url(${staticFile("fonts/InterDisplay-SemiBoldItalic.ttf")}); }`;
