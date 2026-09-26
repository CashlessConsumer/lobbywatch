#!/usr/bin/env python3
"""Offline checks for LobbyWatch: CSV integrity + claim-tracing invariants.

Every row in doors.csv, consultations.csv, interests.csv, regulators.csv must carry a
source_url; consultations must resolve regulator ids; interests org_class values must
be known; dates must be ISO-ish. Fails loudly (exit 1) with a row-by-row report.
Run: python3 tests/check_data.py
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
KNOWN_CLASS = {"industry-body", "sro-layer", "think-tank", "consumer-side", "foreign-lobby"}
KNOWN_STATUS = {"live", "closed", "final", "withdrawn"}
ISO = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")

errors = []


def rows(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


regs = rows("regulators.csv")
reg_ids = {r["id"].strip().lower() for r in regs}
if len(reg_ids) != len(regs):
    errors.append("regulators.csv: duplicate ids")

for r in regs:
    if not r["source_url"].startswith("http"):
        errors.append(f"regulators.csv:{r['id']}: source_url missing")
    if r["publishes_comments"].strip().lower() not in {"yes", "no", "partial", "unknown", "proposed"}:
        errors.append(f"regulators.csv:{r['id']}: bad publishes_comments {r['publishes_comments']!r}")

for c in rows("consultations.csv"):
    cid = c["id"]
    if c["regulator"].strip().lower() not in reg_ids:
        errors.append(f"consultations.csv:{cid}: unknown regulator {c['regulator']!r}")
    if not c["url"].startswith("http") or not c["source_url"].startswith("http"):
        errors.append(f"consultations.csv:{cid}: url/source_url missing")
    if c["comments_published"].strip().lower() not in {"yes", "no", "partial", "unknown", "proposed"}:
        errors.append(f"consultations.csv:{cid}: bad comments_published")
    if c["status"].strip().lower() not in KNOWN_STATUS:
        errors.append(f"consultations.csv:{cid}: bad status {c['status']!r}")
    for col in ("opened", "closed"):
        if c[col] and not ISO.match(c[col].strip()):
            errors.append(f"consultations.csv:{cid}: bad {col} {c[col]!r}")

for i in rows("interests.csv"):
    if i["org_class"] not in KNOWN_CLASS:
        errors.append(f"interests.csv:{i['id']}: bad org_class {i['org_class']!r}")
    if not i["url"].startswith("http") or not i["source_url"].startswith("http"):
        errors.append(f"interests.csv:{i['id']}: url/source_url missing")

for d in rows("doors.csv"):
    if not d["source_url"].startswith("http"):
        errors.append(f"doors.csv:{d['id']}: source_url missing")
    if not ISO.match(d["date"].strip()):
        errors.append(f"doors.csv:{d['id']}: bad date {d['date']!r}")
    if not d["why_consumer_care"].strip():
        errors.append(f"doors.csv:{d['id']}: empty why_consumer_care")

if errors:
    print(f"FAIL — {len(errors)} problem(s):")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"OK — regulators={len(regs)} consultations={len(rows('consultations.csv'))} "
      f"interests={len(rows('interests.csv'))} doors={len(rows('doors.csv'))} "
      "rti_log=" + str(len(rows("rti_log.csv"))))
