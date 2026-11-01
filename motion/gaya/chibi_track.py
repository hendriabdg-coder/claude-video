# Animated chibi presenter for GUIDE-style videos: the green-screen clips in karakter/Animasi Karakter (720x1280, 24 fps,
# ~4 s, every clip starts and ends on the same neutral stance, so hard cuts between them read as one character).
# HyperFrames can't play alpha video reliably, so the character is keyed in ffmpeg and laid over the rendered graphics.
#   make_track(segments, dur, out)   segments = [(start, end, "clip_name"), ...]; a segment longer than its clip loops it
#   composite(graphics_mp4, track_mov, out_mp4, ...)
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLIPS = ROOT / "karakter" / "Animasi Karakter"
GREEN = "0x13C817"
KEY = f"format=rgba,colorkey={GREEN}:0.30:0.08,despill=type=green:mix=0.7:expand=0.05"


def run(args):
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + args, check=True)


def make_track(segments, dur, out, fps=30):
    """One RGBA (qtrle) .mov of length dur: each segment keyed from its clip, transparent where no segment plays."""
    out = Path(out)
    parts = out.parent / (out.stem + "_parts")
    parts.mkdir(parents=True, exist_ok=True)
    listing, t = [], 0.0
    blank = f"color=c=black@0.0:s=720x1280:r={fps},format=rgba"
    for k, (a, b, clip) in enumerate(sorted(segments)):
        if a > t + 1e-3:
            gap = parts / f"g{k:02d}.mov"
            run(["-f", "lavfi", "-i", blank, "-t", f"{a - t:.3f}", "-c:v", "qtrle", str(gap)])
            listing.append(gap)
        seg = parts / f"s{k:02d}.mov"
        src = CLIPS / f"{clip}.mp4"
        if not src.exists():
            sys.exit(f"klip tidak ada: {src}")
        run(["-stream_loop", "-1", "-i", str(src), "-t", f"{b - a:.3f}", "-an", "-vf", f"fps={fps},{KEY}", "-c:v", "qtrle", str(seg)])
        listing.append(seg)
        t = b
    if dur > t + 1e-3:
        tail = parts / "tail.mov"
        run(["-f", "lavfi", "-i", blank, "-t", f"{dur - t:.3f}", "-c:v", "qtrle", str(tail)])
        listing.append(tail)
    lst = parts / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in listing), encoding="utf-8")
    run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out)])
    return out


def watermark(out, x=70, y=1508, until=None):
    """EndrichTech watermark as a transparent 1080x1920 PNG, laid over the character so a waving arm can't hide it
    (IG-safe spot y ~ 1525)."""
    from PIL import Image, ImageDraw, ImageFont
    fonts = ROOT / "motion" / "gaya" / "gaya-showcase" / "public" / "fonts"
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    a, b = ImageFont.truetype(str(fonts / "InterDisplay-Black.ttf"), 30), ImageFont.truetype(str(fonts / "SerifBI.ttf"), 30)
    pad, w1 = 14, d.textlength("Endrich", font=a)
    w = w1 + d.textlength("Tech", font=b)
    d.rounded_rectangle([x - pad, y - 8, x + w + pad, y + 44], radius=22, fill=(238, 235, 228, 215))
    d.text((x, y), "Endrich", font=a, fill=(21, 21, 21, 220))
    d.text((x + w1, y), "Tech", font=b, fill=(21, 21, 21, 220))
    im.save(out)
    return out


def composite(graphics, track, out, scale=1.3, cx=540, top=955, enter=0.1, wm_until=None):
    """Overlay the keyed track (scaled, centred on cx, clip top at y=top) on the graphics render; the character
    rises in from below at t=enter (cubic ease-out, 0.5 s); the watermark goes on top until wm_until.
    Audio from the graphics render is kept."""
    w, h = round(720 * scale), round(1280 * scale)
    y = f"{top}+1000*pow(max(0\\,1-(t-{enter})/0.5)\\,3)"
    wm = watermark(Path(out).with_name("wm.png"))
    on = f":enable='lt(t\\,{wm_until})'" if wm_until else ""
    fx = (f"[1:v]scale={w}:{h}:flags=lanczos,setpts=PTS-STARTPTS[c];"
          f"[0:v][c]overlay=x={cx - w // 2}:y='if(lt(t\\,{enter})\\,1920\\,{y})':eval=frame:shortest=1[v0];"
          f"[v0][2:v]overlay=0:0{on},format=yuv420p[v]")
    run(["-i", str(graphics), "-i", str(track), "-loop", "1", "-i", str(wm), "-filter_complex", fx, "-map", "[v]", "-map", "0:a?",
         "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "copy", "-shortest", "-movflags", "+faststart", str(out)])
    return out


if __name__ == "__main__":
    # python chibi_track.py <video-folder>   (uses <folder>/public/char_track.json + renders/graphics.mp4)
    d = Path(sys.argv[1]).resolve()
    spec = json.loads((d / "public" / "char_track.json").read_text(encoding="utf-8"))
    trk = make_track([tuple(s) for s in spec["segments"]], spec["dur"], d / "renders" / "char_track.mov")
    composite(d / "renders" / "graphics.mp4", trk, d / "renders" / "visual.mp4", **spec.get("place", {}))
    print("ok ->", d / "renders" / "visual.mp4")
