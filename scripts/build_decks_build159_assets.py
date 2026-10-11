#!/usr/bin/env python3
"""Package the Decks build 159 website captures: an Instagram smart layout's Layout screen, and the
four-screen first-run tour.

Pass the exported XCTest attachment folders (xcresulttool export attachments). Every capture
becomes a lossless WebP whose decoded pixels equal the source; records go into oct06-assets.json.
Phone presentations reuse the Apple Frames bezel already on the site (oct06-framed-phone-camera):
the screen pixels that match its known screenshot are replaced with the new capture and every bezel
pixel is kept, so nothing is resampled.

Usage:
  build_decks_build159_assets.py --layout DIR --tour DIR
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'site/decks/assets'
p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument('--layout', required=True, type=Path)
p.add_argument('--tour', required=True, type=Path)
p.add_argument('--commit', required=True)
a = p.parse_args()
sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
manifest_path = DEST / 'oct06-assets.json'
manifest = json.loads(manifest_path.read_text())
entries = []
DEVICE = 'iPhone 17 Pro (simulator, iOS 27.0)'
PHONE = ('oct06-framed-phone-camera.webp', 'oct06-phone-camera.webp')


def save(image, name):
    target = DEST / name
    image.save(target, 'WEBP', lossless=True, exact=True)
    assert Image.open(target).convert(image.mode).tobytes() == image.tobytes(), name
    return target


def capture(source, name, test, note):
    image = Image.open(source).convert('RGB')
    target = save(image, name)
    entries.append(dict(file=name, kind='native-screenshot', width=image.width, height=image.height,
                        source=source.name, sourceSha256=sha(source), sha256=sha(target), build=159,
                        sourceCommit=a.commit, test=test, device=DEVICE, annotation=note,
                        transformation='lossless WebP; decoded pixels equal the capture'))
    return image


def reframe(image, name, source_name):
    framed = Image.open(DEST / PHONE[0]).convert('RGBA')
    old = Image.open(DEST / PHONE[1]).convert('RGBA')
    new = image.convert('RGBA')
    assert old.size == new.size, (name, old.size, new.size)
    cx, cy = (framed.width - old.width) // 2, (framed.height - old.height) // 2
    def matches(offset):
        crop = framed.crop((offset[0], offset[1], offset[0] + old.width, offset[1] + old.height)).convert('RGB')
        return ImageChops.difference(crop, old.convert('RGB')).convert('L').histogram()[0]
    ox, oy = max(((x, y) for x in range(cx - 3, cx + 4) for y in range(cy - 3, cy + 4)), key=matches)
    region = framed.crop((ox, oy, ox + old.width, oy + old.height))
    diff = ImageChops.difference(region.convert('RGB'), old.convert('RGB')).convert('L')
    screen = diff.point(lambda v: 255 if v == 0 else 0)
    alpha = region.getchannel('A').point(lambda v: 255 if v == 255 else 0)
    mask = ImageChops.multiply(screen, alpha)
    share = sum(mask.histogram()[255:]) / (old.width * old.height)
    assert share > 0.9, (name, share)
    region.paste(new, (0, 0), mask)
    framed.paste(region, (ox, oy))
    target = save(framed, name)
    entries.append(dict(file=name, kind='native-screenshot-device-presentation', width=framed.width, height=framed.height,
                        source=source_name, sha256=sha(target), build=159, sourceCommit=a.commit,
                        device='iPhone 17 Pro Portrait Silver',
                        presentation='Apple Frames bezel reused from %s: the screen pixels that matched %s exactly '
                                     '(%.1f%% of the screen) were replaced with this capture; bezel pixels kept; no resampling.'
                                     % (PHONE[0], PHONE[1], share * 100),
                        frameBaseSha256=sha(DEST / PHONE[0])))
    print(name, framed.size, '%.4f' % share)


def by_name(folder):
    names = {}
    for test in json.loads((folder / 'manifest.json').read_text()):
        for item in test['attachments']:
            names[item['suggestedHumanReadableName'].split('_0_')[0]] = folder / item['exportedFileName']
    return names


layout = by_name(a.layout)
TL = 'SocialSmartLayoutScreenUITests.testInstagramSmartLayoutOpensOnItsGroups'
PHOTOS = 'IG Post, Singles & Pairs; Photos seeded with Example03, Example24, Coastline, Example27, Example25 and Example26'
for shot, slug in [('Instagram Smart Layout groups', 'layout-groups')]:
    image = capture(layout[shot], 'build159-phone-%s.webp' % slug, TL, PHOTOS)
    reframe(image, 'build159-framed-phone-%s.webp' % slug, layout[shot].name)

tour = by_name(a.tour)
TT = 'IngestSocialUITests.testIntroductionSectionsAndReplay'
for index in range(1, 5):
    shot = 'Tour screen %d' % index
    image = capture(tour[shot], 'build159-phone-tour-%d.webp' % index, TT, 'First-run tour, screen %d of 4' % index)
    reframe(image, 'build159-framed-phone-tour-%d.webp' % index, tour[shot].name)

files = {entry['file'] for entry in entries}
manifest['images'] = [item for item in manifest['images'] if item['file'] not in files] + entries
manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
print('recorded', len(entries))
