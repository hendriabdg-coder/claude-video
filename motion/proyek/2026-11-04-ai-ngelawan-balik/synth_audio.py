# SFX + musik latar disintesis sendiri (numpy), bebas lisensi. Dipakai di sesi cloud karena library Epidemic `new sfx/`
# tidak ada dan file ElevenLabs tidak bisa diunduh dari server cloud (sama seperti hari 3).
# Menulis audio/{hit,whoosh,pop,glitch,ding,tick,musik}.mp3 untuk mix.py.   python synth_audio.py
import subprocess
from pathlib import Path

import numpy as np

SR = 48000
OUT = Path(__file__).resolve().parent / "audio"
rng = np.random.default_rng(4)


def t_(d):
    return np.arange(int(SR * d)) / SR


def lp(x, a):  # one-pole low-pass, a in (0,1): smaller = darker
    y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x):
        s += a * (v - s); y[i] = s
    return y


def lp_fast(x, cutoff):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / cutoff) ** 4), len(x))


def hp_fast(x, cutoff):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * (f / cutoff) ** 2 / np.sqrt(1 + (f / cutoff) ** 4), len(x))


def save(name, x, stereo=None):
    data = x if stereo is None else stereo
    data = data / (np.abs(data).max() + 1e-9) * 0.89
    ch = 1 if data.ndim == 1 else 2
    raw = (np.clip(data, -1, 1) * 32767).astype(np.int16).tobytes()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", str(ch), "-i", "-",
                    "-b:a", "256k", str(OUT / f"{name}.mp3")], input=raw, check=True)


def hit():
    t = t_(1.6)
    f = 38 + 90 * np.exp(-t * 18)                       # pitch-drop kick
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    click = lp_fast(rng.standard_normal(len(t)), 3500) * np.exp(-t * 60) * 0.6
    tail = lp_fast(rng.standard_normal(len(t)), 900) * np.exp(-t * 6) * 0.25
    return np.tanh(1.6 * (body + click + tail))


def whoosh():
    d = 0.8; t = t_(d)
    n = rng.standard_normal(len(t))
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2.2 * np.exp(-((t - 0.42) ** 2) / 0.05)
    out = np.zeros_like(n)
    for k in range(8):  # sweeping band: crossfade a bank of band-passed noise
        lo, hi = 300 * 1.6 ** k, 300 * 1.6 ** (k + 1)
        band = hp_fast(lp_fast(n, hi), lo)
        c = 0.35 + 0.6 * k / 7
        out += band * np.exp(-((t / d - c) ** 2) / 0.02)
    return out * env


def pop():
    t = t_(0.18)
    f = 900 + 1400 * np.exp(-t * 60)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 38) + lp_fast(rng.standard_normal(len(t)), 6000) * np.exp(-t * 300) * 0.3


def glitch():
    d = 0.8; t = t_(d); x = np.zeros_like(t)
    seg = int(SR * 0.04)
    for i in range(0, len(t) - seg, seg):
        kind = rng.integers(3)
        tt = t[:seg]
        if kind == 0:
            x[i:i + seg] = np.sign(np.sin(2 * np.pi * rng.uniform(200, 1800) * tt)) * 0.5
        elif kind == 1:
            x[i:i + seg] = rng.standard_normal(seg) * 0.6
        else:
            x[i:i + seg] = 0
    x = np.round(x * 6) / 6                              # bitcrush
    f = 70 * np.exp(-t * 2.5) + 30
    drop = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    return (x * np.exp(-t * 2.5) * 0.6 + drop) * np.minimum(1, (d - t) / 0.08)


def ding():
    t = t_(1.2); x = np.zeros_like(t)
    for st, fr in ((0.0, 1318.5), (0.11, 1760.0)):        # E6 -> A6
        m = t >= st; tt = t[m] - st
        x[m] += (np.sin(2 * np.pi * fr * tt) + 0.3 * np.sin(2 * np.pi * fr * 2.01 * tt)) * np.exp(-tt * 5) * np.minimum(1, tt / 0.004)
    return x


def tick():
    d = 4.2; t = t_(d); x = np.zeros_like(t)
    tt = t_(0.012)
    blip = np.sin(2 * np.pi * 3200 * tt) * np.exp(-tt * 500)
    pos, gap = 0.0, 0.035
    while pos < d - 0.02:
        i = int(pos * SR); x[i:i + len(blip)] += blip * rng.uniform(0.7, 1.0)
        pos += gap; gap = min(gap * 1.012, 0.09)
    return x


