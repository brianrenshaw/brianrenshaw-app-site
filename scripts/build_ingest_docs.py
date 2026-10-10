#!/usr/bin/env python3
"""Generate the static Ingest help center from reviewed HTML article content.

Edit docs/ingest/help-content.json, then run this script. No client framework
or JavaScript is required to read articles or navigate between them.
"""
from pathlib import Path
import html
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site/ingest'
LATEST_DOWNLOAD = ET.parse(SITE / 'appcast.xml').find('./channel/item/enclosure').attrib['url']
DATA = json.loads((ROOT / 'docs/ingest/help-content.json').read_text())
esc = html.escape
mapping = {}
for slug, collection in DATA.items():
    for article in collection['articles']:
        route = f'/ingest/{slug}/{article["id"]}/'
        mapping[f'/ingest/{slug}/#{article["id"]}'] = route
        for anchor in re.findall(r'\bid="([^"]+)"', article['body']):
            mapping[f'/ingest/{slug}/#{anchor}'] = route + '#' + anchor


def rewrite(text, slug):
    text = re.sub(r'href="#([^"]+)"', lambda m: 'href="' + mapping.get(f'/ingest/{slug}/#{m[1]}', f'/ingest/{slug}/#{m[1]}') + '"', text)
    return re.sub(r'/ingest/(guide|support|shortcuts)/#[\w-]+', lambda m: mapping.get(m[0], m[0]), text)


def sidebar(slug, active=None):
    collection = DATA[slug]
    nav = '<a class="wiki-home" href="/ingest/guide/">Ingest help</a><nav aria-label="Help collections" class="wiki-collections"><a class="wiki-start-link" href="/ingest/getting-started/">Start here →</a>'
    for key, item in DATA.items():
        current = ' aria-current="page"' if key == slug and not active else ''
        nav += f'<a href="/ingest/{key}/"{current}>{esc(item["title"])}</a>'
    nav += '<a href="/ingest/templates/">Naming &amp; metadata reference</a><a href="/ingest/automation/">Automation reference</a></nav>'
    nav += '<nav aria-label="Article topics">'
    articles = {a['id']: a for a in collection['articles']}
    for group in collection['groups']:
        opened = ' open' if active in group['ids'] else ''
        nav += f'<details class="wiki-group"{opened}><summary>{esc(group["title"])}</summary>'
        for aid in group['ids']:
            a = articles[aid]
            current = ' aria-current="page"' if aid == active else ''
            nav += f'<a href="/ingest/{slug}/{aid}/"{current}>{esc(a["title"])}</a>'
        nav += '</details>'
    return nav + '</nav>'


