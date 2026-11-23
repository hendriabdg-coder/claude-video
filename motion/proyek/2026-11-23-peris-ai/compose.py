# Tempel rekaman acara (aset/screen.mp4, 576x780, bagian stabil mulai 0,5 dtk) ke kartu #vcard di renders/visual.mp4.
# Posisi & waktu dari vcard.txt (ditulis build.py). Sudut membulat lewat mask PNG, fade masuk/keluar 0,2 dtk.
#   python compose.py  ->  renders/visual_v.mp4
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
x, y, w, h, t0, t1 = (float(v) for v in (HERE / "vcard.txt").read_text().split())
x, y, w, h = int(x), int(y), int(w), int(h)
mask = HERE / "renders" / "_vmask.png"
m = Image.new("L", (w, h), 0)
ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=22, fill=255)
m.save(mask)
d = t1 - t0
fx = (f"[1:v]trim=start=0.5:duration={d:.3f},setpts=PTS-STARTPTS,scale={w}:{h}:flags=lanczos,format=yuva420p[v0];"
      f"[2:v]format=gray,scale={w}:{h}[m];[v0][m]alphamerge,fade=t=in:st=0:d=0.2:alpha=1,fade=t=out:st={d - 0.2:.3f}:d=0.2:alpha=1,"
      f"setpts=PTS+{t0:.3f}/TB[ov];[0:v][ov]overlay={x}:{y}:enable='between(t,{t0:.3f},{t1:.3f})':eof_action=pass[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(HERE / "renders" / "visual.mp4"), "-i", str(HERE / "aset" / "screen.mp4"),
                "-loop", "1", "-i", str(mask), "-filter_complex", fx, "-map", "[out]", "-map", "0:a", "-c:v", "libx264", "-crf", "17",
                "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", str(HERE / "renders" / "visual_v.mp4")], check=True)
mask.unlink()
print("ok", x, y, w, h, t0, t1)
