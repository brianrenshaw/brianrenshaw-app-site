#!/usr/bin/env python3
"""Create lossless device presentations using viticci/frames-cli v1.5.0.

Pass --cli /path/to/frames --assets /path/to/Frames. Originals stay unchanged.
The Mac capture is centered, at native pixel size, on a neutral screen canvas;
it is a presentation of an app window, not a full-desktop screenshot.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'site/decks/assets'
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--cli', required=True, type=Path)
p.add_argument('--assets', required=True, type=Path)
a = p.parse_args()
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
version = subprocess.check_output([str(a.cli), '--version'], text=True).strip()
manifest = json.loads((DEST / 'oct06-assets.json').read_text())
jobs = [
    ('phone', 'oct06-phone-layout.webp', 'iPhone 17 Pro Portrait', 'Silver'),
    ('phone-camera', 'oct06-phone-camera.webp', 'iPhone 17 Pro Portrait', 'Silver'),
    ('phone-text', 'oct06-phone-text.webp', 'iPhone 17 Pro Portrait', 'Silver'),
    ('ipad', 'oct06-ipad-editor.webp', 'iPad Air 2020 Portrait', None),
    ('builder', 'oct06-next-ipad-builder-upright.webp', 'iPad Air 2020 Landscape', None),
    ('mac', 'oct06-mac.webp', 'MacBook Pro M5 14', 'Silver'),
]
with tempfile.TemporaryDirectory(prefix='decks-device-frames-') as tmp:
    tmp = Path(tmp)
    for name, source, device, color in jobs:
        original = Image.open(DEST / source).convert('RGBA')
        capture = original
        padding = None
        if name == 'mac':
            capture = Image.new('RGBA', (3024, 1964), '#e4e3df')
            padding = [(capture.width-original.width)//2, (capture.height-original.height)//2]
            capture.alpha_composite(original, tuple(padding))
        input_path = tmp / (name + '.png')
        capture.save(input_path)
        command = [str(a.cli), '--assets', str(a.assets), '--json', 'frame', '-d', device, '-o', str(tmp / 'output')]
        if color:
            command += ['-c', color]
        subprocess.run(command + [str(input_path)], check=True)
        framed = Image.open(tmp / 'output' / (name + '_framed.png')).convert('RGBA')
        target = DEST / ('oct06-framed-' + name + '.webp')
        framed.save(target, 'WEBP', lossless=True, exact=True)
        assert Image.open(target).convert('RGBA').tobytes() == framed.tobytes()
        entry = dict(file=target.name, kind='native-screenshot-device-presentation', width=framed.width, height=framed.height,
                     source=source, sourceSha256=sha(DEST/source), sha256=sha(target),
                     framingTool='https://github.com/viticci/frames-cli', framingVersion=version,
                     framingCommit=subprocess.check_output(['git', '-C', str(a.cli.parent), 'rev-parse', 'HEAD'], text=True).strip(),
                     device=device, color=color, orientation='upright input; no rotation or screenshot resampling',
                     presentation='Native window centered on a neutral 3024x1964 screen canvas at original pixel size.' if padding else 'Original capture with device bezel and hardware mask.',
                     screenPadding=padding)
        frame_asset = a.assets / (device + (' ' + color if color else '') + '.png')
        entry['frameAssetSha256'] = sha(frame_asset)
        manifest['images'] = [i for i in manifest['images'] if i['file'] != target.name] + [entry]
        print(target.name, framed.size)
(DEST / 'oct06-assets.json').write_text(json.dumps(manifest, indent=2) + '\n')
