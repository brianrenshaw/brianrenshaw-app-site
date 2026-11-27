# Decks domain deployment

Live as of October 1, 2026: `https://decksphotoapp.com/` serves Decks.
`decksphoto.app`, `decksphoto.com`, and all three `www` variants redirect to
the primary HTTPS address with status 301, preserving paths and queries.
All three domains remain registered at Hover and use `anna.ns.cloudflare.com`
and `cesar.ns.cloudflare.com`. Cloudflare's GitHub app is limited to this repository.

Decks's dedicated website is built from `site/decks/` in this repository.
Keep editing those source pages and assets; do not edit generated files.
`python3 scripts/build_decks_site.py` generates and validates `dist/decks/`,
rewriting Decks routes and metadata for `https://decksphotoapp.com/` and copying
the shared styles. Portfolio links stay on `brianrenshaw.app`; Ingest links lead to `ingestphotoapp.com`.

## Cloudflare Pages configuration

| Setting | Value |
| --- | --- |
| Project name | `decks-photo-app` |
| Repository | `brianrenshaw/brianrenshaw-app-site` |
| Production branch | `main` |
| Framework preset | None |
| Root directory | Repository root |
| Build command | `python3 scripts/build_decks_site.py` |
| Build output directory | `dist/decks` |
| Custom domain | `decksphotoapp.com` |

The portfolio at `brianrenshaw.app` is the Cloudflare Pages project `brianrenshaw-app`, built with
`python3 scripts/build_portfolio_site.py` (GitHub Pages until November 27, 2026; see HOSTING.md).
The dedicated Decks build is also checked in CI.

## Domains

Keep registration at Hover. Add each domain as a Free Cloudflare zone, copy
all existing DNS records (especially MX and mail TXT records), then replace
its Hover nameservers with the two nameservers assigned to that specific zone.
Check DNSSEC status before switching; an old DS record must not remain when
changing DNS providers. After activation, attach `decksphotoapp.com` through
the Pages project's Custom domains screen rather than only adding DNS manually.

For `decksphoto.app` and `decksphoto.com`, the imported Hover A records for `@`
and `www` are proxied so Cloudflare handles the redirects before contacting
an origin. For a new redirect-only domain, `192.0.2.1` can be used instead,
following Cloudflare's redirect-only-domain guide.
Create a Single Redirect on each zone matching its apex and `www` hostnames:

```text
concat("https://decksphotoapp.com", http.request.uri.path)
```

Use status 301 and enable Preserve query string. For the main zone, add a
proxied `www` DNS record and a Single Redirect matching only
`www.decksphotoapp.com`, with the same target expression and settings. Enable
Always Use HTTPS on the main domain. Verify active edge certificates on every
hostname, especially `.app`, which browsers require to work over HTTPS.

## Portfolio deployment

The real Decks source stays at `site/decks/`. The portfolio export changes
the homepage's Decks links to the dedicated domain, replaces the three old
Decks pages in the generated output with redirect stubs preserving queries
and fragments, and removes old Decks URLs from the portfolio sitemap. Since November 27, 2026, Cloudflare Pages answers these routes with
server-side 301s from the generated `_redirects` file; the JavaScript stubs with
a no-JavaScript refresh fallback remain in the output as a fallback. Decks assets stay
available at their old addresses, including the portfolio card's app icon.

Always publish the generated `dist/portfolio/` output (the `brianrenshaw-app`
Pages project does this); publishing `site/` directly would restore the old Decks pages.
Update app and App Store website/support/privacy URLs as a separate release
task; old installed apps must still reach the existing support/privacy routes.

## Verification

Run `python3 scripts/check_site.py`, `python3 scripts/build_decks_site.py`, and
`python3 scripts/build_portfolio_site.py`.
Preview with `python3 -m http.server 8081 --directory dist/decks`.
Check the landing, support, and privacy pages, icons, screenshots, shared
styles, portfolio link, Ingest link, and TestFlight link.
Verify HTTP and HTTPS requests to all aliases and `www` variants reach the
primary domain with permanent redirects, preserving `/support/?test=1`.

References: [Pages custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/),
[redirect-only domains](https://developers.cloudflare.com/fundamentals/manage-domains/redirect-domain/).

## October 19, 2026 release preparation

Both iOS 1.0 (171) and Mac 1.0 (170) are WAITING_FOR_REVIEW, verified live. Keep TestFlight calls to action until the app is approved and publicly available. The landing page and help now explain the five-batch free allowance, Pro, trial, restore, and TestFlight purchase limitations. On public release, replace beta calls to action with https://apps.apple.com/app/id6817408326 and update the install guide, support source, portfolio status, and generated help pages together. Do not advertise the deferred Smart Layout pricing proposal.

## App Store release — November 27, 2026

Decks Photo App 1.0 is live on the App Store (https://apps.apple.com/app/id6817408326), released November 26, 2026: one universal listing for iPhone, iPad, and Mac (iOS 171, Mac 170). Verified November 27 through Apple's lookup API and the public listing: free download; in-app purchases Decks Pro Monthly $1.99, Annual $9.99, Lifetime $24.99 (USD); requires iOS/iPadOS 18 and macOS 15 on M1 or later.

Site changes for the release:

- Every TestFlight call to action now points to the App Store. The homepage, Aura page, and the closing and pricing sections use Apple's official black "Download on the App Store" badge (`assets/app-store-badge-black.svg`, downloaded unmodified from toolbox.marketingtools.apple.com). The header link reads "App Store ↗".
- Every Decks page has the Smart App Banner (`<meta name="apple-itunes-app" content="app-id=6817408326">`), and the homepage has SoftwareApplication JSON-LD.
- The homepage pricing section shows Free, Decks Pro, and Lifetime cards with US prices, plus five pricing questions whose answers come from `SocialProView.swift` and `SocialAccessController.swift` at build 171.
- The help center footer reads "Decks 1.0 on the App Store." The install guide and the support hub explain App Store installation and moving from the TestFlight beta (the App Store version replaces the beta build; TestFlight purchases do not carry over).
- The portfolio card reads "Free on the App Store" and links to the listing.

App Store Connect campaign links (`pt=` provider token plus `ct=`) are not used yet. To add them, get the provider token from App Store Connect → Apps → Analytics → Campaigns and tag each badge (for example `ct=website-hero`, `ct=website-pricing`).
