#!/usr/bin/env python3
"""Create responsive homepage images without changing any native originals.

Requires Pillow, as do the repository's existing image build scripts.
Run after changing Decks, Ingest, or Valet Notes homepage captures.
"""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import json
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'


class ImageTag(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.attrs = dict(attrs)


def build(source):
    digest = sha256(source.read_bytes()).hexdigest()[:10]
    image = Image.open(source)
    width, height = image.size
    widths = sorted({min(width, w) for w in (480, 960, 1600, 2400)})
    output = source.parent / 'responsive'
    output.mkdir(exist_ok=True)
    variants = []
    for w in widths:
        target = output / f'{source.stem}-{digest}-{w}.webp'
        if not target.exists():
            resized = image.resize((w, round(height * w / width)), Image.Resampling.LANCZOS)
            resized.save(target, 'WEBP', quality=90, method=6)
        variants.append((w, target))
    return variants


def main():
    for slug in ('decks', 'ingest', 'valetnotes'):
        page = SITE / slug / 'index.html'
        html = page.read_text()
        tags = []
        for match in re.finditer(r'<img\b[^>]*>', html):
            parser = ImageTag(); parser.feed(match.group())
            attrs = parser.attrs
            src = attrs.get('data-display-source', attrs.get('src', ''))
            if not src or src.startswith(('http:', 'https:', 'data:')):
                continue
            source = SITE / src.lstrip('/') if src.startswith('/') else page.parent / src
            source = source.resolve()
            if int(attrs.get('width', 0)) <= 128 or not source.is_file():
                continue
            tags.append((match.group(), attrs, src, source))
        sources = sorted({tag[3] for tag in tags})
        with ThreadPoolExecutor(max_workers=4) as executor:
            images = dict(zip(sources, executor.map(build, sources)))
        for original, attrs, src, source in tags:
            variants = images[source]
            urls = [(w, '/' + target.relative_to(SITE).as_posix()) for w, target in variants]
            attrs['data-display-source'] = src
            attrs['src'] = next((url for w, url in urls if w >= 960), urls[-1][1])
            attrs['srcset'] = ', '.join(f'{url} {w}w' for w, url in urls)
            width, height = int(attrs['width']), int(attrs['height'])
            display = 320 if height > width * 1.6 else 450 if height > width * 1.1 else 1200
            if 'hero-macbook' in source.name: display = 740
            if 'framed-mac-home' in source.name or 'framed-mac-drawer' in source.name: display = 680
            attrs['sizes'] = f'(max-width: 650px) min(calc(100vw - 40px), {display}px), {display}px'
            attrs['decoding'] = 'async'
            replacement = '<img ' + ' '.join(f'{key}="{escape(value or "", quote=True)}"' for key, value in attrs.items()) + '>'
            html = html.replace(original, replacement)
        page.write_text(html)
        original_bytes = sum(p.stat().st_size for p in sources)
        fallback_bytes = sum(next((p for w, p in variants if w >= 960), variants[-1][1]).stat().st_size for variants in images.values())
        report = {'original_bytes': original_bytes, 'fallback_bytes': fallback_bytes, 'distinct_images': len(images), 'quality': 90,
                  'images': {str(p.relative_to(SITE)): [str(v.relative_to(SITE)) for _, v in variants] for p, variants in images.items()}}
        (SITE / slug / 'assets/responsive/manifest.json').write_text(json.dumps(report, indent=2)+'\n')
        print(f'{slug}: {len(images)} images; originals {original_bytes/1048576:.1f} MiB; 960px fallback set {fallback_bytes/1048576:.1f} MiB (not a network measurement)')


if __name__ == '__main__':
    main()
