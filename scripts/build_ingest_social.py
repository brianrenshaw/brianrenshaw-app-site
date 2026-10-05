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
text(64, 48, 'INGEST / PHOTO WORKFLOW FOR MAC', 19, '#72511c')
text(60, 112, 'Ingest. Cull.', 88)
text(60, 214, 'Browse. Organize.', 88)
text(64, 365, 'Your workspace. Your photographs.', 30)
text(64, 412, 'Workspaces + Metadata Assist', 26, '#68635a')
draw.line((128, 1016, 2272, 1016), fill='#d8d4ca', width=2)
text(64, 542, 'Free during beta · macOS 15+ · Apple silicon', 20, '#68635a')
text(966, 542, '0.9.5', 20, '#72511c')
canvas.resize((1200, 630), Image.Resampling.LANCZOS).save(
    ROOT / 'site/ingest/assets/share-0.9.5.png', optimize=True)
