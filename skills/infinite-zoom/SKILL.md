---
name: infinite-zoom
description: Use when making a seamless infinite zoom-in or zoom-out AI video — diving from space into a city into a room into an eye into a galaxy, or a loop that returns to the first frame — the hypnotic "never-ending zoom" format. Produces the nested scene chain, outpaint/inpaint-ready frame prompts, then zoom video prompts and loop instructions.
---

# Infinite Zoom

One continuous dive through nested worlds. Hypnotic, loopable, and replayed again and again — loop rewatches boost reach.

## Ask (max 1 question)
- Zoom in or out, and the theme? — default: zoom in, "from the universe to a single cell and back to a universe".

## The nesting rule
Each scene must contain the next scene **in the exact center** of the frame (a window, a pupil, a screen, a drop of water, a painting). The next scene starts as that small center detail.

## Structure (15–30 s, 6–10 layers)
| Time | Beat |
|---|---|
| 0–2 s | **Layer 1** — wide, recognizable |
| 2–25 s | **Layers 2–9** — each 2–3 s, increasingly surprising |
| last 2 s | **Final layer looks like Layer 1** → seamless loop |

## Two production routes
- **Video route** — generate each layer as a frame, then image-to-video with "continuous push-in toward the center"; use start/end frames where the end frame is the next layer.
- **Image route** — generate one frame, then zoom out by outpainting repeatedly (each new image contains the previous one shrunk in the center), and animate the zoom in an editor.

## Workflow
1. **Concept** — layer chain with the "portal" object in each center. Wait for approval.
2. **Frame prompts** — every frame specifies the centered portal object. Wait for approval.
3. **Video prompts** — straight push-in, no rotation, constant speed.
4. **Packaging** — loop check, caption, hashtags, sound.
See `references/models.md`.

## Frame prompt template
```
Vertical 9:16, [LAYER SCENE], perfectly centered in the frame is [PORTAL: a small round window / an eye / a glowing screen] showing [glimpse of the next scene], symmetrical composition, [lighting], [consistent style line], highly detailed
```

## Video prompt template
```
Smooth continuous camera push-in straight toward the exact center of the frame, entering the [portal] which fills the screen and reveals [next scene], constant speed, no rotation, dreamlike seamless transition
```

## Packaging
- No text, or one line at the start ("Keep watching…").
- Caption: "How many times did you watch it? 🔁"
- Hashtags: #infinitezoom #loop #satisfying #aiart #aivideo

## Common mistakes
- Portal off-center → the zoom path jumps.
- Speed changing between clips → visible seams; keep "constant speed".
- No loop ending — the replay is the point.

## Example — "Eye to galaxy"
**Frame 1:** `Vertical 9:16, extreme close-up of a human eye, perfectly centered in the pupil is a tiny glowing spiral galaxy, symmetrical composition, soft studio light, hyperreal macro detail`
**Video 1:** `Smooth continuous camera push-in straight into the pupil, the galaxy grows until it fills the screen, constant speed, no rotation, dreamlike`
