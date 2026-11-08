#!/usr/bin/env python3
"""Application tracker. CSV is the source of truth; optional Google Sheet push.

  tracker.py add --role R --company C --source S --apply-type T --job-url U \
      --stage "Ready to submit" [--apply-url U --match 82 --age 3 --account a@b.com --comments "..."]
  tracker.py seen <url>      exit 0 if already logged, 1 if new
  tracker.py list [--stage STAGE]

Sheet push needs: pip install gspread, env GOOGLE_APPLICATION_CREDENTIALS (service account
JSON) and GOOGLE_SHEET_ID (or profile.json google_sheet_id). Share the sheet with the service account.
"""
import argparse, csv, json, os, sys
from datetime import date
from pathlib import Path

HOME = Path(os.environ.get("VELAI_HOME", Path.home() / ".velai-vettai"))
CSV = HOME / "applications.csv"
COLS = ["serial", "date", "account_email", "role", "company", "source", "apply_type",
        "job_url", "apply_url", "match_pct", "posted_age_days", "stage", "comments"]
STAGES = ["Shortlisted", "Manual", "Too old", "Date unknown", "Registered", "Form filled",
          "Ready to submit", "Needs input", "Blocked", "Applied", "Interview", "Rejected"]


def norm_stage(s):
    for st in STAGES:
        if s.strip().lower() == st.lower():
            return st
    for st in STAGES:
        if s.strip().lower() in st.lower() or st.lower() in s.strip().lower():
            return st
    return s.strip()


def rows():
    if not CSV.exists():
        return []
    with CSV.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def push_sheet(row):
    try:
        import gspread
    except ImportError:
        return "gspread not installed, CSV only"
    sid = os.environ.get("GOOGLE_SHEET_ID")
    prof = HOME / "profile.json"
    if not sid and prof.exists():
        sid = json.loads(prof.read_text()).get("google_sheet_id")
    if not sid or not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        return "no sheet configured, CSV only"
    ws = gspread.service_account().open_by_key(sid).sheet1
    if not ws.get_all_values():
        ws.append_row(COLS)
    ws.append_row([row[c] for c in COLS])
    return "pushed to sheet"


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    for k in ["role", "company", "source", "apply-type", "job-url", "stage"]:
        a.add_argument("--" + k, required=True)
    for k in ["apply-url", "match", "age", "account", "comments"]:
        a.add_argument("--" + k, default="")
    s = sub.add_parser("seen"); s.add_argument("url")
    l = sub.add_parser("list"); l.add_argument("--stage", default=None)
    args = p.parse_args()
    existing = rows()

    if args.cmd == "seen":
        hit = any(args.url in (r["job_url"], r["apply_url"]) for r in existing)
        print("seen" if hit else "new")
        sys.exit(0 if hit else 1)

    if args.cmd == "list":
        for r in existing:
            if args.stage and r["stage"] != args.stage:
                continue
            print(f'{r["serial"]:>3} | {r["stage"]:<15} | {r["match_pct"]:>3}% | {r["company"]} - {r["role"]} | {r["apply_type"]} | {r["job_url"]}')
        return

    key = {args.job_url, args.apply_url} - {""}
    if any(k in (r["job_url"], r["apply_url"]) for r in existing for k in key):
        print("duplicate, not added"); return
    row = {"serial": len(existing) + 1, "date": date.today().isoformat(),
           "account_email": args.account, "role": args.role, "company": args.company,
           "source": args.source, "apply_type": args.apply_type, "job_url": args.job_url,
           "apply_url": args.apply_url, "match_pct": args.match, "posted_age_days": args.age,
           "stage": norm_stage(args.stage), "comments": args.comments}
    HOME.mkdir(parents=True, exist_ok=True)
    new = not CSV.exists()
    with CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        if new:
            w.writeheader()
        w.writerow(row)
    print(f"added #{row['serial']}; {push_sheet(row)}")


if __name__ == "__main__":
    main()
