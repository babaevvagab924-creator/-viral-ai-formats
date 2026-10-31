"""Build a standalone website from the artifact page.

The artifact source (index.html) is written for claude.ai, which adds the
<!doctype>, <head> and <body> itself. This script wraps it into a complete
document with SEO and link-preview tags, ready for GitHub Pages.

Usage: python3 scripts/build_site.py [SITE_URL] [OUT_DIR]
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent.parent
SITE_URL = (sys.argv[1] if len(sys.argv) > 1 else "https://babaevvagab924-creator.github.io/kompromat/").rstrip("/") + "/"
OUT = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "site"

TITLE = "Компромат — итоги года с ИИ без цензуры"
DESC = ("Загрузи экспорт чатов из Claude и получи сторис-карточки: сколько чатов, "
        "сколько слов написал ИИ, твой пиковый час и тип. Бесплатно, всё считается в браузере.")
ICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
        "%3Crect width='64' height='64' rx='14' fill='%2312101a'/%3E"
        "%3Ccircle cx='32' cy='32' r='14' fill='%23ff7a1a'/%3E%3C/svg%3E")

src = (HERE / "index.html").read_text(encoding="utf-8")
body = src[src.index("<link rel=\"preconnect\""):]  # drop artifact-only head lines (charset, viewport, title, meta)

head = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#12101a">
<link rel="icon" href="{ICON}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{SITE_URL}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}img{{max-width:100%}}</style>
</head>
<body>
"""
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "index.html").write_text(head + body + "\n</body>\n</html>\n", encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")
print("built", OUT / "index.html")
