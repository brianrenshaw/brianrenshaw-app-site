#!/usr/bin/env python3
"""Render Walkthrough help from docs/walkthrough; uses only the standard library."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/walkthrough'
SITE = ROOT / 'site/walkthrough'
ARTICLES = json.loads((SOURCE / 'articles.json').read_text())
GROUPS = list(dict.fromkeys(a['group'] for a in ARTICLES))
e = html.escape

def url(a):
    return f'/walkthrough/{a["kind"]}/{a["slug"]}/'

def links(body):
    for a in sorted(ARTICLES, key=lambda item: len(item["slug"]), reverse=True):
        body = body.replace(f'/walkthrough/{a["kind"]}/#{a["slug"]}', url(a))
    return body

def sidebar(current):
    out = '<aside class="wiki-sidebar"><details class="wiki-navigation" open><summary>Browse help topics</summary><div class="wiki-nav-inner"><a class="wiki-home" href="/walkthrough/support/">Walkthrough help</a><nav aria-label="Help topics">'
    for group in GROUPS:
        out += f'<div class="wiki-group"><h2>{e(group)}</h2>'
        for a in ARTICLES:
            if a['group'] == group:
                active = ' aria-current="page"' if current == url(a) else ''
                out += f'<a href="{url(a)}"{active}>{e(a["title"])}</a>'
        out += '</div>'
    return out + '</nav></div></details></aside>'

def page(title, description, route, body):
    frame = (SOURCE / 'help-frame.html').read_text()
    frame = re.sub(r'<title>.*?</title>', f'<title>{e(title)} | Walkthrough Help</title>', frame)
    frame = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda m:m[1]+e(description,quote=True), frame)
    frame = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m:m[1]+e(title+' | Walkthrough Help',quote=True), frame)
    frame = re.sub(r'(<link rel="canonical" href="|<meta property="og:url" content=")[^"]*', lambda m:m[1]+'https://brianrenshaw.app'+route, frame)
    frame = frame.replace('</head>', '<link rel="stylesheet" href="/walkthrough/assets/docs.css"><script src="/walkthrough/assets/docs.js" defer></script></head>')
    frame = frame.replace('class="app-listing-namer"','class="app-listing-namer wiki-docs"')
    frame = frame.replace('>Support</a>', '>Help center</a>')
    layout = '<div class="wiki-toolbar"><a href="/walkthrough/support/">Walkthrough help · Mac</a><a href="/walkthrough/support/#find-topic">Find a topic</a></div>'
    layout += '<div class="wiki-layout">'+sidebar(route)+'<main id="main" tabindex="-1" class="wiki-main">'+body+'<p class="wiki-updated">Guide for Walkthrough 1.4.2 · Updated October 6, 2026. Screenshots use demonstration data with repeated photographs.</p></main></div>'
    dest = ROOT / 'site' / route.strip('/') / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(frame.replace('{{CONTENT}}', layout))

def directory():
    out = '<section id="find-topic"><h2>Find a topic</h2><div class="help-search" hidden><label for="topic-search">Search guides and support</label><input id="topic-search" type="search" placeholder="Try rooms, filenames, copy, or updates" aria-controls="topic-directory"><p id="search-status" role="status" aria-live="polite"></p></div><div id="topic-directory" class="wiki-directory">'
    for group in GROUPS:
        out += f'<section class="help-collection"><h2>{e(group)}</h2><ul>'
        for a in ARTICLES:
            if a['group'] != group:
                continue
            search = re.sub('<[^>]+>', ' ', a['title']+' '+a['summary']+' '+a['body'])
            out += f'<li data-topic="{e(html.unescape(search),quote=True)}"><a href="{url(a)}"><div><strong>{e(a["title"])}</strong><small>{e(a["summary"])}</small></div><span aria-hidden="true">→</span></a></li>'
        out += '</ul></section>'
    return out+'</div></section>'

for i,a in enumerate(ARTICLES):
    body = '<nav class="wiki-breadcrumbs" aria-label="Breadcrumb"><a href="/walkthrough/support/">Walkthrough help</a><span aria-hidden="true">/</span>'+e(a['group'])+'</nav>'
    body += f'<header class="wiki-heading"><h1>{e(a["title"])}</h1><p>{e(a["summary"])}</p></header>'
    content = links(a['body'])
    headings = []
    def section_heading(match):
        text = re.sub('<[^>]+>', '', match[1])
        anchor = 'section-' + str(len(headings) + 1)
        headings.append((anchor, text))
        return f'<h3 id="{anchor}">{match[1]}</h3>'
    content = re.sub(r'<h3>(.*?)</h3>', section_heading, content)
    if len(headings) > 1:
        body += '<details class="wiki-on-page" open><summary>On this page</summary><nav aria-label="On this page">' + ''.join(f'<a href="#{anchor}">{e(text)}</a>' for anchor,text in headings) + '</nav></details>'
    body += '<article class="wiki-article">'+content+'</article>' 
    related = ARTICLES[max(0,i-1):i]+ARTICLES[i+1:i+2]
    body += '<nav class="wiki-related" aria-label="Related articles">'+''.join(f'<a href="{url(b)}"><small>Continue reading</small>{e(b["title"])}</a>' for b in related)+'</nav>'
    page(a['title'],a['summary'],url(a),body)
for kind,title in [('guide','Walkthrough guide'),('support','Walkthrough help and support')]:
    description = 'Open a listing, group and order its photos, and review numbered filenames before processing.'
    body = f'<header class="wiki-heading"><h1>{title}</h1><p>{description}</p></header><div class="wiki-start"><strong>Start with your first listing</strong><a href="/walkthrough/guide/workspace/">Open a folder and assign rooms →</a><a href="/walkthrough/guide/export/">Review filenames and process photos →</a></div>'+directory()
    if kind == 'guide':
        body += '<section class="legacy-topics"><h2>Guide reference links</h2>'
        for a in ARTICLES:
            if a['kind']=='guide':
                body += f'<p id="{a["slug"]}" data-article="{url(a)}"><a href="{url(a)}">{e(a["title"])} →</a></p>'
        body += '</section>'
    else:
        legacy = re.sub(r'<h1>.*?</h1>','',(SOURCE/'support-overview.html').read_text(),count=1)
        body += '<section class="help-reference"><details><summary>Quick reference</summary>'+links(legacy)+'</details></section>'
        body += '<p>Need more help? <a href="/walkthrough/support/contact/">Contact Walkthrough support →</a></p>'
    page(title,description,f'/walkthrough/{kind}/',body)
print(f'PASS: rendered {len(ARTICLES)} articles and two help directories')

# Add article routes without changing the other apps' sitemap entries.
sitemap = ROOT / 'site/sitemap.xml'
xml = sitemap.read_text()
for article in ARTICLES:
    canonical = 'https://brianrenshaw.app' + url(article)
    if f'<loc>{canonical}</loc>' not in xml:
        xml = xml.replace('</urlset>', f'<url><loc>{canonical}</loc></url></urlset>')
sitemap.write_text(xml)
