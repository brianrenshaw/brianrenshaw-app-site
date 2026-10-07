#!/usr/bin/env python3
"""Build Decks share artwork from genuine native exports; no reconstructed UI."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'site/decks/assets'
FONT = ROOT / 'site/ingest/assets/fonts/ibm-plex-sans.ttf'
def font(size):
    return ImageFont.truetype(str(FONT), size)
def main():
    canvas = Image.new('RGB', (1200, 630), '#f5f4f0')
    draw = ImageDraw.Draw(canvas)
    icon = Image.open(ASSETS / 'icon.png').convert('RGBA'); icon.thumbnail((44,44))
    canvas.paste(icon, (52,45), icon)
    draw.text((111,47), 'Decks', font=font(30), fill='#242422')
    for i,line in enumerate(['Frames for', 'your photos.']):
        draw.text((52,151+i*58), line, font=font(43), fill='#242422')
    for i,line in enumerate(['Build your layout. Save your design.', 'Use it again, without starting over.']):
        draw.text((54,370+i*31), line, font=font(21), fill='#60605b')
    draw.text((54,540), 'iPhone · iPad · Mac', font=font(19), fill='#242422')
    draw.text((54,572), 'decksphotoapp.com', font=font(17), fill='#60605b')
    for name,box in [('oct06-frame-blur.webp',(590,94,855,500)),('oct06-hero-pair.webp',(885,47,1150,355)),('oct06-frame-black.webp',(930,355,1150,604))]:
        im = Image.open(ASSETS/name).convert('RGB'); im.thumbnail((box[2]-box[0],box[3]-box[1]), Image.Resampling.LANCZOS)
        canvas.paste(im,(box[0]+(box[2]-box[0]-im.width)//2,box[1]+(box[3]-box[1]-im.height)//2))
    canvas.save(ASSETS/'social-oct06-next.png', optimize=True)
    manifest_path = ASSETS/'oct06-assets.json'
    manifest = json.loads(manifest_path.read_text())
    entry = {
        'file': 'social-oct06-next.png', 'kind': 'share-artwork',
        'width': 1200, 'height': 630,
        'source': 'scripts/build_decks_social.py',
        'sourceSha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'sha256': hashlib.sha256((ASSETS/'social-oct06-next.png').read_bytes()).hexdigest(),
        'compositions': ['oct06-frame-blur.webp', 'oct06-hero-pair.webp', 'oct06-frame-black.webp'],
        'transformation': 'Paper canvas, typography, icon, and resized genuine native compositions; no reconstructed UI'
    }
    manifest['images'] = [i for i in manifest['images'] if i['file'] != entry['file']] + [entry]
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    print('Built 1200 × 630 Decks share artwork')
if __name__ == '__main__': main()
