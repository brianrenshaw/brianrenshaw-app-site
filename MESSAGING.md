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
7. Ingest (Mac app)
8. Lankford Legends (Blog)
9. What Did They Read? (Blog)
10. Spreadsheet Tools (Utility)

Keep the visible numbers in that order. Within the iOS apps, released apps come first and the app still in development comes last; that is why Canceled is the fifth card. The Mac apps sit directly after the iOS apps: Walkthrough, then Ingest, which was added on September 18, 2026. Reading Habit moved ahead of Where Do We Eat on September 16, 2026, when it reached the App Store; Where Do We Eat reached the App Store itself on September 17, 2026 and keeps card 04, so all four released iOS apps now sit ahead of Canceled.

With ten cards the eleventh grid slot is a dashed placeholder labeled “11 / Not yet” with the line “Reserved for the next thing I want to exist.” and a mailto link. It keeps the two-column grid even. Replace it when the next project ships.

## Approved messages

### Reading Habit

**Headline:** Make reading a daily habit.

**Supporting copy:** Mark the days you read without counting pages, chapters, or minutes. See your consistency grow and work toward your own monthly book goal.

**Priority:** Daily reading consistency. A little reading counts, regardless of how much. Monthly book goals chosen by the reader. Five books is a starting point, not a requirement.

**Availability:** Free on the App Store since September 16, 2026 (`id6809740339`). For iPhone and iPad, requiring iOS 27 or iPadOS 27. **There is no Mac release.** A Mac App Store search for this developer returns nothing, and Apple’s lookup holds a single iOS record; the `macosx` target in `BookTracker.xcodeproj` builds but has not shipped. The pages say “Mac coming soon” and “in development and not yet available”, and must not claim a Mac download, a macOS minimum version, or an Apple silicon requirement until a Mac release is verified. The store listing is named “Reading Habit - Book Tracker”; website copy stays “Reading Habit.” There is no subscription or in-app purchase.

**Local app handoff:** `book-tracker/MESSAGING.md` in the sibling app repository.

### Where Do We Eat

**Headline:** Make deciding where to eat easier.

**Supporting copy:** Get suggestions from your favorites and places you’ve been meaning to try, based on what sounds good and who’s coming. Leave out the places they don’t like.

**Priority:** Make the restaurant decision easier. Use favorites, saved recommendations, the occasion, and companions to shape that decision. These are central, not unrelated extras.

**Availability:** Version 1.0 reached the App Store on September 17, 2026, at `https://apps.apple.com/app/id6808350718`. A free download for iPhone and iPad, requiring iOS or iPadOS 27. The TestFlight beta is over; nothing on the site may call this app a beta, link to `testflight.apple.com`, or hedge that its screens may still change. "No ads or tracking" is supported by the privacy policy, which states the app contains no advertising, analytics, or tracking software.

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

## Ingest (September 18, 2026)

Added as the tenth project, taking the reserved slot. Type: Mac app. The second Mac app, and the second one whose pages
are charcoal with a warm accent, so keep them visually apart: Walkthrough is `#111214` with `#e9b454`, Ingest is
`#0B0B0D` with `#F5A524`.

**Positioning updated September 20, 2026:** Ingest is a modern Mac app for quick photo import, culling, and everyday photo file management. The command bar connects these jobs. The earlier card-emptying pitch is superseded.

**Audience:** Photographers who want to import shoots, select keepers, and manage photo files on their Mac, including people looking for a modern alternative to Photo Mechanic. Current fast RAW previews support Sony ARW and Fujifilm RAF; never imply universal RAW preview support.

**Problem:** Importing a shoot, making selections, and organizing existing photo folders involve many repeated actions. Photographers need those actions easy to find and quick to use.

**Primary promise:** Import, cull, and manage photo files on Mac. Use the command bar to find commands, open folders, and apply presets.

**Headline:** Import. Cull. Manage.

