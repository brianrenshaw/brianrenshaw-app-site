# Nearabout website

Source: `site/nearabout/`. Standalone output: `dist/nearabout/`.

Build and validate with `python3 scripts/build_nearabout_site.py`. Cloudflare Pages
uses this repository, production branch `main`, no framework, repository root,
that build command, and output directory `dist/nearabout`.

Intended project: `nearabout-app`. Primary domain: `nearaboutapp.com`.
Attach both apex and `www` through Pages Custom domains. The generated `_redirects`
permanently redirects www to the apex and preserves paths. Registration remains
at Hover. Import existing DNS records and verify DNSSEC before replacing Hover's
nameservers with the nameservers assigned to this Cloudflare zone.

Cloudflare reference: https://developers.cloudflare.com/pages/configuration/custom-domains/

## Message and design

The owner clarified that Nearabout is primarily for making personal lists of
places to try and sharing recommendations. Routes are optional supporting utility.
The owner explicitly rejected slogan copy, including “Keep the recommendation.
Skip the hunt.” and “Good places deserve a place of their own.” Do not restore
those phrases or imitate that style with all-caps labels and punchy abstractions.

Write like a person: remembering a restaurant someone mentioned, looking forward
to trying it, and sending thoughtful recommendations to a friend. The homepage
opens with “Remember that place you wanted to try?” and explains what the app does
in the paragraph immediately below. Plain three-step instructions follow the
personal reason to use the app. Routes appear last among the supporting uses.

StoryBrand informs the structure, not the vocabulary: the visitor wants to remember
and share places; recommendations are easy to lose; Nearabout helps them collect
places, add context, and share a usable list. Avoid exaggerated stakes, fabricated
testimonials, guaranteed time savings, and a long feature inventory.
Reference: https://storybrand.com/downloads/your-brand-is-not-the-hero.pdf

Visual direction: a restrained street atlas with paper, forest green, vermilion,
Newsreader headings, a fictional decorative map, and genuine device captures.
Static HTML/CSS; no framework, runtime JavaScript, remote fonts, or analytics.
21st catalog search returned HTTP 401, so no catalog components were imported.
21st review found only intentional local palette values.

## Availability

On October 16, 2026 the public invitation at
https://testflight.apple.com/join/prASAccF said it was not accepting new testers.
The site therefore says coming soon and offers “Check TestFlight availability.”
Recheck Apple's public page before changing this to “Join the beta.” Do not
equate internal TestFlight processing with availability to public visitors.

Product claims were checked against the sibling `NearMe/README.md` and
`App/Views/HelpGuideView.swift`: saved lists and private iCloud, notes and groups,
export formats, the one-time Notes Shortcut, seven-stop routes, and OS requirements.

## Validation

Run the site validator, standalone Nearabout build, and portfolio build. CI includes
the Nearabout build. The standalone build checks canonical URLs, local links,
fragments, images and CSS font references, and generates the sitemap and robots.
Asset provenance is in `site/nearabout/assets/SOURCES.md` and `screenshots.json`.

## Owner-provided situations

Vacation lists grouped by restaurants, coffee shops, and stores, with routes only
when ready to go; real estate agents presenting nearby amenities and travel details
in social posts; food lovers sharing recommendations by text; schools introducing
the surrounding area; parents arranging five errands; friends planning a bar crawl;
and someone planning an afternoon. These real uses replace generic feature slogans.
The page groups them into four short situations so it stays simple.

Starting points are general: current location or any chosen address. Houses and
schools are examples only, never the defining audience or scope of nearby lists.
