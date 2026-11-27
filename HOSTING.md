# Hosting

Every site in this repository is served by Cloudflare Pages in the Cloudflare account “Brenshaw@sbts.edu's Account”. Each Pages project is connected to `brianrenshaw/brianrenshaw-app-site` and builds `main` on every push. The projects build independently from the same commit.

| Site | Pages project | Build command | Output |
| --- | --- | --- | --- |
| https://brianrenshaw.app/ | `brianrenshaw-app` | `python3 scripts/build_portfolio_site.py` | `dist/portfolio` |
| https://decksphotoapp.com/ | `decks-photo-app` | `python3 scripts/build_decks_site.py` | `dist/decks` |
| https://ingestphotoapp.com/ | `ingest-photo-app` | `python3 scripts/build_ingest_site.py` | `dist/ingest` |
| https://nearaboutapp.com/ | `nearabout-app` | `python3 scripts/build_nearabout_site.py` | `dist/nearabout` |

GitHub Actions (`.github/workflows/pages.yml`) only validates: it runs the site checker and every build on pushes and pull requests. It no longer deploys anything.

## brianrenshaw.app (moved from GitHub Pages, November 27, 2026)

- **Domain and DNS.** Registered at Hover. The nameservers are `anna.ns.cloudflare.com` and `cesar.ns.cloudflare.com`, as on the other domains. The zone became active on November 27, 2026.
- **Web records.** The apex is a proxied CNAME to `brianrenshaw-app.pages.dev`. `www` is proxied, and a Single Redirect rule sends it to `https://brianrenshaw.app` with a 301, keeping the path and query string. Always Use HTTPS is on.
- **Email stays with Hover.** Copied unchanged from Hover:
  - MX `10 mx.hover.com.cust.hostedemail.com`
  - SPF `v=spf1 include:_spf.hostedemail.com ~all`
  - `mail` CNAME `mail.hover.com.cust.hostedemail.com` (DNS only)
  - `_dmarc` `v=DMARC1; p=none;`
  - The `_github-pages-challenge-brianrenshaw` TXT record is kept because it marks the domain as verified on GitHub.
- **Email Obfuscation is on, matching the other zones.** It rewrites `mailto:` links on the served pages. Turn it off in the zone's Scrape Shield settings if those links must work without JavaScript.
- **Old app routes.** `scripts/build_portfolio_site.py` writes `dist/portfolio/_redirects`, which answers old `/decks/`, `/ingest/`, and `/nearabout/` page routes with 301s to each app's domain, keeping query strings. The JavaScript stub pages stay in the output as a fallback. These are never redirected:
  - asset URLs
  - `/ingest/release-notes/`
  - the appcast feeds (`/listing-namer/appcast.xml`, `/ingest/appcast.xml`)
- **GitHub Pages.** The repository's GitHub Pages site and its custom domain were removed after Cloudflare was verified. The legacy GitHub Pages projects (`folio-privacy`, `reading-habit-site`, `spreadsheet-tools`) are separate repositories at `brianrenshaw.github.io/...`. They are unaffected and still point visitors to `brianrenshaw.app`.

Verified November 27, 2026, through Cloudflare:
- The homepage returns 200, and a 404 returns 404.
- `/decks/support/?test=1` returns a 301 to `https://decksphotoapp.com/support/?test=1`.
- `/ingest/` and `/nearabout/` return 301s to their domains.
- The appcasts and `/ingest/release-notes/` return 200.
- `www` and `http://` return 301s to `https://brianrenshaw.app/`.
- The certificate is valid.
