#!/usr/bin/env python3
"""Package the October 9 Decks assets: the Aura page's iPhone Smart Layout steps and the Story example.

--phone is the exported XCTest attachment folder from SocialDestinationUITests.testSmartLayoutWebsiteCaptures
run on an iPhone 17 Pro simulator (build 154). Each step is stored unmarked, then spotlighted the way
build_decks_smart_layout_callouts.py does (outside the regions dimmed, the regions outlined in Decks's Sky
accent) and set in the Apple Frames iPhone bezel the way build_decks_build154_assets.py does.
--story is the PNG written by render_decks_story.swift. Records go into oct06-assets.json.

  build_decks_oct09_assets.py --phone DIR --story PNG
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'site/decks/assets'
COMMIT = '1c2d23f'
SKY = (0x35, 0xB6, 0xE8)
TEST = 'SocialDestinationUITests.testSmartLayoutWebsiteCaptures'
DEVICE = 'iPhone 17 Pro (simulator, iOS 27.0)'
# Regions in screenshot pixels (1206 × 2622), measured on the build 154 captures.
SPOTS = {
    '1-frame': [(60, 380, 458, 484), (60, 1054, 480, 1500)],      # Aura Carver pill; Smart Layout card
    '2-select': [(0, 664, 1206, 1264), (792, 236, 1156, 366)],    # the five photos; Use 5 Items
    '3-groups': [(96, 1585, 1112, 2236)],                         # summary and Vertical Pairs
    '4-swap-selected': [(114, 1630, 332, 1920), (634, 1630, 856, 1920)],  # the tapped photo; the one to trade with
    '5-swapped': [(112, 1630, 570, 1920), (748, 236, 1156, 366)],         # the new pair; Create
}
p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument('--phone', required=True, type=Path)
p.add_argument('--story', required=True, type=Path)
a = p.parse_args()
sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
manifest_path = DEST / 'oct06-assets.json'
manifest = json.loads(manifest_path.read_text())
entries = []

def save(image, name):
    target = DEST / name
    image.save(target, 'WEBP', lossless=True, exact=True)
    assert Image.open(target).convert(image.mode).tobytes() == image.tobytes(), name
    return target

def spotlight(image, regions):
    scale = image.width / 1206
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

def reframe(image, name):
    """Swap the screen pixels of the Apple Frames iPhone presentation for this image; bezel pixels stay."""
    base_framed, base_screen = 'oct06-framed-phone-camera.webp', 'oct06-phone-camera.webp'
    framed = Image.open(DEST / base_framed).convert('RGBA')
    old = Image.open(DEST / base_screen).convert('RGBA')
    new = image.convert('RGBA')
    assert old.size == new.size, (name, old.size, new.size)
    cx, cy = (framed.width - old.width) // 2, (framed.height - old.height) // 2
    def matches(offset):
        crop = framed.crop((offset[0], offset[1], offset[0] + old.width, offset[1] + old.height)).convert('RGB')
        return ImageChops.difference(crop, old.convert('RGB')).convert('L').histogram()[0]
    ox, oy = max(((x, y) for x in range(cx - 3, cx + 4) for y in range(cy - 3, cy + 4)), key=matches)
    region = framed.crop((ox, oy, ox + old.width, oy + old.height))
    diff = ImageChops.difference(region.convert('RGB'), old.convert('RGB')).convert('L')
    mask = ImageChops.multiply(diff.point(lambda v: 255 if v == 0 else 0),
                               region.getchannel('A').point(lambda v: 255 if v == 255 else 0))
    share = sum(mask.histogram()[255:]) / (old.width * old.height)
    assert share > 0.9, (name, share)
    region.paste(new, (0, 0), mask)
    framed.paste(region, (ox, oy))
    return save(framed, name), framed, share, base_framed, base_screen

def by_name(folder):
    names = {}
    for test in json.loads((folder / 'manifest.json').read_text()):
        for item in test['attachments']:
            names[item['suggestedHumanReadableName'].split('_0_')[0]] = folder / item['exportedFileName']
    return names

phone = by_name(a.phone)
for step, regions in SPOTS.items():
    source = phone['Web-smart-phone-%s' % step]
    image = Image.open(source).convert('RGBA')
    assert image.size == (1206, 2622), (step, image.size)
    plain = save(image.convert('RGB'), 'build154-aura-phone-%s.webp' % step)
    entries.append(dict(file=plain.name, kind='native-screenshot', width=image.width, height=image.height, source=source.name,
                        sourceSha256=sha(source), sha256=sha(plain), build=154, sourceCommit=COMMIT, test=TEST, device=DEVICE,
                        annotation='Aura Carver landscape; Photos seeded with Example29, Example27, Example24, NightStreet and Sunset only',
                        transformation='lossless WebP; decoded pixels equal the capture'))
    target, framed, share, base_framed, base_screen = reframe(spotlight(image, regions), 'build154-aura-spot-phone-%s.webp' % step)
    entries.append(dict(file=target.name, kind='annotated-screenshot-device-presentation', width=framed.width, height=framed.height,
                        source=plain.name, sourceSha256=sha(plain), sha256=sha(target), build=154, sourceCommit=COMMIT, device=DEVICE,
                        annotation='Outside %s dimmed (black, 59%%); outlined in Sky #35B6E8' % (regions,),
                        presentation='Apple Frames bezel reused from %s (frames-cli v1.5.0, Apple Frames 4.0.2): the screen pixels '
                                     'that matched %s exactly (%.1f%% of the screen) were replaced; bezel pixels kept; no resampling.'
                                     % (base_framed, base_screen, share * 100),
                        frameBaseSha256=sha(DEST / base_framed)))
    print(target.name, framed.size, '%.4f' % share)

story = Image.open(a.story).convert('RGB')
target = save(story, 'oct09-story.webp')
entries.append(dict(file=target.name, kind='native-render', width=story.width, height=story.height, source=a.story.name,
                    sourceSha256=sha(a.story), sha256=sha(target), sourceCommit=COMMIT,
                    renderer='scripts/render_decks_story.swift',
                    annotation='Example26 on a soft 9:16 background; title in Georgia Italic, centered between the photo border and the page edge'))
print(target.name, story.size)

names = {e['file'] for e in entries}
manifest['images'] = [i for i in manifest['images'] if i['file'] not in names] + entries
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
print('Wrote %d assets' % len(entries))
