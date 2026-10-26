# Contributing a format

A good format is a **repeatable structure** that already works on short-form platforms — not a single video idea.

## Checklist

1. Create `skills/<format-name>/SKILL.md` (kebab-case name).
2. Frontmatter:
   ```yaml
   ---
   name: <format-name>
   description: Use when making … (say what the format is and give 2–3 example titles, so agents know when to trigger it)
   ---
   ```
3. Follow the section order used by every skill:
   - one-line pitch + why it works
   - **Ask** (max 2 questions, with defaults)
   - **Structure** — timed beat table
   - **Hook formulas**
   - **Workflow** — concept → frame prompts → video prompts → packaging, with approval after concept and frames
   - **Frame prompt template**
   - **Video prompt template**
   - **Packaging** — on-screen text, caption, hashtags
   - **Common mistakes**
   - **Example** — at least one frame prompt + its video prompt
4. Add the format to the table in `README.md` and the list in `skills/format-picker/SKILL.md`.
5. Run `python3 scripts/build.py` to refresh `references/` and the zips in `dist/`.

## Rules every format must follow

- Frames first, then video.
- No impersonation of real people, no fake testimonials or reviews, no real-child imagery.
- No copyrighted characters, lyrics or brand assets the user doesn't own.
- Facts in educational formats must be accurate or clearly labeled as speculation.

## Gallery submissions

Open an issue titled `Gallery: <format-name>` with a link to your video. Tell us which models you used.
