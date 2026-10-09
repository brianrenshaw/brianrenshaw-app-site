# Decks website photography and screenshots

The October 1, 2026 redesign uses Brian Renshaw's photographs and Decks 0.1.0 (43). No generated photography or reconstructed app interfaces are used.

`build43-single`, `build43-pair`, `build43-coffee`, and `build43-camera` are unchanged native renderer output from the app's onboarding assets in `photo-importer-acros/Social/Assets.xcassets`. They show the same designs that appear in the build 43 introduction. The bridge design shows its real Fujifilm X-T4 capture details; the Mamiya camera is the subject of its photograph.

`build43-home`, `build43-size`, `build43-frame`, `build43-caption`, and `build43-panorama` are original native iPhone screenshots from `/tmp/decks43-ui.xcresult`, exported to `/tmp/decks43-ui-shots`. The caption illustration is the actual build 43 introduction screen, not a Caption Sheet capture. Size and frame images show the actual two-photo template walkthrough. Screenshots use the app's dark appearance; the website's paper background does not recolor them.

All nine images are lossless WebP at their original dimensions. Their decoded RGB pixels were verified against the PNG sources. `build43-assets.json` records each source, size, and SHA-256. Full-size links are provided for native screenshots that contain controls. Existing historical image URLs remain available.

Original photographs remain untouched in `~/Downloads/Decks/`; the app's imported copies and original-file mappings are in `photo-importer-acros/Social/Resources/Tutorial/README.md`.

## Backgrounds, borders, and camera-detail gallery

The ten additional `build43-frame-*` and `build43-camera-*` images are real exports from the build 43 renderer, `IngestSocialKit` at native commit `1d05ac8`. `scripts/render_decks_examples.swift` records the exact settings. It runs in a temporary Swift executable with that package as its local dependency, using the imported Tutorial JPEGs and writing PNGs to a separate output directory. It does not change the app project or original photos.

The six frame examples use distinct subjects: In-N-Out (`Burger.jpg`, original `fuji_5063.jpg`) on white; baseball (`Example40.jpg`, `fuji_5924.jpg`) on black with a white border and its actual camera details; fall basketball (`Example26.jpg`, `DSCF3213.jpg`) on blur; espresso (`Example29.jpg`, `_DSC1199 1.jpg`) with a black border on white; two autumn woodland photographs (`Example24.jpg` / `Example27.jpg`, `DSCF3198.jpg` / `DSCF3219.jpg`) on blur; and black-and-white baseball (`Example14.jpg`, `7637-05.jpg`) with a film border on white. Film lettering describes the border style, not a claim about the photograph's capture stock.

Four camera examples use an autumn landscape (`Example25.jpg`, `DSCF3202.jpg`) beside its details, a rainbow (`Example19.jpg`, `DSC07096.jpg`) with an overlay, sunset details below the photo, and separate details on food and pizza (`Example37.jpg` / `Example38.jpg`, `fuji_5453.jpg` / `fuji_5458.jpg`). All settings come from actual EXIF through the native importer; none are invented. Each gallery photograph appears only once. The requested `_DSC1997` filename is absent from the supplied collection; `_DSC1199 1.jpg` is the available espresso photo.

`build43-gallery.json` records original PNG hashes, lossless WebP hashes, and original dimensions. All decoded RGB pixels were verified against the PNG exports. Full-size image links let visitors inspect the designs and small camera text.


## Build 77 — October 4, 2026

Current editor captures (`build77-home`, `layout`, `background`, `photo`, `caption`, and `gestures`) come from the actual native iPhone simulator using Brian's bundled Bridge/Mamiya/Coastline photography. No interface was reconstructed. Camera cards use the photograph's own metadata. Screenshots were captured by `SocialQuickArrangeUITests.testCurrentPhotographyAndOnboardingCaptures`; lossless WebP retains their full pixel dimensions.

Frame and camera examples were rendered with the current `IngestSocialKit` using `scripts/render_decks_examples.swift` and Brian's `Social/Resources/Tutorial` originals. Beside/below examples use the production Quick Arrange algorithm, including enlarged cards and balanced margins. The source projects are in `/tmp/decks77-gallery/output/` on the development machine. `build77-assets.json` records dimensions and hashes. Older assets remain available for existing links; unchanged finished photography and the panorama preview retain their original provenance above.


## Build 78 — October 5, 2026

`build78-layout`, `background`, `photo`, and `text` are unmodified native iPhone simulator captures from `testContentSizedPhotographyCaptures`, using the bundled Bridge photograph and its original metadata. They show content-sized panels, the persistent scope menu, Ivory, Color mode without Replace Background, and compact Text actions. Lossless WebP preserves original dimensions and RGB pixels; `build78-assets.json` records hashes. Other build-77 artwork remains current because its rendering has not changed.

## October 6 — iOS 113 / native Mac 112

