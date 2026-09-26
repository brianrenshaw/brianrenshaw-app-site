# Listing Namer assets

Icon: copied from the native Listing Namer AppIcon asset.
Contact Sheet and Preview: native macOS app captures using isolated demo jobs. Three photographs repeat in the fixture; these are not a real client listing.

Photography from Unsplash, under the Unsplash License (https://unsplash.com/license):
- Lisa Anna: https://unsplash.com/photos/a-large-open-concept-kitchen-and-living-room-mNrSV2tB35g
- Bailey Alexander: https://unsplash.com/photos/a-living-room-filled-with-furniture-and-a-kitchen-PE4pFgcYzoQ
- Bailey Alexander: https://unsplash.com/photos/a-living-room-filled-with-furniture-and-a-kitchen-RbbZn_M5fgU

Version 1.0.1 assets use the Walkthrough native icon and the refreshed dark workspace captures in Review/PhotoStudio. The walkthrough image is an unmodified native UI-test capture of the naming-philosophy step.

## Walkthrough 1.1.0
Versioned 1.1.0 screenshots are unmodified native Dark appearance captures from the app repository’s Review/PhotoStudio and Review/SettingsExport collections. They use isolated demonstration libraries and the same credited photo fixtures above. These versioned captures remain with the historical release assets.

## Walkthrough 1.2.0

The `native-*-1.2.0.png` images are unmodified macOS UI-test captures of the redesigned workspace, centered command palette, group rename flow, Settings, and export sheets. Workspace captures use an isolated 100-photo, 18-room demonstration job and the same credited photography above. Getting Started uses a fresh empty demonstration library. The guide, support page, and landing page use these captures. Release-version assets are retained unchanged.

## Walkthrough 1.2.3

`native-tabs-1.2.3.png` is an unmodified native UI-test capture of macOS tabs and removable Recents, using an isolated demonstration library. It contains no customer photographs or listing information.

## Walkthrough 1.3.0

The four `native-export-*-1.3.0.png` images are unmodified Dark appearance native UI-test captures at 1440×900 points, taken September 19, 2026. They show separate naming-warning and skip-error controls using the isolated demonstration library and credited photographs above.

## Walkthrough 1.4.1

All `native-*-1.4.1.png` screenshots are unmodified native macOS window captures of the 1.4.1 implementation using an isolated demonstration library, the credited photographs above, and fictional listing/business details. Captured September 20, 2026 in Dark appearance, plus a Light workspace capture. Update checking is disabled in the isolated screenshot fixture. The teal icon is copied directly from the native 1024px AppIcon asset. Current landing, guide, support, and social metadata use these assets; historical assets remain unchanged.

## Walkthrough 1.4.1 website refresh, September 20, 2026

The four `native-*-1.4.1-retina.webp` images show Contact Sheet, the command bar, the Standard naming preset, and Copy export review. They were captured from a fresh Debug build of the clean 1.4.1 (12) source using its isolated-library screenshot hooks. The library is a copy of the existing demonstration fixture; the photos are the same credited fixture images above, and the address is fictional. No personal jobs or client photos appear. No export was performed.

Captures use `screencapture -x -o -a -l WINDOW_ID` without `-C`. The workspace and Settings are 1222 × 820 logical points (2444 × 1640 pixels); the export sheet is 860 × 660 points (1720 × 1320 pixels). Encode with `cwebp -lossless -exact -z 9 -metadata icc`, without resizing; ICC can also be retained with `webpmux -set icc`. Decoded RGBA pixels and ICC color profiles were verified against the original PNG captures. `screenshots.json` records dimensions; each HTML image preserves its logical display-width limit. Historical PNG captures remain unchanged.

## Walkthrough 1.4.2 dark-mode refresh

All `native-*-1.4.2.png` captures are original, unretouched PNG screenshots of the updated app in Dark appearance, captured September 26, 2026 with `NativeWorkspaceTests.testWebsiteDarkScreenshots`. The fictional listing uses an isolated library and the existing credited demonstration-photo set. No photo processing is confirmed during capture. Workspace images are captured at 1440 × 900 points, settings at the native settings size, and dialogs at their native sheet sizes; HTML width/height attributes preserve the original 2× pixel dimensions.

The five-step guide shows Open, Group, Order, Name, and Process Photos. The workspace and Process Photos screenshots are also bundled in the app. The 1.4.1 screenshots remain archived, while current pages reference this dark capture set.
