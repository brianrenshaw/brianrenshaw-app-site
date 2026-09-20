# Brian Renshaw’s app websites

Canonical website: https://brianrenshaw.app/

One static website for Reading Habit, Where Do We Eat, Who’s First?, and Folio. App source code remains in its existing repositories. Edit public website content here; legacy Pages repositories preserve older links.

## App messaging

Read [MESSAGING.md](MESSAGING.md) for each app’s purpose and copy priorities before changing app descriptions. For Walkthrough, also read [WALKTHROUGH_MESSAGING_PHILOSOPHY.md](WALKTHROUGH_MESSAGING_PHILOSOPHY.md): explain the tools and workflow directly, without slogans or exaggerated promises. The messaging guide also points to app-folder references for future native and App Store work.

## Local preview and checks

```sh
python3 scripts/check_site.py
python3 -m http.server 8080 --directory site
```

`check_site.py` also fails on British spellings. The copy is American English throughout: color, favorite, behavior, recognize, canceled. Extend the word lists in that script rather than letting an exception through.

Open http://localhost:8080/. Links are root-relative because production is served from the custom domain root. The default GitHub project URL is not a supported preview without that domain; use the local server.

GitHub Actions validates links, anchors, local assets, canonical addresses and American spelling before deploying `site/` to Pages on pushes to main. Pull requests validate without deploying. No build framework, package installation, analytics, or external font dependency is needed.

## Routes

| App | Path | Supporting pages |
| --- | --- | --- |
| Reading Habit | `/reading-habit/` | `guide/`, `support/`, `privacy/` |
| Where Do We Eat | `/where-do-we-eat/` | `guide/`, `support/`, `privacy/` |
| Who’s First? | `/whos-first/` | `support/`, `privacy/` |
| Folio | `/folio/` | `support/`, `privacy/` |
| Canceled | `/canceled/` | none yet |
| Ingest | `/ingest/` | `quick-start/`, `guide/`, `shortcuts/`, `templates/`, `automation/`, `support/`, `privacy/`, `release-notes/` |

Support email remains contact@brianrenshaw.app. Keep app-specific privacy policies accurate; don’t substitute a generic portfolio policy. Existing policy language was preserved, and Reading Habit’s new policy reflects its local implementation (private iCloud, Open Library/Apple cover lookups, user-selected link resolution and imports).

See `MIGRATION.md` for rollout status, legacy mapping, DNS, Apple metadata and rollback. See `.21st/DESIGN.md` for the four visual directions.

