#!/usr/bin/env bash
# Render HyperFrames lalu tempel 3 segmen "latar dihapus" (matte/mN.mov dari hf.sh remove-background):
#   m1 1.4-3.6 dtk (shot 1, x0.85)  ·  m2 17.633-20.333 (shot 8-9, x1.25)  ·  m3 51.367-53.867 (shot 25, x1.0)
#   bash composite.sh [--skip-render]
set -e
cd "$(dirname "$0")"
SLUG=2026-11-01-ai-mengawasi-ai-lain
HF="/d/Claude Video/.claude/skills/endrichtech-edit/scripts/hf.sh"
mkdir -p renders "../../hasil/$SLUG"
[ "$1" = "--skip-render" ] || bash "$HF" render public -o "D:/Claude Video/talking-head/proyek/$SLUG/renders/overlay.mp4" --fps 30 --low-memory-mode --quiet
ffmpeg -v error -y -i renders/overlay.mp4 -i matte/m1.mov -i matte/m2.mov -i matte/m3.mov -filter_complex "\
[1:v]scale=918:1632,setpts=PTS-STARTPTS+1.4/TB,format=yuva420p[p1];\
[2:v]scale=1350:2400,setpts=PTS-STARTPTS+(529/30)/TB,format=yuva420p[p2];\
[3:v]scale=1080:1920,setpts=PTS-STARTPTS+(1541/30)/TB,format=yuva420p[p3];\
[0:v][p1]overlay=11:336:enable='between(t,1.4,3.6)':eof_action=pass[v1];\
[v1][p2]overlay=-149:196:enable='between(t,17.633,20.333)':eof_action=pass[v2];\
[v2][p3]overlay=0:170:enable='between(t,51.367,53.867)':eof_action=pass[v]" \
  -map "[v]" -map 0:a? -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k \
  "../../hasil/$SLUG/${SLUG}_motion.mp4"
echo done
