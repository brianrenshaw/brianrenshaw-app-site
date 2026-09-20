#!/usr/bin/env python3
"""Render 1080x1920 Instagram assets from bundled fonts, icons and screenshots.

Ten posts, Stories size only: nine projects plus a lineup card.
This draft set predates Ingest; it does not include every current homepage project.
Each is a subject on a graded ground: a phone in a bezel for the four released
iOS apps, a plain card for Canceled, stacked windows for Walkthrough, and the
project's own mark for the two blogs and the browser tools, which have no device
to photograph. A post carries its icon and name, the approved MESSAGING.md
headline as a tagline, and its availability and site URL along the bottom.
Everything else belongs in the Instagram caption.

All art is a real app icon or a real native screenshot already in the
repository. Nothing here reaches the network. Output goes to social/instagram/,
outside site/, so it is never deployed and never walked by check_site.py.

    python3 scripts/build_instagram.py
"""
from pathlib import Path
from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
OUT = ROOT / 'social' / 'instagram'
SCALE = 2
W, H = 1080, 1920

# Bundled OFL faces only. Archivo carries [Weight, Width] in that axis order.
FACES = {
    'archivo': ('where-do-we-eat/assets/fonts/Archivo[wdth,wght].ttf', 2),
    'lora': ('reading-habit/assets/fonts/Lora[wght].ttf', 1),
    'cormorant': ('reading-habit/assets/fonts/CormorantGaramond[wght].ttf', 1),
}
_FONTS = {}


def font(family, size, weight=400, width=100):
    key = (family, size, weight, width)
    if key not in _FONTS:
        path, axes = FACES[family]
        face = ImageFont.truetype(str(SITE / path), int(size * SCALE))
        face.set_variation_by_axes([weight, width] if axes == 2 else [weight])
        _FONTS[key] = face
    return _FONTS[key]


def px(value):
    return int(round(value * SCALE))


def draw_text(draw, xy, value, face, fill, tracking=0, center=None):
    """Pillow has no tracking, so track by drawing one glyph at a time."""
    width = sum(face.getlength(c) for c in value) + tracking * SCALE * max(len(value) - 1, 0)
    x = px(center) - width / 2 if center is not None else px(xy[0])
    y = px(xy[1])
    if not tracking:
        draw.text((x, y), value, font=face, fill=fill)
        return width
    for ch in value:
        draw.text((x, y), ch, font=face, fill=fill)
        x += face.getlength(ch) + tracking * SCALE
    return width


def wrap(value, face, max_width):
    lines, line = [], ''
    for word in value.split():
        trial = f'{line} {word}'.strip()
        if face.getlength(trial) <= max_width * SCALE or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def centered_block(draw, y, lines, face, fill, leading):
    for line in lines:
        draw_text(draw, (0, y), line, face, fill, center=W / 2)
        y += leading
    return y


def gradient(top, bottom):
    """Vertical ramp, eased so the transition does not read as a hard band."""
    tr, tg, tb = ImageColor.getrgb(top)
    br, bg, bb = ImageColor.getrgb(bottom)
    height = px(H)
    strip = Image.new('RGB', (1, height))
    pixels = strip.load()
    for y in range(height):
        t = y / (height - 1)
        t = t * t * (3 - 2 * t)
        pixels[0, y] = (round(tr + (br - tr) * t), round(tg + (bg - tg) * t), round(tb + (bb - tb) * t))
    return strip.resize((px(W), height), Image.Resampling.BILINEAR).convert('RGBA')


def glow(canvas, center, radius, color, opacity):
    """A soft light source, so the ground has somewhere to fall away from."""
    cx, cy, r = px(center[0]), px(center[1]), px(radius)
    mask = Image.new('L', canvas.size, 0)
    ImageDraw.Draw(mask).ellipse((cx - r, cy - r, cx + r, cy + r), fill=opacity)
    mask = mask.filter(ImageFilter.GaussianBlur(r * 0.55))
    layer = Image.new('RGBA', canvas.size, ImageColor.getrgb(color) + (255,))
    layer.putalpha(mask)
    canvas.alpha_composite(layer)


