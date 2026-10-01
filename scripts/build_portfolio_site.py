#!/usr/bin/env python3
"""Export the portfolio with redirects for Decks's dedicated domain."""

from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site"
OUTPUT = ROOT / "dist/portfolio"
DECKS = "https://decksphotoapp.com/"


def main():
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(SOURCE, OUTPUT)
    for route in ("", "support/", "privacy/"):
        destination = DECKS + route
        (OUTPUT / "decks" / route / "index.html").write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Decks has moved</title><link rel="canonical" href="{destination}">
<meta name="robots" content="noindex">
<noscript><meta http-equiv="refresh" content="0;url={destination}"></noscript>
</head><body><h1>Decks has moved</h1>
<p><a id="destination" href="{destination}">Continue to Decks</a></p>
<script>const destination = new URL(document.getElementById('destination').href);
destination.search = location.search; destination.hash = location.hash;
document.getElementById('destination').href = destination.href;
location.replace(destination.href);</script></body></html>
''')
    # Preserve local app icons, but send portfolio visitors directly to Decks.
    homepage = OUTPUT / "index.html"
    homepage.write_text(homepage.read_text().replace('href="/decks/"', f'href="{DECKS}"'))
    sitemap = OUTPUT / "sitemap.xml"
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)
    tree = ET.parse(sitemap)
    for url in list(tree.getroot()):
        loc = url.find(f"{{{namespace}}}loc")
        if loc is not None and (loc.text or "").startswith("https://brianrenshaw.app/decks/"):
            tree.getroot().remove(url)
    tree.write(sitemap, encoding="UTF-8", xml_declaration=True)
    assert 'href="/decks/"' not in homepage.read_text()
    assert "brianrenshaw.app/decks/" not in sitemap.read_text()
    for route in ("", "support/", "privacy/"):
        text = (OUTPUT / "decks" / route / "index.html").read_text()
        assert f'rel="canonical" href="{DECKS + route}"' in text
        assert "destination.search = location.search" in text
        assert "destination.hash = location.hash" in text
    # Existing installations depend on these exact feeds and routes.
    for feed in ("listing-namer/appcast.xml", "ingest/appcast.xml"):
        assert (OUTPUT / feed).read_bytes() == (SOURCE / feed).read_bytes()
    print("PASS: portfolio export, Decks redirects, sitemap, and permanent app feeds")


if __name__ == "__main__":
    main()
