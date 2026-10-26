---
name: micro-drama
description: Use when making an episodic AI micro-drama — 30–90 second soap-opera-style episodes that end on a cliffhanger ("Part 1", "Part 2"), with recurring characters, revenge/romance/betrayal/mystery arcs, built for series binge on Reels, TikTok or Shorts. Produces the series bible, episode beats, character-locked frame prompts, then video prompts with dialogue and captions.
---

# Micro-Drama (Cliffhanger Series)

Short episodes, big emotions, cliffhanger every time. Viewers follow the account to get Part 2 — the best format for growing followers, not just views.

## Ask (max 2 questions)
- Genre (revenge, secret identity, romance, mystery, workplace)? — default: secret identity reveal.
- Spoken dialogue or text-only? — default: short spoken lines (Veo/lip-sync tools) or subtitles if no audio model.

## First, a series bible (once)
- 2–3 characters with **locked descriptors** and a character sheet each.
- One central secret and the episode it is revealed (e.g. Ep 6).
- 2 recurring locations with fixed style lines.

## Episode structure (45–75 s, 8–12 clips)
| Time | Beat |
|---|---|
| 0–3 s | **Recap/slap** — the last cliffhanger or a shocking line |
| 3–20 s | **Setup** — the scene's conflict |
| 20–45 s | **Escalation** — 2 reversals |
| 45–60 s | **Almost-reveal** |
| last 3 s | **Cliffhanger** — freeze on a face reacting, "Part [n+1]" |

## Hook formulas
- "She didn't know the waiter was the billionaire."
- "He laughed at her. Then she opened the envelope."
- "Part 3: the twin finally speaks."

## Workflow
1. **Concept** — bible (first time) + episode beats + dialogue (max 8 words per line). Wait for approval.
2. **Frame prompts** — descriptors verbatim; shot-reverse-shot for dialogue. Wait for approval.
3. **Video prompts** — one line of dialogue or one reaction per clip.
4. **Packaging** — subtitles, "Part N" title card, caption.
See `references/models.md`.

## Frame prompt template
```
Vertical 9:16, [close-up / over-the-shoulder / two-shot] of [CHARACTER A DESCRIPTOR] [emotion + action], [CHARACTER B DESCRIPTOR if present], in [LOCATION STYLE LINE], dramatic soft key light, shallow depth of field, cinematic drama look
```

## Video prompt template
```
[Character] [one action or line], [micro-expression change], camera [slow push-in on face / static two-shot], dramatic tension, same face and outfit. Sound: "[dialogue, max 8 words]", quiet room tone
```

## Packaging
- Title card: "Part [n]" in the first second.
- Caption: "Part [n+1] tomorrow — follow so you don't miss it."
- Hashtags: #minidrama #shortdrama #series #aidrama

## Common mistakes
- Characters drifting between episodes — reuse the same reference images forever.
- Long dialogue lines — lip-sync breaks; cut to reactions.
- Revealing the secret too early — the secret is the follow button.

## Example — Ep 1 "The Cleaner"
**Frame:** `Vertical 9:16, close-up of Mira, late 20s, dark bob haircut, plain grey cleaner's uniform, small silver ring on thumb, looking up from a mop at a man in a suit, glass office lobby at night, cool blue light, cinematic drama`
**Video:** `Mira slowly straightens up, a faint smirk appears, camera slow push-in on her face. Sound: "You don't recognize me, do you?"`
