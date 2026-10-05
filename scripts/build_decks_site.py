#!/usr/bin/env python3
"""Build the standalone Decks website from its portfolio source pages."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site/decks"
OUTPUT = ROOT / "dist/decks"
ORIGIN = "https://decksphotoapp.com"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.refs = []
        self.canonical = []
        self.ids = set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical.append(attrs.get("href"))
        for attr in ("href", "src", "poster"):
            if attrs.get(attr):
                self.refs.append(attrs[attr])


def main():
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(SOURCE, OUTPUT)
    for name in ("apps.css", "family.css"):
        shutil.copy2(ROOT / "site/assets" / name, OUTPUT / "assets" / name)
    for path in OUTPUT.rglob("*.html"):
        text = path.read_text()
        # The portfolio home link stays external when Decks lives at the root.
        text = text.replace('href="/"', 'href="https://brianrenshaw.app/"')
        text = text.replace("https://brianrenshaw.app/decks/", ORIGIN + "/")
        text = text.replace('href="/ingest/', 'href="https://ingestphotoapp.com/')
        text = text.replace('"/decks/', '"/')
        path.write_text(text)
    routes = sorted("/" + p.relative_to(OUTPUT).as_posix().removesuffix("index.html")
                    for p in OUTPUT.rglob("index.html"))
    (OUTPUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{ORIGIN}{route}</loc></url>\n" for route in routes) +
        "</urlset>\n")
    (OUTPUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n")
    (OUTPUT / "_redirects").write_text("/decks / 301\n/decks/ / 301\n/decks/* /:splat 301\n")
    pages = {path: Page(path.read_text()) for path in OUTPUT.rglob("*.html")}
    errors = []
    for path, page in pages.items():
        route = "/" + path.relative_to(OUTPUT).as_posix()
        url = ORIGIN + route
        if page.canonical != [url.removesuffix("index.html")]:
            errors.append(f"{route}: incorrect canonical URL")
        if "brianrenshaw.app/decks/" in path.read_text() or '"/decks/' in path.read_text():
            errors.append(f"{route}: portfolio Decks URL remains")
        for ref in page.refs:
            target = urlsplit(urljoin(url, ref))
            if target.netloc != "decksphotoapp.com":
                continue
            local = OUTPUT / unquote(target.path).lstrip("/")
            if target.path.endswith("/") or local.is_dir():
                local /= "index.html"
            if not local.is_file():
                errors.append(f"{route}: missing {ref}")
            elif target.fragment and local in pages and unquote(target.fragment) not in pages[local].ids:
                errors.append(f"{route}: missing fragment {ref}")
    if errors:
        sys.exit("\n".join(errors))
    print(f"PASS: built and checked {len(pages)} Decks pages in {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
