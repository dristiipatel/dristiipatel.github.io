#!/usr/bin/env python3
"""Build the Field Notes pages from Markdown files.

Usage (from the root of the dristiipatel.github.io repository):
    python3 build_notes.py

Reads   notes_src/*.md      (files starting with "_" are ignored)
Writes  notes/index.html    (list of posts)
        notes/<slug>/index.html
        notes/img/*         (copied from notes_src/img)

The notes/ folder is regenerated on every run, so never edit it by hand.
"""
import html
import re
import shutil
import sys
from datetime import date
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("Missing dependency. Run:  pip install markdown")

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "notes_src"
OUT = ROOT / "notes"

SITE_TITLE = "Field Notes in Physics"
TAGLINE = "Questions, calculations and sketches from learning neutrino physics."
AUTHOR = "Dristii Patel"
HOME_URL = "/"
NOTES_URL = "/notes/"

# Shown at the top of both Notes list pages, above the tabs.
INTRO = """<p>Hi, I'm Dristii. I'm a third-year physics student at IISc in Bengaluru, and this is where I write about my work: mostly neutrino physics, plus whatever else I get curious about.</p>
<p>I am still learning, so errors will happen. If something looks wrong, email me at <a href="mailto:dristiip@iisc.ac.in">dristiip@iisc.ac.in</a>. Corrections go into the post with a dated note, so the history stays visible.</p>
<p>Thanks for reading.</p>"""

# Each post goes in one section, set with "section:" in its front matter.
# Posts without that line go in "technical". The first section is the
# default tab at /notes/; the others get their own page at /notes/<path>/.
SECTIONS = [
    {"key": "general", "label": "For everyone", "path": "",
     "blurb": "Short explanations for anyone curious about the physics."},
    {"key": "technical", "label": "In depth", "path": "in-depth",
     "blurb": "Derivations, numerical checks and notes from research code."},
]
DEFAULT_SECTION = "technical"

MATHJAX = """<script>window.MathJax={tex:{inlineMath:[['$','$']],displayMath:[['$$','$$']]}};</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>"""

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=DM+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">"""

FAVICON = """<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%231d6b68'/%3E%3Ctext x='16' y='22' font-size='18' font-family='Georgia,serif' text-anchor='middle' fill='%23fff'%3ED%3C/text%3E%3C/svg%3E">"""

