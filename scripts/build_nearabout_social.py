#!/usr/bin/env python3
"""Compose the Nearabout share card from its genuine native iPhone capture."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'site/nearabout/assets'
image = Image.new('RGB', (1200, 630), '#f5f2e9')
draw = ImageDraw.Draw(image)
fonts = Path('/System/Library/Fonts/Supplemental')

def text(x, y, copy, size, color='#233e35', face='Georgia.ttf'):
    draw.text((x, y), copy, fill=color, font=ImageFont.truetype(str(fonts / face), size))

text(65, 55, 'Nearabout', 32)
text(65, 190, '“I’ll send you', 49)
text(65, 260, 'my list.”', 49, '#a8452e')
text(65, 370, 'Make lists of places to share and visit together.', 23, '#5a675e', 'Arial.ttf')
text(65, 530, 'iPhone · iPad · Mac', 19, '#5a675e', 'Arial.ttf')
shot = Image.open(ASSETS / 'iphone-list.webp').convert('RGB')
shot.thumbnail((235, 510), Image.Resampling.LANCZOS)
x, y = 850, 60
draw.rounded_rectangle((x - 7, y - 7, x + shot.width + 7, y + shot.height + 7), radius=23, fill='#233e35')
image.paste(shot, (x, y))
image.save(ASSETS / 'social.png', optimize=True)
print('Built Nearabout social.png (1200 × 630)')
