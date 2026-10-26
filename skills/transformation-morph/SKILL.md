---
name: transformation-morph
description: Use when making a short AI transformation or morph video — one thing seamlessly turning into another: a sketch becoming a photo, a car through the decades, a room before/after renovation, an animal morphing through species, a dish assembling itself. Produces the transformation chain, matched-composition frame prompts, then start/end-frame morph prompts and captions.
---

# Transformation / Morph

A satisfying before → after in one fluid shot. The brain can't look away from a transformation in progress.

## Ask (max 1 question)
- What transforms into what? — default: suggest 3 chains (sketch→real, era→era, raw→finished).

## The matching rule
Start and end frames must share **composition, camera angle and silhouette position**. The more they match, the smoother the morph.

## Structure (8–30 s)
| Variant | Layout |
|---|---|
| Single morph | 1 hold (1 s) → morph (3–5 s) → hold on result (2 s) |
| Chain | 4–8 morphs, 2–3 s each, ending on the most impressive state |
| Before/after | before hold → wipe or morph → after hold → split-screen |

## Hook formulas
- Visual-first: start on the "before" that looks unfinished or ugly.
- Text: "Watch this [thing] turn into [thing]."
- "From [state] to [state] in [n] seconds."

## Workflow
1. **Concept** — chain of states with a shared composition sentence. Wait for approval.
2. **Frame prompts** — generate state 1, then each next state using the previous image as reference. Wait for approval.
3. **Video prompts** — start frame = state N, end frame = state N+1.
4. **Packaging** — caption, hashtags, sound (whoosh / rising tone).
See `references/models.md`.

## Frame prompt template
```
Vertical 9:16, [SHARED COMPOSITION: centered three-quarter view of the subject on a plain studio floor], [STATE N description], [lighting], [style for this state], same framing and camera position as reference image
```

## Video prompt template (start + end frame)
```
Seamless smooth morph transformation from [state A] into [state B], shapes flow and reform organically, camera completely static, [lighting transition], satisfying continuous motion, no cuts
```

## Packaging
- Optional labels for each state (year, stage).
- Caption: "Which stage is your favorite? 👇"
- Hashtags: #transformation #morph #beforeandafter #satisfying #aivideo

## Common mistakes
- Different camera angles between states → the morph becomes a melt.
- Too many changes at once — change silhouette OR material OR color per step.
- Before/after for real services (renovation, cosmetics) presented as real results when they're AI — label them as concepts.

## Example — "Pencil sketch to sports car"
**Frame A:** `Vertical 9:16, centered three-quarter view of a sports car drawn as a rough graphite pencil sketch on white paper, studio top light`
**Frame B:** `Vertical 9:16, centered three-quarter view of a glossy red sports car in a dark studio, dramatic rim light, photoreal, same framing as reference`
**Video:** `Seamless morph from the pencil sketch into the photoreal red car, lines fill with color and metal reflections, camera static, satisfying continuous motion`
