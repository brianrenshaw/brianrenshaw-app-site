#!/usr/bin/env python3
"""Verify certificate, exact deployed HTML and www redirects before cutover."""
from pathlib import Path
from urllib.parse import urlsplit
import subprocess,hashlib,concurrent.futures,sys
ROOT=Path(__file__).resolve().parents[1]
# Resolve directly to GitHub while recursive DNS caches expire. TLS verification stays enabled.
def fetch(url):
 r=subprocess.run(['curl','--silent','--show-error','--fail','--location','--connect-timeout','5','--max-time','20','--resolve','brianrenshaw.app:443:185.199.108.153','--resolve','www.brianrenshaw.app:443:185.199.108.153',url],capture_output=True)
 if r.returncode:raise RuntimeError(url+': '+r.stderr.decode().strip())
 return r.stdout
if __name__=='__main__':
 try:
  index=fetch('https://brianrenshaw.app/')
  assert index==(ROOT/'site/index.html').read_bytes(),'Homepage differs from local deployment'
  pages=list((ROOT/'site').rglob('index.html'))
  def check(p):
   url='https://brianrenshaw.app/'+p.relative_to(ROOT/'site').as_posix().removesuffix('index.html')
   if fetch(url)!=p.read_bytes():raise RuntimeError('Deployed page differs: '+url)
   return url
  for url in concurrent.futures.ThreadPoolExecutor(max_workers=4).map(check,pages):print('PASS',url)
  assert fetch('https://www.brianrenshaw.app/')==index,'www content differs'
  print('PASS: TLS and all deployed routes match the local site; www resolves.')
 except Exception as e:
  print('NOT READY:',e);sys.exit(1)