def vignette(canvas, strength=40):
    """Darken the corners so the device reads as lit from the middle."""
    mask = Image.new('L', canvas.size, strength)
    inset_x, inset_y = px(W) * 0.10, px(H) * 0.07
    ImageDraw.Draw(mask).ellipse(
        (inset_x, inset_y, px(W) - inset_x, px(H) - inset_y), fill=0)
    mask = mask.filter(ImageFilter.GaussianBlur(px(150)))
    layer = Image.new('RGBA', canvas.size, (0, 0, 0, 255))
    layer.putalpha(mask)
    canvas.alpha_composite(layer)


def rounded(image, size, radius, border=None):
    """Resize and clip to a rounded rect, preserving any existing alpha."""
    image = image.convert('RGBA').resize(size, Image.Resampling.LANCZOS)
    mask = Image.new('L', size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius, fill=255)
    # Multiply rather than replace: Icon Composer exports already carry a shape.
    image.putalpha(Image.composite(image.getchannel('A'), Image.new('L', size, 0), mask))
    if border:
        ImageDraw.Draw(image).rounded_rectangle(
            (0, 0, size[0] - 1, size[1] - 1), radius, outline=border, width=max(SCALE, 2))
    return image


# Lankford Legends, What Did They Read? and Spreadsheet Tools ship only as tiny
# SVGs, which Pillow cannot read, so their marks are redrawn here from the same
# geometry as site/assets/*.svg. build_social.py already draws them this way.
def draw_lankford(size):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = size / 128

    def pts(*p):
        return [(x * s, y * s) for x, y in p]

    d.rounded_rectangle((0, 0, size - 1, size - 1), 28 * s, fill='#FFFFFF')
    d.polygon(pts((64, 12), (116, 64), (64, 116), (12, 64)), fill='#C41E3A',
              outline='#0C2340', width=max(1, round(2 * s)))
    for ox in (42, 66):  # the two white L strokes
        d.polygon(pts((ox, 49), (ox + 6, 49), (ox + 6, 74),
                      (ox + 14, 74), (ox + 14, 80), (ox, 80)), fill='#FFFFFF')
    for cx, cy in ((64, 20), (108, 64), (20, 64)):  # three bases
        d.polygon(pts((cx, cy - 4), (cx + 4, cy), (cx, cy + 4), (cx - 4, cy)), fill='#FFFFFF')
    d.polygon(pts((60, 104), (68, 104), (68, 109), (64, 113), (60, 109)), fill='#FFFFFF')
    return im


def draw_what_did_they_read(size):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = size / 128
    d.rounded_rectangle((0, 0, size - 1, size - 1), 28 * s, fill='#f2efe8')
    width = max(1, round(3 * s))
    for y, x2 in ((40, 68), (58, 68), (76, 68), (94, 54)):
        d.line([(24 * s, y * s), (x2 * s, y * s)], fill='#1a1715', width=width)
    mark = ImageFont.truetype(str(SITE / FACES['lora'][0]), int(76 * s))
    mark.set_variation_by_axes([500])
    d.text((98 * s, 86 * s), '?', font=mark, fill='#8c2b18', anchor='ms')
    return im


def draw_spreadsheet(size):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = size / 60
    d.rounded_rectangle((0, 0, size - 1, size - 1), 13 * s, fill='#f3f8fc')
    width = max(1, round(2 * s))
    d.rounded_rectangle((13 * s, 13 * s, 47 * s, 47 * s), 3 * s, outline='#365e83', width=width)
    for a, b in (((13, 23), (47, 23)), ((13, 35), (47, 35)),
                 ((25, 23), (25, 47)), ((36, 23), (36, 47))):
        d.line([(a[0] * s, a[1] * s), (b[0] * s, b[1] * s)], fill='#365e83', width=width)
    return im


def icon_image(spec, size):
    """An icon is either a PNG in the repo or one of the drawers above."""
    if callable(spec):
        return spec(px(size))
    return rounded(Image.open(SITE / spec), (px(size), px(size)), px(size * ICON_RADIUS))


def open_shot(path, crop_top=0.0):
    source = Image.open(SITE / path)
    if crop_top:
        source = source.crop((0, int(source.height * crop_top), source.width, source.height))
    return source