# The style lives in assets/reading.css and is shared with the research page.
PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="{og_type}">
{favicon}
{fonts}
<link rel="stylesheet" href="/assets/reading.css">
<script src="/assets/theme.js"></script>
{extra_head}
</head>
<body>
<div class="wrap">
<header class="top">
<a class="who" href="{home}">{author}</a>
<a href="/#research">Research</a>
<a href="{notes}" aria-current="page">Notes</a>
<a href="/Dristii_Patel_CV.pdf">CV</a>
<button id="theme" type="button" aria-label="Switch between light and dark theme">&#9680;</button>
</header>
{body}
<footer>{site_title} &middot; {author} &middot; <a href="/">Home</a> &middot; <a href="mailto:dristiip@iisc.ac.in">Email</a></footer>
</div>
</body>
</html>
"""

# Fenced code and inline code are matched first so that dollar signs inside
# them are left alone. Group 2 is a math expression.
TOKEN = re.compile(
    r"(```.*?```|`[^`\n]+`)|(\$\$.+?\$\$|(?<![\\$])\$(?![\s$])[^$\n]+?(?<!\s)\$)",
    re.S,
)


def protect_math(text):
    store = []

    def sub(m):
        if m.group(1):
            return m.group(0)
        store.append(m.group(2))
        return f"@@MATH{len(store) - 1}@@"

    return TOKEN.sub(sub, text), store


def restore_math(rendered, store):
    for i, expr in enumerate(store):
        rendered = rendered.replace(f"@@MATH{i}@@", html.escape(expr, quote=False))
    return rendered


def parse_post(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError(f"{path.name}: missing front matter block between --- lines")
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"').strip("'")
    for required in ("title", "date"):
        if required not in meta:
            raise ValueError(f"{path.name}: front matter needs '{required}'")
    meta["date"] = date.fromisoformat(meta["date"])
    meta["draft"] = meta.get("draft", "false").lower() == "true"
    meta["tags"] = [t.strip() for t in meta.get("tags", "").strip("[]").split(",") if t.strip()]
    meta["slug"] = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
    meta["section"] = meta.get("section", DEFAULT_SECTION)
    keys = [s["key"] for s in SECTIONS]
    if meta["section"] not in keys:
        raise ValueError(f"{path.name}: section must be one of {keys}")
    return meta, m.group(2)


def section_url(key):
    s = next(s for s in SECTIONS if s["key"] == key)
    return NOTES_URL + (s["path"] + "/" if s["path"] else "")


def render_body(md_text):
    protected, store = protect_math(md_text)
    rendered = markdown.markdown(
        protected,
        extensions=["fenced_code", "tables", "footnotes", "sane_lists"],
    )
    rendered = restore_math(rendered, store)
    # Turn a lone image paragraph into <figure> with the alt text as caption.
    rendered = re.sub(
        r'<p><img alt="([^"]*)" src="([^"]+)" ?/?></p>',
        r'<figure><img src="\2" alt="\1"><figcaption>\1</figcaption></figure>',
        rendered,
    )
    return rendered, bool(store)


def fmt_date(d):
    return f"{d.day} {d.strftime('%B %Y')}"


def build():
    if not SRC.is_dir():
        sys.exit("notes_src/ not found. Run this script from the repository root.")

    posts = []
    for path in sorted(SRC.glob("*.md")):
        if path.name.startswith("_"):
            continue
        meta, body = parse_post(path)
        if meta["draft"]:
            print(f"  skipped draft: {path.name}")
            continue
        meta["html"], meta["has_math"] = render_body(body)
        meta["words"] = len(re.findall(r"\w+", body))
        posts.append(meta)
    posts.sort(key=lambda p: p["date"], reverse=True)

    reserved = {s["path"] for s in SECTIONS if s["path"]} | {"img"}
    for p in posts:
        if p["slug"] in reserved:
            sys.exit(f"Post slug '{p['slug']}' clashes with a section page. Rename the file.")
    seen = set()
    for p in posts:
        if p["slug"] in seen:
            sys.exit(f"Two posts share the slug '{p['slug']}'. Rename one of the files.")
        seen.add(p["slug"])

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    if (SRC / "img").is_dir():
        shutil.copytree(SRC / "img", OUT / "img")

    for p in posts:
        minutes = max(1, round(p["words"] / 200))
        chips = ""
        if p["tags"]:
            chips = "<span class='chips'>" + "".join(
                f"<span class='chip'>{html.escape(t)}</span>" for t in p["tags"]) + "</span>"
        # Older / newer post in the same tab, so a reader can keep going.
        same = [q for q in posts if q["section"] == p["section"]]
        i = same.index(p)
        older = same[i + 1] if i + 1 < len(same) else None
        newer = same[i - 1] if i > 0 else None
        pager = "<nav class='pager' aria-label='More notes'>"
        if older:
            pager += (f"<a class='prev' href='{NOTES_URL}{older['slug']}/'>"
                      f"<small>&larr; Earlier</small>{html.escape(older['title'])}</a>")
        if newer:
            pager += (f"<a class='next' href='{NOTES_URL}{newer['slug']}/'>"
                      f"<small>Later &rarr;</small>{html.escape(newer['title'])}</a>")
        pager += "</nav>"
        fixes = ("<p class='fixes'>If something here looks wrong, please email me at "
                 "<a href='mailto:dristiip@iisc.ac.in'>dristiip@iisc.ac.in</a>. "
                 "Corrections go into the post with a dated note.</p>")
        body = (
            f"<article><h1>{html.escape(p['title'])}</h1>"
            f"<p class='meta'>{fmt_date(p['date'])} &middot; {minutes} min read{chips}</p>"
            f"{p['html']}{fixes}</article>{pager}"
        )
        desc = html.escape(p.get("summary", TAGLINE))
        page = PAGE.format(
            title=f"{html.escape(p['title'])} | {SITE_TITLE}",
            og_title=html.escape(p["title"]), og_type="article",
            description=desc, favicon=FAVICON, fonts=FONTS,
            extra_head=MATHJAX,
            home=HOME_URL, notes=section_url(p["section"]), author=AUTHOR,
            body=body, site_title=SITE_TITLE,
        )
        folder = OUT / p["slug"]
        folder.mkdir()
        (folder / "index.html").write_text(page, encoding="utf-8")
        print(f"  built: notes/{p['slug']}/")

    for sec in SECTIONS:
        tabs = "".join(
            f"<a href='{section_url(s['key'])}'"
            + (" aria-current='page'" if s is sec else "")
            + f">{html.escape(s['label'])}</a>"
            for s in SECTIONS
        )
        entries = "".join(
            f"<div class='entry'><h2><a href='{NOTES_URL}{p['slug']}/'>{html.escape(p['title'])}</a></h2>"
            f"<p class='meta'>{fmt_date(p['date'])}"
            + ("<span class='chips'>" + "".join(f"<span class='chip'>{html.escape(t)}</span>" for t in p["tags"]) + "</span>" if p["tags"] else "")
            + f"</p><p>{html.escape(p.get('summary', ''))}</p></div>"
            for p in posts if p["section"] == sec["key"]
        ) or "<p>No posts yet.</p>"
        body = (
            f"<h1>{SITE_TITLE}</h1><div class='intro'>{INTRO}</div>"
            f"<nav class='tabs' aria-label='Sections'>{tabs}</nav>"
            f"<p class='blurb'>{html.escape(sec['blurb'])}</p>{entries}"
        )
        title = SITE_TITLE if not sec["path"] else f"{sec['label']} | {SITE_TITLE}"
        index = PAGE.format(
            title=title, og_title=title, og_type="website",
            description=TAGLINE, favicon=FAVICON, fonts=FONTS, extra_head="",
            home=HOME_URL, notes=NOTES_URL, author=AUTHOR,
            body=body, site_title=SITE_TITLE,
        )
        folder = OUT / sec["path"] if sec["path"] else OUT
        folder.mkdir(exist_ok=True)
        (folder / "index.html").write_text(index, encoding="utf-8")
        n = sum(p["section"] == sec["key"] for p in posts)
        print(f"  list: {section_url(sec['key'])} ({sec['label']}, {n} post(s))")
    print(f"Done: {len(posts)} post(s) in notes/")


if __name__ == "__main__":
    build()
