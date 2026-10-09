#!/usr/bin/env python3
"""Render the static Decks help center from reviewed article data.
Edit docs/decks/articles.json and support-overview.html, then run this script.
"""
import html,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site/decks'
articles=json.loads((ROOT/'docs/decks/articles.json').read_text())
dimensions={i['file']:(i['width'],i['height']) for i in json.loads((SITE/'assets/oct06-assets.json').read_text())['images']}
groups=['Getting Started','Make It Yours','Save & Share','Your Library']
e=html.escape
url=lambda slug:f'/decks/guide/{slug}/'
def nav(current):
 out='<aside class="wiki-sidebar"><details class="wiki-navigation" open><summary>Browse help topics</summary><div class="wiki-nav-inner"><a class="wiki-home" href="/decks/support/">Decks help</a><nav aria-label="Help topics">'
 for g in groups:
  out+=f'<div class="wiki-group"><h2>{e(g)}</h2>'
  for a in articles:
   if a['group']==g:out+=f'<a href="{url(a["slug"])}"'+(' aria-current="page"' if current==a['slug'] else '')+f'>{e(a["title"])}</a>'
  out+='</div>'
 return out+'</nav></div></details></aside>'
def shell(title,description,route,body,current=''):
 canonical='https://brianrenshaw.app'+route
 return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)} — Decks Help</title><meta name="description" content="{e(description,quote=True)}"><link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:title" content="{e(title,quote=True)} — Decks Help"><meta property="og:description" content="{e(description,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="https://brianrenshaw.app/decks/assets/social-oct06-next.png"><link rel="icon" href="/decks/assets/icon.png"><link rel="stylesheet" href="/assets/apps.css"><link rel="stylesheet" href="/assets/family.css"><link rel="stylesheet" href="/decks/assets/site.css?v=oct08-smart-steps"><link rel="stylesheet" href="/decks/assets/docs.css?v=2"><script src="/decks/assets/docs.js?v=1" defer></script></head>
<body class="app-decks wiki-docs"><a class="skip-link" href="#main">Skip to content</a><header class="family-header"><a class="family-brand" href="/decks/"><img src="/decks/assets/icon.png" width="36" height="36" alt="">Decks</a><nav aria-label="Main navigation"><a href="/decks/">Overview</a><a href="/decks/support/">Help center</a><a href="/decks/guide/install/">Getting started</a><a href="https://testflight.apple.com/join/SAMjeMy5">Try the beta ↗</a></nav></header><div class="wiki-toolbar"><a href="/decks/support/">Decks help · iPhone, iPad &amp; Mac</a><a href="/decks/support/#find-topic">Find a topic</a></div><div class="wiki-layout">{nav(current)}<main id="main" tabindex="-1" class="wiki-main">{body}<p class="wiki-updated">Updated October 9, 2026 · Public beta guide. Screens and available controls can vary by device and window size.</p></main></div><footer class="family-footer"><span>© 2026 Brian Renshaw</span><nav aria-label="Footer"><a href="/decks/support/">Help center</a><a href="/decks/privacy/">Privacy</a><a href="mailto:contact@brianrenshaw.app">Contact</a></nav></footer></body></html>'''
def write(route,text):
 p=ROOT/'site'/route.removeprefix('/');p.mkdir(parents=True,exist_ok=True);(p/'index.html').write_text(text)
def shot(info):
 if not info:return ''
 asset,original,caption=info;w,h=dimensions[asset]
 return f'<figure class="help-shot"><a href="/decks/assets/{original}" aria-label="View original screenshot: {e(caption,quote=True)}"><img src="/decks/assets/{asset}" width="{w}" height="{h}" loading="lazy" alt="{e(caption,quote=True)}"></a><figcaption>{e(caption)} <a href="/decks/assets/{original}">View full size ↗</a></figcaption></figure>'
def shots(infos):
 if len(infos)<2:return ''.join(shot(info) for info in infos)
 return '<div class="help-shot-row">'+''.join(shot(info) for info in infos)+'</div>'
for i,a in enumerate(articles):
 body=f'<nav class="wiki-breadcrumbs" aria-label="Breadcrumb"><a href="/decks/support/">Decks help</a><span aria-hidden="true">/</span><span>{e(a["group"])}</span></nav><header class="wiki-heading"><h1>{e(a["title"])}</h1><p>{e(a["summary"])}</p></header>'
 body+='<nav class="platform-links" aria-label="Platform instructions"><a href="#iphone">iPhone</a><a href="#ipad">iPad</a><a href="#mac">Mac</a></nav>'
 body+='<article class="wiki-article">'
 if a.get('sections'):
  body+='<h2 id="iphone">iPhone</h2><p>Start with the steps below. Editing tools appear beneath the canvas; tap the active tool to hide or show its controls.</p><h2 id="ipad">iPad</h2><p>Use the same task steps. The sidebar gives you access to Home, Templates, and Projects. In a wide editor window, controls can sit alongside the canvas; narrower windows use the compact panel. A missing control may be inside a collapsed section or the page’s options.</p>'
  body+=shots(a.get('ipadShots',[]))
  for j,sec in enumerate(a['sections']):
   body+=f'<h3 id="step-{j+1}">{e(sec["heading"])}</h3><ol>'+''.join(f'<li>{e(t)}</li>' for t in sec['steps'])+'</ol>'+shots(sec.get('shots',[]))
 else:
  body+='<h2 id="iphone">iPhone</h2><p>Follow the workflow below on your iPhone. Use the Mac notes for desktop-specific controls.</p><h2 id="ipad">iPad</h2><p>The same workflow applies on iPad. Editing controls may appear beside the canvas in a wide window instead of below it.</p>'+a['body']
 body+='<h2 id="mac">Mac</h2>'
 if a.get('macSections'):
  for j,sec in enumerate(a['macSections']):
   body+=f'<h3 id="mac-step-{j+1}">{e(sec["heading"])}</h3><ol>'+''.join(f'<li>{e(t)}</li>' for t in sec['steps'])+'</ol>'
 elif a.get('macSteps'):body+='<ol>'+''.join('<li>'+e(t)+'</li>' for t in a['macSteps'])+'</ol>'
 else:body+='<p>'+e(a['mac'])+'</p>'
 body+=shot(a.get('shot'))+''.join(shot(info) for info in a.get('extraShots',[]))
 if a['slug']=='fujifilm':body+=shot(('oct06-fuji-controls.webp','oct06-fuji-controls.webp','Choose which Fujifilm details appear in the composition.'))
 if a['slug']=='shortcuts':body+=shot(('oct06-shortcut-setup.webp','oct06-shortcut-setup.webp','One-time Photos & Shortcuts setup on iPhone.'))
 if a['slug']=='ingest':body+=shot(('oct06-incoming.webp','oct06-incoming.webp','The Mac receiving window offers a new or existing project.'))
 body+='</article><nav class="wiki-related" aria-label="Related articles">'
 for other,label in [(articles[(i-1)%len(articles)],'Previous guide'),(articles[(i+1)%len(articles)],'Next guide')]:
  body+=f'<a href="{url(other["slug"])}"><small>{label}</small>{e(other["title"])}</a>'
 body+='</nav>'
 write(url(a['slug']),shell(a['title'],a['summary'],url(a['slug']),body,a['slug']))
body='<header class="wiki-heading"><h1>Decks support</h1><p>Choose a task, follow the steps for your device, and get back to your photographs.</p></header><div class="wiki-start"><strong>New to Decks?</strong><a href="/decks/guide/install/">Install the beta →</a><a href="/decks/guide/templates/">Make your first composition →</a><a href="/decks/guide/smart-layout/">Prepare a batch for your frame →</a><a href="/decks/guide/date-stamp/">Add a date stamp →</a></div><section id="find-topic"><h2>Find a topic</h2><div class="help-search" hidden><label for="topic-search">Search guides and instructions</label><input id="topic-search" type="search" placeholder="Try templates, crop, Aura, or iCloud" aria-controls="topic-directory"><p id="search-status" role="status" aria-live="polite"></p></div><div class="wiki-directory" id="topic-directory">'
for g in groups:
 body+=f'<section class="help-collection"><h2>{e(g)}</h2><ul>'
 for a in articles:
  if a['group']!=g:continue
  search=re.sub('<[^>]+>',' ',json.dumps(a,ensure_ascii=False))
  body+=f'<li data-topic="{e(search,quote=True)}"><a href="{url(a["slug"])}"><div><strong>{e(a["title"])}</strong><small>{e(a["summary"])}</small></div><span aria-hidden="true">→</span></a></li>'
 body+='</ul></section>'
body+='</div></section><section class="help-reference"><h2>Quick reference</h2><p>Existing support links still lead to these instructions. The focused guides above include platform notes and further steps.</p>'
legacy=(ROOT/'docs/decks/support-overview.html').read_text()
legacy=re.sub(r'<h1>.*?</h1>','',legacy,count=1)
body+=legacy+'</section>'
write('/decks/support/',shell('Support','Task-based guides for Decks on iPhone, iPad, and Mac: layouts, templates, camera details, date stamps, Fujifilm, exports, Shortcuts, and iCloud.','/decks/support/',body))
write('/decks/guide/',shell('Guide','Find a Decks guide for your next photo composition.','/decks/guide/','<header class="wiki-heading"><h1>Decks guide</h1><p>Task-based help for iPhone, iPad, and Mac.</p></header>'+body[body.index('<div class="wiki-start">'):body.index('<section class="help-reference">')]))
print(f'PASS: rendered {len(articles)} Decks articles, guide directory, and support hub')
