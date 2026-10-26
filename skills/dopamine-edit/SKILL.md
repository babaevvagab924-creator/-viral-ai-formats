---
name: dopamine-edit
description: Use when making a high-energy, fast-cut AI edit — glitch transitions, beat-synced cuts every 0.3–1 s, speed ramps, flashes, rapid aesthetic montages ("cyberpunk Tokyo edit", "dark academia edit", "villain era edit") for Reels, TikTok or Shorts. Produces the beat map, a bank of short-clip frame prompts, then micro-motion video prompts and edit instructions.
---

# Dopamine Edit (Fast-Cut Aesthetic)

Rhythm, contrast, momentum. Lots of short clips cut to a beat — viewers replay to catch details they missed.

## Ask (max 2 questions)
- Aesthetic/theme? — default: pick a trending aesthetic (cyberpunk, dark academia, retro anime, Y2K).
- Song tempo (BPM) or trending sound? — default: ~120–140 BPM.

## Structure (10–20 s, 12–25 micro-clips)
| Time | Beat |
|---|---|
| 0–1 s | **Strongest image** on the first beat |
| 1–8 s | **Build** — cut every 2 beats, wide → medium |
| 8–9 s | **Drop** — flash/glitch transition |
| 9–18 s | **Peak** — cut every beat, close-ups, speed ramps |
| last 1 s | **Hero frame** held, or loop back to frame 1 |

## Beat math
- Seconds per beat = 60 ÷ BPM (128 BPM ≈ 0.47 s).
- Each video clip only needs ~1–2 s of usable motion — generate 3–5 s and trim.

## Workflow
1. **Concept** — aesthetic, palette (2–3 colors), beat map with clip slots. Wait for approval.
2. **Frame prompts** — a bank of 12–25 frames in one locked palette and style line. Wait for approval.
3. **Video prompts** — fast, punchy single motions; vary camera moves.
4. **Edit sheet** — clip order, cut points per beat, transitions (glitch, flash, whip), speed ramps. For CapCut or similar.
See `references/models.md`.

## Frame prompt template
```
Vertical 9:16, [shot type] of [subject in the aesthetic], [one striking detail], [PALETTE: e.g. neon magenta and cyan], [AESTHETIC STYLE LINE], high contrast, cinematic, sharp
```

## Video prompt template
```
[One fast motion: hair whips / neon sign flickers / car streaks past / head turns to camera], camera [crash zoom / whip pan / fast dolly], high energy, motion blur, style unchanged
```

## Packaging
- Use the platform's trending audio (licensed in-app).
- Minimal or no text; one title word at most.
- Caption: "Which frame is your wallpaper? 🔁"
- Hashtags: #edit #aesthetic #[aesthetic]edit #aiart #aivideo

## Common mistakes
- Mixed palettes → looks random; lock 2–3 colors.
- All clips with the same camera move — alternate.
- Cuts off-beat; snap to the beat grid.

## Example — "Rainy cyberpunk night"
**Frame:** `Vertical 9:16, close-up of a woman in a reflective black raincoat under a neon umbrella, rain droplets frozen in magenta and cyan light, cyberpunk city bokeh, high contrast, cinematic`
**Video:** `She snaps her head toward camera, rain streaks past, camera crash zoom, high energy, motion blur`
