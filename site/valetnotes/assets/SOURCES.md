# Valet Notes website screenshots

Captured October 22, 2026 from the `top-drawer` project at commit `0bbc42f` (build 19 source). All writing in the screenshots is demo text seeded into an isolated store with `TOP_DRAWER_DATA_DIR`; no real notes were used. The app's default Classic theme is shown.

- **iPhone and iPad.** A capture-only UI test, `WebsiteCaptureUITests.testWebsiteCaptures`, ran in an exported copy of the source (`git archive`), so the app repository was not changed. Simulators: iPhone 17 Pro and iPad Air 11-inch (M4), iOS 27.0, status bar overridden to 9:41 with full signal and battery. The iPad ran in landscape; XCUIScreen stores those captures in portrait pixel order, so they are rotated 90 degrees to upright.
- **Mac.** A separate TopDrawerMac Debug instance was launched with the demo store and `-appearanceTheme classic`, and its drawer window was captured with `screencapture -x -o -l <window>` on a 2056-point-wide display. `mac-drawer-first-spaces.webp` is the left half of that capture.

`scripts/build_valetnotes_assets.py` packages everything: lossless WebP with decoded pixels verified against the source, device frames made by replacing the screen pixels of the Apple Frames bezels already on the Decks site, and `social.png`. iPhone and iPad captures match those bezels' screen sizes and are not resampled. The Mac drawer is scaled from 4112 to 3024 pixels wide to fit the 14-inch frame and sits below the menu bar area on a plain green desktop; nothing else was added to the screen. `screenshots.json` records sizes, hashes, and these transformations. `python3 scripts/build_product_previews.py` makes the responsive sizes.

`fonts/` holds the unmodified iA Writer Duo files bundled with the app, under the SIL Open Font License (`LICENSE.txt`, `SOURCE.txt`). They are not subset or converted because the license reserves the font name for unmodified versions. `icon.png` is the app's 1024-pixel icon resized to 256.
