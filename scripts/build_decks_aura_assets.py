#!/usr/bin/env python3
"""Package native Aura renders and normalize a screenshot without altering its pixels."""
from pathlib import Path
import hashlib
import json
import sys
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'site/decks/assets'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    source_dir = Path(sys.argv[1])
    manifest = json.loads((ASSETS / 'oct06-assets.json').read_text())
    additions = []
    for name in ['aura-pair', 'aura-soft', 'aura-full', 'aura-thin', 'threads-single', 'ipad-builder-upright']:
        screenshot = name == 'ipad-builder-upright'
        source = ASSETS / 'oct06-ipad-builder.webp' if screenshot else source_dir / (name + '.png')
        original = Image.open(source)
        normalized = ImageOps.exif_transpose(original) if screenshot else original
        target = ASSETS / ('oct06-next-' + name + '.webp')
        normalized.save(target, lossless=True, exact=True)
        reopened = Image.open(target)
        assert normalized.convert('RGBA').tobytes() == reopened.convert('RGBA').tobytes()
        assert reopened.getexif().get(274, 1) == 1
        entry = dict(file=target.name, kind='native-capture' if screenshot else 'native-render',
                     width=reopened.width, height=reopened.height,
                     source=str(source.relative_to(ROOT)) if screenshot else str(source),
                     sourceSha256=sha(source), sha256=sha(target),
                     rendererCommit='9546540',
                     transformation='EXIF orientation applied to pixel coordinates; orientation removed; lossless encoding' if screenshot else 'Lossless WebP encoding of native render')
        if screenshot:
            entry.update(originalWidth=original.width, originalHeight=original.height,
                         originalOrientation=original.getexif().get(274), orientation=1)
        else:
            project = source_dir / (name + '.json')
            entry.update(projectSha256=sha(project), projectSource=str(project))
        additions.append(entry)
        print(target.name, reopened.size, 'pixel equality PASS')
    names = {e['file'] for e in additions}
    manifest['images'] = [e for e in manifest['images'] if e['file'] not in names] + additions
    (ASSETS / 'oct06-assets.json').write_text(json.dumps(manifest, indent=2) + '\n')

if __name__ == '__main__':
    main()