**Supporting copy:** Import a shoot, compare frames, and organize your files. Press ⌘K to find commands, open favorite folders, and apply presets.

**Portfolio headline:** Import, cull, and manage photos.

**Portfolio supporting copy:** Browse photos on a card or in a folder, compare frames, and mark your selections. Use the command bar to import files, rename them, and add metadata.

**Card label:** Photo import and management

**Priorities:** Import, cull, and manage are equally prominent capabilities, not a required sequence. Show the command bar in the hero and explain command search, favorite folders, presets, and workspaces. Make management of existing folders explicit. Use concrete benefits before implementation details; leave embedded-preview mechanics, naming tokens, and shortcut configuration in the documentation. Avoid absolute speed claims.

**Landing page sections:** Hero with command-bar screenshot; “Find and run commands with ⌘K”; import, cull, and manage sections with real screenshots; brief positioning and reassurance; “Download the working beta” closing. Preserve existing section ids even when the headings change.

**Photo Mechanic:** Mention it once in supporting landing-page copy. Approved sentence, updated September 20, 2026: “I built Ingest because I wanted a modern Mac app for the part of the workflow Photo Mechanic has covered for years.” Keep it out of titles, metadata, and headlines. Retain the existing support-page migration reference. Do not claim feature parity or comparative speed, and do not raise Photo Mechanic’s price or its age.

**No automatic culling.** Ingest does not rate or reject photographs on the photographer’s behalf. State this on the landing page in the About bullets and once in the Cull section. Scope the claim to rating and rejecting, never to AI or machine learning generally: the face close-up strip uses Apple’s Vision framework on the Mac, so a broad “no AI” claim would contradict the guide and privacy pages. Acknowledge that AI culling tools exist and work; do not invent frustrations about them or about competing apps. Do not add a standalone page or heading arguing the case.

**Tone:** Explain what the app does and how to use it. Headings name capabilities; captions explain what is shown. Avoid slogans, invented frustrations, strained comparisons, and claims of instant results. Do not replace explanations with generic benefit lines such as “Make room for the photos,” “get moving,” or “keeps your next action close.” Keep explanations concise and useful to photographers, without turning the landing page into implementation documentation.

**Command bar:** Search commands, favorites, presets, and workspaces by name. Do not imply AI, natural-language automation, or a terminal. Marketing calls it the command bar; existing technical references may call it the palette.

**Do not overstate safety.** Write what is verifiable: Card metadata and filenames stay untouched; explicit card deletion is available only after verified copying, as documented on the support page. Do
not extend that into a claim that photographs cannot be lost, and never call the second destination a backup. Same
family rule as the standing ban on calling a settings export "sync".

**Do not overstate verification.** Ingest hashes what it wrote and compares it to the source, and stops when they
differ. Not "guaranteed", not "bit perfect", and it says nothing about corruption that happens later.

**Say the requirements everywhere.** macOS 15 or later, Apple silicon only. An Intel owner downloading a disk image
that will not open is the most expensive support email the page can generate. Sony ARW and Fujifilm RAF preview support is named near the download too; never imply universal raw support.

**Face close-ups need their sentence.** Faces are found on the Mac only in order to zoom in. No names, no identities,
nothing stored, nothing sent. It appears on the guide and on the privacy page.

**Scripts need their sentence.** A shell step runs as you and Ingest does not restrain it. On the automation page and
again on the privacy page.

**Availability:** Show the version beside the download and label the current 0.2.1 release “Working beta.” Use this explanation: “Ingest is a working beta. I use it for my own work and am still developing it for a broader audience.” Avoid vague qualifiers such as “young” or claims that the shape of the app is settled. Release history lives at
/ingest/release-notes/ and is linked from the app's Help menu. Do not restate historical entries in current positioning
language.

**Visual direction:** Real screenshots of the running app, captured against a demonstration card built from Unsplash
photographs, credited in `site/ingest/assets/SOURCES.md`. No client work and no personal photographs, ever. Black pages,
amber accents, the memory card icon.

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

