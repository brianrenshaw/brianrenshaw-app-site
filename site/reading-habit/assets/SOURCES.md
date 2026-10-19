# Reading Habit website assets

Updated October 19, 2026 for the submitted 1.0.1 (12) release.

The `v1-0-1-*.webp` images are genuine, unretouched simulator screenshots from the Reading Habit app in `../book-tracker`. They were captured on dedicated iPhone 17 Pro and iPad Pro 13-inch simulators with isolated sample books and CloudKit disabled. `AppStoreScreenshots.testStoreScreenshots` passed on both devices. Files preserve the source dimensions and decoded RGB pixels using lossless WebP. Exact source paths, dimensions, and hashes are recorded in `screenshots-v1-0-1.json`.

The landing page shows Journal, Stats, Library, book detail, and recommendations. The guide uses the new iPad Stats image. Captions identify these as previews while 1.0.1 awaits App Review. Version 1.0 remains the public App Store download at publication time. Do not describe submission as public availability.

`social-v1-0-1.png` is the submitted search-results marketing artwork from `book-tracker/marketing/app-store/search.png`, 1920 × 1280. It was generated from a real Journal reference, with the app's serif type, paper background, rules, and dated gold checks. It is an illustration used for link previews, not an unretouched screenshot. Generation provenance is in the app's `marketing/app-store/README.md`.

Existing image URLs are retained for compatibility. The native gold R icon and product promise are unchanged, so the portfolio card needs no update.

Validation: `scripts/check_site.py`; desktop and 390 × 844 mobile browser review; Library preview activation and guide anchor navigation. `21st search` returned HTTP 401, so the existing site primitives were reused. `21st review` covered the landing HTML and CSS; its 17 informational findings are the established local color tokens, with no automatic changes.

After Apple releases 1.0.1, verify its public availability and remove the preview labels and pending-review wording from the landing page, guide, and support page together.
