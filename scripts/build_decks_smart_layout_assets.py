#!/usr/bin/env python3
"""Package the October 8 Smart Layout captures for the Aura page and guide.

Inputs are the exported XCTest attachments from
SocialDestinationUITests.testSmartLayoutWebsiteCaptures (iPhone and iPad runs)
and the finished pages that test saved to the simulator's Photos. Screenshots
become lossless WebP at their original pixel size; device presentations use
viticci/frames-cli v1.5.0 with the Apple Frames 4.0.2 asset pack, as in
build_decks_device_frames.py. Records go into oct06-assets.json, which the help
builder reads for image dimensions.

  --phone/--pad   folders from `xcrun xcresulttool export attachments`
  --exports       folder holding the saved pair and single JPEGs, named
                  pair.jpg and single.jpg
  --share         Brian's iPhone screenshot of the share sheet with Aura. The
                  suggested-contacts row is pixelated and blurred here, so the
                  unblurred original never enters the repository.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'site/decks/assets'
p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument('--phone', required=True, type=Path)
p.add_argument('--pad', type=Path)
p.add_argument('--exports', required=True, type=Path)
p.add_argument('--cli', required=True, type=Path)
p.add_argument('--assets', required=True, type=Path)
p.add_argument('--share', type=Path)
p.add_argument('--build', default='132')
a = p.parse_args()
sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
version = subprocess.check_output([str(a.cli), '--version'], text=True).strip()
commit = subprocess.check_output(['git', '-C', str(a.cli.parent), 'rev-parse', 'HEAD'], text=True).strip()
manifest_path = DEST / 'oct06-assets.json'
manifest = json.loads(manifest_path.read_text())
entries = []

def attachments(folder):
    index = json.loads((folder / 'manifest.json').read_text())
    return {item['suggestedHumanReadableName'].split('_')[0]: folder / item['exportedFileName']
            for test in index for item in test['attachments']}

def lossless(image, target):
    image.save(target, 'WEBP', lossless=True, exact=True)
    assert Image.open(target).convert(image.mode).tobytes() == image.tobytes(), target

# Steps the pages use. Only screenshots that appear on the site are packaged.
JOBS = {
    'phone': (['1-frame', '2-select', '3-groups', '4-swap-selected', '5-swapped', '6-styles', '7-editor',
               '8-editor-single'], 'iPhone 17 Pro Portrait', 'Silver'),
    'pad': (['3-groups', '5-swapped', '7-editor'], 'iPad Air 2020 Landscape', None),
}
with tempfile.TemporaryDirectory(prefix='decks-smart-layout-') as tmp:
    tmp = Path(tmp)
    for idiom, folder in (('phone', a.phone), ('pad', a.pad)):
        if folder is None:
            continue
        found = attachments(folder)
        steps, device, color = JOBS[idiom]
        for step in steps:
            # On a landscape iPad, XCTest's app screenshot comes back clipped; the full-screen capture is
            # complete but stored sideways with EXIF orientation 8, so store its upright pixels instead.
            source = found[('Web-smart-%s-%s' if idiom == 'phone' else 'Screen-smart-%s-%s') % (idiom, step)]
            original = Image.open(source)
            rotated = original.getexif().get(0x0112, 1) != 1
            capture = ImageOps.exif_transpose(original).convert('RGBA')
            plain = DEST / ('oct08-smart-%s-%s.webp' % (idiom, step))
            lossless(capture, plain)
            entries.append(dict(file=plain.name, kind='native-' + ('iPhone' if idiom == 'phone' else 'iPad'),
                                width=capture.width, height=capture.height, source=str(folder / 'manifest.json') + ' :: ' + step,
                                sourceSha256=sha(source), sha256=sha(plain), build=a.build,
                                test='SocialDestinationUITests.testSmartLayoutWebsiteCaptures',
                                orientation='EXIF orientation applied to store upright pixels; no resampling' if rotated
                                else 'stored upright; no rotation or resampling'))
            staged = tmp / ('%s-%s.png' % (idiom, step))
            capture.save(staged)
            command = [str(a.cli), '--assets', str(a.assets), '--json', 'frame', '-d', device, '-o', str(tmp / 'out')]
            if color:
                command += ['-c', color]
            subprocess.run(command + [str(staged)], check=True, stdout=subprocess.DEVNULL)
            framed = Image.open(tmp / 'out' / (staged.stem + '_framed.png')).convert('RGBA')
            target = DEST / ('oct08-smart-framed-%s-%s.webp' % (idiom, step))
            lossless(framed, target)
            frame_asset = a.assets / (device + (' ' + color if color else '') + '.png')
            entries.append(dict(file=target.name, kind='native-screenshot-device-presentation', width=framed.width,
                                height=framed.height, source=plain.name, sourceSha256=sha(plain), sha256=sha(target),
                                framingTool='https://github.com/viticci/frames-cli', framingVersion=version,
                                framingCommit=commit, device=device, color=color,
                                orientation='upright input; no rotation or screenshot resampling',
                                presentation='Original capture with device bezel and hardware mask.',
                                screenPadding=None, frameAssetSha256=sha(frame_asset)))
    if a.share:
        # The row between the share sheet's first two dividers holds people: faces, initials, names.
        CONTACTS = (0, 577, 1320, 963)
        shot = Image.open(a.share).convert('RGB')
        assert shot.size == (1320, 2868), shot.size
        row = shot.crop(CONTACTS)
        row = row.resize((row.width // 40, row.height // 40), Image.BILINEAR).resize(row.size, Image.BILINEAR)
        shot.paste(row.filter(ImageFilter.GaussianBlur(40)), CONTACTS)
        shot = shot.convert('RGBA')
        plain = DEST / 'oct08-smart-phone-share-aura.webp'
        lossless(shot, plain)
        entries.append(dict(file=plain.name, kind='device-screenshot', width=shot.width, height=shot.height,
                            source="Brian's iPhone share sheet (not stored)", sourceSha256=sha(a.share), sha256=sha(plain),
                            transformation='Suggested-contacts row %s pixelated (1/40) and Gaussian-blurred (40 px); nothing else changed' % (CONTACTS,)))
        device, color = 'iPhone 17 Pro Max Portrait', 'Silver'
        staged = tmp / 'share.png'
        shot.save(staged)
        subprocess.run([str(a.cli), '--assets', str(a.assets), '--json', 'frame', '-d', device, '-c', color, '-o', str(tmp / 'out'), str(staged)],
                       check=True, stdout=subprocess.DEVNULL)
        framed = Image.open(tmp / 'out' / 'share_framed.png').convert('RGBA')
        target = DEST / 'oct08-smart-framed-phone-share-aura.webp'
        lossless(framed, target)
        entries.append(dict(file=target.name, kind='native-screenshot-device-presentation', width=framed.width,
                            height=framed.height, source=plain.name, sourceSha256=sha(plain), sha256=sha(target),
                            framingTool='https://github.com/viticci/frames-cli', framingVersion=version,
                            framingCommit=commit, device=device, color=color,
                            orientation='upright input; no rotation or screenshot resampling',
                            presentation='Original capture with device bezel and hardware mask.',
                            screenPadding=None, frameAssetSha256=sha(a.assets / (device + ' ' + color + '.png'))))
    for name in ('pair', 'single'):
        source = a.exports / (name + '.jpg')
        image = Image.open(source).convert('RGB')
        target = DEST / ('oct08-smart-aura-%s.webp' % name)
        lossless(image, target)
        entries.append(dict(file=target.name, kind='native-export', width=image.width, height=image.height,
                            source='Decks Save to Photos from the iPhone capture run', sourceSha256=sha(source),
                            sha256=sha(target), build=a.build,
                            transformation='JPEG export decoded to RGB and stored as lossless WebP; no resampling'))

names = {entry['file'] for entry in entries}
manifest['images'] = [item for item in manifest['images'] if item['file'] not in names] + entries
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
print('Wrote %d assets' % len(entries))