### Walkthrough (September 20, 2026, current)

**Writing philosophy:** Read [Walkthrough’s messaging philosophy](WALKTHROUGH_MESSAGING_PHILOSOPHY.md). Explain capabilities and interactions directly. This replaces the earlier StoryBrand framing, invented frustrations, slogans, and guarantees about MLS upload order.

**Audience:** Realtors and listing assistants organizing JPG/JPEG listing photos on a Mac.

**Purpose:** Group photos by room, arrange rooms and photos, preview filenames, and export numbered files. The command bar finds actions, rooms, presets, templates, and recent jobs.

**Headline:** Sort and name listing photos.

**Supporting copy:** Group photos by room, arrange their order, and export numbered filenames. Use the command bar to assign rooms, apply naming presets, and reopen jobs.

**Portfolio headline:** Organize photos for a property listing.

**Portfolio supporting copy:** Group photos by room, set their order, and export copies with numbered filenames. Save room templates and naming presets for future listings.

**Card label:** Real estate photo organization

**Content priorities:** Explain grouping and ordering first, then command-bar actions, reusable naming presets and room templates, and export review. Describe settings-file sharing and saved local jobs separately. Headings name capabilities; screenshot captions explain what is shown.

**Landing page:** Workspace screenshot; grouping, ordering, and exclusions; command bar; naming presets and room templates; export review; settings sharing and saved jobs; download. Preserve real screenshots, supported formats, system requirements, and exact export behavior.

**Upload order:** Numbered filenames support sorting by name. Tell users to sort exported files by name before selecting them and check final order in the MLS or website after uploading. Do not guarantee that any receiving service preserves order or that the first upload is correct.

**Export:** Rename only changes filenames in their existing folders. Copy keeps the source files. Move relocates files. Copy and Move can use a flat output or numbered room folders. Review filenames, paths, and naming warnings before confirming. JPG bytes are preserved without re-encoding; export does not publish a listing.

**Settings sharing:** Export tags, naming presets, and templates to a settings file that someone else can import with Merge or Replace. Do not call this sync or imply that it shares photos, saved jobs, or a live configuration.

**Saved jobs:** Organization is stored in the local app library. Reopening a job restores room assignments, photo order, and naming choices on that Mac. Do not imply cross-device job history.

**Availability:** Current download: Walkthrough 1.4.1. macOS 14 or later, Apple silicon and Intel, no account required. Do not copy Ingest’s beta status, RAW support, or system requirements. Historical release notes remain historical; preserve the original Listing Namer update feed and redirects.

**Visual direction:** Dark charcoal with the native teal accent, house-and-number icon, bundled Archivo, and genuine native screenshots using demonstration data. Use a wide workspace screenshot and alternating explanatory sections. Keep layout styles scoped to the landing page and document layouts intact.

## Canceled (September 17, 2026)

Added at Brian's request as the fifth project and the last of the iOS apps, because it is still in development. Native source is in the sibling `canceled-app` project. Website route is `/canceled/`, a landing page only; add privacy and support when the app reaches TestFlight.

**Audience:** Two friends who both quietly want out of the same plan.

**Problem:** You want to cancel and you have no idea whether your friend does too. Sending the text makes you the flake; saying nothing means going out drained. Canceling shouldn't cost you the friendship, and honesty shouldn't require someone to go first.

**Primary promise:** The plan comes off without either person having to be the one who asked.

**Headline:** Nobody has to be the one who cancels.

**Supporting copy:** You and a friend each privately say whether you want out. If you both do, the plan is off. If not, nobody finds out you wavered.

**Card label:** The quiet way out

**Landing page sections:** 01 / Private, 02 / Mutual, 03 / One app, then the reveal, then the rotating copy bank.

