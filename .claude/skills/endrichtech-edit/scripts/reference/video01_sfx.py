# Mix SFX (HyperFrames bundled Pixabay-licensed library) under the voice of video 01_motion.mp4.
# Each cue is peak-normalised to a target level so effects sit under the voice (voice mean ≈ -16.7 dB).
# Outputs: the video with SFX mixed in (video stream copied) + an SFX-only WAV for CapCut tweaks.
import subprocess

LIB = "C:/Users/aceru/.claude/plugins/cache/hyperframes/hyperframes/0.8.111/skills/media-use/audio/assets/sfx/"
SRC = "../../hasil/video01/video 01_motion.mp4"
OUT = "../../hasil/video01/video 01_motion_sfx.mp4"
STEM = "../../hasil/video01/video 01_sfx_only.wav"
PEAK = {"impact-bass-1": -0.4, "impact-bass-2": 0.0, "whoosh": -2.1, "whoosh-short": -2.1, "pop": -3.2,
        "click": -5.4, "click-soft": -5.4, "typing": -9.0, "chime": -9.3, "ping": -6.2, "error": -21.2,
        "glitch-1": 0.0, "notification": -2.7, "sparkle": 0.0, "key-press": -5.7}

# (time s, sfx, target peak dB, optional max length s)
CUES = [
    (0.00, "impact-bass-2", -17, 1.4),      # hook: JANGAN
    (2.88, "whoosh-short", -17, None),      # "ini alasannya."
    (3.60, "whoosh", -14, None),            # split in: chat
    (4.70, "typing", -17, 1.25),            # question typed
    (6.18, "click-soft", -21, None), (6.32, "click-soft", -21, None),  # AI typing dots
    (6.62, "pop", -14, None),               # Rp25.000/kotak
    (7.04, "chime", -17, 1.2),              # terdengar meyakinkan
    (7.76, "glitch-1", -14, 0.9),           # B&W "tapi angkanya dari mana?"
    (8.48, "error", -14, None),             # red "?"
    (9.04, "whoosh", -14, None),            # split in: AI nggak tahu
    (10.16, "pop", -16, None), (10.46, "click", -20, None),
    (11.90, "pop", -16, None), (12.20, "click", -20, None),
    (12.92, "pop", -16, None), (13.22, "click", -20, None),
    (13.92, "pop", -16, None), (14.22, "click", -20, None),
    (14.92, "whoosh-short", -17, None),     # swipe to DAYA BELI
    (15.16, "pop", -15, None),
    (16.06, "impact-bass-1", -22, 1.0),
    (16.92, "error", -16, None),
    (18.12, "whoosh", -15, None),           # back to face
    (19.26, "pop", -15, None), (20.24, "pop", -15, None),
    (21.26, "impact-bass-1", -19, 1.2),     # red card
    (21.92, "impact-bass-2", -19, 0.9),     # RUGI
    (22.56, "whoosh-short", -13, None),     # KEMAHALAN
    (22.62, "pop", -15, None),
    (23.30, "whoosh", -15, None),           # back to face
    (24.16, "ping", -13, None),             # bulb idea
    (25.04, "whoosh", -14, None),           # split in: hitung
    (25.26, "click", -18, None), (25.64, "click", -18, None), (25.80, "click", -18, None), (26.04, "click", -18, None),
    (27.20, "whoosh-short", -19, None),
    (27.50, "chime", -14, 1.6),             # = MODAL PER PORSI
    (29.06, "notification", -16, 1.4),      # biaya yang mungkin kamu lupa
    (30.86, "whoosh", -15, None),           # back to face
    (31.66, "pop", -15, None), (32.06, "click", -17, None),
    (33.77, "impact-bass-1", -19, 1.2),    # KAMU
    (34.76, "pop", -14, None), (34.80, "sparkle", -19, 1.2),  # FOLLOW
]

args = ["ffmpeg", "-v", "error", "-y", "-i", SRC]
chains, labels = [], []
for k, (t, name, target, maxlen) in enumerate(CUES, start=1):
    args += ["-i", LIB + name + ".mp3"]
    gain = target - PEAK[name]
    trim = f"atrim=0:{maxlen},afade=t=out:st={max(maxlen - 0.25, 0)}:d=0.25," if maxlen else ""
    ms = int(round(t * 1000))
    chains.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,{trim}volume={gain}dB,adelay={ms}:all=1[s{k}]")
    labels.append(f"[s{k}]")
n = len(CUES)
fx = ";".join(chains)
fx += f";{''.join(labels)}amix=inputs={n}:normalize=0:duration=longest,atrim=0:36.37,asplit=2[sfx][stem]"
fx += ";[0:a]aformat=sample_rates=48000:channel_layouts=stereo[voice];[voice][sfx]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[mix]"
cmd = args + ["-filter_complex", fx,
              "-map", "0:v", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT,
              "-map", "[stem]", "-c:a", "pcm_s16le", STEM]
subprocess.run(cmd, check=True)
print("cues:", n, "->", OUT, "+", STEM)
