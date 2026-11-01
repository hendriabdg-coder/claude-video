#!/usr/bin/env bash
# Final composite: HyperFrames render + subject matte (head region only) over the two
# behind-head words, so the giant "DOTS" / "AI" sit behind the speaker's head.
#   m1 = plate frames 117..178 (3.900–5.933s)   m2 = plate frames 1360..1400 (45.333–46.667s)
set -euo pipefail
cd "$(dirname "$0")"
ffmpeg -v error -y -i renders/overlay.mp4 -i matte/m1.mov -i matte/m2.mov -filter_complex "\
[1:v]crop=1080:760:0:0,format=yuva420p,setpts=PTS-STARTPTS+117/30/TB[a];\
[2:v]crop=1080:760:0:0,format=yuva420p,setpts=PTS-STARTPTS+1360/30/TB[b];\
[0:v][a]overlay=0:0:eof_action=pass[v1];[v1][b]overlay=0:0:eof_action=pass,format=yuv420p[v]" \
  -map "[v]" -map 0:a -c:v libx264 -preset medium -crf 17 -c:a copy -movflags +faststart \
  "../../hasil/take/take_motion.mp4"
echo "wrote take_motion.mp4"