**Priorities, in order:** Privacy of the individual choice first. The mutual reveal second. Third, that only the plan's creator needs the app, because the friend can accept and cancel in a browser. Calendar import is a supporting detail, always described as opt-in.

**Voice:** Whimsical and deadpan, in the Carrot Weather register, at Brian's direction on September 17, 2026. The app already has this voice and the website borrows it rather than inventing one; quote the app instead of writing new jokes.

Lines used verbatim on the page: "The plan is still on unless you both cancel." (the load-bearing rule, in the cream slip), "Your evening has been returned to you.", "You both wanted out. Excellent communication, technically.", "Canceled. Beautifully.", "they see nothing, and the plan is still, infuriatingly, on.", "Your calendar still thinks you're going. Bold of it.", "No plans. Suspiciously efficient.", "Look at you, honoring a commitment.", "No scores. No judgment. Well, very little.", and the masthead "The quiet way out".

The reveal's audit row is worth naming on the page: RETURNED 1h 30m and EXCUSES USED None.

**The rotating copy bank is a feature, not decoration.** 120 lines in `PrivateCancelCopy.swift`, mirrored in `Web/public/copy.json`, shuffled so a line never repeats back to back. The page says so and quotes six across the themes: furniture lobby, bureaucracy, past self versus present self, and film notes. Refresh the quoted six from the bank rather than writing new ones.

Keep the headline and the factual claims plain. Snark rides in the section copy, never in an availability or privacy statement.

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

## September 18 implementation record

- Where Do We Eat 1.0 reached the App Store on September 17, 2026. Verified against Apple's public lookup before publishing: free, iOS 27 minimum, universal iPhone and iPad, app ID 6808350718.
- Replaced every TestFlight link with `https://apps.apple.com/app/id6808350718`: the homepage card footer, the shared header nav on the landing, guide and privacy pages, and both landing-page calls to action. The homepage card now reads "Available on the App Store" and the landing page "Download on the App Store", matching Folio, Who's First? and Reading Habit.
- The hero availability list dropped "In beta, screens may evolve" for "Free, No ads or tracking". The first is no longer true and the second is a fact the privacy policy already states. Its `.is-note` accent class and rule were removed, because the line is now a plain fact rather than a caveat and should match its two siblings.
- Renamed the header accent class `nav-beta` to `nav-store` in the page-local stylesheet, so no markup is still named for a beta that ended. It is used only by these four pages.
- Guide: the stamp now reads "Updated September 18, 2026 / Matches version 1.0" rather than "Matches beta build 15". The device question asks which devices run the app instead of the beta, and feedback routes to email with an app version rather than through TestFlight.
- The homepage card kept position 04 and its number. All four released iOS apps already sat ahead of Canceled, so no reorder or renumbering was needed, and the share image needed no rebuild because its cards carry no availability.
- `MIGRATION.md` was left alone. Its App Store Connect table is a dated record of the September rollout, not current status, and the repo keeps historical records historical.
- Static checks passed: 32 HTML pages and 468 local links/assets. The App Store URL returns 200.

### Functionality and screenshot audit, same day

Audited the page against the shipping build rather than the source tree: unpacked `Distribution/build/1.0-25/WhereDoWeEat.ipa` from the sibling app project and read its `Info.plist`. It is version 1.0, build 25, minimum iOS 27, iPhone and iPad, and it contains `PlugIns/WhereDoWeEatWidget.appex` and `Metadata.appintents`.

