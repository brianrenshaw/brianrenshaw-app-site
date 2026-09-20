#!/usr/bin/env python3
"""Concept round: posts designed around each product's own idea, not a template.

Three registers, deliberately unlike each other, so the direction can be judged
before it is rolled out to all ten:

  walkthrough  a typographic data poster. The room order IS the product.
  reading-habit  a habit grid. The mechanic drawn, not described.
  canceled  the app's own voice and motifs, quoted verbatim.

Reuses the helpers in build_instagram.py. Writes to social/instagram/concepts/.

    python3 scripts/build_instagram_concepts.py
"""
from PIL import Image, ImageDraw, ImageFilter

from build_instagram import (
    FOOT_Y, LOCKUP_Y, OUT, W, centered_block, draw_text, font, footing,
    gradient, glow, icon_image, lockup, px, vignette, wrap,
)

CONCEPTS = OUT / 'concepts'


def right_text(draw, right, y, value, face, fill):
    """build_instagram.draw_text centres or left-aligns; this pins to a right edge."""
    width = sum(face.getlength(c) for c in value) / SCALE_ONE
    draw_text(draw, (right - width, y), value, face, fill)


def tick(draw, x, y, size, color, width):
    """A check mark drawn from two strokes, so no font has to carry the glyph."""
    draw.line([(px(x + size * 0.18), px(y + size * 0.54)),
               (px(x + size * 0.41), px(y + size * 0.78)),
               (px(x + size * 0.84), px(y + size * 0.24))],
              fill=color, width=px(width), joint='curve')


