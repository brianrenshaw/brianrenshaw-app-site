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

The feed path is permanent. Every shipped build has `https://brianrenshaw.app/ingest/appcast.xml` compiled into it, so
that file must keep serving real XML permanently. `scripts/check_site.py` asserts it exists.
Current releases embed self-contained HTML in the feed's `description`, so Sparkle can show the changes without another network request. Omit `sparkle:releaseNotesLink` for these items because Sparkle gives that external URL precedence over the embedded description. Use `sparkle:fullReleaseNotesLink` for the complete notes at `https://ingestphotoapp.com/release-notes/#vX.Y.Z`.
Older entries may retain a direct `sparkle:releaseNotesLink` to that same canonical page.
Keep the old `/ingest/release-notes/` HTML available for cached appcasts; Sparkle does not follow JavaScript redirects.

## Publishing a version

1. In `photo-importer`, run `release.sh` with a `BUILD_NUMBER` higher than any already in the feed. Apple must accept both
   the app and the disk image.
2. Create the GitHub release here and attach the disk image:

   ```sh
   gh release create ingest-vX.Y.Z /path/to/dist/Ingest-X.Y.Z.dmg \
     --repo brianrenshaw/brianrenshaw-app-site --title "Ingest X.Y.Z" --notes "…"
   ```

3. Copy `dist/updates/appcast.xml` to `site/ingest/appcast.xml`. Check that the current item's embedded notes contain the actual changes, its full-notes link has the correct version anchor, and previous signed enclosure attributes remain unchanged.
4. Add the release notes entry at `site/ingest/release-notes/` with `id="vX.Y.Z"`, matching the fragment the appcast links
   to, and put the new version first in `nav.release-index`.
5. Update the version string in the two places it appears: the download links on `site/ingest/index.html` and the line in
   `README.md` that names the current download.
6. `python3 scripts/check_site.py`, then commit and push. Pushing `main` deploys.
7. Open the feed URL and the disk image URL in a browser, then use Check for Updates in an installed copy and confirm it
   offers the new build, renders the embedded changes, and installs it. Verify the full notes as well. If a local network filter blocks the custom domain, do not disable TLS or change network controls; verify published content through the trusted Cloudflare deployment URL and the retained legacy HTML route, and report the limitation.

Keep `dist/updates` between releases in the native project, so earlier items stay in the feed.

## Things that will drift

The shortcut tables on `/ingest/shortcuts/` and the token tables on `/ingest/templates/` are transcribed from
`Sources/Ingest/Commands/CommandCatalog.swift` and `Sources/IngestCore/Templates/TemplateParser.swift`. The link checker
cannot catch a wrong key, so diff them against those files whenever the app's commands change.

Anchor ids under `/ingest/` are a contract: the app's Help menu, the appcast, and the pages themselves link to them.

## History

