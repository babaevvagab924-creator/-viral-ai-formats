"""Noir soundtrack for promo v5 (30 s): drone, slow heartbeat, ticking clock, lamp, stamps, typewriter, flash.
Reuses the synth helpers from audio.py. Usage: python3 noir_audio.py out.wav"""
import sys, os
import numpy as np
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio.py")).read()
exec(src[: src.index("# ---- music")])          # SR, N, L, R, add, env, lowpass, kick, hat, bass, impact, whoosh, riser, tick, ding, scratch, typing, glitch
t_ = np.arange(N) / SR
# low minor drone (A1 + E2 + slight detune), breathing filter
drone = (np.sin(2 * np.pi * 55 * t_) + 0.6 * np.sin(2 * np.pi * 82.6 * t_) + 0.4 * np.sin(2 * np.pi * 55.4 * t_)) * 0.18
drone *= (0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * t_)) * np.minimum(1, t_ / 1.5)
drone[int(17.85 * SR):int(18.95 * SR)] *= 0.05      # silence for the joke
L += drone; R += drone * 0.95
def thud(big=1.0):
    n = int(0.6 * SR); tt = np.arange(n) / SR; f = 40 + 70 * np.exp(-tt * 25)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9) + lowpass(rs.standard_normal(n), 900) * np.exp(-tt * 30) * 0.6) * big
def click(): n = int(0.03 * SR); return lowpass(rs.standard_normal(n), 4000) * np.exp(-np.arange(n) / SR * 200)
def clocktick(): n = int(0.04 * SR); tt = np.arange(n) / SR; return (np.sin(2 * np.pi * 2200 * tt) + np.sin(2 * np.pi * 1300 * tt)) * np.exp(-tt * 160) * 0.25
def paper(): n = int(0.35 * SR); tt = np.linspace(0, 1, n); return lowpass(rs.standard_normal(n), 2500 + 3000 * tt) * np.sin(np.pi * tt) ** 2 * 0.5
def keys(t0, dur, cps=22):
    for k in range(int(dur * cps)): add(click() * 1.4, t0 + k / cps + rs.uniform(0, 0.02), 0.7, pan=rs.uniform(-0.3, 0.3))
    add(ding(1800), t0 + dur, 0.25)
# heartbeat pulse ~ 72 bpm after the stamp
t = 1.3
while t < 29.4:
    if not (17.85 <= t < 18.95): add(kick() * 0.9, t, 0.8); add(kick() * 0.5, t + 0.22, 0.5)
    t += 60 / 72
# clock ticking all through (louder at midnight)
t = 0.6
while t < 29.4:
    if not (17.85 <= t < 18.95): add(clocktick(), t, 0.9 if 11.5 < t < 14.9 else 0.35, pan=0.4)
    t += 0.5
add(click() * 3, 0.15, 1.0); add(lowpass(rs.standard_normal(int(0.4 * SR)), 300) * np.exp(-np.arange(int(0.4 * SR)) / SR * 6) * 0.3, 0.17, 0.6)   # lamp switch + hum
add(riser(1.2), 0.1, 0.5)
for at, g in [(1.3, 1.3), (20.6, 0.8), (21.0, 0.8), (21.4, 0.8), (25.35, 1.1)]: add(thud(g), at, 1.0)     # stamps
for at in [3.5, 11.5, 20.0, 25.3]: add(impact(0.6), at, 0.7)
for at in [3.4, 5.0, 6.95, 14.85, 23.4]: add(paper(), at, 0.8, pan=rs.uniform(-0.5, 0.5))
keys(1.8, 1.0); keys(8.6, 1.1); keys(13.3, 0.6); keys(18.05, 0.9); keys(20.05, 0.7)
for a, d in [(3.7, 0.9), (5.15, 1.0), (7.1, 1.4), (16.0, 1.5)]:
    for k in range(int(d / 0.05)): add(tick(), a + k * 0.05, 0.4)
n = int(0.5 * SR); add(rs.standard_normal(n) * np.exp(-np.arange(n) / SR * 14) * 0.9, 17.85, 1.0)   # camera flash pop
add(ding(1320), 18.6, 0.4)
add(thud(1.4), 29.5, 1.0); add(click() * 3, 29.5, 1.0)    # lamp off
peak = max(np.abs(L).max(), np.abs(R).max()); L /= peak / 0.89; R /= peak / 0.89
import wave
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([L, R], 1) * 32767).astype(np.int16).tobytes())
print("noir audio ok")
