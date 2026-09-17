# Listing Namer publishing

- Native source: sibling `../real-estate-photos-renamer`, private GitHub repository `brianrenshaw/listing-namer`.
- App page and homepage card: this repository, `site/listing-namer/` and `site/index.html`.
- Feed: `site/listing-namer/appcast.xml`, served at `https://brianrenshaw.app/listing-namer/appcast.xml`.
- Downloads: public GitHub Releases in `brianrenshaw/brianrenshaw-app-site`, with tags prefixed `listing-namer-`.

The first release is `listing-namer-v1.0.0-preview`, containing `Listing-Namer-1.0.0-preview.dmg`. It is Developer ID signed but not notarized. The page and release notes disclose this; the feed has no installable update until notarization is configured. Do not represent this as the final public release.

For each notarized release:

1. Run the native project's `release.sh`, with an increasing BUILD_NUMBER, VERSION, NOTARY_PROFILE, and `SPARKLE_DOWNLOAD_URL_PREFIX=https://github.com/brianrenshaw/brianrenshaw-app-site/releases/download/listing-namer-vVERSION/`.
2. Upload the completed DMG to that GitHub release first. Preserve immutable release filenames and tags.
3. Copy its generated `dist/updates/appcast.xml` into this site's `site/listing-namer/appcast.xml`. The private signing key stays in the native publisher's Keychain; only the public feed is copied here.
4. Update the page download link and availability statement, run `python3 scripts/check_site.py`, commit, and push. Existing GitHub Pages deployment publishes the feed and page together.
5. Verify the live feed and DMG URLs, then test an actual Sparkle upgrade from the previous installed version and reopen a saved job.

Screenshots are native app captures using demonstration photos. `site/listing-namer/assets/SOURCES.md` records image sources. Website content belongs here; do not create a separate website inside the native app repository.
