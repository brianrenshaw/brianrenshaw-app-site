#!/usr/bin/env python3
"""Build and validate Ingest's standalone Cloudflare Pages website."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import json
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'site/ingest'
OUTPUT = ROOT / 'dist/ingest'
ORIGIN = 'https://ingestphotoapp.com'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.refs, self.canonical, self.ids = [], [], set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs.get('href'))
        for attr in ('href', 'src', 'poster'):
            if attrs.get(attr):
                self.refs.append(attrs[attr])
        if tag == 'meta' and attrs.get('property') in ('og:image', 'og:url'):
            self.refs.append(attrs['content'])


def main():
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(SOURCE, OUTPUT)
    for name in ('apps.css', 'family.css'):
        shutil.copy2(ROOT / 'site/assets' / name, OUTPUT / 'assets' / name)
    for path in OUTPUT.rglob('*'):
        if path.suffix not in ('.html', '.js', '.json', '.css'):
            continue
        text = path.read_text()
        if path.suffix == '.html':
            text = text.replace('href="/"', 'href="https://brianrenshaw.app/"')
        text = text.replace('https://brianrenshaw.app/ingest/', ORIGIN + '/')
        text = text.replace('/ingest/', '/')
        path.write_text(text)
    routes = sorted('/' + p.relative_to(OUTPUT).as_posix().removesuffix('index.html')
                    for p in OUTPUT.rglob('index.html') if p.parent.name != 'quick-start')
    (OUTPUT / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        ''.join(f'  <url><loc>{ORIGIN}{route}</loc></url>\n' for route in routes) +
        '</urlset>\n')
    (OUTPUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')
    (OUTPUT / '_redirects').write_text(
        '/ingest / 301\n/ingest/ / 301\n/ingest/* /:splat 301\n'
        '/quick-start /getting-started/ 301\n/quick-start/ /getting-started/ 301\n')
    # A real 404 prevents Pages' SPA fallback from serving the homepage for typos.
    (OUTPUT / '404.html').write_text('''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found — Ingest</title><meta name="robots" content="noindex">
<link rel="stylesheet" href="/assets/apps.css"><link rel="stylesheet" href="/assets/family.css">
<link rel="stylesheet" href="/assets/site.css"></head><body class="app-ingest ingest-docs">
<main class="family-document"><h1>Page not found.</h1><p><a href="/">Return to Ingest</a>
 or <a href="/guide/">open the guide</a>.</p></main></body></html>\n''')
    pages = {p: Page(p.read_text()) for p in OUTPUT.rglob('*.html')}
    errors = []

    def check_ref(ref, url):
        target = urlsplit(urljoin(url, ref))
        if target.netloc != 'ingestphotoapp.com':
            return
        local = OUTPUT / unquote(target.path).lstrip('/')
        if target.path.endswith('/') or local.is_dir():
            local /= 'index.html'
        if not local.is_file():
            errors.append(f'{url}: missing {ref}')
        elif target.fragment and local in pages and unquote(target.fragment) not in pages[local].ids:
            errors.append(f'{url}: missing fragment {ref}')

    for path, page in pages.items():
        url = ORIGIN + '/' + path.relative_to(OUTPUT).as_posix()
        if path.name != '404.html' and page.canonical != [url.removesuffix('index.html')]:
            errors.append(f'{url}: incorrect canonical URL')
        if '/ingest/' in path.read_text():
            errors.append(f'{url}: old Ingest route remains')
        for ref in page.refs:
            check_ref(ref, url)
        if path.name == 'index.html':
            source = SOURCE / path.relative_to(OUTPUT)
            if not Page(source.read_text()).ids <= page.ids:
                errors.append(f'{url}: source anchor removed')
    for item in json.loads((OUTPUT / 'assets/search-index.json').read_text()):
        check_ref(item['url'], ORIGIN + '/')
    for path in OUTPUT.rglob('*.css'):
        for ref in re.findall(r'url\([\'"]?([^\)\'"]+)', path.read_text()):
            if not ref.startswith('data:'):
                check_ref(ref, ORIGIN + '/' + path.relative_to(OUTPUT).as_posix())
    for path in OUTPUT.rglob('*'):
        if path.is_file() and path.stat().st_size > 25 * 1024 * 1024:
            errors.append(f'{path}: exceeds Cloudflare Pages 25 MiB asset limit')
    if (OUTPUT / 'appcast.xml').read_bytes() != (SOURCE / 'appcast.xml').read_bytes():
        errors.append('Sparkle feed changed')
    if errors:
        sys.exit('\n'.join(errors))
    print(f'PASS: built {len(pages)} Ingest pages; routes, anchors, search, assets, feed, and Pages size limits')


if __name__ == '__main__':
    main()
