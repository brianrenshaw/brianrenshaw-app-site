#!/usr/bin/env python3
"""Spotlight what each Smart Layout screenshot is showing.

Reads the unmarked oct08-smart screenshots in site/decks/assets, dims everything
outside the part a step is about, outlines that part in Decks's Sky accent
(#35B6E8, SocialAppearance.accents), and frames the result with frames-cli as
build_decks_device_frames.py does. The unmarked screenshots stay published and
linked as the originals. Regions are in screenshot pixels.
The editor steps stay unmarked: the whole screen is the point there.

  python3 scripts/build_decks_smart_layout_callouts.py --cli /path/to/frames --assets /path/to/Frames
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'site/decks/assets'
SKY = (0x35, 0xB6, 0xE8)
PHONE = ('iPhone 17 Pro Portrait', 'Silver')
SPOTS = {
    'phone-1-frame': ([(61, 735, 1145, 863), (61, 1152, 581, 1441)], PHONE),
    'phone-2-select': ([(0, 662, 1206, 1263), (789, 235, 1157, 368)], PHONE),
    'phone-3-groups': ([(49, 1508, 1152, 2206)], PHONE),
    'phone-4-swap-selected': ([(74, 1142, 314, 1456)], PHONE),
    'phone-5-swapped': ([(61, 1128, 588, 1471)], PHONE),
    'phone-6-styles': ([(61, 534, 1145, 1213)], PHONE),
    'phone-8-editor-single': ([(1059, 196, 1169, 306)], PHONE),
    'phone-share-aura': ([(305, 1015, 502, 1276)], ('iPhone 17 Pro Max Portrait', 'Silver')),
    'pad-3-groups': ([(1470, 600, 2063, 805)], ('iPad Air 2020 Landscape', None)),
    'pad-5-swapped': ([(1470, 600, 2063, 805)], ('iPad Air 2020 Landscape', None)),
}
p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument('--cli', required=True, type=Path)
p.add_argument('--assets', required=True, type=Path)
a = p.parse_args()
sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
version = subprocess.check_output([str(a.cli), '--version'], text=True).strip()
commit = subprocess.check_output(['git', '-C', str(a.cli.parent), 'rev-parse', 'HEAD'], text=True).strip()

def spotlight(image, regions):
    scale = image.width / 1206 if image.width < image.height else image.width / 2360
    pad, line, radius = round(16 * scale), max(8, round(12 * scale)), round(30 * scale)
    boxes = [(max(0, x0 - pad), max(0, y0 - pad), min(image.width, x1 + pad), min(image.height, y1 + pad))
             for x0, y0, x1, y1 in regions]
    hole = Image.new('L', image.size, 255)
    draw = ImageDraw.Draw(hole)
    for box in boxes:
        draw.rounded_rectangle(box, radius, fill=0)
    shade = Image.new('RGBA', image.size, (0, 0, 0, 0))
    shade.putalpha(hole.point(lambda v: v * 150 // 255))
    out = Image.alpha_composite(image, shade)
    draw = ImageDraw.Draw(out)
    for box in boxes:
        draw.rounded_rectangle(box, radius, outline=SKY + (255,), width=line)
    return out

manifest_path = DEST / 'oct06-assets.json'
manifest = json.loads(manifest_path.read_text())
entries = []
with tempfile.TemporaryDirectory(prefix='decks-callouts-') as tmp:
    tmp = Path(tmp)
    for name, (regions, (device, color)) in SPOTS.items():
        source = DEST / ('oct08-smart-%s.webp' % name)
        marked = spotlight(Image.open(source).convert('RGBA'), regions)
        staged = tmp / (name + '.png')
        marked.save(staged)
        command = [str(a.cli), '--assets', str(a.assets), '--json', 'frame', '-d', device, '-o', str(tmp / 'out')]
        if color:
            command += ['-c', color]
        subprocess.run(command + [str(staged)], check=True, stdout=subprocess.DEVNULL)
        framed = Image.open(tmp / 'out' / (name + '_framed.png')).convert('RGBA')
        target = DEST / ('oct08-smart-spot-%s.webp' % name)
        framed.save(target, 'WEBP', lossless=True, exact=True)
        assert Image.open(target).convert('RGBA').tobytes() == framed.tobytes()
        entries.append(dict(file=target.name, kind='annotated-screenshot-device-presentation', width=framed.width,
                            height=framed.height, source=source.name, sourceSha256=sha(source), sha256=sha(target),
                            annotation='Outside %s dimmed (black, 59%%); outlined in Sky #35B6E8' % (regions,),
                            framingTool='https://github.com/viticci/frames-cli', framingVersion=version,
                            framingCommit=commit, device=device, color=color,
                            frameAssetSha256=sha(a.assets / (device + (' ' + color if color else '') + '.png'))))
names = {entry['file'] for entry in entries}
manifest['images'] = [item for item in manifest['images'] if item['file'] not in names] + entries
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
print('Wrote %d spotlighted screenshots' % len(entries))