- **Screenshots are current and were not replaced.** All four site captures differ byte for byte from the September 13 App Store set, so they were compared directly. The design is identical: same paper background `(247,245,241)`, same row fill `(232,227,222)`, same typography, same controls, same sparkle glyphs on saved-place rows. The only differences are sample data, dates about four days apart, one restaurant name in the choices screen, and a scroll position on the log screen. The Paper redesign that shipped in builds 16 to 22 is already what the site shows.
- **The Decide widget was missing from the whole site.** It ships in the released build. Added `#widget` to the guide and a landing-page block. Facts taken from `WhereDoWeEatWidget/DecideWidget.swift`: the display name is Decide, it supports `systemSmall` and `systemMedium` only, it is a static configuration that never reads the shared store, and accessory families are deliberately omitted so dining entry points never reach the Lock Screen. Do not describe it as showing suggestions, restaurants, or any saved data.
- **Siri was described only as a privacy toggle, never as a capability.** There are eight App Shortcuts in `WhereDoWeEat/Intents/DiningAppShortcuts.swift`: Decide Where to Eat, Ask What Sounds Good, Pick One, Open Restaurant, Add Restaurant, Log a Meal, Plan a Meal, and Search Dining Memory. Apple requires the app name inside the phrase, so quoted phrases must read "Decide where to eat with Where Do We Eat", not "Decide where to eat".
- **Planning was in the guide and the privacy policy but not the landing page,** even though the log screenshot shows a PLANNED section. Added a Plans block. A plan and a logged visit are separate records; keep that distinction.
- Reused `.steps-section`, `.section-head` and `.steps` for the new landing section, so no CSS was added. The `.steps .number` slot carries the labels Widget, Siri and Plans instead of numbers, because the section is not a sequence and the first section already promises three steps.
- Fixed the support page metadata: `og:title` and `og:description` were both the placeholder "Support", and its `og:image` had no alt text. Folio's support page has the same placeholder pair and Reading Habit's and Who's First?'s support pages have no Open Graph tags at all; neither was touched here.
- Verified accurate and left alone: the guide's control names all match the shipping UI (All saved, Want to try, What sounds good?, Show 3 choices, Browse matches, Pick One for Me, Three More, Log & Get Directions, Directions Only). Sharing, Apple Intelligence, voice entry, and the permission list are already covered correctly in the guide.
- Corrected a now-false rule in the sibling app project's `MESSAGING.md`, which still told editors the website offered a TestFlight beta and said not to describe the app as released. That edit is uncommitted in `where-do-we-eat`, which has a large amount of unrelated pending work.
- Static checks after the additions: 32 HTML pages and 472 local links/assets.

## September 18 audit of the other three apps

Same method as Where Do We Eat: check the shipped build and Apple's public listing, not the source tree or the existing copy.

**Support page metadata, all four apps.** Every support page had `og:title` and `og:description` set to the bare placeholder "Support", and none had `og:image:alt`. All four now carry a real title and a one-line summary of what the page covers. An earlier pass reported Reading Habit's and Who's First?'s pages as having no Open Graph tags at all; that was wrong, a regex that assumed `property` came before `content`. Read the raw markup rather than trusting an extraction.

**Who's First? claimed less than it ships.** The landing page said "For iPhone · iOS 26 or later". The app's own `MESSAGING.md` recorded this as deliberate and said to verify the release before changing public device availability, so that verification was done: live version 1.2 reports `iosUniversal` with 80 iPad devices, its store listing carries six screenshots in iPad 3:4 aspect, and the Xcode project sets `TARGETED_DEVICE_FAMILY = "1,2"`. The line now reads "For iPhone and iPad". Update `chooser-web-app/MESSAGING.md` to match when convenient.

**Folio's Files integration was documented nowhere.** The shipped IPA embeds `FileProviderExt.appex`, `ShareExt.appex` and `WidgetExt.appex`. The File Provider publishes the library as a browsable location in Files and the document picker and is read only by design, because Folio reconciles the library against watched folders and Drive. Added a support-page section. Also corrected the widget paragraph: `WidgetExt` declares `systemSmall`, `systemMedium` and `accessoryCircular`, so there is a Lock Screen placement the page did not mention.

**Folio's landing page named one import route out of four.** It said pages come from Files or another app's share sheet. The build also imports from Google Drive, with `drive.file` scope and OAuth confirmed in the binary, and watches a folder to keep pages current. Both were already documented on the support and privacy pages. The feature block now names all four.

