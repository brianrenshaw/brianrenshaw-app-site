#!/usr/bin/env python3
"""Render the homepage's featured Ingest and Decks card images from each site's hero art (Pillow, cwebp)."""
from pathlib import Path
import subprocess
import tempfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
WIDTH = 1200


def save(image, name):
    image = image.crop(image.getchannel('A').point(lambda a: 255 if a > 8 else 0).getbbox())
    image = image.resize((WIDTH, round(image.height * WIDTH / image.width)), Image.Resampling.LANCZOS)
    with tempfile.NamedTemporaryFile(suffix='.png') as png:
        image.save(png.name)
        subprocess.run(['cwebp', '-quiet', '-q', '82', '-alpha_q', '90', '-m', '6', png.name,
                        '-o', str(SITE / 'assets' / name)], check=True)
    print(name, image.size)


# Ingest: the MacBook composition from the ingestphotoapp.com hero.
save(Image.open(SITE / 'ingest/assets/hero-macbook-workflow-0.9.8.webp').convert('RGBA'),
     'featured-ingest-0.9.8.webp')

# Decks: the iPhone, iPad and Mac trio, placed as .hero-devices places it on
# decksphotoapp.com (aspect 1.55; Mac 86% wide at left 7%, bottom 3%; iPad 50%
# at right 0; iPhone 23% at left 0; later devices sit in front).
canvas = Image.new('RGBA', (2400, round(2400 / 1.55)))
for name, share, left, right, bottom in [('oct06-framed-mac.webp', .86, .07, None, .03),
                                          ('oct06-framed-builder.webp', .50, None, 0, 0),
                                          ('oct06-framed-phone-camera.webp', .23, 0, None, 0)]:
    device = Image.open(SITE / 'decks/assets' / name).convert('RGBA')
    width = round(canvas.width * share)
    device = device.resize((width, round(device.height * width / device.width)), Image.Resampling.LANCZOS)
    x = round(canvas.width * left) if left is not None else canvas.width - width - round(canvas.width * right)
    canvas.alpha_composite(device, (x, canvas.height - device.height - round(canvas.height * bottom)))
save(canvas, 'featured-decks-devices-oct06.webp')
