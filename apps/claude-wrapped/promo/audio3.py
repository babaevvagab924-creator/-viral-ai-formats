"""Synthesize music + sound effects for promo2 (28 s), timed to the animation.
Usage: python3 audio.py out.wav"""
import sys, wave
import numpy as np

SR, DUR = 44100, 30.0
N = int(SR * DUR)
L = np.zeros(N); R = np.zeros(N)
rs = np.random.default_rng(7)

def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR); sig = sig[: max(0, N - i)]
    L[i:i + len(sig)] += sig * gain * (1 - max(0, pan)); R[i:i + len(sig)] += sig * gain * (1 + min(0, pan))

def env(n, a, d):  # attack/decay in seconds
    t = np.arange(n) / SR; e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d); return e

def lowpass(sig, cutoff):
    cutoff = np.broadcast_to(cutoff, sig.shape); out = np.zeros_like(sig); y = 0.0
    a = 1 - np.exp(-2 * np.pi * cutoff / SR)
    for i in range(len(sig)): y += a[i] * (sig[i] - y); out[i] = y
    return out

def kick():
    n = int(0.35 * SR); t = np.arange(n) / SR; f = 45 + 110 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.16)

def hat():
    n = int(0.06 * SR); w = rs.standard_normal(n); w = np.diff(w, prepend=0); return w * env(n, 0.001, 0.015) * 0.5

def clap():
    n = int(0.2 * SR); w = rs.standard_normal(n); e = env(n, 0.001, 0.05)
    for k in (0.01, 0.02): e += env(n, 0.001, 0.05) * (np.arange(n) >= k * SR)
    return lowpass(w, 2500) * e * 0.6

def bass(freq, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * freq * h * t) / h for h in range(1, 6))
    return lowpass(s, 600) * env(n, 0.005, dur * 0.6) * 0.5

def impact(big=1.0):
    n = int(1.4 * SR); t = np.arange(n) / SR; f = 28 + 90 * np.exp(-t * 9)
    low = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.55)
    noise = lowpass(rs.standard_normal(n), 3000) * env(n, 0.001, 0.08)
    return (low * 1.2 + noise * 0.8) * big

def whoosh(dur=0.45):
    n = int(dur * SR); t = np.linspace(0, 1, n); e = np.sin(np.pi * t) ** 2
    return lowpass(rs.standard_normal(n), 300 + 5000 * t) * e * 0.9

def riser(dur):
    n = int(dur * SR); t = np.linspace(0, 1, n)
    tone = np.sin(2 * np.pi * np.cumsum(200 + 1400 * t ** 2) / SR) * 0.25
    return (lowpass(rs.standard_normal(n), 200 + 7000 * t ** 2) * 0.6 + tone) * t ** 1.5

def tick():
    n = int(0.02 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * 3200 * t) * env(n, 0.0005, 0.005) * 0.4

def ding(f=1320):
    n = int(0.9 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.01 * t) + 0.25 * np.sin(2 * np.pi * f * 3 * t)) * env(n, 0.002, 0.25) * 0.35

def scratch():
    n = int(0.4 * SR); t = np.linspace(0, 1, n); f = 300 + 1600 * np.abs(np.sin(t * np.pi * 3))
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4 + lowpass(rs.standard_normal(n), f) * 0.6) * np.sin(np.pi * t)

def typing(t0, dur, cps):
    for k in range(int(dur * cps)): add(tick() * 0.8, t0 + k / cps, 0.6, pan=rs.uniform(-0.3, 0.3))

def glitch(dur=0.3):
    n = int(dur * SR); s = np.sign(np.sin(2 * np.pi * 80 * np.arange(n) / SR)) * (rs.random(n) > 0.6)
    return s * 0.25 * np.linspace(1, 0, n)

# ---- music: 125 bpm, A minor, starts on the stamp ----
BPM = 125; beat = 60 / BPM; start = 1.48
notes = [55.0, 55.0, 43.65, 49.0]  # A1 A1 F1 G1 per bar
t = start; b = 0
while t < 29.4:
    silent = 17.85 <= t < 18.95  # comedic pause for "massager"
    if not silent:
        add(kick(), t, 0.9)
        add(hat(), t + beat / 2, 0.5, pan=0.2)
        if b % 2 == 1: add(clap(), t, 0.5)
        if b % 4 == 0: add(bass(notes[(b // 4) % 4], beat * 4), t, 0.8)
    b += 1; t += beat
# intro: typing + riser
typing(0.05, 1.0, 40)
add(riser(1.3), 0.0, 0.7)
add(glitch(0.3), 1.0, 0.8)
for ti, g in [(1.48, 1.3), (3.5, 0.6), (11.5, 0.7), (17.85, 0.4), (20.0, 0.8), (25.3, 0.6), (28.6, 0.5)]: add(impact(g), ti, 0.9)
for ti in [3.3, 6.8, 11.3, 14.65, 19.8, 23.05, 25.1]: add(whoosh(), ti, 0.7, pan=rs.uniform(-0.4, 0.4))
for a, d in [(3.65, 1.0), (7.5, 1.2), (16.05, 1.6)]:  # slot counters
    for k in range(int(d / 0.045)): add(tick(), a + k * 0.045, 0.5)
add(scratch(), 17.85, 0.9)
typing(18.1, 1.0, 30)
for k, ti in enumerate([20.6, 21.0, 21.4]): add(ding(1320 * (1.12 ** k)), ti, 0.8)
add(tick() * 3, 26.25, 1.0)  # tap
for k in range(5): add(whoosh(0.3), 26.45 + k * 0.08, 0.35, pan=(k - 2) * 0.3)
add(ding(1760), 28.6, 0.6)
# ---- v3 extras: montage glitch hits, tape swooshes, rip sounds, hard-cut ending ----
for k in range(6): add(glitch(0.08), k * 0.09, 1.0); add(tick() * 2, k * 0.09, 0.8)
for at in [3.5, 7.0, 14.85, 23.25, 25.3]: add(whoosh(0.35), at - 0.2, 0.6, pan=-0.5); add(whoosh(0.35), at - 0.12, 0.6, pan=0.5)
def rip():
    n = int(0.25 * SR); t = np.linspace(0, 1, n); return lowpass(rs.standard_normal(n), 1500 + 6000 * t) * np.exp(-t * 6) * 0.9
for at in [3.68, 7.15, 12.55, 16.15, 24.1]: add(rip(), at, 0.8)
add(impact(0.9), 29.5, 1.0)
# master: fade out, normalize
fade = np.ones(N); fl = int(0.15 * SR); fade[-fl:] = np.linspace(1, 0, fl)
L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max()); L /= peak / 0.89; R /= peak / 0.89
data = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())
print("audio ok")
