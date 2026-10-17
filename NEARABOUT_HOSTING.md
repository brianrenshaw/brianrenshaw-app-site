# Nearabout website

Source: `site/nearabout/`. Standalone output: `dist/nearabout/`.

Build and validate with `python3 scripts/build_nearabout_site.py`. Cloudflare Pages
uses this repository, production branch `main`, no framework, repository root,
that build command, and output directory `dist/nearabout`.

Cloudflare project: `nearabout-app` (`nearabout-app.pages.dev`). Primary domain: `nearaboutapp.com`.
Attach both apex and `www` through Pages Custom domains. Configure the www-to-apex
redirect in Cloudflare Redirect Rules, preserving paths and query strings.
Pages `_redirects` only supports relative source paths. Registration remains
at Hover. Import existing DNS records and verify DNSSEC before replacing Hover's
nameservers with the nameservers assigned to this Cloudflare zone.

Cloudflare reference: https://developers.cloudflare.com/pages/configuration/custom-domains/

## Message and design

The owner clarified that Nearabout is for cataloging your places to share with
others and make plans. It is not positioned as a personal favorites app for saving
new discoveries. Vacation research remains a use case. Route planning is equally
important: lists and routes are related but distinct uses, useful together or on
their own. Never describe routes as merely optional supporting utility.
The owner explicitly rejected slogan copy, including “Keep the recommendation.
Skip the hunt.” and “Good places deserve a place of their own.” Do not restore
those phrases or imitate that style with all-caps labels and punchy abstractions.

Write like a person: sending a friend your recommendations, showing someone around,
and putting together plans. The homepage opens with “I’ll send you my list.” and
introduces both sharing recommendations and planning a route immediately below.
Two matching sections explain sharing a list and ordering route stops. They replace
the sharing-only three-step sequence to keep the page short and give both uses room.

StoryBrand informs the structure, not the vocabulary: the visitor knows places they
want to share or visit together; putting those recommendations into something useful
takes effort. A separate need is working out the order and timing of multiple stops.
Nearabout helps with both, without requiring someone to share a list before planning
a route or turn every recommendation list into a route. Avoid exaggerated stakes, fabricated testimonials,
guaranteed time savings, and a long feature inventory.
Reference: https://storybrand.com/downloads/your-brand-is-not-the-hero.pdf

Visual direction: a restrained street atlas with paper, forest green, vermilion,
Newsreader headings, a fictional decorative map, and genuine device captures.
Static HTML/CSS; no framework, application JavaScript, or remote fonts.
Cloudflare injects its Web Analytics beacon on the custom domain; the website
privacy section discloses performance and page-view measurement.
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

## Deployment record

Created the Git-connected Cloudflare Pages project on October 16, 2026.
Production follows `main`; build output is `dist/nearabout`. Registered apex and
www custom domains with Pages and changed their imported parking records to
proxied CNAMEs targeting `nearabout-app.pages.dev`. Hover nameservers were changed
to `anna.ns.cloudflare.com` and `cesar.ns.cloudflare.com`; Cloudflare confirmed
the zone active. No MX records or DNSSEC delegation existed during migration.
The portfolio export redirects Nearabout pages to the dedicated domain, preserving
query strings and anchors.

Cloudflare Redirect Rule `Nearabout www to main domain` matches
`http.host eq "www.nearaboutapp.com"` and returns a 301 to
`concat("https://nearaboutapp.com", http.request.uri.path)`, preserving query strings.
Verified both HTTP and HTTPS, nested paths, and query strings. Apex HTTP redirects
to HTTPS. Both custom-domain certificates are active. Live HTML, screenshots,
stylesheet, font, social image, robots, and sitemap were fetched successfully.
