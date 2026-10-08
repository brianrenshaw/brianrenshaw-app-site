# Decks refresh — October 6, 2026

## Messaging and design

The photographer knows the presentation they want. The obstacle is limited tools or painstakingly rebuilding the same design. Decks supplies creative control, saved designs, and a repeatable workflow.

The approved headline is “Give your photos the presentation they deserve.” The primary action remains “Try Decks on TestFlight”; the secondary action goes to finished examples. The homepage follows desired result → recognizable frustration → examples → build/save/reuse → specific workflows → developer introduction and beta action. Competitor positioning stays internal.

Use light paper, charcoal system type, generous spacing, complete compositions, and genuine native screenshots. No autoplay, motion, invented app interfaces, external UI framework, or JavaScript dependency. Reuse the site's header/footer/document primitives. Native `details`/`summary` elements reveal additional features. Preserve prior routes, fragment IDs, and historical asset URLs.

## Content boundaries

- Destination examples are exported files for later posting, uploading, or editing. Aura is a prepared composition uploaded through Aura. YouTube is a photograph placed in a video edit.
- Fujifilm reads available MakerNotes from supported original JPEGs. Names of recipes come from the photographer. The cards present settings, rather than applying an image effect.
- “Snippets” means saved caption presets. Sync promises cover projects/templates and their referenced media, not all local presets, recipes, gear, or preferences.
- The Shortcuts section illustrates a still-photo workflow with Brian's original photo, the current native setup screen, and an actual template render. It does **not** pretend these are screenshots of selection or execution inside Apple Photos.
- The video image is a frame extracted from an actual Decks MP4 export. Its source clip is a slow zoom made from Brian's coastline photograph; the caption says so.
- Privacy copy describes implementation: optional integrated Photos access, local working copies, private CloudKit storage, handoffs, and configurable export metadata. GPS/contact metadata is excluded by default, not unconditionally stripped.

## Availability

Apple's App Store Connect API was checked October 6: iOS build 113 and macOS build 112 were `VALID` and `IN_BETA_TESTING`, with the public external TestFlight group enabled at https://testflight.apple.com/join/SAMjeMy5. Minimums are iOS/iPadOS 18 and macOS 15 on Apple silicon. Recheck before any later publication.

## Artwork and reproduction

See `site/decks/assets/SOURCES.md` and `oct06-assets.json`. All `oct06-` artwork is lossless at its original dimensions, with full-size links. The manifest includes input and output SHA-256 values. For landscape XCTest captures, retain the original EXIF orientation; display dimensions are recorded separately from stored pixel dimensions.

`scripts/render_decks_refresh.swift` runs against the native `IngestSocialKit` package. It imports Brian's tutorial photographs, writes isolated projects and native render output, checks the same saved template on three different sources, and imports an original Fujifilm JPEG with MakerNotes. It optionally exports `source-clip.mp4` through `SocialVideoExporter`. `scripts/build_decks_social.py` builds the 1200 × 630 social card from these real compositions.

Capture work used isolated Decks probe stores and an Ingest library rooted at `/tmp/decks-site-ingest-library`. Source photographs were copied into the demo library. Personal project libraries were not edited.

## Verification

- Native renderer completed; the saved Everyday Frame template reproduced the same style on Coffee, Burger, and Example29.
- Camera details came from the native EXIF importer. The Fuji example is original `DSCF0205.JPG`: Classic Negative, dynamic range 100, highlights -1, shadows -1, color 0. It was paired with the actual native field-selection sheet.
- Current iPhone camera/layout/text capture test passed. Current iPad Layout Builder test passed, including rotation and keeping the selected page/shape. Demo Photos contained Brian's photographs for the final capture.
- Current Shortcuts setup/share-file test passed. The broader native shortcut acceptance test initially failed its obsolete 256-pixel assertion because `photoWidth` now takes precedence over the legacy `width` field. In a separate scratch checkout, setting the fixture’s `photoWidth` to 256 made the complete native service acceptance test pass: single and batch inputs, Apply Template output, ordered files, mixed photo/video handling, save-only isolation, retry, promotion, and callback receipts. Production app source was unchanged. Result: `/tmp/decks-site-shortcut-calibrated2.xcresult`. A complete Apple Photos → Shortcuts → Photos UI run, including permissions and batch completion, remains a manual release check; it is not claimed as a passed UI end-to-end test here.
- A separate older home-capture test failed because it still looks for “Home” rather than the current “Layout Builder” tab. Its output was not used.
- Ingest 0.9.7 prepared a six-photo handoff. The local package was opened explicitly in the isolated Decks Mac build, the New/Existing Project chooser was captured, and Add Photos created six correctly ordered pages. Recipient sharing and iCloud delivery were not part of this local check.
- Every original homepage/support/privacy fragment ID is retained. Native/export WebP RGBA pixels match the source files; screenshot orientation is retained separately.
- `python3 scripts/check_site.py`, `python3 scripts/build_decks_site.py`, and `python3 scripts/build_portfolio_site.py` pass. Builds check dedicated-domain links/metadata and legacy redirects/assets.
- `21st review site/decks/index.html site/decks/assets/site.css` reported no HTML findings and only three informational notes for approved color values. The 21st catalog search returned HTTP 401; no catalog component was imported.