def phone(shot, screen_w):
    """Put a screenshot in a phone body: dark shell, bright rim, inset screen."""
    screen_h = int(round(screen_w * shot.height / shot.width))
    radius = px(screen_w * 0.088)
    screen = rounded(shot, (px(screen_w), px(screen_h)), radius)

    bezel = px(13)
    body = Image.new('RGBA', (px(screen_w) + bezel * 2, px(screen_h) + bezel * 2), (0, 0, 0, 0))
    edge = ImageDraw.Draw(body)
    edge.rounded_rectangle((0, 0, body.width - 1, body.height - 1), radius + bezel, fill='#0a0a0c')
    # A one-pixel rim catches the light and stops the shell reading as a hole.
    edge.rounded_rectangle((0, 0, body.width - 1, body.height - 1), radius + bezel,
                           outline='#4a4c52', width=px(1.5))
    body.alpha_composite(screen, (bezel, bezel))
    return body


def window(shot, target_w, radius=0.018, border='#4a4c5288'):
    """Walkthrough's captures already carry Mac chrome, so no bezel is added."""
    target_h = int(round(target_w * shot.height / shot.width))
    return rounded(shot, (px(target_w), px(target_h)), px(target_w * radius), border=border)


def place(canvas, device, center, angle, lift=30, opacity=0.62, spread=42):
    """Rotate, drop a soft shadow, composite. The shadow is what sells depth."""
    device = device.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    x = px(center[0]) - device.width // 2
    y = px(center[1]) - device.height // 2

    shadow = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    silhouette = Image.new('RGBA', device.size, (0, 0, 0, 255))
    silhouette.putalpha(device.getchannel('A').point(lambda v: int(v * opacity)))
    shadow.alpha_composite(silhouette, (x, y + px(lift)))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(px(spread))))
    canvas.alpha_composite(device, (x, y))


ICON_RADIUS = 0.224  # The site's icon corner mask. Where Do We Eat's source is square.
LOCKUP_Y = 258       # Clear of the Stories chrome across the top.
FOOT_Y = 1706        # Above the Stories chrome across the bottom.


def drop_icon(canvas, icon, x, y, opacity=0.30, spread=14, lift=9):
    shadow = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    silhouette = Image.new('RGBA', icon.size, (0, 0, 0, 255))
    silhouette.putalpha(icon.getchannel('A').point(lambda v: int(v * opacity)))
    shadow.alpha_composite(silhouette, (px(x), px(y) + px(lift)))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(px(spread))))
    canvas.alpha_composite(icon, (px(x), px(y)))


def lockup(canvas, draw, icon_spec, name, tagline, ink, size=98):
    """Icon and name on one line, then the approved headline beneath it."""
    icon = icon_image(icon_spec, size)
    label = font('archivo', 40, 680)
    gap = 24
    width = size + gap + sum(label.getlength(c) for c in name) / SCALE
    x = (W - width) / 2

    drop_icon(canvas, icon, x, LOCKUP_Y)
    draw_text(draw, (x + size + gap, LOCKUP_Y + size / 2 - 28), name, label, ink)

    face = font('archivo', 37, 450)
    centered_block(draw, LOCKUP_Y + size + 44, wrap(tagline, face, 820), face, ink, 50)


def footing(draw, availability, url, ink, muted):
    draw_text(draw, (0, FOOT_Y), availability, font('archivo', 26, 450), muted, center=W / 2)
    draw_text(draw, (0, FOOT_Y + 42), url, font('archivo', 31, 620), ink,
              tracking=0.4, center=W / 2)


