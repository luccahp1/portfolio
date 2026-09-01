"""Scrape the public contribution calendar. No token, no GraphQL, no service.

GitHub serves the same calendar fragment the profile page uses at
https://github.com/users/<user>/contributions, as plain public HTML. Parse the
day cells out of it and write profile/data/contributions.json with the raw days
plus the stats the heatmap footer needs.

    python scripts/fetch_contributions.py
    python scripts/fetch_contributions.py --user someone-else
    python scripts/fetch_contributions.py --html saved.html   # offline
"""

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
import profile_config as cfg  # noqa: E402

URL = "https://github.com/users/{user}/contributions"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; profile-art/1.0; +https://github.com/{user})",
    "Accept": "text/html",
    "X-Requested-With": "XMLHttpRequest",
}
COUNT_RE = re.compile(r"([\d,]+)\s+contribution")
TOTAL_RE = re.compile(r"([\d,]+)\s+contributions?\s+in\s+the\s+last\s+year",
                      re.I)


def fetch(user, timeout=30):
    url = URL.format(user=user)
    headers = {k: v.format(user=user) for k, v in HEADERS.items()}
    print(f"fetching {url}")
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r.text


def cell_count(cell, tips):
    """Pull a day's count out of whichever shape GitHub is serving today."""
    if cell.has_attr("data-count"):
        return int(cell["data-count"])
    texts = []
    tip = tips.get(cell.get("id"))
    if tip:
        texts.append(tip)
    if cell.has_attr("aria-label"):
        texts.append(cell["aria-label"])
    sr = cell.find("span", class_="sr-only")
    if sr:
        texts.append(sr.get_text(" ", strip=True))
    texts.append(cell.get_text(" ", strip=True))
    for text in texts:
        if not text:
            continue
        if text.lower().startswith("no contribution"):
            return 0
        m = COUNT_RE.search(text)
        if m:
            return int(m.group(1).replace(",", ""))
    return 0


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    tips = {t["for"]: t.get_text(" ", strip=True)
            for t in soup.find_all("tool-tip") if t.has_attr("for")}

    cells = soup.select("td.ContributionCalendar-day[data-date]")
    if not cells:
        cells = soup.select("[data-date][data-level], rect.ContributionCalendar-day[data-date]")
    if not cells:
        raise SystemExit(
            "no day cells found - GitHub changed the calendar markup. "
            "Save the page with --html and update the selectors in parse().")

    days = []
    for cell in cells:
        level = int(cell.get("data-level", 0) or 0)
        days.append({"date": cell["data-date"],
                     "count": cell_count(cell, tips),
                     "level": level})
    days.sort(key=lambda d: d["date"])
    # A cell can repeat if GitHub ships a duplicated grid; keep the last one.
    seen = {}
    for d in days:
        seen[d["date"]] = d
    return [seen[k] for k in sorted(seen)]


def promote_top_level(days):
    """Give the very best days a level of their own.

    GitHub only emits levels 0-4, and the palette has a sixth, brighter step.
    The busiest sliver of the level-4 days earns it.
    """
    fours = sorted(d["count"] for d in days if d["level"] == 4)
    if len(fours) < 4:
        return
    cut = fours[int(len(fours) * 0.85)]
    floor = max(cut, fours[0] + 1)
    for d in days:
        if d["level"] == 4 and d["count"] >= floor:
            d["level"] = 5


def streaks(days):
    current = longest = run = 0
    for d in days:
        run = run + 1 if d["count"] else 0
        longest = max(longest, run)
    # Today may simply not have happened yet, so it does not break the streak.
    tail = days[:]
    if tail and tail[-1]["count"] == 0:
        tail = tail[:-1]
    for d in reversed(tail):
        if d["count"] == 0:
            break
        current += 1
    return current, longest


def summarise(days, stated_total=None):
    counts = [d["count"] for d in days]
    total = sum(counts)
    active = sum(1 for c in counts if c)
    best = max(days, key=lambda d: d["count"]) if days else {"date": None, "count": 0}
    current, longest = streaks(days)

    months = Counter()
    for d in days:
        months[d["date"][:7]] += d["count"]
    busiest = max(months.items(), key=lambda kv: kv[1]) if months else ("", 0)

    return {
        "user": None,  # filled in by main()
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"from": days[0]["date"] if days else None,
                  "to": days[-1]["date"] if days else None},
        "total": total,
        "stated_total": stated_total,
        "days_tracked": len(days),
        "days_active": active,
        "average": round(total / len(days), 2) if days else 0,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
        "busiest_month": {"month": busiest[0], "count": busiest[1]},
        "months": dict(sorted(months.items())),
        "days": days,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--user", default=cfg.USERNAME)
    ap.add_argument("--html", help="parse a saved page instead of fetching")
    args = ap.parse_args()

    html = Path(args.html).read_text(encoding="utf-8") if args.html \
        else fetch(args.user)

    days = parse(html)
    promote_top_level(days)

    # GitHub prints its own headline total on the page. Keep it so a drift
    # between it and our sum is visible rather than silently ours.
    stated = None
    m = TOTAL_RE.search(BeautifulSoup(html, "html.parser")
                        .get_text(" ", strip=True))
    if m:
        stated = int(m.group(1).replace(",", ""))

    data = summarise(days, stated)
    data["user"] = args.user

    cfg.CONTRIB_JSON.parent.mkdir(parents=True, exist_ok=True)
    cfg.CONTRIB_JSON.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {cfg.CONTRIB_JSON.relative_to(cfg.ROOT)}: "
          f"{data['total']:,} contributions across {data['days_tracked']} days, "
          f"streak {data['current_streak']} (best {data['longest_streak']})")


if __name__ == "__main__":
    main()
