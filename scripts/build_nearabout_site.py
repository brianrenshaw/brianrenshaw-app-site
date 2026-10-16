#!/usr/bin/env python3
"""Build and validate Nearabout's standalone Cloudflare Pages site."""
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import re
import shutil
import sys
from build_decks_site import Page

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'site/nearabout'
OUTPUT = ROOT / 'dist/nearabout'
ORIGIN = 'https://nearaboutapp.com'


def main():
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(SOURCE, OUTPUT)
    for path in OUTPUT.rglob('*.html'):
        text = path.read_text().replace('https://brianrenshaw.app/nearabout/', ORIGIN + '/')
        path.write_text(text.replace('/nearabout/', '/'))
    pages = {p: Page(p.read_text()) for p in OUTPUT.rglob('*.html')}
    errors = []
    for path, page in pages.items():
        route = '/' + path.relative_to(OUTPUT).as_posix().removesuffix('index.html')
        if page.canonical != [ORIGIN + route]:
            errors.append(f'{route}: incorrect canonical')
        for ref in page.refs:
            target = urlsplit(urljoin(ORIGIN + route, ref))
            if target.netloc != 'nearaboutapp.com':
                continue
            local = OUTPUT / unquote(target.path).lstrip('/')
            if target.path.endswith('/') or local.is_dir():
                local /= 'index.html'
            if not local.is_file():
                errors.append(f'{route}: missing {ref}')
            elif target.fragment and local in pages and unquote(target.fragment) not in pages[local].ids:
                errors.append(f'{route}: missing fragment {ref}')
    for css in OUTPUT.rglob('*.css'):
        for ref in re.findall(r'url\([\'"]?([^\)\'\"]+)', css.read_text()):
            if not (css.parent / ref).is_file():
                errors.append(f'{css.name}: missing {ref}')
    routes = sorted('/' + p.relative_to(OUTPUT).as_posix().removesuffix('index.html') for p in pages)
    (OUTPUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{ORIGIN}{r}</loc></url>\n' for r in routes) + '</urlset>\n')
    (OUTPUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')
    (OUTPUT / '_redirects').write_text('/nearabout / 301\n/nearabout/ / 301\n/nearabout/* /:splat 301\n')
    (OUTPUT / '_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n')
    if errors:
        sys.exit('\n'.join(errors))
    print(f'PASS: built {len(pages)} Nearabout pages; routes, assets, fonts, fragments, and canonical URLs verified')


if __name__ == '__main__':
    main()