**"No account." became "No account required."** Folio works fully without one, but it offers optional iCloud sync and an optional Google Drive connection, both off by default. The absolute phrasing read as a promise the app does not quite make. This matches how Walkthrough states the same thing.

**Reading Habit needed only a wording fix.** Its guide said the Add Book control is "available in supported system control galleries", which is true but tells a reader nothing. It now names Control Center, the Lock Screen, and the Action button, and states that the control shows nothing from the library. Its landing page omits widgets and Shortcuts, which the guide covers; that is an editorial choice and was left alone.

**Wrongly left in place, corrected September 18:** Reading Habit's claim of iPhone, iPad and Mac. The first pass reasoned that Apple's `supportedDevices` does not enumerate Macs for an iOS app, so the listing could not confirm or deny it, and that a `macosx` target plus Mac notes in the guide made the claim deliberate. That was a rationalisation of an unverified claim. Brian said the honest line was "Mac coming soon", and a Mac App Store search settles it: `entity=macSoftware` returns nothing for this developer while returning other developers' apps for the same query. Availability claims were removed from the landing page, its meta description, the availability paragraph and the guide note, along with the guide's Mac-specific asides about clicking, barcode scanning and the Mac widget gallery. **A platform claim needs a positive check, not the absence of a disproof.** Who's First?'s "Eight visual worlds" is correct: `ChooserColorTheme.swift` defines exactly eight world cases. Every other app page's control names and feature descriptions matched their shipping builds.

## September 18, third pass: the gaps the first two passes missed

Brian asked whether all the real gaps were fixed. They were not. Two were missed for different reasons, and both are worth recording.

**The Reading Habit Mac claim was the miss that mattered.** It was flagged, investigated, and then left in place with a written justification. That justification inverted the burden of proof: it treated "Apple's listing cannot disprove this" as grounds to keep a platform claim. The check that settles it is trivial, `entity=macSoftware` against the search endpoint, which returns nothing for this developer and returns other developers' apps for the same query. **A platform claim needs a positive check, not the absence of a disproof.** Fixed across the landing page eyebrow, status line, meta description and availability paragraph, the guide note, and the guide's Mac asides about clicking, barcode scanning and the Mac widget gallery. The pages now say "Mac coming soon" and "in development and not yet available", which is Brian's wording.

**Landing-page omissions were dismissed as editorial when some were real.** The second pass reasoned that a landing page not listing every capability is a choice rather than a defect. That holds for Reading Habit, whose landing page already covers goals, rest days, rereads, sync and export, and for Who's First?, which has three modes and eight worlds and little else. It did not hold for Folio, whose landing page described three capabilities while the app ships a widget with a Lock Screen placement, per-page Face ID locking, optional iCloud sync, a Files location, PDF export and an iPad workspace, all documented only on the support page. `.features` is a fixed three-column grid, so three more articles fill a second row with no CSS change.

**Also done in this pass:**

- Walkthrough was audited for the first time; earlier passes covered only the iOS apps. Version 1.2.2 build 8 matches the site. The command palette, contact sheet, inspector, keyboard shortcuts, templates, recent jobs and settings export are all documented across the landing, guide, support and release-notes pages. No gaps found.
- `book-tracker/MESSAGING.md` still described the app as in development with no public download, and listed Mac. Corrected and committed there as a single file; that repo was clean.
- `chooser-web-app/MESSAGING.md` was corrected to record the verified iPad support. It is an untracked file in a repo with other pending work, so the edit is on disk and uncommitted rather than added to git.
- Folio's own `MESSAGING.md` was checked and needed nothing.

## Folio verified against the exact live build

The earlier Folio audit used `build/export/HTMLViewer.ipa`, which is 1.1 build 11 from August 25, while the App Store serves 1.1.2. Brian asked for the live build. No rebuild was needed: the project's source is already at `MARKETING_VERSION = 1.1.2` and `CURRENT_PROJECT_VERSION = 18`, and commit `92cae0a` is "Release 1.1.2 (18)", so every claim was re-checked with `git show` and `git grep` pinned to that commit.

