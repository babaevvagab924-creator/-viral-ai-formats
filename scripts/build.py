#!/usr/bin/env python3
"""Copy shared/models.md into every skill and build upload zips in dist/."""
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
SHARED = ROOT / "shared" / "models.md"
DIST = ROOT / "dist"


def check(skill_dir: Path) -> list[str]:
    errors = []
    md = skill_dir / "SKILL.md"
    if not md.exists():
        return [f"{skill_dir.name}: missing SKILL.md"]
    text = md.read_text(encoding="utf-8")
    m = re.match(r"^---\nname: ([a-z0-9-]+)\ndescription: (.+?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{skill_dir.name}: bad frontmatter")
    else:
        if m.group(1) != skill_dir.name:
            errors.append(f"{skill_dir.name}: name '{m.group(1)}' != folder")
        if len(m.group(2)) > 1024:
            errors.append(f"{skill_dir.name}: description over 1024 chars")
    return errors


def main() -> int:
    skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    errors = [e for d in skill_dirs for e in check(d)]
    if errors:
        print("\n".join(errors))
        return 1

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    all_zip = zipfile.ZipFile(DIST / "viral-ai-formats-all.zip", "w", zipfile.ZIP_DEFLATED)
    for d in skill_dirs:
        refs = d / "references"
        refs.mkdir(exist_ok=True)
        shutil.copy(SHARED, refs / "models.md")
        with zipfile.ZipFile(DIST / f"{d.name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(d.rglob("*")):
                if f.is_file():
                    arc = Path(d.name) / f.relative_to(d)
                    z.write(f, arc)
                    all_zip.write(f, Path("viral-ai-formats") / arc)
    all_zip.close()
    print(f"Built {len(skill_dirs)} skills into {DIST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
