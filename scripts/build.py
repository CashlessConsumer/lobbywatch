#!/usr/bin/env python3
"""Build LobbyWatch — layer 3 (rule-buyers) of the sousveillance stack.

Single source of truth: data/*.csv -> all HTML pages, data/lobbywatch.duckdb,
llms.txt / llms-full.txt, sitemap.xml, robots.txt, og.png.
Design language: shared gazette/ledger skin (SROTrac is the reference; css/style.css).
Run: python3 scripts/build.py
"""
import csv
import html
import json
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
BASE = "https://lobbywatch.cashlessconsumer.in"
BRAND = "LobbyWatch"
TAGLINE = "A CashlessConsumer Register"
GITHUB = "https://github.com/CashlessConsumer/lobbywatch"

GENERIC_DESC = ("Independent register of the interests that buy influence over India's "
                "financial rules: consultation records, meeting access and the revolving "
                "door between regulators and the regulated. Layer 3 (rule-buyers) of the "
                "sousveillance stack, by CashlessConsumer.")

NAV = [
    ("index.html", "Home"),
    ("consultations.html", "Consultations"),
    ("interests.html", "Interests"),
    ("doors.html", "Revolving Doors"),
    ("access.html", "Access & RTI"),
    ("blog/index.html", "Blog"),
    ("about.html", "About"),
]


def esc(s):
    return html.escape(str(s or ""), quote=True)


