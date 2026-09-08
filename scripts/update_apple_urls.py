#!/usr/bin/env python3
"""Inventory or update canonical app URLs. No releases or review submissions are created."""
from pathlib import Path
import os,time,json,urllib.request,urllib.error,sys,subprocess
import jwt
ROOT=Path(__file__).resolve().parents[1]
APPS={'6806757289':'whos-first','6808350718':'where-do-we-eat','6809740339':'reading-habit','6803229706':'folio'}
KEY_ID=os.environ['APP_STORE_KEY_ID'];ISSUER=os.environ['APP_STORE_ISSUER_ID']
KEY=Path(os.environ.get('APP_STORE_KEY_PATH',str(Path.home()/f'.appstoreconnect/private_keys/AuthKey_{KEY_ID}.p8')))
def request(path,method='GET',data=None):
 token=jwt.encode({'iss':ISSUER,'iat':int(time.time()),'exp':int(time.time())+600,'aud':'appstoreconnect-v1'},KEY.read_text(),algorithm='ES256',headers={'kid':KEY_ID,'typ':'JWT'})
 req=urllib.request.Request('https://api.appstoreconnect.apple.com/v1/'+path,headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'},method=method,data=json.dumps(data).encode() if data else None)
 with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
def records(path):
 # Endpoint page size covers this account; follow pagination for future localizations.
 out=[]
 while path:
  d=request(path);out+=d['data'];n=d.get('links',{}).get('next');path=n.split('/v1/',1)[1] if n else None
 return out
if __name__=='__main__':
 apply=sys.argv[1:]==['--apply']
 if sys.argv[1:] not in [[],['--apply']]:sys.exit('Usage: update_apple_urls.py [--apply]')
 if apply:subprocess.run([sys.executable,str(ROOT/'scripts/check_live.py')],check=True)
 log=[]
 for aid,slug in APPS.items():
  base='https://brianrenshaw.app/'+slug+'/'
  app=request('apps/'+aid)['data'];versions=records('apps/'+aid+'/appStoreVersions?limit=200');selected=[]
  # Latest record per platform plus editable drafts; don't rewrite historical releases.
  for platform in {v['attributes']['platform'] for v in versions}:
   vv=[v for v in versions if v['attributes']['platform']==platform]
   latest=max(vv,key=lambda v:tuple(int(n) if n.isdigit() else 0 for n in v['attributes']['versionString'].split('.')))
   selected.append(latest)
   selected.extend(v for v in vv if v!=latest and v['attributes']['appStoreState'] in ['PREPARE_FOR_SUBMISSION','DEVELOPER_REJECTED','REJECTED','METADATA_REJECTED'])
  tasks=[]
  for v in selected:
   for loc in records('appStoreVersions/'+v['id']+'/appStoreVersionLocalizations?limit=200'):
    tasks.append((loc,{'marketingUrl':base,'supportUrl':base+'support/'},v['attributes']['appStoreState'],v['attributes']['versionString']))
  for info in records('apps/'+aid+'/appInfos?limit=200'):
   for loc in records('appInfos/'+info['id']+'/appInfoLocalizations?limit=200'):
    tasks.append((loc,{'privacyPolicyUrl':base+'privacy/'},info['attributes'].get('appStoreState'),'app information'))
  for loc in records('apps/'+aid+'/betaAppLocalizations?limit=200'):
   tasks.append((loc,{'marketingUrl':base,'privacyPolicyUrl':base+'privacy/'},'TestFlight','beta'))
  for loc,attrs,state,version in tasks:
   path=loc['type']+'/'+loc['id'];before={k:loc['attributes'].get(k) for k in attrs}
   item={'app':app['attributes']['name'],'appId':aid,'resource':path,'locale':loc['attributes']['locale'],'version':version,'state':state,'before':before,'desired':attrs,'result':'planned'}
   if before==attrs:item['result']='already matches'
   elif apply:
    try:
     request(path,'PATCH',{'data':{'type':loc['type'],'id':loc['id'],'attributes':attrs}})
     after=request(path)['data']['attributes'];item['after']={k:after.get(k) for k in attrs}
     if item['after']!=attrs:raise RuntimeError('Read-back mismatch: '+path)
     item['result']='saved and verified'
     item['releaseNote']='TestFlight metadata saved' if state=='TestFlight' else 'Saved metadata; public release timing is controlled by Apple. No release was submitted.'
    except urllib.error.HTTPError as e:
     if e.code not in [403,409,422]:raise
     errors=json.loads(e.read()).get('errors',[])
     item['result']='pending editable app version';item['errors']=[{'code':v.get('code'),'detail':v.get('detail')} for v in errors]
   log.append(item)
   print(item['app'],item['version'],item['locale'],loc['type'],item['result'])
 out=ROOT/'migration'/('apple-results.json' if apply else 'apple-plan.json');out.write_text(json.dumps(log,indent=2)+'\n')
 print('Report:',out)
