# Mix SFX under the voice of a rendered video.
#   python sfx.py sfx.json
# sfx.json:
# { "src": "../../video 02_motion_nosfx.mp4", "out": "../../video 02_motion.mp4", "stem": "../../video 02_sfx_only.wav",
#   "cues": [[0.00,"impact-bass-2",-17,1.4], [3.60,"whoosh",-14,null], ...] }    # [time s, name, target peak dB, max len s|null]
# Library: HyperFrames bundled Pixabay-licensed SFX (whoosh, whoosh-short, pop, click, click-soft, typing, key-press, ping,
# chime, notification, error, glitch-1..3, impact-bass-1/2, riser, sparkle). Each file is peak-normalised to its target,
# so targets are absolute. Video stream is copied; an SFX-only WAV stem is written for CapCut tweaks.
import glob, json, os, re, subprocess, sys

C = json.load(open(sys.argv[1], encoding="utf-8"))
libs = sorted(glob.glob(os.path.expanduser("~/.claude/plugins/cache/hyperframes/hyperframes/*/skills/media-use/audio/assets/sfx/")))
if not libs:
    sys.exit("HyperFrames SFX library not found under ~/.claude/plugins/cache/hyperframes")
LIB = libs[-1]

_peak = {}
def peak(name):
    if name not in _peak:
        r = subprocess.run(["ffmpeg", "-v", "info", "-i", LIB + name + ".mp3", "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True)
        m = re.search(r"max_volume:\s*(-?[\d.]+) dB", r.stderr)
        _peak[name] = float(m.group(1)) if m else 0.0
    return _peak[name]

dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", C["src"]],
                           capture_output=True, text=True, check=True).stdout.strip())
args = ["ffmpeg", "-v", "error", "-y", "-i", C["src"]]
chains, labels = [], []
for k, (t, name, target, maxlen) in enumerate(C["cues"], start=1):
    if not os.path.exists(LIB + name + ".mp3"):
        sys.exit(f"unknown sfx '{name}' (see {LIB})")
    args += ["-i", LIB + name + ".mp3"]
    gain = target - peak(name)
    trim = f"atrim=0:{maxlen},afade=t=out:st={max(maxlen - 0.25, 0)}:d=0.25," if maxlen else ""
    chains.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,{trim}volume={gain:.2f}dB,adelay={int(round(t * 1000))}:all=1[s{k}]")
    labels.append(f"[s{k}]")
fx = ";".join(chains)
fx += f";{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{dur:.3f},asplit=2[sfx][stem]"
fx += ";[0:a]aformat=sample_rates=48000:channel_layouts=stereo[voice];[voice][sfx]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[mix]"
subprocess.run(args + ["-filter_complex", fx, "-map", "0:v", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                       "-movflags", "+faststart", C["out"], "-map", "[stem]", "-c:a", "pcm_s16le", C["stem"]], check=True)
print("cues:", len(labels), "->", C["out"], "+", C["stem"])
