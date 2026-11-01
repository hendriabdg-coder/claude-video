#!/usr/bin/env bash
# matte (head region) + HyperFrames render + final composite for "video 01".
#   m1 = plate frames 0..85     ("JANGAN" behind head, 0.000–2.833s)
#   m2 = plate frames 1013..1041 ("KAMU" behind head, 33.767–34.700s)
set -euo pipefail
cd "$(dirname "$0")"
HF="node C:/Users/aceru/.claude/plugins/cache/hyperframes/hyperframes/0.8.111/skills/hyperframes/scripts/plugin-cli.mjs"
mkdir -p matte renders
ffmpeg -v error -y -i public/plate.mp4 -vf "select='between(n,0,85)',setpts=N/30/TB" -an -c:v libx264 -crf 8 -pix_fmt yuv420p matte/seg1.mp4
ffmpeg -v error -y -i public/plate.mp4 -vf "select='between(n,1013,1041)',setpts=N/30/TB" -an -c:v libx264 -crf 8 -pix_fmt yuv420p matte/seg2.mp4
$HF remove-background matte/seg1.mp4 -o matte/m1.mov --device cpu > matte/log1.txt 2>&1
$HF remove-background matte/seg2.mp4 -o matte/m2.mov --device cpu > matte/log2.txt 2>&1
$HF render public --skill=talking-head-recut -o "D:/Claude Video/talking-head/proyek/video01/renders/overlay.mp4" --fps 30 --low-memory-mode --quiet > render.log 2>&1
ffmpeg -v error -y -i renders/overlay.mp4 -i matte/m1.mov -i matte/m2.mov -filter_complex "\
[1:v]crop=1080:760:0:0,format=yuva420p,setpts=PTS-STARTPTS[a];\
[2:v]crop=1080:760:0:0,format=yuva420p,setpts=PTS-STARTPTS+1013/30/TB[b];\
[0:v][a]overlay=0:0:eof_action=pass[v1];[v1][b]overlay=0:0:eof_action=pass,format=yuv420p[v]" \
  -map "[v]" -map 0:a -c:v libx264 -preset medium -crf 17 -c:a copy -movflags +faststart \
  "../../hasil/video01/video 01_motion.mp4"
echo "wrote video 01_motion.mp4"
