#!/usr/bin/env python3
"""Export the portfolio with redirects for dedicated app domains."""

from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site"
OUTPUT = ROOT / "dist/portfolio"
DECKS = "https://decksphotoapp.com/"
INGEST = "https://ingestphotoapp.com/"


def main():
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(SOURCE, OUTPUT)
    redirects = [("decks", "Decks", route, DECKS + route)
                 for route in ("", "support/", "privacy/")]
    redirects += [("ingest", "Ingest", p.relative_to(SOURCE / "ingest").as_posix().removesuffix("index.html"),
                   INGEST + ("getting-started/" if p.parent.name == "quick-start" else
                             p.relative_to(SOURCE / "ingest").as_posix().removesuffix("index.html")))
                  for p in (SOURCE / "ingest").rglob("index.html")]
    for slug, name, route, destination in redirects:
        (OUTPUT / slug / route / "index.html").write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} has moved</title><link rel="canonical" href="{destination}">
<meta name="robots" content="noindex">
<noscript><meta http-equiv="refresh" content="0;url={destination}"></noscript>
</head><body><h1>{name} has moved</h1>
<p><a id="destination" href="{destination}">Continue to {name}</a></p>
<script>const destination = new URL(document.getElementById('destination').href);
destination.search = location.search; destination.hash = location.hash;
document.getElementById('destination').href = destination.href;
location.replace(destination.href);</script></body></html>
''')
    # Preserve old app assets while links lead directly to the dedicated domains.
    homepage = OUTPUT / "index.html"
    homepage.write_text(homepage.read_text().replace('href="/decks/"', f'href="{DECKS}"').replace('href="/ingest/"', f'href="{INGEST}"'))
    sitemap = OUTPUT / "sitemap.xml"
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    ET.register_namespace("", namespace)
    tree = ET.parse(sitemap)
    for url in list(tree.getroot()):
        loc = url.find(f"{{{namespace}}}loc")
        if loc is not None and (loc.text or "").startswith(("https://brianrenshaw.app/decks/", "https://brianrenshaw.app/ingest/")):
            tree.getroot().remove(url)
    tree.write(sitemap, encoding="UTF-8", xml_declaration=True)
    assert 'href="/decks/"' not in homepage.read_text()
    assert "brianrenshaw.app/decks/" not in sitemap.read_text()
    assert 'href="/ingest/"' not in homepage.read_text()
    assert "brianrenshaw.app/ingest/" not in sitemap.read_text()
    for slug, name, route, destination in redirects:
        text = (OUTPUT / slug / route / "index.html").read_text()
        assert f'rel="canonical" href="{destination}"' in text
        assert "destination.search = location.search" in text
        assert "destination.hash = location.hash" in text
    # Existing installations depend on these exact feeds and routes.
    for feed in ("listing-namer/appcast.xml", "ingest/appcast.xml"):
        assert (OUTPUT / feed).read_bytes() == (SOURCE / feed).read_bytes()
    # Historical media URLs remain byte-for-byte available to external links.
    for asset in (SOURCE / "ingest/assets").rglob("*"):
        if asset.is_file():
            assert (OUTPUT / asset.relative_to(SOURCE)).read_bytes() == asset.read_bytes()
    print("PASS: portfolio export, Decks/Ingest redirects, sitemap, archived assets, and permanent app feeds")


if __name__ == "__main__":
    main()
