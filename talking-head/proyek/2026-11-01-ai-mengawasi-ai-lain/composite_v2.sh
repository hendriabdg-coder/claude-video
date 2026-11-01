#!/usr/bin/env bash
# v2: render HyperFrames, lalu tempel orang tajam (matte) di posisi aslinya untuk 3 split-pop.
# Matte di-erode 1 px + dihaluskan (buang halo dinding putih), turun dengan kurva power3.out 0.4 dtk
# yang sama dengan video blur di build_v2.py (CUTS: 1.4/300, 529/30/280 s.d. 568/30, 1541/30/180 s.d. 1616/30).
set -e
cd "$(dirname "$0")"
SLUG=2026-11-01-ai-mengawasi-ai-lain
HF="/d/Claude Video/.claude/skills/endrichtech-edit/scripts/hf.sh"
[ "$1" = "--skip-render" ] || bash "$HF" render public -o "D:/Claude Video/talking-head/proyek/$SLUG/renders/overlay_v2.mp4" --fps 30 --low-memory-mode --quiet
m() { # input-index start-expr label
  echo "[$1:v]setpts=PTS-STARTPTS+($2)/TB,format=yuva420p,split[c$1][a$1];[a$1]alphaextract,erosion,boxblur=1:1[k$1];[c$1][k$1]alphamerge[p$1];"
}
Y() { echo "$2*(1-pow(1-min(1\,max(0\,(t-$1)/0.4))\,3))"; }
ffmpeg -v error -y -i renders/overlay_v2.mp4 -i matte/m1.mov -i matte/m2.mov -i matte/m3.mov -filter_complex "\
$(m 1 1.4)$(m 2 529/30)$(m 3 1541/30)\
[0:v][p1]overlay=x=0:y='$(Y 1.4 300)':eval=frame:enable='between(t,1.4,3.6)':eof_action=pass[v1];\
[v1][p2]overlay=x=0:y='$(Y 17.6333 280)':eval=frame:enable='between(t,17.633,18.933)':eof_action=pass[v2];\
[v2][p3]overlay=x=0:y='$(Y 51.3667 180)':eval=frame:enable='between(t,51.367,53.867)':eof_action=pass[v]" \
  -map "[v]" -map 0:a? -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k \
  "../../hasil/$SLUG/${SLUG}_motion_v2.mp4"
echo done
