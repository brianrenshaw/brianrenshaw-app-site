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
  aliases={'chooser/':'whos-first/','chooser/play/':'whos-first/','chooser/support/':'whos-first/support/','chooser/privacy/':'whos-first/privacy/','listing-namer/':'walkthrough/','listing-namer/guide/':'walkthrough/guide/','listing-namer/support/':'walkthrough/support/','listing-namer/privacy/':'walkthrough/privacy/','listing-namer/release-notes/':'walkthrough/release-notes/'}
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
# American spellings only. Brian is from the Midwest, and British forms keep
# creeping into drafted copy. aria-labelledby is a real ARIA attribute, so it is
# stripped before the scan rather than excused word by word. Suffixes are listed
# deliberately: cancelled is British, cancellation is correct in both.
_OUR='col behavi fav hon lab neighb flav hum rum endeav sav arm vap od val vig splend harb parl'
_ISE='organ recogn real apolog custom optim categor summar priorit standard personal special visual minim maxim util author synchron normal initial final local modern digit item memor familiar character central general sanit emphas critic'
_LL='trave labe mode cance fue signa tota marve jewe counse'
_PLAIN='centre metre litre fibre calibre theatre sombre spectre lustre meagre manoeuvre licence defence offence pretence whilst amongst learnt spelt dreamt programme catalogue analogue instalment enrolment skilful wilful judgement ageing storey tyre kerb cheque aluminium aeroplane maths'
BRITISH=re.compile('(?i)\\b(?:'+'|'.join([
 '(?:%s)our(?:s|ed|ing|ite|ites|able|ably|ful|less|ist|ists)?'%'|'.join(_OUR.split()),
 '(?:%s)is(?:e|es|ed|ing|ation|ations|er|ers|able)'%'|'.join(_ISE.split()),
 '(?:%s)ll(?:ed|ing|er|ers|or|ors|ous|ery)'%'|'.join(_LL.split()),
 '(?:anal|paral|catal)ys(?:e|es|ed|ing|er|ers)',
 'practis(?:e|es|ed|ing)','fulfil(?:s|ment|ments)?','sceptic(?:al|ism)?','mould(?:s|ed|ing|y)?','grey(?:s|ed|ish|scale)?',
 '(?:%s)s?'%'|'.join(_PLAIN.split()),
])+')\\b')
for p,page in pages.items():
 for word in sorted(set(BRITISH.findall(re.sub(r'\saria-labelledby="[^"]*"','',p.read_text())))):
  errors.append(f'{p.relative_to(ROOT).as_posix()}: British spelling "{word}"')
for slug in ['reading-habit','where-do-we-eat','whos-first','folio','walkthrough','ingest']:
 for sub in ['','privacy','support']:
  if not (ROOT/slug/sub/'index.html').exists():errors.append(f'Missing route {slug}/{sub}')
if not (ROOT/'walkthrough/release-notes/index.html').exists():errors.append('Missing Walkthrough release history')
for sub in ['guide/','quick-start/','shortcuts/','templates/','automation/','release-notes/']:
 if not (ROOT/'ingest'/sub/'index.html').exists():errors.append(f'Missing Ingest page {sub}')
# Every shipped Ingest build has https://brianrenshaw.app/ingest/appcast.xml compiled into SUFeedURL.
if not (ROOT/'ingest/appcast.xml').exists():errors.append('Missing Sparkle feed for Ingest')
if not (ROOT/'walkthrough/guide/index.html').exists():errors.append('Missing Walkthrough illustrated guide')
# Walkthrough moved to /walkthrough/, but every shipped copy of the Mac app has
# https://brianrenshaw.app/listing-namer/appcast.xml compiled into SUFeedURL, and a
# static host cannot redirect it. This file must keep serving real XML permanently.
if not (ROOT/'listing-namer/appcast.xml').exists():errors.append('Missing Sparkle feed at the original /listing-namer/ path')
for sub in ['','guide/','support/','privacy/','release-notes/']:
 if not (ROOT/'listing-namer'/sub/'index.html').exists():errors.append(f'Missing listing-namer/{sub} redirect')
if errors:print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(pages)} HTML pages; {links} local links/assets; canonical URLs, fragments, fonts, required routes and American spelling.')