| Version | Build | Date | Notes |
| --- | --- | --- | --- |
| 0.9.8 | 48 | October 6, 2026 | Native title-bar controls, adaptive source tabs, a new welcome, compact Browse by, Scenes removal, and closed-eye palette filtering. |
| 0.9.7 | 47 | October 6, 2026 | Guided Workspace Builder, named photo groups, resolved metadata previews, independently scoped actions, consistent macOS controls, and Decks iCloud transfers. |
| 0.9.6 | 42 | October 5, 2026 | Send to Decks replaces the built-in Social Export editor. |
| 0.9.5 | 41 | October 5, 2026 | Review queue and face inspection, independent editors, Import Settings, reliable eye assessments, shortcuts, and steadier navigation. |
| 0.9.4.6 | 40 | September 30, 2026 | Photo Suggestions shows one section per set of similar shots and leaves out photos with nothing to compare; a group bar, clickable headings and [ ] move between group-by sections, scenes and suggestion sets. |
| 0.9.4.5 | 39 | September 30, 2026 | Sort by Visual appeal (the stored on-device estimate, highest first, unassessed last) replaces Photo Suggestions' Find highlights mode, which excluded most photos of people and buried its picks. |
| 0.9.4.4 | 38 | September 30, 2026 | Ingest sidebar rebuilt in three planes with one destination tree, project job folders follow the Subfolders template, sharper focus peaking, ranked palette metadata searches, Metadata Assist location summary, and metadata read retries. |
| 0.9.4.3 | 37 | September 27, 2026 | Saved GPS locations, photo-by-photo Metadata Assist, explicit import scopes, and import/export reliability fixes. |
| 0.9.4.2 | 36 | September 25, 2026 | Informational retained-pair receipts, conservative cleanup checks, and stable Focus Mode window bounds. |
| 0.9.4.1 | 35 | September 25, 2026 | Focus Mode synchronization, Settings layout and narrow-window fixes, and Basic card-handling value correction. |
| 0.9.4 | 34 | September 25, 2026 | Reviewed camera/lens and exposure metadata for film scans, saved equipment, folder-preview fixes, and clearer Settings contrast. |
| 0.9.3 | 33 | September 25, 2026 | Sharper Social Export with Sharpen for Screen, no enlarging by default, Actual Pixels, size estimates, and full-bleed starters for every Instagram shape. |
| 0.9.2 | 32 | September 25, 2026 | Simpler workspace settings and refreshed five-screen walkthrough with Metadata Assist. |
| 0.9.1 | 30 | September 25, 2026 | Visible tag and selection filters, selection-based import, workspace defaults, unified metadata editing, Focus Peaking, and thumbnail spacing. |
| 0.9.0 | 29 | September 25, 2026 | Metadata Assist, local history and Tab completion, workspace and Focus Mode controls, learning tips, and progressive photo browsing. |
| 0.8.6 | 28 | September 24, 2026 | Screenshot walkthrough on first launch, Getting Started guide, workspace Photos switches, and large-library Photos performance fixes. |
| 0.8.5 | 27 | September 24, 2026 | Includes 0.8.4 refinements and fixes blocked folder-watch setup during restored-session launch. |
| 0.8.4 | 26 | September 24, 2026 | Withdrawn: startup stall with slow folder providers. Quiet dark surfaces, folder search in the palette, metadata facets, per-workspace sidebar controls, and direct Organize entry. |
| 0.8.3 | 25 | September 24, 2026 | Burst stacks, optional scene sections, persistent scene corrections, and review through the existing views. |
| 0.8.2 | 24 | September 24, 2026 | Review and protection, grid loupe, Select/Candidate and whole-stack Survey, visual keeper suggestions, crop and metadata editing, source tools, and ingest safety. |
| 0.8.1 | 23 | September 23, 2026 | Vision culling assists (similar stacks, faces, Soft), Workspaces with per-tab settings, Compare as one mode with drag-to-pan, a one-list sidebar, the histogram counted from the preview, a redesigned Camera Details card, and budgets for 16 GB Macs. |
| 0.8.0 | 22 | September 22, 2026 | Apple Photos as a source inside Browse, a rebuilt photo bar with sortable order and a filter panel, the Ingest tab with routed destinations, the keyword manager, and new typography. |
| 0.7.8 | 21 | September 22, 2026 | Explain iCloud-only preview waits in the Photos workspace and Settings. |
| 0.7.7 | 20 | September 22, 2026 | Bounded album preview warmup, visible cloud fetching, and immediate fallback images. |
| 0.7.6 | 19 | September 22, 2026 | Responsive native Photos browsing, progressive cached previews, and independent inspector loading. |
| 0.7.5 | 18 | September 21, 2026 | Recipe controls above the details and an optional after-ingest confirmation. |
| 0.7.4 | 17 | September 21, 2026 | Restore recipe details on Cancel, clarify keyword actions, and queue card recipe edits after ingest. |
| 0.7.3 | 16 | September 21, 2026 | Fujifilm JPEG recipe notes, simulation keywords, and Copy/Text/Markdown export. |
| 0.7.2 | 15 | September 21, 2026 | Shared Photos browsing layout with Grid, Preview, Split, and right-hand Photo Info. |
| 0.7.1 | 14 | September 21, 2026 | Fix signed-release Photos permission and blocked connection handling. |
| 0.7.0 | 13 | September 21, 2026 | Optional Apple Photos workspace, albums, reviewed JPEG-first sends, metadata, and Social Export integration. |
| 0.6.0 | 12 | September 21, 2026 | RAW sensor histograms, same-photo preview comparison, configurable Photo Info, reviewed AI suggestions, and structured metadata. |
| 0.5.0 | 11 | September 21, 2026 | Folder browsing, simpler tagging, richer Social Export, and workflow improvements. |
| 0.4.1 | 10 | September 21, 2026 | Live Social previews, automatic layouts, explicit navigation/import, filmstrip selection, export sheet, project cleanup, and Organize setup/resume. |
| 0.4.0 | 9 | September 21, 2026 | Social Export compositions and saved projects, Organize workspace, and workflow improvements. |
| 0.3.1 | 8 | September 20, 2026 | Refresh filmstrip thumbnails when preview information arrives. |
| 0.3.0 | 7 | September 20, 2026 | Expanded camera formats, RAW + JPEG/HEIF pairing, XMP metadata, folder refresh, and safer interrupted imports. |
| 0.2.1 | 6 | September 20, 2026 | Native editing fixes, accessible shortcut recording, contextual palette Actions, and appearance polish. |
| 0.2.0 | 5 | September 20, 2026 | The Studio design pass: Archivo throughout, sectioned inspector, two-stage ingest bar, and a completion receipt that reports what is still only on the card. |
| 0.1.0 | 4 | September 18, 2026 | First public release. Signed, notarized, stapled. macOS 15 or later, Apple silicon only. |

Release-note source is `docs/ingest/release-notes.json`, newest version first. Add release content there without dates, then run `python3 scripts/build_ingest_release_notes.py` to regenerate the version pages, latest page, dropdown, legacy anchors, and search destinations. Preserve the permanent appcast and its signed enclosure metadata.