# Gradients stay inside each app's own hue rather than running down to black.
# A warm ground falling to near-black turns muddy once the vignette lands on it.
APPS = [
    {
        'stem': 'folio', 'name': 'Folio',
        'tagline': 'Your HTML reports and dashboards, available offline.',
        'availability': 'Free on the App Store', 'url': 'brianrenshaw.app/folio',
        'foot_ink': '#ffe9d4', 'foot_muted': '#e8b98c',
        'top': '#ffcf9c', 'bottom': '#8f3a02', 'glow': '#ffe6cd', 'ink': '#5a3410',
        'icon': 'folio/assets/icon.png',
        'shot': 'folio/assets/screen-1.webp', 'kind': 'phone',
    },
    {
        'stem': 'whos-first', 'name': 'Who’s First?',
        'tagline': 'Choose who goes first. Get on with the game.',
        'availability': 'Free on the App Store', 'url': 'brianrenshaw.app/whos-first',
        'foot_ink': '#e8f5ef', 'foot_muted': '#a6c8c2',
        'top': '#cbe7d9', 'bottom': '#14494a', 'glow': '#eaf6ef', 'ink': '#123c39',
        'icon': 'whos-first/assets/icon-native.png',
        'shot': 'whos-first/assets/chooser-current.webp', 'kind': 'phone',
    },
    {
        'stem': 'reading-habit', 'name': 'Reading Habit',
        'tagline': 'Make reading a daily habit.',
        'availability': 'Free on the App Store', 'url': 'brianrenshaw.app/reading-habit',
        'foot_ink': '#f8ebc9', 'foot_muted': '#c2ad84',
        'top': '#ebcd85', 'bottom': '#42351f', 'glow': '#f8e9c3', 'ink': '#3d3423',
        'icon': 'reading-habit/assets/icon-native.png',
        'shot': 'reading-habit/assets/screen-journal.webp', 'kind': 'phone',
    },
    {
        'stem': 'where-do-we-eat', 'name': 'Where Do We Eat',
        'tagline': 'Make deciding where to eat easier.',
        'availability': 'Free on the App Store', 'url': 'brianrenshaw.app/where-do-we-eat',
        'foot_ink': '#ffeee5', 'foot_muted': '#f2b9a5',
        'top': '#ffdccb', 'bottom': '#a81c06', 'glow': '#ffefe6', 'ink': '#7c1405',
        'icon': 'where-do-we-eat/assets/app-icon.png',
        'shot': 'where-do-we-eat/assets/work-lunch-decide.png', 'kind': 'phone',
    },
    {
        'stem': 'walkthrough', 'name': 'Walkthrough',
        'tagline': 'Organize photos for a property listing.',
        'availability': 'macOS 14 or later · Apple silicon and Intel', 'url': 'brianrenshaw.app/walkthrough',
        'foot_ink': '#f1efe9', 'foot_muted': '#969ca6',
        # A neutral light, not amber. Amber over charcoal reads as olive mud.
        'top': '#41454c', 'bottom': '#111316', 'glow': '#aab0ba', 'glow_opacity': 46,
        'ink': '#f1efe9',
        'icon': 'walkthrough/assets/icon-1.4.1.png',
        # One landscape window leaves the tall frame half empty, so the two
        # captures are stacked and offset to fill it with depth instead.
        'kind': 'stack', 'stack': [
            ('walkthrough/assets/native-command-palette-1.4.1-retina.webp', 860, (596, 900), -7),
            ('walkthrough/assets/native-contact-sheet-1.4.1-retina.webp', 984, (540, 1330), -3),
        ],
    },
]

APPS += [
    {
        'stem': 'canceled', 'name': 'Canceled',
        'tagline': 'Nobody has to be the one who cancels.',
        # In development. No download, no beta link, no call to action.
        'availability': 'In development', 'url': 'brianrenshaw.app/canceled',
        'top': '#2d5180', 'bottom': '#0d1523', 'glow': '#7ba0cf', 'glow_opacity': 52,
        'ink': '#eaf1f9', 'foot_ink': '#fffdf6', 'foot_muted': '#9fb3cc',
        'icon': 'canceled/assets/icon.png',
        # The Demo mode captures are cropped, so the aspect is not a phone's.
        # Shown as a plain rounded card rather than in a bezel that would lie.
        'shot': 'canceled/assets/invite.png', 'kind': 'card', 'shot_w': 470,
    },
    {
        'stem': 'lankford-legends', 'name': 'Lankford Legends',
        'tagline': 'Catch up on the Cardinals, every day.',
        'availability': 'Cardinals and MLB updates', 'url': 'lankfordlegends.co',
        # Cardinals navy, which is this card's own dark-mode ground.
        'top': '#1c4272', 'bottom': '#081727', 'glow': '#4d7cb0', 'glow_opacity': 54,
        'ink': '#f2f5f8', 'foot_ink': '#ffffff', 'foot_muted': '#a8bdd4',
        'icon': draw_lankford, 'kind': 'icon',
    },
    {
        'stem': 'what-did-they-read', 'name': 'What Did They Read?',
        'tagline': 'Find the books mentioned on podcasts.',
        'availability': 'Books from podcasts', 'url': 'whatdidtheyread.com',
        'top': '#f7e9dc', 'bottom': '#6b2416', 'glow': '#fdf6ee',
        'ink': '#26201c', 'foot_ink': '#f9efe9', 'foot_muted': '#d9a795',
        'icon': draw_what_did_they_read, 'kind': 'icon',
    },
    {
        'stem': 'spreadsheet-tools', 'name': 'Spreadsheet Tools',
        'tagline': 'Make everyday spreadsheet tasks easier.',
        'availability': 'No installation or account needed',
        'url': 'brianrenshaw.app/spreadsheet-tools',
        'top': '#dcebf7', 'bottom': '#25405a', 'glow': '#f2f9ff',
        'ink': '#1f3346', 'foot_ink': '#e9f2fa', 'foot_muted': '#a6bdd1',
        'icon': draw_spreadsheet, 'kind': 'icon',
    },
]

