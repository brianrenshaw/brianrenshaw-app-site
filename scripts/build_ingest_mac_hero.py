#!/usr/bin/env python3
"""Make hero artwork with Frames CLI; leave the native screenshot untouched.

python3 scripts/build_ingest_mac_hero.py --frames /path/to/frames \
    --assets /path/to/Frames
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "site/ingest/assets"
SOURCE = ASSETS / "editorial-landscapes-0.9.8-retina.webp"
OUTPUT = ASSETS / "hero-macbook-0.9.8.png"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", required=True, type=Path)
    parser.add_argument("--assets", required=True, type=Path)
    args = parser.parse_args()
    # A real app window, proportionally contained on a plain display background.
    # No app controls are cropped, stretched, reconstructed, or painted over.
    screenshot = Image.open(SOURCE).convert("RGBA")
    screenshot.thumbnail((3296, 2100), Image.Resampling.LANCZOS)
    screen = Image.new("RGBA", (3456, 2234), "#343936")
    screen.alpha_composite(screenshot, (
        (screen.width - screenshot.width) // 2,
        (screen.height - screenshot.height) // 2,
    ))
    with tempfile.TemporaryDirectory(prefix="ingest-mac-hero-") as temporary:
        directory = Path(temporary)
        source = directory / "screen.png"
        screen.save(source)
        result = subprocess.run([
            sys.executable, str(args.frames), "--assets", str(args.assets),
            "--json", "-d", "MacBook Pro M5 16", "-c", "Silver",
            "-o", str(directory / "output"), str(source),
        ], check=True, capture_output=True, text=True)
        info = json.loads(result.stdout)
        artwork = Image.open(info["output"]).convert("RGBA")
        # Trim transparent space outside the laptop, not the screenshot.
        artwork = artwork.crop(artwork.getchannel("A").getbbox())
        artwork.save(OUTPUT, optimize=True)
    metadata = {
        "kind": "device-framed marketing artwork; not a native screenshot",
        "appVersion": "0.9.8", "appBuild": 48,
        "nativeScreenshot": SOURCE.name,
        "nativeScreenshotSHA256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "output": OUTPUT.name, "width": artwork.width, "height": artwork.height,
        "device": info["device"], "color": info["color"],
        "tool": "https://github.com/viticci/frames-cli",
        "composition": "Proportional app window on a plain display background; original controls and full-resolution link preserved.",
    }
    (ASSETS / "hero-macbook.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Created {OUTPUT.name}: {artwork.width} × {artwork.height}")


if __name__ == "__main__":
    main()
