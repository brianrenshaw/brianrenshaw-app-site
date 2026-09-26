#!/usr/bin/env python3
"""Generate solo marketing visuals for the Ingest homepage.

Creates illustrated metaphor art (not fake UI) and cropped mode-ribbon
thumbnails from existing site screenshots. Run from repo root.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "site" / "ingest" / "assets"

# Site palette
BG = (251, 250, 247, 255)
SURFACE = (255, 255, 255, 255)
INK = (36, 38, 34, 255)
MUTED = (96, 99, 93, 255)
ACCENT = (134, 82, 11, 255)
GOLD = (239, 173, 57, 255)
LINE = (222, 223, 215, 255)
STAGE = (238, 238, 231, 255)
CARD_BODY = (48, 52, 46, 255)
CARD_METAL = (90, 94, 86, 255)
LIGHT = (255, 220, 140, 255)
FOLDER = (214, 186, 120, 255)
FOLDER_DARK = (168, 132, 72, 255)


def font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def save_webp(im: Image.Image, path: Path, quality: int = 90):
    rgb = im.convert("RGB") if im.mode == "RGBA" else im
    rgb.save(path, "WEBP", lossless=True, method=6)
    print(f"wrote {path.relative_to(ROOT)} {rgb.size}")


def rounded_rect(draw, xy, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def draw_sd_card(base: Image.Image, origin: tuple[int, int], scale: float = 1.0):
    """Stylized SD/CF hybrid card — metaphor, not a product mock."""
    x, y = origin
    w, h = int(220 * scale), int(300 * scale)
    d = ImageDraw.Draw(base)
    # Card body
    rounded_rect(d, (x, y, x + w, y + h), int(18 * scale), fill=CARD_BODY)
    # Notch / bevel
    notch = [
        (x + int(w * 0.68), y),
        (x + w, y + int(40 * scale)),
        (x + w, y),
    ]
    d.polygon(notch, fill=STAGE)
    # Contact pads
    pad_w, pad_h = int(28 * scale), int(48 * scale)
    pad_y = y + int(36 * scale)
    for i in range(5):
        px = x + int(28 * scale) + i * int(34 * scale)
        rounded_rect(d, (px, pad_y, px + pad_w, pad_y + pad_h), 4, fill=CARD_METAL)
    # Write-protect slider
    rounded_rect(
        d,
        (x + int(16 * scale), y + int(h * 0.55), x + int(36 * scale), y + int(h * 0.72)),
        4,
        fill=CARD_METAL,
    )
    # Label area
    label = (x + int(28 * scale), y + int(h * 0.42), x + w - int(28 * scale), y + int(h * 0.88))
    rounded_rect(d, label, 8, fill=(58, 62, 54, 255))
    f = font(int(22 * scale), bold=True)
    d.text((x + int(44 * scale), y + int(h * 0.52)), "CARD", font=f, fill=GOLD)
    f2 = font(int(15 * scale))
    d.text((x + int(44 * scale), y + int(h * 0.62)), "64 GB", font=f2, fill=(200, 198, 188, 255))
    d.text((x + int(44 * scale), y + int(h * 0.72)), "RAW · JPEG", font=f2, fill=(160, 158, 148, 255))


def draw_folder_tree(base: Image.Image, origin: tuple[int, int], scale: float = 1.0):
    x, y = origin
    d = ImageDraw.Draw(base)
    f = font(int(18 * scale))
    f_sm = font(int(15 * scale))

    def folder_row(fx, fy, label, depth=0, open_=False):
        indent = depth * int(28 * scale)
        # Folder glyph
        fw, fh = int(28 * scale), int(20 * scale)
        tab = int(10 * scale)
        pts = [
            (fx + indent, fy + tab),
            (fx + indent + tab, fy),
            (fx + indent + tab * 2 + int(6 * scale), fy),
            (fx + indent + tab * 2 + int(6 * scale), fy + tab),
            (fx + indent + fw, fy + tab),
            (fx + indent + fw, fy + fh),
            (fx + indent, fy + fh),
        ]
        d.polygon(pts, fill=FOLDER if open_ else FOLDER_DARK)
        d.text((fx + indent + fw + int(12 * scale), fy + int(1 * scale)), label, font=f, fill=INK)

    folder_row(x, y, "Shoots", 0, True)
    folder_row(x, y + int(36 * scale), "2026-09-25 Wedding", 1, True)
    folder_row(x, y + int(72 * scale), "01-Originals", 2, False)
    folder_row(x, y + int(108 * scale), "02-Selects", 2, False)
    folder_row(x, y + int(144 * scale), "03-Delivery", 2, False)
    # Quiet file names under Selects
    d.text((x + int(84 * scale), y + int(180 * scale)), "W-001.jpg", font=f_sm, fill=MUTED)
    d.text((x + int(84 * scale), y + int(204 * scale)), "W-002.jpg", font=f_sm, fill=MUTED)
    d.text((x + int(84 * scale), y + int(228 * scale)), "W-003.jpg", font=f_sm, fill=MUTED)


def draw_light_path(base: Image.Image, start, end):
    """Thin warm path of light from card to folders."""
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    # Outer soft glow
    for i, alpha in enumerate((18, 28, 40, 55)):
        width = 28 - i * 6
        g.line([start, end], fill=(*LIGHT[:3], alpha), width=width)
    # Core
    g.line([start, end], fill=(*GOLD[:3], 220), width=3)
    # Soften
    glow = glow.filter(ImageFilter.GaussianBlur(radius=6))
    base.alpha_composite(glow)
    # Crisp core on top
    d = ImageDraw.Draw(base)
    d.line([start, end], fill=(*GOLD[:3], 255), width=2)
    # Small nodes
    for pt in (start, ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2), end):
        r = 5
        d.ellipse((pt[0] - r, pt[1] - r, pt[0] + r, pt[1] + r), fill=GOLD)


def build_filmstrip():
    W, H = 2400, 860
    im = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(im)
    # Stage panel
    rounded_rect(d, (48, 48, W - 48, H - 48), 28, fill=STAGE, outline=LINE, width=2)

    # Left label
    fl = font(22, bold=True)
    d.text((120, 100), "FROM THE CARD", font=fl, fill=ACCENT)
    # Right label
    d.text((W - 520, 100), "INTO YOUR FOLDERS", font=fl, fill=ACCENT)

    draw_sd_card(im, (180, 220), scale=1.7)
    draw_folder_tree(im, (W - 620, 250), scale=1.55)

    # Path of light
    start = (180 + int(220 * 1.7) + 20, 220 + int(300 * 1.7) // 2)
    end = (W - 640, 250 + int(120 * 1.55))
    draw_light_path(im, start, end)

    save_webp(im, ASSETS / "card-to-folders-filmstrip.webp", quality=88)


def build_setup_panels():
    W, H = 1600, 1000

    # BEFORE — messy rename pile
    before = Image.new("RGBA", (W, H), STAGE)
    d = ImageDraw.Draw(before)
    rounded_rect(d, (40, 40, W - 40, H - 40), 24, fill=SURFACE, outline=LINE, width=2)
    d.text((80, 80), "BEFORE", font=font(24, bold=True), fill=ACCENT)
    d.text((80, 120), "Every card, reinvented.", font=font(36, bold=True), fill=INK)

    messy = [
        ("IMG_3847.CR3", 120, 240, -12),
        ("DSC_0291.JPG", 420, 210, 8),
        ("_MG_1102.CR2", 760, 280, -6),
        ("R5_004812.CR3", 180, 420, 14),
        ("IMG_3848.CR3", 560, 390, -9),
        ("P1040291.RW2", 980, 360, 5),
        ("DSC_0292.JPG", 300, 580, 11),
        ("IMG_3849.CR3", 720, 560, -4),
        ("Untitled-12.psd", 1040, 520, 7),
        ("final_FINAL_v3.jpg", 480, 720, -8),
        ("selects???.zip", 860, 700, 10),
        ("card dump", 200, 760, 3),
    ]
    f = font(28)
    for name, x, y, rot in messy:
        chip = Image.new("RGBA", (360, 64), (0, 0, 0, 0))
        cd = ImageDraw.Draw(chip)
        rounded_rect(cd, (0, 0, 350, 56), 10, fill=(245, 240, 230, 255), outline=(210, 180, 150, 255), width=2)
        cd.text((16, 14), name, font=f, fill=(110, 70, 40, 255))
        chip = chip.rotate(rot, expand=True, resample=Image.BICUBIC)
        before.alpha_composite(chip, (x, y))

    d.text((80, H - 100), "Renames, folders, and destinations rebuilt by hand.", font=font(22), fill=MUTED)
    save_webp(before, ASSETS / "setup-once-before.webp", quality=88)

    # AFTER — workspace that sticks
    after = Image.new("RGBA", (W, H), STAGE)
    d = ImageDraw.Draw(after)
    rounded_rect(d, (40, 40, W - 40, H - 40), 24, fill=SURFACE, outline=LINE, width=2)
    d.text((80, 80), "AFTER", font=font(24, bold=True), fill=ACCENT)
    d.text((80, 120), "One workspace. Next card ready.", font=font(36, bold=True), fill=INK)

    # Calm workspace card
    panel = (80, 220, W - 80, H - 140)
    rounded_rect(d, panel, 18, fill=(248, 247, 242, 255), outline=LINE, width=2)
    d.text((120, 260), "Workspace · Wedding", font=font(28, bold=True), fill=INK)

    rows = [
        ("Naming", "{date}-{seq}"),
        ("Folders", "01-Originals / 02-Selects / 03-Delivery"),
        ("Metadata", "Shared shoot details"),
        ("View", "Photo-first · bursts grouped"),
        ("Extras", "Backup on · Social Export off"),
    ]
    y = 330
    for label, value in rows:
        d.text((120, y), label, font=font(22, bold=True), fill=ACCENT)
        d.text((360, y), value, font=font(22), fill=INK)
        d.line((120, y + 42, W - 120, y + 42), fill=LINE, width=1)
        y += 70

    d.text((80, H - 100), "Configure once. The next card opens ready.", font=font(22), fill=MUTED)
    save_webp(after, ASSETS / "setup-once-after.webp", quality=88)


def crop_mode_thumbs():
    """Crop existing screenshots into labeled mode ribbon thumbs."""
    sources = {
        "ingest": ASSETS / "ingest-0.9.2-retina.webp",
        "cull": ASSETS / "grid-cull-0.8.0-retina.webp",
        "browse": ASSETS / "browse-0.9.2-retina.webp",
        "organize": ASSETS / "organize-0.9.2-retina.webp",
    }
    # Prefer a center-upper crop that shows the grid / main workspace, not chrome alone.
    # Output ~1200×760 retina thumbs.
    out_w, out_h = 1200, 760
    for key, path in sources.items():
        im = Image.open(path).convert("RGB")
        w, h = im.size
        # Crop a slightly inset window interior (drop outer chrome a bit)
        left = int(w * 0.08)
        right = int(w * 0.92)
        top = int(h * 0.10)
        bottom = int(h * 0.78)
        crop = im.crop((left, top, right, bottom))
        # Cover-fit into target
        cw, ch = crop.size
        scale = max(out_w / cw, out_h / ch)
        resized = crop.resize((int(cw * scale), int(ch * scale)), Image.LANCZOS)
        rw, rh = resized.size
        x0 = (rw - out_w) // 2
        y0 = (rh - out_h) // 2
        thumb = resized.crop((x0, y0, x0 + out_w, y0 + out_h))
        save_webp(thumb, ASSETS / f"mode-{key}.webp", quality=86)


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    build_filmstrip()
    build_setup_panels()
    crop_mode_thumbs()
    print("done")


if __name__ == "__main__":
    main()
