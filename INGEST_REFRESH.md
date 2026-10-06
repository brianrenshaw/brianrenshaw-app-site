# Ingest editorial homepage — October 6, 2026

Production publication authorized by Brian on October 6, 2026.

## Product story and design

The homepage leads with “Modern photo management for Mac.” Its visible chapters cover the photographer's problem, workspaces for five shoot types, reusable project questions and naming, Command-K, Review, Metadata Assist, verified importing and editor handoff, existing-folder organization, specialist tools, Decks, and a three-step start with Brian's story. There is one supporting Photo Mechanic mention and no parity or fastest-performance claim.

The static HTML/CSS architecture is retained. Homepage layout is scoped to the homepage, with warm neutral surfaces, system typography, charcoal text, amber accents, substantial native screenshots, and full-resolution links. No video, automatic hero rotation, simulated app UI, new framework, or hidden primary feature descriptions. Responsive styles adapt the website for visitors on phones; Ingest is consistently presented as a Mac app, using Mac screenshots only.

Old homepage IDs remain as section anchors or aliases. Historical image/video bytes, release history, public routes, and the permanent appcast path are retained. Existing unrelated Decks work is preserved. Supporting documentation received release 0.9.8 behavior corrections, including the removed Scenes option, current navigation, and tone-versus-sensor histogram wording. The portfolio Ingest headline, search entries, share artwork, MESSAGING.md, and .21st design records agree with the new positioning.

## Build and capture evidence

All new Ingest screenshots use local build **0.9.8 (48)** from source `0c84a1adaa196cf473ad506e0814699e80c17105`. The later source HEAD `62cc685` contains release records only. The public GitHub release `ingest-v0.9.8` was published at `2026-10-06T20:21:17Z`; the app's `docs/release-0.9.8.json` identifies the same source commit, signed/notarized artifact, and verified download. On-page downloads and search fallback use that released DMG.

The isolated app uses `/tmp/ingest-editorial-captures/Library`. It does not replace the installed app. Native captures preserve original Retina RGBA pixels in lossless WebP; dimensions, source version, and PNG hashes live in `site/ingest/assets/screenshots.json`. Full capture and licensing provenance is in `site/ingest/assets/SOURCES.md`. Twelve new native captures appear directly on the homepage; the thirteenth supplies the framed hero and appears unchanged in the guide. One alternate hero is archived.

Hands-on verification covered Workspace Builder and its save preview, Command-K, Review faces, RAW/JPEG comparison, Metadata Assist `;loc` + Map Location + Return, actual Apple Maps results, a verified demo import, Organize preview, client pick-list matches, and Camera & Lens fields. Metadata and organization drafts were not applied to originals. One RAW and its XMP were actually imported and verified in a disposable destination.

Source/guide verification supplies conditional behavior for Fujifilm JPEG recipes, Apple Photos global/workspace requirements and supported fields, cross-card numbering, sensor histograms, and after-import scopes. This is not a new end-to-end test of Lightroom, a second physical backup drive, iCloud, or every third-party metadata reader. Copy distinguishes GPS from descriptive IPTC locations, shared metadata from internal tags, and Decks photo transfer from workspace settings. Scene grouping is omitted because 0.9.8 removed it.

At Brian's request, the hero uses a silver MacBook frame from Frames CLI around a proportional copy of the genuine app window. It is recorded as marketing artwork separately from the native capture. Other screenshots remain unframed; clicking the hero opens the unchanged original. Desktop places the promise and MacBook side by side. The Decks legacy anchor was moved inside the text block so it cannot consume a grid cell. See SOURCES.md.

## Validation

- `python3 scripts/check_site.py`: passed all routes, anchors, local assets, canonical URLs, fonts, and copy checks.
- `python3 scripts/check_ingest_screenshots.py`: passed genuine-capture manifest, encoding, dimensions, checksums, and display-size checks; no active video sources.
- `python3 scripts/build_ingest_site.py`: passed dedicated-domain output, search/anchors, feed, and Cloudflare file-size checks.
- `python3 scripts/build_portfolio_site.py`: passed legacy redirects, sitemap, assets, and permanent feed checks.
- `node scripts/check_ingest_interactions.cjs`: passed the retained historical video-controller regression checks. The new homepage does not load that controller.
- `21st review site/ingest/index.html site/ingest/assets/landing.css`: six informational intentional-color findings; no required fix. Catalog search returned HTTP 401, so project primitives were reused.
- Native Chrome: inspected desktop and phone-width hero/chapter layouts; exercised image enlargement, Tab focus containment, Escape dismissal and focus return, Command-K search, and result navigation. With JavaScript disabled, the product story and image links remain usable; the inactive Search control is hidden. JavaScript was restored after testing.
- `git diff --check`: passed. Homepage legacy IDs were compared against the original; none were removed. Appcast has no diff from this task.

