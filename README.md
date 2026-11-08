# வேலை வேட்டை · Velai Vettai

> *Velai Vettai* (வேலை வேட்டை) is Tamil for **"job hunt"**. An open-source skill that hunts jobs for you and leaves the final click to you.

Works in **Claude Code** and **Codex** (and any agent that supports `SKILL.md` skills).

## What it does

1. **Asks first.** Saves your notice period, expected salary, work authorization and years of experience to a JSON file you can edit any time.
2. **Scans** Naukri, LinkedIn, Himalayas, Wellfound and any boards you add, plus company career pages (Greenhouse, Lever, Ashby).
3. **Gates, then scores** each job against your resume. Anything under your threshold (default 75%) is dropped.
4. **Checks freshness** on the employer's career page. Postings older than 5-10 days (your choice) are dropped.
5. **Tailors your resume** per job: reorders and emphasizes your real experience. It never invents roles, and extra skills only go in after you confirm them.
6. **Pre-fills the application** on the career site (registers with your base Gmail and a unique password per site), cross-checks fields against your resume, and **stops at the submit page**. You review and click Submit.
7. **Logs** every job to a CSV and optionally a Google Sheet: serial, role, URL, how far it got, comments.
8. **Runs daily** at a time you pick.

LinkedIn Easy Apply and Naukri direct-apply jobs are only logged (labelled as such). You apply to those yourself.

## Install

```bash
git clone https://github.com/<you>/velai-vettai
cd velai-vettai
./install.sh --claude     # copies to ~/.claude/skills/velai-vettai
./install.sh --codex      # copies to ~/.agents/skills/velai-vettai
```

Codex also reads repo-level skills from `.agents/skills/`. Check your Codex version's docs if your user-level skills folder differs. Restart the tool after installing.

Add the Playwright MCP so the agent can drive a browser:

```bash
claude mcp add playwright -- npx @playwright/mcp@latest
codex mcp add playwright -- npx @playwright/mcp@latest
```

Optional, for PDF resumes and Google Sheets: `pip install playwright gspread && playwright install chromium`.

## Use

```
> setup job search          # first run: your details and answers saved to ~/.velai-vettai/profile.json
> scan                      # find, gate, score, freshness-check; shows a shortlist
> go and apply              # tailor + pre-fill every shortlisted job, stop at submit
> daily run                 # the unattended version of the above
> status                    # tracker view
```

Your data stays in `~/.velai-vettai/` (never in this repo): `profile.json`, `cv.md`, `applications.csv`, `resumes/`.

## Google Sheets

Create a service account, download its JSON key, share your sheet with the service account email, then set `GOOGLE_APPLICATION_CREDENTIALS` and `GOOGLE_SHEET_ID` (or `google_sheet_id` in the profile).

## Daily schedule

Pick a time during setup, then schedule a headless run:

```cron
# every day at 09:00
0 9 * * *  cd ~ && claude -p "Use the velai-vettai skill: daily run"
0 9 * * *  cd ~ && codex exec "Use the velai-vettai skill: daily run"
```

Unattended runs need the browser and file tools pre-approved in your tool's permission settings. They never submit applications; they leave forms ready for you. On Windows use Task Scheduler with the same commands.

## Safety and honesty

- Human in the loop: the agent never clicks the final Submit.
- No invented facts. Unknown required answers are asked, then remembered.
- Passwords are shown once for your password manager and never written to files or the sheet.
- CAPTCHAs, OTP and phone verification are handed to you. The agent does not bypass them.
- Some sites (LinkedIn, Naukri) restrict automation in their terms. Use modest volume and your own account at your own risk.

## Credits

Ideas such as gate filters before scoring, scan-then-evaluate, markdown master CV to ATS PDF, dedup and health checks, and batch workers come from [career-ops](https://github.com/santifer/career-ops) by Santiago Fernández de Valderrama (MIT). This repo is an independent implementation and does not copy its code.

## License

MIT