def read_csv(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fmt_date(d):
    d = (d or "").strip()
    if not d:
        return ""
    for fmt in ("%Y-%m", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(d, fmt)
            return dt.strftime("%b %Y") if fmt == "%Y-%m" else dt.strftime("%d %b %Y")
        except ValueError:
            continue
    return d


def page(title, active, body, desc=None, extra_head=""):
    v = time.strftime("%Y%m%d%H%M")
    nav = ""
    for href, label in NAV:
        cls = ' class="active"' if href == active else ""
        nav += f'<a href="/{href}"{cls}>{label}</a>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — {BRAND}</title>
<meta name="description" content="{esc(desc or GENERIC_DESC)}">
<link rel="canonical" href="{BASE}/{active}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)} — {BRAND}">
<meta property="og:description" content="{esc(desc or GENERIC_DESC)}">
<meta property="og:url" content="{BASE}/{active}">
<meta property="og:image" content="{BASE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ededf0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=Newsreader:ital,opsz,wght@0,6..72,300..700;1,6..72,300..700&family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;1,400&display=swap">
<link rel="icon" href='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="%231d4ed8"/><text x="32" y="46" font-family="Georgia,serif" font-size="38" font-weight="bold" text-anchor="middle" fill="%23faf9f7">L</text></svg>'>
<link rel="stylesheet" href="/css/style.css?v={v}">
{extra_head}
</head>
<body>
<header class="site-header">
  <div class="wrap mast-main">
    <a class="brand" href="/">Lobby<em>Watch</em><small>{TAGLINE}</small></a>
    <nav>{nav}</nav>
  </div>
</header>
<main>
{body}
</main>
<section class="stack" aria-label="The sousveillance stack">
  <div class="wrap">
    <p class="stack-kicker"><b>The Sousveillance Stack</b> — who writes, borrows and buys the rules</p>
    <div class="stack-row">
      <a href="https://regtrac.cashlessconsumer.in/"><i>Layer 1 · rule-writers</i><b>RegTrac</b><span>India's statutory financial regulators</span><em>live</em></a>
      <a href="https://srotrac.cashlessconsumer.in/"><i>Layer 2 · rule-borrowers</i><b>SROTrac</b><span>India's financial-sector self-regulatory organisations</span><em>live</em></a>
      <a href="/"><i>Layer 3 · rule-buyers</i><b>LobbyWatch</b><span>consultations, access, revolving doors</span><em class="here">you are here</em></a>
    </div>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap">
    <p><strong>{BRAND}</strong> — an independent CashlessConsumer project tracking who buys influence over India's financial rules: consultation records, meeting access and revolving doors. Not affiliated with any regulator, association or company; every claim is sourced per entry.</p>
    <p class="colophon">Layer 3 of the sousveillance stack: <a href="https://regtrac.cashlessconsumer.in/">RegTrac</a> (rule-writers) · <a href="https://srotrac.cashlessconsumer.in/">SROTrac</a> (rule-borrowers) · LobbyWatch (rule-buyers).</p>
    <p><a href="https://cashlessconsumer.in">cashlessconsumer.in</a> · data &amp; code: <a href="{GITHUB}">GitHub</a> · <a href="/about.html">methodology</a> · <a href="/llms.txt">llms.txt</a></p>
    <p><strong>Data: CC BY 4.0</strong> — copy, remix and republish with attribution to LobbyWatch / CashlessConsumer. Code: MIT.</p>
    <p class="colophon">No insinuation without a paper trail — access and influence are documented through published comments, RTI replies, minutes and appointment orders, not vibes.</p>
  </div>
</footer>
<script src="/js/main.js?v={v}"></script>
</body>
</html>"""


CLASS_LABEL = {
    "industry-body": "Industry bodies",
    "sro-layer": "SROTrac layer (rule-borrowers — rosters live there)",
    "think-tank": "Think tanks & policy shops",
    "consumer-side": "Consumer & research side",
    "foreign-lobby": "Foreign lobbies",
}
CLASS_ORDER = ["industry-body", "foreign-lobby", "think-tank", "consumer-side", "sro-layer"]


def stance_pill(v):
    v = (v or "").strip().lower()
    if v == "yes":
        return '<span class="badge" style="--c:#166534">yes</span>'
    if v == "no":
        return '<span class="badge" style="--c:#b91c1c">no</span>'
    if v == "partial":
        return '<span class="badge" style="--c:#92400e">partial</span>'
    return '<span class="badge" style="--c:#57534e">unknown</span>'


def build_home(regs, consults, interests, doors):
    live = [c for c in consults if (c["status"] or "").lower() == "live"]
    yes = sum(1 for r in regs if (r["publishes_comments"] or "").strip().lower() == "yes")
    body = f"""<section class="hero"><div class="wrap">
  <p class="kicker">Layer 3 · rule-buyers · the sousveillance stack</p>
  <h1>Who buys the rules of Indian finance?</h1>
  <p class="lede">Regulators write the rules; <strong>RegTrac</strong> watches the writers.
  SROs borrow them; <strong>SROTrac</strong> watches the borrowers. This register watches
  the <strong>buyers</strong>: the interests that flood consultations, get the meetings,
  and hire the regulators after retirement. Access and influence are documented through
  published comments, RTI replies, minutes and appointment orders — not vibes.</p>
  <span class="stamp">watching the watchers, room three</span>
  <div class="stats">
    <div><strong>{len(regs)}</strong><span>consultation desks</span></div>
    <div><strong>{len(consults)}</strong><span>consultations tracked</span></div>
    <div><strong>{len(live)}</strong><span>open for comments</span></div>
    <div><strong>{len(interests)}</strong><span>interests registered</span></div>
    <div><strong>{len(doors)}</strong><span>documented door moves</span></div>
  </div>
</div></section>
<div class="wrap">
<h2 id="scorecard">Comment-transparency scorecard</h2>
<p>The first test of a captured consultation is whether anyone can see what was said to
the rule-writer. Stance per desk, as verified on the regulator's own site.</p>
<table class="listing">
<thead><tr><th>Desk</th><th>Statute</th><th>Publishes comments?</th><th>Documented practice</th><th></th></tr></thead>
<tbody>"""
    for r in sorted(regs, key=lambda r: r["id"]):
        body += f"""<tr>
<td><a href="{esc(r["source_url"])}">{esc(r["name"])}</a></td>
<td>{esc(r["statute"])}</td>
<td>{stance_pill(r["publishes_comments"])}</td>
<td>{esc(r["stance_note"])}</td>
<td class="linkcell"><a href="{esc(r["source_url"])}">source</a></td>
</tr>"""
    body += "</tbody></table>"
    body += """<div class="callout"><p><strong>Why the person paying should care:</strong>
when comments are secret, you cannot tell whether a rule was rewritten for the industry
that asked — or tested against the public that pays. RBI's 2022 Charges-in-Payment-Systems
paper drew submissions from every major industry body; none were published, and the
commenters had to self-publish. A rule made in a closed room still lands on your bill.</p></div>"""

    body += "<h2 id=\"live\">Live consultations</h2>"
    if live:
        body += '<ul class="feed">'
        for c in sorted(live, key=lambda c: c["closed"] or "", reverse=True):
            body += (f'<li><span class="date">{esc(c["closed"])}</span>'
                     f'<a href="{esc(c["url"])}">{esc(c["title"])}</a>'
                     f'<span class="pill small">{esc(c["regulator"].upper())}</span></li>')
        body += "</ul>"
    else:
        body += "<p class=\"muted\">No open comment windows tracked right now.</p>"
    body += '<p><a class="btn" href="/consultations.html">The full consultation ledger →</a></p>'

    body += "<h2 id=\"doors\">The revolving door, on the record</h2><ul class=\"feed\">"
    for d in sorted(doors, key=lambda d: d["date"] or "", reverse=True)[:6]:
        body += (f'<li><span class="date">{esc(d["date"])}</span>'
                 f'<a href="/doors.html#{esc(d["id"])}">{esc(d["person"])} → {esc(d["new_org"])}</a>'
                 f'<span class="pill small">{esc(d["former_org"])}</span></li>')
    body += ('</ul><p><a class="btn" href="/doors.html">The full door ledger →</a></p>')
    body += "</div>"
    return body


def build_consultations(regs, consults):
    reg_names = {r["id"].upper(): r["name"] for r in regs}
    counts = Counter(c["regulator"] for c in consults)
    body = """<section class="hero slim"><div class="wrap">
<p class="kicker">the consultation ledger</p>
<h1>Every paper, every window, every answer</h1>
<p class="lede">Consultation papers of India's financial regulators — with the one fact
that decides whether a consultation means anything: <strong>were the comments
published?</strong></p>
</div></section><div class="wrap">"""
    body += '<div class="factbar">'
    for rid in sorted(counts):
        body += f'<div><span>{esc(rid)}</span><strong>{counts[rid]}</strong></div>'
    body += "</div>"
    body += """<div class="filters"><input id="mq" type="search" placeholder="filter the ledger…">
<div class="chips" id="chips">
<button class="chip active" data-f="all">all</button>
<button class="chip" data-f="live">live</button>
<button class="chip" data-f="closed">closed</button>
<button class="chip" data-f="pub-yes">comments: yes</button>
<button class="chip" data-f="pub-no">comments: no</button>
<button class="chip" data-f="pub-unknown">comments: unknown</button>
</div></div>"""
    body += """<table class="listing" id="ledger">
<thead><tr><th>Opened</th><th>Closed</th><th>Consultation</th><th>Desk</th><th>Status</th><th>Comments published?</th></tr></thead>
<tbody>"""
    for c in sorted(consults, key=lambda c: (c["opened"] or ""), reverse=True):
        pub = (c["comments_published"] or "").strip().lower()
        pcls = "pub-yes" if pub == "yes" else ("pub-no" if pub == "no" else "pub-unknown")
        body += f"""<tr data-status="{esc((c["status"] or "").lower())}" data-pub="{pcls}">
<td>{esc(fmt_date(c["opened"]))}</td>
<td>{esc(fmt_date(c["closed"]))}</td>
<td><a href="{esc(c["url"])}">{esc(c["title"])}</a>{f'<div class="small muted">{esc(c["outcome_note"])}</div>' if c["outcome_note"] else ''}</td>
<td><span class="pill small">{esc(c["regulator"].upper())}</span></td>
<td>{esc(c["status"])}</td>
<td>{stance_pill(c["comments_published"])} <a class="linkcell" href="{esc(c["source_url"])}">source</a></td>
</tr>"""
    body += "</tbody></table>"
    body += """<div class="callout"><p><strong>How to read this table:</strong>
"unknown" is a finding, not a gap in this register — it means the regulator has not
demonstrated a practice of publishing what it receives. RTI is the fallback route;
see <a href="/access.html">Access &amp; RTI</a> for ready-to-file templates.</p></div>
</div>"""
    return body


def build_interests(interests):
    counts = Counter(i["org_class"] for i in interests)
    body = """<section class="hero slim"><div class="wrap">
<p class="kicker">the interests register</p>
<h1>Who is in the room</h1>
<p class="lede">The organised interests that seek to shape India's financial policy —
industry bodies, think tanks, foreign lobbies, and (for balance) the consumer side.
Every entry is a fact of existence and a public role; positions are recorded only where
documented.</p>
</div></section><div class="wrap"><div class="factbar">"""
    for cls in CLASS_ORDER:
        if cls in counts:
            body += f'<div><span>{esc(CLASS_LABEL[cls])}</span><strong>{counts[cls]}</strong></div>'
    body += "</div>"
    for cls in CLASS_ORDER:
        rows = [i for i in interests if i["org_class"] == cls]
        if not rows:
            continue
        body += f"<h2>{esc(CLASS_LABEL[cls])}</h2><table class=\"listing\"><thead><tr><th>Interest</th><th>Sector</th><th>Documented role</th><th></th></tr></thead><tbody>"
        for i in sorted(rows, key=lambda r: r["name"]):
            link = ""
            if i["layer_link"]:
                link = f'<div class="small"><a href="{esc(i["layer_link"])}">SROTrac dossier →</a></div>'
            body += f"""<tr id="{esc(i["id"])}">
<td><strong>{esc(i["name"])}</strong></td>
<td>{esc(i["sector"])}</td>
<td>{esc(i["role"])}{link}</td>
<td class="linkcell"><a href="{esc(i["url"])}">site</a> · <a href="{esc(i["source_url"])}">source</a></td>
</tr>"""
        body += "</tbody></table>"
    body += """<div class="callout"><p><strong>Layer discipline:</strong> RBI-recognised
SROs keep their rosters in <a href="https://srotrac.cashlessconsumer.in/">SROTrac</a>
(rule-borrowers). They appear here only as layer links — the same institutions also
lobby directly, which is exactly why the two layers are cross-referenced.</p></div>
</div>"""
    return body


def build_doors(doors):
    by_person = {}
    for d in doors:
        by_person.setdefault(d["person"], []).append(d)
    body = """<section class="hero slim"><div class="wrap">
<p class="kicker">the revolving-door ledger</p>
<h1>From the regulator's chair to the board's</h1>
<p class="lede">Documented post-office moves of financial regulators into the boards of
the entities they regulated — and the bodies that set their industry's codes. Every row
is an appointment order, an exchange filing or a credible press record. Where an
appointment required the former employer's approval, that fact is stated.</p>
</div></section><div class="wrap">"""
    for person, rows in sorted(by_person.items(), key=lambda kv: -len(kv[1])):
        former = rows[0]["former_office"]
        body += f'<h2 id="{esc(rows[0]["id"])}">{esc(person)}</h2>'
        body += f'<p class="muted">Former office: {esc(former)}</p>'
        body += '<table class="listing"><thead><tr><th>Date</th><th>Move</th><th>On the record</th><th>Why the person paying cares</th></tr></thead><tbody>'
        for d in sorted(rows, key=lambda r: r["date"] or "", reverse=True):
            note = f'<div class="small muted">{esc(d["appointer_note"])}</div>' if d["appointer_note"] else ""
            body += f"""<tr id="{esc(d["id"])}">
<td>{esc(fmt_date(d["date"]))}</td>
<td><strong>{esc(d["new_role"])}</strong>, {esc(d["new_org"])}{note}</td>
<td><a href="{esc(d["source_url"])}">record</a></td>
<td>{esc(d["why_consumer_care"])}</td>
</tr>"""
        body += "</tbody></table>"
    body += """<div class="callout"><p><strong>What this ledger is not:</strong> it is not
an accusation of wrongdoing, and no row implies a quid pro quo. It is the factual
substrate for the capture question: who moved, when, to whom, with whose approval.
Interpret it; don't outsouce interpretation to us.</p></div>
</div>"""
    return body


def build_access(rti_rows):
    t1 = (ROOT / "content" / "rti-templates" / "comments-disclosure.md").read_text(encoding="utf-8")
    t2 = (ROOT / "content" / "rti-templates" / "meeting-minutes.md").read_text(encoding="utf-8")

    def block(md):
        out, in_ul = [], False
        for ln in md.splitlines():
            s = ln.strip()
            if s.startswith("# "):
                if in_ul:
                    out.append("</ul>")
                    in_ul = False
                out.append(f"<h2>{esc(s[2:])}</h2>")
            elif s.startswith("- "):
                if not in_ul:
                    out.append("<ul class=\"watchlist\">")
                    in_ul = True
                out.append(f"<li>{esc(s[2:])}</li>")
            elif s.startswith("> "):
                out.append(f"<p><em>{esc(s[2:])}</em></p>")
            elif s.startswith("SUBJECT:"):
                out.append(f"<p><strong>Subject:</strong> {esc(s[8:].strip())}</p>")
            elif s:
                out.append(f"<p>{esc(s)}</p>")
        if in_ul:
            out.append("</ul>")
        return "\n".join(out)

    body = """<section class="hero slim"><div class="wrap">
<p class="kicker">access & RTI</p>
<h1>Ask what they won't publish</h1>
<p class="lede">Where a regulator does not publish consultation comments or minutes,
the Right to Information Act is the fallback. These are ready-to-file templates and the
running log of what this desk has asked and received. File at
<a href="https://rtionline.gov.in" rel="noopener">rtionline.gov.in</a> (₹10; first copy
of pages free).</p>
</div></section><div class="wrap">"""
    body += "<h2>Template 1 — comments on a consultation</h2>" + block(t1)
    body += "<h2>Template 2 — committee minutes</h2>" + block(t2)
    body += "<h2>Filed by this desk</h2>"
    body += '<table class="listing"><thead><tr><th>Filed</th><th>Authority</th><th>Subject</th><th>Status</th><th>Outcome</th></tr></thead><tbody>'
    for r in rti_rows:
        body += (f'<tr><td>{esc(fmt_date(r["filed_date"]))}</td><td>{esc(r["authority"])}</td>'
                 f'<td>{esc(r["subject"])}</td><td>{esc(r["status"])}</td><td>{esc(r["outcome"])}</td></tr>')
    body += "</tbody></table>"
    body += """<div class="callout"><p><strong>House rule:</strong> this log fills only
with filings actually made. A template waiting to be filed is marked as such — we don't
claim RTI victories we haven't fought.</p></div>
</div>"""
    return body


def build_about(regs, consults, interests, doors):
    body = """<section class="hero slim"><div class="wrap">
<p class="kicker">methodology</p>
<h1>About LobbyWatch</h1>
<p class="lede">LobbyWatch is the third layer of India's financial-policy
<strong>sousveillance stack</strong>. Surveillance is watching citizens; sousveillance
is citizens watching back. Room one (rule-writers) is watched by
<a href="https://regtrac.cashlessconsumer.in/">RegTrac</a>; room two (rule-borrowers) by
<a href="https://srotrac.cashlessconsumer.in/">SROTrac</a>; this register watches room
three — the rule-buyers.</p>
</div></section><div class="wrap">
<h2>Ground rules</h2>
<ol class="ticks">
<li><strong>Public data first</strong> — statutes, gazettes, published comments, regulator websites, press of record.</li>
<li><strong>Every claim sourced per row</strong> — with dates. If a figure has no source, it stays out.</li>
<li><strong>"As of" stamped everywhere</strong> — corrections are visible, never silent.</li>
<li><strong>Consumer payoff required</strong> — every page answers "why should the person paying care".</li>
<li><strong>No insinuation without a paper trail</strong> — access and influence are documented through meetings, minutes, comment letters and appointment orders, not vibes.</li>
</ol>
<h2>What is in the register today</h2>
<div class="factbar">
<div><span>consultation desks scored</span><strong>""" + str(len(regs)) + """</strong></div>
<div><span>consultations tracked</span><strong>""" + str(len(consults)) + """</strong></div>
<div><span>interests registered</span><strong>""" + str(len(interests)) + """</strong></div>
<div><span>documented door moves</span><strong>""" + str(len(doors)) + """</strong></div>
</div>
<h2>The roadmap (build order from SOUSVEILLANCE.md)</h2>
<ul class="watchlist">
<li><strong>Done — consultation ledger.</strong> Cross-regulator ledger with the comments-published fact (this release).</li>
<li><strong>Done — interests register.</strong> Industry bodies, think tanks, foreign lobbies, consumer side (this release).</li>
<li><strong>Done — revolving-door ledger.</strong> Sourced post-office appointments (this release).</li>
<li><strong>Done — RTI playbook.</strong> Ready-to-file templates + filing log (this release).</li>
<li><strong>Next — consultation-index scrapers.</strong> Automated refresh of RBI/SEBI/IRDAI/PFRDA/IBBI/IFSCA consultation indexes (formats vary wildly).</li>
<li><strong>Next — comments corpus.</strong> Download published comments at scale; file RTIs for the unpublished ones.</li>
<li><strong>Then — the diff engine.</strong> Draft clause → final clause → which commenter's language appears in the rule.</li>
</ul>
<h2>How the layers join</h2>
<div class="cols">
<div>
<h3>RegTrac ↔ LobbyWatch</h3>
<p>Appointment authorities (Appointments Committee of the Cabinet; Financial Sector
Regulatory Appointments Search Committee) are RegTrac rows. The revolving door lands
people from this layer into room one.</p>
</div>
<div>
<h3>SROTrac ↔ LobbyWatch</h3>
<p>SRO members are the same institutions that flood consultation processes. A rule that
survives consultation unchanged toward industry comments is a LobbyWatch finding; the
membership that wanted it is a SROTrac fact.</p>
</div>
</div>
<h2>Data & code</h2>
<p>Everything is CSV-first in the open repo (<a href=\"""" + GITHUB + """\">GitHub</a>);
HTML is generated from the CSVs. Data licensed <strong>CC BY 4.0</strong> (attribute
"LobbyWatch / CashlessConsumer"); code MIT. Agent entry point:
<a href="/llms.txt">llms.txt</a>.</p>
</div>"""
    return body


def write_duckdb(regs, consults, interests, doors, rti_rows):
    import duckdb
    out = DATA / "lobbywatch.duckdb"
    if out.exists():
        out.unlink()
    con = duckdb.connect(str(out))
    for table, rows in (
        ("regulators", regs), ("consultations", consults), ("interests", interests),
        ("doors", doors), ("rti_log", rti_rows),
    ):
        if not rows:
            continue
        cols = list(rows[0].keys())
        collist = ", ".join(f'"{c}" VARCHAR' for c in cols)
        con.execute(f"CREATE TABLE {table} ({collist})")
        ph = ", ".join(["?"] * len(cols))
        con.executemany(f"INSERT INTO {table} VALUES ({ph})",
                        [tuple(r[c] for c in cols) for r in rows])
    con.close()
    return out


def strip_html(h):
    import re
    h = re.sub(r"<script.*?</script>", "", h, flags=re.S)
    h = re.sub(r"<style.*?</style>", "", h, flags=re.S)
    h = re.sub(r"<[^>]+>", " ", h)
    h = html.unescape(h)
    h = re.sub(r"[ \t]+", " ", h)
    return re.sub(r"\n\s*\n+", "\n\n", h).strip()


def write_agent_files(pages, stats):
    built = time.strftime("%Y-%m-%d %H:%M UTC")
    llms = f"""# LobbyWatch — the rule-buyers of Indian finance, watched

> Independent register of the interests that buy influence over India's financial rules:
> a comment-transparency scorecard for the six statutory consultation desks (RBI, SEBI,
> IRDAI, IBBI, PFRDA, IFSCA), a consultation ledger (were comments published?), an
> interests register (industry bodies, think tanks, foreign lobbies, consumer side), a
> sourced revolving-door ledger, and an RTI playbook with ready-to-file templates.
> Layer 3 (rule-buyers) of the sousveillance stack — RegTrac (rule-writers) and SROTrac
> (rule-borrowers) are layers 1 and 2. Run by CashlessConsumer. Data CC BY 4.0.

Base URL: {BASE}

## Pages
- [Home]({BASE}/index.html): comment-transparency scorecard per desk, live consultations, latest door moves.
- [Consultations]({BASE}/consultations.html): the consultation ledger — opened, closed, status, and whether comments were published.
- [Interests]({BASE}/interests.html): the interests register — industry bodies, foreign lobbies, think tanks, consumer side, SROTrac layer links.
- [Revolving Doors]({BASE}/doors.html): documented post-regulator appointments, per person, each with a record link.
- [Access & RTI]({BASE}/access.html): ready-to-file RTI templates for unpublished comments and committee minutes + the filing log.
- [About]({BASE}/about.html): ground rules, roadmap (index scrapers → comments corpus → clause-diff engine), how the stack joins.

## Quick facts
- Consultation desks tracked: {stats['regs']}
- Consultations tracked: {stats['consults']}
- Interests registered: {stats['interests']}
- Documented door moves: {stats['doors']}

## House rule
No insinuation without a paper trail — access and influence are documented through
published comments, RTI replies, minutes and appointment orders, not vibes.

Built {built}.
"""
    (ROOT / "llms.txt").write_text(llms, encoding="utf-8")
    full = [llms]
    for fname, htmltext in pages:
        full.append(f"\n\n## {fname}\n\n{strip_html(htmltext)}")
    (ROOT / "llms-full.txt").write_text("".join(full), encoding="utf-8")

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    today = time.strftime("%Y-%m-%d")
    for fname, _ in pages:
        sitemap.append(f"<url><loc>{BASE}/{fname}</loc><lastmod>{today}</lastmod></url>")
    blog_dir = ROOT / "blog"
    if blog_dir.is_dir():
        for bp in sorted(blog_dir.glob("*.html")):
            sitemap.append(f"<url><loc>{BASE}/blog/{bp.name}</loc><lastmod>{today}</lastmod></url>")
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")

    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        "User-agent: GPTBot\nAllow: /\n\n"
        "User-agent: OAI-SearchBot\nAllow: /\n\n"
        "User-agent: ChatGPT-User\nAllow: /\n\n"
        "User-agent: ClaudeBot\nAllow: /\n\n"
        "User-agent: anthropic-ai\nAllow: /\n\n"
        "User-agent: PerplexityBot\nAllow: /\n\n"
        "User-agent: Google-Extended\nAllow: /\n\n"
        "User-agent: CCBot\nAllow: /\n\n"
        "Sitemap: " + BASE + "/sitemap.xml\n", encoding="utf-8")


def write_og():
    from PIL import Image, ImageDraw, ImageFont
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), "#ededf0")
    d = ImageDraw.Draw(img)
    for y in range(0, H, 32):
        d.line([(0, y), (W, y)], fill="#e4e5e9", width=1)
    d.rectangle([0, 0, W, 14], fill="#1d4ed8")
    d.rectangle([0, H - 90, W, H], fill="#1d4ed8")
    f_xl = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 84)
    f_l = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 40)
    f_s = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 24)
    d.text((80, 96), "LobbyWatch", font=f_xl, fill="#191b20")
    d.text((84, 210), "Who buys the rules of Indian finance?", font=f_l, fill="#41454e")
    d.text((84, 300), "LAYER 3 · RULE-BUYERS · THE SOUSVEILLANCE STACK", font=f_s, fill="#1d4ed8")
    d.text((84, 350), "RegTrac watches rule-writers  ·  SROTrac watches rule-borrowers", font=f_s, fill="#6f747f")
    d.text((84, 392), "LobbyWatch watches: consultations · access · revolving doors", font=f_s, fill="#6f747f")
    d.text((84, H - 62), "lobbywatch.cashlessconsumer.in  ·  A CashlessConsumer register  ·  CC BY 4.0",
           font=f_s, fill="#f8f8fa")
    img.save(ROOT / "og.png")


def main():
    regs = read_csv("regulators.csv")
    consults = read_csv("consultations.csv")
    interests = read_csv("interests.csv")
    doors = read_csv("doors.csv")
    rti_rows = read_csv("rti_log.csv")

    pages = [
        ("index.html", build_home(regs, consults, interests, doors)),
        ("consultations.html", build_consultations(regs, consults)),
        ("interests.html", build_interests(interests)),
        ("doors.html", build_doors(doors)),
        ("access.html", build_access(rti_rows)),
        ("about.html", build_about(regs, consults, interests, doors)),
    ]
    for fname, body in pages:
        title = {
            "index.html": "Home",
            "consultations.html": "Consultations",
            "interests.html": "Interests",
            "doors.html": "Revolving Doors",
            "access.html": "Access & RTI",
            "about.html": "About",
        }[fname]
        (ROOT / fname).write_text(
            page(title, fname, body), encoding="utf-8")

    write_agent_files(pages, {
        "regs": len(regs), "consults": len(consults),
        "interests": len(interests), "doors": len(doors),
    })
    write_og()
    db = write_duckdb(regs, consults, interests, doors, rti_rows)
    print(f"built {len(pages)} pages -> {BASE}")
    print(f"duckdb: {db}")
    print(f"consultations={len(consults)} interests={len(interests)} doors={len(doors)} built {time.strftime('%Y-%m-%d %H:%M UTC')}")


if __name__ == "__main__":
    main()
