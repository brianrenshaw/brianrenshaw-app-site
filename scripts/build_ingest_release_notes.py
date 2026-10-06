#!/usr/bin/env python3
"""Render undated, version-specific release notes with native version selection."""
from pathlib import Path
import json,re,html
from ingest_doc_navigation import add_page_navigation
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site/ingest'
notes=json.loads((ROOT/'docs/ingest/release-notes.json').read_text())
base=(SITE/'guide/index.html').read_text()
latest=notes[0]['version']
for note in notes:
    version=note['version']
    options=''.join(f'<option value="/ingest/release-notes/{n["version"]}/"'+(' selected' if n['version']==version else '')+f'>{n["version"]}'+(' · Latest' if n['version']==latest else '')+'</option>' for n in notes)
    picker=f'<div class="release-picker"><label for="release-version">Version</label><select id="release-version" aria-label="Release version">{options}</select></div>'
    links=''.join(f'<a id="v{n["version"]}" data-article="/ingest/release-notes/{n["version"]}/" href="/ingest/release-notes/{n["version"]}/">Version {n["version"]}</a>' for n in notes if n['version']!=version)
    content=f'<nav class="wiki-breadcrumbs" aria-label="Breadcrumb"><a href="/ingest/guide/">Help center</a><span aria-hidden="true">/</span><a href="/ingest/release-notes/">Release notes</a></nav><header class="wiki-heading"><h1>What’s new in Ingest</h1></header>{picker}<article class="wiki-article" id="v{version}"><h2>Ingest {version}</h2>{note["body"]}</article><nav class="release-legacy" aria-label="Other releases">{links}</nav>'
    s=re.sub(r'<main\b.*?</main>',lambda m:'<main id="main" tabindex="-1" class="wiki-main">'+content+'</main>',base,flags=re.S)
    sidebar='<nav aria-label="Help collections" class="wiki-collections"><a href="/ingest/guide/">Guide</a><a href="/ingest/support/">Support</a><a href="/ingest/shortcuts/">Keyboard shortcuts</a><a href="/ingest/release-notes/" aria-current="page">Release notes</a></nav>'
    s=re.sub(r'<aside class="wiki-sidebar">.*?</aside>',lambda m:'<aside class="wiki-sidebar"><details class="wiki-navigation" open><summary>Browse help topics</summary><div class="wiki-nav-inner">'+sidebar+'</div></details></aside>',s,flags=re.S)
    s=re.sub(r'<title>.*?</title>',f'<title>Ingest {version} — Release notes</title>',s)
    s=re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*',lambda m:m[1]+f'Improvements and fixes in Ingest {version}.',s)
    s=re.sub(r'(<meta property="og:title" content=")[^"]*',lambda m:m[1]+f'Ingest {version} — Release notes',s)
    s=s.replace('</head>','<script src="/ingest/assets/releases.js" defer></script><noscript><style>.release-picker{display:none}.release-legacy{display:grid!important;gap:10px;margin-top:24px}</style></noscript></head>')
    route=f'https://brianrenshaw.app/ingest/release-notes/{version}/'
    s=s.replace('https://brianrenshaw.app/ingest/guide/',route)
    s=add_page_navigation(s)
    target=SITE/'release-notes'/version/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(s)
    if version==latest:
        (SITE/'release-notes/index.html').write_text(s.replace(route,'https://brianrenshaw.app/ingest/release-notes/'))
print(f'Built {len(notes)} undated release pages and latest-release index.')

index_path=SITE/'assets/search-index.json'
items=json.loads(index_path.read_text())
for item in items:
    item['url']=re.sub(r'/ingest/release-notes/#v([0-9.]+)',r'/ingest/release-notes/\1/',item['url'])
index_path.write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
