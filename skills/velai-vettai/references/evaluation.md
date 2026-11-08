# Evaluation: gates, rubric, report

Idea borrowed from career-ops: filter cheaply first, then reason deeply on survivors.

## Gates (fail any = drop, log reason)
1. Title matches one of the user's target roles (or a clear synonym).
2. Location / work mode fits `target_locations`, `remote_only`, `relocate`.
3. Seniority fits (no junior/intern for a senior profile; no VP-level for an IC).
4. Must-have skills: no more than one hard requirement missing from the resume.
5. Posting age within `max_posting_age_days` (confirmed in Step 4).
6. Not already in `applications.csv`.

## Score 0-100 (reason over the resume vs the full JD)
- 40% required skills and tools present
- 25% seniority and years fit
- 15% domain / industry fit
- 10% location and work-mode fit
- 10% title fit

Drop below `min_match_pct`. Keep a one-line reason and the top 3 gaps.

## Short report per shortlisted job (6 blocks, keep each to 1-2 lines)
Role summary; resume match and gaps; level fit; compensation signal if visible (never guess); what to emphasize in the tailored resume; likely interview focus.
