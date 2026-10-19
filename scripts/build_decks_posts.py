#!/usr/bin/env python3
"""Compose the ten Decks feature posts from native renders and simulator captures.

Inputs, all under social/decks/ (see posts.json):
  renders/post-NN/<id>[-page-K].png   finished pages from scripts/render_decks_posts.swift
  captures/<name>.png                  screens from SocialFeaturePostsUITests (photo-importer-details)

Finished pages are used exactly as rendered: no text, no resampling when the render already
matches the post size. Screen slides put the capture in a phone or tablet body on the Decks
stone-paper ground with one plain line naming the control, set in the margin. Story frames keep
all text out of the top and bottom 155 px. Output goes to social/decks/post-NN/slide-N.png,
outside site/, so it is never deployed.

    python3 scripts/build_decks_posts.py [--root social/decks]
"""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SCALE = 2
STORY_CLEAR = 155

# Decks site tokens (site/decks/assets/site.css).
BG, SURFACE, INK, MUTED = '#f5f4f0', '#eae8e2', '#242422', '#60605b'
SF = '/System/Library/Fonts/SFNS.ttf'

# One entry per slide, in posting order. ('render', id) uses every page of that render in order;
# ('screen', capture, line[, (top, bottom)]) places a capture, or only that band of it (shares of its
# height) at a readable size; ('row', [ids], line) sets finished pages side by side.
SLIDES = {
    1: [('render', 'hero'),
        ('screen', 'home-ig-post', 'Choose where the photos are going, then a layout.'),
        ('screen', 'pages-layout-panel', 'Every page on one screen before you create the project.', (0.36, 0.87)),
        ('row', ['set-1', 'set-2', 'set-3'], 'One layout, used across a set.')],
    2: [('render', 'smart'),
        ('screen', 'smart-pages-strip', 'Vertical photos get their own pages. Horizontal photos share one.'),
        ('screen', 'smart-split-join', 'Split a shared page, or join it with the next.', (0.40, 0.84))],
    3: [('render', 'fill-frame'), ('render', 'white-border'), ('render', 'black-border'), ('render', 'depth'),
        ('screen', 'frame-panel', 'Frame. Border, frame color and background.', (0.45, 0.87))],
    4: [('render', 'template'),
        ('screen', 'save-as-template', 'Save as Template.'),
        ('screen', 'templates-tab', 'Your templates, ready for the next set.')],
    5: [('render', 'pano'),
        ('screen', 'panorama-editor', 'The panel count comes from the photo’s width.')],
    6: [('render', 'threads-pano'),
        ('screen', 'home-threads', 'Choose Threads on Home for the panorama shapes.', (0.12, 0.55))],
    7: [('render', 'story'),
        ('screen', 'home-ig-story', 'Choose IG Story on Home.'),
        ('screen', 'story-editor-background', 'Background, behind the photo and its border.', (0.54, 0.90))],
    8: [('render', 'wall-label'), ('render', 'gear-band'), ('render', 'fuji-recipe'),
        ('screen', 'camera-panel', 'Camera details come from the photo’s metadata.', (0.44, 0.90)),
        ('screen', 'lens-rename', 'Rename a lens once. The EXIF data is not changed.', (0.08, 0.52))],
    9: [('render', 'stamped'),
        ('screen', 'stamp-panel', 'Stamp. Choose a style and the lines it prints.', (0.50, 0.90)),
        ('screen', 'place-editor', 'Name the place. Only the stamp changes.', (0.08, 0.61))],
    10: [('screen', 'devices-mac', 'Mac.'),
         ('screen', 'devices-ipad', 'iPad.'),
         ('screen', 'devices-iphone', 'iPhone.')],
}


def px(v):
    return int(round(v * SCALE))


_FONTS = {}


def font(size, weight=500):
    key = (size, weight)
    if key not in _FONTS:
        face = ImageFont.truetype(SF, px(size))
        # SF Pro's axes are Width, Optical Size, GRAD, Weight, in that order.
        values = {b'Width': 100, b'Optical Size': max(17, min(96, size)), b'GRAD': 400, b'Weight': weight}
        face.set_variation_by_axes([values[a['name']] for a in face.get_variation_axes()])
        _FONTS[key] = face
    return _FONTS[key]


def wrap(text, face, width):
    lines, line = [], ''
    for word in text.split():
        trial = f'{line} {word}'.strip()
        if face.getlength(trial) <= px(width) or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + ([line] if line else [])


def rounded(image, size, radius):
    image = image.convert('RGBA').resize(size, Image.Resampling.LANCZOS)
    mask = Image.new('L', size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius, fill=255)
    image.putalpha(mask)
    return image


def device(shot, screen_w, corner):
    """Dark shell, bright rim, inset screen; corner is the screen radius as a share of width."""
    screen_h = int(round(screen_w * shot.height / shot.width))
    radius = px(screen_w * corner)
    screen = rounded(shot, (px(screen_w), px(screen_h)), radius)
    bezel = px(11)
    body = Image.new('RGBA', (screen.width + bezel * 2, screen.height + bezel * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(body)
    d.rounded_rectangle((0, 0, body.width - 1, body.height - 1), radius + bezel, fill='#0a0a0c',
                        outline='#4a4c52', width=px(1.5))
    body.alpha_composite(screen, (bezel, bezel))
    return body


def drop(canvas, layer, x, y, lift=24, opacity=0.28, spread=36):
    shadow = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    silhouette = Image.new('RGBA', layer.size, (0, 0, 0, 255))
    silhouette.putalpha(layer.getchannel('A').point(lambda v: int(v * opacity)))
    shadow.alpha_composite(silhouette, (x, y + px(lift)))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(px(spread))))
    canvas.alpha_composite(layer, (x, y))