The `oct06-` series uses current native Decks rendering and unmodified native interfaces. `oct06-assets.json` records original dimensions, source paths, and input/output SHA-256 hashes. Every converted image was compared against its source as RGBA pixels. Mac screenshots retain transparent window corners. The landscape iPad image retains its EXIF orientation and records both stored and displayed dimensions. Full-size links remain available; no historical assets were removed.

`scripts/render_decks_refresh.swift` documents the photo and layout settings. The ten frame/camera subjects and original-file mappings are those listed above. Additional examples use `Mamiya.jpg` and `Coastline.jpg` (paired composition), `Example26.jpg` (Story), `Example29.jpg` (Aura), `Mamiya.jpg` (YouTube edit), `Example24.jpg`/`Example27.jpg` (Threads), and `Coastline.jpg` (three panorama panels). Coffee, Burger, and Example29 demonstrate the same saved Everyday Frame template. `oct06-shortcut-original.webp` is the unchanged Coffee photograph; its matching finished design is `oct06-reuse-1.webp`.

The Fuji composition imports Brian's original `~/Downloads/Decks/DSCF0205.JPG`, rather than a converted tutorial copy. Its MakerNotes report Classic Negative, dynamic range 100, highlights -1, shadows -1, and color 0. No recipe name was invented. `oct06-fuji-controls.webp` is the native Mac field-selection sheet for that imported photograph.

Phone camera/layout/text captures came from `/tmp/decks-site-phone-final.xcresult`, `SocialQuickArrangeUITests.testContentSizedPhotographyCaptures`, using the real bundled Bridge photograph. The iPad editor came from that same capture test in `/tmp/decks-site-ipad-final.xcresult`; the dark capture succeeded before an unrelated simulator relaunch failure. The final iPad Layout Builder capture came from the passing `SocialWorkspaceUITests.testIPadLayoutBuilderUsesLargePreviewAndKeepsChoicesOnRotation` run in `/tmp/decks-website-ipad-photography.xcresult`, showing Brian's Burger photograph. Earlier captures containing simulator stock photos were rejected.

`oct06-shortcut-setup.webp` comes from the passing native `IngestSocialUITests.testStarterShortcutFileIsAvailable` in `/tmp/decks-website-shortcuts-setup.xcresult`. It shows Decks's genuine one-time setup, not a reconstructed Apple Shortcuts interface. The surrounding original/result images illustrate the workflow; they are not screenshots of a completed Apple Photos share-sheet run. See `DECKS_REFRESH.md` for the remaining end-to-end check and the obsolete export-width assertion in the existing native acceptance test.

Mac workspace and Template Builder images were captured at native 2× resolution from an isolated probe store. The workspace pairs Mamiya and Coastline. Template Builder shows Brian's native bundled Louisville night photograph. Ingest Send to Decks was captured from 0.9.7 with six copied photographs in a separate test library; the receiver is the actual Decks Mac new/existing-project chooser for that package.

`oct06-video-still.webp` is a frame at one second from `framed-video.mp4`, actually exported through Decks's `SocialVideoExporter`. The input is a short slow zoom made from Brian's `scripps_pierre-184935.jpg`; it is labeled as a sample clip made from a photograph. `oct06-video-poster.webp` is retained as a renderer preview but is not the homepage's video evidence. `social-oct06.png` is a 1200 × 630 layout of real Decks exports, reproducible with `scripts/build_decks_social.py`.

## October 6 next pass — Aura and screenshot orientation

Historical `oct06-` URLs above are retained byte for byte. The new assets use `oct06-next-` names. `render_decks_refresh.swift --aura-pass` ran against an isolated `git archive` of IngestSocialKit at `9546540`, the released renderer baseline, rather than concurrent unshipped destination changes. Native PNG/project output is in `/tmp/decks-next-assets`; the reproducible packaging script is `scripts/build_decks_aura_assets.py`.

- `aura-pair`: Example24/Example27, side-by-side with narrow white margins; 1280 × 800, Carver shape. This one export appears in the homepage, Aura hero, and paired-layout example.
- `aura-soft`: Example26, fit within its own blurred background; 1280 × 800.
- `aura-full`: Coastline, native fill crop with no margins; 1600 × 1200.
- `aura-thin`: Sunset, native fill crop and 0.018 margins; 1600 × 1200.
- `threads-single`: Example29, white 4:5 page; 1080 × 1350.
- `ipad-builder-upright`: the original `oct06-ipad-builder.webp` has stored dimensions 1640 × 2360 and EXIF orientation 8. The derivative applies that orientation to pixel positions, producing 2360 × 1640 with no orientation tag. Its decoded pixels exactly match the EXIF-normalized original. No UI content was retouched; the historical file remains untouched.

