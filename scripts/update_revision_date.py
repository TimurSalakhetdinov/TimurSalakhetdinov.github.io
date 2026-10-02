"""Stamp today's date (Europe/Berlin) into the homepage revision fields and current-year markers.

Usage:
  python scripts/update_revision_date.py               # revision dates and year
  python scripts/update_revision_date.py --year-only   # only the year markers
  python scripts/update_revision_date.py 2027-01-15    # a fixed date, for testing
"""
import datetime
import re
import sys
from zoneinfo import ZoneInfo

DE_MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
             "August", "September", "Oktober", "November", "Dezember"]

args = sys.argv[1:]
year_only = "--year-only" in args
dates = [a for a in args if not a.startswith("--")]
today = datetime.date.fromisoformat(dates[0]) if dates else datetime.datetime.now(ZoneInfo("Europe/Berlin")).date()
en = f"{today.day} {today.strftime('%B')} {today.year}"
de = f"{today.day}. {DE_MONTHS[today.month - 1]} {today.year}"
year = str(today.year)

# Current-year markers only; project years in the work table stay fixed.
YEAR_RULES = [
    (r'(<div class="mk">Index</div><div class="mv">TS · )\d{4}(</div>)', year),
    (r'(<span>© timur salakhetdinov · )\d{4}(</span>)', year),
]
DATE_RULES = {
    "index.html": [
        (r'(<div class="mk">Last revision</div><div class="mv">)[^<]*(</div>)', en),
        (r'(· last edited )[^<]*(</span>)', en),
    ],
    "de.html": [
        (r'(<div class="mk">Letzte Aktualisierung</div><div class="mv">)[^<]*(</div>)', de),
        (r'(· zuletzt bearbeitet am )[^<]*(</span>)', de),
    ],
}

for path, date_rules in DATE_RULES.items():
    with open(path, encoding="utf-8") as f:
        text = f.read()
    rules = YEAR_RULES + ([] if year_only else date_rules)
    for pattern, value in rules:
        text, n = re.subn(pattern, lambda m: m.group(1) + value + m.group(2), text)
        if n != 1:
            sys.exit(f"{path}: expected one match for {pattern!r}, found {n}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
print(f"Year set to {year}" + ("" if year_only else f"; revision date {en} / {de}"))