def caption_block(canvas, text, top, width_pt):
    """One plain line (wrapped if needed), centered, starting at `top` in points. Returns its bottom."""
    face = font(38, 500)
    draw = ImageDraw.Draw(canvas)
    y = top
    for line in wrap(text, face, width_pt):
        w = face.getlength(line)
        draw.text(((canvas.width - w) / 2, px(y)), line, font=face, fill=INK)
        y += 50
    return y


def fragment(shot, width_pt):
    """A band of a screen, shown large: rounded corners and the device's dark rim, no full body."""
    height_pt = width_pt * shot.height / shot.width
    radius = px(width_pt * 0.04)
    screen = rounded(shot, (px(width_pt), px(height_pt)), radius)
    rim = px(6)
    body = Image.new('RGBA', (screen.width + rim * 2, screen.height + rim * 2), (0, 0, 0, 0))
    ImageDraw.Draw(body).rounded_rectangle((0, 0, body.width - 1, body.height - 1), radius + rim,
                                           fill='#0a0a0c', outline='#4a4c52', width=px(1.5))
    body.alpha_composite(screen, (rim, rim))
    return body


def screen_slide(shot, line, size, story, crop=None):
    W, H = size
    canvas = Image.new('RGBA', (px(W), px(H)), BG)
    top = (STORY_CLEAR + 60) if story else 84
    bottom_clear = (STORY_CLEAR + 50) if story else 70
    text_bottom = caption_block(canvas, line, top, W - 160)
    area_top = text_bottom + 44
    area_h = H - bottom_clear - area_top
    if crop:
        shot = shot.crop((0, round(shot.height * crop[0]), shot.width, round(shot.height * crop[1])))
        body = fragment(shot, min(W - 120, area_h * shot.width / shot.height) - 16)
    else:
        landscape = shot.width > shot.height
        area_w = W - (80 if landscape else 160)
        corner = 0.03 if landscape else 0.088
        # Fit the device into the area left under the line.
        screen_w = min(area_w, area_h * shot.width / shot.height) - 24
        body = device(shot, screen_w, corner)
    x = (canvas.width - body.width) // 2
    y = px(area_top) + (px(area_h) - body.height) // 2
    drop(canvas, body, x, y)
    return canvas.convert('RGB').resize((W, H), Image.Resampling.LANCZOS)


def row_slide(pages, line, size):
    W, H = size
    canvas = Image.new('RGBA', (px(W), px(H)), BG)
    gap, side = 22, 60
    each_w = (W - side * 2 - gap * (len(pages) - 1)) / len(pages)
    each_h = each_w * pages[0].height / pages[0].width
    y = (H - each_h) / 2 + 40
    for i, page in enumerate(pages):
        thumb = page.convert('RGBA').resize((px(each_w), px(each_h)), Image.Resampling.LANCZOS)
        drop(canvas, thumb, px(side + i * (each_w + gap)), px(y), lift=10, opacity=0.18, spread=18)
    caption_block(canvas, line, y - 120, W - 160)
    return canvas.convert('RGB').resize((W, H), Image.Resampling.LANCZOS)


def finished(page, size):
    """A finished page as rendered. Pages at the post size pass through untouched."""
    if page.size == tuple(size):
        return page.convert('RGB')
    # Threads panels and other shapes keep their own ratio; only shrink, never enlarge.
    assert page.width >= size[0] or page.height >= size[1], 'would enlarge a render'
    return page.convert('RGB')


def pages_for(renders, n, render_id):
    folder = renders / f'post-{n:02d}'
    exact = folder / f'{render_id}.png'
    if exact.exists():
        return [exact]
    pages = sorted(folder.glob(f'{render_id}-page-*.png'),
                   key=lambda p: int(p.stem.rsplit('-', 1)[1]))
    return pages


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--root', type=Path, default=ROOT / 'social/decks')
    args = parser.parse_args()
    spec = json.loads((args.root / 'posts.json').read_text())
    renders, captures = args.root / 'renders', args.root / 'captures'
    missing, report = [], []
    for post in spec['posts']:
        n, size, story = post['n'], post['size'], post['channel'] == 'ig-story'
        out = args.root / f'post-{n:02d}'
        out.mkdir(parents=True, exist_ok=True)
        for old in out.glob('slide-*.png'):
            old.unlink()
        slides = []
        for kind, *rest in SLIDES[n]:
            if kind == 'render':
                pages = pages_for(renders, n, rest[0])
                if not pages:
                    missing.append(f'post {n}: render {rest[0]}')
                slides += [finished(Image.open(p), size) for p in pages]
            elif kind == 'row':
                ids, line = rest
                pages = [p for i in ids for p in pages_for(renders, n, i)[:1]]
                if len(pages) != len(ids):
                    missing.append(f'post {n}: row {ids}')
                    continue
                slides.append(row_slide([Image.open(p) for p in pages], line, (1080, 1350)))
            else:
                name, line, *crop = rest
                shot = captures / f'{name}.png'
                if not shot.exists():
                    missing.append(f'post {n}: capture {name}')
                    continue
                # Threads screens use the feed's 4:5 so they sit beside the panels at a readable size.
                frame_size = (1080, 1920) if story else (1080, 1350)
                slides.append(screen_slide(Image.open(shot), line, frame_size, story, crop[0] if crop else None))
        for i, slide in enumerate(slides, 1):
            target = out / f'slide-{i}.png'
            slide.save(target, optimize=True)
            report.append(f'{slide.width}x{slide.height}  {target.relative_to(args.root)}')
    print('\n'.join(report))
    if missing:
        print('\nMissing inputs:\n  ' + '\n  '.join(missing))


if __name__ == '__main__':
    main()
