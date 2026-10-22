#!/usr/bin/env python3
"""Package the Valet Notes website captures.

Pass the exported XCTest attachment folders for iPhone and iPad and the Mac drawer window
capture. Every capture becomes a lossless WebP whose decoded pixels equal the upright source.
Records go into site/valetnotes/assets/screenshots.json.

Device presentations reuse the Apple Frames bezels already on the Decks site, as
build_decks_build154_assets.py does: the screen pixels that exactly match a known Decks
capture are replaced with the new one and every bezel pixel is kept. iPhone and iPad captures
are the same pixel size as those originals, so nothing is resampled. The Mac drawer spans a
2056-point-wide display, so on the 14-inch frame's 3024 x 1964 screen it is scaled to the
screen width and placed below the menu bar area on a plain desktop. That is the only resampled
presentation, and the manifest says so.

Usage:
  build_valetnotes_assets.py --phone DIR --pad DIR --mac PNG --commit SHA
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'site/valetnotes/assets'
DECKS = ROOT / 'site/decks/assets'
p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
for name in ['phone', 'pad', 'mac']:
    p.add_argument('--' + name, required=True, type=Path)
p.add_argument('--commit', required=True)
a = p.parse_args()
sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
entries = []
TEST = 'WebsiteCaptureUITests.testWebsiteCaptures (capture-only test in an exported copy of the source)'


def save(image, name):
    target = DEST / name
    image.save(target, 'WEBP', lossless=True, exact=True)
    assert Image.open(target).convert(image.mode).tobytes() == image.tobytes(), name
    return target


def by_name(folder):
    names = {}
    for test in json.loads((folder / 'manifest.json').read_text()):
        for item in test['attachments']:
            names[item['suggestedHumanReadableName'].split('_0_')[0]] = folder / item['exportedFileName']
    return names


def capture(source, name, device, rotate=0):
    image = Image.open(source).convert('RGB')
    if rotate:  # XCUIScreen stores landscape iPad screenshots in portrait pixel order.
        image = image.rotate(rotate, expand=True)
    target = save(image, name)
    entries.append(dict(file=name, kind='native-screenshot', width=image.width, height=image.height,
                        source=source.name, sourceSha256=sha(source), sha256=sha(target), sourceCommit=a.commit,
                        test=TEST, device=device,
                        transformation='lossless WebP; decoded pixels equal the upright capture'
                        + ('; rotated %d degrees to upright' % rotate if rotate else '')))
    return image


def reframe(image, base_framed, base_screen, name, device, note):
    framed = Image.open(DECKS / base_framed).convert('RGBA')
    old = Image.open(DECKS / base_screen).convert('RGBA')
    if old.size != image.size:  # The Mac screen: the Decks window sat centered on a neutral canvas.
        canvas = Image.new('RGBA', image.size, '#e4e3df')
        canvas.alpha_composite(old, ((image.width - old.width) // 2, (image.height - old.height) // 2))
        old = canvas
    new = image.convert('RGBA')
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
                        sha256=sha(target), device=device, frameBase='decks/assets/' + base_framed,
                        frameBaseSha256=sha(DECKS / base_framed),
                        presentation='Apple Frames bezel reused from the Decks site: the screen pixels that matched %s '
                                     'exactly (%.1f%% of the screen) were replaced; bezel pixels kept. %s'
                                     % (base_screen, share * 100, note)))
    print(name, framed.size, '%.4f' % share)


def mac_screen(drawer):
    """The drawer as it opens at the top of the display, fitted to the 14-inch screen."""
    width, height = 3024, 1964
    scale = width / drawer.width
    menu_bar = 39 * 2  # The panel opens 39 points below the top of the display, clear of the notch.
    screen = Image.new('RGB', (width, height))
    top, bottom = (72, 86, 77), (40, 47, 42)  # Desktop in the app icon's green.
    for y in range(height):
        t = y / (height - 1)
        ImageDraw.Draw(screen).line([(0, y), (width, y)], fill=tuple(round(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    fitted = drawer.convert('RGB').resize((width, round(drawer.height * scale)), Image.Resampling.LANCZOS)
    shadow = Image.new('L', (width, height), 0)
    ImageDraw.Draw(shadow).rectangle([0, menu_bar, width, menu_bar + fitted.height + 18], fill=150)
    screen.paste((18, 22, 19), None, shadow.filter(ImageFilter.GaussianBlur(24)))
    screen.paste(fitted, (0, menu_bar))
    return screen


DEST.mkdir(parents=True, exist_ok=True)
PHONE = ('oct06-framed-phone-camera.webp', 'oct06-phone-camera.webp', 'iPhone 17 Pro (simulator, iOS 27.0)')
PAD = ('oct06-framed-builder.webp', 'oct06-next-ipad-builder-upright.webp', 'iPad Air 11-inch M4 (simulator, iOS 27.0), landscape')
phone = by_name(a.phone)
for shot in ['writing', 'commands', 'send-tasks']:
    image = capture(phone[shot], 'phone-%s.webp' % shot, PHONE[2])
    reframe(image, PHONE[0], PHONE[1], 'framed-phone-%s.webp' % shot, 'iPhone 17 Pro Portrait Silver', 'No resampling.')
pad = by_name(a.pad)
image = capture(pad['writing'], 'pad-writing.webp', PAD[2], rotate=90)
reframe(image, PAD[0], PAD[1], 'framed-pad-writing.webp', 'iPad Air 2020 Landscape', 'No resampling.')

drawer = Image.open(a.mac).convert('RGBA')
target = save(drawer, 'mac-drawer.webp')
entries.append(dict(file=target.name, kind='native-screenshot', width=drawer.width, height=drawer.height, source=a.mac.name,
                    sourceSha256=sha(a.mac), sha256=sha(target), sourceCommit=a.commit,
                    device='Mac (Apple silicon), TopDrawerMac Debug build, 2056-point-wide display',
                    test='screencapture -x -o -l <window> of a separate instance launched with TOP_DRAWER_DATA_DIR and '
                         '-appearanceTheme classic',
                    transformation='lossless WebP; decoded pixels equal the window capture'))
half = drawer.crop((0, 0, drawer.width // 2, drawer.height))
target = save(half, 'mac-drawer-first-spaces.webp')
entries.append(dict(file=target.name, kind='native-screenshot-crop', width=half.width, height=half.height, source='mac-drawer.webp',
                    sha256=sha(target), transformation='left half of mac-drawer.webp, spaces 1 and 2; no resampling'))
reframe(mac_screen(drawer),'oct06-framed-mac.webp', 'oct06-mac.webp', 'framed-mac-drawer.webp', 'MacBook Pro M5 14 Silver',
        'The drawer was scaled from %d to 3024 pixels wide to fit this screen and placed below the menu bar area on a '
        'plain green desktop; no other interface was added.' % drawer.width)

(DEST / 'screenshots.json').write_text(json.dumps(dict(images=entries), indent=2) + '\n')

# Share image: the hero arrangement on the page's paper color, 1200 x 630.
social = Image.new('RGBA', (1200, 630), '#f5f2ea')
for name, share, left, right, bottom in [('framed-mac-drawer.webp', .80, .10, None, .08), ('framed-pad-writing.webp', .46, None, .04, .03),
                                         ('framed-phone-writing.webp', .21, .04, None, .03)]:
    art = Image.open(DEST / name).convert('RGBA')
    width = round(1200 * share)
    art = art.resize((width, round(art.height * width / art.width)), Image.Resampling.LANCZOS)
    x = round(1200 * left) if left is not None else 1200 - width - round(1200 * right)
    social.alpha_composite(art, (x, 630 - art.height - round(630 * bottom)))
social.convert('RGB').save(DEST / 'social.png', optimize=True)
