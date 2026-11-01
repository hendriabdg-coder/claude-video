#!/usr/bin/env bash
# BEHIND matte ("SISTEM" 2x) + HyperFrames render + final composite for "Chat WhatsApp".
#   m1 = plate frames 1017..1067 (33.900–35.567 s)   m2 = plate frames 1689..1720 (56.300–57.333 s)
set -euo pipefail
cd "$(dirname "$0")"
HF="bash /d/Claude Video/.claude/skills/endrichtech-edit/scripts/hf.sh"
mkdir -p matte renders
ffmpeg -v error -y -i public/plate.mp4 -vf "select='between(n,1017,1067)',setpts=N/30/TB" -an -c:v libx264 -crf 8 -pix_fmt yuv420p matte/seg1.mp4
ffmpeg -v error -y -i public/plate.mp4 -vf "select='between(n,1689,1720)',setpts=N/30/TB" -an -c:v libx264 -crf 8 -pix_fmt yuv420p matte/seg2.mp4
bash "/d/Claude Video/.claude/skills/endrichtech-edit/scripts/hf.sh" remove-background matte/seg1.mp4 -o matte/m1.mov --device cpu > matte/log1.txt 2>&1
bash "/d/Claude Video/.claude/skills/endrichtech-edit/scripts/hf.sh" remove-background matte/seg2.mp4 -o matte/m2.mov --device cpu > matte/log2.txt 2>&1
bash "/d/Claude Video/.claude/skills/endrichtech-edit/scripts/hf.sh" render public --skill=talking-head-recut -o "D:/Claude Video/talking-head/proyek/chatwhatsapp/renders/overlay.mp4" --fps 30 --low-memory-mode --quiet > render.log 2>&1
ffmpeg -v error -y -i renders/overlay.mp4 -i matte/m1.mov -i matte/m2.mov -filter_complex "\
[1:v]crop=1080:760:0:0,format=yuva420p,setpts=PTS-STARTPTS+1017/30/TB[a];\
[2:v]crop=1080:760:0:0,format=yuva420p,setpts=PTS-STARTPTS+1689/30/TB[b];\
[0:v][a]overlay=0:0:eof_action=pass[v1];[v1][b]overlay=0:0:eof_action=pass,format=yuv420p[v]" \
  -map "[v]" -map 0:a -c:v libx264 -preset medium -crf 17 -c:a copy -movflags +faststart \
  "../../hasil/chatwhatsapp/Chat WhatsApp_motion.mp4"
echo "wrote Chat WhatsApp_motion.mp4"
