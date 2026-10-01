# Decks domain deployment

Decks's dedicated website is built from `site/decks/` in this repository.
Keep editing those source pages and assets; do not edit generated files.
`python3 scripts/build_decks_site.py` generates and validates `dist/decks/`,
rewriting Decks routes and metadata for `https://decksphotoapp.com/` and copying
the shared styles. Portfolio and Ingest links stay on `brianrenshaw.app`.

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

GitHub Pages continues deploying `site/` for the portfolio. Its custom domain
must remain `brianrenshaw.app`. The dedicated Decks build is also checked in CI.

## Domains

Keep registration at Hover. Add each domain as a Free Cloudflare zone, copy
all existing DNS records (especially MX and mail TXT records), then replace
its Hover nameservers with the two nameservers assigned to that specific zone.
Check DNSSEC status before switching; an old DS record must not remain when
changing DNS providers. After activation, attach `decksphotoapp.com` through
the Pages project's Custom domains screen rather than only adding DNS manually.

For `decksphoto.app` and `decksphoto.com`, use proxied A records for `@` and
`www` pointing to `192.0.2.1`, following Cloudflare's redirect-only-domain guide.
Create a Single Redirect on each zone matching its apex and `www` hostnames:

```text
concat("https://decksphotoapp.com", http.request.uri.path)
```

Use status 301 and enable Preserve query string. For the main zone, add a
proxied `www` DNS record and a Single Redirect matching only
`www.decksphotoapp.com`, with the same target expression and settings. Enable
Always Use HTTPS on the main domain. Verify active edge certificates on every
hostname, especially `.app`, which browsers require to work over HTTPS.

## Cutover

Do not switch portfolio links or replace the old pages until the dedicated
HTTPS website is live and verified. Then update the portfolio's Decks link,
replace the three old Decks pages with redirect stubs preserving query strings
and fragments, and remove their old addresses from the portfolio sitemap.
Keep the source pages for the dedicated build: if the old routes become stubs,
move the real source to a separate folder and update the build script first.
Update app and App Store website/support/privacy URLs as a separate release
task; old installed apps must still reach the existing support/privacy routes.

## Verification

Run `python3 scripts/check_site.py` and `python3 scripts/build_decks_site.py`.
Preview with `python3 -m http.server 8081 --directory dist/decks`.
Check the landing, support, and privacy pages, icons, screenshots, shared
styles, portfolio link, Ingest link, and TestFlight link.
Verify HTTP and HTTPS requests to all aliases and `www` variants reach the
primary domain with permanent redirects, preserving `/support/?test=1`.

References: [Pages custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/),
[redirect-only domains](https://developers.cloudflare.com/fundamentals/manage-domains/redirect-domain/).
