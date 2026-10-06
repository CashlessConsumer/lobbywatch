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

- Deploy = push to `main` (GitHub Actions → Pages). Live: https://lobbywatch.cashlessconsumer.in (CNAME added 2026-09-26 on Netlify DNS; HTTP live, HTTPS cert provisioning — see Live status).
- `tests/test_live.py [--base URL]` is the post-deploy smoke test (defaults to custom domain, falls back to GH Pages URL).
- duckdb ≥1.4: explicit column types in CREATE TABLE (build.py emits VARCHAR).
- Per-rule: explicit absolute output paths for any CLI that writes files; `agent-browser screenshot` takes `--full`, not `--full-page`.

## Pipeline (parity with RegTrac/SROTrac, 2026-09-27)

- `scripts/bloggen.py` — builds `blog/index.html` + `blog/<slug>.html` from `blog/posts/*.md` (front matter: title, date, summary; body starts with an H1). Same pattern as SROTrac's bloggen. Inaugural post: 2026-09-26 launch note.
- `scripts/refresh.sh` — daily refresh: gates (`tests/check_data.py`, `tests/verify_urls.py`, both non-fatal — SEBI/IRDAI walls curl from some egresses; GH-runners CI is the arbiter) → `build.py` → `bloggen.py` → second `build.py` (picks new posts up in sitemap/llms) → commit+push on change. No fetch step yet: consultation-index scraper is roadmap item 1; when it lands, add its fetch to refresh.sh.
- Automations: daily refresh 08:00 IST `8de7b8fb-63bd-488b-b02f-1e3b25f25e51`; weekly blog brief Mon 09:30 IST (after the RegTrac/SROTrac 09:20 weeklies) `b59685aa-36af-4c11-a23c-38808801d2f6`. Both post one line to Discord #policy-research (1540886397621458).

## Design language

Shared gazette/ledger skin of the sousveillance stack (paper #ededf0, seal blue #1d4ed8, Fraunces/Newsreader/IBM Plex Mono). SROTrac's `scripts/site.py` CSS is the reference; `css/style.css` here is byte-identical to SROTrac's output (2026-09-26). GOTCHA FIXED 2026-09-26: the port had dropped the `:root{` opener on line 1 — the browser then discarded the whole custom-property block and every `var()`-themed rule (boxes, borders, seal accents, paper tint) silently died while literal rules (grid, ruled-line gradient) kept working, which read as "a different, flatter design". If the skin ever looks unstyled-flat again, check the first byte of css/style.css first. The `.stack` band markup is identical across all three sites, with "you are here" on the live layer — when a sibling's band moves, land it here same-day, and vice versa.

## Roadmap (build order from SOUSVEILLANCE.md)

1. **Scraper**: consultation-paper indexes of the six desks (RBI, SEBI, IRDAI, PFRDA, IBBI, IFSCA) — index URLs already in `regulators.csv`; formats vary wildly, so one parser per desk; run on a schedule, append new papers to `consultations.csv` with status `live`.
2. **Comments corpus**: download published comments (SEBI/IBBI portals); file the RTI templates in `content/rti-templates/` for the rest, log in `rti_log.csv`.
3. **Diff engine**: draft clause → final clause → which commenter's language appears (L0–L5 claim discipline; a match is language-similarity evidence, not proof of causation — say so on the page).
4. **Door ledger expansion**: monthly sweep of PSU board appointments (PIB), exchange/MII filings, SRO governing-council changes (cross-check SROTrac).
5. **Per-consultation pages** (STARTED 2026-10-06, case file #1): `data/consultation_feedback.csv` (consultation_id, seq, feedback, outcome accepted/not_accepted/omitted, response, regulation, commenter_class, inferred) → `build_consultation_detail()` in build.py renders `consultation-<id>.html`; ledger rows link to it when the id has feedback rows. Per-case narrative lives in `TIMELINES` / `CASE_WATCHPOINTS` / `CASE_LEDES` / `CASE_TITLES` / `CASE_DESCS` dicts in build.py. First instance: RBI EXIM FEMA 2026 (https://lobbywatch.cashlessconsumer.in/consultation-rbi-exim-fema-2026.html) — RBI's first published feedback annex on this desk; `comments_published=partial` (responses summarized, commenter identities withheld; annex archived at `notes/evidence/2026-10-06-rbi-exim-fema-2026-feedback-annex.pdf` — live rbidocs CAPTCHA-walls bots, use the repo copy or Wayback).

## Sibling-sync contract

Stack band, masthead anatomy and footer are shared contract. Current state (2026-09-26): all three sites live, bands show LobbyWatch as Layer 3 "you are here" only on this site and as a live link on siblings. RegTrac/SROTrac generate their bands in `scripts/build.py` / `scripts/site.py` respectively.

## Live status (2026-09-26)

- Live at https://lobbywatch.cashlessconsumer.in — DNS CNAME added 2026-09-26; HTTP 200. GitHub Pages LE cert was still provisioning at publish time (https:// returned 000): once `curl -o /dev/null -w "%{http_code}" https://lobbywatch.cashlessconsumer.in/` returns 200, run `gh api -X PUT repos/CashlessConsumer/lobbywatch/pages -f cname=lobbywatch.cashlessconsumer.in -F https_enforced=true` (must be `-F`, not `-f`, or the API 422s on the boolean).
- Doors ledger: 32 sourced moves across 15 people (2026-09-26 expansion added: Mundra→BSE chair 2022, Khuntia→Jana SFB chair 2021, Kanungo→BharatPe 2022 / Shriram Life chair 2023 / IIFL chair 2025, Gopinath→CRISIL 2025, Tyagi→PRISM/Oyo 2026, Bhatia→ICICI Bank 2026, Mahalingam→CARE Ratings 2025 / LIC 2026). Earlier base (RBI DGs Gandhi/Khan/Mundra/Gopinath/Vishwanathan/Kanungo, SEBI WTM Sinha/Saran, IRDAI Panda/Vijayan, RBI DG Thorat). Person strings are canonicalised (one section per human in build_doors, keyed on exact `person`) Malegam (SBI board + RBI committee chair) deliberately excluded — his SBI-directorship half lacks a single citable source; add only when an SBI annual-report citation is in hand.
- Page shell: brand is `Lobby<em>Watch</em>` (the `.brand em` rule expects `em`, not `span` — SROTrac's own markup still has the span variant and renders plain ink; ported correctly here). Stack-band kicker casing follows SROTrac ("The Sousveillance Stack").

## Blog archive layer (2026-09-27)

`scripts/bloggen.py` renders the full archive machinery from `blog/posts/*.md`: `blog/index.html` (latest 12 + year nav), `blog/archive.html` (all editions grouped year → month with category chips), `blog/<year>.html` per year, `blog/feed.xml` (RSS 2.0, latest 20), and patches `sitemap.xml`. Front matter requires `category:` — taxonomy: consultation / doors / rti / interests / weekly / note (default `note`; briefs use `weekly`). The weekly agent (`b59685aa`) is instructed to always set it; on the first Monday of January it writes the annual review edition ("The year in influence <YYYY>").