def music(d=44.0, bpm=110):
    t = t_(d); beat = 60 / bpm; L = np.zeros_like(t); R = np.zeros_like(t)
    # Am - F - C - G, two bars each
    chords = [(57, 60, 64), (53, 57, 60), (48, 55, 64), (55, 59, 62)]
    bass = [45, 41, 48, 43]
    bar = 4 * beat

    def hz(m):
        return 440 * 2 ** ((m - 69) / 12)

    # pad: detuned saws, slow attack, darkened
    pad = np.zeros_like(t)
    for ci in range(int(d / (2 * bar)) + 1):
        c = chords[ci % 4]; st = ci * 2 * bar; en = min(st + 2 * bar, d)
        m = (t >= st) & (t < en); tt = t[m] - st
        seg = np.zeros(m.sum())
        for n in c:
            for det in (-0.12, 0.12):
                ph = (hz(n + det) * tt) % 1
                seg += 2 * ph - 1
        env = np.minimum(1, tt / 0.6) * np.minimum(1, (en - st - tt) / 0.4)
        pad[m] += seg * env
    pad = lp_fast(pad, 1100) * 0.18
    lfo = 0.8 + 0.2 * np.sin(2 * np.pi * t / (2 * bar))
    pad *= lfo
    # sub bass: 8th-note pulse
    sub = np.zeros_like(t)
    k = 0
    while k * beat / 2 < d:
        st = k * beat / 2; ci = int(st / (2 * bar)) % 4
        tt = t_(beat / 2 * 0.9); i = int(st * SR); n = min(len(tt), len(t) - i)
        note = np.sin(2 * np.pi * hz(bass[ci] - 12) * tt[:n]) + 0.25 * np.sin(2 * np.pi * hz(bass[ci]) * tt[:n])
        sub[i:i + n] += note * np.exp(-tt[:n] * 7) * (1.0 if k % 2 == 0 else 0.7)
        k += 1
    sub *= 0.55
    # drums: soft kick on 1 & 3, closed hats on 8ths, rim on 2 & 4; intro light, build in last 15 s
    dr = np.zeros_like(t); hatL = np.zeros_like(t); hatR = np.zeros_like(t)
    kt = t_(0.35); kick = np.sin(2 * np.pi * np.cumsum(45 + 80 * np.exp(-kt * 30)) / SR) * np.exp(-kt * 9)
    ht = t_(0.05); hat = hp_fast(rng.standard_normal(len(ht)), 7000) * np.exp(-ht * 90)
    rt = t_(0.12); rim = (hp_fast(rng.standard_normal(len(rt)), 1500) * 0.6 + np.sin(2 * np.pi * 820 * rt)) * np.exp(-rt * 45)
    k = 0
    while k * beat / 2 < d:
        st = k * beat / 2; i = int(st * SR)
        build = 1.0 if st < d - 15 else 1.25
        def add(buf, s, g):
            n = min(len(s), len(t) - i); buf[i:i + n] += s[:n] * g
        if st >= 0.0:
            if k % 4 == 0:
                add(dr, kick, 0.9 * build)
            if k % 4 == 2 and st > bar:
                add(dr, rim, 0.22 * build)
            if st > 2 * bar or k % 2 == 1:
                g = (0.16 if k % 2 else 0.10) * build
                add(hatL, hat, g * 0.8); add(hatR, hat, g * 1.2)
        k += 1
    # opening downbeat accent (hentakan musik di detik 0)
    acc = np.zeros_like(t); a = hit() * 0.6; acc[:len(a)] += a
    mono = pad + sub + dr + acc
    L = mono + hatL + np.roll(pad, int(0.011 * SR)) * 0.25
    R = mono + hatR + np.roll(pad, int(0.017 * SR)) * 0.25
    fade = np.minimum(1, (d - t) / 2.0)
    return np.stack([L * fade, R * fade], 1)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, fn in (("hit", hit), ("whoosh", whoosh), ("pop", pop), ("glitch", glitch), ("ding", ding), ("tick", tick)):
        save(name, fn())
    save("musik", None, stereo=np.tanh(music() * 1.2))
    print("ok ->", OUT)
