#!/usr/bin/env python3
"""Frame existing Mac captures: --cli /path/to/frames --assets /path/to/Frames.
Requires Pillow and viticci/frames-cli. Original screenshots stay untouched.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'site/walkthrough/assets'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cli', required=True, type=Path)
    parser.add_argument('--assets', required=True, type=Path)
    args = parser.parse_args()
    entries = []
    for name in ['workspace', 'commands']:
        source = DEST / f'native-{name}-1.4.2.png'
        original = Image.open(source).convert('RGBA')
        canvas = Image.new('RGBA', (3024, 1964), '#303737')
        assert original.width <= canvas.width and original.height <= canvas.height
        canvas.alpha_composite(original, ((canvas.width-original.width)//2, (canvas.height-original.height)//2))
        with tempfile.TemporaryDirectory(prefix='walkthrough-frames-') as temporary:
            temp = Path(temporary)
            capture = temp / f'{name}.png'
            canvas.save(capture)
            result = subprocess.run([sys.executable, str(args.cli), '--assets', str(args.assets), '--json', 'frame', '-d', 'MacBook Pro M5 14', '-c', 'Silver', '-o', str(temp/'output'), str(capture)], check=True, capture_output=True, text=True)
            info = json.loads(result.stdout)
            artwork = Image.open(info['output']).convert('RGBA')
            artwork = artwork.crop(artwork.getchannel('A').getbbox())
            output = DEST / f'macbook-{name}-1.4.2.webp'
            artwork.save(output, 'WEBP', lossless=True, exact=True)
            entries.append(dict(file=output.name, width=artwork.width, height=artwork.height, source=source.name, sourceSHA256=hashlib.sha256(source.read_bytes()).hexdigest(), device='MacBook Pro M5 14',color='Silver',tool='https://github.com/viticci/frames-cli',version='1.5.0',presentation='Original native app window, unscaled and uncropped, centered on a neutral 3024 by 1964 display canvas.'))
            print(output.name, artwork.size)
    (DEST/'macbook-frames.json').write_text(json.dumps(entries,indent=2)+'\n')

if __name__ == '__main__':
    main()
