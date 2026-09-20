#!/usr/bin/env python3
"""Reject undersized/lossy Ingest captures and missing display-size limits."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import struct

ROOT = Path(__file__).resolve().parents[1] / 'site'
ASSETS = ROOT / 'ingest/assets'
manifest = json.loads((ASSETS / 'screenshots.json').read_text())['images']
errors = []
seen = set()


def lossless_dimensions(path):
    data = path.read_bytes()
    assert data[:4] == b'RIFF' and data[8:12] == b'WEBP', 'not WebP'
    offset = 12
    while offset + 8 <= len(data):
        kind = data[offset:offset + 4]
        size = struct.unpack_from('<I', data, offset + 4)[0]
        payload = data[offset + 8:offset + 8 + size]
        assert kind != b'VP8 ', 'lossy encoding'
        if kind == b'VP8L':
            assert payload[0] == 0x2f, 'invalid lossless header'
            bits = int.from_bytes(payload[1:5], 'little')
            return (bits & 0x3fff) + 1, ((bits >> 14) & 0x3fff) + 1
        offset += 8 + size + size % 2
    raise AssertionError('missing lossless image')


for name, meta in manifest.items():
    try:
        size = lossless_dimensions(ASSETS / name)
        assert size == (meta['width'], meta['height']), 'dimensions differ from manifest'
        assert size == (2 * meta['displayWidth'], 2 * meta['displayHeight']), 'capture must be native 2x'
        for alias in [name.replace('-retina', ''), name.replace('-0.2.1-retina', '')]:
            path = ASSETS / alias
            if path.exists():
                assert path.read_bytes() == (ASSETS / name).read_bytes(), f'stale alias {alias}'
    except (AssertionError, OSError) as error:
        errors.append(f'{name}: {error}')


class Images(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        src = attrs.get('src', '')
        if tag != 'img' or not src.startswith('/ingest/assets/') or not src.endswith('.webp'):
            return
        name = src.rsplit('/', 1)[-1]
        if name not in manifest:
            errors.append(f'{page}: untracked or stale screenshot {name}')
            return
        seen.add(name)
        meta = manifest[name]
        if (attrs.get('width'), attrs.get('height')) != (str(meta['width']), str(meta['height'])):
            errors.append(f'{page}: incorrect intrinsic dimensions for {name}')
        if attrs.get('style') != f'--capture-width:{meta["displayWidth"]}px':
            errors.append(f'{page}: missing native display-size limit for {name}')


for page in ROOT.rglob('*.html'):
    Images().feed(page.read_text())
for name in manifest.keys() - seen:
    errors.append(f'{name}: capture is unused')
css = (ASSETS / 'site.css').read_text()
if 'max-width:var(--capture-width,100%)' not in css:
    errors.append('Missing screenshot display-size cap')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(manifest)} lossless Retina captures, aliases, HTML dimensions, and display-size limits.')
