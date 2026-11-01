# Audio for the AI web-security edit: original dialog (untouched timing) + a few soft SFX from the Epidemic
# library on key graphic events, then -14 LUFS / TP -1.5 dBFS (two-pass loudnorm).
#   python mix.py renders/overlay.mp4 <out.mp4> [--voice-only]
import json, subprocess, sys

src_video, out = sys.argv[1], sys.argv[2]
voice_only = "--voice-only" in sys.argv
RAW = "../../mentah/ai-web-security/Video Mentah.mp4"
L = "../../../new sfx/"
SOFT = L + "whosh/ES_Swooshes, Whoosh, Softs - Epidemic Sound.mp3"
POP = L + "ui/ES_User Interface, Click, Software, Interface, Pop Up, Notification - Epidemic Sound.mp3"
CLICK = L + "ui/ES_User Interface, Click, Button, Double Click, Fast, Phone Tap - Epidemic Sound.mp3"
SAVE = L + "ES_Text Message, Notification, Confirm, Round, Soft - Epidemic Sound.mp3"
MARK = L + "hight light/ES_Objects, Writing, Text, Highlight Drag, Marker Highlighter - Epidemic Sound.mp3"
BUB = L + "ui/ES_Text Message, Notification, Round Tone, Clicky - Epidemic Sound.mp3"

# (time s, file, gain dB, max length s)
CUES = [
    (0.00, SOFT, -20, 0.9),    # hook lands on frame 0
    (3.44, POP, -22, 0.4),     # ≠
    (7.30, SOFT, -24, 0.7),    # risk card 01
    (10.60, CLICK, -24, 0.3),  # card 02
    (12.56, CLICK, -24, 0.3),  # card 03
    (14.50, POP, -22, 0.4),    # = CELAH KEAMANAN
    (15.80, SAVE, -22, 0.8),   # SIMPAN DULU
    (20.66, SOFT, -24, 0.7),   # checklist in
    (22.98, MARK, -26, 0.35), (23.80, MARK, -26, 0.35), (24.58, MARK, -26, 0.35),
    (27.06, BUB, -22, 0.6),    # "Beres!" bubble
]
if voice_only:
    CUES = []

def run(args):
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")

inputs = ["-i", src_video, "-i", RAW]
fl, labels = [], ["[1:a]"]
for k, (t, f, g, d) in enumerate(CUES):
    inputs += ["-i", f]
    ms = int(t * 1000)
    fl.append(f"[{k+2}:a]atrim=0:{d},afade=t=out:st={max(d-0.12,0)}:d=0.12,volume={g}dB,adelay={ms}|{ms},aformat=channel_layouts=stereo[s{k}]")
    labels.append(f"[s{k}]")
pre = ";".join(fl + [f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first[m]"])

# pass 1: measure
r = run(["ffmpeg", "-hide_banner", *inputs, "-filter_complex", pre + ";[m]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[o]",
         "-map", "[o]", "-f", "null", "-"])
js = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}"
      f":measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
# pass 2: apply + safety limiter, keep the rendered video stream as is
r = run(["ffmpeg", "-y", "-hide_banner", "-v", "error", *inputs, "-filter_complex",
         pre + f";[m]{ln},alimiter=limit=0.84:level=false,aresample=48000[o]",
         "-map", "0:v", "-map", "[o]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out])
print(r.stderr[-800:] or "ok", "| measured:", js["input_i"], js["input_tp"])
