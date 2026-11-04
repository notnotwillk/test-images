#!/usr/bin/env python3
"""Renders the knowledge base's Markdown into the pages nginx serves.

Runs when the image is built (mkosi.postinst.chroot), and exits non-zero on a
missing page or a dead link, so a broken knowledge base fails the build. Each
source is copied beside its page. Links between pages are written as NAME.md, so
they also work on GitHub, and become NAME.html here.
"""
import html
import re
import shutil
import sys
from pathlib import Path

import markdown

# Every page, in the order the navigation shows them.
PAGES = {
    "index": "Home",
    "getting-started": "Getting started",
    "image-recipes": "Image recipes",
    "runners": "Runners",
    "volumes": "Volumes",
    "exposures": "Exposures",
    "troubleshooting": "Troubleshooting",
}

TEMPLATE = """<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{title} - Buzz Herd knowledge base</title>
<style>
body {{ font: 1rem/1.6 system-ui, sans-serif; margin: 0 auto; max-width: 48rem; padding: 1rem; }}
nav {{ border-bottom: 1px solid #8884; display: flex; flex-wrap: wrap; gap: .25rem 1rem; padding-bottom: .75rem; }}
nav [aria-current] {{ font-weight: 700; }}
h1 {{ line-height: 1.2; }}
pre {{ background: #8882; overflow-x: auto; padding: .75rem; }}
code {{ font: .9em ui-monospace, monospace; overflow-wrap: anywhere; }}
pre code {{ overflow-wrap: normal; }}
table {{ border-collapse: collapse; display: block; overflow-x: auto; }}
th, td {{ border: 1px solid #8884; padding: .35rem .6rem; text-align: left; vertical-align: top; }}
</style>
<nav>{nav}</nav>
<main>
{body}
</main>
</html>
"""


def fail(message):
    sys.exit(f"knowledge base: {message}")


def navigation(current):
    links = []
    for name, label in PAGES.items():
        here = ' aria-current="page"' if name == current else ""
        links.append(f'<a href="{name}.html"{here}>{html.escape(label)}</a>')
    return "".join(links)


def render(source, output):
    found = {path.stem for path in source.glob("*.md")}
    if found != set(PAGES):
        fail(f"the pages don't match PAGES: {sorted(found ^ set(PAGES))}")

    bodies = {}
    anchors = {}
    for name in PAGES:
        convert = markdown.Markdown(extensions=["tables", "fenced_code", "toc"])
        bodies[name] = convert.convert((source / f"{name}.md").read_text(encoding="utf-8"))
        anchors[name] = set(re.findall(r'\sid="([^"]+)"', bodies[name]))
        if not bodies[name].startswith("<h1"):
            fail(f"{name}.md must start with a level 1 heading")

    def relink(name):
        def replace(match):
            target = match.group(1)
            if re.match(r"[a-z][a-z0-9+.-]*:", target):
                return match.group(0)
            page, _, fragment = target.partition("#")
            page = page.removesuffix(".md") if page.endswith(".md") else None if page else name
            if page not in PAGES:
                fail(f"{name}.md links to {target}, which isn't a page")
            if fragment and fragment not in anchors[page]:
                fail(f"{name}.md links to {target}, which isn't a heading")
            return f'href="{page}.html{"#" + fragment if fragment else ""}"'

        return replace

    output.mkdir(parents=True, exist_ok=True)
    for name in PAGES:
        body = re.sub(r'href="([^"]*)"', relink(name), bodies[name])
        title = re.sub(r"<[^>]+>", "", body.split("</h1>", 1)[0])
        page = TEMPLATE.format(title=title, nav=navigation(name), body=body)
        (output / f"{name}.html").write_text(page, encoding="utf-8")
        shutil.copyfile(source / f"{name}.md", output / f"{name}.md")


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    render(
        Path(sys.argv[1]) if len(sys.argv) > 1 else here,
        Path(sys.argv[2]) if len(sys.argv) > 2 else Path("/var/www/knowledge-base"),
    )