## Browser review and remaining release check

Safari responsive mode reviewed the current page at 375, 834, and 1440 CSS pixels. The hero reflows, exported compositions remain complete, navigation stays within the viewport, and the large iPad Layout Builder screenshot remains readable at tablet width. Desktop Shortcuts examples were checked side by side. Native feature disclosures were opened with Space and reached in sequence with Tab, with visible focus. The homepage and support page were reviewed at an explicitly selected 200% page zoom, then restored to 100%. No horizontal overflow was observed in those views.

Chrome at 375 pixels was also reviewed earlier. After the computer interruption, its control connection failed (`codex app-server` missing) and native keyboard targeting was unreliable, so final review continued in Safari. No browser security setting was changed.

Before publication, complete the single-photo and batch Apple Photos share-sheet workflow on a physical device, including first-run permissions and confirming finished images in Photos. The website uses genuine setup UI and rendered results rather than depicting an unverified Photos execution screen. This refresh is prepared locally; it has not been published.

## October 6 next pass — implemented locally

Homepage copy now uses the approved platform eyebrow, “Built by a photographer. Made for your photos.” byline, destination heading, and “Decks · Frames for your photos.” page/social title. The Aura example is a real paired autumn export; Threads uses a separate 4:5 espresso photo. Carousel wording explains Snippets and copied-caption tracking; YouTube emphasizes consistent templates for photographs used in an edit. Shortcuts, Fujifilm, devices, and the photographer frustration copy remain intact. Destination examples stack at phone widths so the longer Aura explanation and complete images remain readable.

The dedicated Aura source page is `site/decks/aura/index.html`. It follows the supplied eight sections and six native FAQ disclosures, with four native exports, a semantic frame table, TestFlight explanation, and the softer cropping answer. Mobile heroes show finished work immediately after the headline. Brian confirmed his knowledge of Aura display behavior; no new physical-frame test was performed or claimed.

### Shipping dependencies and preview

A fresh App Store Connect read confirmed iOS 113 and Mac 112 as the latest valid builds, both `IN_BETA_TESTING` and attached to the enabled public group. Named frame sizes, destination-aware export setup, destination onboarding, and shape-aware previews are newer local app changes; none is advertised as shipped on the production homepage. Instagram remains the existing 4:5 example. The 4K wording and new menu/preview captures are deferred.

`site/decks/aura/.unreleased` gates the Aura page out of default Decks and portfolio output. The default homepage has no link to the unavailable route. `python3 scripts/build_decks_site.py --preview-unreleased` creates a separate `dist/decks-preview`, adds the homepage link, and marks all preview HTML `noindex, nofollow` with disallow-all robots.txt. Production output directories and Cloudflare deployment configuration are unchanged. When named sizes ship publicly, capture the shipped menu, verify its model/orientation choices, record the new build evidence, and remove the marker. The normal Decks build will include the route, link, and sitemap entry; the portfolio build automatically adds its legacy redirect.

The iPad orientation fix is immediate: a new lossless derivative stores the actual upright pixels and removes EXIF orientation. Original captures and historical URLs are retained. This supersedes the earlier instruction to rely on EXIF rotation in website screenshot assets. See SOURCES.md and the manifest for the exact transform and pixel checks.

### External facts checked

