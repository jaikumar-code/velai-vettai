#!/usr/bin/env python3
"""Health check: python, playwright, data files, profile completeness, CSV integrity."""
import csv, json, os, shutil, sys
from pathlib import Path

HOME = Path(os.environ.get("VELAI_HOME", Path.home() / ".velai-vettai"))
ok = lambda m: print("OK   ", m)
bad = lambda m: print("FIX  ", m)

ok(f"python {sys.version.split()[0]}") if sys.version_info >= (3, 9) else bad("need Python 3.9+")
try:
    import playwright  # noqa
    ok("python playwright installed (needed only for make_pdf.py)")
except ImportError:
    bad("pip install playwright && playwright install chromium (for PDF resumes)")
try:
    import gspread  # noqa
    ok("gspread installed (Google Sheet push)")
except ImportError:
    print("INFO  gspread not installed: tracker writes CSV only")
for tool in ["claude", "codex", "npx"]:
    print("INFO ", tool, "found" if shutil.which(tool) else "not found")

prof = HOME / "profile.json"
if not prof.exists():
    bad(f"{prof} missing: run setup")
else:
    d = json.loads(prof.read_text())
    need = ["name", "target_roles", "notice_period", "expected_salary", "work_authorization",
            "total_years_experience", "base_email"]
    miss = [k for k in need if not d.get(k)]
    bad("profile missing: " + ", ".join(miss)) if miss else ok("profile complete")
(ok if (HOME / "cv.md").exists() else bad)(f"{HOME/'cv.md'} master resume")
t = HOME / "applications.csv"
if t.exists():
    rows = list(csv.DictReader(t.open(encoding="utf-8")))
    urls = [r["job_url"] for r in rows]
    dup = len(urls) - len(set(urls))
    bad(f"{dup} duplicate job URLs in tracker") if dup else ok(f"tracker has {len(rows)} rows, no duplicates")
