# LobbyWatch — the rule-buyers, watched

*Surveillance is watching citizens; **sousveillance** is citizens watching back.*

**LobbyWatch is the watch tower for the various interests acting on India's financial policy landscape**: the industry bodies, think tanks, foreign lobbies and consumer-side researchers that flood consultations, get the meetings, and hire the regulators after retirement. Access and influence are documented through published comments, RTI replies, minutes and appointment orders — not vibes.

Layer 3 of the **sousveillance stack**:

| Layer | Site | Watches |
| --- | --- | --- |
| 1 · rule-writers | [RegTrac](https://regtrac.cashlessconsumer.in) | Statutory financial regulators: RBI, SEBI, IRDAI, PFRDA, IBBI, IFSCA, NABARD… |
| 2 · rule-borrowers | [SROTrac](https://srotrac.cashlessconsumer.in) | RBI-recognised SROs and their member rosters |
| 3 · rule-buyers | **LobbyWatch** (this site) | Consultations, access (RTI), revolving doors, the interests register |

**Live**: https://lobbywatch.cashlessconsumer.in

## What's in the register

- **Comment-transparency scorecard** — per consultation desk: does the regulator publish what was said to it? RBI: no general practice. SEBI and IBBI: yes. IRDAI: reform proposed (Jun 2026), not yet notified. PFRDA/IFSCA: unverified, flagged for checking.
- **Consultation ledger** — one row per tracked consultation paper (opened, closed, comments published?, outcome), with source links.
- **Interests register** — who acts on policy: PCI, IAMAI, NASSCOM, IBA, FICCI, CII, ASSOCHAM, USISPF, iSPIRT, Digital India Foundation; consumer-side researchers (Vidhi, Dvara, CUTS); and layer-links to the SRO layer tracked in SROTrac.
- **Revolving-door ledger** — documented post-retirement moves (R. Gandhi → Yes Bank/Sahamati; H.R. Khan → Bandhan/AU SFB; U.K. Sinha → Vedanta/NDTV/Nippon MF…), each row sourced and stamped "as of".
- **Access & RTI playbook** — copy-paste RTI templates for comment disclosure and committee minutes, plus the request log.

## Ground rules

1. Public data first: statutes, gazettes, regulator websites, RTI, published rosters.
2. Every claim sourced per row, with an "as of" date.
3. Corrections visible, never silent.
4. Consumer payoff required: each page answers "why should the person paying care".
5. No insinuation without a paper trail.

## Repo layout

```
data/*.csv          single source of truth (regulators, consultations, interests, doors, rti_log)
content/rti-templates/   RTI drafts (markdown)
scripts/build.py    regenerates all HTML + duckdb + llms.txt + sitemap + robots + og.png
tests/check_data.py offline data QA (schema, enums, date sanity, as_of coverage)
tests/verify_urls.py  live check: every source URL in the CSVs must return 200
tests/test_live.py  post-deploy smoke test (--base to retarget)
.github/workflows/  Pages deploy (push to main)
```

## Rebuild

```bash
python3 scripts/build.py       # all pages + data artifacts
python3 tests/check_data.py    # offline QA
python3 tests/verify_urls.py   # every source link resolves
```

Deploy = push to `main` (GitHub Actions → Pages). Custom domain `lobbywatch.cashlessconsumer.in` via CNAME.

## License

Data: **CC BY 4.0** — copy, remix and republish with attribution to LobbyWatch / CashlessConsumer. Code: MIT.

An independent [CashlessConsumer](https://cashlessconsumer.in) project. Not affiliated with any regulator, association or company.
