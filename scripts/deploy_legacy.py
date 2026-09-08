#!/usr/bin/env python3
"""Deploy prepared compatibility pages only after verified HTTPS and clean-source checks."""
from pathlib import Path
import subprocess,hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
def git(root,*args):return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
if __name__=='__main__':
 if sys.argv[1:]!=['--apply']:sys.exit('Usage: python3 scripts/deploy_legacy.py --apply (publishes legacy repositories)')
 subprocess.run([sys.executable,str(ROOT/'scripts/check_live.py')],check=True)
 changes=json.loads((ROOT/'migration/legacy-manifest.json').read_text());groups={}
 for item in changes:groups.setdefault(item['root'],[]).append(item)
 # Preflight every repository before touching any file; reruns tolerate an already published payload.
 for root,items in groups.items():
  subprocess.run(['git','fetch','origin'],cwd=root,check=True)
  branch=git(root,'branch','--show-current')
  if git(root,'rev-parse','HEAD')!=git(root,'rev-parse','origin/'+branch):raise RuntimeError('Local/remote heads differ: '+root)
  if git(root,'diff','--cached','--name-only'):raise RuntimeError('Staged user changes: '+root)
  for item in items:
   current=(Path(root)/item['file']).read_bytes();prepared=(ROOT/item['prepared']).read_bytes()
   if hashlib.sha256(current).hexdigest()!=item['original_sha256'] and current!=prepared:raise RuntimeError('Source changed since preparation: '+str(Path(root)/item['file']))
 for root,items in groups.items():
  paths=[]
  for item in items:
   p=Path(root)/item['file'];p.write_bytes((ROOT/item['prepared']).read_bytes());paths.append(item['file'])
  subprocess.run(['git','add','--',*paths],cwd=root,check=True)
  if git(root,'diff','--cached','--name-only'):
   subprocess.run(['git','commit','-m','Preserve legacy app URLs during custom-domain migration'],cwd=root,check=True)
   subprocess.run(['git','push','origin',git(root,'branch','--show-current')],cwd=root,check=True)
  print('Published compatibility pages:',root)
