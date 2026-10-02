"""Set the homepage "Last revision" and footer "last edited" dates to today (Europe/Berlin)."""
import datetime
import re
import sys
from zoneinfo import ZoneInfo

DE_MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
             "August", "September", "Oktober", "November", "Dezember"]

today = datetime.datetime.now(ZoneInfo("Europe/Berlin")).date()
if len(sys.argv) > 1:
    today = datetime.date.fromisoformat(sys.argv[1])
en = f"{today.day} {today.strftime('%B')} {today.year}"
de = f"{today.day}. {DE_MONTHS[today.month - 1]} {today.year}"

RULES = {
    "index.html": [
        (r'(<div class="mk">Last revision</div><div class="mv">)[^<]*(</div>)', en),
        (r'(· last edited )[^<]*(</span>)', en),
    ],
    "de.html": [
        (r'(<div class="mk">Letzte Aktualisierung</div><div class="mv">)[^<]*(</div>)', de),
        (r'(· zuletzt bearbeitet am )[^<]*(</span>)', de),
    ],
}

for path, rules in RULES.items():
    with open(path, encoding="utf-8") as f:
        text = f.read()
    for pattern, value in rules:
        text, n = re.subn(pattern, lambda m: m.group(1) + value + m.group(2), text)
        if n != 1:
            sys.exit(f"{path}: expected one match for {pattern!r}, found {n}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
print(f"Revision date set to {en} / {de}")