Every new WebP was verified pixel-identical to its native source (or orientation-normalized source). `oct06-assets.json` records hashes, dimensions, project-source hashes, and transformations. The named frame-menu screenshot and shape-aware Layout Builder recapture are deferred until those interfaces ship publicly. No local unreleased UI is represented as a shipped screenshot.

`social-oct06-next.png` is the new 1200 × 630 share artwork, with “Frames for your photos.” beside the Decks name and unchanged native compositions. `build_decks_social.py` now generates this version; `social-oct06.png` remains the historical artwork.

## Device presentations — October 6, 2026

`oct06-framed-{phone,ipad,builder,mac}.webp` use the existing genuine isolated-library native captures, framed with [Federico Viticci’s Apple Frames CLI](https://github.com/viticci/frames-cli), v1.5.0, commit `2a62a0c9b77d3d8582f5d1a41d97a80677664e0f`, and its Apple Frames 4.0.2 asset pack. These are hardware presentations, not new captures or new release evidence. Hardware artwork is supplied by Apple Frames; the CLI is MIT licensed, copyright Federico Viticci (2026).

The iPhone uses an explicit iPhone 17 Pro Silver frame rather than the CLI’s newer automatic default. The iPad uses the matching 1640×2360 opening (and its landscape equivalent). The Mac window is centered at its original 2640×1760 pixel size on a neutral 3024×1964 background inside a MacBook frame: this is not represented as a full-desktop capture. No screenshot is stretched or resampled. The phone’s hardware mask trims screen corners. The builder uses the previously normalized upright derivative. All outputs are lossless WebP, with dimensions, source and artwork hashes, CLI version/commit, and orientation recorded in `oct06-assets.json`. Historical assets and full-size original links remain available.

Rebuild with `python3 scripts/build_decks_device_frames.py --cli /path/to/frames --assets /path/to/Frames`.

`oct06-framed-phone-camera.webp` adds a second iPhone presentation from the historical `oct06-phone-camera.webp`, using the same explicit iPhone 17 Pro Silver frame and lossless process. The platform showcase reuses the genuine landscape `oct06-framed-builder.webp` for iPad; the portrait iPad asset remains available at its historical URL.

`oct06-framed-phone-text.webp` wraps the genuine Text-tool capture in the same iPhone 17 Pro Silver bezel. Screenshot pixels and full-size original URL remain unchanged. This capture shows Add Text/Add Logo entry actions, not an expanded text editor.

### Build 132 native Mac captures

`build132-mac-builder.png` and `build132-mac-frame-menu.png` were captured through CUA from installed Decks build 132. They contain built-in preview photography and the named frame menu only. WebP versions are lossless, upright, full-window derivatives with no resampling; originals remain linked. The equivalent named destinations and Smart Layout entry are public in Mac TestFlight 125. Dimensions and SHA-256 hashes are recorded in oct06-assets.json.

## October 8 YouTube example

`oct08-youtube-autumn-soft.png` and its lossless WebP use the user-supplied `/Users/brianrenshaw/Downloads/09141.jpg`. Rendered with IngestSocialKit at commit 95a303fc005e0e32fb238027672fc0d5fcf82e17 through SocialRenderService in an isolated DemoStore. The 1920×1080 composition fits the entire upright photo, with a soft photo background and thin white border, and adds no text. Source and output hashes are in oct06-assets.json. `scripts/render_decks_youtube.swift` preserves the native rendering recipe.

## October 8 Smart Layout walkthrough

`oct08-smart-phone-*` and `oct08-smart-pad-*` are unmodified native screenshots from Decks build 132 (`photo-importer-acros` at 95a303f), captured by the new `SocialDestinationUITests.testSmartLayoutWebsiteCaptures` in `/tmp/decks-smart-layout-phone.xcresult` (iPhone 17 Pro, iOS 27.0) and `/tmp/decks-smart-layout-pad.xcresult` (iPad Air 11-inch M3, iOS 27.0, launched in landscape). Each simulator was created for this run. Its Photos library was emptied of Apple's sample images and seeded with `simctl addmedia` using only Brian's tutorial photos Example29 (espresso), Example27 and Example24 (autumn woodland), NightStreet, and Sunset. Capture-date order starts the woodland photos in different pairs; the test's one tap-to-swap brings them together. Black Border is Smart Layout's default single-photo style. On the landscape iPad, XCTest's app screenshot comes back clipped, so the iPad assets use the same run's full-screen `XCUIScreen` captures. Those are stored sideways with EXIF orientation 8; the WebPs hold the upright 2360 × 1640 pixels, with no resampling.

`oct08-smart-framed-*` wrap those captures with frames-cli v1.5.0 (commit 2a62a0c9) and the Apple Frames 4.0.2 pack: iPhone 17 Pro Portrait Silver, iPad Air 2020 Landscape, and iPhone 17 Pro Max Portrait Silver for the share sheet. No screenshot is resampled.

`oct08-smart-aura-pair.webp` and `oct08-smart-aura-single.webp` are the actual 1280 × 800 JPEG pages that the same iPhone run saved with Export → Save to Photos for an Aura Carver, decoded and stored losslessly. The export screen's free-export counter (unreleased pricing UI) and the simulator share sheet, which can't show Aura, are captured in the xcresult but not used on the site. `scripts/build_decks_smart_layout_assets.py` packages everything and records sizes and SHA-256 hashes in oct06-assets.json.

`oct08-smart-phone-share-aura.webp` is Brian's own iPhone screenshot of the iOS share sheet showing Aura (1320 × 2868), supplied October 8. The suggested-contacts row (pixels 0–1320 × 577–963) is pixelated and blurred by the packaging script so no face, initials, or name is legible; the unblurred original is not stored in this repository. The three images in its header are unrelated to the Aura example pages.

`oct08-smart-spot-*` are the same screenshots with the part each step describes spotlighted: everything else dimmed and the part outlined in Decks's Sky accent `#35B6E8` (`SocialAppearance.accents`). `scripts/build_decks_smart_layout_callouts.py` holds the regions and applies them before framing. The unmarked `oct08-smart-phone-*`/`oct08-smart-pad-*` screenshots remain the linked originals; the earlier unmarked `oct08-smart-framed-*` presentations stay published at their URLs.

## Build 148 refresh — October 9, 2026

`build148-*` assets come from Decks build 148, native source `photo-importer-details` at `42c30ae` (branch `codex/camera-details`), built in an isolated clone so the working copy was untouched. Hashes, dimensions, test names and source files for every file are in `oct06-assets.json`.

- **iPhone and iPad captures** (`build148-phone-*`, `build148-pad-*`, `build148-aura-pad-*`): new XCTest UI tests `SocialWebsiteBuild148UITests` (`testWebsiteHomePagesAndEditor`, `testWebsiteTemplatesAndSmartLayoutBuilder`, `testWebsiteDesignCameraDetailsAndStamp`) and the updated `SocialDestinationUITests.testSmartLayoutWebsiteCaptures`, which now opens the Layout tool of the build 147 pages screen before the groups step. Simulators were created for this run (iPhone 17 Pro and iPad Air 11-inch M3, iOS 27.0), their Photos libraries emptied of Apple's samples, and seeded with `simctl addmedia` using only Brian's tutorial photos: Example40, Example27, Example24, Burger, Coffee, Sunset, Example29 and Bridge for the website tests, and Example29, Example27, Example24, NightStreet and Sunset for the Aura run. Each app launch used a fresh `--social-probe-run` store with no demo project. Status bars use `simctl status_bar` (9:41). iPad captures are the full-screen `XCUIScreen` images, stored sideways with EXIF orientation 8; the WebPs hold the upright 2360 × 1640 pixels with no resampling. No tutorial photo has GPS, so no stamp shows a place.
- **Mac captures** (`build148-mac-home`, `build148-mac-smart-builder`): the DecksMac Debug build from the same commit, launched with `--social-probe-run` and an unused UUID so it opened an empty isolated store, captured with `screencapture -o -l <window>`. They show only the built-in sample photographs. No personal library, project or Photos content is visible.
- **Device presentations** (`build148-framed-*`, `build148-aura-framed-*`): frames-cli could not be reinstalled for this pass, so the existing Apple Frames bezels were reused. `oct06-framed-phone-camera`, `oct06-framed-builder` and `oct06-framed-mac` were made from known captures; the screen is exactly the set of pixels where each framed image equals that capture (98.7% phone, 99.9% iPad, 99.6% Mac, located by exact pixel matching). Those pixels were replaced with the new capture at identical size; bezel, corner and camera-housing pixels were kept. `scripts/build_decks_build148_assets.py` records the method for each file.
- **Native renders** (`build148-stamp-*`, `build148-design-*`): `scripts/render_decks_build148.swift` with IngestSocialKit at `42c30ae` in an isolated store. Stamps use each photo's own capture date (Example40 Digital; Coffee Clean with time; Burger Typewriter, Sideways on Vertical Photos). Designs are started the way Home starts them: Gear Band on Example27, Wall Label on Example29, Spine on Example24, and Spec Sheet on Brian's original `~/Downloads/Decks/DSCF0205.JPG`, whose recorded Classic Negative recipe appears as dials. No recipe name was invented.

Deliberately not shown: the Decks Pro sheet, trial or pricing screens, the free-export counter, and Film-style exports. The Stamp panel's style row shows the app's own small PRO label on the Film tile; that is unmodified app UI. The iPhone Aura capture test still cannot reach the All Destinations chip at the end of the destination row, so the Aura steps use the iPad captures. The earlier `oct06-*`, `oct08-*` and `build132-*` files remain for existing links.
