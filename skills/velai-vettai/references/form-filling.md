# Form filling rules

## Source order for every field
1. `profile.json` (including `answers`)
2. Master resume / tailored resume
3. Ask the user, then save to `profile.json` `answers`

## Never guess
Notice period, CTC, expected salary, work authorization / visa / sponsorship, years of experience, relocation, criminal record, background-check consent, non-compete, referral names, security clearance.

## Safe neutral choices (fine without asking)
- "How did you hear about us?": Job board / LinkedIn / Other
- Optional marketing consent: unchecked
- EEO / diversity questions: "Prefer not to say" / "Decline to answer" unless the user stored an answer
- Preferred contact method: Email

## Mismatch check (before leaving each page)
Compare typed values to the resume: employers, titles, dates, education, total experience, current CTC. If the form auto-parsed the resume wrongly, fix it to match the resume and note the correction in `comments`.

## Account creation
Base email from the profile (plus-addressing allowed), unique password per site from `scripts/gen_password.py`. Show the password once for the user's password manager. For email verification links, ask the user to confirm unless a mail tool is connected.

## Stop point
Navigate to the final review/summary page. Do not click Submit. Leave the tab open and log `Ready to submit`.

## ATS quirks
Workday: account per employer, multi-page, re-enter history if parsing fails. Greenhouse/Lever/Ashby: usually one page, upload resume first. SmartRecruiters / iCIMS: may require an account. For unfamiliar fields read the label and helper text first.
