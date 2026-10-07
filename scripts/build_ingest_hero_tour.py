#!/usr/bin/env python3
"""Frame three native demo captures using Frames CLI, recording provenance."""
from pathlib import Path
import json,hashlib,subprocess,sys,tempfile
from PIL import Image
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--captures', type=Path, required=True)
parser.add_argument('--frames', type=Path, required=True)
parser.add_argument('--assets', type=Path, required=True)
args=parser.parse_args()
root=Path(__file__).resolve().parents[1];assets=root/'site/ingest/assets';capture=args.captures
m=json.loads((assets/'screenshots.json').read_text());items=[]
for name in ['workflow','focus','details']:
 source=capture/f'tour-{name}.png';im=Image.open(source).convert('RGBA');native=assets/f'hero-{name}-0.9.8-retina.webp';im.save(native,lossless=True,exact=True)
 assert Image.open(native).convert('RGBA').tobytes()==im.tobytes()
 m['images' if native.name in m['images'] else 'archivedImages'][native.name]={'width':im.width,'height':im.height,'displayWidth':im.width//2,'displayHeight':im.height//2,'source':'Ingest 0.9.8 (48), source 0c84a1a. Native Retina capture; isolated demo library; source for hero artwork. See SOURCES.md.','pngSHA256':hashlib.sha256(source.read_bytes()).hexdigest()}
 im.thumbnail((3296,2100),Image.Resampling.LANCZOS);screen=Image.new('RGBA',(3456,2234),'#343936');screen.alpha_composite(im,((3456-im.width)//2,(2234-im.height)//2))
 with tempfile.TemporaryDirectory() as tmp:
  p=Path(tmp);screen.save(p/'screen.png');r=subprocess.run([sys.executable,str(args.frames),'--assets',str(args.assets),'--json','-d','MacBook Pro M5 16','-c','Silver','-o',str(p/'out'),str(p/'screen.png')],capture_output=True,text=True,check=True)
  info=json.loads(r.stdout);art=Image.open(info['output']).convert('RGBA');art=art.crop(art.getchannel('A').getbbox());out=assets/f'hero-macbook-{name}-0.9.8.webp';art.save(out,lossless=True,exact=True)
 items.append({'view':name,'photo':('015-Mountain-Light.DNG' if name=='focus' else '001-Wedding-Selects.CR2'),'photographerCredit':('Original filename: July_mReKo_002.DNG; Signature Edits' if name=='focus' else 'Christian Meza; embedded Artist; Signature Edits'),'nativeScreenshot':native.name,'nativeScreenshotSHA256':hashlib.sha256(native.read_bytes()).hexdigest(),'output':out.name,'width':art.width,'height':art.height,'outputSHA256':hashlib.sha256(out.read_bytes()).hexdigest()})
 print(name,art.size,out.stat().st_size)
(assets/'screenshots.json').write_text(json.dumps(m,indent=2)+'\n')
(assets/'hero-tour.json').write_text(json.dumps({'appVersion':'0.9.8','appBuild':48,'kind':'Device-framed marketing artwork using genuine unretouched native screenshots','device':'MacBook Pro M5 16','tool':'https://github.com/viticci/frames-cli','photoSource':'Signature Edits; individual credit evidence recorded per view','views':items},indent=2)+'\n')
