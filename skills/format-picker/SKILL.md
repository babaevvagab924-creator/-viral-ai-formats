---
name: format-picker
description: Use when someone has a rough idea, niche, product or topic for a short vertical AI video (Reels, TikTok, Shorts) and needs to choose which viral format to make it in, or asks "what kind of video should I make about X". Recommends the best-fitting formats from the viral-ai-formats library and hands off to that format's skill.
---

# Format Picker

Turns "I want a video about X" into a concrete format choice before any prompt is written.

## How to run it

1. **Read the idea.** If the user gave a topic, niche or product, do not ask more than one question. Infer the rest.
2. **Score formats** on four things (1–5 each):
   - Fit — does the topic naturally live in this format?
   - Hook strength — can the first 2 seconds stop a scroll with sound off?
   - Production cost — fewer clips and one character = cheaper.
   - Series potential — can it become 10+ episodes?
3. **Recommend 3**, best first. For each: one-line pitch of THIS idea in that format, the hook line, clip count, and why it fits.
4. **Ask the user to pick.** Then follow the chosen format skill's workflow.

## Output shape

```
1. <Format name> — <one-line pitch of their idea in this format>
   Hook: "<first on-screen line>"
   Clips: ~N · Characters: N · Series: yes/no
   Why: <one sentence>
2. …
3. …
Which one should we build?
```

## Format map

| Goal / topic | Strong formats |
|---|---|
| History, cultures, eras | how-they-lived, what-if-world, day-in-the-life, time-evolution |
| Fiction, worldbuilding | what-if-world, micro-drama, horror-narration, pov-object |
| Kids-friendly / family humor | silent-cartoon-gag, objects-alive, animal-job, ai-baby-dance |
| Facts, science, education | what-happens-if, scale-comparison, tier-list, myth-explained |
| Product or brand | product-alive, product-hero, ai-presenter, transformation-morph, miniature-world |
| Pure visual / aesthetic | infinite-zoom, transformation-morph, miniature-world, asmr-satisfying, dopamine-edit |
| Music | ai-music-video, dopamine-edit |
| Places, cities, travel | time-evolution, miniature-world, infinite-zoom, day-in-the-life |
| Food | asmr-satisfying, objects-alive, product-hero |

## All formats in the library

what-if-world · how-they-lived · day-in-the-life · pov-object · horror-narration · time-evolution · micro-drama · silent-cartoon-gag · objects-alive · animal-job · ai-baby-dance · tier-list · what-happens-if · scale-comparison · myth-explained · product-alive · product-hero · ai-presenter · infinite-zoom · transformation-morph · dopamine-edit · ai-music-video · miniature-world · asmr-satisfying

## Rules

- Prefer formats with one recurring character for beginners — cheapest path to a series.
- If the idea involves real people, public figures or real brands the user does not own, steer to a format that does not impersonate them.
- Never promise views. Say which formats are proven, not which will go viral.
