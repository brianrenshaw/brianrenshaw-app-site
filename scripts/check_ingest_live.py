#!/usr/bin/env python3
"""Verify Ingest's Cloudflare deployment, media, redirects, and legacy feed."""
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import json
import subprocess
import sys
from build_ingest_site import main as build_ingest, OUTPUT, ORIGIN, SOURCE


def fetch(url, headers=False):
    args = ['curl', '--silent', '--show-error', '--connect-timeout', '5', '--max-time', '40']
    if headers:
        args += ['--head']
    else:
        args += ['--fail']
    return subprocess.check_output(args + [url])


class Metadata(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.canonical, self.meta, self.ids, self.links = [], {}, set(), []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical.append(a.get('href'))
        if tag == 'meta':
            self.meta[a.get('property', a.get('name'))] = a.get('content')
        if 'id' in a:
            self.ids.add(a['id'])
        if tag == 'a':
            self.links.append(a.get('href', ''))


def redirect(url, destination):
    response = fetch(url, headers=True).decode()
    assert ' 301 ' in response.splitlines()[0], (url, response)
    location = next(line.split(': ', 1)[1].strip() for line in response.splitlines()
                    if line.lower().startswith('location:'))
    assert urljoin(url, location) == destination, (url, location)


def main():
    build_ingest()
    pages = [p for p in OUTPUT.rglob('index.html') if p.parent.name != 'quick-start']

    def page_check(path):
        url = ORIGIN + '/' + path.relative_to(OUTPUT).as_posix().removesuffix('index.html')
        actual = Metadata(fetch(url).decode())
        expected = Metadata(path.read_text())
        # Cloudflare may obfuscate public contact email addresses at the edge.
        # Check page metadata/anchors/first-party navigation independently of that transform.
        assert actual.canonical == expected.canonical == [url], url
        assert actual.meta == expected.meta, url + ': metadata differs'
        assert actual.ids == expected.ids, url + ': anchors differ'
        expected_links = [x for x in expected.links if not x.startswith('mailto:')]
        actual_links = [x for x in actual.links if not x.startswith(('mailto:', '/cdn-cgi/l/email-protection'))]
        assert actual_links == expected_links, url + ': navigation differs'
        return url

    with ThreadPoolExecutor(max_workers=4) as pool:
        for url in pool.map(page_check, pages):
            print('PASS', url, flush=True)
    manifest = json.loads((OUTPUT / 'assets/screenshots.json').read_text())
    share = urlsplit(Metadata((OUTPUT / 'index.html').read_text()).meta['og:image']).path.removeprefix('/assets/')
    assets = list(manifest['images']) + list(manifest['videos']) + [
        share, 'hero-macbook-0.9.8.png', 'docs.css', 'docs.js', 'releases.js', 'hero-tour.js', 'hero-macbook-workflow-0.9.8.webp', 'hero-macbook-focus-0.9.8.webp', 'hero-macbook-details-0.9.8.webp', 'search-index.json', 'command-palette.js', 'overlays.js',
        'landing.js', 'site.css', 'landing.css', 'apps.css', 'family.css', 'icon.png',
        'fonts/ibm-plex-sans.ttf', 'fonts/ia-writer-mono.ttf']

    def asset_check(name):
        assert fetch(ORIGIN + '/assets/' + name) == (OUTPUT / 'assets' / name).read_bytes(), name
        return name

    with ThreadPoolExecutor(max_workers=4) as pool:
        for name in pool.map(asset_check, assets):
            print('PASS asset', name, flush=True)
    for scheme, host in [('http', 'ingestphotoapp.com'), ('http', 'www.ingestphotoapp.com'),
                         ('https', 'www.ingestphotoapp.com')]:
        redirect(f'{scheme}://{host}/support/?test=1', ORIGIN + '/support/?test=1')
    redirect(ORIGIN + '/quick-start/?test=1', ORIGIN + '/getting-started/?test=1')
    redirect(ORIGIN + '/ingest/guide/?test=1', ORIGIN + '/guide/?test=1')
    response = fetch(ORIGIN + '/not-a-real-ingest-route/', headers=True).decode()
    assert ' 404 ' in response.splitlines()[0], response
    for name in ['robots.txt', 'sitemap.xml', 'appcast.xml']:
        assert fetch(ORIGIN + '/' + name) == (OUTPUT / name).read_bytes(), name
    assert fetch('https://brianrenshaw.app/ingest/appcast.xml') == (SOURCE / 'appcast.xml').read_bytes()
    for name in ['hero-wedding-dark-0.9.4.2-retina.webp', 'metadata-assist-demo-0.9.4.2.mp4']:
        assert fetch('https://brianrenshaw.app/ingest/assets/' + name) == (SOURCE / 'assets' / name).read_bytes()
    print('PASS: TLS, pages, media, search, metadata, host/path/query redirects, 404, sitemap, and legacy feed/assets.')


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, subprocess.CalledProcessError) as exc:
        print('NOT READY:', exc)
        sys.exit(1)