Two blogs are linked from homepage cards without local pages: Lankford Legends (https://lankfordlegends.co/) and What Did They Read? (https://www.whatdidtheyread.com/). Both are built in the sibling `blog-explorer` repository. Their card copy is in `MESSAGING.md`.

Spreadsheet Tools lives at `/spreadsheet-tools/`. Its React source remains in the sibling `spreadsheet-webapp` repository (`brianrenshaw/spreadsheet-tools` on GitHub). Run that project's `scripts/sync-website.py` to rebuild and copy generated files here, then commit and push this repository. Keep the utility link at the bottom of the portfolio. See that project's `WEBSITE_MIGRATION.md` for the complete workflow.

Walkthrough (formerly Listing Namer) is at `/walkthrough/`, with `guide/`, `support/`, `privacy/`, and `release-notes/`. Its native source is in the private sibling `real-estate-photos-renamer` project / `brianrenshaw/listing-namer` repository. Public DMGs are GitHub Release assets in this website repository; they are not committed into `site/`. See `LISTING_NAMER_RELEASES.md` for the release handoff. The current download is signed and notarized Walkthrough 1.4.1, build 12.

### Do not delete the `folio-privacy` Pages repository

Folio 1.1.2 (18) is the build on the App Store, and its Settings screen opens `https://brianrenshaw.github.io/folio-privacy/`. The move to `brianrenshaw.app/folio/privacy/` is committed in the app project but has not shipped, so every installed copy still uses the old address. That URL is live and its policy is substantively identical to the current one, same headings and the same August 26, 2026 date. Folio 1.1.3 (19) carries the new URL and was uploaded to App Store Connect on September 18, 2026; it is not released yet. Keep the legacy repository published until a build carrying the new URL has replaced 1.1.2 for everyone, because an App Store app needs a working privacy policy link. This is the same constraint as the Sparkle feed below, for the same reason.

### Do not delete `site/listing-namer/`

Walkthrough moved from `/listing-namer/` to `/walkthrough/` on September 17, 2026. The old path is not dead weight:

- **`site/listing-namer/appcast.xml` must stay exactly where it is, permanently.** Every shipped copy of the Mac app, 1.0 through 1.2.1, has `SUFeedURL = https://brianrenshaw.app/listing-namer/appcast.xml` compiled into its `Info.plist`. Sparkle needs real XML at that URL, and GitHub Pages cannot issue a redirect. Move or delete this file and every existing installation silently stops receiving updates. Publishing a release still means updating this file, not a copy under `/walkthrough/`. Only after a future build ships with a new `SPARKLE_FEED_URL`, and every user has taken it, could that change, which in practice means never.
- The five `index.html` files under `site/listing-namer/` are redirect stubs to `/walkthrough/`, following the same pattern as the older `/chooser/` stubs. They carry the query and hash across, which matters because Sparkle opens release notes at `/release-notes/#v1.2.1` and older builds still ask for the old path.

`scripts/check_site.py` asserts the feed and all five stubs exist, so this cannot be removed by accident.

Release notes are published at `/walkthrough/release-notes/`, with links in the native app’s Help menu and Settings. Public copy explains grouping listing photos by room, arranging their order, and exporting numbered filenames, for realtors and listing assistants. Avoid guarantees about how an MLS or website orders uploads. Read the Walkthrough section of `MESSAGING.md` before changing it, including the rule against describing settings export as “sync.”

Canceled is at `/canceled/`, a landing page only. The app is in development for iPhone and iPad, is not on TestFlight, and has nothing to download, so the page states status and offers no call to action. Its native source is in the sibling `canceled-app` project. Add `support/` and `privacy/` when it reaches TestFlight, and add `canceled` to the required-routes list in `scripts/check_site.py` at the same time. Page assets under `site/canceled/assets/` are copied from that project; its Archivo woff2 is the same file already bundled for Where Do We Eat.

The homepage grid is grouped by platform: iOS apps, then the Mac app, then the blogs, then the utility. See `MESSAGING.md` for the numbered order. The share image `assets/social-projects-v10.png` holds ten projects, three rows of three plus one; rebuild it with `python3 scripts/build_social.py` and bump the filename plus both metadata URLs when the artwork changes.


Ingest is at `/ingest/`, the second Mac app. Its native source is in the private sibling `photo-importer` project. Public DMGs are GitHub Release assets in this repository, tagged `ingest-v*`; they are not committed into `site/`. See `INGEST_RELEASES.md` for the release handoff. The current download is signed and notarized Ingest 0.3.1, build 8.

The Sparkle feed for Ingest is `site/ingest/appcast.xml`, and every shipped build has that URL compiled into it, so the path is permanent. `scripts/check_site.py` asserts the file exists.

Anchor ids under `/ingest/` are a contract. The app's Help menu links to `/ingest/guide/`, `/ingest/shortcuts/`, `/ingest/release-notes/`, and `/ingest/support/`, the appcast links to `/ingest/release-notes/#vX.Y.Z`, and the pages link to each other's sections. Rename a section heading if you like, but leave its `id` alone.

Facts that live in exactly one place, because the site has no includes: shortcuts on `/ingest/shortcuts/`, name tokens and quick entry on `/ingest/templates/`, requirements and file formats on `/ingest/support/`, the URL scheme and the settings file on `/ingest/automation/`, network behavior on `/ingest/privacy/`. Everything else links to those. The shortcut tables are transcribed from `Sources/Ingest/Commands/CommandCatalog.swift`; diff them against that file at each release, because the link checker cannot catch a wrong key.

### Ingest screenshot quality

Use macOS native `screencapture -x -o -a -l WINDOW_ID capture.png` for app screenshots.
Do not include `-C` (cursor). Use an isolated demo library and capture the released app
at native Retina resolution. Encode lossless WebP without resizing; verify decoded
pixels match the PNG. Keep fonts, colors, and native controls unchanged.

`site/ingest/assets/screenshots.json` records physical and logical dimensions. Every
screenshot limits its CSS width to the native logical width, preserving at least 2×
density. Fresh filenames invalidate cached captures; legacy aliases receive the same
new bytes. Run `python3 scripts/check_ingest_screenshots.py` and visually inspect all
captures and desktop/mobile pages before pushing. CI checks encoding, dimensions,
aliases, and display-size limits; cursor absence still requires visual review.

Walkthrough’s refreshed landing screenshots are native 2× captures with lossless WebP encoding. Their source and capture procedure are recorded in `site/walkthrough/assets/SOURCES.md`; `screenshots.json` records pixel and logical dimensions. Preserve the per-image `--capture-width` limit and intrinsic dimensions when moving these images between pages.
