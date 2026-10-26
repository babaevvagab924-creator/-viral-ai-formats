---
name: time-evolution
description: Use when making a short AI video showing one place, object, city, animal or person-type evolving over time from the same camera angle — "This street from 1000 BC to 3000 AD", "Evolution of the kitchen", "Your city in 500 years". Produces the era list, locked-composition frame prompts, then morph/transition video prompts and captions.
---

# Time Evolution (Same Spot, Many Eras)

One locked camera angle, the world changes around it. The fixed frame lets the brain spot every difference — highly rewatchable.

## Ask (max 2 questions)
- What place/object, and start → end eras? — default: past → present → speculative future.
- How many stops? — default: 8–10.

## The golden rule
**Same composition in every frame.** Same horizon line, same main landmark position, same camera height, same lens. Only the era changes.

## Structure (25–40 s, 8–12 frames)
| Time | Beat |
|---|---|
| 0–2 s | **Year stamp + oldest era** |
| 2–25 s | **Era stops** — 2–3 s each, year overlay each time |
| 25–32 s | **Present day** — recognizable anchor |
| 32–40 s | **Future** — 1–2 speculative stops, the most shared frame |

## Hook formulas
- "This exact spot, from [year] to [year]."
- "[City] in 10,000 years — every 1,000 years."
- "Evolution of the [object] in 30 seconds."

## Workflow
1. **Concept** — place, era list with years, one landmark that stays (river bend, hill, rock). Wait for approval.
2. **Frame prompts** — one master composition sentence pasted in every prompt; vary only era details. Generate frame 1, then use it as image reference for all others. Wait for approval.
3. **Video prompts** — start frame = era N, end frame = era N+1 (start/end-frame models), or quick morph prompts.
4. **Packaging** — year overlays, caption, hashtags.
See `references/models.md`.

## Frame prompt template
```
Vertical 9:16, [MASTER COMPOSITION: e.g. eye-level view down a street with the river bend on the left and the hill in the center background], in the year [YEAR]: [3 era-specific details: buildings, transport, clothing], [era lighting], photoreal, same camera position as reference image
```

## Video prompt template (start + end frame)
```
Smooth time-lapse transition from [era A] to [era B]: buildings rise and change, people and vehicles flicker through, sky cycles day to night once, camera completely locked, landmark stays fixed
```

## Packaging
- Large year number, same position every stop.
- Caption: "Which year would you live in? 👇"
- Hashtags: #evolution #timelapse #throughtheages #aivideo #[city]

## Common mistakes
- Camera angle drifting between eras — always use the previous frame as reference.
- Too many eras with tiny differences — pick visibly distinct ones.
- Inaccurate past details on real places — keep it "inspired by" or check facts.

## Example — "A river valley from 10,000 BC to 3000 AD"
**Frame (1200 AD):** `Vertical 9:16, eye-level view across a river valley, the river bend in the lower left, the twin hills centered in the background, in the year 1200: timber houses, a stone bridge, smoke from chimneys, overcast daylight, photoreal, same camera position as reference`
**Video (1200 → 1800):** `Smooth time-lapse transition: timber houses become brick buildings, a mill wheel appears, the bridge widens, clouds race, camera completely locked, hills fixed`
