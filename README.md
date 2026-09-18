# Brian Renshaw’s app websites

Canonical website: https://brianrenshaw.app/

One static website for Reading Habit, Where Do We Eat, Who’s First?, and Folio. App source code remains in its existing repositories. Edit public website content here; legacy Pages repositories preserve older links.

## App messaging

Read [MESSAGING.md](MESSAGING.md) before changing app descriptions. It records the approved purpose and copy priorities for all four apps and points to self-contained app-folder references for future native and App Store work.

## Local preview and checks

```sh
python3 scripts/check_site.py
python3 -m http.server 8080 --directory site
```

Open http://localhost:8080/. Links are root-relative because production is served from the custom domain root. The default GitHub project URL is not a supported preview without that domain; use the local server.

GitHub Actions validates links, anchors, local assets and canonical addresses before deploying `site/` to Pages on pushes to main. Pull requests validate without deploying. No build framework, package installation, analytics, or external font dependency is needed.

## Routes

| App | Path | Supporting pages |
| --- | --- | --- |
| Reading Habit | `/reading-habit/` | `guide/`, `support/`, `privacy/` |
| Where Do We Eat | `/where-do-we-eat/` | `guide/`, `support/`, `privacy/` |
| Who’s First? | `/whos-first/` | `support/`, `privacy/` |
| Folio | `/folio/` | `support/`, `privacy/` |
| Canceled | `/canceled/` | none yet |

Support email remains contact@brianrenshaw.app. Keep app-specific privacy policies accurate; don’t substitute a generic portfolio policy. Existing policy language was preserved, and Reading Habit’s new policy reflects its local implementation (private iCloud, Open Library/Apple cover lookups, user-selected link resolution and imports).

See `MIGRATION.md` for rollout status, legacy mapping, DNS, Apple metadata and rollback. See `.21st/DESIGN.md` for the four visual directions.

Two blogs are linked from homepage cards without local pages: Lankford Legends (https://lankfordlegends.co/) and What Did They Read? (https://www.whatdidtheyread.com/). Both are built in the sibling `blog-explorer` repository. Their card copy is in `MESSAGING.md`.

Spreadsheet Tools lives at `/spreadsheet-tools/`. Its React source remains in the sibling `spreadsheet-webapp` repository (`brianrenshaw/spreadsheet-tools` on GitHub). Run that project's `scripts/sync-website.py` to rebuild and copy generated files here, then commit and push this repository. Keep the utility link at the bottom of the portfolio. See that project's `WEBSITE_MIGRATION.md` for the complete workflow.

Walkthrough (formerly Listing Namer) is at `/walkthrough/`, with `guide/`, `support/`, `privacy/`, and `release-notes/`. Its native source is in the private sibling `real-estate-photos-renamer` project / `brianrenshaw/listing-namer` repository. Public DMGs are GitHub Release assets in this website repository; they are not committed into `site/`. See `LISTING_NAMER_RELEASES.md` for the release handoff. The current download is signed and notarized Walkthrough 1.2.1, build 7.

### Do not delete `site/listing-namer/`

Walkthrough moved from `/listing-namer/` to `/walkthrough/` on September 17, 2026. The old path is not dead weight:

- **`site/listing-namer/appcast.xml` must stay exactly where it is, permanently.** Every shipped copy of the Mac app, 1.0 through 1.2.1, has `SUFeedURL = https://brianrenshaw.app/listing-namer/appcast.xml` compiled into its `Info.plist`. Sparkle needs real XML at that URL, and GitHub Pages cannot issue a redirect. Move or delete this file and every existing installation silently stops receiving updates. Publishing a release still means updating this file, not a copy under `/walkthrough/`. Only after a future build ships with a new `SPARKLE_FEED_URL`, and every user has taken it, could that change, which in practice means never.
- The five `index.html` files under `site/listing-namer/` are redirect stubs to `/walkthrough/`, following the same pattern as the older `/chooser/` stubs. They carry the query and hash across, which matters because Sparkle opens release notes at `/release-notes/#v1.2.1` and older builds still ask for the old path.

`scripts/check_site.py` asserts the feed and all five stubs exist, so this cannot be removed by accident.

Release notes are published at `/walkthrough/release-notes/`, with links in the native app’s Help menu and Settings. Public copy leads with the outcome: listing photos that upload to the MLS in the order you chose, for realtors and listing assistants. Read the Walkthrough section of `MESSAGING.md` before changing it, including the rule against describing settings export as “sync.”

Canceled is at `/canceled/`, a landing page only. The app is in development for iPhone and iPad, is not on TestFlight, and has nothing to download, so the page states status and offers no call to action. Its native source is in the sibling `canceled-app` project. Add `support/` and `privacy/` when it reaches TestFlight, and add `canceled` to the required-routes list in `scripts/check_site.py` at the same time. Page assets under `site/canceled/assets/` are copied from that project; its Archivo woff2 is the same file already bundled for Where Do We Eat.

The homepage grid is grouped by platform: iOS apps, then the Mac app, then the blogs, then the utility. See `MESSAGING.md` for the numbered order. The share image `assets/social-projects-v8.png` holds nine projects in a 3x3 grid; rebuild it with `python3 scripts/build_social.py` and bump the filename plus both metadata URLs when the artwork changes.
