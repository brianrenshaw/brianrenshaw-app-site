# Brian Renshaw’s app websites

Canonical website: https://brianrenshaw.app/

One static website for Reading Habit, Where Do We Eat, Who’s First?, and Folio. App source code remains in its existing repositories. Edit public website content here; legacy Pages repositories preserve older links.

## Local preview and checks

```sh
python3 scripts/check_site.py
python3 -m http.server 8080 --directory site
```

Open http://localhost:8080/. Links are root-relative because production is served from the custom domain root. The default GitHub project URL is not a supported preview without that domain; use the local server.

GitHub Actions validates links, anchors, local assets and canonical addresses before deploying `site/` to Pages on pushes to main. Pull requests validate without deploying. No build framework, package installation, analytics, or external font dependency is needed.

## Routes

| App | Path | Supporting pages |
| --- | --- | --- |
| Reading Habit | `/reading-habit/` | `guide/`, `support/`, `privacy/` |
| Where Do We Eat | `/where-do-we-eat/` | `guide/`, `support/`, `privacy/` |
| Who’s First? | `/whos-first/` | `support/`, `privacy/` |
| Folio | `/folio/` | `support/`, `privacy/` |

Support email remains contact@brianrenshaw.app. Keep app-specific privacy policies accurate; don’t substitute a generic portfolio policy. Existing policy language was preserved, and Reading Habit’s new policy reflects its local implementation (private iCloud, Open Library/Apple cover lookups, user-selected link resolution and imports).

See `MIGRATION.md` for rollout status, legacy mapping, DNS, Apple metadata and rollback. See `.21st/DESIGN.md` for the four visual directions.

Spreadsheet Tools lives at `/spreadsheet-tools/`. Its React source remains in the sibling `spreadsheet-webapp` repository (`brianrenshaw/spreadsheet-tools` on GitHub). Run that project's `scripts/sync-website.py` to rebuild and copy generated files here, then commit and push this repository. Keep the utility link at the bottom of the portfolio. See that project's `WEBSITE_MIGRATION.md` for the complete workflow.
