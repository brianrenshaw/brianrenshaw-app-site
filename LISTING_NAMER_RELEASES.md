# Walkthrough publishing

- Native source: sibling `../real-estate-photos-renamer`, private GitHub repository `brianrenshaw/listing-namer`.
- App page and homepage card: this repository, `site/listing-namer/` and `site/index.html`.
- Feed: `site/listing-namer/appcast.xml`, served at `https://brianrenshaw.app/listing-namer/appcast.xml`.
- Downloads: public GitHub Releases in `brianrenshaw/brianrenshaw-app-site`, with tags prefixed `listing-namer-`.

The current public release is `listing-namer-v1.1.0`, Walkthrough version 1.1.0 build 5. Its universal app and DMG are Developer ID signed, notarized, and stapled. The website feed offers build 5 to existing installations and preserves earlier release download URLs.

For each notarized release:

1. Run the native project's `release.sh`, with an increasing BUILD_NUMBER, VERSION, NOTARY_PROFILE, and `SPARKLE_DOWNLOAD_URL_PREFIX=https://github.com/brianrenshaw/brianrenshaw-app-site/releases/download/listing-namer-vVERSION/`.
2. Upload the completed DMG to that GitHub release first. Preserve immutable release filenames and tags.
3. Copy its generated `dist/updates/appcast.xml` into this site's `site/listing-namer/appcast.xml`. The private signing key stays in the native publisher's Keychain; only the public feed is copied here.
4. Update the page download link and availability statement, run `python3 scripts/check_site.py`, commit, and push. Existing GitHub Pages deployment publishes the feed and page together.
5. Verify the live feed and DMG URLs, then test an actual Sparkle upgrade from the previous installed version and reopen a saved job.

Screenshots are native app captures using demonstration photos. `site/listing-namer/assets/SOURCES.md` records image sources. Website content belongs here; do not create a separate website inside the native app repository.

## 1.0.2

Version 1.0.2, build 4, adds the refined house icon, purpose-focused Getting Started copy, and Release Notes links in Help and Settings. Public history: `/listing-namer/release-notes/`, with `#v1.0.2` and a stable anchor for every release. For future updates, add an undated, user-facing entry, refresh changed native captures, upload the versioned DMG, then publish the matching appcast and website version together. The native appcast postprocessor supplies release-note links and preserves older download URLs.

## 1.1.0
Command palette, keyboard ordering, native toolbar, grouped Copy/Move exports, and refreshed Settings. The illustrated guide at `/listing-namer/guide/` documents the shipped behavior. Release notes have one Updated date at the bottom. Screenshots use native 1.1.0 captures.
