# App messaging

Approved with Brian on September 9, 2026. Use these promises for homepage cards, app landing pages, search/social descriptions, and future app copy. The customer’s goal comes first; features support that goal.

## Approved messages

### Reading Habit

**Headline:** Make reading a daily habit.

**Supporting copy:** Mark the days you read without counting pages, chapters, or minutes. See your consistency grow and work toward your own monthly book goal.

**Priority:** Daily reading consistency. A little reading counts, regardless of how much. Monthly book goals chosen by the reader. Five books is a starting point, not a requirement.

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

**Visual direction:** Keep the existing project card structure. Use a muted rose background, standard system headline typography at the shared 500 weight, and smaller, thinner LL letters in the baseball-diamond icon. No yellow accents, heavy serif headline, or dark navy card in light mode.

**Scope:** This copy describes the linked blog at https://lankfordlegends.co/. Updating this portfolio card does not change the blog’s publishing system or content.

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
