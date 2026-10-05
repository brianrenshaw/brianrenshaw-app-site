# Ingest domain deployment

Live as of October 5, 2026: https://ingestphotoapp.com/.

Ingest's dedicated Cloudflare Pages website is built from `site/ingest/` in
this repository for `https://ingestphotoapp.com/`. Keep editing the source
pages and assets; do not edit generated files.

`python3 scripts/build_ingest_site.py` exports `dist/ingest/`, rewrites routes,
search data and scripts, canonical/social metadata, and shared styles for the
new root domain. It validates all local links, fragments, search entries,
source anchors, CSS assets, and Cloudflare's per-file size limit. Archived
captures and current videos are included. A real 404 page prevents the Pages
SPA fallback. `/ingest/*` redirects to the equivalent root route, and
`/quick-start/` redirects to `/getting-started/`.

## Cloudflare Pages configuration

| Setting | Value |
| --- | --- |
| Project | `ingest-photo-app` |
| Repository | `brianrenshaw/brianrenshaw-app-site` |
| Production branch | `main` |
| Framework | None |
| Root directory | Repository root |
| Build command | `python3 scripts/build_ingest_site.py` |
| Output | `dist/ingest` |
| Custom domain | `ingestphotoapp.com` |

The existing GitHub integration is already authorized for this repository.
Do not expand its repository access. Cloudflare deploys this site and Decks
independently from the same source repository; GitHub Pages continues to serve
the generated `dist/portfolio/` export at `brianrenshaw.app`.

## DNS

Registration stays at Hover. The new domain originally had only Hover parking
A records (`@` and `*`, `216.40.34.41`), with no mail records or published DS.
Cloudflare assigned `anna.ns.cloudflare.com` and `cesar.ns.cloudflare.com`.
Both were saved at Hover on October 5, 2026. The Free Cloudflare plan is used.
Attach the apex through Pages Custom domains so both the DNS record and Pages
hostname binding are configured. `www` redirects permanently to the apex,
preserving path and query. Always Use HTTPS is enabled for the zone.

## Compatibility and cutover

Publish and verify the new domain before publishing the portfolio redirects.
`build_portfolio_site.py` keeps all Ingest assets at their historical URLs and
replaces its old HTML pages with redirects that preserve query strings and
fragments. Quick Start goes directly to Getting Started. The portfolio card leads directly to the new domain. The standalone Decks
build also rewrites any Ingest navigation links to the dedicated domain.
Old Ingest URLs are removed from the portfolio sitemap.

**`https://brianrenshaw.app/ingest/appcast.xml` is permanent.** Installed apps
have that URL compiled into them. The portfolio build preserves its exact
source bytes, including signed enclosure metadata and GitHub release URLs.
The new website also serves an unchanged copy at `/appcast.xml`; it is not a
replacement for the installed app's feed. Existing release-note anchors
continue through the old-route redirect. Native app URL changes are a separate
release task, not part of this website migration.

## Checks

Run the site, screenshot, and interaction checks plus all three site exports.
Run `python3 scripts/check_ingest_live.py` for the dedicated domain and
`python3 scripts/check_live.py` for the portfolio after deployment.
Preview `dist/ingest` at the server root. Verify `/`, all guides, Search,
workspace dialogs, screenshots, video, the download link, social metadata,
sitemap, 404, and Quick Start. Check apex and `www` over HTTP and HTTPS,
including `/support/?test=1`, for HTTPS and canonical-host redirects.
Compare live HTML/assets with the generated export; verify old media and the
permanent feed still match their source bytes after the portfolio cutover.

References: [Pages custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/),
[monorepos](https://developers.cloudflare.com/pages/configuration/monorepos/).

## October 5 verification

The Cloudflare custom domain reports Active with SSL enabled. The www redirect
rule is `cf5231a45e364eb1abf585b56e5ec98c`, matching only
`www.ingestphotoapp.com`, with a dynamic apex target, status 301, and Preserve
query string enabled. The zone is `c1fbee0f656800e93d306a92a5259d4a`.

The cutover deployment (`46d609a`) passed GitHub Pages and both Cloudflare
project builds. All nine content pages, current media, search assets, fonts,
metadata, sitemap, HTTPS/www/path/query redirects, 404, historical media, and
the permanent feed passed live verification. Chrome confirmed site search,
workspace/full-resolution dialogs, video playback, and the old Guide URL
redirecting with both its query string and `#workspaces` fragment preserved.
Cloudflare's default email obfuscation may transform public contact links at
the edge; the live checker accounts for that while checking navigation and
metadata. Decks's existing pages remain available.
