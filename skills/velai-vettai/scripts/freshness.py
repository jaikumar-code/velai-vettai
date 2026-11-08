#!/usr/bin/env python3
"""Check whether a posting date is within N days.

Usage: freshness.py "Posted 3 days ago" --max-days 7 [--today YYYY-MM-DD]
Exit: 0 fresh, 1 too old, 2 unknown. Prints JSON.
"""
import argparse, json, re, sys
from datetime import date, datetime

UNITS = {"minute": 0, "hour": 0, "day": 1, "week": 7, "month": 30, "year": 365}
FORMATS = ["%Y-%m-%d", "%b %d, %Y", "%B %d, %Y", "%d %b %Y", "%d %B %Y", "%b %d %Y"]


def age_days(text, today):
    t = text.strip().lower()
    if re.search(r"just now|today|few (seconds|minutes|hours)|an? hour|new\b", t):
        return 0
    if "yesterday" in t:
        return 1
    m = re.search(r"(\d+)\+?\s*(minute|hour|day|week|month|year)s?", t)
    if m:
        return int(m.group(1)) * UNITS[m.group(2)]
    m = re.search(r"(\d{4}-\d{2}-\d{2})", t)
    candidates = [m.group(1)] if m else []
    clean = re.sub(r"^(posted|date posted|published)( on)?:?\s*", "", t, flags=re.I)
    candidates.append(re.sub(r"(\d)(st|nd|rd|th)", r"\1", clean).title())
    for c in candidates:
        for f in FORMATS:
            try:
                return (today - datetime.strptime(c, f).date()).days
            except ValueError:
                pass
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("text")
    p.add_argument("--max-days", type=int, default=7)
    p.add_argument("--today", default=None)
    a = p.parse_args()
    today = datetime.strptime(a.today, "%Y-%m-%d").date() if a.today else date.today()
    d = age_days(a.text, today)
    if d is None:
        print(json.dumps({"age_days": None, "fresh": None, "reason": "unknown date format"}))
        sys.exit(2)
    fresh = d <= a.max_days
    print(json.dumps({"age_days": d, "fresh": fresh, "reason": f"{d}d old, limit {a.max_days}d"}))
    sys.exit(0 if fresh else 1)


if __name__ == "__main__":
    main()
