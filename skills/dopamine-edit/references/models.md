# Model cheatsheet — adapting prompts per tool

Every format skill writes prompts in two passes:

1. **Frame prompts** (still images, one per storyboard beat) — for Nano Banana, Higgsfield Soul, Midjourney, Flux, GPT-Image, etc.
2. **Video prompts** (one per frame, image-to-video) — for Kling, Veo, Seedance, Higgsfield, Runway, Hailuo, Wan, etc.

Always generate and approve the frames first. Image-to-video from a locked frame is cheaper and far more consistent than text-to-video.

Model capabilities change fast. Treat the notes below as starting habits, not specs — check the tool's current docs for durations, aspect ratios and pricing.

## Universal frame prompt order

`[shot type] of [subject + locked character descriptor], [action/pose], [setting], [lighting], [style], [camera/lens], [aspect ratio]`

- Paste the **locked character descriptor** verbatim in every frame. Never shorten it — that is where faces drift.
- One frame = one moment. No "then".
- Put the aspect ratio in the tool setting AND the prompt: `vertical 9:16`.
- Leave negative space where on-screen text or captions will go (usually the top third).

## Universal video prompt order

`[what moves] + [how it moves] + [camera move] + [pace/mood] + [what stays still]`

- One action per clip. Never a sequence of actions.
- Describe motion, not the picture — the start frame already shows the picture.
- Name the camera move explicitly: `slow push-in`, `handheld follow`, `orbit left`, `static locked-off`, `crash zoom`, `whip pan`.
- Say what must NOT change: `face and outfit stay identical`, `background static`.
- Keep most clips 3–6 seconds. Short clips cut faster and hide drift.

## Per-tool habits

**Nano Banana (Gemini image)** — strongest for editing and keeping one character across frames. Upload the character sheet as reference and say `same character as reference image, same face, same outfit`. Good at in-image text when it is short and quoted.

**Higgsfield** — a hub for many image and video models plus camera-move presets. Use its character/reference features (e.g. Soul ID) for a recurring face, pick a camera preset instead of describing complex moves, and keep prompts short — presets do the heavy lifting.

**Kling** — reliable image-to-video with good physics. Supports start (and on some versions end) frames — use an end frame for transformations and loops. Describe one clear motion; add `smooth, natural motion` for people, `exaggerated cartoon motion` for 2D styles.

**Veo** — strong realism and native sound. Add a `Sound:` line (ambience, SFX, short dialogue in quotes). Keep dialogue under ~8 words per clip so lip-sync holds.

**Seedance** — good multi-shot and reference handling. You can describe 2–3 short shots in one prompt with `Shot 1: … Shot 2: …` and attach character references. Some versions restrict realistic human faces — use stylized characters if blocked.

**Runway / Hailuo / Wan / others** — follow the universal order; keep prompts under ~60 words.

## Consistency kit (use for any recurring character)

1. Generate a **character sheet**: front, 3/4, side, back, face close-up, on plain background.
2. Write a **locked descriptor** (35–60 words): age range, build, face shape, hair, eyes, skin, outfit with colors, one signature accessory, art style.
3. Reuse the same seed/reference and the same descriptor in every frame.
4. Lock lighting and palette per episode in one **style line** and paste it into every frame.

## Vertical video basics

- 9:16, subject centered in the middle 60% (UI covers the edges and bottom).
- First frame must be readable as a thumbnail with sound off.
- Burn in captions; most viewers watch muted.
- Label AI-generated content where the platform requires it.
