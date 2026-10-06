# [EDF] RBI FEMA (Export & Import of Goods and Services) Regulations, 2026 — consultation anatomy

**Date:** 2026-10-06 · **Trigger:** https://x.com/nixxin/status/2107361918424076424 (Nikhil Pahwa quoting Arvind Jha on freelancers chasing banks over EDF) · **Stack layers:** rule-writer RBI consulted (unusually, with a published response annex); rule-borrowers (AD banks) inherit the operational rule-making via "internal policy".

## What's in force from 1 Oct 2026

- FEMA (Export and Import of Goods and Services) Regulations, 2026 (FEMA 23(R)/2026-RB, notified 2026-01-13; amendments to 2026-09-22) + Directions (2026-01-16). Supersedes 2015 Regulations + Export/Import Master Directions (2016) + **167 circulars**.
- One Export Declaration Form (EDF) for goods + services + software (SOFTEX folded in; STPI retained alongside AD for non-physical software exports).
- Service exporters: **one consolidated monthly EDF**, due within 30 days of month-end of invoice, **no minimum invoice value** — this is what catches the $5–$50 remote-task freelancers.
- Banks credit only after EDPMS match; proceeds due in 9 months (12 if INR-invoiced); >1 year unpaid → bank may require full advance or irrevocable LC for further exports. Non-filing = FEMA contravention (s.13 penalty up to 3x the sum involved).
- Softeners accepted in consultation: monthly consolidation regardless of invoice values; threshold-based EDPMS/IDPMS marking off (₹10 lakh simplified closure); travellers' personal effects not "exports"; shipping bill alone suffices for goods at EDI ports.

## Consultative process (verified timeline)

| Date | Event |
| --- | --- |
| 2024-07-02 | Draft Regulations 2024 + Draft Directions published; comments via email by **2024-09-01** (RBI PR) |
| 2025-04-04 | Revised draft Regulations 2025 + Directions; comments by **2025-04-30** (KPMG flash note) |
| 2026-01-13 | Final Regulations notified (gazette) |
| 2026-01-16 | Directions issued; PR 1933 with **"Statement on feedback received"** annex (15 items, summarized, **commenter identities not disclosed**) |
| 2026-10-01 | In force |

Evidence: `notes/evidence/2026-10-06-rbi-exim-fema-2026-feedback-annex.pdf` (Wayback capture 2026-01-16 of rbidocs PR193316012026_A.pdf — live rbidocs is CAPTCHA-walled for bots).

## Who won / who lost (annex scorecard)

| Feedback item (annex wording) | Outcome | Probable commenter class (our inference) |
| --- | --- | --- |
| 5-working-day extension for E/IDPMS entry — "ADs had requested" | ✅ Accepted (Reg 18(1)) | AD banks — **only commenter class RBI names explicitly** |
| Retain STPI as specified authority for non-physical software exports | ✅ Accepted (Reg 2(1)(f)) | Software industry / STPI units |
| Define "software" | ✅ Accepted (Reg 2(1)(e)) | Software industry |
| MTT same-AD relaxation + third-party receipts | ✅ Accepted (Reg 16(1)) | Trading houses / merchant exporters |
| Direct-dispatch of documents relaxation | ✅ Clause omitted | Exporters |
| Third-party payments without AD permission | ✅ Accepted (Reg 8) | Exporters/traders |
| Change of AD for advance payments | ✅ Accepted (Reg 10(1),(2)) | Exporters/importers |
| Threshold-based EDPMS/IDPMS marking off | ✅ Accepted (Reg 4(2)) | SME exporters |
| Consolidated service EDF, any invoice value | ✅ Accepted (Reg 3(2)) | Service exporters |
| **EDF waiver continuation / service exports exempt from EDF** | ❌ **Not accepted** — "Section 7 of FEMA makes declaration mandatory… process made flexible" | Service exporters incl. freelancer/platform interests |
| Retain PEM (Project & Service Exports MoU) | ❌ Not accepted — principle-based, ADs' internal policy | Project/service exporters (EPC ecosystem) |
| Fixed import-payment timeline | ❌ Not accepted — "as per the contract" | Importers |

Pattern: organized, banked interests won timing/discretion concessions; the largest-by-headcount unorganized class (micro service exporters) lost the substantive ask and got procedural softeners instead.

## Watchpoints (LobbyWatch angles)

1. **Commenter anonymity:** RBI's annex is better than its usual practice (no disclosure at all), but comments are summarized without names or counts. An RTI could extract commenter identities — candidate for `rti_log.csv` (comments-disclosure template exists in `content/rti-templates/`).
2. **Rule-making delegated to AD bank internal policies** (PEM rejection language): the operational rules freelancers actually face are now unpublished, bank-by-bank policies — a rule-borrowers (SROTrac) watchpoint: no consultation at the layer where the rule bites.
3. **No de minimis:** US customs exempts exports under $2,500 from EEI filing; RBI chose monthly consolidation over a value floor, so a $5 invoice carries the same legal weight as a $5M contract. The design choice (not statute) is what Nikhil Pahwa's critique lands on.
4. **Enforcement asymmetry risk:** s.13 3x penalty headroom against $5 invoices; bank fund-holding until EDPMS match is the real sanction.

## Proposed consultations.csv row (not yet added — needs owner sign-off before live push)

```csv
rbi-exim-fema-2026,rbi,"Regulations + Directions on Export and Import of Goods and Services (unified EDF for goods/services/software; SOFTEX folded in)",2024-07-02,2025-04-30,final,no,https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=62049,https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=62049,"RBI published a 15-item summarized feedback annex (PR 1933) — first for this desk where responses ARE published but commenter identities are not. Rejected asks: EDF waiver continuation, service-export EDF exemption (FEMA s.7 cited), PEM retention. Accepted: monthly consolidated EDF, ₹10L threshold marking-off, STPI retention, AD 5-day EDPMS window. In force 2026-10-01.",2026-10-06
```

Note: verify exact `comments_published` enum against build.py before adding.
