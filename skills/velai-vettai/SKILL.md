---
name: velai-vettai
description: Automates the job hunt (வேலை வேட்டை) end to end. Use whenever the user wants to find jobs, scan job boards or company career pages (Naukri, LinkedIn, Himalayas, Wellfound, Greenhouse, Lever, Ashby), score jobs against their resume, tailor an ATS resume per job, pre-fill applications on career sites, track applications in a Google Sheet or CSV, or run a daily job search. Triggers include "setup job search", "find me jobs", "go and apply", "run my daily job hunt", "tailor my resume for these jobs". It fills applications up to the submit page; the user always reviews and clicks Submit.
compatibility: Needs a browser tool (Playwright MCP recommended) and Python 3.9+. Works in Claude Code and Codex.
---

# Velai Vettai (வேலை வேட்டை, "job hunt")

Automate the analysis, not the decision. Find fresh, well-matched jobs, tailor the resume, pre-fill applications on the employer's own career site, log everything, and stop at the submit page. **The user reviews and clicks Submit. Never click the final Submit/Apply button.**

Data lives in `~/.velai-vettai/` (override with `VELAI_HOME`): `profile.json`, `cv.md` (master resume), `applications.csv`, `resumes/`, `portals.yml`. Scripts are in `scripts/` next to this file. Run `python scripts/doctor.py` if anything seems broken.

## Hard rules

1. Never invent facts: roles, employers, degrees, dates, or answers to eligibility questions.
2. Never click the final submit.
3. Never write passwords to the sheet, CSV, chat, or files. Show a new password to the user once for their password manager.
4. Do not solve CAPTCHAs, bypass bot detection, or work around OTP/phone verification. Hand that step to the user.
5. LinkedIn Easy Apply and Naukri direct apply are done manually by the user. Log them only.

## Step 0: Setup (always first)

Run `python scripts/doctor.py`. If `profile.json` is missing, copy `assets/profile.template.json` to `~/.velai-vettai/` and interview the user. **Ask these before anything else**, in one short batch:

- Name, phone, location, relocation / remote-only
- Target roles, locations, minimum match % (default 75), max posting age in days (default 7, allowed 5-10)
- Notice period, current CTC, expected salary, work authorization, total years of experience
- Resume file; convert it to `cv.md` (markdown master) and confirm it with the user
- Job boards to use (defaults in `references/boards.md`) and optional target companies for `portals.yml`
- Daily run time, optional Google Sheet ID (CSV is always written)
- The base Gmail the user created for this search (the user creates it; you cannot pass verification)

Save every answer to `profile.json`. Tell the user they can edit it any time. Later runs only ask for what is missing.

## Step 1: Scan (wide net)

For each target role and board, search and collect title, company, location, posted date, URL. Also scan companies in `portals.yml` via their public ATS pages (see `references/boards.md`). Use separate browser tabs per board. Dedupe with `python scripts/tracker.py seen <url>`; skip jobs already logged. Scan does not do deep evaluation.

## Step 2: Gate, then score (deep dive)

First apply the **gates** in `references/evaluation.md` (title match, location/work mode, seniority, must-have skills, posting age). Anything failing a gate is dropped with a one-line reason. Then score survivors 0-100 with the rubric there, by reasoning about the resume against the job description, not keyword counting. Drop anything below the user's minimum. For 10+ survivors, evaluate in parallel with independent sub-agents or `claude -p` / `codex exec` workers, one job each, and merge results.

## Step 3: Resolve the apply path

Click Apply and classify:

- Redirects to the employer or ATS career site: continue.
- LinkedIn Easy Apply: log `apply_type="LinkedIn Easy Apply"`, stage `Manual`. Skip.
- Naukri direct apply: log `apply_type="Naukri Direct Apply"`, stage `Manual`. Skip.

## Step 4: Check freshness

Read the posting date on the career page (fall back to the board). Run `python scripts/freshness.py "<date text>" --max-days <N>`. Exit 0 fresh, 1 too old (drop), 2 unknown (log `Date unknown`, do not apply, mention in summary).

## Step 5: Tailor the resume

Per job, edit a copy of `cv.md`, then render with `assets/cv-template.html` and `python scripts/make_pdf.py` to `resumes/<company>_<role>.pdf`. You may reorder sections and bullets, rewrite the summary, and use the job description's wording for experience the user really has. Add industry skills only after the user confirms each one (store in `confirmed_extra_skills`). Never add roles, employers, certifications, or years. Use US Letter or A4 to match the job's region. Never touch the master `cv.md`.

## Step 6: Fill the application

Follow `references/form-filling.md`. In short: register if needed using the base email (plus-addressing ok) and a unique password from `python scripts/gen_password.py`; fill from `profile.json`, then the resume; cross-check every field against the resume; fill every mandatory field; if a value is unknown, ask the user and save it under `answers` (in an unattended run leave it blank and log `Needs input: <field>`); upload the tailored PDF; go to the review page and stop.

## Step 7: Log

For every job, including skipped ones: `python scripts/tracker.py add --help`. Columns: serial, date, account email, role, company, source, apply type, job URL, apply URL, match %, posted age, stage, comments. Stages (normalized by the script): `Shortlisted`, `Manual`, `Too old`, `Registered`, `Form filled`, `Ready to submit`, `Needs input`, `Blocked`, `Applied`, `Interview`, `Rejected`. If a Sheet ID is set, the script also pushes the row.

## Commands

- **setup**: Step 0.
- **scan**: Steps 1-4, present a shortlist table.
- **go and apply**: for each shortlisted job not yet `Ready to submit`, run Steps 5-7 across multiple browser tabs. End with a table of what is ready for review.
- **daily run**: scan, gate, score, freshness, tailor, pre-fill, log. Never submit. Summarize what waits for review.
- **status**: `python scripts/tracker.py list`.
- Optional extras in `references/extras.md`: outreach note, company research, interview story bank, negotiation prep.

## When blocked

CAPTCHA, OTP, phone verification, login walls, rate limits: stop that site, log `Blocked` with the reason, tell the user which tab needs them, continue with other jobs. Default max 15 pre-filled applications per run.