def page(slug, title, description, body, active=None, route_override=None):
    route = route_override or f'/ingest/{slug}/' + (active + '/' if active else '')
    # Reuse the existing native site header/footer and scripts.
    template = (ROOT / 'docs/ingest/help-frame.html').read_text()
    meta_description = description or f'{title}: instructions and keyboard context for Ingest, the native Mac photo management app.'
    head = template[:template.index('<body')]
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(title)} — Ingest Help</title>', head)
    head = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda m: m[1] + esc(meta_description, quote=True), head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m[1] + esc(title + ' — Ingest Help'), head)
    head = head.replace('https://brianrenshaw.app/ingest/getting-started/', 'https://brianrenshaw.app' + route)
    head = head.replace('share-0.9.5.png', 'share-editorial-0.9.8.png')
    head = head.replace('</head>', '<link rel="stylesheet" href="/ingest/assets/docs.css?v=wiki-1"><script src="/ingest/assets/docs.js?v=wiki-1" defer></script><noscript><style>.nav-search{display:none!important}</style></noscript></head>')
    header = re.search(r'<header class="family-header">.*?</header>', template, re.S)[0]
    header = header.replace(' aria-current="page"', '')
    header = re.sub(r'https://github\.com/brianrenshaw/brianrenshaw-app-site/releases/download/ingest-v[^"]+/Ingest-[^"]+\.dmg', lambda _: LATEST_DOWNLOAD, header)
    footer = re.search(r'<footer\b.*?</footer>', template, re.S)[0]
    crumb = f'<nav class="wiki-breadcrumbs" aria-label="Breadcrumb"><a href="/ingest/">Ingest</a><span aria-hidden="true">/</span><a href="/ingest/{slug}/">{esc(DATA[slug]["title"])}</a>'
    if active: crumb += f'<span aria-hidden="true">/</span><span aria-current="page">{esc(title)}</span>'
    crumb += '</nav>'
    return head + f'''<body class="app-ingest ingest-docs wiki-docs">
<a class="skip-link" href="#main">Skip to content</a>{header}
<div class="wiki-toolbar"><a href="/ingest/guide/">Help center</a><button type="button" class="nav-search wiki-search" data-ingest-palette aria-haspopup="dialog">Search the guide and support <kbd>⌘K</kbd></button></div>
<div class="wiki-layout"><aside class="wiki-sidebar"><details class="wiki-navigation" open><summary>Browse help topics</summary><div class="wiki-nav-inner">{sidebar(slug,active)}</div></details></aside>
<main id="main" tabindex="-1" class="wiki-main">{crumb}<header class="wiki-heading"><h1>{esc(title)}</h1><p>{esc(description)}</p></header>{body}</main></div>{footer}</body></html>'''


INTRO = {'guide': 'Choose a task. Follow a focused guide, then get back to your photographs.',
         'support': 'Find the problem you’re seeing and the steps to resolve it.',
         'shortcuts': 'Find a command by task. These are Mac keyboard shortcuts; your custom bindings may differ.'}
for slug, collection in DATA.items():
    cards = '<div id="doc-content" class="wiki-directory">'
    for group in collection['groups']:
        cards += f'<section><h2>{esc(group["title"])}</h2><ul>'
        for aid in group['ids']:
            a = next(a for a in collection['articles'] if a['id'] == aid)
            url = f'/ingest/{slug}/{aid}/'
            aliases = re.findall(r'\bid="([^"]+)"', a['body'])
            cards += f'<li id="{aid}" data-article="{url}">' + ''.join(f'<span id="{alias}" data-article="{url}#{alias}"></span>' for alias in aliases)
            cards += f'<a href="{url}">{esc(a["title"])}<span aria-hidden="true"> →</span></a></li>'
        cards += '</ul></section>'
    cards += '</div>'
    if slug == 'guide':
        cards = '<div class="wiki-start"><strong>Start here</strong><span> Your first shoot in five steps.</span><a href="/ingest/getting-started/">Open → Review → Add details → Import → Save your setup</a></div>' + cards
    if slug == 'support':
        cards = '<div class="wiki-start"><strong>Common issues</strong><a href="/ingest/support/ingest-problems/">An import did not finish →</a><a href="/ingest/support/metadata-problems/">Metadata is missing →</a><a href="/ingest/support/photos-support/">Apple Photos needs help →</a></div>' + cards
    if slug == 'shortcuts':
        cards = '<div class="wiki-start"><strong>You only need one to begin: <kbd>⌘K</kbd>.</strong> Type an action in the app’s command palette. <a href="/ingest/shortcuts/palette/">How the palette works →</a></div>' + cards
    (SITE / slug / 'index.html').write_text(page(slug, collection['title'], INTRO[slug], cards))
    for i, a in enumerate(collection['articles']):
        body = rewrite(a['body'], slug)
        # Allow keyboard combinations to wrap between keycaps, with explicit
        # labels on compact table rows. Keep semantic tables for assistive tools.
        def table(match):
            t=match[0]
            labels=[re.sub('<[^>]*>', '', v) for v in re.findall(r'<th\b[^>]*>(.*?)</th>',t,re.S)]
            def row(m):
                cells=re.findall(r'<td([^>]*)>(.*?)</td>',m[0],re.S)
                if not cells:return m[0]
                return '<tr>'+''.join(f'<td{attrs} data-label="{esc(labels[n] if n<len(labels) else "",quote=True)}">{content}</td>' for n,(attrs,content) in enumerate(cells))+'</tr>'
            return re.sub(r'<tr>.*?</tr>',row,t,flags=re.S)
        body=re.sub(r'<table\b.*?</table>',table,body,flags=re.S)
        body = body.replace('<table>', '<table role="table">').replace('<tr>', '<tr role="row">').replace('<th scope=', '<th role="columnheader" scope=').replace('<td ', '<td role="cell" ')
        article = f'<article class="wiki-article" id="{a["id"]}">{body}</article>'
        others = collection['articles']
        links=[]
        if i: links.append(f'<a href="/ingest/{slug}/{others[i-1]["id"]}/"><small>Previous topic</small>{esc(others[i-1]["title"])}</a>')
        if i+1<len(others): links.append(f'<a href="/ingest/{slug}/{others[i+1]["id"]}/"><small>Next topic</small>{esc(others[i+1]["title"])}</a>')
        article += '<nav class="wiki-related" aria-label="Adjacent articles">'+''.join(links)+'</nav>'
        article += f'<p class="wiki-updated">Applies to Ingest 0.9.9.4 (55) · <a href="/ingest/support/contact/">Still need help?</a></p>'
        dest=SITE/slug/a['id']/'index.html';dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(page(slug,a['title'],'',article,a['id']))
