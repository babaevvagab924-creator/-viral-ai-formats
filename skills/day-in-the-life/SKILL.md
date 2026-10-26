---
name: day-in-the-life
description: Use when making a short AI "day in the life" video — a full day compressed into 30–60 seconds for a job, era, creature, fictional role or place (e.g. "A day as a lighthouse keeper in 1890", "A day in the life of a dragon's dentist"). Produces timestamped beats, storyboard frame prompts, then video prompts and captions.
---

# A Day in the Life of…

A clock ticking through one day. The timestamps create a built-in progress bar, so people stay to see "the night part".

## Ask (max 2 questions)
- Whose day? (real job, past era, fantasy role, animal) — default: an unusual real job or a past-era job.
- Narrated or text-only? — default: on-screen timestamps + short text, no VO.

## Structure (30–50 s, 8–10 clips)
| Time | Beat |
|---|---|
| 0–2 s | **"5:00 AM"** — wake-up in the most unusual setting | 
| 2–8 s | **Morning ritual** — the weird prep step |
| 8–25 s | **3 work moments** — routine → hardest task → unexpected moment |
| 25–35 s | **Break/meal** — what they eat, where |
| 35–45 s | **Night** — the part nobody sees |
| 45–50 s | **Reflection line** — "Would you take this job?" |

## Hook formulas
- "5:00 AM. Day 1 as a [role]."
- "A day in the life of a [role] in [year]."
- "Nobody shows you this part of being a [role]."

## Workflow
1. **Concept** — role, character descriptor, 8–10 timestamped beats. Wait for approval.
2. **Frame prompts** — same descriptor in every frame; lighting changes with the clock (dawn → noon → dusk → night). Wait for approval.
3. **Video prompts** — one action per clip.
4. **Packaging** — timestamp overlays, caption, hashtags.
See `references/models.md`.

## Frame prompt template
```
Vertical 9:16, [shot type] of [CHARACTER DESCRIPTOR] [action] in [workplace], [time-of-day lighting: blue dawn / harsh noon / golden dusk / lamp-lit night], [style line], cinematic, upper third clear for timestamp text
```

## Video prompt template
```
[Character] [one action], [environmental motion], camera [move], [pace], same face and outfit as start frame
```

## Packaging
- Timestamp in the same font and corner every clip ("5:00 AM", "7:30 AM"…).
- Caption: "Rate this job 1–10 👇"
- Hashtags: #dayinthelife #ditl #[role] #aivideo

## Common mistakes
- Same lighting all day — the clock must be visible in the light.
- Only the glamorous moments — the hard/gross/boring part is the retention peak.
- Timestamps out of order or too many (max 8).

## Example — "A day as a lighthouse keeper, 1890"
**Frame 1 (4:45 AM):** `Vertical 9:16, medium shot of a weathered man, 50s, grey beard, navy wool coat, brass buttons, climbing a spiral iron staircase holding an oil can, blue pre-dawn light through a small window, painterly realism`
**Video 1:** `Man climbs two steps and pauses to catch breath, wind rattles the window, camera slow tilt up the spiral, quiet, face and coat unchanged`
