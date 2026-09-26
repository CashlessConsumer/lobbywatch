#!/usr/bin/env python3
"""Validate every URL in lobbywatch data CSVs: well-formed + reachable (HTTP <= 399 or 999/403 quirks flagged)."""
import csv, re, sys, concurrent.futures, urllib.request, socket
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
URL_RE = re.compile(r"https?://[^\s,]+")
COLS = {"regulators.csv": ["consultations_url", "source_url"],
        "consultations.csv": ["url", "source_url"],
        "doors.csv": ["source_url"],
        "rti_log.csv": []}

def check(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) LobbyWatchVerify/1.0", "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return url, r.status
    except urllib.error.HTTPError as e:
        return url, e.code
    except (urllib.error.URLError, socket.timeout, ConnectionResetError, OSError) as e:
        return url, f"ERR:{type(e).__name__}"

def main():
    urls = {}
    for fn, cols in COLS.items():
        for row in csv.DictReader(open(DATA / fn)):
            for c in cols:
                u = (row.get(c) or "").strip()
                if u:
                    urls.setdefault(u, []).append(f"{fn}:{row['id']}:{c}")
    # dedupe, verify
    uniq = sorted(urls)
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        results = dict(ex.map(check, uniq))
    bad = 0
    for u in uniq:
        st = results[u]
        ok = isinstance(st, int) and st < 400
        flag = "OK " if ok else "BAD"
        print(f"{flag} {st}  {u}  <- {', '.join(urls[u])}")
        if not ok:
            bad += 1
    print(f"\n{len(uniq)} URLs checked, {bad} bad")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
