# App messaging

Approved with Brian on September 9, 2026. Use these promises for homepage cards, app landing pages, search/social descriptions, and future app copy. The customer’s goal comes first; features support that goal.

## Homepage order

Grouped by platform since September 17, 2026, at Brian’s request: the iOS apps first, then the Mac app, then the blogs, then the utility.

1. Folio (iOS app)
2. Who’s First? (iOS app)
3. Reading Habit (iOS app)
4. Where Do We Eat (iOS app)
5. Canceled (iOS app)
6. Walkthrough (Mac app)
7. Lankford Legends (Blog)
8. What Did They Read? (Blog)
9. Spreadsheet Tools (Utility)

Keep the visible numbers in that order. Within the iOS apps, released apps come before the app in TestFlight, and the app still in development comes last; that is why Canceled is the fifth card. Walkthrough sits directly after the iOS apps because it is the only Mac app. Reading Habit moved ahead of Where Do We Eat on September 16, 2026, when it reached the App Store.

With nine cards the tenth grid slot is a dashed placeholder labeled “10 / Not yet” with the line “Reserved for the next thing I want to exist.” and a mailto link. It keeps the two-column grid even. Replace it when the next project ships.

## Approved messages

### Reading Habit

**Headline:** Make reading a daily habit.

**Supporting copy:** Mark the days you read without counting pages, chapters, or minutes. See your consistency grow and work toward your own monthly book goal.

**Priority:** Daily reading consistency. A little reading counts, regardless of how much. Monthly book goals chosen by the reader. Five books is a starting point, not a requirement.

**Availability:** Free on the App Store since September 16, 2026 (`id6809740339`). For iPhone, iPad, and Mac with Apple silicon, requiring iOS 27, iPadOS 27, or macOS 27. The store listing is named “Reading Habit - Book Tracker”; website copy stays “Reading Habit.” There is no subscription or in-app purchase.

**Local app handoff:** `book-tracker/MESSAGING.md` in the sibling app repository.

### Where Do We Eat

**Headline:** Make deciding where to eat easier.

**Supporting copy:** Get suggestions from your favorites and places you’ve been meaning to try, based on what sounds good and who’s coming. Leave out the places they don’t like.

**Priority:** Make the restaurant decision easier. Use favorites, saved recommendations, the occasion, and companions to shape that decision. These are central, not unrelated extras.

**Local app handoff:** `where-do-we-eat/MESSAGING.md` in the sibling app repository.

### Who’s First?

**Headline:** Choose who goes first. Get on with the game.

**Supporting copy:** Quickly and fairly pick your first player. Use fingers on the screen for up to five people, or choose a mode with room for a larger group.

**Priority:** Choose the first player quickly and fairly. Include the whole group: Chooser for two to five fingers, Tap In for up to 50 people, Pinball for two to twelve seats.

**Local app handoff:** `chooser-web-app/MESSAGING.md` in the sibling app repository.

### Folio

**Headline:** Your HTML reports and dashboards, available offline.

**Supporting copy:** Save HTML reports and dashboards from work or AI chats. Open and use them offline on your iPhone or iPad.

**Priority:** Open and use saved HTML files offline on iPhone and iPad. Keep useful work dashboards and AI-generated reports outside the original chat.

**Local app handoff:** `HTML Viewer iOS Ass/MESSAGING.md` in the sibling app repository.

### Lankford Legends

**Audience:** Cardinals fans who also want to follow the rest of MLB.

**Problem:** Game coverage is scattered across scores, blogs, and podcasts, often surrounded by ads or more detail than the reader needs.

**Primary promise:** A concise daily catch-up on the Cardinals, with the rest of MLB alongside it.

**Headline:** Catch up on the Cardinals, every day.

**Supporting copy:** Cardinals highlights, one-paragraph recaps from around MLB, and occasional analysis. Together in one clean, ad-free place.

**Card label:** Cardinals & MLB updates

