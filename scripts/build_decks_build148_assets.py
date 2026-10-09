#!/usr/bin/env python3
"""Package the Decks build 148 website captures and native renders.

Pass the exported XCTest attachment folders, the Mac window captures and the native render
output. Every capture becomes a lossless WebP whose decoded pixels equal the source (after EXIF
orientation is applied to the sideways landscape iPad screens). Records go into oct06-assets.json.

Device presentations reuse the Apple Frames bezels already on the site (oct06-framed-phone-camera,
oct06-framed-builder, oct06-framed-mac). Each of those was made from a known screenshot, so the
visible screen is exactly the set of pixels where the framed image equals that screenshot; those
pixels are replaced with the new capture and every bezel pixel is kept. New captures have the same
pixel size as the originals, so nothing is resampled.

Usage:
  build_decks_build148_assets.py --phone DIR --phone2 DIR --pad DIR --pad2 DIR --aura-pad DIR \
      --mac DIR --renders DIR
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageOps

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'site/decks/assets'
COMMIT = '42c30ae'
p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
for name in ['phone', 'phone2', 'pad', 'pad2', 'aura-pad', 'mac', 'renders']:
    p.add_argument('--' + name, required=True, type=Path)
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

def upright(path):
    raw = Image.open(path)
    oriented = ImageOps.exif_transpose(raw).convert('RGB')
    return oriented, raw.getexif().get(274)

def capture(source, name, test, device, note=None):
    image, orientation = upright(source)
    target = save(image, name)
    entry = dict(file=name, kind='native-screenshot', width=image.width, height=image.height,
                 source=source.name, sourceSha256=sha(source), sha256=sha(target), build=148,
                 sourceCommit=COMMIT, test=test, device=device,
                 orientation='EXIF orientation %s applied; upright pixels stored' % orientation if orientation not in (None, 1)
                 else 'stored as captured', transformation='lossless WebP; decoded pixels equal the upright capture')
    if note:
        entry['annotation'] = note
    entries.append(entry)
    return image

def reframe(image, base_framed, base_screen, name, device, source_name, canvas=None):
    framed = Image.open(DEST / base_framed).convert('RGBA')
    old = Image.open(DEST / base_screen).convert('RGBA')
    new = image.convert('RGBA')
    if canvas:  # Mac: the window sits centered on a neutral screen canvas.
        def centered(window):
            c = Image.new('RGBA', canvas, '#e4e3df')
            c.alpha_composite(window, ((canvas[0] - window.width) // 2, (canvas[1] - window.height) // 2))
            return c
        old, new = centered(old), centered(new)
    assert old.size == new.size, (name, old.size, new.size)
    # The screen is near the center; find the exact offset where the old capture matches.
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
                        source=source_name, sha256=sha(target), build=148, sourceCommit=COMMIT, device=device,
                        presentation='Apple Frames bezel reused from %s (frames-cli v1.5.0, Apple Frames 4.0.2): the screen pixels '
                                     'that matched %s exactly (%.1f%% of the screen) were replaced with this capture; bezel pixels kept; '
                                     'no resampling.' % (base_framed, base_screen, share * 100),
                        frameBaseSha256=sha(DEST / base_framed)))
    print(name, framed.size, '%.4f' % share)

PHONE = ('oct06-framed-phone-camera.webp', 'oct06-phone-camera.webp', 'iPhone 17 Pro (simulator, iOS 27.0)')
PAD = ('oct06-framed-builder.webp', 'oct06-next-ipad-builder-upright.webp', 'iPad Air 11-inch M3 (simulator, iOS 27.0), landscape')
T1 = 'SocialWebsiteBuild148UITests.testWebsiteHomePagesAndEditor'
T2 = 'SocialWebsiteBuild148UITests.testWebsiteTemplatesAndSmartLayoutBuilder'
T3 = 'SocialWebsiteBuild148UITests.testWebsiteDesignCameraDetailsAndStamp'
TA = 'SocialDestinationUITests.testSmartLayoutWebsiteCaptures'

phone_jobs = [
    (a.phone, 'Web148-phone-01-home.png', 'home', T1),
    (a.phone, 'Web148-phone-02-home-designs.png', 'designs', T1),
    (a.phone, 'Web148-phone-04-pages.png', 'pages', T1),
    (a.phone, 'Web148-phone-05-layout-panel.png', 'layout-panel', T1),
    (a.phone, 'Web148-phone-06-split.png', 'split', T1),
    (a.phone, 'Web148-phone-11-stamp.png', 'stamp', T1),
    (a.phone, 'Web148-phone-12-stamp-date.png', 'stamp-date', T1),
    (a.phone, 'Web148-phone-22-builder-my-photos.png', 'builder', T2),
    (a.phone, 'Web148-phone-24-templates-smart.png', 'templates', T2),
    (a.phone2, 'Web148-phone-32-details-card.png', 'details-card', T3),
]
for folder, file, slug, test in phone_jobs:
    image = capture(folder / file, 'build148-phone-%s.webp' % slug, test, PHONE[2])
    reframe(image, PHONE[0], PHONE[1], 'build148-framed-phone-%s.webp' % slug, 'iPhone 17 Pro Portrait Silver', file)

pad_jobs = [
    (a.pad, 'Screen148-pad-01-home.png', 'home', T1),
    (a.pad, 'Screen148-pad-05-layout-panel.png', 'layout-panel', T1),
    (a.pad2, 'Screen148-pad-32-details-card.png', 'details-card', T3),
]
for folder, file, slug, test in pad_jobs:
    image = capture(folder / file, 'build148-pad-%s.webp' % slug, test, PAD[2])
    reframe(image, PAD[0], PAD[1], 'build148-framed-pad-%s.webp' % slug, 'iPad Air 2020 Landscape', file)

for step in ['1-frame', '2b-pages', '3-groups', '4-swap-selected', '5-swapped', '7-editor']:
    file = 'Screen-smart-pad-%s.png' % step
    image = capture(a.aura_pad / file, 'build148-aura-pad-%s.webp' % step, TA, PAD[2],
                    'Aura Carver landscape; Photos seeded with Example29, Example27, Example24, NightStreet and Sunset only')
    reframe(image, PAD[0], PAD[1], 'build148-aura-framed-pad-%s.webp' % step, 'iPad Air 2020 Landscape', file)

for slug in ['home', 'smart-builder']:
    file = a.mac / ('mac-%s.png' % slug)
    image = Image.open(file).convert('RGBA')
    target = save(image, 'build148-mac-%s.webp' % slug)
    entries.append(dict(file=target.name, kind='native-screenshot', width=image.width, height=image.height, source=file.name,
                        sourceSha256=sha(file), sha256=sha(target), build=148, sourceCommit=COMMIT,
                        device='Mac (Apple silicon), DecksMac Debug build from %s' % COMMIT,
                        test='screencapture -o -l <window> of an isolated --social-probe-run store; built-in sample photos only',
                        transformation='lossless WebP; decoded pixels equal the window capture'))
    reframe(image, 'oct06-framed-mac.webp', 'oct06-mac.webp', 'build148-framed-mac-%s.webp' % slug, 'MacBook Pro M5 14 Silver',
            file.name, canvas=(3024, 1964))

renders = {
    'stamp-digital': 'Example40.jpg, Digital date stamp with its capture date',
    'stamp-clean': 'Coffee.jpg, Clean date stamp with capture date and time',
    'stamp-typewriter-sideways': 'Burger.jpg, Typewriter date stamp, Sideways on Vertical Photos',
    'design-gear-band': 'Example27.jpg, Gear Band design',
    'design-wall-label': 'Example29.jpg, Wall Label design',
    'design-spec-sheet': 'original DSCF0205.JPG, Spec Sheet design with its recorded Classic Negative recipe (Dials)',
    'design-spine': 'Example24.jpg, Spine design',
}
for slug, note in renders.items():
    file = a.renders / (slug + '.png')
    image = Image.open(file)
    image = image.convert('RGBA' if 'A' in image.getbands() else 'RGB')
    target = save(image, 'build148-%s.webp' % slug)
    entries.append(dict(file=target.name, kind='native-render', width=image.width, height=image.height, source=file.name,
                        sourceSha256=sha(file), sha256=sha(target), build=148, rendererCommit=COMMIT,
                        renderer='scripts/render_decks_build148.swift (IngestSocialKit SocialRenderService)',
                        projectSha256=sha(a.renders / (slug + '.json')), annotation=note,
                        transformation='lossless WebP; decoded pixels equal the native PNG'))

names = {e['file'] for e in entries}
manifest['images'] = [i for i in manifest['images'] if i['file'] not in names] + entries
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
print('Wrote %d assets' % len(entries))