def stamp(canvas, text, center, angle, color, size, pad=26):
    """The rotated CANCELED stamp: boxed, tracked, rubber-stamped on an angle."""
    face = font('archivo', size, 900)
    tracking = 6
    width = sum(face.getlength(c) for c in text) / SCALE_ONE + tracking * (len(text) - 1)
    layer = Image.new('RGBA', (px(width + pad * 2), px(size + pad * 1.7)), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((0, 0, layer.width - 1, layer.height - 1), px(8),
                        outline=color, width=px(5))
    x = px(pad)
    for ch in text:
        d.text((x, px(pad * 0.55)), ch, font=face, fill=color)
        x += face.getlength(ch) + px(tracking)
    layer = layer.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    canvas.alpha_composite(layer, (px(center[0]) - layer.width // 2,
                                   px(center[1]) - layer.height // 2))


SCALE_ONE = 2  # build_instagram renders at 2x; face.getlength returns device px.


# ---------------------------------------------------------------- Walkthrough
# The product is an order. So the poster is that order, set as a list. Room
# names and the filename pattern are the real ones from the app's own captures
# and support page (123-Oak-St_01_Entry-02.jpg).
ROOMS = [
    'Front Exterior', 'Back Exterior', 'Drone', 'Kitchen', 'Living Room',
    'Dining Room', 'Primary Bedroom', 'Primary Bath', 'Bedroom Two', 'Garage',
]


def walkthrough():
    canvas = gradient('#22262b', '#0a0b0d')
    glow(canvas, (W / 2, 560), 620, '#e9b454', 26)
    draw = ImageDraw.Draw(canvas)

    lockup(canvas, draw, 'walkthrough/assets/icon-1.4.1.png', 'Walkthrough',
           'Organize photos for a property listing.', '#f1efe9')

    num = font('archivo', 34, 760, width=88)
    room = font('archivo', 36, 500)
    fname = font('archivo', 22, 400, width=76)
    y = 552
    for index, name in enumerate(ROOMS, start=1):
        draw_text(draw, (96, y), f'{index:02d}', num, '#e9b454', tracking=1)
        draw_text(draw, (188, y - 1), name, room, '#f1efe9')
        tail = f'123-Oak-St_{index:02d}_{name.replace(" ", "-")}-01.jpg'
        right_text(draw, W - 96, y + 8, tail, fname, '#8d9299')
        draw.line([(px(96), px(y + 62)), (px(W - 96), px(y + 62))], fill='#2f343a', width=px(1))
        y += 104

    vignette(canvas, strength=34)
    footing(draw, 'macOS 14 or later · Apple silicon and Intel', 'brianrenshaw.app/walkthrough',
            '#f1efe9', '#969ca6')
    return canvas


# -------------------------------------------------------------- Reading Habit
# The mechanic drawn rather than described: a run of days, and the rest day the
# app hands you after seven consecutive ones. No invented statistics.
#   x = read   o = rest day   . = not yet
PATTERN = (
    'xxxxxxx'
    'xxxxoxx'
    'xxxxxxx'
    'xxoxxxx'
    'xxxxxxx'
    'xxxxxxo'
    'xxxxxxx'
    'xxxxx..'
)


def reading_habit():
    canvas = gradient('#f7edd7', '#7a5c26')
    glow(canvas, (W / 2, 620), 640, '#fff8e8', 96)
    draw = ImageDraw.Draw(canvas)

    lockup(canvas, draw, 'reading-habit/assets/icon-native.png', 'Reading Habit',
           'Make reading a daily habit.', '#3d3423')

    tile, gap, cols = 104, 20, 7
    left = (W - (cols * tile + (cols - 1) * gap)) / 2
    for index, mark in enumerate(PATTERN):
        col, row = index % cols, index // cols
        x, y = left + col * (tile + gap), 556 + row * (tile + gap)
        box = (px(x), px(y), px(x + tile), px(y + tile))
        draw.rounded_rectangle(box, px(16), fill='#ffffff2e', outline='#8a6a3555', width=px(1))
        if mark == 'x':
            tick(draw, x, y, tile, '#8a5f18', 7)
        elif mark == 'o':  # a rest day, spent automatically after seven in a row
            c, r = (x + tile / 2, y + tile / 2), tile * 0.2
            draw.ellipse((px(c[0] - r), px(c[1] - r), px(c[0] + r), px(c[1] + r)),
                         outline='#8a5f18', width=px(5))

    note = font('archivo', 27, 500)
    centered_block(draw, 556 + 8 * (tile + gap) + 26,
                   ['Seven days in a row earns one rest day.'], note, '#4a3c24', 40)

    vignette(canvas, strength=30)
    footing(draw, 'Free on the App Store', 'brianrenshaw.app/reading-habit',
            '#fdf3dd', '#c9ab72')
    return canvas


# -------------------------------------------------------------------- Canceled
# The app already has a voice, so the poster quotes it instead of inventing one.
# Motifs are the documented ones: the cream slip and the rotated red stamp.
def canceled():
    canvas = gradient('#2d5180', '#0d1523')
    glow(canvas, (W / 2, 640), 620, '#7ba0cf', 52)
    draw = ImageDraw.Draw(canvas)

    lockup(canvas, draw, 'canceled/assets/icon.png', 'Canceled',
           'Nobody has to be the one who cancels.', '#eaf1f9')

    slip_w, slip_h, slip_y = 828, 440, 596
    slip = Image.new('RGBA', (px(slip_w), px(slip_h)), (0, 0, 0, 0))
    sd = ImageDraw.Draw(slip)
    sd.rounded_rectangle((0, 0, slip.width - 1, slip.height - 1), px(20), fill='#fffdf6')
    sd.text((px(52), px(48)), 'T H E   P L A N', font=font('archivo', 20, 700), fill='#6b7d95')
    plan = font('archivo', 58, 900)
    yy = px(96)
    for line in wrap('Dinner & good intentions', plan, slip_w - 104):
        sd.text((px(52), yy), line, font=plan, fill='#142d4e')
        yy += px(64)
    sd.text((px(52), yy + px(16)), 'Sep 18, 2026 at 7:00 PM  ·  The usual place',
            font=font('archivo', 27, 450), fill='#5d6f88')

    rotated = slip.rotate(-2.5, resample=Image.Resampling.BICUBIC, expand=True)
    shadow = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    ghost = Image.new('RGBA', rotated.size, (0, 0, 0, 255))
    ghost.putalpha(rotated.getchannel('A').point(lambda v: int(v * 0.5)))
    ox = px(W / 2) - rotated.width // 2
    shadow.alpha_composite(ghost, (ox, px(slip_y) + px(26)))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(px(34))))
    canvas.alpha_composite(rotated, (ox, px(slip_y)))

    stamp(canvas, 'CANCELED', (W / 2 + 40, slip_y + slip_h - 78), 9, '#a42620', 54)

    quote = font('archivo', 40, 500)
    centered_block(draw, slip_y + slip_h + 116,
                   wrap('“Your evening has been returned to you.”', quote, 880),
                   quote, '#dce8f5', 56)

    # The reveal's audit row, which MESSAGING.md calls out as worth naming.
    label, value = font('archivo', 24, 700), font('archivo', 30, 600)
    row_y = slip_y + slip_h + 232
    for key, amount in (('RETURNED', '1h 30m'), ('EXCUSES USED', 'None')):
        draw.line([(px(126), px(row_y - 16)), (px(W - 126), px(row_y - 16))],
                  fill='#3f5a7e', width=px(1))
        draw_text(draw, (126, row_y + 6), key, label, '#8fa6c2', tracking=2.4)
        right_text(draw, W - 126, row_y, amount, value, '#f7dc12')
        row_y += 86

    vignette(canvas, strength=36)
    footing(draw, 'In development', 'brianrenshaw.app/canceled', '#fffdf6', '#9fb3cc')
    return canvas


def main():
    CONCEPTS.mkdir(parents=True, exist_ok=True)
    for name, render in (('walkthrough', walkthrough),
                         ('reading-habit', reading_habit),
                         ('canceled', canceled)):
        path = CONCEPTS / f'{name}.png'
        render().convert('RGB').resize((W, 1920), Image.Resampling.LANCZOS).save(path, optimize=True)
        print(f'{W}x1920  {path.relative_to(OUT.parents[1])}')


if __name__ == '__main__':
    main()