# Homepage order: the iOS apps, the Mac app, the blogs, then the utility.
LINEUP = [
    ('Folio', 'folio/assets/icon.png'),
    ('Who’s First?', 'whos-first/assets/icon-native.png'),
    ('Reading Habit', 'reading-habit/assets/icon-native.png'),
    ('Where Do We Eat', 'where-do-we-eat/assets/app-icon.png'),
    ('Canceled', 'canceled/assets/icon.png'),
    ('Walkthrough', 'walkthrough/assets/icon-1.4.1.png'),
    ('Lankford Legends', draw_lankford),
    ('What Did They Read?', draw_what_did_they_read),
    ('Spreadsheet Tools', draw_spreadsheet),
]


def render_app(app):
    canvas = gradient(app['top'], app['bottom'])
    glow(canvas, (W / 2, 620), 640, app['glow'], app.get('glow_opacity', 70))

    if app['kind'] == 'stack':
        for path, width, center, angle in app['stack']:
            place(canvas, window(open_shot(path), width), center, angle, lift=26, spread=36)
    elif app['kind'] == 'icon':
        # A blog or a browser tool has no device to photograph, so its own mark
        # carries the frame. Squared up, because a tilted flat mark reads as a
        # mistake rather than a photograph.
        place(canvas, icon_image(app['icon'], 520), (W / 2, 1076), 0,
              lift=34, opacity=0.42, spread=46)
    elif app['kind'] == 'card':
        place(canvas, window(open_shot(app['shot']), app['shot_w'],
                             radius=0.05, border='#7d96b8'), (W / 2, 1096), -5)
    else:
        # Sized and centred so the rotated corners clear both the tagline above
        # and the URL below.
        place(canvas, phone(open_shot(app['shot']), 492), (W / 2, 1096), -5)

    vignette(canvas)
    draw = ImageDraw.Draw(canvas)
    lockup(canvas, draw, app['icon'], app['name'], app['tagline'], app['ink'])
    footing(draw, app['availability'], app['url'], app['foot_ink'], app['foot_muted'])
    return canvas


def render_lineup():
    # Paper to a warmer paper, never down to black. A light ground running to
    # dark passes through a long stretch of dead grey in the middle.
    canvas = gradient('#faf8f3', '#d5cfc1')
    glow(canvas, (W / 2, 620), 660, '#ffffff', 90)

    ink, muted = '#1f211f', '#6a675f'
    tile, gap, label_gap = 236, 56, 28
    draw = ImageDraw.Draw(canvas)
    name_face = font('archivo', 23, 600)

    for index, (name, spec) in enumerate(LINEUP):
        row, col = divmod(index, 3)
        x = (W - (3 * tile + 2 * gap)) / 2 + col * (tile + gap)
        y = 626 + row * 330
        place(canvas, icon_image(spec, tile), (x + tile / 2, y + tile / 2), 0,
              lift=20, opacity=0.30, spread=24)
        draw_text(draw, (0, y + tile + label_gap), name, name_face, ink, center=x + tile / 2)

    vignette(canvas, strength=26)
    draw_text(draw, (0, 292), 'brianrenshaw.app', font('archivo', 58, 650), ink,
              tracking=0.5, center=W / 2)
    draw_text(draw, (0, 372), 'Apps, tools and experiments', font('archivo', 29, 450),
              muted, center=W / 2)
    return canvas


def save(canvas, path):
    canvas.convert('RGB').resize((W, H), Image.Resampling.LANCZOS).save(path, optimize=True)
    print(f'{W}x{H}  {path.relative_to(ROOT)}')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for app in APPS:
        save(render_app(app), OUT / f'{app["stem"]}.png')
    save(render_lineup(), OUT / 'lineup.png')


if __name__ == '__main__':
    main()
