#!/usr/bin/env python3
"""Check static links, fragments, metadata, assets, and deployment completeness."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin,urlsplit,unquote
import re,sys
ROOT=Path(__file__).resolve().parents[1]/'site'
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=True);self.refs=[];self.ids=set();self.canonical=[];self.h1=0;self.lang=False;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='html':self.lang=bool(a.get('lang'))
  if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
  for attr in ['href','src','poster']:
   if a.get(attr):self.refs.append((tag,attr,a[attr]))
pages={p:Page(p.read_text()) for p in ROOT.rglob('*.html')};errors=[];links=0
for p,page in pages.items():
 rel=p.relative_to(ROOT).as_posix();url='https://brianrenshaw.app/'+rel
 if not page.lang:errors.append(f'{rel}: missing language')
 if page.h1!=1:errors.append(f'{rel}: expected one h1, found {page.h1}')
 if p.name=='index.html':
  expected=url.removesuffix('index.html')
  aliases={'chooser/':'whos-first/','chooser/play/':'whos-first/','chooser/support/':'whos-first/support/','chooser/privacy/':'whos-first/privacy/'}
  expected='https://brianrenshaw.app/'+aliases.get(rel.removesuffix('index.html'),rel.removesuffix('index.html'))
  if page.canonical!=[expected]:errors.append(f'{rel}: canonical {page.canonical}, expected {expected}')
 for tag,attr,ref in page.refs:
  if ref.startswith(('mailto:','tel:','data:')):continue
  target=urlsplit(urljoin(url,ref))
  if target.hostname!='brianrenshaw.app':
   if attr=='src' or tag=='link' and not ref.startswith('https://brianrenshaw.app'):errors.append(f'{rel}: external asset {ref}')
   continue
  path=ROOT/unquote(target.path).lstrip('/')
  if target.path.endswith('/') or path.is_dir():path=path/'index.html'
  if not path.exists():errors.append(f'{rel}: missing {ref}')
  elif target.fragment and path in pages and unquote(target.fragment) not in pages[path].ids:errors.append(f'{rel}: missing fragment {ref}')
  links+=1
for p in ROOT.rglob('*.css'):
 for ref in re.findall(r'url\([\'\"]?([^\)\'\"]+)',p.read_text()):
  if ref.startswith('data:'):continue
  if not (p.parent/ref).exists():errors.append(f'{p.relative_to(ROOT)}: missing CSS asset {ref}')
for slug in ['reading-habit','where-do-we-eat','whos-first','folio']:
 for sub in ['','privacy','support']:
  if not (ROOT/slug/sub/'index.html').exists():errors.append(f'Missing route {slug}/{sub}')
if errors:print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(pages)} HTML pages; {links} local links/assets; canonical URLs, fragments, fonts and required routes.')
