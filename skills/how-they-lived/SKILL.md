---
name: how-they-lived
description: Use when making a short AI history video about everyday life in a past era or culture — "How people lived in…", "A day of a Roman soldier", "What a medieval peasant ate" — faceless, narrated, built from AI images or clips. Produces researched beats, voiceover script, storyboard frame prompts, then video prompts and captions.
---

# How They Lived (Everyday History)

Daily-life history — food, sleep, hygiene, work, money — beats battles for retention because viewers compare it to their own life.

## Ask (max 2 questions)
- Era/culture and one angle (food, hygiene, sleep, work, kids, money)? — default: one surprising angle.
- Voiceover language and length? — default: English, 45–60 s.

## Accuracy rules
- Only state facts you're confident are widely accepted. Mark uncertain ones as "historians think…".
- Avoid stereotypes; show ordinary people with dignity.
- Name one source type in the caption ("based on Roman household records") only if true.

## Structure (45–60 s, 10–12 clips, ~140 words VO)
| Time | Beat |
|---|---|
| 0–3 s | **Hook fact** — the most surprising detail, shown |
| 3–10 s | **Setting** — who, where, when, one establishing shot |
| 10–40 s | **4 daily moments** — morning → work → food → night, one clip each, one fact each |
| 40–52 s | **Twist** — the thing modern people get wrong |
| 52–60 s | **Comparison + CTA** — "Would you survive it?" |

## Hook formulas
- "In [era], people [shocking normal habit]."
- "You wouldn't last a day as a [role] in [era]. Here's why."
- "This is what [role] ate for breakfast in [year]."

## Workflow
1. **Concept** — angle, hook, 5–6 facts, VO script with clip markers. Wait for approval.
2. **Frame prompts** — one per VO line, consistent period palette. Wait for approval.
3. **Video prompts** — subtle motion (steam, fire flicker, slow push-in) suits documentary pace.
4. **Packaging** — captions, title, hashtags, music mood.
Use `references/models.md` for tool-specific tweaks.

## Frame prompt template
```
Vertical 9:16, [shot type] of [ordinary person: age, role, period-accurate clothing], [daily action], inside [period-accurate place with 2 material details], [light source of the era: oil lamp/candle/daylight through shutters], documentary realism, muted earthy palette, film grain
```

## Video prompt template
```
[Small action: hands kneading dough / breath in cold air], [ambient motion: smoke, flicker, dust], camera slow push-in, calm documentary pace, faces stable
```

## Packaging
- Burn-in captions word-by-word synced to VO.
- Title: "How [role] lived in [era]".
- Hashtags: #history #howtheylived #historyfacts #[era] #aihistory

## Common mistakes
- Modern objects sneaking into frames (glass windows, zippers) — add "no modern objects".
- Too many facts — one per clip.
- Epic battle music on a domestic story; use soft period-flavored ambient.

## Example — "Roman apartment dwellers"
VO 1: "Most Romans didn't have kitchens."
**Frame:** `Vertical 9:16, medium shot of a Roman man, 30s, short tunic, carrying a clay bowl down a crowded street toward a thermopolium counter with sunken jars, morning light, documentary realism, muted palette`
**Video:** `Man walks toward the food counter, steam rises from the jars, camera handheld follow, busy street extras move softly, face stable`
