#!/usr/bin/env python3
"""Post-deploy smoke test for LobbyWatch.

Default target: https://lobbywatch.cashlessconsumer.in
  python3 tests/test_live.py [--base URL]...
Fallback shape (GH Pages path deploy):
  python3 tests/test_live.py --base https://cashlessconsumer.github.io/lobbywatch
"""
import argparse, sys, urllib.request, urllib.error

PAGES = {
    "index.html": ["Who buys the rules", "Comment-transparency scorecard",
                   "The sousveillance stack", "you are here", "Reserve Bank of India"],
    "consultations.html": ["consultation ledger", "Comments published?", "Recalibrating Economics of Insurance Distribution"],
    "interests.html": ["interests register", "Payments Council of India", "SRO layer (SROTrac)"],
    "doors.html": ["revolving-door ledger", "R. Gandhi", "U.K. Sinha", "H.R. Khan"],
    "access.html": ["RTI playbook", "comments-disclosure", "meeting-minutes"],
    "about.html": ["methodology", "Consumer payoff required", "sousveillance"],
    "llms.txt": ["LobbyWatch"],
    "sitemap.xml": ["lobbywatch.cashlessconsumer.in"],
    "robots.txt": ["Sitemap"],
}

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "lobbywatch-smoke/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read().decode("utf-8", "ignore")

def run(base):
    base = base.rstrip("/")
    failures = []
    for page, needles in PAGES.items():
        url = f"{base}/{page}"
        try:
            status, body = fetch(url)
        except (urllib.error.URLError, OSError) as e:
            failures.append(f"{url}: fetch failed ({e})")
            continue
        if status != 200:
            failures.append(f"{url}: HTTP {status}")
            continue
        low = body.lower()
        for n in needles:
            if n.lower() not in low:
                failures.append(f"{url}: missing marker {n!r}")
    return failures

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", action="append", default=[],
                    help="base URL to test (repeatable); default: custom domain then GH Pages fallback")
    args = ap.parse_args()
    bases = args.base or ["https://lobbywatch.cashlessconsumer.in",
                          "https://cashlessconsumer.github.io/lobbywatch"]
    all_fail = []
    for b in bases:
        fails = run(b)
        print(f"== {b}: {'PASS' if not fails else f'{len(fails)} failure(s)'}")
        for f in fails:
            print("  -", f)
        all_fail += [f"[{b}] {f}" for f in fails]
    if all_fail:
        print(f"FAIL — {len(all_fail)} problem(s)")
        sys.exit(1)
    print("ALL PASS")

if __name__ == "__main__":
    main()
