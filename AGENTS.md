# LobbyWatch — agent conventions

Layer 3 (rule-buyers) of the sousveillance stack: RegTrac (rule-writers, `Projects/regtrac/`) · SROTrac (rule-borrowers, `Projects/srotrac/`) · LobbyWatch (this). Read `Projects/regtrac/SOUSVEILLANCE.md` for the stack contract; keep layer language consistent ("rule-writers / rule-borrowers / rule-buyers").

## Scope rules

- **LobbyWatch = the interests acting on the policy landscape**: consultation records, comment disclosure, access (RTI), revolving doors. Statutory regulators themselves belong to RegTrac; SRO rosters belong to SROTrac (layer-link, never duplicate rosters — the `sro-layer` class in `interests.csv` is a cross-link, not a roster).
- Every row carries `source_url` + `as_of`. Unverified = say "unverified — flagged for checking" in the note; never silently assert.
- No insinuation without a paper trail. A door move is documented only with a dated press/regulatory/filing source. Meeting access is documented through RTI replies, minutes or published attendee lists — not vibes.
- Person naming: public figures in public roles only (regulator officials' post-retirement appointments are public record).

## Data

- Single source of truth: `data/*.csv` → `python3 scripts/build.py` regenerates all HTML + `data/lobbywatch.duckdb` + llms.txt/llms-full.txt + sitemap + robots + og.png. Never hand-edit generated HTML.
- `publishes_comments` / `comments_published` enums: `yes` / `no` / `partial` / `unknown` / `proposed` (a formally proposed-but-unnotified reform).
- `tests/check_data.py` (offline QA) must pass before any push; `tests/verify_urls.py` re-verifies every source URL (all 200). Both run before build in CI-minded edits.

## Build & deploy

- Deploy = push to `main` (GitHub Actions → Pages). Live: https://lobbywatch.cashlessconsumer.in (CNAME in repo; **DNS CNAME record `lobbywatch → cashlessconsumer.github.io` needs manual add on Netlify DNS** — token cannot write DNS records; until then the site serves at https://cashlessconsumer.github.io/lobbywatch/).
- `tests/test_live.py [--base URL]` is the post-deploy smoke test (defaults to custom domain, falls back to GH Pages URL).
- duckdb ≥1.4: explicit column types in CREATE TABLE (build.py emits VARCHAR).
- Per-rule: explicit absolute output paths for any CLI that writes files; `agent-browser screenshot` takes `--full`, not `--full-page`.

## Design language

Shared gazette/ledger skin of the sousveillance stack (paper #ededf0, seal blue #1d4ed8, Fraunces/Newsreader/IBM Plex Mono). SROTrac's `scripts/site.py` CSS is the reference; `css/style.css` here is ported from it. The `.stack` band markup is identical across all three sites, with "you are here" on the live layer — when a sibling's band moves, land it here same-day, and vice versa.

## Roadmap (build order from SOUSVEILLANCE.md)

1. **Scraper**: consultation-paper indexes of the six desks (RBI, SEBI, IRDAI, PFRDA, IBBI, IFSCA) — index URLs already in `regulators.csv`; formats vary wildly, so one parser per desk; run on a schedule, append new papers to `consultations.csv` with status `live`.
2. **Comments corpus**: download published comments (SEBI/IBBI portals); file the RTI templates in `content/rti-templates/` for the rest, log in `rti_log.csv`.
3. **Diff engine**: draft clause → final clause → which commenter's language appears (L0–L5 claim discipline; a match is language-similarity evidence, not proof of causation — say so on the page).
4. **Door ledger expansion**: monthly sweep of PSU board appointments (PIB), exchange/MII filings, SRO governing-council changes (cross-check SROTrac).
5. **Per-consultation pages**: timeline of access + transparency scorecard per regulator (the index scorecard is the seed).

## Sibling-sync contract

Stack band, masthead anatomy and footer are shared contract. Current state (2026-09-26): all three sites live, bands show LobbyWatch as Layer 3 "you are here" only on this site and as a live link on siblings. RegTrac/SROTrac generate their bands in `scripts/build.py` / `scripts/site.py` respectively.

## Live status (2026-09-26)

- Live at https://lobbywatch.cashlessconsumer.in — DNS CNAME added 2026-09-26; HTTP 200. GitHub Pages LE cert was still provisioning at publish time (https:// returned 000): once `curl -o /dev/null -w "%{http_code}" https://lobbywatch.cashlessconsumer.in/` returns 200, run `gh api -X PUT repos/CashlessConsumer/lobbywatch/pages -f cname=lobbywatch.cashlessconsumer.in -F https_enforced=true` (must be `-F`, not `-f`, or the API 422s on the boolean).
- Doors ledger: 22 sourced moves (RBI DGs Gandhi/Khan/Mundra/Gopinath/Vishwanathan/Kanungo, SEBI WTM Sinha/Saran, IRDAI Panda/Vijayan, RBI DG Thorat). Malegam (SBI board + RBI committee chair) deliberately excluded — his SBI-directorship half lacks a single citable source; add only when an SBI annual-report citation is in hand.
- Page shell: brand is `Lobby<em>Watch</em>` (the `.brand em` rule expects `em`, not `span` — SROTrac's own markup still has the span variant and renders plain ink; ported correctly here). Stack-band kicker casing follows SROTrac ("The Sousveillance Stack").
