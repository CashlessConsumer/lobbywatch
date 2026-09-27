#!/usr/bin/env bash
# LobbyWatch daily refresh: run data gates, rebuild the register + blog, commit & push on change.
# Designed to be run by the daily automation agent (and safe to run by hand).
# Ported from SROTrac refresh.sh (pipeline parity, 2026-09-27). No fetch step yet:
# the consultation-index scraper is an open item — until it lands, content updates
# land by hand and this script's job is verify → rebuild → deploy.
set -uo pipefail
cd "$(dirname "$0")/.."

python3 tests/check_data.py  || { echo "CHECK_DATA FAIL"; exit 1; }
python3 tests/verify_urls.py || echo "VERIFY_URLS FAIL (non-fatal: known flaky external .gov.in walls)"
python3 scripts/build.py     || exit 1
python3 scripts/bloggen.py   || exit 1

if [ -n "$(git status --porcelain -- data blog *.html css js sitemap.xml llms.txt llms-full.txt)" ]; then
  git add -A
  git -c user.name="LobbyWatch bot" -c user.email="cashlessconsumerin@gmail.com" \
    commit -q -m "Daily refresh $(date -u +%F-%H%M) UTC — gates + rebuild"
  git push -q origin main && echo "PUSHED: changes found and deployed"
else
  echo "NO-CHANGE: ledgers and content unchanged"
fi
echo "REFRESH OK"