**Priorities:** Cardinals highlights first, brief league-wide game recaps second, and occasional analysis informed by blogs and podcasts third. Emphasize staying informed in one clean, ad-free place. AI is a production method, not the headline benefit.

**Visual direction:** Keep the existing project card structure. Use a neutral paper background with Cardinals navy (#0C2340) text and Cardinals red (#C41E3A) accents. Keep standard system headline typography at the shared 500 weight and smaller, thinner white LL letters on a Cardinals red baseball diamond. The owner rejected dusty rose: do not mute or reinterpret the team colors. No heavy serif headline or dark navy card in light mode.

**Scope:** This copy describes the linked blog at https://lankfordlegends.co/. Updating this portfolio card does not change the blog’s publishing system or content.

### What Did They Read?

Approved with Brian on September 11, 2026.

**Audience:** Podcast listeners who hear a book mentioned on a leadership or business show and want to find it again, with the original conversation attached.

**Primary promise:** Find the books people talk about on podcasts.

**Headline:** Find the books mentioned on podcasts.

**Supporting copy:** Books from leadership and business podcasts, each linked to the conversation that mentioned it. Plus a searchable archive of what Cal Newport has been reading.

**Card label:** Books from podcasts

**Links:** “Browse books” goes to https://www.whatdidtheyread.com/books. “Visit the site →” goes to https://www.whatdidtheyread.com/.

**Priorities:** The podcast book collection first, always with the episode link. What Is Cal Reading? is a second feature, named in one clause. Do not name the individual shows on the card; the site lists them under Shows and the list may grow. AI is a production method, not a benefit to advertise.

**Visual direction:** Keep the shared card structure. Use the site’s own palette: paper #f2efe8, ink #1a1715, oxblood #8c2b18 accents, and a Georgia serif headline at weight 400 to echo the site’s Newsreader. Dark mode uses a warm dark brown with paper text and a lighter oxblood. The icon is four ruled lines beside an oxblood question mark.

**Scope:** This copy describes the linked site at https://www.whatdidtheyread.com/. Its templates, copy, and publishing live in the sibling `blog-explorer` repository under `blogs/whatdidtheyread/`.

## Editorial rules

- No em dashes. Use short sentences and plain language.
- Explain the app’s main purpose before its supporting features.
- Preserve each app’s visual identity and accurate availability.
- Who’s First? is free with no subscription, a firm commitment. Do not extend that commitment to other apps.
- Folio’s offline promise covers saved content and bundled resources; live online services still require internet access.
- Reading Habit’s detailed progress is optional. Daily consistency comes before recommendations.
- Where Do We Eat suggests saved places. Recommendations and companions’ preferences support deciding; meal memories are secondary.
- App Store descriptions target 80 to 120 words, never exceed 150, and use at most four short benefit bullets. Avoid implementation details and minor feature inventories.

## Keeping surfaces aligned

Each app repository has a self-contained `MESSAGING.md`, linked from its `AGENTS.md`. That file includes approved copy, prepared en-US store fields, factual boundaries, and exact native-copy locations. Future app LLMs should start there. Update both references when the owner changes an app’s purpose.

The website copy is maintained here. App-folder references and App Store copy are prepared locally for future work; they do not claim that native apps or App Store listings have been updated. Historical release records remain historical. Native source edits and release submissions require their own task.

## Validation and publication

Run `python3 scripts/check_site.py`, then review the homepage and all four app landing pages at phone, tablet, and desktop widths. Check claims, headline readability, CTA links, social metadata, and punctuation. Publish only website-repository changes, confirm the deployment succeeds, and run `python3 scripts/check_live.py`.

## September 9 implementation record

- Updated homepage cards, four app landing pages, search/social metadata, two guide introductions, and Folio support introduction.
- Preserved existing styling, assets, routes, and availability. Reordered Reading Habit’s content and changed the dining steps to focus on making a decision.
- Added app-local messaging documents and AGENTS links without changing native source or historical submission records. Store descriptions are 92 words (Reading Habit), 91 (Where Do We Eat), 89 (Who’s First?), and 95 (Folio).
- Static checks passed: 21 HTML pages and 288 local links/assets. Responsive checks covered five pages at 375, 834, and 1440 pixels, plus dark/reduced-motion phone checks and dining gallery click/keyboard interaction. Full-page screenshots were reviewed in an isolated Chromium browser after the connected preview timed out.
- App-folder documentation remains local. No App Store Connect writes, native builds, or release submissions were performed.

## September 16 release update

Reading Habit 1.0 reached the App Store on September 16, 2026. Website availability copy changed accordingly:

- Homepage card: “In development” became “Available on the App Store,” matching Folio and Who’s First?
- Landing page: the hero action is now the App Store download with the guide as the secondary link, the status line reads “Free on the App Store · iPhone, iPad, and Mac,” the closing callout leads with the download, and the Availability section describes version 1.0 and the Apple silicon requirement for Mac.
- Guide: the pending-release note became a release note with a download link, the version line reads “Version 1.0 · Updated September 16, 2026,” and the sync paragraph no longer defers verification to a future public release.
- Privacy policy: the version descriptor is “Version 1.0.” The effective date and policy text are unchanged because data practices did not change.
- Homepage order: Reading Habit is now card 03 and Where Do We Eat card 04. The share image `assets/social-projects-v4.png` was rebuilt in the new order and replaces v3.
- Availability was verified against Apple’s public lookup and the store listing before publishing: version 1.0, free, no in-app purchases, iOS/iPadOS 27 and macOS 27 minimums.
- Card accent: Reading Habit’s eyebrow and footer links use its own `#7d5411` gold (`#e2b15f` in dark mode), so the released card reads as actively as Folio, Where Do We Eat and the two blogs. Who’s First? and Spreadsheet Tools keep inherited ink because their card colors already read as accents.
- Screenshots: the landing page and guide use real 1.0 captures from the store-library fixture. The first capture showed duplicate books and doubled goals; that was a fixture seeding bug, fixed in `book-tracker`, and the published images are recaptured from a clean library. They now show three books under way and 2 of 4 books this month, which matches “a little reading counts” better than the doubled figures did.
- Card type label: Reading Habit stays “iOS app.” The label is a coarse category alongside Blog and Utility, not a platform list; the landing page’s “For iPhone, iPad, and Mac” carries the detail. Decided September 16, 2026; do not reopen without changing the whole taxonomy.

## Lankford Legends blog alignment

Approved with Brian in this blog workspace on September 9, 2026:

- Use the Lankford Legends headline and supporting copy above on the blog homepage. Link visibly to “How this site is made.”
- Describe the reading experience as a quick catch-up with room to go deeper. Do not imply every article is brief.
- Keep the latest three analysis titles and their existing summaries discoverable under “Beyond the box score,” below the daily features.
- About starts with the reader's purpose, then explains the three series and separates source data, calculated statistics, attributed commentary, and AI-written prose with automated numerical checks.
- Footer links: About, Sources and AI, Follow via RSS. Sources and AI links to `/about#how-this-site-is-made`.
- Preserve the blog's existing typography, colors, spacing, and publishing workflow. The visual instructions for the portfolio card above do not replace the blog's design.

Blog copy locations: `template/entries.html` (homepage), `template/package.json` (site descriptions), `template/footer.html` (footer), and `pages/about.md` (About). Blog validation and publication use this repository's `npm test`, `npm run preview:build`, and scripts documented in `README.md`; the portfolio validation commands above apply to the separate portfolio repository.

Homepage hierarchy refinement: daily reports use separate bordered sections with Cardinals red and navy accents. Analysis uses a neutral paper panel. Recent posts use a stronger section divider and smaller navy headlines. These changes distinguish the homepage sections while preserving article typography and spacing.

Priority clarification: the latest Cardinals Daily is the primary feature, the latest MLB Roundup is secondary, and infrequent analysis is tertiary. Keep that order and show publication dates on homepage analysis entries. Use the strongest red headline and bordered treatment for Cardinals Daily, a smaller navy headline with a simple divider for MLB Roundup, and a lighter neutral analysis section.

## Listing Namer (September 17, 2026)

Added at Brian's request as the eighth project, replacing the reserved slot. Type: Mac app. Headline: “Give every listing photo its place.” Lead with organizing real estate shoots and consistent delivery filenames while preserving JPG quality. Support keyboard grouping, ordering, presets, and local jobs with practical copy. Availability must say Mac preview until a notarized release is ready. Current requirements: macOS 14+, Apple silicon and Intel. No account is required. Do not describe address search or update checking as offline. The download is Developer ID signed but not yet notarized; disclose that macOS may block it.

### Walkthrough (September 17, 2026, current)

Repositioned with Brian on September 17, 2026 using the StoryBrand frame. This supersedes the earlier preview, tour, and “Rename photos. Set their order.” wording above.

**Audience:** Realtors and listing assistants. Name both; the assistant is often the person doing the uploading.

**Problem:** A camera names files in the order it shot them, not the order a buyer should walk the house, so photos sorted by filename land on the MLS scrambled. The fallback is dragging them into place one at a time in a browser, and not knowing it is right until the listing is live.

**Primary promise:** Photos upload to the MLS in the order you chose, on the first upload.

**Headline:** Upload listing photos in the right order.

**Supporting copy:** Sort a whole shoot visually, group photos by room, and export numbered filenames. Your photos land on the MLS in the order you chose.

**Card label:** Listing photos in order

**Priorities, in order:** Visual sorting of a whole shoot first. Renaming is the mechanism that carries the order, not the headline benefit. Then repeatability: templates with rooms already ordered, or your own group names for a house that does not fit the pattern. Then the team: sharing your setup so filenames match. JPG integrity and export review are the trust line in the closing section, not a feature block.

**Landing page sections:** 01 / Sort, 02 / Repeat, 03 / Share. These replaced Organize / Name / Deliver, which described what the app does to files rather than why anyone would want it.

**Do not say “sync.”** There is no sync service. Settings export writes a `.listingnamersettings` file containing tags, presets, and templates, shared manually, with Merge or Replace on import. It carries no photographs and no job history. Say “share your setup.” Never imply a cloud service, shared jobs, or shared photos.

**Availability:** Show only the current version number beside the download, without build, signing, or notarization copy. Release history lives at /listing-namer/release-notes/ and is linked from the website and the app’s Help and Settings. Historical release entries stay as written; do not restate them in current positioning language.

**Visual direction:** Unchanged. Genuine current native screenshots, the house icon with the 01 label, charcoal app pages with amber accents.

## Canceled (September 17, 2026)

Added at Brian's request as the fifth project and the last of the iOS apps, because it is still in development. Native source is in the sibling `canceled-app` project. Website route is `/canceled/`, a landing page only; add privacy and support when the app reaches TestFlight.

**Audience:** Two friends who both quietly want out of the same plan.

**Problem:** You want to cancel and you have no idea whether your friend does too. Sending the text makes you the flake; saying nothing means going out drained. Canceling shouldn't cost you the friendship, and honesty shouldn't require someone to go first.

**Primary promise:** The plan comes off without either person having to be the one who asked.

**Headline:** Nobody has to be the one who cancels.

**Supporting copy:** You and a friend each privately say whether you want out. If you both do, the plan is off. If not, nothing is revealed.

**Card label:** The quiet way out

**Landing page sections:** 01 / Private, 02 / Mutual, 03 / One app.

**Priorities, in order:** Privacy of the individual choice first. The mutual reveal second. Third, that only the plan's creator needs the app, because the friend can accept and cancel in a browser. Calendar import is a supporting detail, always described as opt-in.

**Voice:** The app has its own dry voice and the website borrows it rather than inventing one. Canonical lines: "The plan is still on unless you both cancel." (the load-bearing rule, used verbatim in the cream slip), "Two friends. One mutual understanding.", "Your evening has been returned to you.", and the masthead line "The quiet way out". Keep the plain StoryBrand framing for the headline and the app's wit in the section copy.

**Factual boundaries:**

- In development. TestFlight distribution is unverified, so there is no download, beta link, or call to action. The page states status and stops.
- Notifications are off in the beta service. Do not promise reminders or push.
- `canceledapp.com` is not yet the application. Do not link to it.
- Calendar discovery is local and opt-in, starting with no calendars selected.
- Spelling is Canceled, one L. The wordmark carries a trailing period with the full stop in Sunshine yellow.
- Screenshots come from the app's Demo mode. Always caption them as example data. The reveal capture is cropped below the "DEMO / MUTUAL CANCELLATION" line, because that is a mode indicator rather than product interface; the caption carries the disclosure instead. Recapture with `--demo --invite-preview --invite-flow-test` for the invite screen and `--demo --demo-reveal` for the reveal, on an iPhone 17 Pro simulator with the status bar overridden to 9:41.

**Visual direction:** The app's own palette, not the portfolio's warm paper. Navy ground `#142d4e` in light mode and `#151d2c` in dark, cream surface `#fffdf6`, Sunshine `#f7dc12` for eyebrows and links, cancellation red `#a42620`, muted `#c5d0df`, rules `#4a5c74`. Archivo at weight 900 for headings, on a smaller headline scale than the shared one because Archivo sets much heavier. Motifs are the cream slip with its Sunshine tick and the rotated red CANCELED stamp. This is the first homepage card that is dark in light mode; navy is the brand's ground in both appearances, so it is intentional here even though a dark navy card was rejected for Lankford Legends.

## September 17 implementation record

- Repositioned Walkthrough on the homepage card, the landing page, the guide and support introductions, and search/social metadata, using the StoryBrand brief above. Feature blocks became Sort / Repeat / Share.
- Added the `/canceled/` landing page, its `assets/site.css` theme, the `.canceled` portfolio card, and a sitemap entry. The app icon is the 1024 capture from `canceled-app`. Both screenshots are fresh iPhone 17 Pro simulator captures taken for this page, resized to 603px wide; the reveal is cropped below its demo-mode label. They replaced the first pass, which showed a sample dinner at 3:36 AM and a reveal clipped mid-button. The odd time came from the demo fixture offsetting every sample plan by a flat eight hours from launch; `DemoEngine.swift` in `canceled-app` now anchors the samples to sensible evening times, which is an uncommitted change in that project for Brian to review. Archivo is the existing `archivo.woff2` already bundled for Where Do We Eat, copied in at 189KB rather than shipping the 658KB variable TTF; the two source files are byte-identical.
- Reordered the homepage to nine platform-grouped cards and renumbered cards 5 through 9. Reinstated the dashed placeholder as slot 10 to keep the two-column grid even. Preserved the `#lankford-legends`, `#what-did-they-read`, and `#utilities` anchors.
- Rebuilt the share image as `social-projects-v8.png`. Nine projects do not fit the old four-column grid inside 1200x630, so `scripts/build_social.py` now lays out a 3x3 grid with a compacted hero. The homepage `og:image` and `twitter:image` point at v8 and the two alt strings were updated to nine projects. `portfolio.css` is now served as `?v=9`.
- Corrected two stale Walkthrough privacy-page facts found while surveying: the policy said "Applies to Walkthrough 1.0" against a shipping 1.2.1, and its `og:image` still referenced a 1.1.0 capture.
- Removed the one em dash on the Walkthrough landing page. Em dashes remain in several older privacy and support pages; a site-wide pass was not in scope.
- Download URLs, DMG filenames, release tags, the appcast, and the historical release notes were left untouched.
- Static checks passed: 27 HTML pages and 457 local links/assets. Pages were reviewed in Chrome at 375, 834, and 1440 pixels in light and dark mode.
