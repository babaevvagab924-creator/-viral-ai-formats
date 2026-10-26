---
name: scale-comparison
description: Use when making a short AI size or scale comparison video — "How big is the biggest animal ever compared to you?", "Monsters by size", "Ships through history next to a human", "Planets compared" — a camera pulling back as objects grow. Produces the ordered item list with sizes, consistent-scale frame prompts, then zoom-out video prompts and captions.
---

# Scale Comparison

Things lined up from small to impossibly big, with a human for reference. Pure visual awe — works muted and in any language.

## Ask (max 1 question)
- Category? — default: animals extinct and living, with a human silhouette.

## Accuracy rules
- Use widely published sizes; round honestly ("about 30 m").
- Keep one reference object (a 1.75 m human, a bus) visible in every frame.
- For fictional things, say "fictional" on screen.

## Structure (25–45 s, 8–12 frames)
| Time | Beat |
|---|---|
| 0–2 s | **Small and relatable** — a human or a house cat |
| 2–35 s | **Each bigger item** — 2–3 s, camera pulls back |
| 35–42 s | **The absurd final item** — fills the screen |
| 42–45 s | **Reference reminder** — tiny human dot |

## Hook formulas
- "You vs. the biggest [thing] ever."
- "How small you really are next to [category]."
- "[Category] by size. Wait for the last one."

## Workflow
1. **Concept** — ordered list with sizes, the reference object, background (flat ground line + sky). Wait for approval.
2. **Frame prompts** — same ground line, same side-on orthographic-like angle, reference human at fixed position. Wait for approval.
3. **Video prompts** — continuous pull-back/zoom-out between frames (start/end frames ideal).
4. **Packaging** — size labels, caption, hashtags.
See `references/models.md`.

## Frame prompt template
```
Vertical 9:16, side view on a flat plain with a horizon line at the lower third, a [REFERENCE: 1.75 m human silhouette in red] standing on the left, next to [ITEM] shown at accurate relative scale, clear daylight, clean realistic render, size-comparison infographic style, no clutter
```

## Video prompt template
```
Smooth continuous camera pull-back revealing [next bigger item] beside the previous ones, everything stays at correct relative scale, ground line fixed, calm awe
```

## Packaging
- Label each item with name + size in the same font.
- Caption: "Which one surprised you? 👇"
- Hashtags: #scale #sizecomparison #howbig #science #aivideo

## Common mistakes
- Inconsistent camera angle → sizes become unreadable.
- Losing the reference object — awe needs a ruler.
- Sizes made up for drama.

## Example — "Sea creatures vs. you"
**Frame (blue whale):** `Vertical 9:16, side view underwater with a sandy seabed line at the lower third, a tiny diver in a red wetsuit on the left, a blue whale stretching across the frame at accurate relative scale, sunbeams from above, clean realistic render, infographic style`
**Video:** `Smooth continuous camera pull-back, the whale's full length is revealed next to the tiny diver, seabed fixed, calm awe`