# Search results lead straight to an article rather than a long-page fragment.
p=SITE/'assets/search-index.json';items=json.loads(p.read_text())
for item in items: item['url']=mapping.get(item['url'],item['url'])
known={x['url'] for x in items}
for slug,collection in DATA.items():
    for a in collection['articles']:
        route=f'/ingest/{slug}/{a["id"]}/'
        for item in items:
            if item['url'] == route:
                item.update(title=a['title'], keywords=re.sub('<[^>]+>', ' ', a['body'])[:600], hint=collection['title'])
        if route not in known:
            items.append({'type':'section','title':a['title'],'url':route,'keywords':re.sub('<[^>]+>',' ',a['body'])[:600],'hint':collection['title']})
for item in items:
    if item['url'] == '/ingest/getting-started/': item.update(title='Start here: your first shoot', keywords='start here getting started first import card folder review metadata Lightroom Classic workspace')
p.write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
print('Built',sum(len(c['articles']) for c in DATA.values()),'articles and three help directories.')

# Keep the other task references in the same help shell.
references = json.loads((ROOT / 'docs/ingest/reference-content.json').read_text())
for slug, ref in references.items():
    body = re.sub(r'/ingest/(guide|support|shortcuts)/#[\w-]+', lambda m: mapping.get(m[0], m[0]), ref['body'])
    body = re.sub(r'<table\b.*?</table>', table, body, flags=re.S)
    body = body.replace('<table>', '<table role="table">').replace('<tr>', '<tr role="row">').replace('<th scope=', '<th role="columnheader" scope=').replace('<td ', '<td role="cell" ')
    body = re.sub(r'<nav class="guide-toc"(.*?)>(.*?)</nav>', '', body, flags=re.S)
    output = page('guide', html.unescape(ref['title']), '', '<article class="wiki-article">' + body + '</article>', route_override=f'/ingest/{slug}/')
    output = output.replace('href="/ingest/guide/" aria-current="page"', 'href="/ingest/guide/"')
    output = output.replace(f'href="/ingest/{slug}/">', f'href="/ingest/{slug}/" aria-current="page">')
    (SITE / slug / 'index.html').write_text(output)

from ingest_doc_navigation import add_page_navigation
for slug in [*DATA, *references]:
    for path in (SITE / slug).rglob('index.html'):
        path.write_text(add_page_navigation(path.read_text()))
