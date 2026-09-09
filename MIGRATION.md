# Domain migration — September 8, 2026

## Rollout status

`.app` domains are HSTS-preloaded and require valid HTTPS in browsers. GitHub showing an HTTP deployment URL does not mean the domain is visitor-ready. GitHub has now issued the certificate and HTTPS enforcement is enabled. [Google Registry requirement](https://www.registry.google/domains/app/)

- New public repository and GitHub Actions deployment are working.
- Hover DNS and GitHub domain ownership verification are complete.
- GitHub certificate approved for apex and www; HTTPS enabled. All 19 deployed routes match local HTML over validated TLS. www returns HTTP 301 to the HTTPS apex.
- HTTPS checks passed; all four legacy site repositories received compatibility-page commits.
- Migration documentation is committed and synced in all five requested app repositories and the nested Where Do We Eat website repository. Folio documentation is synced on GitHub main; its local v1.1 privacy-link change is committed locally, leaving five earlier unpublished release commits alone.

## URL mapping

All old paths are on `https://brianrenshaw.github.io`; new paths are on `https://brianrenshaw.app`.

| Old path | New path | Compatibility |
| --- | --- | --- |
| `/reading-habit-site/` | `/reading-habit/` | HTML redirect |
| `/reading-habit-site/guide/` | `/reading-habit/guide/` | Redirect with fragment preservation |
| `/where-do-we-eat-site/` | `/where-do-we-eat/` | HTML redirect |
| `/where-do-we-eat-site/guide/` | `/where-do-we-eat/guide/` | Redirect with fragment preservation |
| `/where-do-we-eat-site/privacy/` | `/where-do-we-eat/privacy/` | Readable legacy policy and canonical link |
| `/chooser-web-app/` | `/whos-first/` | HTML redirect to native app landing |
| `/chooser-web-app/privacy.html` | `/whos-first/privacy/` | Readable legacy policy and canonical link |
| `/chooser-web-app/support.html` | `/whos-first/support/` | Readable legacy support and canonical link |
| `/folio-privacy/` and `/folio-privacy/index.html` | `/folio/privacy/` | Readable legacy policy and canonical link |
| `/folio-privacy/home.html` | `/folio/` | HTML redirect |
| `/folio-privacy/support.html` | `/folio/support/` | Readable legacy support and canonical link |

Keep legacy Pages deployments and Folio's Google verification file indefinitely. Browser redirects preserve query strings and fragments with `location.replace`, include a no-JavaScript fallback, and show a direct link. They are not HTTP 301 redirects. Unknown URLs should return 404. Other GitHub Pages projects are not migrated.

## Apple inventory

Read directly from App Store Connect; all four apps currently have only iOS / en-US records.

| App / ID | Version and state | Action after HTTPS |
| --- | --- | --- |
| Reading Habit / 6809740339 | 1.0 prepare for submission | Draft marketing/support/privacy; no beta localization exists |
| Where Do We Eat / 6808350718 | 1.0 prepare for submission | Draft marketing/support/privacy and TestFlight marketing/privacy |
| Who's First? / 6806757289 | 1.2 ready for sale | Editable URLs; document fields requiring next release; TestFlight URLs |
| Folio / 6803229706 | 1.1.2 ready for sale | Editable URLs; document fields requiring next release; TestFlight URLs |

No additional locales or macOS platform records were returned. Who's First? 1.2 and Folio 1.1.2 downloads were verified against Apple's public lookup. Where Do We Eat's TestFlight public link is enabled and its landing page was verified. Reading Habit has no public download.

Use `appStoreVersionLocalizations` for marketing/support, `appInfoLocalizations` for privacy, and `betaAppLocalizations` for TestFlight URLs. Read back all mutations. Do not create or submit app releases, change release states, modify privacy questionnaire answers, or change app/OAuth/CloudKit identities.

## Validation and limitations

- Static check passes: 20 HTML files (19 routes plus 404); 275 local links/assets, guide anchors, canonical URLs, CSS fonts, and required routes.
- The playable browser version was removed at the user’s request. The legacy chooser homepage now showcases the native iPhone app; the deployment excludes retired game files.
- 21st review reports no findings on the portfolio, app landings and migrated guides.
- Visual browser checks remain pending: no browser is connected to the agent. Verify widths 375, 768 and 1280, keyboard focus, dark appearance, guides, before claiming visual QA complete.

## DNS and rollback

Hover nameservers remain `ns1.hover.com` and `ns2.hover.com`. Four apex A records: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`. The www CNAME is `brianrenshaw.github.io`. Preserve the `_github-pages-challenge-brianrenshaw` TXT verification record and the existing MX `10 mx.hover.com.cust.hostedemail.com`.

Before migration, apex and www resolved to Hover's `216.40.34.41`. No existing app site depended on this domain. Existing GitHub Pages app URLs remain the fallback until HTTPS works. Revert individual website/redirect commits to restore prior content. Confirm old policy/support pages work before reverting Apple URLs.

## References

- [GitHub domain configuration](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
- [GitHub HTTPS recovery](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)
- [Apple privacy URL release timing](https://developer.apple.com/help/app-store-connect/manage-app-information/manage-app-privacy)

## Finish the cutover

Legacy payloads were deployed after HTTPS passed. The following commands document the reproducible rollout. No secret key or token is stored here.

1. Open repository Settings → Pages and confirm the certificate is issued. Enable Enforce HTTPS. Keep DNS unchanged.
2. Run `python3 scripts/check_live.py`. It verifies TLS without disabling certificate checks and compares all deployed HTML routes against local files. During DNS propagation it resolves directly to a GitHub Pages address.
3. Run `python3 scripts/deploy_legacy.py --apply`. It checks HTTPS again, checks all original file hashes and local/remote branch equality, then commits and pushes only the 11 prepared legacy pages. It stops if someone changed the source pages after preparation.
4. Set `APP_STORE_KEY_ID` and `APP_STORE_ISSUER_ID` for the existing App Store Connect API key. Optionally set `APP_STORE_KEY_PATH`; otherwise it reads the matching file from `~/.appstoreconnect/private_keys/`. Install PyJWT and cryptography if unavailable. Run `python3 scripts/update_apple_urls.py` for a fresh inventory, then add `--apply` to update the URL fields. It verifies HTTPS before updates, reads back every successful write, and records release-dependent errors in `migration/apple-results.json`.
5. Check old URLs, query strings and guide fragments; verify www redirects to the apex. Update this log and each app's WEBSITE_MIGRATION.md with final results, then commit and push those records.

Prepared redirect source repositories live in the original project folders; Folio's public website repo is now checked out at `/Users/brianrenshaw/Projects/folio-privacy`. All original app worktrees retain their unrelated changes. The Folio main branch predates its privacy-link UI, so only documentation was changed there; its local release branch carries the URL edit for the next release.

## Native-design correction

Who’s First? uses its current Icon Composer Five Seats, One Table mark and native app screenshots from the existing build-18 capture set. The current native board palette, all three modes and eight visual worlds guide the page design. Support copy now reflects version 1.2. Reading Habit uses the exact current AppIcon-1024.png (unframed gold R), including favicon/social/portfolio derivatives. The browser game and all play links are removed; `/chooser/play/` redirects to the native app landing page. The old chooser-web-app Pages URL now serves the iPhone marketing/support/privacy pages without a game, with its homepage redirect pointing to `/whos-first/`.

Homepage arrows use one shared SVG shape across all app cards, independent of heading typography.

## Remaining screenshot work

Reading Habit needs fresh, publication-ready screenshots; no usable captures of its latest editorial UI were found. Where Do We Eat now uses the clean Work Lunch capture set described below. Fresh Who’s First? simulator capture stalled and was stopped; the published gallery uses existing real native screenshots, including Pinball in flight.

## HTTPS rollout completed

Certificate approved and HTTPS enforced on September 8, 2026. All 19 routes were fetched over valid TLS and matched local files; www redirects to the HTTPS apex. Legacy compatibility pages are committed/pushed for all four websites. App Store Connect draft URLs for Reading Habit and Where Do We Eat and existing TestFlight URL fields were saved and read back. Released Who’s First? and Folio marketing/support/privacy fields require the next editable app version; old support/privacy pages remain readable. See brianrenshaw-app-site/migration/apple-results.json for exact outcomes.

Remaining: clean current Reading Habit screenshots and visual review of other app pages. Where Do We Eat screenshot and responsive review completed September 9. Homepage arrows share one SVG shape.

## September 9: Work Lunch website refresh

Replaced the Where Do We Eat website imagery with four genuine iPhone 17 Pro Max simulator captures: Decide, choices, Log, and Juniper Kitchen visit details. All use an explicitly enabled, isolated in-memory Work Lunch fixture with fictional restaurants and people. The hero retains Decide; a responsive Choices/Log gallery precedes the memory section, which now shows visit details. Published imagery is labeled sample data.

The icon is the exact native 4A red-background AppIcon-light.png master, with an HTML corner mask and square source artwork. Portfolio, landing, subpages, favicon, touch and social references use the refreshed asset; the readable legacy privacy page also uses it. Superseded deployed screenshots and inverted icon bytes are removed. Coral now uses #E8391A in the app and widget; other context tokens and aliases remain unchanged.

Validation: iOS Simulator and macOS builds passed; DiningType color/alias tests and native screenshot navigation tests passed. Native light/dark screens were inspected. Isolated Chromium checks passed at 375, 834 and 1440px, including dark appearance, keyboard focus, reduced motion, image loading, icon masking and no horizontal overflow. The static checker passes 20 HTML pages and 279 local links/assets. Reading Habit screenshot work and visual review of other app pages remain separate. No App Store Connect metadata or TestFlight changes were made.

## People and context messaging refinement

The dining landing page now explains context collections, selected guests, and per-person do-not-recommend exclusions. A compact Choose/Remember showcase replaces the two tall screenshot columns, using the same unmodified native assets and sample-data captions. Keyboard tabs, full-size image links, reduced motion and no-JavaScript fallback verified at 375, 834 and 1440px in light/dark Chromium. Static checker passes 20 pages and 283 links/assets. No native app or compatibility-route changes.
