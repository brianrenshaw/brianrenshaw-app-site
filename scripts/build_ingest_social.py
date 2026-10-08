#!/usr/bin/env python3
"""Build Ingest's share artwork from the site's bundled font and colors."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[1]
SCALE = 2
canvas = Image.new('RGB', (2400, 1260), '#f7f6f2')
draw = ImageDraw.Draw(canvas)
font_path = ROOT / 'site/where-do-we-eat/assets/fonts/Archivo[wdth,wght].ttf'
def text(x, y, value, size, color='#242321'):
    font = ImageFont.truetype(str(font_path), size * SCALE)
    draw.text((x * SCALE, y * SCALE), value, font=font, fill=color)
draw.rectangle((0, 0, 20, 1260), fill='#efa817')
text(64, 48, 'INGEST / NATIVE MAC APP', 19, '#72511c')
text(60, 112, 'Modern photo', 78)
text(60, 214, 'management for Mac.', 78)
text(64, 365, 'Import, review, and organize your photos.', 30)
text(64, 412, 'Workspaces · Command-K · Review · Metadata', 26, '#68635a')
draw.line((128, 1016, 2272, 1016), fill='#d8d4ca', width=2)
text(64, 542, 'Free during beta · macOS 15+ · Apple silicon', 20, '#68635a')

canvas.resize((1200, 630), Image.Resampling.LANCZOS).save(
    ROOT / 'site/ingest/assets/share-editorial-oct08.png', optimize=True)
