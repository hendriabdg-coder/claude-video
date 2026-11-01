# v2 finishing: composite the person matte over the "behind-head" words, then mix original dialog + SFX
# (Epidemic, new sfx/) and normalise to -14 LUFS / TP -1.5 dBFS (two-pass loudnorm).
#   python mix_v2.py renders/v2_overlay.mp4 <out.mp4> [--voice-only]
import json, subprocess, sys

src, out = sys.argv[1], sys.argv[2]
voice_only = "--voice-only" in sys.argv
RAW = "../../mentah/ai-web-security/Video Mentah.mp4"
L = "../../../new sfx/"
HIT = L + "ES_Short, Deep, Dry - Epidemic Sound.mp3"
DARK = L + "ES_Impact, Dark, Cinematic, Hard Hit 01 - Epidemic Sound.mp3"
CRACK = L + "ES_Impact, Crack 05 - Epidemic Sound.mp3"
MOUSE = L + "universfield-mouse-click-351398.mp3"
FAST = L + "whosh/fast whoosh.mp3"
CINE = L + "whosh/cinematic whoosh.mp3"
IMPW = L + "whosh/impact whoosh.mp3"
SWISH = L + "whosh/ES_Swooshes, Swish, Short, Wind Gusts, Dry - Epidemic Sound.mp3"
SOFT = L + "whosh/ES_Swooshes, Whoosh, Softs - Epidemic Sound.mp3"
POP = L + "ui/ES_User Interface, Click, Software, Interface, Pop Up, Notification - Epidemic Sound.mp3"
SAVE = L + "ES_Text Message, Notification, Confirm, Round, Soft - Epidemic Sound.mp3"
BUB = L + "ui/ES_Text Message, Notification, Round Tone, Clicky - Epidemic Sound.mp3"
TAP = L + "ui/ES_User Interface, Click, Button, Double Click, Fast, Phone Tap - Epidemic Sound.mp3"

# (time s, file, gain dB, skip-in s, length s) — whooshes start a little before the visual hit
CUES = [
    (0.00, HIT, -16, 0.28, 0.9),     # hook lands on frame 0
    (0.62, SOFT, -22, 0.0, 0.7),     # focus pull
    (1.52, FAST, -20, 0.30, 0.6),    # CEPAT. thrown
    (3.72, DARK, -24, 0.0, 1.2),     # AMAN behind the head
    (5.70, POP, -22, 0.0, 0.4),      # RAPI ≠ AMAN
    (7.00, CINE, -20, 0.38, 0.9),    # into the code cutaway
    (8.46, MOUSE, -16, 0.14, 0.3),   # cursor click
    (9.22, POP, -24, 0.0, 0.4),      # REPO PUBLIK
    (9.60, SOFT, -20, 0.0, 0.7),     # light beam out
    (10.96, SWISH, -22, 0.23, 0.45), # ADMIN
    (12.56, SWISH, -22, 0.23, 0.45), # INPUT
    (14.50, CRACK, -20, 0.04, 0.8),  # line cracks = celah
    (15.80, SAVE, -22, 0.0, 0.8),    # bookmark
    (17.34, IMPW, -22, 0.22, 0.9),   # FOLLOW
    (21.28, SWISH, -24, 0.23, 0.45), # cek lagi.
    (22.94, SWISH, -24, 0.23, 0.4), (23.76, SWISH, -24, 0.23, 0.4), (24.54, SWISH, -24, 0.23, 0.4),
    (26.48, BUB, -22, 0.0, 0.6),     # AI bubble
    (27.06, TAP, -18, 0.0, 0.3),     # "?" stamp
    (28.62, SOFT, -22, 0.0, 0.7),    # diuji
]
if voice_only:
    CUES = []

# person matte segments: (file, start s) — overlaid only on the top band where the words sit
MATTES = [("matte/mA.mov", 3.70), ("matte/mB.mov", 17.30)]
BAND = 700

def run(a):
    return subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace")

inputs = ["-i", src, "-i", RAW]
for f, _ in MATTES:
    inputs += ["-i", f]
vf, cur = [], "[0:v]"
for k, (_, t) in enumerate(MATTES):
    i = 2 + k
    vf.append(f"[{i}:v]format=rgba,crop=1080:{BAND}:0:0,setpts=PTS-STARTPTS+{t}/TB[mt{k}]")
    vf.append(f"{cur}[mt{k}]overlay=0:0:eof_action=pass:format=auto[v{k}]")
    cur = f"[v{k}]"
vf.append(f"{cur}format=yuv420p[vout]")

base = 2 + len(MATTES)
af, labels = [], ["[1:a]"]
for k, (t, f, g, sk, d) in enumerate(CUES):
    inputs += ["-i", f]
    ms = int(t * 1000)
    af.append(f"[{base+k}:a]atrim={sk}:{sk+d},asetpts=PTS-STARTPTS,afade=t=out:st={max(d-0.12,0)}:d=0.12,volume={g}dB,"
              f"adelay={ms}|{ms},aformat=channel_layouts=stereo[s{k}]")
    labels.append(f"[s{k}]")
af.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first[m]")
pre = ";".join(vf + af)

r = run(["ffmpeg", "-hide_banner", *inputs, "-filter_complex", ";".join(af) + ";[m]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[o]",
         "-map", "[o]", "-f", "null", "-"])
js = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}"
      f":measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
r = run(["ffmpeg", "-y", "-hide_banner", "-v", "error", *inputs, "-filter_complex",
         pre + f";[m]{ln},alimiter=limit=0.84:level=false,aresample=48000[o]",
         "-map", "[vout]", "-map", "[o]", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", "29.733", out])
print(r.stderr[-1200:] or "ok", "| measured:", js["input_i"], js["input_tp"])