- [Aura’s frame comparison guide](https://help.auraframes.com/hc/en-us/articles/360049410694-Aura-Frame-Comparison-Guide-Which-Aura-Frame-Should-I-Choose): screen sizes and orientations; the guide also lists Parker, so the page says “Aura choices in Decks” rather than claiming an exhaustive lineup.
- [Aura Photo Match](https://help.auraframes.com/hc/en-us/articles/360051589374-Showing-two-portrait-photos-next-to-each-other-Carver-Frames): automatic portrait pairing and side bars on Carver. The pairing cannot be manually curated in Aura.
- [Aura gift preparation](https://help.auraframes.com/hc/en-gb/articles/27487175372055-Gifting-a-Frame-Overview-Preparation): preloading is supported with gift setup; the page links to the current instructions and does not instruct owners to connect a gift frame to their own Wi-Fi.

### Next-pass verification

Native renderer output: paired/soft 1280 × 800, full/thin 1600 × 1200, Threads 1080 × 1350. All new lossless WebPs match source pixels, with orientation normalized for the iPad derivative. The source manifest includes original and derived dimensions and SHA-256 hashes.

Site checker, production Decks build, unreleased preview build, portfolio build, and `git diff --check` pass. 21st review reports no HTML findings; the three informational color notes are the existing approved palette. Catalog search returned HTTP 401; no dependency or generated interface was imported.

Safari review covered both pages at 375, 834, and 1440 CSS pixels. The corrected Layout Builder is upright and readable at tablet width; the Aura table fits at phone width. Native FAQ controls respond to Tab and Space with a visible focus outline. Both pages were reviewed at 200% zoom, confirmed through Safari’s Page Menu, and zoom was restored afterward. No horizontal overflow was observed in these views. Nothing has been deployed.

Final release-gate checks also passed in an isolated source copy: removing only the draft marker enables the production Aura page, homepage link, sitemap entry, and legacy redirect with query/hash preservation. The real marker remains in place. A final portfolio check was run to `/tmp/decks-next-portfolio-verification` after concurrent Ingest asset creation interrupted the shared-output checks; all portfolio assertions passed there.

### Apple Frames screenshot pass

Added explicit device framing to the genuine iPhone, iPad, Mac, and upright Layout Builder captures using viticci/frames-cli v1.5.0. The platform section now explains what visitors are seeing and links each original capture; “Inside the app” in navigation makes the section directly discoverable without changing page order. The Mac is an unscaled app-window presentation on a neutral screen canvas. No new app availability claims or release-gate changes. See `assets/SOURCES.md` and the manifest for reproducible framing and provenance.

Validation for the framing pass: site checker passed (46 pages, 1,163 local references); production and unreleased-preview Decks builds passed; portfolio build passed in an isolated output directory; all four derivative/source hashes and dimensions matched the manifest, and lossless output pixels matched the CLI PNGs. Direct visual inspection covered the framed phone, tablet, and Mac assets. `21st review` reported only the three existing palette notices. A fresh browser viewport review was not completed: Safari was actively in use and the isolated in-app browser was unavailable. The earlier responsive review predates these framing changes.

Phone-first revision: the platform showcase now leads with two framed iPhone captures (Layout and Camera Details), then Mac, then the genuine landscape iPad Layout Builder. The phone pair stays side by side, with original screenshots linked. No portrait capture is rotated to imitate landscape.

### Aura navigation and support alignment

Added Aura Frames to the top navigation. The public build links to support’s new `#aura` walkthrough; the unreleased preview links to `/aura/`. The existing release gate remains intact. Rechecked External Testers through App Store Connect on October 6: newest group builds remain 113 and 112. Support keeps manual frame-ratio instructions usable in those builds rather than promising unreleased named destinations. Added support-topic links, Aura arrangement/upload/template steps, photo export sizes, metadata toggles, and archive-after-export troubleshooting. Export labels and behavior checked against the release-matching 9546540 source. Existing linked anchors retained. Site checker and both Decks builds passed.

Layered hero: genuine Mac pair, landscape iPad restaurant layout, and foreground iPhone bridge/camera-controls captures. Static CSS overlap, responsive phone-first arrangement, original full-size links, and visible keyboard focus. Existing three finished exports now sit immediately below the hero. No screenshot pixels modified.

Hero validation: site checker (46 pages, 1,184 local references), production/preview Decks builds, isolated portfolio build, and diff whitespace checks passed. Desktop hero visually inspected in Safari: all three compositions visible with full device outlines inside the page. Narrow-viewport visual review remains pending because Safari responsive controls were disabled in this session.

### Production publication — October 6, 2026

Published the validated `dist/decks` artifact directly to Cloudflare Pages project `decks-photo-app`, production branch `main`, using Wrangler. Deployment: `https://2a2b4819.decks-photo-app.pages.dev`. This publishes the Decks site only; it does not commit or push the shared workspace or publish unrelated portfolio/Ingest changes. The Aura landing-page release gate remains enabled, so public Aura navigation opens the supported setup walkthrough. Local source changes remain uncommitted.

### Grounded device trio correction

Researched and visually inspected the Things multi-device photograph (https://www.aeq-web.com/things3-app-testbericht/) and Yellow Images front-facing trio (https://yellowimages.com/stock/apple-macbook-with-iphone-and-ipad-mockup-147200). Applied their shared-baseline/controlled-overlap principle using only existing Decks assets: phone foreground-left, Mac rear-center, landscape iPad foreground-right. Removed the separate mobile phone-above-pair arrangement. One proportional stage now scales across breakpoints. Reference artwork was not copied into the site. 21st catalog search returned HTTP 401; existing static primitives retained.

The camera/text disclosure now uses matching Apple Frames derivatives with intact source links, accurate Text-tool caption, and single-column phone-width layout. Hero inspected in Safari at 375 and 834 pixels: all devices remain on one baseline with no floating phone. Site checker and production/preview builds passed.

Published the trio/control-frame correction to production: https://faac011a.decks-photo-app.pages.dev. Verified live homepage revision plus exact CSS and new phone asset hashes.

### StoryBrand clarity pass
Implemented concrete hero promise, ordered three-step plan, early founder empathy, template reuse before destinations, shorter destination descriptions with native disclosures, and TestFlight explanation plus support/#install. Preserved all existing anchors including reuse-heading. No approved customer testimonial found; requested exact quote, attribution, example and publication permission. Genuine native exports remain the proof in the meantime. TestFlight installation checked against Apple’s public invitation/help.

StoryBrand pass published: https://57645fea.decks-photo-app.pages.dev. Live homepage and support installation anchors verified. Site checker, Decks production/preview and isolated portfolio builds passed; template proof reviewed at 375 and 834 pixels in Safari. Testimonial remains pending user-supplied approved material.

### Decks wiki-style help center

Added 21 task guides at `/guide/`, a support directory and full-text topic filter, desktop sidebar, compact mobile disclosures, explicit platform anchors, related guides, and original-linked native screenshots. Existing support anchors and their quick-reference content retained. Homepage workflow links now open focused guides. Reuses the Ingest help layout with Decks styling; no cross-product JavaScript dependency. Editorial source and review limits are in `docs/decks/VALIDATION.md`; content and static HTML regenerate with `scripts/build_decks_docs.py`.

Published help center to production deployment https://f07eda96.decks-photo-app.pages.dev. Verified all 25 live Decks pages, canonical URLs, platform anchors, and exact help CSS/JS hashes.

### Deployment regression repair

A Git-connected deployment from main at 944f493 replaced the direct upload with pre-refresh Decks source. Restored all refreshed source and documentation in an isolated checkout based on current origin/main, removed the unwanted hero byline, and committed the Decks changes so subsequent automatic deployments retain them. No unrelated local Ingest edits included.

## Photo-first headline, visible video support

Lead with photos in the headline and hero introduction. Keep video in search metadata, link to the video section from the examples overview, and label the existing genuine export still “Frames and layouts for video, too.” Link the section to the video guide; retain video export instructions and MP4 support. The device trio is unchanged.

## Aura landing page publication

The Aura navigation now opens /aura/. Publish the existing landing page with page-shape instructions (16:10, 4:3, and 3:4), without claiming the named preset menu has shipped. The prior whole-page release gate is removed; named-menu claims and capture remain deferred. Existing build logic includes the sitemap entry and portfolio legacy redirect. Aura gift preparation instructions were rechecked October 6, 2026; the existing official link remains. This is not a new hardware test.

## Build 132 / Mac workflow refresh — October 7, 2026

The user’s “Build 32” request was resolved to current iOS build 132 (source 95a303f and installed Mac build 132), whose Smart Layout features match the request. Read-only App Store Connect verification confirmed iOS 132 and Mac 125 VALID and IN_BETA_TESTING externally; named destinations and Smart Layout shipped on both. The native Mac app was inspected through CUA. Captures show its built-in sample layouts and frame menu, not private library photographs. Original PNGs and lossless WebP derivatives retain all pixels; hashes, dimensions, build and provenance are in oct06-assets.json. Historical assets remain.

Homepage and Aura messaging explain mixed-batch grouping, choosing pairs, odd-photo soft backgrounds, upright frames, and uploading finished files through Aura. New Smart Layout and Mac automation guides join 21 existing guides. Existing task guides now use separate current iPhone/iPad and Mac help sections from source; named destinations, guided Mac Layout Builder, page sequence templates, shortcuts, and expanded settings sync replace stale instructions. Privacy text now reflects default-on optional sync and supported settings, retaining GPS/contact exclusion by default.

No new hardware Aura test or cross-device acceptance is claimed. An isolated Debug capture attempt could not open its test storage; it was closed without importing media. The two new native screenshots use built-in previews/settings only. Seven existing SocialSmartLayoutTests passed against current source, including pairing, squares, odd photos, orientation, swaps and page styles. 21st catalog search returned HTTP 401; existing static sections and disclosures were reused, and review reported zero findings.

## October 8: direct copy and YouTube photo

Replaced the YouTube example with the supplied 09141.jpg, rendered by current IngestSocialKit in an isolated store. The complete photograph fits within a 1920×1080 page with a soft photo background with a thin white frame and no added slogan. Native PNG and lossless WebP have versioned URLs; historical assets remain. The renderer recipe is scripts/render_decks_youtube.swift and asset hashes/provenance are in oct06-assets.json.

Removed the hero “See what you can make” action; Examples navigation and anchors remain. Replaced slogan fragments with feature descriptions throughout the homepage and clarified Smart Layout orientation as vertical/horizontal on both homepage and Aura page. Shared editorial direction is now recorded in MESSAGING.md for every site.