## Publication handoff

Publication uses an isolated checkout based on the latest production commit `3781b75`, preserving its 0.9.8 Sparkle feed byte-for-byte. Only Ingest changes are included; unrelated Decks work remains in the original working tree. The latest published GitHub release was rechecked as 0.9.8 before publication.

## Guide and Support follow-up

At Brian's request, Guide and Support now use a shared documentation layout: six workflow groups in the guide, six problem-based groups in support, desktop sticky topic navigation, compact native disclosure navigation, task shortcuts, section return links, and existing Command-K search. All original anchors remain. New sections cover client pick lists, multi-camera capture-time adjustment, and Fujifilm recipes; support adds workspace, review, location, pick-list, recipe, after-import, and Decks troubleshooting. Fresh native captures replace relevant older examples.

Behavior was checked against 0.9.8 source and the capture work above, including all-loaded-camera scope for time adjustment, GPS versus descriptive place names, file/number pick-list matching, workspace preferences, and tagged-copy after-import scope. Search includes the new sections. The enhancement is optional: native topic disclosures and anchor navigation remain functional without JavaScript.

Documentation validation: site and capture checks, dedicated/portfolio builds, JavaScript syntax, and diff whitespace checks passed. `21st review` of Guide, Support, docs.css, and docs.js returned zero findings. Native Chrome verified the desktop guide sidebar, capture-time anchor and search result, and compact Support disclosure plus location-topic jump.

## Wiki-style documentation follow-up

Brian approved the supporting hero line “Your photo workflow shouldn’t feel stuck in the ’90s.” Guide, Support and Shortcuts are now categorized directories leading to 68 focused static articles. Getting Started, Naming & Metadata, and Automation share the compact help shell. Existing anchors remain on the directories; JavaScript redirects old links to the corresponding article and no-script visitors get a normal article link. Search favors title matches and help articles in the help center.

Desktop uses a sticky collapsible sidebar and breadcrumbs. Compact screens use native navigation disclosure and labeled stacked table rows, preserving keyboard shortcuts with 12px keycaps. Article headings are 26–32px. Real screenshots and feature content remain unchanged. Native Chrome verified desktop guide layout, the 393px shortcut view, legacy anchor routing, search to capture-time instructions, and no-script navigation; scripting was restored. 21st catalog returned HTTP 401; existing project primitives were reused.

Ingest brevity pass: homepage copy reduced by roughly half. Screenshots are static illustrations, with no enlargement links, popup script, or version captions. Detailed instructions stay in the wiki. Lead handoff with Open in Lightroom Classic. Keep exact Mac and optional Apple Intelligence/Photos compatibility wording in a short section. Footer has Support, Release notes, and Privacy only. Release notes use undated per-version pages and a native version dropdown; old anchors remain compatible.

Help articles use a sticky right-side “On this page” rail for section and subsection links on wide Mac windows, with an expandable menu on smaller screens.

### Manual MacBook tour and clearer help — October 6, 2026
The hero now starts with Sources, the photo grid, and Inspector visible. Three manual tabs show the same wedding photo in the whole workflow, Focus Mode, and face inspection with focus peaking. No automatic rotation; tabs support arrow keys and mobile horizontal swipes, with all stills readable without JavaScript. The headline and download action stay stationary. The third still uses native Browse inspection tools, not the inconclusive Focused Review comparison panel.

All three new native captures use 0.9.8 (48), matching the newest local Debug build and published release checked this session. Genuine captures retain Retina pixels; derived laptop artwork is recorded separately in hero-tour.json and generated with build_ingest_hero_tour.py. The selected photo embeds Artist Christian Meza and Copyright ChristianMezaMedia. Signature Edits source/license and recorded contributor names/handles are exposed in Support credits, and embedded/filename evidence is added to raw-samples.json. No author is invented for uncredited files.

Long guide passages now have concise task headings linked from the sticky On this page rail. Apple Photos is shortened; the guide landing page and navigation highlight Start here, linking to the existing five-step walkthrough. Existing routes and anchor compatibility are retained.