All seven published claims hold at `92cae0a`:

| Claim | Evidence at the shipped commit |
| --- | --- |
| Widget in small, medium and circular Lock Screen sizes, per page | `WidgetExt/FolioWidget.swift`: `supportedFamilies([.systemSmall, .systemMedium, .accessoryCircular])` with `AppIntentConfiguration` |
| Touch and hold for favorite and recent pages | `QuickActions.swift`, `UIApplicationShortcutItem` |
| Face ID **or the device passcode** | `PrivacyLock.swift` uses `.deviceOwnerAuthentication`, deliberately not `...WithBiometrics`, which is what makes the passcode fallback real |
| Locked pages hidden in the app switcher | `PrivacyLock.swift`: `needsShield && scenePhase != .active` |
| iCloud off until asked, page files and settings separate | `AppSettings.swift`: three independent flags, all read with `UserDefaults.bool(forKey:)`, which is `false` when unset |
| Any page can be left out of iCloud | `PageSettingsView.swift` binds `store.isCloudSynced(current)`; `BulkActions.swift` also offers "Don't Sync with iCloud" for a batch |
| PDF export | `PagePrinting.swift`; `HelpView.swift` describes the same action |

**One finding, now in the README.** Only one source file changed after the release commit: `SettingsView.swift`, moving the in-app privacy link from `brianrenshaw.github.io/folio-privacy/` to `brianrenshaw.app/folio/privacy/`. That change is unreleased, so the build on the App Store still opens the legacy URL. It returns 200 and its policy matches the current one, so users are not reading anything stale, but the legacy Pages repository has to stay published until a build with the new URL has fully replaced 1.1.2. Same class of constraint as the Sparkle feed.

**Method note.** Verifying against a checked-out release commit is better than unpacking whichever IPA happens to be on disk, and it is what should have been done the first time. Confirm `MARKETING_VERSION` and `CURRENT_PROJECT_VERSION` at that commit match the live listing before trusting it.

## Ingest About section rewritten, September 20, 2026

The About section on the Ingest landing page was a single positioning sentence under a bullet list, so the bullets read as a detached feature inventory. It now opens with two short paragraphs and the bullets follow as the same argument.

- The Photo Mechanic sentence changed from "I'm building Ingest as a modern alternative to Photo Mechanic" to "I built Ingest because I wanted a modern Mac app for the part of the workflow Photo Mechanic has covered for years." Still one mention, still out of titles and headlines. A draft of this sentence said "for twenty years"; the age reference was cut because raising a competitor's age is the same move as raising its price.
- A draft also summarized file support as "current RAW support," which would have implied the universal RAW previews this document forbids. The shipped sentence names Sony ARW and Fujifilm RAF.
- New first bullet: "You make the selects. Nothing rates or rejects on your behalf." It has no link, which the existing `.assurance-links` styling handles.
- The Cull section gained one line, "No automatic rating or rejection. Every tag, rating, and label is one you applied," so the claim reaches someone comparing culling tools without a scroll to About. A slogan version ("Ingest doesn't decide anything for you. It tries to make deciding fast") was rejected under the standing rule against slogans and benefit lines.
- A proposed support-page essay, "Why there's no AI culling," was not added. The face close-up strip runs Apple's Vision framework on the Mac, documented on the guide and privacy pages, so a page-length "no AI" argument would contradict them; the bullet is scoped to rating and rejecting and does not. It would also commit a 0.2.1 beta to a permanent roadmap position on a public page.
- The beta note near the download is unchanged and remains the only place the beta is explained. A third About paragraph ending "That's who it's built for first" was dropped as a duplicate of it.
- `python3 scripts/check_site.py` passes: 41 HTML pages, 823 local links and assets.
