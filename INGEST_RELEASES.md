# Releasing Ingest

Ingest's native source is in the private sibling `photo-importer` project. Its full release procedure, including signing
and notarization, is in that project's `RELEASE.md`. This file covers the part that happens here.

## What lives in this repository

| Thing | Where |
| --- | --- |
| The pages | `site/ingest/` |
| The Sparkle feed | `site/ingest/appcast.xml` |
| The disk images | GitHub Release assets, tagged `ingest-vX.Y.Z` |
| Release notes | `site/ingest/release-notes/`, one `article.release-entry` per version with `id="vX.Y.Z"` |

The feed path is permanent. Every shipped build has `https://brianrenshaw.app/ingest/appcast.xml` compiled into it, and a
static host cannot redirect, so that file must keep serving real XML for ever. `scripts/check_site.py` asserts it exists.

## Publishing a version

1. In `photo-importer`, run `release.sh` with a `BUILD_NUMBER` higher than any already in the feed. Apple must accept both
   the app and the disk image.
2. Create the GitHub release here and attach the disk image:

   ```sh
   gh release create ingest-vX.Y.Z /path/to/dist/Ingest-X.Y.Z.dmg \
     --repo brianrenshaw/brianrenshaw-app-site --title "Ingest X.Y.Z" --notes "…"
   ```

3. Copy `dist/updates/appcast.xml` to `site/ingest/appcast.xml`.
4. Add the release notes entry at `site/ingest/release-notes/` with `id="vX.Y.Z"`, matching the fragment the appcast links
   to, and put the new version first in `nav.release-index`.
5. Update the version string in the two places it appears: the download links on `site/ingest/index.html` and the line in
   `README.md` that names the current download.
6. `python3 scripts/check_site.py`, then commit and push. Pushing `main` deploys.
7. Open the feed URL and the disk image URL in a browser, then use Check for Updates in an installed copy and confirm it
   offers the new build and installs it.

Keep `dist/updates` between releases in the native project, so earlier items stay in the feed.

## Things that will drift

The shortcut tables on `/ingest/shortcuts/` and the token tables on `/ingest/templates/` are transcribed from
`Sources/Ingest/Commands/CommandCatalog.swift` and `Sources/IngestCore/Templates/TemplateParser.swift`. The link checker
cannot catch a wrong key, so diff them against those files whenever the app's commands change.

Anchor ids under `/ingest/` are a contract: the app's Help menu, the appcast, and the pages themselves link to them.

## History

| Version | Build | Date | Notes |
| --- | --- | --- | --- |
| 0.2.1 | 6 | September 20, 2026 | Native editing fixes, accessible shortcut recording, contextual palette Actions, and appearance polish. |
| 0.2.0 | 5 | September 20, 2026 | The Studio design pass: Archivo throughout, sectioned inspector, two-stage ingest bar, and a completion receipt that reports what is still only on the card. |
| 0.1.0 | 4 | September 18, 2026 | First public release. Signed, notarized, stapled. macOS 15 or later, Apple silicon only. |
