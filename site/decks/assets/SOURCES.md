# Decks website photography and screenshots

The October 1, 2026 redesign uses Brian Renshaw's photographs and Decks 0.1.0 (43). No generated photography or reconstructed app interfaces are used.

`build43-single`, `build43-pair`, `build43-coffee`, and `build43-camera` are unchanged native renderer output from the app's onboarding assets in `photo-importer-acros/Social/Assets.xcassets`. They show the same designs that appear in the build 43 introduction. The bridge design shows its real Fujifilm X-T4 capture details; the Mamiya camera is the subject of its photograph.

`build43-home`, `build43-size`, `build43-frame`, `build43-caption`, and `build43-panorama` are original native iPhone screenshots from `/tmp/decks43-ui.xcresult`, exported to `/tmp/decks43-ui-shots`. The caption illustration is the actual build 43 introduction screen, not a Caption Sheet capture. Size and frame images show the actual two-photo template walkthrough. Screenshots use the app's dark appearance; the website's paper background does not recolor them.

All nine images are lossless WebP at their original dimensions. Their decoded RGB pixels were verified against the PNG sources. `build43-assets.json` records each source, size, and SHA-256. Full-size links are provided for native screenshots that contain controls. Existing historical image URLs remain available.

Original photographs remain untouched in `~/Downloads/Decks/`; the app's imported copies and original-file mappings are in `photo-importer-acros/Social/Resources/Tutorial/README.md`.

## Backgrounds, borders, and camera-detail gallery

The ten additional `build43-frame-*` and `build43-camera-*` images are real exports from the build 43 renderer, `IngestSocialKit` at native commit `1d05ac8`. `scripts/render_decks_examples.swift` records the exact settings. It runs in a temporary Swift executable with that package as its local dependency, using the imported Tutorial JPEGs and writing PNGs to a separate output directory. It does not change the app project or original photos.

The six frame examples show the coastline on white, black with a white border, and photo blur with a white border; a winter detail with a black border on white; a two-photo layout on blur; and a library photograph with a film border. Film lettering describes the border style, not a claim about the photograph's capture stock.

Four camera examples show a transparent details panel beside the Fujifilm bridge photograph, an overlay on the Hasselblad coastline photograph, Sony sunset details below the photo, and separate details on the Fujifilm bridge and Sony winter photographs. All settings come from the photos' actual EXIF through the native importer; none are invented.

`build43-gallery.json` records original PNG hashes, lossless WebP hashes, and original dimensions. All decoded RGB pixels were verified against the PNG exports. Full-size image links let visitors inspect the designs and small camera text.
